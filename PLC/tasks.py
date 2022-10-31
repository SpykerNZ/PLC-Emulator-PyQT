from abc import ABC


class PLC_PRG(ABC):
    def update(self):
        pass


class PLCTask:
    def __init__(self, name: str, poll_rate: int, task: PLC_PRG):
        self.name = name
        self.poll_rate = poll_rate
        self.task = task
        self.cycle_count = 0
        self.last_run_time_ms = 0

    def reset(self):
        self.cycle_count = 0
        self.last_run_time_ms = 0

    def run(self):
        self.task.update()
