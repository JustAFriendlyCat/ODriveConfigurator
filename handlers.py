import odrive
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
import params

class GUI_Handler:
    def __init__(self, window : QMainWindow):
        self.window = window
        self.drive = None
        self.currentWidget = self.window.general
        for widget in self.window.widgetGroup.children():
            widget.setVisible(False)

    #makes old widget not visible and sets new widget visible
    def setNewWidget(self, newWidget: str):
        self.currentWidget.setVisible(False)
        self.currentWidget = getattr(self.window, newWidget)
        self.currentWidget.setVisible(True)
    
    #handles odrive connection button
    def odriveSelectHandler(self):
        for item in self.window.odriveList.selectedItems():
            for drive_ in odrive.connected_devices:
                if int(item.text()) == drive_.serial_number:
                    self.drive = drive_
                    self.odriveTreeHandler(item=self.window.odriveTree.currentItem())

    #updates the axis parameters
    def updateParams(self, axis: int):
        if axis == 0:
            drive_axis = self.drive.axis0
        elif axis == 1:
            drive_axis = self.drive.axis1

        for k, v in params.textBoxes.items():
            getattr(self.window, k).setText(str(eval(v)))
            print(v)

        for k, v in params.selectors.items():
            if eval(v) == True:
                getattr(self.window, k).setCurrentIndex(0)
            else:
                getattr(self.window, k).setCurrentIndex(1)

        match drive_axis.requested_state:
            #state 5 doesnt exist
            case 6:
                self.window.requestedStateSelect.setCurrentIndex(5)
            case 7:
                self.window.requestedStateSelect.setCurrentIndex(6)
            case 8:
                self.window.requestedStateSelect.setCurrentIndex(7)
            case 9:
                self.window.requestedStateSelect.setCurrentIndex(8)
            case 10:
                self.window.requestedStateSelect.setCurrentIndex(9)
            case 11:
                self.window.requestedStateSelect.setCurrentIndex(10)
            case 12:
                self.window.requestedStateSelect.setCurrentIndex(11)
            case 13:
                self.window.requestedStateSelect.setCurrentIndex(12)  
            case _:
                self.window.requestedStateSelector.setCurrentIndex(drive_axis.requested_state)
        
        match drive_axis.encoder.config.mode:
            case 256:
                self.window.modeSelector.setCurrentIndex(3)
            case 257:
                self.window.modeSelector.setCurrentIndex(4)
            case 258:
                self.window.modeSelector.setCurrentIndex(5)
            case 259:
                self.window.modeSelector.setCurrentIndex(6)
            case 260:
                self.window.modeSelector.setCurrentIndex(7)
            case _:
                self.window.modeSelector.setCurrentIndex(drive_axis.encoder.config.mode)
            
    #handles the main navigator/tree
    def odriveTreeHandler(self, item):
        parent = item.parent()
        itemText = item.text(0)

        if self.drive != None and self.window.vbusVoltage.text() == "0.0V":
            if self.window.axisSelector.currentIndex() == 0:
                self.updateParams(0)
            elif self.window.axisSelector.currentIndex() == 1:
                self.updateParams(1)

        match itemText:
            case "General":
                self.setNewWidget("general")
                for device in odrive.connected_devices:
                    #if self.window.odriveList.findItems(str(device.serial_number), Qt.MatchContains):
                    #    break
                    self.window.odriveList.addItem(f"{device.serial_number}")
            case "Axis":
                self.setNewWidget("axisGeneral")
            case "Config":
                match parent.text(0):
                    case "Axis":   
                        self.setNewWidget("axisConfig")
                    case "Encoder":
                        self.setNewWidget("encoderConfig")
                    case "Controller":
                        self.setNewWidget("controllerConfig")
                    case "Can":
                        self.setNewWidget("canConfig")
            case "General Lockin":
                self.setNewWidget("generalLockin")
            case "Sensorless Ramp":
                self.setNewWidget("sensorlessRamp")
            case "Calibration Lockin":
                self.setNewWidget("calibrationLockin")
            case "Controller":
                self.setNewWidget("controllerGeneral")     
            case "Autotuning":
                self.setNewWidget("controllerAutotuning")
            case "Encoder":
                self.setNewWidget("encoderGeneral")
            case "Motor":
                self.setNewWidget("motor")
            case "Can":
                if parent == None:
                    self.setNewWidget("canGeneral")
                    pass
                elif parent.text(0) == "Config":
                    self.setNewWidget("axisCanConfig")
                elif parent.text(0) == "ODrive":
                    self.setNewWidget("canGeneral")