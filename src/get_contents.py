import os


def getIndexPage():
    return os.popen('cat /var/task/index.html').read()
