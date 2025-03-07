# Secure Email Authentication Demo

This project demonstrates a secure email authentication system that combines device identification, biometric verification, and token expiration to create a secure multi-factor authentication flow.

## Features

- Device-based authentication using unique device IDs
- Biometric verification using WebAuthn (fingerprint, face ID, etc.)
- Time-based token expiration
- Simple JSON-based device database

## Prerequisites

- Python 3.7+
- A modern web browser with WebAuthn support (Chrome, Firefox, Safari, Edge)
- A device with biometric capabilities (fingerprint reader, facial recognition)

## Setup Instructions

1. Clone this repository:

   ```bash
   git clone <repository-url>
   cd secure-email-auth-demo
   ```

2. Activate the included virtual environment:

   ```bash
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. Create your first trusted device:

   ```bash
   python add_device.py your@email.com
   ```

   Note the device ID that is generated.

4. Start the server:

   ```bash
   python main.py
   ```

5. Open your browser and navigate to:
   ```
   http://localhost:8000
   ```

## How It Works

1. **Device Registration**:

   - Run `add_device.py` with your email to register a trusted device
   - The generated device ID is stored in `database.json`
   - Add this device ID to `localStorage` in the browser

2. **Authentication Flow**:
   - Enter your email in the web interface
   - The system initiates biometric verification via WebAuthn
   - If successful, the server verifies that the device ID is trusted
   - If the device is trusted and associated with the email, authentication succeeds

## Project Structure

- `main.py`: FastAPI server that handles API requests and serves static content
- `add_device.py`: Utility to add trusted devices to the database
- `database.json`: Simple JSON database of trusted devices
- `static/`: Directory containing frontend assets (CSS, JavaScript)
- `index.html`: Main web interface

## Security Features

- Biometric authentication that stays local to the device
- Device-based validation against a trusted device list
- Time-based token expiration (5 minutes)
- Binding of email addresses to specific devices

## Development Notes

- For production use, update CORS settings in `main.py` to specific domains
- The WebAuthn implementation creates temporary passkeys - in a production environment, you would implement a more sophisticated WebAuthn registration and authentication flow
- The current database is a simple JSON file - for production, use a proper database system

## Troubleshooting

- If you see "Device not trusted" error, ensure you've added your device using `add_device.py`
- If biometric authentication fails, check that your device supports WebAuthn and has biometric capabilities enabled
- For any other issues, check the server logs for detailed error messages


