from dataclasses import dataclass
import time
from FunctionBlocks.example_model import FB_Example_Model
from PyQt6.QtCore import (
    pyqtBoundSignal,
)


@dataclass
class FB_Example_ViewData:
    PB_State: bool = False
    OUT_Count: int = 0
    OUT_State: bool = False

    def update(self, callback: pyqtBoundSignal):
        while True:
            callback.emit(self)
            time.sleep(0.1)


class FB_Example_ViewModel:
    def __init__(
        self, model: FB_Example_Model, view_data: FB_Example_ViewData
    ):
        self.data = view_data
        self.model = model

    def update_inputs(self):
        self.model.state = self.data.PB_State

    def update_outputs(self):
        self.data.OUT_Count = self.model.count
        self.data.OUT_State = self.model.state
