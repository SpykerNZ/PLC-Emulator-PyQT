from dataclasses import dataclass
from FunctionBlocks.example_model import FB_Example_Model


@dataclass
class FB_Example_ViewData:
    OUT_Count: int = 0


class FB_Example_ViewModel:
    def __init__(self, model: FB_Example_Model):
        self.model = model
        self.data = FB_Example_ViewData()

    def update_inputs(self):
        pass

    def update_outputs(self):
        self.data.OUT_Count = self.model.count
