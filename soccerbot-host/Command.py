import pickle


class Command:
    def __init__(self, left_drive, right_drive, do_kick):
        self.left_drive = left_drive
        self.right_drive = right_drive
        self.do_kick = do_kick

    def get_pickled(self):
        return pickle.dumps(self, protocol=4)

    @staticmethod
    def unpickled(command_pickle):
        return pickle.loads(command_pickle)
    
    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, Command):
            return self.left_drive == other.left_drive and self.right_drive == other.right_drive and self.do_kick == other.do_kick
        return False