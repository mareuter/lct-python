'''
Created on Jun 13, 2012

@author: Michael Reuter
'''
import ephem
import math
import utils

class MoonInfo(object):
    '''
    This class is responsible for handling all of the information and 
    calculations dealing with the Moon.
    '''
    
    NM, WAXING_CRESENT, FQ, WAXING_GIBBOUS, FM, WANING_GIBBOUS, TQ, \
    WANING_CRESENT = range(8)
    PHASE_NAMES = ("New Moon", "Waxing Cresent", "First Quarter", 
                   "Waxing Gibbous", "Full Moon", "Waning Gibbous",
                   "Third Quarter", "Waning Cresent")
    MORNING, EVENING = range(2)
    FEATURE_CUTOFF = 15.0 # degrees
    NO_CUTOFF_TYPE = ("Mare", "Oceanus")

    def __init__(self):
        '''
        Constructor
        '''
        self._moon = ephem.Moon()
        
    def compute(self, observer):
        '''
        This function sets the observer into the Moon object and triggers the 
        calculations for the Moon's parameters.
        @param observer: The object holding the current location and date/time.
        '''
        self._observer = observer
        self._moon.compute(self._observer)
            
    def age(self):
        '''
        This function returns the age of the Moon (time since New).
        @return: The age of the Moon in days.
        '''
        prev_new = ephem.previous_new_moon(self._observer.date)
        age = self._observer.date - prev_new
        return utils.StrFmt.floatString(age, 2)
        
    def colong(self):
        '''
        This function returns the current selenographic colongitude.
        @return: The selenographic colongitude in DMS.
        '''
        return str(self._moon.colong)
    
    def illumination(self, use_postfix=False):
        '''
        This function returns the illuminated fraction of the Moon.
        @param use_postfix: If true, put a % after the number in the string.
        @return: The fraction of the illuminated Moon (<=100.0).
        '''
        if use_postfix:
            pf = '%'
        else:
            pf = None
        return utils.StrFmt.floatString(self._moon.moon_phase * 100.0, 
                                        1, postfix=pf)
    
    def isVisible(self, lfeature):
        '''
        This function determines if the given lunar feature is visible based 
        on the current selenographic colongitude (SELCO). For most features 
        near the equator, from NM to FM once the SELCO recedes about 15 
        degrees, the shadow relief makes it tough to observe. Conversely, the 
        SELCO needs to be within 15 degrees of the feature from FM to NM. 
        Features closer to the poles are visible much longer after the 15 
        degree cutoff. A 1/cos(latitude) will be applied to the cutoff. 
        Mare and Oceanus are special exceptions and once FULLY visible they are 
        always visible.
        @param lfeature: The lunar feature to check for visibility
        @return: True if the feature is visible.
        '''
        selco_longitude = self._colongToLong()
        print "Q:", selco_longitude
        cur_tod = self._getTimeOfDay()
        
        min_long = lfeature.longitude - lfeature.delta_longitude / 2.0
        max_long = lfeature.longitude + lfeature.delta_longitude / 2.0
        
        print "A:", lfeature
        print "B:", min_long, max_long
        
        if min_long > max_long:
            temp = min_long
            min_long = max_long
            max_long = temp

        is_visible = False
        latitude_scaling = math.cos(math.radians(math.fabs(lfeature.latitude)))
        cutoff = MoonInfo.FEATURE_CUTOFF / latitude_scaling

        if cur_tod == MoonInfo.MORNING:
            # Minimum longitude for morning visibility
            long_cutoff = min_long - cutoff
            print "D:", min_long, long_cutoff
            if lfeature.feature_type in MoonInfo.NO_CUTOFF_TYPE:
                is_visible = selco_longitude <= min_long
            else:
                is_visible = long_cutoff <= selco_longitude <= min_long
        if cur_tod == MoonInfo.EVENING:
            # Maximum longitude for evening visibility
            long_cutoff = max_long + cutoff
            print "DD:", max_long, long_cutoff
            if lfeature.feature_type in MoonInfo.NO_CUTOFF_TYPE:
                is_visible = max_long <= selco_longitude
            else:
                is_visible = max_long <= selco_longitude <= long_cutoff
            
        print "C:", is_visible
        return is_visible
    
    def libration(self, coord_type):
        '''
        This function retrieves the current lunar libration for the given 
        coordinate: [lat, long]. The value from the Moon object is in radians
        and needs to be converted to degrees.
        @param coord_type: Either latitude or longitude.
        @return: The libration coordinate as a string.
        '''
        libration = getattr(self._moon, 'libration_%s' % coord_type)
        dms = utils.Converter.ddToDms(math.degrees(libration))
        # Only take degrees and minutes.
        return utils.StrFmt.dmsString(dms[:2])
    
    def _getPhase(self):
        '''
        This function returns the moon phase according to standard nomenclature.
        @return: The moon phase as an enum value.
        '''
        colong = math.degrees(self._moon.colong)
        if colong == 270.0:
            return MoonInfo.NM
        if 270.0 < colong < 360.0:
            return MoonInfo.WAXING_CRESENT
        if colong == 0.0 or colong == 360.0:
            return MoonInfo.FQ
        if 0.0 < colong < 90.0:
            return MoonInfo.WAXING_GIBBOUS
        if colong == 90.0:
            return MoonInfo.FM
        if 90.0 < colong < 180.0:
            return MoonInfo.WANING_GIBBOUS
        if colong == 180.0:
            return MoonInfo.TQ
        if 180.0 < colong < 270.0:
            return MoonInfo.WANING_CRESENT
    
    def getPhaseAsString(self):
        '''
        This function returns the phase of the moon as a string.
        @return: The moon phase as a string.
        '''
        return MoonInfo.PHASE_NAMES[self._getPhase()]
    
    def _getTimeOfDay(self):
        '''
        This function determines the current time of day on the moon. In 
        otherwords, if the sun is rising on the moon it is morning or if the 
        sun is setting on the moon it is evening.
        @return: The current time of day.
        '''
        phase = self._getPhase()
        if phase in (MoonInfo.NM, MoonInfo.WAXING_CRESENT, MoonInfo.FQ,
                     MoonInfo.WAXING_GIBBOUS):
            return MoonInfo.MORNING
        if phase in (MoonInfo.FM, MoonInfo.WANING_GIBBOUS, MoonInfo.TQ,
                     MoonInfo.WANING_CRESENT):
            return MoonInfo.EVENING
        
    def _colongToLong(self):
        '''
        This function calculates the conversion between the selenographic  
        colongitude and actual lunar longitude.
        @return: The lunar longitude for the current selenographic colongitude
        '''
        colong = math.degrees(self._moon.colong)
        cur_phase = self._getPhase()
        if cur_phase in (MoonInfo.NM, MoonInfo.WAXING_CRESENT):
            return 360.0 - colong
        if cur_phase in (MoonInfo.FQ, MoonInfo.WAXING_GIBBOUS):
            return -1.0 * colong
        if cur_phase in (MoonInfo.FM, MoonInfo.WANING_GIBBOUS):
            return 180.0 - colong
        if cur_phase in (MoonInfo.TQ, MoonInfo.WANING_CRESENT):
            return -1.0 * (colong - 180.0)
