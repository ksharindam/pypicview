from photogrid_dialog import Ui_GridDialog
from PyQt5.QtCore import Qt, pyqtSignal, QRect, QPoint
from PyQt5.QtGui import QPixmap, QPainter, QImageReader
from PyQt5.QtWidgets import QLabel, QDialog, QHBoxLayout, QSizePolicy, QFileDialog


class GridDialog(QDialog, Ui_GridDialog):
    def __init__(self, pixmap, parent):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.resize(1020, 640)
        layout = QHBoxLayout(self.scrollAreaWidgetContents)
        layout.setContentsMargins(0, 0, 0, 0)
        self.gridPaper = GridPaper(self)
        layout.addWidget(self.gridPaper)
        thumbnail = Thumbnail(pixmap, self.frame)
        self.verticalLayout.addWidget(thumbnail)
        thumbnail.clicked.connect(self.gridPaper.setPhoto)
        self.addPhotoBtn.clicked.connect(self.addPhoto)
        self.gridPaper.photo = pixmap

    def addPhoto(self):
        filepath, sel_filter = QFileDialog.getOpenFileName(self, 'Open Image', '')            
        if filepath == '' : return
        image_reader = QImageReader(filepath)
        image_reader.setAutoTransform(True)
        pm = QPixmap.fromImageReader(image_reader)
        if not pm.isNull() :
            thumbnail = Thumbnail(pm, self.frame)
            self.verticalLayout.addWidget(thumbnail)
            thumbnail.clicked.connect(self.gridPaper.setPhoto)

    def accept(self):
        # Create final grid when ok is clicked
        self.gridPaper.createFinalGrid()
        QDialog.accept(self)

class Thumbnail(QLabel):
    clicked = pyqtSignal(QPixmap)
    def __init__(self, pixmap, parent):
        QLabel.__init__(self, parent)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.photo = pixmap
        self.setPixmap(pixmap.scaledToWidth(100))
        
    def mousePressEvent(self, ev):
        self.clicked.emit(self.photo)


class GridPaper(QLabel):
    def __init__(self, parent):
        QLabel.__init__(self, parent)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setMouseTracking(True)
        #self.scale = 1.0
        self.pixmap_dict = {}
        self.boxes = []
        self.setupGrid()

    def setupGrid(self):
        self.paperW, self.paperH = 1800, 1200
        self.W, self.H = 413, 531
        self.col, self.row = 4, 2           # total no. of columns and rows
        self.spacingX, self.spacingY = (self.paperW-self.col*self.W)/(self.col+1), (self.paperH-self.row*self.H)/(self.row+1)
        # Setup Foreground Grid
        w, h = self.W/2, self.H/2
        spacingX, spacingY = self.spacingX/2, self.spacingY/2
        for i in range(self.col*self.row):
            row, col = i//self.col, i%self.col        # Position of the box as row & col
            box = QRect(spacingX+col*(spacingX+w), spacingY+row*(spacingY+h), w-1, h-1)
            #print(spacingX+col*(spacingX+w), spacingY+row*(spacingY+h), w, h)
            self.boxes.append(box)
        fg = QPixmap(self.paperW/2, self.paperH/2)
        fg.fill()
        painter = QPainter(fg)
        for box in self.boxes:
            painter.drawRect(box)
        painter.end()
        self.setPixmap(fg)

    def setPhoto(self, pixmap):
        self.photo = pixmap

    def mouseMoveEvent(self, ev):
        # Change cursor whenever cursor comes over a box
        for box in self.boxes:
            if box.contains(ev.pos()):
                self.setCursor(Qt.PointingHandCursor)
                return
        self.setCursor(Qt.ArrowCursor)

    def mousePressEvent(self, ev):
        blank_pm = QPixmap(self.W/2, self.H/2)
        blank_pm.fill()
        for box in self.boxes:
            if box.contains(ev.pos()):
                topleft = box.topLeft()
                #print(topleft.x(), topleft.y())
                pm = self.photo.scaled(self.W/2, self.H/2, 1, 1)
                bg = self.pixmap()
                painter = QPainter(bg)
                painter.drawPixmap(topleft, blank_pm) # Erase older image by placing blank image over it
                painter.drawPixmap(topleft, pm)
                painter.end()
                self.setPixmap(bg)
                self.pixmap_dict[self.boxes.index(box)] = self.photo
                break

    def createFinalGrid(self):
        self.photo_grid = QPixmap(self.paperW, self.paperH)
        self.photo_grid.fill()
        painter = QPainter(self.photo_grid)
        for index in self.pixmap_dict:
            row, col = index//self.col, index%self.col
            topleft = QPoint(self.spacingX+col*(self.spacingX+self.W), self.spacingY+row*(self.spacingY+self.H))
            pm = self.pixmap_dict[index].scaled(self.W, self.H, 1, 1)
            painter.drawPixmap(topleft, pm)
        painter.end()



