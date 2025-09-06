import hashlib
from typing import Union, List


def hash_utility(*args: Union[str, List[str]]) -> str:
    """
        Generate a 64-bit deterministic hex hash from a list of strings.
        - Accepts either multiple string arguments or a single list of strings.
            Example inputs hash_utility("one", "two", "three") or hash_utility(["one", "two", "three"])
        - Requires at least 3 non-empty values.
        - Returns a 16-character hex string.
        """
    # if a single list of strings is provided, use it directly
    if len(args) == 1 and isinstance(args[0], list):
        values = args[0]
    else:
        # otherwise, convert the individual arguments to a list of strings
        values = list(args)

    normalized_values = []
    for v in values:
        if v and v.strip(): # get into the loop only if the value is not empty
            cleaned = v.strip().lower() # remove leading and trailing spaces and convert to lowercase
            normalized_values.append(cleaned) # add the cleaned value to the list
    values = normalized_values
    # The above code is equivalent to the following using List comprehensions:
    # values = [v.strip().lower() for v in values if v and v.strip()]
    if len(values) < 3:
        raise ValueError("At least 3 non-empty values are required.")
    # Concatenate with delimiter "|"
    key_str = "|".join(values)
    # SHA256 → take first 8 bytes → hex string (16 chars)
    # hashlib.sha256(key_str.encode("utf-8")).digest() -> produces 32 bytes has which is 256 bits
    # hashlib.sha256(key_str.encode("utf-8")).digest()[:8] -> produces 8 bytes which is 64 bits
    hash_bytes = hashlib.sha256(key_str.encode("utf-8")).digest()[:8]
    hash_hex = hash_bytes.hex()
    return hash_hex