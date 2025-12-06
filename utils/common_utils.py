import secrets
import string


def merge_objects(obj1, obj2, override=True):
    for attr, value in vars(obj2).items():
        if value is not None:
            if override or getattr(obj1, attr, None) is None:
                setattr(obj1, attr, value)
    return obj1

def generate_unique_code(self, length=15):
    chars = string.ascii_uppercase + string.digits
    return ''.join(secrets.choice(chars) for _ in range(length))
