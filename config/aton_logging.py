from pathlib import Path
import logging.config
import yaml
import re
import os


def setup_logging(config_file='logging.yaml'):
    """
    Configures the logging system by reading a YAML configuration file and resolving any
    environment variable placeholders present in the configuration. It also ensures log file
    directories exist before initialization.

    :param config_file: The name of the logging configuration file. Defaults to 'logging.yaml'.
    :type config_file: str
    :return: None
    """
    base_dir = Path(__file__).resolve().parent
    config_path = base_dir / config_file

    with open(config_path, 'r') as f:
        config_text = f.read()

    r"""
        1.The variable contains a regular expression (regex) that is used to find and parse environment variable 
        placeholders in a logging configuration file. Let's analyze the regex pattern: `pattern`
            - `\$\{` - Matches the literal characters "${"
            - `([^:}]+)` - First capture group that matches one or more characters that are not ":" or "}"
            - `(:-([^}]+))?` - Optional second capture group that matches:
                - `:-` - Literal characters ":-"
                - `([^}]+)` - Third capture group that matches one or more characters that are not "}"
            - `\}` - Matches the literal character "}"

        This pattern is designed to match expressions like:
            - `${LOG_FORMAT}` - Simple environment variable reference
            - `${LOG_FILE_FORMAT:-json}` - Environment variable with a default value
                - "LOG_FILE_FORMAT" in group 1
                - "json" in group 3
            On this pattern
            1. group 1: `([^:}]+` captures "LOG_FILE_FORMAT
            2. group 2: `(:-([^}]+)` captures ":-json"
            3. group 3: `([^}]+)` captures "json
    """
    pattern = re.compile(r"\$\{([^:}]+)(:-([^}]+))?\}")

    def replacer(match):
        var_name = match.group(1)
        default_value = match.group(3) if match.group(3) else ""
        return os.getenv(var_name, default_value)

    # resolved_config will be a fully resolved logging configuration with no placeholders
    resolved_config = pattern.sub(replacer, config_text)

    # Convert the resolved configuration to a dictionary
    config = yaml.safe_load(resolved_config)
    # Sets up the loggers, handlers, levels and formatters as defined in the logging.yaml

    # Ensure log file directories exist
    # Get all the handlers defined in the logging configuration
    for handler in config.get("handlers", {}).values():
        # Check if the handler has a 'filename' key
        if 'filename' in handler:
            # handler['filename'] is the path to the log file. e.g. logs/aton-mock-data
            # Convert it to a Path object
            log_path: Path = Path(handler['filename'])
            # log.path.parent - gets the parent directory of the log file
            # creates the directory if it doesn't exist. For not raise an error if the directory exists
            log_path.parent.mkdir(parents=True, exist_ok=True)

    logging.config.dictConfig(config)
