# utils/string_helpers.py

def sanitize_data(data):
    """
    Strips whitespace from the beginning and end of strings in the provided dictionary.

    The function iterates over each key-value pair in the dictionary. If the value is a string,
    it strips whitespace from the beginning and end and updates the dictionary with the sanitized string.

    Args:
    - data (dict): Dictionary containing data to be sanitized.

    Returns:
    - dict: Dictionary with sanitized strings.
    """
    
    # Iterate over each key-value pair in the dictionary
    for key, value in data.items():
        # Check if the current value is a string
        if isinstance(value, str):
            # Strip whitespace from the beginning and end of the string
            data[key] = value.strip()
    
    # Return the updated dictionary
    return data
