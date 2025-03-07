from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import Dict, Optional
import time
import uvicorn
import os
import json
from pathlib import Path
import uuid

app = FastAPI(title="Secure Email Authentication API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Functions to interact with database.json
def load_trusted_devices():
    try:

        with open("database.json", "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_trusted_devices(devices):
    with open("database.json", "w") as f:
        json.dump(devices, f, indent=4)

# Initialize database from database.json, in production this will be a real database
trusted_devices = load_trusted_devices()

class EmailSubmission(BaseModel):
    email: EmailStr
    deviceId: str
    timestamp: int
    expires: int

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_index():
    return FileResponse("index.html")

@app.post("/api/submit-email")
async def submit_email(submission: EmailSubmission):
    # Load latest device data
    trusted_devices = load_trusted_devices()
    
    # Check if the token is expired
    current_time = int(time.time() * 1000)
    if submission.expires < current_time:
        raise HTTPException(status_code=400, detail="Authentication token expired")
    
    # Check if device is trusted or add it to trusted devices
    device_info = trusted_devices.get(submission.deviceId)
    
    if not device_info:
        # Device is not trusted
        return JSONResponse(
            status_code=403,
            content={
                "success": False,
                "message": "Device not trusted",
                "deviceId": submission.deviceId
            }
        )
    else:
        # Update last used timestamp
        device_info["last_used"] = current_time
        trusted_devices[submission.deviceId] = device_info
        
        # Save changes to database
        save_trusted_devices(trusted_devices)
        
        if device_info["email"] != submission.email:
            return JSONResponse(
                status_code=400,
                content={
                    "success": False,
                    "message": "Invalid email for this device",
                    "deviceId": submission.deviceId
                }
            )

    
    return JSONResponse(
        content={
            "success": True,
            "message": f"Email {submission.email} successfully authenticated and submitted",
            "deviceId": submission.deviceId
        }
    )

@app.post("/api/register-device")
async def register_device(request: Request):
    data = await request.json()
    email = data.get("email")
    
    if not email:
        return JSONResponse(
            status_code=400,
            content={"success": False, "message": "Email is required"}
        )
    
    # Generate a device ID
    timestamp = int(time.time() * 1000)
    random_part = uuid.uuid4().hex[:12]
    device_id = f"device_{timestamp}_{random_part}"
    
    # Load trusted devices
    trusted_devices = load_trusted_devices()
    
    # Add the new device
    trusted_devices[device_id] = {
        "email": email,
        "first_seen": timestamp,
        "last_used": timestamp
    }
    
    # Save the updated devices
    save_trusted_devices(trusted_devices)
    
    return JSONResponse(
        content={
            "success": True,
            "message": f"Device registered for {email}",
            "deviceId": device_id
        }
    )

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)