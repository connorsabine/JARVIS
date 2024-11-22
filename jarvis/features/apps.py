import subprocess

def open(app_name):
    try:
        subprocess.run([app_name], check=True)
        return True
    
    except FileNotFoundError:
        return False

    except Exception as e:
        return False