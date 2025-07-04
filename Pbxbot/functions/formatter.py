import math
import re

# --- Text Formatting Utilities ---

def format_text(text: str) -> str:
    """Removes all emoji characters from a string.

    Args:
        text (str): The input string that may contain emojis.

    Returns:
        str: The string with all emojis removed.
    """
    # A comprehensive regex pattern to match most emoji unicodes
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F700-\U0001F77F"  # alchemical symbols
        "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
        "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
        "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
        "\U0001FA00-\U0001FA6F"  # Chess Symbols
        "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
        "\U00002702-\U000027B0"  # Dingbats
        "\U000024C2-\U0001F251"  # enclosed characters
        "]+",
        flags=re.UNICODE,
    )
    return re.sub(emoji_pattern, "", text)


def superscript(text: str) -> str:
    """Converts digits in a string to their superscript equivalents.

    Args:
        text (str): The input string containing digits.

    Returns:
        str: The string with digits converted to superscript.
    """
    superscript_digits = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")
    return text.translate(superscript_digits)


def subscript(text: str) -> str:
    """Converts digits in a string to their subscript equivalents.

    Args:
        text (str): The input string containing digits.

    Returns:
        str: The string with digits converted to subscript.
    """
    subscript_digits = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
    return text.translate(subscript_digits)


# --- Time and Data Size Utilities ---

def readable_time(seconds: int) -> str:
    """Converts a total number of seconds into a human-readable string (days, hrs, mins, secs).

    Args:
        seconds (int): The total number of seconds.

    Returns:
        str: A human-readable time format, e.g., "1 days, 2 hrs 30 mins 5 secs".
    """
    count = 0
    out_time = ""
    time_list = []
    time_suffix_list = ["secs", "mins", "hrs", "days"]

    while count < 4:
        count += 1
        # Calculate minutes and hours by dividing by 60
        if count < 3:
            remainder, result = divmod(seconds, 60)
        # Calculate days by dividing by 24
        else:
            remainder, result = divmod(seconds, 24)
        
        if seconds == 0 and remainder == 0:
            break
            
        time_list.append(f"{int(result)} {time_suffix_list[count-1]}")
        seconds = int(remainder)

    if not time_list:
        return "0 secs"

    time_list.reverse()
    return " ".join(time_list)


def humanbytes(size_bytes: int) -> str:
    """Converts a size in bytes to a human-readable format (e.g., KiB, MiB, GiB).

    Args:
        size_bytes (int): The size in bytes.

    Returns:
        str: The human-readable string with the appropriate unit (e.g., "1.50 MiB").
    """
    if not isinstance(size_bytes, (int, float)) or size_bytes == 0:
        return "0 B"
    
    power = 1024  # 2**10
    power_n = 0
    power_labels = {0: "B", 1: "KiB", 2: "MiB", 3: "GiB", 4: "TiB"}
    
    while size_bytes >= power and power_n < len(power_labels):
        size_bytes /= power
        power_n += 1
        
    return f"{size_bytes:.2f} {power_labels[power_n]}"


def secs_to_mins(seconds: int) -> str:
    """Converts seconds to a 'minutes:seconds' format (MM:SS).

    Args:
        seconds (int): The total number of seconds.

    Returns:
        str: A string in MM:SS format (e.g., "02:30").
    """
    if not isinstance(seconds, int) or seconds < 0:
        return "00:00"
    minutes, secs = divmod(seconds, 60)
    return f"{minutes:02}:{secs:02}" # Pads with leading zeros


# --- Dictionary Utilities ---

def add_to_dict(data: dict, keys: list, value: any) -> None:
    """Adds a value to a nested dictionary using a list of keys. Creates keys if they don't exist.

    Args:
        data (dict): The dictionary to modify.
        keys (list): A list of keys representing the path.
        value (any): The value to set at the final key.
    """
    current_level = data
    for key in keys[:-1]:
        current_level = current_level.setdefault(key, {})
    current_level[keys[-1]] = value


def get_from_dict(data: dict, keys: list) -> any:
    """Retrieves a value from a nested dictionary using a list of keys.

    Args:
        data (dict): The dictionary to search in.
        keys (list): The list of keys representing the path.

    Returns:
        any: The value found at the path, or raises a KeyError if not found.
    """
    current_level = data
    for k in keys:
        current_level = current_level[k]
    return current_level

# --- Miscellaneous Utilities ---

def limit_per_page(total_items: int, items_per_page: int = 10) -> int:
    """Calculates the number of pages needed for a given number of items.

    Args:
        total_items (int): The total number of items.
        items_per_page (int, optional): The number of items on each page. Defaults to 10.

    Returns:
        int: The total number of pages required.
    """
    if total_items <= 0:
        return 0
    return math.ceil(total_items / items_per_page)


# --- Example Usage ---
if __name__ == "__main__":
    print("--- Function Demonstrations ---")

    # format_text
    print(f"Text Formatting: '{format_text('Hello World 👋! This is a test. 😊')}'")
    
    # superscript & subscript
    print(f"Superscript: 'E = mc2' -> '{superscript('E = mc2')}'")
    print(f"Subscript: 'H2O' -> '{subscript('H2O')}'")

    # readable_time
    print(f"Readable Time (90061s): {readable_time(90061)}") # 1 day, 1 hr, 1 min, 1 sec

    # humanbytes
    print(f"Human Bytes (1,500,000 bytes): {humanbytes(1500000)}")

    # secs_to_mins
    print(f"Seconds to Minutes (155s): {secs_to_mins(155)}")

    # limit_per_page
    print(f"Pages for 95 items (10 per page): {limit_per_page(95)}")

    # Dictionary utilities
    my_data = {}
    add_to_dict(my_data, ['user', 'profile', 'id'], 12345)
    add_to_dict(my_data, ['user', 'profile', 'name'], 'Ravi')
    print(f"Created Nested Dictionary: {my_data}")
    
    user_name = get_from_dict(my_data, ['user', 'profile', 'name'])
    print(f"Retrieved Name from Dictionary: {user_name}")