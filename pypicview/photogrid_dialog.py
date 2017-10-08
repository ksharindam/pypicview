# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'photogrid-dialog.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_GridDialog(object):
    def setupUi(self, GridDialog):
        GridDialog.setObjectName("GridDialog")
        GridDialog.resize(640, 480)
        self.gridLayout = QtWidgets.QGridLayout(GridDialog)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setHorizontalSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.frame = QtWidgets.QFrame(GridDialog)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout.setContentsMargins(2, 2, 2, 2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.addPhotoBtn = QtWidgets.QPushButton(self.frame)
        self.addPhotoBtn.setObjectName("addPhotoBtn")
        self.verticalLayout.addWidget(self.addPhotoBtn)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)
        self.scrollArea = QtWidgets.QScrollArea(GridDialog)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setAlignment(QtCore.Qt.AlignCenter)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 544, 442))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.scrollArea, 0, 1, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(GridDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 2)

        self.retranslateUi(GridDialog)
        self.buttonBox.accepted.connect(GridDialog.accept)
        self.buttonBox.rejected.connect(GridDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(GridDialog)

    def retranslateUi(self, GridDialog):
        _translate = QtCore.QCoreApplication.translate
        GridDialog.setWindowTitle(_translate("GridDialog", "Create Photo Grid"))
        self.addPhotoBtn.setText(_translate("GridDialog", "Add Photo"))

