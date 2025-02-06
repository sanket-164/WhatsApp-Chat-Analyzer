# Function to read and parse the file
def read_traffic(file_path):
    data = {}
    try:
        with open(file_path, "r") as file:
            for line in file:
                key, value = line.strip().split(": ")
                data[key] = int(value)
    except FileNotFoundError:
        # Initialize the file if not found
        data = {"Visits": 0, "Chats Analyzed": 0}
        update_traffic(file_path, data)
    return data

# Function to write updated data back to the file
def update_traffic(file_path, data):
    with open(file_path, "w") as file:
        for key, value in data.items():
            file.write(f"{key}: {value}\n")

def add_feedback(file_name, username, feedback):
    """Appends feedback to a text file."""
    with open(file_name, "a") as file:
        file.write(f"{username}: {feedback}\n")

def read_feedback(file_name):
    """Reads all feedback from the text file."""
    try:
        with open(file_name, "r") as file:
            feedbacks = file.readlines()
        return feedbacks
    except FileNotFoundError:
        return []  # Return empty list if file doesn't exist yet