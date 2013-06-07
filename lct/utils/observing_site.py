'''
Created on Jun 1, 2012
@author: Michael Reuter
'''
import ephem
import os
import time

class ObservingSite(object):
    '''
    This class handles the information for the observing site include 
    latitude/longitude and date/time
    '''
    _name = "Oak Ridge, TN"
    _latitude = (35, 58, 10)
    _longitude = (-84, 19, 0)
    _observer = None

    def __init__(self):
        '''
        Constructor
        '''
        curtime = time.time()
        obdatetime = ephem.Date(time.gmtime(curtime)[:-3])
        self._observer = ephem.Observer()
        self._observer.date = obdatetime
        self._observer.lat = self.toCoordString("lat")
        self._observer.long = self.toCoordString("long")
    
    def __str__(self):
        '''
        This function gives the string representation of the feature object.
        @return: A string representation.
        '''
        result = []
        result.append("Latitude: %s" % self.toCoordString("lat"))
        result.append("Longitude: %s" % self.toCoordString("long"))
        result.append("DateTime: %s" % self.getDateTime())
        return os.linesep.join(result)
    
    def _tupleToString(self, coordinate):
        return ":".join([str(x) for x in coordinate])
    
    def _tupleToDmsString(self, coord_type):
        dir_str = ""
        coord = getattr(self, "_"+coord_type+"itude")
        if coord_type == "lat":
            if coord[0] < 0:
                dir_str = "S"
            else:
                dir_str = "N"
        if coord_type == "long":
            if coord[0] < 0:
                dir_str = "W"
            else:
                dir_str = "E"
        import math
        return str(int(math.fabs(coord[0])))+u'\u00b0 '+str(coord[1])+"\' "+ str(coord[2])+"\" "+dir_str  
    
    def fromCoordTuple(self, coord_type, coords):
        '''
        This function sets the given named coordinate from the 3-tuple 
        provided.
        @param coord_type: Either lat or long
        @param coords: 3-tuple of (degrees, minutes, seconds)
        '''
        setattr(self, "_"+coord_type+"itude", coords)
        setattr(self._observer, coord_type, self.toCoordString(coord_type))
    
    def toCoordString(self, coord_type):
        '''
        This function returns
        @param coord_type: The coordinate to request: [lat, long].
        @return: A colon-separated string of the coordinate.
        '''
        coord = getattr(self, "_"+coord_type+"itude")
        return self._tupleToString(coord)
    
    def toCoordTuple(self, coord_type):
        '''
        This function returns the requested coordinate as a 3-tuple (DMS).
        @param coord_type: The coordinate to request: [lat, long].
        @return: The DMS 3-tuple.
        '''
        return getattr(self, "_"+coord_type+"itude")
    
    def getDateTime(self):
        '''
        This function returns an ISO8600 date/time string.
        @return: The local date/time.
        '''
        local_time = ephem.localtime(self._observer.date)
        return str(local_time.strftime("%Y-%m-%dT%H:%M:%S%z"))
    
    def getLocalDate(self):
        '''
        This function returns the local date as a string.
        @return: The local date.
        '''
        return self.getDateTime().split('T')[0]
    
    def getLocalTime(self):
        '''
        This function returns the local time as a string.
        @return: The local time.
        '''
        return self.getDateTime().split('T')[-1]
    
    def getObserver(self):
        '''
        This function returns the PyEphem Observer object.
        @return: The current observer object.
        '''
        return self._observer
    
    def getLocationString(self):
        '''
        This function returns the latitude and longitude as a combined string.
        Each coordinate has a directional tag.
        @return: The latitude and longitude as a single string.
        '''
        result = []
        result.append(self._tupleToDmsString("lat"))
        result.append(self._tupleToDmsString("long"))
        return "  ".join(result)
    
    def setLocationName(self, name):
        '''
        This function sets the label name for the given observing location.
        @param name: The text name to give the observing site.
        '''
        self._name = name
        
    def setLocation(self, name, latitude, longitude):
        '''
        This function sets all of the location information.
        @param name: A string for the observing location.
        @param latitude: The location latitude as a 3-tuple of DMS
        @param longitude: The location longitude as a 3-tuple of DMS
        '''
        self.setLocationName(name)
        self.fromCoordTuple('lat', latitude)
        self.fromCoordTuple('long', longitude)
        
if __name__ == "__main__":
    obs = ObservingSite()
    print obs
    
    