# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# Copyright (c) 2014, Michael Reuter
# Distributed under the MIT License. See LICENSE.txt for more information.
#------------------------------------------------------------------------------

from PyQt4 import QtGui
from PyQt4 import QtCore

class FractionWidget(QtGui.QWidget):
    '''
    This class draws the moon with the current illuminated fraction.
    '''
    
    # Set the widget margin size to 5%
    MARGIN_SIZE = 0.05
    
    def __init__(self, parent=None):
        '''
        Constructor
        '''
        super(FractionWidget, self).__init__(parent)
        self.fraction = 0.0
        self.waxing_phase = True
        self.setMinimumSize(self.minimumSizeHint())
        
    def setPhaseInformation(self, fraction, waxing_phase):
        '''
        This function can set the phase information for drawing the widget.
        @param fraction: The illuminated fraction (decimal, less than one).
        @param waxing_phase: Boolean for waxing (True) or waning (False) phase.
        '''
        self.fraction = fraction
        self.waxing_phase = waxing_phase
        
    def paintEvent(self, event=None):
        '''
        This function draws the widget with the phase information.
        '''
        import math
        # Set a size for the logical coordinate system.
        logical_size = 100.0;
        
        # This is the BO chord, as a unitless number, in the figure on Page 345 in 
        # Astronomical Algorithms 2nd Ed. by Jean Meeus.
        bo = 1.0 - 2.0 * self.fraction
        
        # Set the overlap color to black unless we are the gibbous phases (BO < 0).
        overlap_color = QtCore.Qt.black
        if bo < 0:
            overlap_color = QtCore.Qt.white
        
        # Margin sizes
        margin_width = logical_size * self.MARGIN_SIZE
        margin_height = logical_size * self.MARGIN_SIZE
        # Half the widget size
        half_width = logical_size / 2.0
        # This is the diameter of the moon sphere.
        width = logical_size - (2.0 * margin_width)
        height = logical_size - (2.0 * margin_height)
        
        # Begin drawing
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        side = min(self.width(), self.height())
        # Set the viewport over the center of the drawing. Allows Qt to convert logical to 
        # physical coordinates.
        painter.setViewport(QtCore.QRect((self.width() - side)/2, 
                                         (self.height() - side)/2,
                                         side, side))
        painter.setWindow(0, 0, logical_size, logical_size)
        
        # Set the base moon drawing as a New Moon.
        painter.setPen(QtCore.Qt.black)
        painter.setBrush(QtCore.Qt.black)
        painter.drawEllipse(QtCore.QRectF(margin_width, margin_height, width, height))
        
        # Draw either First or Third Quarter depending on phase state.
        painter.setBrush(QtCore.Qt.white)
        painter.setPen(QtCore.Qt.NoPen)       
        painter.drawChord(QtCore.QRectF(margin_width, margin_height, 
                                        width, height), 
                          (-1 if self.waxing_phase else 1) * 90 * 16, 180 * 16)

        # Draw the overlap ellipse that represents the correct illuminated fraction.
        painter.setBrush(overlap_color)
        illum_chord = math.fabs(bo) * width
        painter.drawEllipse(QtCore.QRectF(half_width - 0.5 * illum_chord, margin_height, 
                                          illum_chord, height))
        
    def minimumSizeHint(self):
        '''
        This function returns the minimum size of the widget. 
        '''
        return QtCore.QSize(200, 200)
        
if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    widget = FractionWidget()
    # Set a waning cresent phase.
    widget.setPhaseInformation(0.3, False)
    widget.move(0, 0)
    widget.show()
    widget.resize(400, 400)
    app.exec_()
    
