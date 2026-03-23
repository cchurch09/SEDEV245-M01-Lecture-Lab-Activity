import hashlib
import os
import json
import base64

USER_FILE = "users.json"
users = {}

# -----------------------------
# Helper Functions
# -----------------------------
def hash_with_salt(password, salt):
    return hashlib.sha256(salt + password.encode()).hexdigest()

def encode_salt(salt):
    return base64.b64encode(salt).decode('utf-8')

def decode_salt(salt_str):
    return base64.b64decode(salt_str.encode('utf-8'))

# -----------------------------
# File Operations
# -----------------------------
def load_users():
    global users
    if not os.path.exists(USER_FILE):
        print("No existing user file found. Starting fresh.")
        return
    with open(USER_FILE, "r") as f:
        data = json.load(f)
    for username, info in data.items():
        users[username] = {
            "salt": decode_salt(info["salt"]),
            "hash": info["hash"],
            "role": info["role"]
        }
    print(f"Loaded {len(users)} user(s) from file.")

def save_users():
    data = {}
    for username, info in users.items():
        data[username] = {
            "salt": encode_salt(info["salt"]),
            "hash": info["hash"],
            "role": info["role"]
        }
    with open(USER_FILE, "w") as f:
        json.dump(data, f, indent=4)
    print("User data saved to file.")

# -----------------------------
# Core Functionality
# -----------------------------

#I added a way for when the user has to make a password it has to be atleast ten characters long.
def valid_password(password):   
    if len(password) < 10:
        return False, "Password must be at least ten characters long."
    return True, ""

def register_user():
    username = input("Enter new username: ").strip()
    if username in users:
        print(f"User '{username}' already exists.")
        return
    password = input("Enter password: ").strip()
    valid, message = valid_password(password)  #second part of adding user
    if not valid:
        print(message)
        return
    role = input("Enter role (admin/user): ").strip().lower()
    if role not in ["admin", "user"]:
        print("Invalid role. Defaulting to 'user'.")
        role = "user"
    salt = os.urandom(16)
    password_hash = hash_with_salt(password, salt)
    users[username] = {
        "salt": salt,
        "hash": password_hash,
        "role": role
    }
    print(f"User '{username}' registered successfully.")

def list_users():
    if not users:
        print("No users registered.")
        return
    print("\nCurrent users (salt & hash shown, passwords hidden):")
    for username, info in users.items():
        print(f"{username}:")
        print(f"  salt: {encode_salt(info['salt'])}")
        print(f"  hash: {info['hash']}")
        print(f"  role: {info['role']}")
    print()

def validate_user():
    username = input("Enter username to validate: ").strip()
    password = input("Enter password to check: ").strip()
    if username not in users:
        #print(f"User '{username}' not found.")
        print("Invalid Credentials!!!")
        return
    salt = users[username]["salt"]
    stored_password_hash = users[username]["hash"]
    password_hash = hash_with_salt(password, salt)
    if password_hash == stored_password_hash:
        print("Password correct!")
        if users[username]["role"] == "admin":
            print("Access: admin panel allowed.")
        else:
            print("Access: standard user privileges.")
    else:
        print("Invalid Credentials!!!")

# -----------------------------
# Main Program Loop
# -----------------------------
def main():
    load_users()
    while True:
        print("\n--- Secure Auth System ---")
        print("1. Create a new user")
        print("2. List users")
        print("3. Validate a user's password")
        print("4. Exit")
        choice = input("Enter choice (1-4): ").strip()
        if choice == "1":
            register_user()
        elif choice == "2":
            list_users()
        elif choice == "3":
            validate_user()
        elif choice == "4":
            save_users()
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
