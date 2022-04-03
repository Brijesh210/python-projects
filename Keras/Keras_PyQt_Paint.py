import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtGui import QImage, QPainter, QPen, QBrush, QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QFormLayout, QGridLayout, QMessageBox, QPushButton, QLineEdit, QPlainTextEdit, QSpinBox

### "Paint" implementation


# The size and color of the pen
PEN_WIDTH = 25
PEN_COLOR = Qt.white

# The size of the drawing field PIXMAP_SIZE x PIXMAP_SIZE
PIXMAP_SIZE = 256

# Simple Paint implementation
class Paint(QtWidgets.QMainWindow):

    def __init__(self, predict_function):
        """
        predict_function - function called when drawing is finished.
         Should return the value (number) that was returned by the neural network
        """
        super().__init__()

        # The main widget that stores the layout
        self.window = QWidget()

        # Creating a window in which it will be possible to draw
        self.paint = QtWidgets.QLabel()
        self.canvas = QtGui.QPixmap(PIXMAP_SIZE, PIXMAP_SIZE)
        self.paint.setPixmap(self.canvas)

        # Creating a storing layout: 
        # - drawing window 
        # - image clearing button 
        # - window displaying the neural network response
        self.layout = QGridLayout()
        self.prediction = QLineEdit()
        self.clear_button = QPushButton("Clear")
        self.clear_button.clicked.connect(self.clear)   

        self.layout.addWidget(self.prediction,1,0) 
        self.layout.addWidget(self.clear_button,1,1) 
        self.layout.addWidget(self.paint,0,0) 

        self.prediction.setDisabled(1)
        self.window.setLayout(self.layout)
        self.setCentralWidget(self.window)

        # Variables that hold the last position of the mouse 
        self.last_x = None
        self.last_y = None

        self.predict_function = predict_function

    def clear(self):
        """
        A function that clears the drawing area
        """
        self.paint.pixmap().fill(Qt.black)
        self.update()

    def mouseMoveEvent(self, e):
        """
        Function called when the mouse is moved with the mouse button pressed.
        """
        if self.last_x is None: 
            self.last_x = e.x()
            self.last_y = e.y()
            return 

        # Drawing support
        painter = QPainter(self.paint.pixmap())
        painter.setPen(QPen(PEN_COLOR, PEN_WIDTH, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            
        x = self.paint.geometry().x()
        y = self.paint.geometry().y()

        painter.drawLine(self.last_x - x, self.last_y - y, e.x() - x, e.y() - y)

        self.update()
        

        self.last_x = e.x()
        self.last_y = e.y()
        #
        #
        #
        #
        # Place the returned neural netwrk result in a text field
        # self.paint.pixmap().toImage() - zwraca obiekt QImage
        self.prediction.setText(str(self.predict_function(self.paint.pixmap().toImage())))

    def mouseReleaseEvent(self, e):
        """
        Function called when the mouse button is released.
        """
        self.last_x = None
        self.last_y = None



import Keras_PyQt_Paint_Model as kppm

app = QtWidgets.QApplication(sys.argv)
window = Paint(lambda x: kppm.predict(x, kppm.get_model()))
window.show()
app.exec_()