import sys, traceback
import os
import time
from PyQt6 import uic
from PyQt6.QtCore import QRunnable, QThreadPool, QObject, pyqtSignal
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLCDNumber

class RealtimePLC:
    
    def __init__(self):
        self.time_ms = 0
        self.timestep_ms = 20
        self.run_time_ms = 5000
        self.state = False
    
    def run(self, plc_callback):
        print("PLC Running")
        self.time_ms = 0
        while self.time_ms<self.run_time_ms:
            time.sleep(self.timestep_ms/1000)
            self.time_ms+=self.timestep_ms
            plc_callback.emit(self)
        print("PLC Finished")
        

class WorkerSignals(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    plc = pyqtSignal(RealtimePLC)

class Worker(QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()
        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()
        # Add the callback to our kwargs
        self.kwargs['plc_callback'] = self.signals.plc

    def run(self):
        # Retrieve args/kwargs here; and fire processing using them
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        print(os.getcwd())
        uic.load_ui.loadUi("./ui/gui.ui", self)
        
        self.button_plc_run = self.findChild(QPushButton, 'plcRunButton')
        self.button_plc_run.clicked.connect(self.run_plc)
        
        self.button_plc_state = self.findChild(QPushButton, 'plcSwapStateButton')
        self.button_plc_state.clicked.connect(self.swap_plc_state)
        
        self.lcd_number = self.findChild(QLCDNumber, 'number')
        
        self.threadpool = QThreadPool()
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())
        
        self.plc = RealtimePLC()
        
    def run_plc(self):
        
        worker = Worker(self.plc.run)
        worker.signals.plc.connect(self.callback)
        self.threadpool.start(worker)
        
    def swap_plc_state(self):
        self.plc.state = not self.plc.state
        
    def callback(self, plc: RealtimePLC):
        print(plc.time_ms)
        print(plc.state)
        self.lcd_number.display(int(plc.state))

def app():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()    

if __name__ == '__main__':
    app()