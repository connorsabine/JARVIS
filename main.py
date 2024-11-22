from jarvis import interface, config

from mycroft import MycroftSkill, intent_file_handler
import logging
import openai
import tkinter as tk
import math
import time
import pyaudio
import struct
import pvporcupine
import winsound

class JarvisGUI:
    def __init__(self, root, radius=100, num_latitude=20, num_longitude=30):
        self.root = root
        self.radius = radius
        self.num_latitude = num_latitude
        self.num_longitude = num_longitude
        self.time_start = time.time()

        self.canvas_width = 800
        self.canvas_height = 600
        self.canvas = tk.Canvas(root, width=self.canvas_width, height=self.canvas_height, bg='gray')
        self.canvas.pack()

        self.oscillation_speeds = {
            "latitude": 0.5,
            "longitude": 1.0
        }

        self.points = self.generate_points()
        self.animate()

    def spherical_to_cartesian(self, radius, theta, phi):
        x = radius * math.sin(phi) * math.cos(theta)
        y = radius * math.sin(phi) * math.sin(theta)
        z = radius * math.cos(phi)
        return x, y, z

    def project_to_2d(self, x, y, z, width, height):
        factor = 200 / (z + 5)
        x_proj = x * factor + width / 2
        y_proj = -y * factor + height / 2
        return x_proj, y_proj

    def generate_points(self):
        points = []
        for i in range(self.num_latitude + 1):
            phi = math.pi * i / self.num_latitude
            for j in range(self.num_longitude):
                theta = 2 * math.pi * j / self.num_longitude
                
                x1, y1, z1 = self.spherical_to_cartesian(self.radius, theta, phi)
                x2, y2, z2 = self.spherical_to_cartesian(self.radius, theta + 2 * math.pi / self.num_longitude, phi)
                x3, y3, z3 = self.spherical_to_cartesian(self.radius, theta, phi + math.pi / self.num_latitude)
                x4, y4, z4 = self.spherical_to_cartesian(self.radius, theta + 2 * math.pi / self.num_longitude, phi + math.pi / self.num_latitude)

                points.append(((x1, y1, z1), (x2, y2, z2)))
                points.append(((x1, y1, z1), (x3, y3, z3)))
                points.append(((x2, y2, z2), (x4, y4, z4)))
                points.append(((x3, y3, z3), (x4, y4, z4)))
        
        return points

    def animate(self):
        elapsed_time = time.time() - self.time_start
        self.canvas.delete("all")
        for (point1, point2) in self.points:
            x1, y1, z1 = point1
            x2, y2, z2 = point2

            z1 += math.sin(elapsed_time * self.oscillation_speeds["latitude"]) * 10
            z2 += math.sin(elapsed_time * self.oscillation_speeds["longitude"]) * 10

            x1_proj, y1_proj = self.project_to_2d(x1, y1, z1, self.canvas_width, self.canvas_height)
            x2_proj, y2_proj = self.project_to_2d(x2, y2, z2, self.canvas_width, self.canvas_height)

            self.canvas.create_line(x1_proj, y1_proj, x2_proj, y2_proj, fill='blue', width=3)

        self.root.after(120, self.animate)


class MainThread:
    def __init__(self):
        super(MainThread, self).__init__()

        # Conmfigure Libs
        logging.basicConfig(filename="logs/jarvis.log", level=logging.INFO, format='%(asctime)s - %(message)s')
        openai.api_key = config.OPENAI_API_KEY

        # Initialize History
        self.history = []

        # Initialize Porcupine
        self.porcupine = None
        self.pa = None
        self.audio_stream = None

        # Start Mycroft Skill
        self.mycroft_skill = MycroftSkill()
        self.mycroft_skill.initialize()

        # Start Interface
        interface.startup()

        # Start GUI
        # gui = threading.Thread(target=self.start_gui)
        # gui.daemon = True
        # gui.start()


    def run(self):
        while True:
            try:
                self.porcupine = pvporcupine.create(access_key=config.PICOVOICE_API_KEY, keywords=["jarvis"])
                self.pa = pyaudio.PyAudio()
                self.audio_stream = self.pa.open(
                    rate=self.porcupine.sample_rate,
                    channels=1,
                    format=pyaudio.paInt16,
                    input=True,
                    frames_per_buffer=self.porcupine.frame_length)
                
                while True:
                    pcm = self.audio_stream.read(self.porcupine.frame_length)
                    pcm = struct.unpack_from("h" * self.porcupine.frame_length, pcm)
                    keyword_index = self.porcupine.process(pcm)
                    if keyword_index >= 0:
                        self.run_command(interface.mic_input())
            
            finally:
                if self.porcupine is not None:
                    self.porcupine.delete()

                if self.audio_stream is not None:
                    self.audio_stream.close()
                
                if self.pa is not None:
                    self.pa.terminate()


    def listen_tone(self):
        winsound.Beep(400, 250)


    def say(self, text):
        interface.speak(text)
        self.history.append({"role": "system", "content": text})
        # add gui manip here


    def run_command(self, input):
        logging.info(f"User Input: {input}")
        self.history.append({"role": "user", "content": input})
        
        # Get Response from Mycroft
        response = self.mycroft_skill.process_intent(input)

        # Speak Response
        if response:
            self.say(response)
        else:
            logging.warning(f"Command not recognized: {input}")
            self.say("Sorry, I didn't catch that. Please repeat.")


    def start_gui(self):
        root = tk.Tk()
        self.gui_instance = JarvisGUI(root)
        root.mainloop()


exe = MainThread()
exe.run()