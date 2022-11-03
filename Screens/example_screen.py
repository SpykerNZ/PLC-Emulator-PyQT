from PyQt6 import uic
from PyQt6.QtCore import (
    QThreadPool,
)
from PyQt6.QtWidgets import QMainWindow, QLabel, QPushButton
from GUI.workers import CallbackWorker
from FunctionBlocks.example_viewmodel import FB_Example_ViewData


class ExampleWindow(QMainWindow):
    def __init__(self, view_data: FB_Example_ViewData):
        super().__init__()
        uic.load_ui.loadUi("./Screens/example.ui", self)
        self.view_data = view_data

        self.label_count: QLabel = self.findChild(QLabel, "countOutputLabel")
        self.label_state: QLabel = self.findChild(QLabel, "stateOutputLabel")

        self.button_state: QPushButton = self.findChild(
            QPushButton, "stateButton"
        )

        self.button_state.pressed.connect(lambda: self.button_press())
        self.button_state.released.connect(lambda: self.button_released())

        self.threadpool = QThreadPool()
        self.worker = CallbackWorker(self.view_data.update)
        self.worker.signals.callback.connect(self.callback)
        self.threadpool.start(self.worker)

    def button_press(self):
        self.view_data.PB_State = True

    def button_released(self):
        self.view_data.PB_State = False

    def callback(self, view_data: FB_Example_ViewData):
        self.label_count.setText(str(view_data.OUT_Count))
        self.label_state.setText(str(view_data.OUT_State))
