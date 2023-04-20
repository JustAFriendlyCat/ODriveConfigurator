import sys
import odrive
import handlers
import qdarktheme

from PyQt6.QtWidgets import *
from PyQt6.uic import loadUi

app = QApplication(sys.argv)

qdarktheme.setup_theme("light")

window = QMainWindow()
loadUi("untitled.ui", window)

odrive.start_discovery(path='usb:idVendor=0x1209,idProduct=0x0D32,bInterfaceClass=0,bInterfaceSubClass=1,bInterfaceProtocol=0')

handler = handlers.GUI_Handler(window)
window.show()
app.exec()
