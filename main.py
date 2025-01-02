import hashlib

# Function to compute the hash of a file
def compute_file_hash(file_path: str, hash_algorithm: str = "sha256") -> str:
    try:
        # Initialize the hash object
        hash_func = hashlib.new(hash_algorithm)
        with open(file_path, "rb") as file:
            while chunk := file.read(8192):  # Read the file in chunks
                hash_func.update(chunk)
        return hash_func.hexdigest()
    except FileNotFoundError:
        return f"Error: File '{file_path}' not found."
    except ValueError:
        return f"Error: Unsupported hash algorithm '{hash_algorithm}'."

# Function to compare two hash values
def verify_file_integrity(original_hash: str, file_path: str, hash_algorithm: str = "sha256") -> bool:
    computed_hash = compute_file_hash(file_path, hash_algorithm)
    if computed_hash == original_hash:
        print(f"[PASS] File integrity verified. Hash: {computed_hash}")
        return True
    else:
        print(f"[FAIL] File integrity check failed.\nOriginal Hash: {original_hash}\nComputed Hash: {computed_hash}")
        return False

# Example usage
if __name__ == "__main__":
    # Compute the hash of a file
    file_path = "input_file.txt"
    original_hash = compute_file_hash(file_path)
    print(f"Original Hash: {original_hash}")

    # Verify the integrity of the file later
    is_valid = verify_file_integrity(original_hash, file_path)