# ----- Python Standard Library ----- #
import logging
import importlib

# ----- Project Command----- #
from .bot_settings import command as bot_settings_cmd
from .esteem import command as esteem_cmd
from .ping import command as ping_cmd

Log = logging.getLogger(__name__)

def get_command(cmd_name):
    try:
        Log.debug(f"Importing: .{cmd_name} inside {__name__}")
        module = importlib.import_module(f".{cmd_name}", __name__)
        return getattr(module, "command")
    except (ImportError, AttributeError):
        return None
