import numpy as np
import cv2
import pyautogui

def take_screenshot(file_name):
    return pyautogui.screenshot(f"screenshots/{file_name}")

def open_screenshot(file_name):
    return cv2.imread(f"screenshots/{file_name}")