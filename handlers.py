import odrive
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *

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
    
    #handles both axisGeneral widgets
    def axisGeneral(self, axis : int):
        drive_axis = getattr(self.drive, f'axis{axis}')

        self.window.currentStateText.setText(str(drive_axis.current_state))
        self.window.requestedStateSelector.setCurrentIndex(drive_axis.requested_state)
        self.window.axisErrorText.setText(str(drive_axis.error))
        self.window.isHomedText.setText(str(drive_axis.is_homed))
        self.window.lastDriverFaultText.setText(str(drive_axis.last_drv_fault))
        self.window.stepDirActiveText.setText(str(drive_axis.step_dir_active))
        self.window.stepsText.setText(str(drive_axis.steps))

    #handles odrive connection button
    def odriveSelectHandler(self):
        for item in self.window.odriveList.selectedItems():
            for drive_ in odrive.connected_devices:
                if int(item.text()) == drive_.serial_number:
                    self.drive = drive_
                    self.odriveTreeHandler(item=self.window.odriveTree.currentItem())
    
    #handles the main navigator/tree
    def odriveTreeHandler(self, item):
        parent = item.parent()
        item = item.text(0)

        match item:
            case "General":
                self.setNewWidget("general")
                if self.drive != None:
                    self.window.serialNumber.setText(str(self.drive.serial_number))
                    self.window.softwareVersion.setText(f"{self.drive.fw_version_major}.{self.drive.fw_version_minor}.{self.drive.fw_version_revision}")
                    self.window.hardwareVersion.setText(f"{self.drive.hw_version_major}.{self.drive.hw_version_minor}.{self.drive.hw_version_variant}")
                    self.window.vbusVoltage.setText(str(self.drive.vbus_voltage))
                for device in odrive.connected_devices:
                    #if self.window.odriveList.findItems(str(device.serial_number), Qt.MatchContains):
                    #    break
                    self.window.odriveList.addItem(f"{device.serial_number}")

            case "Axis0":
                self.setNewWidget("axisGeneral")
                if self.drive != None:
                    self.axisGeneral(0)
            case "Axis1":
                self.setNewWidget("axisGeneral")
                if self.drive != None:
                    self.axisGeneral(1)

            case "Config":
                match parent.text(0):
                    case "Axis0":   
                        self.setNewWidget("axisConfig")
                    case "Axis1":
                        self.setNewWidget("axisConfig")
                    case "Encoder":
                        self.setNewWidget("encoderConfig")
                    case "Controller":
                        self.setNewWidget("controllerConfig")
                    case "Can":
                        self.setNewWidget("canConfig")
            
            case "General Lockin":
                self.setNewWidget("lockinConfig")
            case "Sensorless Ramp":
                self.setNewWidget("lockinConfig")

            case "Calibration Lockin":
                self.setNewWidget("calibrationLockin")

            case "Controller":
                print(parent.text(0))
                self.setNewWidget("controllerGeneral")
            
            case "Autotuning":
                self.setNewWidget("controllerAutotuning")

            case "Encoder":
                self.setNewWidget("encoderGeneral")

            case "Motor":
                self.setNewWidget("motor")
            case "Can":
                match parent.text(0):
                    case "Config":
                        self.setNewWidget("axisCanConfig")
                    case "ODrive":
                        self.setNewWidget("canGeneral")
