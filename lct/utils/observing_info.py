'''
Created on Jun 7, 2012

@author: Michael Reuter
'''

import utils
from moon_info import MoonInfo
from observing_site import ObservingSite

class ObservingInfo(object):
    '''
    This class is responsible for keeping the observing site information and 
    the moon information object together. It will be responsible for updating 
    any of the observing site information that then affects the moon 
    information.
    '''
    __shared_state = {"obs_site": ObservingSite(),
                      "moon_info": MoonInfo()}

    def __init__(self):
        '''
        Constructor
        '''
        self.__dict__ = self.__shared_state
        
    def update(self):
        self.moon_info.compute(self.obs_site.getObserver())
        
if __name__ == "__main__":
    oi = ObservingInfo()
    oi.update()
    print oi.obs_site
    import time
    time.sleep(2)
    oi2 = ObservingInfo()
    oi2.update()
    print oi2.obs_site