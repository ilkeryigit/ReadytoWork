import ctypes
import sys

import app
import config

MUTEX_NAME = "ReadytoWork.SingleInstance"

_mutex_handle = None


def single_instance() -> bool:
    global _mutex_handle
    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel32.CreateMutexW.restype = ctypes.c_void_p
    kernel32.CreateMutexW.argtypes = [ctypes.c_void_p, ctypes.c_bool, ctypes.c_wchar_p]
    _mutex_handle = kernel32.CreateMutexW(None, False, MUTEX_NAME)
    return ctypes.get_last_error() != 183


def main() -> None:
    if not single_instance():
        sys.exit(0)
    config.migrate_legacy()
    items, browser, lang = config.load()
    first_run = not config.config_path().exists()
    app.TrayApp(items, browser, lang, first_run).run()


if __name__ == "__main__":
    main()
