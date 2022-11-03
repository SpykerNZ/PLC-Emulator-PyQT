class FB_Example_Model:
    def __init__(self):
        self.count = 0
        self.state = False

    def update(self):
        if self.state:
            self.count += 1
            print(self.count)
