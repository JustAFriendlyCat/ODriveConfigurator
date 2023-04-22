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
        
        #set all boxes to not visible and skip first element because it is the grid layout
        for widget in self.window.scrollAreaWidgetContents.children()[1:]:
            widget.setVisible(False)
        else:
            #set generalBox to visible
            self.currentBox.setVisible(True)
        
        #update parameters every second
        timer = QTimer(self.window)
        timer.timeout.connect(self.updateParams)
        timer.start(1000)

        #set odrivetree and odriveselect button to appropriate handlers
        self.window.odriveTree.itemClicked.connect(lambda item: self.odriveTreeHandler(item))
        self.window.odriveSelect.clicked.connect(self.odriveSelectHandler)

        #set all textboxes and selectors to setOnEdit(), editingFinished and activated are important because they dont emit signal when value is programmatically changed 
        for textBox in params.textBoxes:
            getattr(self.window, textBox).editingFinished.connect(self.setOnEdit)
        for selector in params.selectors:
            getattr(self.window, selector).activated.connect(self.setOnEdit)

        #error reporting stuff
        for textBox in params.textBoxes:
            if "ErrorText" in textBox:
                getattr(self.window, textBox).textChanged.connect(self.errorReporting)

        #set all controls buttons clicked handler to controlButtonHandler()
        for button in params.controls:
            getattr(self.window, button).clicked.connect(self.controlButtonHandler)

    def errorReporting(self):
        name = self.window.sender().objectName()

        splitString = params.textBoxes[name].rsplit('.', 1)
        currentCode = getattr(eval(splitString[0]), splitString[1])

        if currentCode != 0:
            self.window.debugConsole.appendPlainText(f"[ERROR] Encounted {name[:-9]} error with code: {currentCode}")

    def setOnEdit(self):
        if self.drive == None: return

        name = self.window.sender().objectName()
        
        if "Text" in name:
            value = getattr(self.window, name).text()
            s = params.textBoxes[name]
        elif "Selector" in name:
            value = getattr(self.window, name).currentIndex()
            s = params.selectors[name]

        splitString = s.rsplit('.', 1)
        #['self.drive.can.config', 'baud_rate']

        setattr(eval(splitString[0]), splitString[1], value)
        #      self.drive.can.config  baud_rate       textbox value  

        self.window.debugConsole.appendPlainText(f"[DEBUG] Set {s} to {value}")

    #makes old widget not visible and sets new widget visible
    def setNewBox(self, newBox: str):
        self.currentBox.setVisible(False)
        self.currentBox = getattr(self.window, newBox)
        self.currentBox.setVisible(True)
    
    #handles odrive connection button
    def odriveSelectHandler(self):
        if len(self.window.odriveList.selectedItems()) == 0: return

        item = self.window.odriveList.selectedItems()[0]

        for drive in odrive.connected_devices:
            if int(item.text()) == drive.serial_number:
                self.drive = drive
                self.window.debugConsole.appendPlainText(f"[DEBUG] Connected to ODrive {drive.serial_number}")

    #handles control buttons
    def controlButtonHandler(self):
        if self.drive == None: return
        
        buttonPressedName = self.window.sender().objectName()

        match buttonPressedName:
            case "reboot":
                self.drive.reboot()
            case "clearErrors":
                self.drive.clear_errors()
                self.window.debugConsole.appendPlainText(f"[DEBUG] Cleared Errors")
            case "saveConfiguration":
                self.drive.save_configuration()
            case "eraseConfiguration":
                confirmMessageBox = QMessageBox.question(self.window, "Confirm?", "Are you sure you want to erase the configuration?")
                if confirmMessageBox == QMessageBox.StandardButton.Yes:
                    self.drive.erase_configuration()

    #updates the axis parameters
    def updateParams(self):
        for device in odrive.connected_devices:
            if self.window.odriveList.findItems(str(device.serial_number), QtCore.Qt.MatchFlag.MatchContains):
                continue
            self.window.odriveList.addItem(str(device.serial_number))
            self.window.debugConsole.appendPlainText(f"[DEBUG] Found new ODrive {device.serial_number}")

        if self.drive == None: return
        
        self.drive_axis = getattr(self.drive, f"axis{self.window.axisSelector.currentIndex()}")

        for k, v in params.textBoxes.items():
            textBox = getattr(self.window, k)
            if not textBox.hasFocus():
                textBox.setText(str(eval(v)))

        for k, v in params.selectors.items():
            getattr(self.window, k).setCurrentIndex(int(eval(v)))

        self.window.requestedStateSelector.setCurrentIndex(self.drive_axis.current_state)
        self.window.inputModeSelector.setCurrentIndex(self.drive_axis.controller.config.input_mode)
        self.window.controlModeSelector.setCurrentIndex(self.drive_axis.controller.config.control_mode)

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

        match itemText:
            case "General":
                self.setNewBox("generalBox")
            case "Axis":
                self.setNewBox("axisGeneralBox")
            case "Config":
                if parent != None:
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
                else:
                    self.setNewBox("config")
                
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