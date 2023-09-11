from flask import Flask, request, jsonify

app = Flask(__name__)

# File path for storing UID and generated password
file_path = "/opt/test.txt"

# Dictionary to store UID-password mappings
uid_passwords = {}

# Load existing UID-password mappings from the file
try:
    with open(file_path, "r") as file:
        for line in file:
            uid, password = line.strip().split(", ")
            uid_passwords[uid] = password
except FileNotFoundError:
    # Create the file if it doesn't exist
    with open(file_path, "w") as file:
        pass

@app.route('/generate-password', methods=['POST'])
def generate_password():
    uid = request.json.get('uid').strip()  # Strip leading/trailing whitespace

    if uid in uid_passwords:
        return jsonify({"error": "UID already exists"}), 400

    # Generate a password using Caesar cipher
    password = caesar_cipher(uid[:6], 3)

    # Store UID and generated password in the file
    with open(file_path, "a") as file:
        file.write(f"{uid}, {password}\n")

    # Update the uid_passwords dictionary
    uid_passwords[uid] = password

    return jsonify({"password": password})

@app.route('/get-password', methods=['GET'])
def get_password():
    uid = request.args.get('uid')

    if uid in uid_passwords:
        return jsonify({"password": uid_passwords[uid]})
    else:
        return jsonify({"error": "UID not found"}), 404

def caesar_cipher(text, key):
    result = ""
    for char in text:
        if char.isalpha():
            shift = (ord(char) - key)
            if char.islower():
                if shift < ord('a'):
                    shift += 26
            else:
                if shift < ord('A'):
                    shift += 26
            result += chr(shift)
        else:
            result += char
    return result

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4455, debug=True)

