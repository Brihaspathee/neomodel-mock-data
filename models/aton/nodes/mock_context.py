import contextvars

mock_mode: contextvars.ContextVar[bool]  = contextvars.ContextVar("mock_mode", default=False)
create_entity_code: contextvars.ContextVar[bool] = contextvars.ContextVar("create_entity_code", default=False)

def enable_mock():
    mock_mode.set(True)

def disable_mock():
    mock_mode.set(False)

def is_mock_enabled():
    return mock_mode.get()

def set_create_entity_code(code: bool):
    create_entity_code.set(code)

def get_create_entity_code():
    return create_entity_code.get()