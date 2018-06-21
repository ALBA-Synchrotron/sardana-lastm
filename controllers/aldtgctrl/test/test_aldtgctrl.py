from taurus.external import unittest
from taurus.test.resource import getResourcePath

from aldtgctrl import ALDTangoTGCtrl


class TestALDTangoTGCtrl(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)
        inst = None
        props = {"Device": "sys/tg_test/1"}
        self.ald_tg_ctrl = ALDTangoTGCtrl(inst, props)

    def test_configuration1(self):
        self.ald_tg_ctrl.AddDevice(1)
        conf_file = getResourcePath("aldtgctrl.test.res",
                                    "ald_sequence_config.py")
        # due to sardana-org/sardana#787 use lowercase
        self.ald_tg_ctrl.SetCtrlPar("configurationfile", conf_file)
        self.ald_tg_ctrl.SynchOne(1, None)

