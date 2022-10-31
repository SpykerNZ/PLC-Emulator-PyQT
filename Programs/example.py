from PLC.tasks import PLC_PRG


class PRG_Example(PLC_PRG):
    def __init__(self):
        self.count = 1

    def update(self):
        self.count += 1
