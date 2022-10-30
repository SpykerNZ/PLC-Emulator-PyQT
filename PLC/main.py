class Plc:
    def __init__(self, timestep_ms: int):
        self.timestep_ms = timestep_ms
        self.running = False
        self.time_ms = 0
        self.cycle_count = 0

    def start(self):
        self.running = True

    def pause(self):
        self.running = False

    def reset(self):
        self.running = False
        self.time_ms = 0
        self.cycle_count = 0

    def update(self):
        if self.running:
            self._timestep()

    def _timestep(self):
        self.time_ms += self.timestep_ms
        self.cycle_count += 1
        # run PLC tasks here
