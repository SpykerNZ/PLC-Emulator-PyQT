import sys
from PyQt6.QtWidgets import QApplication
from GUI.PLC import PlcViewModel, PlcWindow
from PLC.main import Plc
from PLC.tasks import PLCTask
from Programs.example import PRG_Example


def app():
    app = QApplication(sys.argv)

    program = PRG_Example()
    task = PLCTask(name="Example Program", poll_rate=50, task=program)

    plc = Plc(timestep_ms=10)
    plc.add_task(task)

    plc_view = PlcViewModel(plc)
    plc_window = PlcWindow(plc_view)
    plc_window.show()
    app.exec()


if __name__ == "__main__":
    app()
