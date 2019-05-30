import pickle


class Command:
    def __init__(self, left_drive, right_drive, do_kick):
        self.left_drive = left_drive
        self.right_drive = right_drive
        self.do_kick = do_kick

    def get_pickled(self):
        return pickle.dumps(self)

    @staticmethod
    def unpickled(command_pickle):
        return pickle.loads(command_pickle)