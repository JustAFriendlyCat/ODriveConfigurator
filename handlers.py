import odrive
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6 import QtCore
import params

class GUI_Handler:
    def __init__(self, window : QMainWindow):
        self.window = window
        self.drive = None
        self.drive_axis = None
        self.currentBox = self.window.generalBox

        #set all boxes to not visible
        skipFirst = 0
        for widget in self.window.scrollAreaWidgetContents.children():
            if skipFirst == 0:
                skipFirst = 1
                continue
            
            widget.setVisible(False)
        else:
            #set generalBox to visible
            self.currentBox.setVisible(True)
        
        #set all send buttons clicked handler to sendButtonHandler()
        for button in params.sendButtons:
            eval(f"self.window.{button}.clicked.connect(self.sendButtonHandler)")

        #set all controls buttons clicked handler to controlButtonHandler()
        for button in params.controls:
            eval(f"self.window.{button}.clicked.connect(self.controlButtonHandler)")

    #makes old widget not visible and sets new widget visible
    def setNewBox(self, newBox: str):
        self.currentBox.setVisible(False)
        self.currentBox = getattr(self.window, newBox)
        self.currentBox.setVisible(True)
    
    #handles odrive connection button
    def odriveSelectHandler(self):
        for item in self.window.odriveList.selectedItems():
            for drive_ in odrive.connected_devices:
                if int(item.text()) == drive_.serial_number:
                    self.drive = drive_
                    self.odriveTreeHandler(item=self.window.odriveTree.currentItem())

    #handles control buttons
    def controlButtonHandler(self):
        if self.drive != None:
            buttonPressedName = self.window.sender().objectName()

            match buttonPressedName:
                case "reboot":
                    self.drive.reboot()
                case "clearErrors":
                    self.drive.clear_errors()
                    self.updateParams()
                case "saveConfiguration":
                    self.drive.save_configuration()
                case "eraseConfiguration":
                    confirmMessageBox = QMessageBox.question(self.window, "Confirm?", "Are you sure you want to erase the configuration?")
                    if confirmMessageBox == QMessageBox.StandardButton.Yes:
                        self.drive.erase_configuration()
                
    #handles all send buttons
    def sendButtonHandler(self):
        buttonPressed = self.window.sender()
            
        paramPrefix = buttonPressed.objectName()[:-4]
        
        if f"{paramPrefix}Text" in params.textBoxes:
            woa = eval(f"self.window.{paramPrefix}Text").text()
            s = params.textBoxes[f"{paramPrefix}Text"]
        #elif f"{paramPrefix}Selector" in params.selectors:
        else:
            woa = eval(f"self.window.{paramPrefix}Selector").currentIndex()
            s = params.selectors[f"{paramPrefix}Selector"]

        
        splitString = s.rsplit('.', 1)
        #['self.drive.can.config', 'baud_rate']

        setattr(eval(splitString[0]), splitString[1], woa)
        #      self.drive.can.config  baud_rate       textbox value               

        self.updateParams()

        #"encoderModeSelector": "drive_axis.encoder.config.mode"
        #"requestedStateSelector": "drive_axis.requested_state"

    #updates the axis parameters
    def updateParams(self):
        if self.window.axisSelector.currentIndex() == 0:
            self.drive_axis = self.drive.axis0
        elif self.window.axisSelector.currentIndex() == 1:
            self.drive_axis = self.drive.axis1

        for k, v in params.textBoxes.items():
            getattr(self.window, k).setText(str(eval(v)))
            print(v)

        for k, v in params.selectors.items():
            if eval(v) == True:
                getattr(self.window, k).setCurrentIndex(1)
            else:
                getattr(self.window, k).setCurrentIndex(0)

        match self.drive_axis.requested_state:
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
                self.window.requestedStateSelector.setCurrentIndex(self.drive_axis.requested_state)
        
        match self.drive_axis.encoder.config.mode:
            case 256:
                self.window.encoderModeSelector.setCurrentIndex(3)
            case 257:
                self.window.encoderModeSelector.setCurrentIndex(4)
            case 258:
                self.window.encoderModeSelector.setCurrentIndex(5)
            case 259:
                self.window.encoderModeSelector.setCurrentIndex(6)
            case 260:
                self.window.encoderModeSelector.setCurrentIndex(7)
            case _:
                self.window.encoderModeSelector.setCurrentIndex(self.drive_axis.encoder.config.mode)
    
    #handles the main navigator/tree
    def odriveTreeHandler(self, item):
        parent = item.parent()
        itemText = item.text(0)

        if self.drive != None and self.window.vbusVoltage.text() == "0.0V":
            self.updateParams()

        match itemText:
            case "General":
                self.setNewBox("generalBox")
                for device in odrive.connected_devices:
                    if self.window.odriveList.findItems(str(device.serial_number), QtCore.Qt.MatchFlag.MatchContains):
                        continue
                    self.window.odriveList.addItem(str(device.serial_number))
            case "Axis":
                self.setNewBox("axisGeneralBox")
            case "Config":
                match parent.text(0):
                    case "Axis":   
                        self.setNewBox("axisConfigBox")
                    case "Encoder":
                        self.setNewBox("encoderConfigBox")
                    case "Controller":
                        self.setNewBox("controllerConfigBox")
                    case "Can":
                        self.setNewBox("canConfigBox")
                    case "Motor":
                        self.setNewBox("motorConfigBox")
            case "General Lockin":
                self.setNewBox("generalLockinBox")
            case "Sensorless Ramp":
                self.setNewBox("sensorlessRampBox")
            case "Calibration Lockin":
                self.setNewBox("calibrationLockinBox")
            case "Controller":
                self.setNewBox("controllerGeneralBox")     
            case "Autotuning":
                self.setNewBox("controllerAutotuningBox")
            case "Encoder":
                self.setNewBox("encoderGeneralBox")
            case "Motor":
                self.setNewBox("motorBox")
            case "Can":
                if parent == None:
                    self.setNewBox("canGeneralBox")
                    pass
                elif parent.text(0) == "Config":
                    self.setNewBox("axisCanConfigBox")
                elif parent.text(0) == "ODrive":
                    self.setNewBox("canGeneralBox")