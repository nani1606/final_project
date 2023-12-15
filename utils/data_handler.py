import json

def read_data(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error decoding JSON data in {file_path}.")
        return None
    except Exception as e:
        print(f"An error occurred while reading {file_path}: {e}")
        return None

def write_data(file_path, data):
    try:
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=2)
    except Exception as e:
        print(f"An error occurred while writing to {file_path}: {e}")
