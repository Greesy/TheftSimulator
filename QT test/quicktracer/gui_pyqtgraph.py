# -*- coding: utf-8 -*-

'''
GUI for quicktracer
'''

from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import sys
import os
import threading
import json
import traceback
import importlib.util

from displays import default_display_classes

ANIMATION_UPDATE_INTERVAL = 10 # ms

# Globals
key_to_display = {}

# Protocol constants
KEY = 'k'
VALUE = 'v'
TIME = 't'
CUSTOM_DISPLAY = 'custom_display'
VIEW_BOX = 'view_box'

def read_input():
    global key_to_display
    try:
        while True:
            try:
                line = input()
            except EOFError as e:
                return
            message = json.loads(line)
            key = message[KEY]
            view_box = message.get(VIEW_BOX, None)
            if key not in key_to_display:
                plot = create_plot(message)
                plot.set_view_box_id(view_box)
                plot.set_title(view_box or key)
                plot.add_value(message)
                key_to_display[key] = plot
            else:
                key_to_display[key].add_value(message)
    except Exception as e:
        traceback.print_exc()
        sys.stdout.flush()
        sys.stderr.flush()
        sys.exit(-1)

def create_plot(message):
    global key_to_display
    key = message[KEY]
    value = message[VALUE]
    custom_display = message.get(CUSTOM_DISPLAY, None)
    if custom_display:
        module_path, display_class_name = custom_display
        sys.path.append(os.path.dirname(module_path))
        spec = importlib.util.spec_from_file_location(display_class_name, module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        display_class = getattr(module, display_class_name)
        return display_class()
    for display_class in default_display_classes:
        if display_class.accepts_value(value):
            display = display_class()
            return display
    raise Exception('unexpected datatype. key={} value={}: '.format(key, repr(value)))

class NonFocusStealingGraphicsWindow(pg.GraphicsWindow):
    def show(self):
        self.setAttribute(98) # Qt::WA_ShowWithoutActivating
        super().show()



def main():
    app = QtGui.QApplication([])
    win = NonFocusStealingGraphicsWindow(title='quicktracer')
    win.setGeometry(0, 30, 600, 600)

    threading.Thread(target=read_input, daemon=True).start()

    def update():
        global key_to_display
        try:
            for key in sorted(key_to_display):
                key_to_display[key].render_with_init(win)
        except Exception as e:
            traceback.print_exc()
            sys.stdout.flush()
            sys.stderr.flush()
    timer = QtCore.QTimer()
    timer.timeout.connect(update)
    timer.start(10)

    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()


if __name__ == '__main__':
    main()
