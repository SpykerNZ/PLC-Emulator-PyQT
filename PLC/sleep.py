import time


class RealtimeSleeper:
    def __init__(self):
        self.i = 0
        self.t0 = time.time()
        self.timestep_ms = 0

    def set_timestep(self, time_ms: int):
        self.timestep_ms = time_ms
        self.i = 0
        self.t0 = time.time()

    def sleep(self, timestep_ms: int):
        if timestep_ms == 0:
            time.sleep(0.001)
            return

        if self.timestep_ms != timestep_ms:
            self.set_timestep(timestep_ms)

        self.i += 1
        delta = self.t0 + (self.timestep_ms / 1000) * self.i - time.time()
        if delta > 0:
            time.sleep(delta)
