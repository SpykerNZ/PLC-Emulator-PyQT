from PyQt6 import uic
from PyQt6.QtCore import (
    QThreadPool,
)
from PyQt6.QtWidgets import (
    QMainWindow,
    QLabel,
)
from GUI.workers import CallbackWorker
from FunctionBlocks.example_viewmodel import FB_Example_ViewData


class ExampleWindow(QMainWindow):
    def __init__(self, view_data: FB_Example_ViewData):
        super().__init__()
        uic.load_ui.loadUi("./GUI/plc_control.ui", self)
        self.view_data = view_data

        self.label_count: QLabel = self.findChild(QLabel, "countOutputLabel")

        self.threadpool = QThreadPool()
        self.worker = CallbackWorker(self.plc_view.run)
        self.worker.signals.callback.connect(self.callback)
        self.threadpool.start(self.worker)

    def callback(self, plc_view: FB_Example_ViewData):
        self.label_plc_rtc_time.setText(str(plc_view.plc.time_ms) + "ms")
        self.label_plc_cycle_count.setText(str(plc_view.plc.task.cycle_count))
