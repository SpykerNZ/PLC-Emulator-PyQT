from FunctionBlocks.example_model import FB_Example_Model
from FunctionBlocks.example_viewmodel import FB_Example_ViewModel
from PLC.tasks import PLC_PRG


class PRG_Example(PLC_PRG):
    def __init__(self):
        self.example_model = FB_Example_Model()
        self.example_viewmodel = FB_Example_ViewModel(self.example_model)

    def update(self):
        self.example_viewmodel.update_inputs()
        self.example_model.update()
        self.example_viewmodel.update_outputs()
