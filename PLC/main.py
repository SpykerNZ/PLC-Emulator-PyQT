from PLC.sleep import RealtimeSleeper
from PLC.tasks import PLCTask


class Plc:
    def __init__(self, timestep_ms: int):
        self.timestep_ms = timestep_ms
        self.running = False
        self.time_ms = 0
        self.tasks: list[PLCTask] = []

    def start(self):
        self.running = True

    def pause(self):
        self.running = False

    def reset(self):
        self.running = False
        self.time_ms = 0
        for task in self.tasks:
            task.reset()

    def add_task(self, task: PLCTask):
        self.tasks.append(task)

    def update(self):
        if self.running:
            self._timestep()

    def _timestep(self):
        self.time_ms += self.timestep_ms
        for task in self.tasks:
            duration_since_last_run = self.time_ms - task.last_run_time_ms
            if duration_since_last_run >= task.poll_rate:
                task.cycle_count += 1
                task.run()
                task.last_run_time_ms = self.time_ms
