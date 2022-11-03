class FB_Example_Model:
    def __init__(self):
        self.count = 1
        self.state = False

    def update(self):
        self.count += 1
        print(self.count)
