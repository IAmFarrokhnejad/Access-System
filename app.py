import serial
import time
import face_recognition
import cv2
import numpy as np
import os
import logging
from logging.handlers import RotatingFileHandler

# Configure logging
log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(log_formatter)
logger.addHandler(console_handler)

# File handler
file_handler = RotatingFileHandler('access.log', maxBytes=1e6, backupCount=3)
file_handler.setFormatter(log_formatter)
logger.addHandler(file_handler)

# Configuration
CONFIG = {
    'PORT': 'COM3',
    'BAUDRATE': 9800,
    'KNOWN_FACES_DIR': 'known_faces',
    'PASSWORD': [1, 2, 3],
    'FACE_MATCH_THRESHOLD': 0.6,
    'MAX_PASSWORD_ATTEMPTS': 3,
    'MAX_FACE_ATTEMPTS': 3,
    'LOCKOUT_TIME': 60  # seconds
}

# Global state
ser = None
known_face_encodings = []
known_face_names = []

def initialize_serial():
    global ser
    try:
        ser = serial.Serial(CONFIG['PORT'], CONFIG['BAUDRATE'], timeout=1)
        time.sleep(2)
        logger.info("Serial connection established")
    except serial.SerialException as e:
        logger.error(f"Serial connection failed: {e}")
        exit(1)

def load_known_faces():
    global known_face_encodings, known_face_names
    try:
        for filename in os.listdir(CONFIG['KNOWN_FACES_DIR']):
            path = os.path.join(CONFIG['KNOWN_FACES_DIR'], filename)
            if os.path.isfile(path) and filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                image = face_recognition.load_image_file(path)
                encodings = face_recognition.face_encodings(image)
                if encodings:
                    known_face_encodings.append(encodings[0])
                    known_face_names.append(os.path.splitext(filename)[0])
                    logger.debug(f"Loaded face: {filename}")
                else:
                    logger.warning(f"No faces found in {filename}")
        logger.info(f"Successfully loaded {len(known_face_encodings)} known faces")
    except Exception as e:
        logger.error(f"Error loading known faces: {e}")
        exit(1)

def send_arduino_command(command):
    try:
        if ser and ser.is_open:
            ser.write(command.encode())
            logger.debug(f"Sent command: {command}")
    except serial.SerialException as e:
        logger.error(f"Failed to send command: {e}")

def perform_face_scan():
    logger.info("Initiating face recognition")
    send_arduino_command('P')  # Face scan in progress
    
    video = cv2.VideoCapture(0)
    if not video.isOpened():
        logger.error("Failed to access camera")
        send_arduino_command('F')
        return False

    face_matched = False
    attempts = 0

    while attempts < CONFIG['MAX_FACE_ATTEMPTS'] and not face_matched:
        ret, frame = video.read()
        if not ret:
            logger.warning("Failed to capture frame")
            continue

        # Process frame
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Detect faces
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(
                known_face_encodings, face_encoding, CONFIG['FACE_MATCH_THRESHOLD']
            )
            if True in matches:
                name = known_face_names[matches.index(True)]
                logger.info(f"Access granted to: {name}")
                face_matched = True
                break

        cv2.imshow('Face Recognition', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        attempts += 1
        time.sleep(1)

    video.release()
    cv2.destroyAllWindows()

    if face_matched:
        send_arduino_command('G')  # Access granted
        return True
    else:
        logger.warning("Face recognition failed")
        send_arduino_command('R')  # Access denied
        return False

def main_loop():
    password_attempts = 0
    entered_password = []

    while True:
        if password_attempts >= CONFIG['MAX_PASSWORD_ATTEMPTS']:
            logger.warning("Too many attempts - system locked")
            send_arduino_command('L')
            time.sleep(CONFIG['LOCKOUT_TIME'])
            password_attempts = 0
            continue

        try:
            line = ser.readline().decode().strip()
        except UnicodeDecodeError:
            continue

        if not line:
            continue

        logger.debug(f"Received: {line}")

        if line == 'A':  # Backspace
            if entered_password:
                entered_password.pop()
                logger.info(f"Current input: {entered_password}")
        elif line == 'B':  # Submit
            if entered_password == CONFIG['PASSWORD']:
                logger.info("Password correct - starting face recognition")
                if perform_face_scan():
                    logger.info("Full access granted")
                else:
                    password_attempts += 1
            else:
                logger.warning("Incorrect password")
                password_attempts += 1
                send_arduino_command('R')
            entered_password = []
        elif line == 'D':  # Reset
            entered_password = []
            password_attempts = 0
            send_arduino_command('X')
            logger.info("System reset")
        elif line.isdigit():
            entered_password.append(int(line))
            logger.info(f"Current input: {entered_password}")

if __name__ == "__main__":
    try:
        initialize_serial()
        load_known_faces()
        main_loop()
    except KeyboardInterrupt:
        logger.info("Shutting down")
    except Exception as e:
        logger.critical(f"Critical error: {e}")
    finally:
        if ser and ser.is_open:
            ser.close()