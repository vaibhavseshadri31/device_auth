document.addEventListener('DOMContentLoaded', function () {
    const emailInput = document.getElementById('email');
    const verifyBtn = document.getElementById('verifyBtn');
    const statusDiv = document.getElementById('status');
    const emailForm = document.getElementById('emailForm');
    const successMessage = document.getElementById('successMessage');

    verifyBtn.addEventListener('click', async function () {
        const email = emailInput.value.trim();

        if (!email || !validateEmail(email)) {
            updateStatus('Please enter a valid email address.', 'error');
            return;
        }

        try {
            updateStatus('Requesting biometric verification...', 'info');

            // Get or generate a unique device ID
            let deviceId = localStorage.getItem('device_id');
            if (!deviceId) {
                alert("Please run 'python add_device.py your@email.com' to generate a device ID and add it to localStorage");
                throw new Error("No device ID found");
            }

            // Perform biometric authentication
            const biometricResult = await performBiometricAuth();

            if (biometricResult) {
                // Generate a token with email, device ID, and expiration
                const tokenData = {
                    email: email,
                    deviceId: deviceId,
                    timestamp: Date.now(),
                    expires: Date.now() + 5 * 60 * 1000, // 5 minutes expiration
                };

                // Send token and email to the server
                const response = await fetch('/api/submit-email', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(tokenData),
                });

                const data = await response.json();

                if (data.success) {
                    // Show success message
                    emailForm.classList.add('hidden');
                    successMessage.classList.remove('hidden');
                } else {
                    updateStatus(data.message || 'Authentication failed. Please try again.', 'error');
                }
            }
        } catch (error) {
            console.error('Authentication error:', error);
            updateStatus(`Authentication failed: ${error.message || 'Unknown error'}`, 'error');
        }
    });

    /**
     * Perform device biometric authentication locally.
     */
    async function performBiometricAuth() {
        try {
            // Check browser support for WebAuthn
            if (!window.PublicKeyCredential) {
                throw new Error('WebAuthn not supported by this browser.');
            }

            const supported = await PublicKeyCredential.isUserVerifyingPlatformAuthenticatorAvailable();
            if (!supported) {
                throw new Error('Platform authenticator is not available.');
            }

            // Generate ephemeral WebAuthn authentication
            const challenge = new Uint8Array(32);
            window.crypto.getRandomValues(challenge);
            
            
            // Use WebAuthn to trigger biometric verification, forces passkey creation unfortunately 
            const credential = await navigator.credentials.create({
                publicKey: {
                    challenge: challenge,
                    rp: {
                        name: "TEMPORARY VERIFICATION",
                        id: window.location.hostname
                    },
                    user: {
                        id: new Uint8Array(16).fill(Date.now() % 255),
                        name: `delete-me-TEMPORARY-VERIFICATION-${Date.now()}@verification.local`, // Unique identifier for this verification attempt
                        displayName: 'TEMPORARY VERIFICATION'
                    },
                    pubKeyCredParams: [
                        { type: 'public-key', alg: -7 },  // ES256
                        { type: 'public-key', alg: -257 } // RS256
                    ],
                    authenticatorSelection: {
                        authenticatorAttachment: 'platform',
                        userVerification: 'required',
                        requireResidentKey: false
                    },
                    timeout: 60000,
                    attestation: 'none'
                }
            });
            
            
            return {
                timestamp: Date.now(),
                expires: Date.now() + 5 * 60 * 1000,
                deviceId: getDeviceId()
            };
        } catch (error) {
            console.error('Biometric authentication error:', error);
            throw error;
        }
    }


    function getDeviceId() {
        let deviceId = localStorage.getItem('device_id');
        if (!deviceId) {
            deviceId = 'device_' + Date.now() + '_' + Math.random().toString(36).substring(2, 15);
            localStorage.setItem('device_id', deviceId);
        }
        return deviceId;
    }

    function validateEmail(email) {
        const re =
            /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        return re.test(String(email).toLowerCase());
    }


    function generateDeviceId() {
        return `device_${Date.now()}_${Math.random().toString(36).substring(2, 15)}`;
    }

    function updateStatus(message, type) {
        statusDiv.textContent = message;
        statusDiv.className = 'status'; 
        statusDiv.classList.add(type); 
    }
});