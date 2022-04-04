import PyQt5.QtWidgets as qt
import PyQt5.QtGui as qtg
import PyQt5.QtCore as qtc
import os


class Window(qt.QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('PyQt5 Lab')
        self.setGeometry(500, 300, 800, 600)
        # Menu
        self.exitAction = qt.QAction('Exit', self)
        self.prepareMenu()
        # tabs
        self.tabsWidget = qt.QTabWidget()
        self.tabs = [ImageViewerTab(self), TextEditorTab(self), ThreeTab(self)]
        tabTitles = {
            0: "Image Viewer",
            1: "Text Editor",
            2: "Input Addition"
        }
        for i, tab in enumerate(self.tabs):
            self.tabsWidget.addTab(tab, tabTitles.get(i))
        self.setCentralWidget(self.tabsWidget)

    def prepareMenu(self):
        fileMenu = self.menuBar().addMenu("File")
        self.exitAction.setShortcut("Alt+F4")
        fileMenu.addAction(self.exitAction)
        fileMenu.triggered.connect(self.handleClose)

    def handleClose(self):
        self.close()

    def selectTab(self, tab: qt.QWidget):
        self.tabsWidget.setCurrentIndex(self.tabsWidget.indexOf(tab))


class ImageViewerTab(qt.QWidget):

    def __init__(self, parent: Window):
        super().__init__()
        self.layout = qt.QHBoxLayout()
        self.setLayout(self.layout)
        # Actions
        self.openTaskOne = qt.QAction('Open', self)
        self.prepareMenu(parent)
        self.selectTab = lambda: parent.selectTab(self)

    def prepareMenu(self, parent: Window):
        taskOneMenu = parent.menuBar().addMenu("Task 1")
        self.openTaskOne.setShortcut("Ctrl+G")
        taskOneMenu.addAction(self.openTaskOne)
        taskOneMenu.triggered.connect(self.handleOpenImage)

    def handleOpenImage(self, action):
        fileName, selectedFilter = qt.QFileDialog.getOpenFileName(self, "Select an image file", "",
                                                                  "All Files (*);; JPG (*.jpg);; "
                                                                  "PNG (*.png);; GIF (*.gif)")
        if not fileName:
            return
        x = self.layout.itemAt(0)
        img: qt.QLabel
        if x:
            img = x.widget()
        else:
            img = qt.QLabel()
            self.layout.addWidget(img)
        pixmap = qtg.QPixmap(fileName)
        resized = pixmap.scaled(self.width(), self.height(), qtc.Qt.KeepAspectRatio)
        img.setPixmap(resized)
        self.selectTab()


class TextEditorTab(qt.QWidget):

    def __init__(self, parent: Window):
        super().__init__()
        self.layout = qt.QGridLayout()
        self.setLayout(self.layout)
        # Menu
        self.actionsDict = {
            "New": ["Ctrl+N", self.doOpenNew],
            "Open": ["Ctrl+O", self.openFile],
            "Clear": ["Ctrl+W", self.clear],
            "Save": ["Ctrl+S", self.doSave],
            "Save As": ["Ctrl+K", self.doSaveAs]
        }
        self.prepareMenu(parent)
        # Widgets
        self.textEditorWidget = qt.QPlainTextEdit()
        self.textEditorWidget.textChanged.connect(self.handleFileChange)
        self.textEditorSaveButton = qt.QPushButton("SAVE")
        self.textEditorSaveButton.clicked.connect(self.doSave)
        self.textEditorClearButton = qt.QPushButton("CLEAR")
        self.textEditorClearButton.clicked.connect(self.clear)
        self.fileNameLabel = qt.QLabel("*New File")
        self.layout.addWidget(self.fileNameLabel, 0, 0)
        self.layout.addWidget(self.textEditorWidget, 1, 0)
        buttonLayout = qt.QHBoxLayout()
        buttonLayout.addWidget(self.textEditorSaveButton)
        buttonLayout.addWidget(self.textEditorClearButton)
        self.layout.addLayout(buttonLayout, 2, 0)
        self.selectTab = lambda: parent.selectTab(self)
        self.file = None
        self.saved: bool = False

    def prepareMenu(self, parent: Window):
        menu = parent.menuBar().addMenu("Task 2")
        for i in self.actionsDict:
            action = qt.QAction(i, self)
            action.setShortcut(self.actionsDict[i][0])
            menu.addAction(action)
        menu.triggered.connect(self.handleMenuTriggers)

    def handleMenuTriggers(self, action: qt.QAction):
        self.actionsDict[action.text()][1]()
        self.selectTab()

    def doOpenNew(self):
        self.clear()
        self.file = None
        self.fileNameLabel.setText("*New File")
        self.saved = False

    def doSave(self):
        if self.file and os.path.exists(self.file):
            self.write()
            self.saved = True
            self.fileNameLabel.setText(self.file)
        else:
            self.doSaveAs()

    def doSaveAs(self):
        file, ext = qt.QFileDialog.getSaveFileName(self, "Save As...", "", "Text File (.txt);; All Files (*))")
        if file:
            file = file if ext == 'All Files (*)' else file+'.txt'
            with open(file, 'w'): pass
            self.file = file
            self.doSave()

    def clear(self):
        self.textEditorWidget.clear()

    def read(self):
        with open(self.file, "r") as fileRead:
            return fileRead.read()

    def write(self):
        with open(self.file, "w") as fileWrite:
            fileWrite.write(self.textEditorWidget.toPlainText())

    def openFile(self):
        file, selectedFilter = qt.QFileDialog.getOpenFileName(self, "Select a file", "", "All Files (*))")
        if not file:
            return
        self.file = file
        self.clear()
        try:
            self.textEditorWidget.setPlainText(self.read())
            self.fileNameLabel.setText(self.file)
        except:
            self.file = None
            self.fileNameLabel.setText("New File")
        self.saved = True

    def handleFileChange(self):
        if self.saved:
            self.fileNameLabel.setText('*' + self.file)
            self.saved = False


class ThreeTab(qt.QWidget):

    def __init__(self, parent: Window):
        super().__init__()
        self.layout = qt.QGridLayout()
        # Menu
        self.clearTaskThree = qt.QAction('Clear', self)
        self.prepareMenu(parent)
        self.setLayout(self.layout)
        # Widgets
        self.widgets = [[qt.QLabel("Pole A"), qt.QLabel("Pole B"), qt.QLabel("Pole C"), qt.QLabel("Pole A + B + C ")],
                        [qt.QLineEdit(), qt.QLineEdit(), qt.QSpinBox(), qt.QLineEdit()]]
        for i in range(4):
            self.layout.addWidget(self.widgets[0][i], i, 0)
            self.layout.addWidget(self.widgets[1][i], i, 1)
            if not i == 3:
                self.widgets[1][i].textChanged.connect(self.handleChange)
        self.widgets[1][3].setEnabled(False)
        self.layout.setRowStretch(4, 10)
        self.selectTab = lambda: parent.selectTab(self)

    def prepareMenu(self, parent: Window):
        menu = parent.menuBar().addMenu("Task 3")
        self.clearTaskThree.setShortcut("Ctrl+Q")
        menu.addAction(self.clearTaskThree)
        menu.triggered.connect(self.handleClear)

    def handleClear(self):
        for i, wid in enumerate(self.widgets[1]):
            if i == 2:
                wid.setValue(0)
            else:
                wid.clear()
        self.selectTab()

    def handleChange(self):
        result = ""
        for i in range(3):
            result += self.widgets[1][i].text()+" "
        self.widgets[1][3].setText(result)


if __name__ == '__main__':
    app = qt.QApplication([])
    window = Window()
    window.show()
    app.exec_()
