# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'window.ui'
#
# Created: Sat Apr 21 14:40:25 2012
#      by: PyQt4 UI code generator 4.8.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(496, 434)
        MainWindow.setMinimumSize(QtCore.QSize(496, 411))
        MainWindow.setBaseSize(QtCore.QSize(496, 411))
        MainWindow.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Komunikator - 0.2", None, QtGui.QApplication.UnicodeUTF8))
        MainWindow.setAutoFillBackground(True)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.centralwidget.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.centralwidget.setAutoFillBackground(True)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.teKonwersacja = QtGui.QTextEdit(self.centralwidget)
        self.teKonwersacja.setGeometry(QtCore.QRect(0, -3, 391, 320))
        self.teKonwersacja.setFocusPolicy(QtCore.Qt.NoFocus)
        self.teKonwersacja.setStatusTip(QtGui.QApplication.translate("MainWindow", "Okno rozmowy", None, QtGui.QApplication.UnicodeUTF8))
        self.teKonwersacja.setAutoFillBackground(True)
        self.teKonwersacja.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.teKonwersacja.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.teKonwersacja.setAutoFormatting(QtGui.QTextEdit.AutoAll)
        self.teKonwersacja.setUndoRedoEnabled(False)
        self.teKonwersacja.setReadOnly(True)
        self.teKonwersacja.setHtml(QtGui.QApplication.translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Cantarell\'; font-size:11pt; font-weight:296;\"></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.teKonwersacja.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.teKonwersacja.setObjectName(_fromUtf8("teKonwersacja"))
        self.layoutWidget = QtGui.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(1, 319, 492, 71))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.leWyslij = QtGui.QPlainTextEdit(self.layoutWidget)
        self.leWyslij.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.leWyslij.setAcceptDrops(False)
        self.leWyslij.setAutoFillBackground(True)
        self.leWyslij.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.leWyslij.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.leWyslij.setTabChangesFocus(True)
        self.leWyslij.setOverwriteMode(False)
        self.leWyslij.setTabStopWidth(40)
        self.leWyslij.setObjectName(_fromUtf8("leWyslij"))
        self.horizontalLayout.addWidget(self.leWyslij)
        self.pbWyslij = QtGui.QPushButton(self.layoutWidget)
        self.pbWyslij.setToolTip(QtGui.QApplication.translate("MainWindow", "Wyślij wiadomość", None, QtGui.QApplication.UnicodeUTF8))
        self.pbWyslij.setStatusTip(_fromUtf8(""))
        self.pbWyslij.setAutoFillBackground(True)
        self.pbWyslij.setText(QtGui.QApplication.translate("MainWindow", "Wyślij", None, QtGui.QApplication.UnicodeUTF8))
        self.pbWyslij.setObjectName(_fromUtf8("pbWyslij"))
        self.horizontalLayout.addWidget(self.pbWyslij)
        self.lvUzytkownicy = QtGui.QListWidget(self.centralwidget)
        self.lvUzytkownicy.setGeometry(QtCore.QRect(393, -1, 103, 318))
        self.lvUzytkownicy.setStatusTip(QtGui.QApplication.translate("MainWindow", "Lista użytkowników", None, QtGui.QApplication.UnicodeUTF8))
        self.lvUzytkownicy.setAutoFillBackground(True)
        self.lvUzytkownicy.setAutoScroll(False)
        self.lvUzytkownicy.setEditTriggers(QtGui.QAbstractItemView.AllEditTriggers)
        self.lvUzytkownicy.setDefaultDropAction(QtCore.Qt.IgnoreAction)
        self.lvUzytkownicy.setAlternatingRowColors(True)
        self.lvUzytkownicy.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.lvUzytkownicy.setVerticalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        self.lvUzytkownicy.setHorizontalScrollMode(QtGui.QAbstractItemView.ScrollPerItem)
        self.lvUzytkownicy.setObjectName(_fromUtf8("lvUzytkownicy"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 496, 22))
        self.menubar.setAutoFillBackground(True)
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuPlik = QtGui.QMenu(self.menubar)
        self.menuPlik.setTitle(QtGui.QApplication.translate("MainWindow", "Rozmowa", None, QtGui.QApplication.UnicodeUTF8))
        self.menuPlik.setObjectName(_fromUtf8("menuPlik"))
        self.menuStatus = QtGui.QMenu(self.menubar)
        self.menuStatus.setTitle(QtGui.QApplication.translate("MainWindow", "Status", None, QtGui.QApplication.UnicodeUTF8))
        self.menuStatus.setObjectName(_fromUtf8("menuStatus"))
        self.menuEdycja = QtGui.QMenu(self.menubar)
        self.menuEdycja.setTitle(QtGui.QApplication.translate("MainWindow", "Edycja", None, QtGui.QApplication.UnicodeUTF8))
        self.menuEdycja.setObjectName(_fromUtf8("menuEdycja"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setAutoFillBackground(True)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionZakoncz = QtGui.QAction(MainWindow)
        self.actionZakoncz.setText(QtGui.QApplication.translate("MainWindow", "Za&kończ", None, QtGui.QApplication.UnicodeUTF8))
        self.actionZakoncz.setStatusTip(QtGui.QApplication.translate("MainWindow", "Wyjście z programu", None, QtGui.QApplication.UnicodeUTF8))
        self.actionZakoncz.setObjectName(_fromUtf8("actionZakoncz"))
        self.actionDostepny = QtGui.QAction(MainWindow)
        self.actionDostepny.setCheckable(True)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("icons/available.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionDostepny.setIcon(icon)
        self.actionDostepny.setText(QtGui.QApplication.translate("MainWindow", "&Dostępny", None, QtGui.QApplication.UnicodeUTF8))
        self.actionDostepny.setStatusTip(QtGui.QApplication.translate("MainWindow", "Gdy jesteś przy komputerze", None, QtGui.QApplication.UnicodeUTF8))
        self.actionDostepny.setIconVisibleInMenu(True)
        self.actionDostepny.setObjectName(_fromUtf8("actionDostepny"))
        self.actionZarazWracam = QtGui.QAction(MainWindow)
        self.actionZarazWracam.setCheckable(True)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8("icons/away.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionZarazWracam.setIcon(icon1)
        self.actionZarazWracam.setText(QtGui.QApplication.translate("MainWindow", "Zaraz wracam", None, QtGui.QApplication.UnicodeUTF8))
        self.actionZarazWracam.setStatusTip(QtGui.QApplication.translate("MainWindow", "Gdy nie ma cię przy komputerze", None, QtGui.QApplication.UnicodeUTF8))
        self.actionZarazWracam.setIconVisibleInMenu(True)
        self.actionZarazWracam.setObjectName(_fromUtf8("actionZarazWracam"))
        self.actionZajety = QtGui.QAction(MainWindow)
        self.actionZajety.setCheckable(True)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8("icons/busy.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionZajety.setIcon(icon2)
        self.actionZajety.setText(QtGui.QApplication.translate("MainWindow", "Zajęty", None, QtGui.QApplication.UnicodeUTF8))
        self.actionZajety.setStatusTip(QtGui.QApplication.translate("MainWindow", "Gdy nie masz czasu na rozmowę, bo jesteś zajęty", None, QtGui.QApplication.UnicodeUTF8))
        self.actionZajety.setIconVisibleInMenu(True)
        self.actionZajety.setObjectName(_fromUtf8("actionZajety"))
        self.actionNiedostepny = QtGui.QAction(MainWindow)
        self.actionNiedostepny.setCheckable(True)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8("icons/offline.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionNiedostepny.setIcon(icon3)
        self.actionNiedostepny.setText(QtGui.QApplication.translate("MainWindow", "Niedostępny", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNiedostepny.setStatusTip(QtGui.QApplication.translate("MainWindow", "Gdy chcesz się rozłączyć", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNiedostepny.setIconVisibleInMenu(True)
        self.actionNiedostepny.setObjectName(_fromUtf8("actionNiedostepny"))
        self.actionZapiszRozmoweHtml = QtGui.QAction(MainWindow)
        self.actionZapiszRozmoweHtml.setText(QtGui.QApplication.translate("MainWindow", "Zapisz rozmowę jako &HTML", None, QtGui.QApplication.UnicodeUTF8))
        self.actionZapiszRozmoweHtml.setStatusTip(QtGui.QApplication.translate("MainWindow", "Zapisuje rozmowę do pliku HTML", None, QtGui.QApplication.UnicodeUTF8))
        self.actionZapiszRozmoweHtml.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+Shift+S", None, QtGui.QApplication.UnicodeUTF8))
        self.actionZapiszRozmoweHtml.setObjectName(_fromUtf8("actionZapiszRozmoweHtml"))
        self.actionZapiszRozmoweTekst = QtGui.QAction(MainWindow)
        self.actionZapiszRozmoweTekst.setText(QtGui.QApplication.translate("MainWindow", "Zapisz rozmowę jako &tekst", None, QtGui.QApplication.UnicodeUTF8))
        self.actionZapiszRozmoweTekst.setStatusTip(QtGui.QApplication.translate("MainWindow", "Zapisuje rozmowę jako zwykły tekst", None, QtGui.QApplication.UnicodeUTF8))
        self.actionZapiszRozmoweTekst.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+S", None, QtGui.QApplication.UnicodeUTF8))
        self.actionZapiszRozmoweTekst.setObjectName(_fromUtf8("actionZapiszRozmoweTekst"))
        self.actionWyczyscOknoRozmowy = QtGui.QAction(MainWindow)
        self.actionWyczyscOknoRozmowy.setText(QtGui.QApplication.translate("MainWindow", "Wyczyść okno rozmowy", None, QtGui.QApplication.UnicodeUTF8))
        self.actionWyczyscOknoRozmowy.setIconText(QtGui.QApplication.translate("MainWindow", "Wyczyść okno &rozmowy", None, QtGui.QApplication.UnicodeUTF8))
        self.actionWyczyscOknoRozmowy.setStatusTip(QtGui.QApplication.translate("MainWindow", "Czyści okno rozmowy", None, QtGui.QApplication.UnicodeUTF8))
        self.actionWyczyscOknoRozmowy.setObjectName(_fromUtf8("actionWyczyscOknoRozmowy"))
        self.actionSkopiuj = QtGui.QAction(MainWindow)
        self.actionSkopiuj.setEnabled(False)
        self.actionSkopiuj.setText(QtGui.QApplication.translate("MainWindow", "S&kopiuj", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSkopiuj.setStatusTip(QtGui.QApplication.translate("MainWindow", "Kopiuje zaznaczony tekst do schowka", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSkopiuj.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+C", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSkopiuj.setObjectName(_fromUtf8("actionSkopiuj"))
        self.actionWklej = QtGui.QAction(MainWindow)
        self.actionWklej.setEnabled(False)
        self.actionWklej.setText(QtGui.QApplication.translate("MainWindow", "Wk&lej", None, QtGui.QApplication.UnicodeUTF8))
        self.actionWklej.setStatusTip(QtGui.QApplication.translate("MainWindow", "Wkleja zaznaczony tekst ze schowka", None, QtGui.QApplication.UnicodeUTF8))
        self.actionWklej.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+V", None, QtGui.QApplication.UnicodeUTF8))
        self.actionWklej.setObjectName(_fromUtf8("actionWklej"))
        self.actionWytnij = QtGui.QAction(MainWindow)
        self.actionWytnij.setEnabled(False)
        self.actionWytnij.setText(QtGui.QApplication.translate("MainWindow", "Wy&tnij", None, QtGui.QApplication.UnicodeUTF8))
        self.actionWytnij.setStatusTip(QtGui.QApplication.translate("MainWindow", "Wycina zaznaczony tekst do schowka", None, QtGui.QApplication.UnicodeUTF8))
        self.actionWytnij.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+X", None, QtGui.QApplication.UnicodeUTF8))
        self.actionWytnij.setObjectName(_fromUtf8("actionWytnij"))
        self.actionZnajdz = QtGui.QAction(MainWindow)
        self.actionZnajdz.setText(QtGui.QApplication.translate("MainWindow", "Znajdź", None, QtGui.QApplication.UnicodeUTF8))
        self.actionZnajdz.setStatusTip(QtGui.QApplication.translate("MainWindow", "Znjaduje tekst w oknie rozmowy", None, QtGui.QApplication.UnicodeUTF8))
        self.actionZnajdz.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+F", None, QtGui.QApplication.UnicodeUTF8))
        self.actionZnajdz.setVisible(False)
        self.actionZnajdz.setIconVisibleInMenu(False)
        self.actionZnajdz.setObjectName(_fromUtf8("actionZnajdz"))
        self.actionPreferencje = QtGui.QAction(MainWindow)
        self.actionPreferencje.setText(QtGui.QApplication.translate("MainWindow", "&Preferencje...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPreferencje.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+P", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPreferencje.setObjectName(_fromUtf8("actionPreferencje"))
        self.menuPlik.addAction(self.actionZapiszRozmoweHtml)
        self.menuPlik.addAction(self.actionZapiszRozmoweTekst)
        self.menuPlik.addAction(self.actionWyczyscOknoRozmowy)
        self.menuPlik.addSeparator()
        self.menuPlik.addAction(self.actionZakoncz)
        self.menuStatus.addAction(self.actionDostepny)
        self.menuStatus.addAction(self.actionZarazWracam)
        self.menuStatus.addAction(self.actionZajety)
        self.menuStatus.addAction(self.actionNiedostepny)
        self.menuEdycja.addAction(self.actionSkopiuj)
        self.menuEdycja.addSeparator()
        self.menuEdycja.addAction(self.actionZnajdz)
        self.menuEdycja.addSeparator()
        self.menuEdycja.addAction(self.actionPreferencje)
        self.menubar.addAction(self.menuPlik.menuAction())
        self.menubar.addAction(self.menuEdycja.menuAction())
        self.menubar.addAction(self.menuStatus.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.actionZakoncz, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        self.lvUzytkownicy.setSortingEnabled(True)

