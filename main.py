import sys
from PyQt6.QtWidgets import QApplication
from GUI.PLC import PlcViewModel, PlcWindow
from PLC.main import Plc


def app():
    app = QApplication(sys.argv)
    plc = Plc(timestep_ms=10)
    plcView = PlcViewModel(plc)
    window = PlcWindow(plcView)
    window.show()
    app.exec()


if __name__ == "__main__":
    app()
