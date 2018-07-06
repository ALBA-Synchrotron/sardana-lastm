import time

import tango
from sardana.macroserver.macro import Macro, Type

__author__ = "zreszela@cells.es"
__docformat__ = "restructuredtext"
__all__ = ("ald_set_conf", "ald_get_conf", "ald_run")


class ald_set_conf(Macro):
    """Set path to ALD configuration file (must be accessible on the host
    where MacroServer is running)."""

    env = ("ALDTGCtrl",)

    param_def = [["file", Type.Filename, "/home/operatorstm/ald_seq_conf.py",
                  "Full path to configuration file"]]

    def run(self, file_):
        ctrl_name = self.getEnv("ALDTGCtrl")
        ctrl = self.getController(ctrl_name)
        ctrl.getAttribute("ConfigurationFile").write(file_)


class ald_get_conf(Macro):
    """Get path to ALD configuration file"""

    env = ("ALDTGCtrl",)

    result_def = [["file", Type.Filename, None, "Full path to configuration "
                                                "file"]]

    def run(self):
        ctrl_name = self.getEnv("ALDTGCtrl")
        ctrl = self.getController(ctrl_name)
        return ctrl.getAttribute("ConfigurationFile").read().value


class ald_run(Macro):
    """Execute ALD according to configuration file set with ald_set_conf
    macro"""

    env = ("ALDMeasGrp",)

    param_def = [["repeats", Type.Integer, 1, "Number of repetitions"],
                 ["wait_time", Type.Float, 0, "Wait time (s) between "
                                              "repetitions"]]

    def run(self, repeats, wait_time):
        meas_grp_name = self.getEnv("ALDMeasGrp")
        meas_grp = self.getObj(
            meas_grp_name, type_class=Type.MeasurementGroup)
        conf_file = self.execMacro("ald_get_conf").getResult()
        self.info("Configuration: %s" % conf_file)
        for i in xrange(repeats):
            self.info("Running %d repetition" % (i + 1))
            meas_grp.count(0.001)
            time.sleep(wait_time)
        self.info("Done")


class ald_init(Macro):
    """Initialize ALD hardware.

    This includes:
    - set RPi GPIO output pins
    """

    env = ("ALDTGCtrl",)

    def run(self):
        ctrl_name = self.getEnv("ALDTGCtrl")
        ctrl = self.getController(ctrl_name)
        axes = ctrl.getUsedAxes()
        ctrl_proxy = ctrl.getDeviceProxy()
        raspi_name = ctrl_proxy.get_property("device")["device"][0]
        raspi_proxy = tango.DeviceProxy(raspi_name)
        for axis in axes:
            self.output("Setting PIN %d to output" % axis)
            raspi_proxy.write_attribute("pin%d_output" % axis, True)

