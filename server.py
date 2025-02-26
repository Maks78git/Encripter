from flask import Flask, render_template_string, request
import pickle
import os
import re

app = Flask(__name__)
MESSAGE_FILE = "message.dat"

# HTML Template
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Secure Message Receiver</title>
</head>
<body>
    <h1>Secure Message Receiver</h1>
    <form method="POST">
        <button type="submit">Receive Message</button>
    </form>
    {% if decoded_message %}
        <h2>Decoded Message:</h2>
        <p>{{ decoded_message }}</p>
    {% endif %}
</body>
</html>
"""

# Decoding function
def decode_message():
    if not os.path.exists(MESSAGE_FILE):
        return "No message found"
    try:
        with open(MESSAGE_FILE, "rb") as f:
            data = pickle.load(f)

        print("Raw Encrypted Data:", data)  # Debugging line to check what’s stored

        if len(data) == 2:
            encrypted_message, chaotic_key = data
        elif len(data) == 3:
            encrypted_message, chaotic_key, _ = data  # Ignore extra values
        else:
            return "Unexpected data format"

        print("Extracted Encrypted Message:", encrypted_message)  # Debug print
        print("Chaotic Key:", chaotic_key)  # Debug print

        # Extract only the first character of each encoded block
        decoded_chars = []
        encoded_parts = encrypted_message.split(" | ")

        for part in encoded_parts:
            print("Processing:", part)  # Debug print
            match = re.match(r"(.+?)\(.+?,.+?\)", part)  # Extract the first character before color/shape
            if match:
                decoded_chars.append(match.group(1))  # Append only the original character

        decoded_message = "".join(decoded_chars)
        print("Decoded Message:", decoded_message)  # Final debug print
        return decoded_message
    except Exception as e:
        print("Decoding Error:", str(e))  # Print error for debugging
        return f"Error decoding message: {str(e)}"


@app.route("/", methods=["GET", "POST"])
def index():
    decoded_message = None
    if request.method == "POST":
        decoded_message = decode_message()
    return render_template_string(HTML_PAGE, decoded_message=decoded_message)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
