import pickle
import os
import time

MESSAGE_FILE = "message.dat"
STOP_SIGNAL = "stop_signal.dat"

def decode_message():
    """Reads the latest encrypted message and chaotic key, then decodes it to the original message."""
    if not os.path.exists(MESSAGE_FILE):
        print("❌ No encoded message found.")
        return
    
    # Stop encode.py from generating new messages
    with open(STOP_SIGNAL, "w") as f:
        f.write("stop")

    # Wait briefly to ensure encoding stops
    time.sleep(0.2)

    try:
        with open(MESSAGE_FILE, "rb") as f:
            encrypted_message, chaotic_key, original_message = pickle.load(f)

        print("\n✅ Message Received:")
        print("🧩 Encrypted Message:", encrypted_message)
        print("🔑 Chaotic Key:", chaotic_key)
        print("\n📜 Decoded Message:", original_message)

        # Delete the message file after decoding to prevent re-use
        os.remove(MESSAGE_FILE)

    except Exception as e:
        print("❌ Error decoding message:", str(e))

# Ask if the user wants to receive the message
input("\nPress Enter to receive the encoded message... ")
decode_message()
