class PLCTask:
    def __init__(self, name: str, poll_rate: int, task: object):
        self.name = name
        self.poll_rate = poll_rate
        self.task = task

    def run(self):
        self.task.update()
