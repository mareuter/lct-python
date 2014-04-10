'''
Created on Apr 4, 2014

@author: Michael Reuter
'''
from PyQt4 import QtGui, QtCore

class FractionWidget(QtGui.QWidget):
    '''
    classdocs
    '''
    def __init__(self, parent=None):
        '''
        Constructor
        '''
        super(FractionWidget, self).__init__(parent)
        self.setMinimumSize(self.minimumSizeHint())
        
    def paintEvent(self, event=None):
        import math
        logical_size = 100.0;
        fraction = 0.0
        waxing_phase = True
        b0 = 1.0 - 2.0 * fraction
        
        overlap_color = QtCore.Qt.black
        if b0 < 0:
            overlap_color = QtCore.Qt.white
        
        margin_width = logical_size * 0.05
        margin_height = logical_size * 0.05
        half_width = logical_size / 2.0
        width = logical_size - (2.0 * margin_width)
        height = logical_size - (2.0 * margin_height)
        
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        side = min(self.width(), self.height())
        painter.setViewport(QtCore.QRect((self.width() - side)/2, 
                                         (self.height() - side)/2,
                                         side, side))
        painter.setWindow(0, 0, logical_size, logical_size)
        painter.setPen(QtCore.Qt.black)
        painter.setBrush(QtCore.Qt.black)
        painter.drawEllipse(QtCore.QRectF(margin_width, margin_height, width, height))
        
        painter.setBrush(QtCore.Qt.white)
        painter.setPen(QtCore.Qt.NoPen)       
        painter.drawChord(QtCore.QRectF(margin_width, margin_height, 
                                        width, height), 
                          (-1 if waxing_phase else 1) * 90 * 16, 180 * 16)

        painter.setBrush(overlap_color)
        illum_chord = math.fabs(b0) * width
        painter.drawEllipse(QtCore.QRectF(half_width - 0.5 * illum_chord, margin_height, 
                                          illum_chord, height))
        
    def minimumSizeHint(self):
        return QtCore.QSize(200, 200)
        
if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    widget = FractionWidget()
    widget.move(0, 0)
    widget.show()
    widget.resize(400, 400)
    app.exec_()