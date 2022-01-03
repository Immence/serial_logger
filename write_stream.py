import sys

class WriteStream(object):
    def __init__(self, queue):
        self.queue = queue

    def write(self, text):
        self.queue.put(text)
    
    def flush(self):
        # noinspection PyStatementEffect
        None

    def isatty(self):
        None