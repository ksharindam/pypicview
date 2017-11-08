from photogrid_dialog import Ui_GridDialog
from gridsetup_dialog import Ui_GridSetupDialog
from PyQt5.QtCore import Qt, QObject, pyqtSignal, QRect, QPoint
from PyQt5.QtGui import QPixmap, QPainter, QImageReader, QPen
from PyQt5.QtWidgets import QApplication, QLabel, QDialog, QHBoxLayout, QSizePolicy, QFileDialog, QMessageBox

helptext = '''Click on a image thumbnail to select an image to drop. Then click on the blank boxes to drop the selected photo.

If you want to create grid with more different photos then load photo by clicking Add Photo button.

You can change the photo of a box by selecting another image and clicking over the box.'''

class GridDialog(QDialog, Ui_GridDialog):
    def __init__(self, pixmap, parent):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.resize(1020, 640)
        layout = QHBoxLayout(self.scrollAreaWidgetContents)
        layout.setContentsMargins(0, 0, 0, 0)
        self.gridPaper = GridPaper(self)
        layout.addWidget(self.gridPaper)
        self.thumbnailGr = ThumbnailGroup(self)
        thumbnail = Thumbnail(pixmap, self.frame)
        self.verticalLayout.addWidget(thumbnail)
        thumbnail.select(True)
        thumbnail.clicked.connect(self.gridPaper.setPhoto)
        self.thumbnailGr.append(thumbnail)
        self.configureBtn.clicked.connect(self.configure)
        self.addPhotoBtn.clicked.connect(self.addPhoto)
        self.helpBtn.clicked.connect(self.showHelp)
        self.gridPaper.photo = pixmap

    def configure(self):
        dialog = GridSetupDialog(self)
        if dialog.exec_()==1:
            self.gridPaper.paperW = dialog.paperW
            self.gridPaper.paperH = dialog.paperH
            self.gridPaper.rows = dialog.rows
            self.gridPaper.cols = dialog.cols
            self.gridPaper.W = dialog.W
            self.gridPaper.H = dialog.H
            self.gridPaper.DPI = dialog.DPI
            self.gridPaper.setupGrid()

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
            self.thumbnailGr.append(thumbnail)

    def accept(self):
        # Create final grid when ok is clicked
        self.gridPaper.createFinalGrid()
        QDialog.accept(self)

    def showHelp(self):
        global helptext
        QMessageBox.about(self, 'How to Create Grid', helptext)

class Thumbnail(QLabel):
    clicked = pyqtSignal(QPixmap)
    def __init__(self, pixmap, parent):
        QLabel.__init__(self, parent)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.photo = pixmap
        self.setPixmap(pixmap.scaledToWidth(100))
        
    def mousePressEvent(self, ev):
        self.clicked.emit(self.photo)

    def select(self, select):
        if select:
            pm = self.photo.scaledToWidth(100)
            painter = QPainter(pm)
            pen = QPen(Qt.blue)
            pen.setWidth(4)
            painter.setPen(pen)
            painter.drawRect(2, 2 , 100-4, pm.height()-4)
            painter.end()
            self.setPixmap(pm)
        else:
            self.setPixmap(self.photo.scaledToWidth(100))

class ThumbnailGroup(QObject):
    def __init__(self, parent):
        QObject.__init__(self, parent)
        self.thumbnails = []

    def append(self, thumbnail):
        self.thumbnails.append(thumbnail)
        thumbnail.clicked.connect(self.selectThumbnail)

    def selectThumbnail(self):
        ''' This can only be used as slot connect to Thumbnail obj'''
        for thumbnail in self.thumbnails:
            thumbnail.select(False)
        self.sender().select(True)

class GridPaper(QLabel):
    def __init__(self, parent):
        QLabel.__init__(self, parent)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setMouseTracking(True)
        self.pixmap_dict = {}
        self.DPI = 300
        self.paperW, self.paperH = 1800, 1200
        self.W, self.H = 413, 531
        self.cols, self.rows = 4, 2           # total no. of columns and rows
        self.setupGrid()

    def setupGrid(self):
        self.boxes = []
        self.spacingX, self.spacingY = (self.paperW-self.cols*self.W)/(self.cols+1), (self.paperH-self.rows*self.H)/(self.rows+1)
        # Setup Foreground Grid
        screenDPI = QApplication.desktop().logicalDpiX()
        self.scale = screenDPI/self.DPI
        w, h = self.W*self.scale, self.H*self.scale
        spacing_x, spacing_y = self.spacingX*self.scale, self.spacingY*self.scale
        for i in range(self.cols*self.rows):
            row, col = i//self.cols, i%self.cols        # Position of the box as row & col
            box = QRect(spacing_x+col*(spacing_x+w), spacing_y+row*(spacing_y+h), w-1, h-1)
            #print(spacingX+col*(spacingX+w), spacingY+row*(spacingY+h), w, h)
            self.boxes.append(box)
        fg = QPixmap(self.paperW*self.scale, self.paperH*self.scale)
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
        blank_pm = QPixmap(self.W*self.scale, self.H*self.scale)
        blank_pm.fill()
        for box in self.boxes:
            if box.contains(ev.pos()):
                topleft = box.topLeft()
                #print(topleft.x(), topleft.y())
                pm = self.photo.scaled(self.W*self.scale, self.H*self.scale, 1, 1)
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
            row, col = index//self.cols, index%self.cols
            topleft = QPoint(self.spacingX+col*(self.spacingX+self.W), self.spacingY+row*(self.spacingY+self.H))
            pm = self.pixmap_dict[index].scaled(self.W, self.H, 1, 1)
            painter.drawPixmap(topleft, pm)
        painter.end()


class GridSetupDialog(QDialog, Ui_GridSetupDialog):
    def __init__(self, parent):
        QDialog.__init__(self, parent)
        self.setupUi(self)

    def accept(self):
        units = [1, 1/2.54, 1/25.4]
        DPI = self.spinDPI.value()
        unit_mult = units[self.paperSizeUnit.currentIndex()]
        paperW = self.spinPaperWidth.value()*unit_mult*DPI
        paperH = self.spinPaperHeight.value()*unit_mult*DPI
        W, H = self.spinPhotoWidth.value()*DPI/2.54, self.spinPhotoHeight.value()*DPI/2.54
        rows1, cols1 = int(paperH//H), int(paperW//W)
        rows2, cols2 = int(paperW//H), int(paperH//W)
        if rows1*cols1 >= rows2*cols2:
            self.paperW = paperW
            self.paperH = paperH
            self.rows = rows1
            self.cols = cols1
        else:
            self.paperW = paperH
            self.paperH = paperW
            self.rows = rows2
            self.cols = cols2
        self.W = W
        self.H = H
        self.DPI = DPI
        QDialog.accept(self)
