# Access System 🔒

**Two-Factor Authentication System combining Arduino Keypad and Python Face Recognition**


A robust security system that combines password authentication via physical keypad with facial recognition for secure access control. Built with Arduino and Python.

## Features ✨
- **Dual Authentication**: Requires both password AND face recognition
- **Physical Keypad Interface**: 4x4 matrix keypad for secure password entry
- **Real-Time Face Recognition**: Live camera face matching with tolerance control
- **Security Measures**:
  - Password attempt limits
  - System lockout after multiple failures
  - Encrypted face data storage
- **Visual Feedback**: Three-color LED status indicators
- **Comprehensive Logging**: Detailed access attempts and system events
- **Remote Management**: Serial communication between Arduino and Python

## Hardware Requirements 🛠️
- Arduino Uno/Nano
- 4x4 Matrix Membrane Keypad
- USB Webcam
- 3x LEDs (Green, Red, Blue)
- Resistors (220Ω)
- Breadboard and jumper wires

**Connection Guide**:
| Arduino Pin | Component  |
|-------------|------------|
| 2-6         | Keypad Columns |
| 7-9         | Keypad Rows |
| 10          | Green LED  |
| 11          | Red LED    |
| 12          | Blue LED   |

## Software Requirements 💻
- Python 3.8+
- Arduino IDE 2.x
- Required Python Packages:
  ```bash
  face_recognition, opencv-python, pyserial, numpy


## Installation 📦
1. Clone repository:

  ```bash
git clone https://github.com/IAmFarrokhnejad/access-system.git
cd access-system
```

2. Upload Arduino sketch:

- Open ===sketch.ino=== in Arduino IDE

- Install Keypad library (Tools > Manage Libraries)

- Upload to Arduino board

3. Install Python dependencies:

  ```bash
  face_recognition, opencv-python, pyserial, numpy
  ```
4. Set up known faces:

  ```bash
mkdir known_faces
```

5. Configure settings in app.py


## Usage 🚀
1. Start the system:

  ```bash
python app.py

```
2. Keypad commands:

- Digits 0-9: Password entry

- A: Backspace

- B: Submit password

- C: Start face scan

- D: System reset

3. LED Status Indicators:

**sGreen**: Access granted

**Red**: Access denied/system locked

**Blue**: Face scan in progress

4. Typical workflow:

- Enter password using keypad

- Press B to submit

- If password correct, face scan automatically initiates

- Look at camera for face verification

- Receive access grant/denial via LEDs

## Troubleshooting 🐞
**Common Issues:**

- **Camera not detected**: Ensure no other applications are using the webcam

- **Serial connection errors:**

- Verify correct COM port in configuration

- Check Arduino drivers are installed

- **Face recognition failures:**

- Ensure good lighting conditions

- Add multiple face angles to known_faces

- Adjust FACE_MATCH_THRESHOLD in config

## Safety & Privacy 🔐
- All face data stored locally in known_faces directory

- System logs contain no biometric data

- Recommended for secure environments only

- Rotate passwords regularly for enhanced security

## License 📄
MIT License - See LICENSE for details
