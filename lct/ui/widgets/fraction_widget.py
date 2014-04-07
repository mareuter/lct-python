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
        
    def paintEvent(self, event=None):
        logical_size = 100.0;
        
        def logicalFromPhysical(length, side):
            return (length / side) * logical_size
        fm = QtGui.QFontMetricsF(self.font())
        
        margin_width = logical_size * 0.05
        margin_height = logical_size * 0.05
        width = logical_size - (2.0 * margin_width)
        height = logical_size - (2.0 * margin_height)
        
        painter = QtGui.QPainter(self)
        painter.setWindow(0, 0, logical_size, logical_size)
        painter.setPen(QtCore.Qt.black)
        painter.setBrush(QtCore.Qt.black)
        painter.drawEllipse(QtCore.QRectF(margin_width, margin_height, width, height))
        
        painter.setBrush(QtCore.Qt.white)
        painter.drawChord(QtCore.QRectF(margin_width, margin_height, width, height), 
            -90 * 16, 180 * 16)
        
        painter.setBrush(QtCore.Qt.black)
        painter.drawChord(QtCore.QRectF(logical_size/2.0, margin_height, (width / 2.0) * 0.28, height), 
            -90 * 16, 180 * 16)
        
if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    widget = FractionWidget()
    widget.move(0, 0)
    widget.show()
    widget.resize(400, 400)
    app.exec_()