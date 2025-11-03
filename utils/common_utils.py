def merge_objects(obj1, obj2, override=True):
    for attr, value in vars(obj2).items():
        if value is not None:
            if override or getattr(obj1, attr, None) is None:
                setattr(obj1, attr, value)
    return obj1
