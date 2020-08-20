class JacyError(Exception):
    msg: str = 'Unknown error'

    def __init__(self, msg):
        self.msg = msg

class DevError(Exception):
    def __str__(self):
        return '[DevError]: '+ super.msg

