# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/robertlanglois/workspace/arachnida/src/arachnid/core/gui/pyui/PlotViewer.ui'
#
# Created: Fri Aug 16 09:47:18 2013
#      by: pyside-uic 0.2.13 running on PySide 1.1.0
#
# WARNING! All changes made in this file will be lost!

from ..util.qt4_loader import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(762, 654)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.centralHLayout = QtGui.QHBoxLayout()
        self.centralHLayout.setObjectName("centralHLayout")
        self.plotDockWidget = QtGui.QDockWidget(self.centralwidget)
        self.plotDockWidget.setFeatures(QtGui.QDockWidget.AllDockWidgetFeatures)
        self.plotDockWidget.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea|QtCore.Qt.RightDockWidgetArea)
        self.plotDockWidget.setObjectName("plotDockWidget")
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.verticalLayout = QtGui.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout.setContentsMargins(2, 3, 2, 3)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget = QtGui.QWidget(self.dockWidgetContents)
        self.widget.setObjectName("widget")
        self.formLayout = QtGui.QFormLayout(self.widget)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.FieldsStayAtSizeHint)
        self.formLayout.setContentsMargins(0, 0, 0, 10)
        self.formLayout.setObjectName("formLayout")
        self.label = QtGui.QLabel(self.widget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.xComboBox = QtGui.QComboBox(self.widget)
        self.xComboBox.setObjectName("xComboBox")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.xComboBox)
        self.label_2 = QtGui.QLabel(self.widget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.yComboBox = QtGui.QComboBox(self.widget)
        self.yComboBox.setObjectName("yComboBox")
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.yComboBox)
        self.label_6 = QtGui.QLabel(self.widget)
        self.label_6.setObjectName("label_6")
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_6)
        self.colorComboBox = QtGui.QComboBox(self.widget)
        self.colorComboBox.setObjectName("colorComboBox")
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.colorComboBox)
        self.label_7 = QtGui.QLabel(self.widget)
        self.label_7.setObjectName("label_7")
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_7)
        self.subsetComboBox = QtGui.QComboBox(self.widget)
        self.subsetComboBox.setObjectName("subsetComboBox")
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.subsetComboBox)
        self.verticalLayout.addWidget(self.widget)
        self.subsetListView = QtGui.QListView(self.dockWidgetContents)
        self.subsetListView.setObjectName("subsetListView")
        self.verticalLayout.addWidget(self.subsetListView)
        self.widget_2 = QtGui.QWidget(self.dockWidgetContents)
        self.widget_2.setObjectName("widget_2")
        self.horizontalLayout = QtGui.QHBoxLayout(self.widget_2)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.selectAllPushButton = QtGui.QPushButton(self.widget_2)
        self.selectAllPushButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/mini/mini/tick.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.selectAllPushButton.setIcon(icon)
        self.selectAllPushButton.setObjectName("selectAllPushButton")
        self.horizontalLayout.addWidget(self.selectAllPushButton)
        self.unselectAllPushButton = QtGui.QPushButton(self.widget_2)
        self.unselectAllPushButton.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/mini/mini/shape_square.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.unselectAllPushButton.setIcon(icon1)
        self.unselectAllPushButton.setObjectName("unselectAllPushButton")
        self.horizontalLayout.addWidget(self.unselectAllPushButton)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addWidget(self.widget_2)
        self.plotDockWidget.setWidget(self.dockWidgetContents)
        self.centralHLayout.addWidget(self.plotDockWidget)
        self.horizontalLayout_2.addLayout(self.centralHLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar()
        self.menubar.setGeometry(QtCore.QRect(0, 0, 762, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtGui.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.imageDockWidget = QtGui.QDockWidget(MainWindow)
        self.imageDockWidget.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea|QtCore.Qt.RightDockWidgetArea)
        self.imageDockWidget.setObjectName("imageDockWidget")
        self.dockWidgetContents_2 = QtGui.QWidget()
        self.dockWidgetContents_2.setObjectName("dockWidgetContents_2")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.dockWidgetContents_2)
        self.verticalLayout_2.setContentsMargins(2, 3, 2, 3)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.widget_3 = QtGui.QWidget(self.dockWidgetContents_2)
        self.widget_3.setObjectName("widget_3")
        self.formLayout_2 = QtGui.QFormLayout(self.widget_3)
        self.formLayout_2.setContentsMargins(0, 10, 0, 10)
        self.formLayout_2.setObjectName("formLayout_2")
        self.keepSelectedCheckBox = QtGui.QCheckBox(self.widget_3)
        self.keepSelectedCheckBox.setText("")
        self.keepSelectedCheckBox.setObjectName("keepSelectedCheckBox")
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.FieldRole, self.keepSelectedCheckBox)
        self.label_9 = QtGui.QLabel(self.widget_3)
        self.label_9.setObjectName("label_9")
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_9)
        self.label_3 = QtGui.QLabel(self.widget_3)
        self.label_3.setObjectName("label_3")
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_3)
        self.imageCountSpinBox = QtGui.QSpinBox(self.widget_3)
        self.imageCountSpinBox.setObjectName("imageCountSpinBox")
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.FieldRole, self.imageCountSpinBox)
        self.selectGroupComboBox = QtGui.QComboBox(self.widget_3)
        self.selectGroupComboBox.setObjectName("selectGroupComboBox")
        self.formLayout_2.setWidget(4, QtGui.QFormLayout.FieldRole, self.selectGroupComboBox)
        self.label_11 = QtGui.QLabel(self.widget_3)
        self.label_11.setObjectName("label_11")
        self.formLayout_2.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_11)
        self.label_5 = QtGui.QLabel(self.widget_3)
        self.label_5.setObjectName("label_5")
        self.formLayout_2.setWidget(5, QtGui.QFormLayout.LabelRole, self.label_5)
        self.imageSepSpinBox = QtGui.QSpinBox(self.widget_3)
        self.imageSepSpinBox.setMinimum(1)
        self.imageSepSpinBox.setMaximum(1000)
        self.imageSepSpinBox.setSingleStep(1)
        self.imageSepSpinBox.setProperty("value", 40)
        self.imageSepSpinBox.setObjectName("imageSepSpinBox")
        self.formLayout_2.setWidget(5, QtGui.QFormLayout.FieldRole, self.imageSepSpinBox)
        self.imageZoomDoubleSpinBox = QtGui.QDoubleSpinBox(self.widget_3)
        self.imageZoomDoubleSpinBox.setMinimum(0.0)
        self.imageZoomDoubleSpinBox.setMaximum(10.0)
        self.imageZoomDoubleSpinBox.setSingleStep(0.1)
        self.imageZoomDoubleSpinBox.setProperty("value", 0.4)
        self.imageZoomDoubleSpinBox.setObjectName("imageZoomDoubleSpinBox")
        self.formLayout_2.setWidget(6, QtGui.QFormLayout.FieldRole, self.imageZoomDoubleSpinBox)
        self.label_8 = QtGui.QLabel(self.widget_3)
        self.label_8.setObjectName("label_8")
        self.formLayout_2.setWidget(6, QtGui.QFormLayout.LabelRole, self.label_8)
        self.averageCountSpinBox = QtGui.QSpinBox(self.widget_3)
        self.averageCountSpinBox.setMaximum(10000)
        self.averageCountSpinBox.setObjectName("averageCountSpinBox")
        self.formLayout_2.setWidget(3, QtGui.QFormLayout.FieldRole, self.averageCountSpinBox)
        self.label_4 = QtGui.QLabel(self.widget_3)
        self.label_4.setObjectName("label_4")
        self.formLayout_2.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_4)
        self.verticalLayout_2.addWidget(self.widget_3)
        self.imageDockWidget.setWidget(self.dockWidgetContents_2)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.imageDockWidget)
        self.fileDockWidget = QtGui.QDockWidget(MainWindow)
        self.fileDockWidget.setAllowedAreas(QtCore.Qt.BottomDockWidgetArea|QtCore.Qt.TopDockWidgetArea)
        self.fileDockWidget.setObjectName("fileDockWidget")
        self.dockWidgetContents_3 = QtGui.QWidget()
        self.dockWidgetContents_3.setObjectName("dockWidgetContents_3")
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.dockWidgetContents_3)
        self.verticalLayout_3.setContentsMargins(2, 2, 2, 2)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.fileTableView = QtGui.QTableView(self.dockWidgetContents_3)
        self.fileTableView.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.fileTableView.setProperty("showDropIndicator", False)
        self.fileTableView.setDragDropOverwriteMode(False)
        self.fileTableView.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.fileTableView.setObjectName("fileTableView")
        self.fileTableView.horizontalHeader().setStretchLastSection(True)
        self.fileTableView.verticalHeader().setVisible(False)
        self.verticalLayout_3.addWidget(self.fileTableView)
        self.fileDockWidget.setWidget(self.dockWidgetContents_3)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(8), self.fileDockWidget)
        self.advancedDockWidget = QtGui.QDockWidget(MainWindow)
        self.advancedDockWidget.setFloating(True)
        self.advancedDockWidget.setAllowedAreas(QtCore.Qt.NoDockWidgetArea)
        self.advancedDockWidget.setObjectName("advancedDockWidget")
        self.dockWidgetContents_4 = QtGui.QWidget()
        self.dockWidgetContents_4.setObjectName("dockWidgetContents_4")
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.dockWidgetContents_4)
        self.verticalLayout_4.setContentsMargins(2, 2, 2, 2)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.advancedSettingsTreeView = QtGui.QTreeView(self.dockWidgetContents_4)
        self.advancedSettingsTreeView.setEditTriggers(QtGui.QAbstractItemView.DoubleClicked|QtGui.QAbstractItemView.EditKeyPressed|QtGui.QAbstractItemView.SelectedClicked)
        self.advancedSettingsTreeView.setAlternatingRowColors(True)
        self.advancedSettingsTreeView.setIndentation(15)
        self.advancedSettingsTreeView.setUniformRowHeights(True)
        self.advancedSettingsTreeView.setObjectName("advancedSettingsTreeView")
        self.advancedSettingsTreeView.header().setCascadingSectionResizes(True)
        self.verticalLayout_4.addWidget(self.advancedSettingsTreeView)
        self.advancedDockWidget.setWidget(self.dockWidgetContents_4)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(4), self.advancedDockWidget)
        self.actionOpen = QtGui.QAction(MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/mini/mini/folder.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionOpen.setIcon(icon2)
        self.actionOpen.setObjectName("actionOpen")
        self.actionPan = QtGui.QAction(MainWindow)
        self.actionPan.setCheckable(True)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/mini/mini/arrow_out.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPan.setIcon(icon3)
        self.actionPan.setObjectName("actionPan")
        self.actionHome = QtGui.QAction(MainWindow)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/mini/mini/house.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionHome.setIcon(icon4)
        self.actionHome.setObjectName("actionHome")
        self.actionZoom = QtGui.QAction(MainWindow)
        self.actionZoom.setCheckable(True)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/mini/mini/zoom_out.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionZoom.setIcon(icon5)
        self.actionZoom.setObjectName("actionZoom")
        self.actionForward = QtGui.QAction(MainWindow)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/mini/mini/resultset_next.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionForward.setIcon(icon6)
        self.actionForward.setObjectName("actionForward")
        self.actionBackward = QtGui.QAction(MainWindow)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/mini/mini/resultset_previous.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionBackward.setIcon(icon7)
        self.actionBackward.setObjectName("actionBackward")
        self.actionSave = QtGui.QAction(MainWindow)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(":/mini/mini/disk.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSave.setIcon(icon8)
        self.actionSave.setObjectName("actionSave")
        self.actionShow_Options = QtGui.QAction(MainWindow)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(":/mini/mini/database_table.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionShow_Options.setIcon(icon9)
        self.actionShow_Options.setObjectName("actionShow_Options")
        self.actionHide_Controls = QtGui.QAction(MainWindow)
        self.actionHide_Controls.setCheckable(True)
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap(":/mini/mini/application_side_list.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionHide_Controls.setIcon(icon10)
        self.actionHide_Controls.setObjectName("actionHide_Controls")
        self.actionRefresh = QtGui.QAction(MainWindow)
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap(":/mini/mini/arrow_refresh.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionRefresh.setIcon(icon11)
        self.actionRefresh.setObjectName("actionRefresh")
        self.toolBar.addAction(self.actionOpen)
        self.toolBar.addAction(self.actionSave)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionHome)
        self.toolBar.addAction(self.actionBackward)
        self.toolBar.addAction(self.actionForward)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionPan)
        self.toolBar.addAction(self.actionZoom)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionRefresh)
        self.toolBar.addAction(self.actionShow_Options)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.plotDockWidget.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Plotting controls", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "x", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MainWindow", "y", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("MainWindow", "Color", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("MainWindow", "Subset", None, QtGui.QApplication.UnicodeUTF8))
        self.selectAllPushButton.setToolTip(QtGui.QApplication.translate("MainWindow", "Select All", None, QtGui.QApplication.UnicodeUTF8))
        self.unselectAllPushButton.setToolTip(QtGui.QApplication.translate("MainWindow", "Unselect All", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBar.setWindowTitle(QtGui.QApplication.translate("MainWindow", "toolBar", None, QtGui.QApplication.UnicodeUTF8))
        self.imageDockWidget.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Image Controls", None, QtGui.QApplication.UnicodeUTF8))
        self.label_9.setText(QtGui.QApplication.translate("MainWindow", "Keep Selected", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("MainWindow", "Count", None, QtGui.QApplication.UnicodeUTF8))
        self.label_11.setText(QtGui.QApplication.translate("MainWindow", "Highlight Group", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("MainWindow", "Separation", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("MainWindow", "Zoom", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("MainWindow", "Average", None, QtGui.QApplication.UnicodeUTF8))
        self.fileDockWidget.setWindowTitle(QtGui.QApplication.translate("MainWindow", "File Explorer", None, QtGui.QApplication.UnicodeUTF8))
        self.advancedDockWidget.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Advanced", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpen.setText(QtGui.QApplication.translate("MainWindow", "Open", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpen.setToolTip(QtGui.QApplication.translate("MainWindow", "Open a file to plot or a stack of images to display", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpen.setShortcut(QtGui.QApplication.translate("MainWindow", "Meta+O", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPan.setText(QtGui.QApplication.translate("MainWindow", "pan", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPan.setToolTip(QtGui.QApplication.translate("MainWindow", "Move the data in the plot", None, QtGui.QApplication.UnicodeUTF8))
        self.actionHome.setText(QtGui.QApplication.translate("MainWindow", "home", None, QtGui.QApplication.UnicodeUTF8))
        self.actionHome.setToolTip(QtGui.QApplication.translate("MainWindow", "Reset the view", None, QtGui.QApplication.UnicodeUTF8))
        self.actionZoom.setText(QtGui.QApplication.translate("MainWindow", "zoom", None, QtGui.QApplication.UnicodeUTF8))
        self.actionZoom.setToolTip(QtGui.QApplication.translate("MainWindow", "Use the cursor to zoom in on an area of the plot", None, QtGui.QApplication.UnicodeUTF8))
        self.actionForward.setText(QtGui.QApplication.translate("MainWindow", "forward", None, QtGui.QApplication.UnicodeUTF8))
        self.actionForward.setToolTip(QtGui.QApplication.translate("MainWindow", "Step forward in action history", None, QtGui.QApplication.UnicodeUTF8))
        self.actionBackward.setText(QtGui.QApplication.translate("MainWindow", "backward", None, QtGui.QApplication.UnicodeUTF8))
        self.actionBackward.setToolTip(QtGui.QApplication.translate("MainWindow", "Step backward in action history", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave.setText(QtGui.QApplication.translate("MainWindow", "save", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave.setToolTip(QtGui.QApplication.translate("MainWindow", "Save the current plot", None, QtGui.QApplication.UnicodeUTF8))
        self.actionShow_Options.setText(QtGui.QApplication.translate("MainWindow", "Show Options", None, QtGui.QApplication.UnicodeUTF8))
        self.actionShow_Options.setToolTip(QtGui.QApplication.translate("MainWindow", "Display dialog to configure plot options", None, QtGui.QApplication.UnicodeUTF8))
        self.actionHide_Controls.setText(QtGui.QApplication.translate("MainWindow", "Hide Controls", None, QtGui.QApplication.UnicodeUTF8))
        self.actionHide_Controls.setToolTip(QtGui.QApplication.translate("MainWindow", "Hide the controls", None, QtGui.QApplication.UnicodeUTF8))
        self.actionRefresh.setText(QtGui.QApplication.translate("MainWindow", "Refresh", None, QtGui.QApplication.UnicodeUTF8))
        self.actionRefresh.setToolTip(QtGui.QApplication.translate("MainWindow", "Replot the points and images", None, QtGui.QApplication.UnicodeUTF8))
        self.actionRefresh.setShortcut(QtGui.QApplication.translate("MainWindow", "Space", None, QtGui.QApplication.UnicodeUTF8))

from ..icons import icons_rc;icons_rc;
