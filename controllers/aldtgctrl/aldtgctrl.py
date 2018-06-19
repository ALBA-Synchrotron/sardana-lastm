import time
import threading

import PyTango
from raspberry_pi.RPi import Raspberry

from sardana import State
from sardana.sardanaevent import EventReceiver
from sardana.util.funcgenerator import FunctionGenerator
from sardana.pool.controller import TriggerGateController, Type, Description
from sardana.pool.pooldefs import SynchDomain


__author__ = "zreszela@cells.es"
__docformat__ = "restructuredtext"
__all__ = ("ALDTGCtrl", "ALDTangoTGCtrl")


class RasPiDOCallback(EventReceiver):

    def __init__(self, device, axis):
        EventReceiver.__init__(self)
        self.device = device
        self.attr_name = "Pin%d_voltage" % axis
        self.axis = axis

    def event_received(self, src, type_, value):
        print "event_received(%s, %s, %s): %f" % (
        src, type_, value, time.time())
        if type_.name == "active":
            voltage = True
        elif type_.name == "passive":
            voltage = False
        else:
            return
        self.device.setvoltage(self.axis, voltage)


class ALDTGCtrl(TriggerGateController):
    """Basic controller intended for demonstration purposes only.
    """
    organization = "ALBA-Cells"
    MaxDevice = 1

    class_prop = {
        "Device": {Type: str,
                   Description: "Raspberry PI device"}
    }

    def __init__(self, inst, props, *args, **kwargs):
        """Constructor"""
        TriggerGateController.__init__(self, inst, props, *args, **kwargs)
        #        self.device = PyTango.DeviceProxy(self.Device)
        self.device = Raspberry("raspi030")
        self.device.connect_to_pi()
        self.tg = {}
        self.cbs = {}
        self.conf = {}

    def AddDevice(self, axis):
        self._log.debug('AddDevice(%d): entering...' % axis)
        idx = axis - 1
        self.device.setoutput(axis, True)
        func_generator = FunctionGenerator()
        func_generator.initial_domain = SynchDomain.Time
        func_generator.active_domain = SynchDomain.Time
        cb = RasPiDOCallback(self.device, axis)
        func_generator.add_listener(cb)
        self.tg[idx] = func_generator
        self.cbs[idx] = cb
        self._log.debug('AddDevice(%d): leaving...' % axis)

    def SynchOne(self, axis, conf):
        idx = axis - 1
        tg = self.tg[idx]
        tg.set_configuration(conf)
        self.conf[idx] = conf

    def StateOne(self, axis):
        """Get the dummy trigger/gate state"""
        try:
            self._log.debug('StateOne(%d): entering...' % axis)
            sta = State.On
            status = "Stopped"
            idx = axis - 1
            tg = self.tg[idx]
            if tg.is_running() or tg.is_started():
                sta = State.Moving
                status = "Moving"
            self._log.debug('StateOne(%d): returning (%s, %s)' %
                            (axis, sta, status))
        except Exception, e:
            print e
        return sta, status

    def PreStartAll(self):
        pass

    def StartAll(self):
        pass

    def PreStartOne(self, axis, value=None):
        return True

    def StartOne(self, axis):
        """Start the specified trigger
        """
        self._log.debug('StartOne(%d): entering...' % axis)
        idx = axis - 1
        tg = self.tg[idx]
        print tg._listeners
        tg.start()
        self.thread = threading.Thread(target=tg.run)
        self.thread.start()

    def AbortOne(self, axis):
        """Start the specified trigger
        """
        self._log.debug('AbortOne(%d): entering...' % axis)
        idx = axis - 1
        self.tg[idx].stop()


class RasPiTangoDOCallback(EventReceiver):

    def __init__(self, device, axis):
        EventReceiver.__init__(self)
        self.device = device
        self.attr_name = "Pin%d_voltage" % axis

    def event_received(self, src, type_, value):
        print "event_received(%s, %s, %s): %f" % (
        src, type_, value, time.time())
        if type_.name == "active":
            voltage = True
        elif type_.name == "passive":
            voltage = False
        else:
            return
        self.device.write_attribute(self.attr_name, voltage)


class ALDTangoTGCtrl(TriggerGateController):
    """Basic controller intended for demonstration purposes only.
    """
    organization = "ALBA-Cells"
    MaxDevice = 1

    class_prop = {
        "Device": {Type: str,
                   Description: "Raspberry PI device"}
    }

    def __init__(self, inst, props, *args, **kwargs):
        """Constructor"""
        TriggerGateController.__init__(self, inst, props, *args, **kwargs)
        self.device = PyTango.DeviceProxy(self.Device)
        self.tg = {}
        self.cbs = {}
        self.conf = {}

    def AddDevice(self, axis):
        self._log.debug('AddDevice(%d): entering...' % axis)
        idx = axis - 1
        func_generator = FunctionGenerator()
        func_generator.initial_domain = SynchDomain.Time
        func_generator.active_domain = SynchDomain.Time
        cb = RasPiTangoDOCallback(self.device, axis)
        func_generator.add_listener(cb)
        self.tg[idx] = func_generator
        self.cbs[idx] = cb
        self._log.debug('AddDevice(%d): leaving...' % axis)

    def SynchOne(self, axis, conf):
        idx = axis - 1
        tg = self.tg[idx]
        tg.set_configuration(conf)
        self.conf[idx] = conf

    def StateOne(self, axis):
        """Get the dummy trigger/gate state"""
        try:
            self._log.debug('StateOne(%d): entering...' % axis)
            sta = State.On
            status = "Stopped"
            idx = axis - 1
            tg = self.tg[idx]
            if tg.is_running() or tg.is_started():
                sta = State.Moving
                status = "Moving"
            self._log.debug('StateOne(%d): returning (%s, %s)' %
                            (axis, sta, status))
        except Exception, e:
            print e
        return sta, status

    def PreStartAll(self):
        pass

    def StartAll(self):
        pass

    def PreStartOne(self, axis, value=None):
        return True

    def StartOne(self, axis):
        """Start the specified trigger
        """
        self._log.debug('StartOne(%d): entering...' % axis)
        idx = axis - 1
        tg = self.tg[idx]
        print tg._listeners
        tg.start()
        self.thread = threading.Thread(target=tg.run)
        self.thread.start()

    def AbortOne(self, axis):
        """Start the specified trigger
        """
        self._log.debug('AbortOne(%d): entering...' % axis)
        idx = axis - 1
        self.tg[idx].stop()
