import random
import time
import hashlib
import secrets
import threading
import string
import pickle
import os

MESSAGE_FILE = "message.dat"
STOP_SIGNAL = "stop_signal.dat"

CUSTOM_CHAR_SET = [chr(i) for i in range(1000, 11000)]
COLORS = ["red", "blue", "green", "yellow", "purple", "orange", "cyan", "magenta", "white", "black"]
SHAPES = ["circle", "square", "triangle", "star", "hexagon", "diamond"]

ALL_CHARACTERS = string.printable + ''.join(CUSTOM_CHAR_SET)

last_valid_key = None

def generate_chaotic_key():
    seed = str(time.time_ns()) + secrets.token_hex(64)
    random.seed(seed)
    return ''.join(random.choices(ALL_CHARACTERS, k=128))

def encode_message(message):
    global last_valid_key
    encrypted_message = ""
    chaotic_key = generate_chaotic_key()
    last_valid_key = chaotic_key

    for char in message:
        random.seed(ord(char) + int(time.time_ns()) % 1000)

        new_chars = [random.choice(CUSTOM_CHAR_SET) for _ in range(3)]
        colors = [random.choice(COLORS) for _ in range(3)]
        shapes = [random.choice(SHAPES) for _ in range(3)]

        encrypted_message += " ".join(f"{c}({col},{shp})" for c, col, shp in zip(new_chars, colors, shapes)) + " | "

    return encrypted_message.strip(), chaotic_key

def continuously_encode(message, interval=0.1):
    global last_valid_key
    while True:
        if os.path.exists(STOP_SIGNAL):  # Stop encoding if stop signal is found
            os.remove(STOP_SIGNAL)
            print("⛔ Encoding stopped.")
            return

        encoded, key = encode_message(message)
        
        # Save encoded message, chaotic key, and original message
        with open(MESSAGE_FILE, "wb") as f:
            pickle.dump((encoded, key, message), f)

        print("💠Encoded Message:", encoded)
        print("🔑Chaotic Key:", key, "(🚫Previous key is now invalid)")
        print("-")

        time.sleep(interval)

message = input("📜Enter the message to encode: ")
th = threading.Thread(target=continuously_encode, args=(message, 0.1))
th.start()
