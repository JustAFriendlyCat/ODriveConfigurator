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

        self.window.axisErrorText.setText(str(drive_axis.error))
        self.window.isHomedText.setText(str(drive_axis.is_homed))
        self.window.lastDriverFaultText.setText(str(drive_axis.last_drv_fault))
        self.window.stepDirActiveText.setText(str(drive_axis.step_dir_active))
        self.window.stepsText.setText(str(drive_axis.steps))
    
    #handles both axisConfig widgets
    def axisConfig(self, axis : int):
        drive_axis = getattr(self.drive, f'axis{axis}')
        config = drive_axis.config

        match config.enable_step_dir:
            case True:
                self.window.enableStepDirSelector.setCurrentIndex(0)
            case False:
                self.window.enableStepDirSelector.setCurrentIndex(1)

        match config.step_dir_always_on:
            case True:
                self.window.stepDirAlwaysOnSelector.setCurrentIndex(0)
            case False:
                self.window.stepDirAlwaysOnSelector.setCurrentIndex(1)
        
        self.window.dirGPIOPinText.setText(str(config.dir_gpio_pin))
        self.window.stepGPIOPinText.setText(str(config.step_gpio_pin))

        match config.startup_closed_loop_control:
            case True:
                self.window.startupClosedLoopControlSelector.setCurrentIndex(0)
            case False:
                self.window.startupClosedLoopControlSelector.setCurrentIndex(1)

        match config.startup_encoder_index_search:
            case True:
                self.window.startupEncoderIndexSearchSelector.setCurrentIndex(0)
            case False:
                self.window.startupEncoderIndexSearchSelector.setCurrentIndex(1)

        match config.startup_encoder_offset_calibration:
            case True:
                self.window.startupEncoderOffsetCalibrationSelector.setCurrentIndex(0)
            case False:
                self.window.startupEncoderOffsetCalibrationSelector.setCurrentIndex(1)

        match config.startup_homing:
            case True:
                self.window.startupHomingSelector.setCurrentIndex(0)
            case False:
                self.window.startupHomingSelector.setCurrentIndex(1)
            
        match config.startup_motor_calibration:
            case True:
                self.window.startupMotorCalibrationSelector.setCurrentIndex(0)
            case False:
                self.window.startupMotorCalibrationSelector.setCurrentIndex(1)

        match config.enable_watchdog:
            case True:
                self.window.enableWatchdogSelector.setCurrentIndex(0)
            case False:
                self.window.enableWatchdogSelector.setCurrentIndex(1)

        self.window.watchdogTimeoutText.setText(str(config.watchdog_timeout))

        match config.enable_sensorless_mode:
            case True:
                self.window.enableSensorlessModeSelector.setCurrentIndex(0)
            case False:
                self.window.enableSensorlessModeSelector.setCurrentIndex(1)

    #handles both controllerGeneral widgets
    def controllerGeneral(self, axis : int):
        drive_axis = getattr(self.drive, f'axis{axis}')
        drive_controller = drive_axis.controller

        self.window.controllerErrorText.setText(str(drive_controller.error))
        self.window.lastErrorTimeText.setText(str(drive_controller.last_error_time))
        self.window.inputPositionText.setText(str(drive_controller.input_pos))
        self.window.inputVelocityText.setText(str(drive_controller.input_vel))
        self.window.inputTorqueText.setText(str(drive_controller.input_torque))
        self.window.positionSetpointText.setText(str(drive_controller.pos_setpoint))
        self.window.torqueSetpointText.setText(str(drive_controller.torque_setpoint))
        self.window.velocitySetpointText.setText(str(drive_controller.vel_setpoint))
        self.window.anticoggingValidText.setText(str(drive_controller.anticogging_valid))
        self.window.autotuningPhaseText.setText(str(drive_controller.autotuning_phase))
        self.window.electricalPowerText.setText(str(drive_controller.electrical_power))
        self.window.mechanicalPowerText.setText(str(drive_controller.mechanical_power))
        self.window.trajectoryDoneText.setText(str(drive_controller.trajectory_done))
        self.window.velocityIntegratorTorqueText.setText(str(drive_controller.vel_integrator_torque))

    #handles both controllerConfig widgets
    def controllerConfig(self, axis : int):
        drive_axis = getattr(self.drive, f'axis{axis}')
        config = drive_axis.controller.config

        self.window.controlModeSelector.setCurrentIndex(config.control_mode)
        self.window.inputModeSelector.setCurrentIndex(config.input_mode)

        match config.enable_overspeed_error:
            case True:
                self.window.enableOverspeedErrorSelector.setCurrentIndex(0)
            case False:
                self.window.enableOverspeedErrorSelector.setCurrentIndex(1)

        self.window.homingSpeedText.setText(str(config.homing_speed))
        self.window.inertiaText.setText(str(config.inertia))
        self.window.loadEncoderAxisText.setText(str(config.load_encoder_axis))
        self.window.positionGainText.setText(str(config.pos_gain))
        self.window.velocityGainText.setText(str(config.vel_gain))
        self.window.velocityIntegratorGainText.setText(str(config.vel_integrator_gain))

        match config.enable_vel_limit:
            case True:
                self.window.enableVelocityLimitSelector.setCurrentIndex(0)
            case False:
                self.window.enableVelocityLimitSelector.setCurrentIndex(1)
        
        match config.enable_torque_mode_vel_limit:
            case True:
                self.window.enableTorqueModeVelocityLimitSelector.setCurrentIndex(0)
            case False:
                self.window.enableTorqueModeVelocityLimitSelector.setCurrentIndex(1)
        
        self.window.velocityLimitText.setText(str(config.vel_limit))
        self.window.velocityLimitToleranceText.setText(str(config.vel_limit_tolerance))
        self.window.velocityIntegratorLimitText.setText(str(config.vel_integrator_limit))

        self.window.spinoutMechanicalPowerThresholdText.setText(str(config.spinout_mechanical_power_threshold))
        self.window.spinoutElectricalPowerThresholdText.setText(str(config.spinout_electrical_power_threshold))

        match config.enable_gain_scheduling:
            case True:
                self.window.enableGainSchedulingSelector.setCurrentIndex(0)
            case False:
                self.window.enableGainSchedulingSelector.setCurrentIndex(1)
        
        self.window.gainSchedulingWidthText.setText(str(config.gain_scheduling_width))

        self.window.torqueRampRateText.setText(str(config.torque_ramp_rate))
        self.window.velocityRampRateText.setText(str(config.vel_ramp_rate))

        self.window.inputFilterBandwidthText.setText(str(config.input_filter_bandwidth))
        self.window.mechanicalPowerBandwidthText.setText(str(config.mechanical_power_bandwidth))
        self.window.electricalPowerBandwidthText.setText(str(config.electrical_power_bandwidth))

        match config.circular_setpoints:
            case True:
                self.window.circularSetpointsSelector.setCurrentIndex(0)
            case False:
                self.window.circularSetpointsSelector.setCurrentIndex(1)

        self.window.circularSetpointRangeText.setText(str(config.circular_setpoint_range))

        self.window.axisToMirrorText.setText(str(config.axis_to_mirror))
        self.window.mirrorRatioText.setText(str(config.mirror_ratio))
        self.window.torqueMirrorRatioText.setText(str(config.torque_mirror_ratio))
        
    #handles both controllerAutotuning widgets
    def controllerAutotuning(self, axis : int):
        drive_axis = getattr(self.drive, f'axis{axis}')
        autotuning = drive_axis.controller.autotuning

        self.window.frequencyText.setText(str(autotuning.frequency))
        self.window.positionAmplitudeText.setText(str(autotuning.pos_amplitude))
        self.window.velocityAmplitudeText.setText(str(autotuning.vel_amplitude))
        self.window.torqueAmplitudeText.setText(str(autotuning.torque_amplitude))

    #handles both encoderGeneral widgets
    def encoderGeneral(self, axis : int):
        drive_axis = getattr(self.drive, f'axis{axis}')
        encoder = drive_axis.encoder

        self.window.errorText.setText(str(encoder.error))
        self.window.spiErrorRateText.setText(str(encoder.spi_error_rate))

        #set linear count

        self.window.isReadyText.setText(str(encoder.is_ready))
        self.window.indexFoundText.setText(str(encoder.index_found))
        self.window.shadowCountText.setText(str(encoder.shadow_count))
        self.window.countInCprText.setText(str(encoder.count_in_cpr))
        self.window.interpolationText.setText(str(encoder.interpolation))
        self.window.phaseText.setText(str(encoder.phase))
        self.window.hallStateText.setText(str(encoder.hall_state))

        self.window.linearPositionEstimateText.setText(str(encoder.pos_estimate))
        self.window.linearPositionEstimateCountsText.setText(str(encoder.pos_estimate_counts))
        self.window.circularPositionEstimateText.setText(str(encoder.pos_circular))
        self.window.circularPositionEstimateCprCountsText.setText(str(encoder.pos_cpr_counts))
        self.window.circularPositionDeltaCprCountsText.setText(str(encoder.delta_pos_cpr_counts))

        self.window.velocityEstimateText.setText(str(encoder.vel_estimate))
        self.window.velocityEstimateCountsText.setText(str(encoder.vel_estimate_counts))
        self.window.calibrationScanResponseText.setText(str(encoder.calib_scan_response))
        self.window.absolutePositionText.setText(str(encoder.pos_abs))

    #handles both encoderConfig widgets
    def encoderConfig(self, axis : int):
        drive_axis = getattr(self.drive, f'axis{axis}')
        encoderConfig = drive_axis.encoder.config

        match encoderConfig.mode:
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
                self.window.modeSelector.setCurrentIndex(encoderConfig.mode)

        self.window.cprText.setText(str(encoderConfig.cpr))
        
        match encoderConfig.pre_calibrated:
            case True:
                self.window.preCalibratedSelector.setCurrentIndex(0)
            case False:
                self.window.preCalibratedSelector.setCurrentIndex(1)
        
        match encoderConfig.use_index:
            case True:
                self.window.useIndexSelector.setCurrentIndex(0)
            case False:
                self.window.useIndexSelector.setCurrentIndex(1)

        self.window.indexOffsetText.setText(str(encoderConfig.index_offset))
        
        match encoderConfig.use_index_offset:
            case True:
                self.window.useIndexOffsetSelector.setCurrentIndex(0)
            case False:
                self.window.useIndexOffsetSelector.setCurrentIndex(1)

        match encoderConfig.enable_phase_interpolation:
            case True:
                self.window.enablePhaseInterpolationSelector.setCurrentIndex(0)
            case False:
                self.window.enablePhaseInterpolationSelector.setCurrentIndex(1)
        
        match encoderConfig.find_idx_on_lockin_only:
            case True:
                self.window.findIndexOnLockinOnlySelector.setCurrentIndex(0)
            case False:
                self.window.findIndexOnLockinOnlySelector.setCurrentIndex(1)

        self.window.directionText.setText(str(encoderConfig.direction))
        self.window.phaseOffsetText.setText(str(encoderConfig.phase_offset))
        self.window.phaseOffsetFloatText.setText(str(encoderConfig.phase_offset_float))
        self.window.bandwidthText.setText(str(encoderConfig.bandwidth))
        self.window.calibrationRangeText.setText(str(encoderConfig.calib_range))
        self.window.calibrationScanDistanceText.setText(str(encoderConfig.calib_scan_distance))
        self.window.calibrationScanOmegaText.setText(str(encoderConfig.calib_scan_omega))

        self.window.hallPolarityText.setText(str(encoderConfig.hall_polarity))

        match encoderConfig.hall_polarity_calibrated:
            case True:
                self.window.hallPolarityCalibratedSelector.setCurrentIndex(0)
            case False:
                self.window.hallPolarityCalibratedSelector.setCurrentIndex(1)
        
        match encoderConfig.ignore_illegal_hall_state:
            case True:
                self.window.ignoreIllegalHallStateSelector.setCurrentIndex(0)
            case False:
                self.window.ignoreIllegalHallStateSelector.setCurrentIndex(1)
        
        self.window.absoluteSpiCsGpioPinText.setText(str(encoderConfig.abs_spi_cs_gpio_pin))
        self.window.sinCosGpioPinSinText.setText(str(encoderConfig.sincos_gpio_pin_sin))
        self.window.sinCosGpioPinCosText.setText(str(encoderConfig.sincos_gpio_pin_cos))


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
        itemText = item.text(0)

        match itemText:
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
                print(parent.text(0))
                match parent.text(0):
                    case "Axis0":   
                        self.setNewWidget("axisConfig")
                        if self.drive != None:
                            self.axisConfig(0)

                    case "Axis1":
                        self.setNewWidget("axisConfig")
                        if self.drive != None:
                            self.axisConfig(1)

                    case "Encoder":
                        self.setNewWidget("encoderConfig")
                        if self.drive != None:
                            parent = parent.parent()
                            if parent.text(0) == "Axis0":
                                self.encoderConfig(0)
                            elif parent.text(0) == "Axis1":
                                self.encoderConfig(1)

                    case "Controller":
                        self.setNewWidget("controllerConfig")
                        if self.drive != None:
                            parent = parent.parent()
                            if parent.text(0) == "Axis0":
                                self.controllerConfig(0)
                            elif parent.text(0) == "Axis1":
                                self.controllerConfig(1)
                    case "Can":
                        self.setNewWidget("canConfig")
            
            case "General Lockin":
                self.setNewWidget("lockinConfig")
            case "Sensorless Ramp":
                self.setNewWidget("lockinConfig")

            case "Calibration Lockin":
                self.setNewWidget("calibrationLockin")

            case "Controller":
                self.setNewWidget("controllerGeneral")
                if self.drive != None:
                    if parent.text(0) == "Axis0":
                        self.controllerGeneral(0)
                    elif parent.text(0) == "Axis1":
                        self.controllerGeneral(1)

            
            case "Autotuning":
                self.setNewWidget("controllerAutotuning")
                if self.drive != None:
                    parent = parent.parent()
                    if parent.text(0) == "Axis0":
                        self.controllerAutotuning(0)
                    elif parent.parent.text(0) == "Axis1":
                        self.controllerAutotuning(1)

            case "Encoder":
                self.setNewWidget("encoderGeneral")
                if self.drive != None:
                    if parent.text(0) == "Axis0":
                        self.encoderGeneral(0)
                    elif parent.text(0) == "Axis1":
                        self.encoderGeneral(1)

            case "Motor":
                self.setNewWidget("motor")

            case "Can":
                if parent == None:
                    self.setNewWidget("canGeneral")
                    pass
                else:
                    match parent.text(0):
                        case "Config":
                            self.setNewWidget("axisCanConfig")
                        case "ODrive":
                            self.setNewWidget("canGeneral")
