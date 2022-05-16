from sai_thrift.sai_headers import *
from sai_base_test import *

class InitBasicData(PlatformSaiHelper):
    """
    This is a test class use to trigger some basic verification when set up the basic t0 data configuration.
    """
    #Todo remove this class when T0 data is ready, this class should not be checked into repo
    def setUp(self):
        """
        Test the basic setup proecss
        """
        #this process contains the switch_init process
        SaiHelperBase.setUp(self)

    def runTest(self):
        """
        Test the basic runTest proecss
        """
        pass

    def tearDown(self):
        """
        Test the basic tearDown proecss
        """
        pass
