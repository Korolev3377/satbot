# ----- Python Standard Library ----- #
import asyncio
import logging
import os

Log = logging.getLogger(__name__)

class FileLock:
    def __init__(self, lockname):
        self.lockname = lockname
        self.fd = None

    def __enter__(self):
        while 1:
            try:
                self.fd = os.open(self.lockname, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                break
            except FileExistsError:
                asyncio.sleep(0.05)

    def __exit__(self, *_):
        if self.fd is not None:
            os.close(self.fd)
            try:
                os.remove(self.lockname)
            except OSError:
                pass