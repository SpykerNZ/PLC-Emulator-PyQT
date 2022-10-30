import sys
import traceback
from PyQt6.QtCore import (
    QRunnable,
    QObject,
    pyqtSignal,
)


class CallbackWorkerSignals(QObject):
    error = pyqtSignal(tuple)
    callback = pyqtSignal(object)


class CallbackWorker(QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super(CallbackWorker, self).__init__()
        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = CallbackWorkerSignals()
        # Add the callback to our kwargs
        self.kwargs["callback"] = self.signals.callback

    def run(self):
        # Retrieve args/kwargs here; and fire processing using them
        try:
            self.fn(*self.args, **self.kwargs)
        except Exception:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
