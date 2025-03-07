# Secure Email Authentication Demo

This project demonstrates a secure email authentication system that combines device identification, biometric verification, and token expiration to create a secure multi-factor authentication flow.

## Features

- Device-based authentication using unique device IDs
- Biometric verification using WebAuthn (fingerprint, face ID, etc.)
- Time-based token expiration
- Simple JSON-based device database
- Real-time status messages for authentication feedback

## Prerequisites

- Python 3.7+
- A modern web browser with WebAuthn support (Chrome, Firefox, Safari, Edge)
- A device with biometric capabilities (fingerprint reader, facial recognition)

## Setup Instructions

1. Clone this repository:

   ```bash
   git clone https://github.com/vaibhavseshadri31/device_auth.git
   cd device_auth
   ```

2. Activate the included virtual environment:

   ```bash
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. Start the server:

   ```bash
   python main.py
   ```

4. Open your browser and navigate to:
   ```
   http://localhost:8000
   ```

## How It Works

1. **Device Registration**:

   - Enter your email in the web interface
   - Click the "Register This Device" button
   - The system will register your device in the database
   - Status messages appear under the registration button to provide feedback

2. **Authentication Flow**:
   - Enter your email in the web interface
   - Click "Verify with Biometrics" to initiate biometric verification via WebAuthn
   - If successful, the server verifies that the device ID is trusted
   - If the device is trusted and associated with the email, authentication succeeds
   - Status messages appear under the verification button to provide real-time feedback on each step

## User Interface

- Email input field for entering your registered email
- "Verify with Biometrics" button to initiate the authentication process
- "Register This Device" button to associate the current device with your email
- Status messages appear under the buttons to provide feedback about the authentication or registration process

## Project Structure

- `main.py`: FastAPI server that handles API requests and serves static content
- `database.json`: Simple JSON database of trusted devices
- `static/`: Directory containing frontend assets (CSS, JavaScript)
- `index.html`: Main web interface

## Security Features

- Biometric authentication that stays local to the device
- Device-based validation against a trusted device list
- Time-based token expiration (5 minutes)
- Binding of email addresses to specific devices


## Troubleshooting

- If you see "Device not trusted" error, ensure you've registered your device using the "Register This Device" button
- If biometric authentication fails, check that your device supports WebAuthn and has biometric capabilities enabled
- For any other issues, check the server logs for detailed error messages
