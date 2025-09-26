import contextvars

mock_mode = contextvars.ContextVar("mock_mode", default=False)

def enable_mock():
    mock_mode.set(True)

def disable_mock():
    mock_mode.set(False)

def is_mock_enabled():
    return mock_mode.get()