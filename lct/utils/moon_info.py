# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# Copyright (c) 2012-2014, Michael Reuter
# Distributed under the MIT License. See LICENSE.txt for more information.
#------------------------------------------------------------------------------

import logging
import math

import ephem

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
    DAYS_TO_HOURS = 24.0

    def __init__(self):
        '''
        Constructor
        '''
        self._moon = ephem.Moon()
        self.logger = logging.getLogger('lct.utils.moon_info.MoonInfo')
        
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
        return self._observer.date - prev_new
        
    def colong(self):
        '''
        This function returns the current selenographic colongitude.
        @return: The selenographic colongitude in radians.
        '''
        return self._moon.colong
    
    def illumination(self):
        '''
        This function returns the illuminated fraction of the Moon.
        @return: The fraction of the illuminated Moon (<=1.0).
        '''
        return self._moon.moon_phase
    
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
        self.logger.debug("Longitude from colongitude: %.2lf", selco_longitude)
        cur_tod = self._getTimeOfDay()
        
        min_long = lfeature.longitude - lfeature.delta_longitude / 2.0
        max_long = lfeature.longitude + lfeature.delta_longitude / 2.0

        self.logger.debug("Feature: %s", lfeature)
        self.logger.debug("Min,Max Longitude: %.2lf, %.2lf", min_long, max_long)
        
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
            self.logger.debug("Min Longitude and Longitude cutoff: %.2lf, %.2lf", min_long, long_cutoff)
            if lfeature.feature_type in MoonInfo.NO_CUTOFF_TYPE:
                is_visible = selco_longitude <= min_long
            else:
                is_visible = long_cutoff <= selco_longitude <= min_long
        if cur_tod == MoonInfo.EVENING:
            # Maximum longitude for evening visibility
            long_cutoff = max_long + cutoff
            self.logger.debug("Max Longitude and Longitude cutoff: %.2lf, %.2lf", max_long, long_cutoff)
            if lfeature.feature_type in MoonInfo.NO_CUTOFF_TYPE:
                is_visible = max_long <= selco_longitude
            else:
                is_visible = max_long <= selco_longitude <= long_cutoff
            
        self.logger.debug("Is Visible: %s", is_visible)
        return is_visible
    
    def libration(self, coord_type):
        '''
        This function retrieves the current lunar libration for the given 
        coordinate: [lat, long].
        @param coord_type: Either latitude or longitude.
        @return: The libration coordinate in radians
        '''
        return getattr(self._moon, 'libration_%s' % coord_type)
    
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
    
    def getPhase(self):
        '''
        This function gets the numeric code for the phase of the moon. 
        @return: The moon phase as a numeric code.
        '''
        return self._getPhase()
    
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
        
    def findNextFourPhases(self):
        '''
        This function returns a sorted tuple of the next four phases with the key being the short 
        name for the phase. The value is a modified Julian date for the phase.
        @return: A list of tuples sorted by the value date.
        '''
        phases = {}
        phases["new"] = ephem.next_new_moon(self._observer.date)
        phases["fq"] = ephem.next_first_quarter_moon(self._observer.date)
        phases["full"] = ephem.next_full_moon(self._observer.date)
        phases["tq"] = ephem.next_last_quarter_moon(self._observer.date)
        
        return sorted(phases.items(), key=lambda x:x[1])
        
    def timeFromNewMoon(self):
        '''
        This function calculates the time from the previous new moon.
        @returns: The time from new moon in decimal hours.
        '''
        prev_new_moon = ephem.previous_new_moon(self._observer.date)
        return MoonInfo.DAYS_TO_HOURS * (self._observer.date - prev_new_moon)
    
    def timeToNewMoon(self):
        '''
        This function calculates the time to the next new moon.
        @returns: The time to new moon in decimal hours.
        '''
        next_new_moon = ephem.next_new_moon(self._observer.date)
        return MoonInfo.DAYS_TO_HOURS * (next_new_moon - self._observer.date)
    
    def timeToFullMoon(self):
        '''
        This function calculates the time to the next full moon.
        @returns: The time to full moon in decimal days.
        '''
        next_full_moon = ephem.next_full_moon(self._observer.date)
        return next_full_moon - self._observer.date
