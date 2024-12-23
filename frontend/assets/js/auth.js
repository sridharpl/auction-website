const BACKEND_URL = "https://auction-website.streamlit.app/";

document.getElementById('auth-form').addEventListener('submit', async (event) => {
    event.preventDefault();
    const phoneNumber = document.getElementById('phone-number').value;
    const statusMessage = document.getElementById('status-message');

    try {
        const response = await fetch(`${BACKEND_URL}/api/send-otp`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ phone_number: phoneNumber }),
        });
        const result = await response.json();

        if (result.success) {
            statusMessage.textContent = 'OTP sent! Please check your mobile.';
        } else {
            statusMessage.textContent = result.message || 'Failed to send OTP.';
        }
    } catch (error) {
        console.error('Error sending OTP:', error);
        statusMessage.textContent = 'An error occurred. Please try again.';
    }
});