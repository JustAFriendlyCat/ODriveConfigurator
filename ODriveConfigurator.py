import sys
import odrive
import handlers

from PyQt6.QtWidgets import *
from PyQt6.uic import loadUi

app = QApplication(sys.argv)
window = QMainWindow()
loadUi("untitled.ui", window)

odrive.start_discovery(path='usb:idVendor=0x1209,idProduct=0x0D32,bInterfaceClass=0,bInterfaceSubClass=1,bInterfaceProtocol=0')

handler = handlers.GUI_Handler(window)

window.odriveTree.itemClicked.connect(lambda item: handler.odriveTreeHandler(item))
window.odriveSelect.clicked.connect(lambda: handler.odriveSelectHandler())
window.show()
app.exec()
