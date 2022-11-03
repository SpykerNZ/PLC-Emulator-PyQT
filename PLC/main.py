from PLC.sleep import RealtimeSleeper
from PLC.tasks import PLCTask


class Plc:
    def __init__(self, timestep_ms: int):
        self.timestep_ms = timestep_ms
        self.running = False
        self.time_ms = 0
        self.task: PLCTask = None

    def start(self):
        self.running = True

    def pause(self):
        self.running = False

    def reset(self):
        self.running = False
        self.time_ms = 0
        self.task.reset()

    def set_task(self, task: PLCTask):
        self.task = task

    def update(self):
        if self.running:
            self._timestep()

    def _timestep(self):
        self.time_ms += self.timestep_ms
        duration_since_last_run = self.time_ms - self.task.last_run_time_ms
        if duration_since_last_run >= self.task.poll_rate:
            self.task.cycle_count += 1
            self.task.run()
            self.task.last_run_time_ms = self.time_ms
