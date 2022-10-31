import time
from PyQt6 import uic
from PyQt6.QtCore import (
    QThreadPool,
    pyqtBoundSignal,
)
from PyQt6.QtWidgets import (
    QMainWindow,
    QPushButton,
    QLabel,
    QSpinBox,
)
from GUI.workers import CallbackWorker
from PLC.main import Plc
from PLC.sleep import RealtimeSleeper


class PlcViewModel:
    def __init__(self, plc: Plc):
        self.plc = plc
        self.realtime = RealtimeSleeper()

    def run(self, callback: pyqtBoundSignal):
        while True:
            self.plc.update()
            callback.emit(self)
            self.realtime.sleep(self.plc.timestep_ms)

    def start(self):
        self.plc.start()

    def pause(self):
        self.plc.pause()

    def reset(self):
        self.plc.reset()

    def set_timestep(self, time_ms: int):
        self.plc.timestep_ms = time_ms


class PlcWindow(QMainWindow):
    def __init__(self, plc_view: PlcViewModel):
        super().__init__()
        uic.load_ui.loadUi("./GUI/plc_control.ui", self)
        self.plc_view = plc_view

        self.button_plc_start: QPushButton = self.findChild(
            QPushButton, "plcStartButton"
        )
        self.button_plc_pause: QPushButton = self.findChild(
            QPushButton, "plcPauseButton"
        )
        self.button_plc_reset: QPushButton = self.findChild(
            QPushButton, "plcResetButton"
        )
        self.label_plc_rtc_time: QLabel = self.findChild(
            QLabel, "rtcTimeOutputLabel"
        )
        self.label_plc_cycle_count: QLabel = self.findChild(
            QLabel, "cycleCountOutputLabel"
        )
        self.spinbox_plc_timestep: QSpinBox = self.findChild(
            QSpinBox, "timestepSpinBox"
        )

        self.threadpool = QThreadPool()

        self.spinbox_plc_timestep.setValue(self.plc_view.plc.timestep_ms)

        self.button_plc_start.clicked.connect(self.plc_view.plc.start)
        self.button_plc_pause.clicked.connect(self.plc_view.plc.pause)
        self.button_plc_reset.clicked.connect(self.plc_view.plc.reset)
        self.spinbox_plc_timestep.valueChanged.connect(
            lambda: self.plc_view.set_timestep(
                self.spinbox_plc_timestep.value()
            )
        )

        self.plc_worker = CallbackWorker(self.plc_view.run)
        self.plc_worker.signals.callback.connect(self.callback)
        self.threadpool.start(self.plc_worker)

    def callback(self, plc_view: PlcViewModel):
        self.label_plc_rtc_time.setText(str(plc_view.plc.time_ms) + "ms")
        self.label_plc_cycle_count.setText(
            str(plc_view.plc.tasks[0].cycle_count)
        )
