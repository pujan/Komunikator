#!/usr/bin/env python
#-*- coding: utf-8 -*-

u"""
Author: Łukasz 'Pujan' Pelc
Email: pujan8@o2.pl
Wyprodukowane w Polsce - 2011-2012
"""

import sys, os, time, re
from PyQt4 import QtCore, QtGui
from win.windowUi import Ui_MainWindow
from win.preferencjeUi import Ui_Dialog
from com import siec, log, dzwiek
from com.konfiguracja import Konfiguracja
import com.typWiadomosci as tw
import com.typStatusu as ts
import win.windowUi

DEBUG = True

class Main( QtGui.QMainWindow ):
    u"""Główne okno programu."""
    
    def __init__( self ):
        QtGui.QMainWindow.__init__( self )
        
        # to jest zawsze takie samo
        self.ui = Ui_MainWindow()
        self.ui.setupUi( self )
        self.komunikatWyjscia = False
        
        # ikonka w zasobniku systemowym (tray)
        self.tray = QtGui.QSystemTrayIcon( self )
        if self.tray.isSystemTrayAvailable():
            self.tray.setIcon( QtGui.QIcon(os.path.join('icons', 'busy.png')) )
            self.tray.show()
            self.tray.activated.connect( self.activate )
        
        # ikonka okna głównego
        self.setWindowIcon( QtGui.QIcon(os.path.join('icons', 'busy.png')) )
        
        # okno preferencji
        self.initPreferencje()
        
        self.ui.leWyslij.installEventFilter( self )
        
        self.cfg = Konfiguracja()
        self.cfg.loadConfig()
        
        self.setGeometry( self.cfg.getWindowPosition()[ 0 ], \
            self.cfg.getWindowPosition()[ 1 ], \
            self.cfg.getWindowSize()[ 0 ], \
            self.cfg.getWindowSize()[ 1 ] )
        
        # histora rozmowy
        self.log = None
        
        # dzień miesiąca po zmianie dnia zmieniamy plik log na inny
        self.dzien = time.strftime( '%d' )
        self.WlWylHistorie( self.cfg.getLogsSave() )
        
        # początkowy status
        self.status = ts.STS_AVAILABLE
        
        # sieć
        self.recv = siec.Odbieranie()
        self.recv.start( QtCore.QThread.HighPriority )
        self.send = siec.Wysylanie()
        
        # dzwięk
        self.snd = dzwiek.Dzwiek(self.cfg.getSoundOn(), self.cfg.getSoundMsg())
        
        # połączenia obiektow z metodami
        self.connect( self.ui.pbWyslij, QtCore.SIGNAL('clicked()'), \
                      self.slWyslij )
        self.connect( self.ui.leWyslij, QtCore.SIGNAL('returnPressed()'), \
                      self.slWyslij )
        self.connect( self.ui.teKonwersacja, QtCore.SIGNAL('selectionChanged()'), \
                      self.slUaktywnijOpcje )
        self.ui.lvUzytkownicy.addItem( QtGui.QListWidgetItem( \
                QtGui.QIcon("icons/" + self.status + ".png"), \
                self.cfg.nazwaUzytkownika) )
        
        # połączenia menu z metodami
        self.ui.actionDostepny.triggered.connect( self.slStatusDostepny )
        self.ui.actionZarazWracam.triggered.connect( self.slStatusZarazWracam )
        self.ui.actionZajety.triggered.connect( self.slStatusZajety )
        self.ui.actionNiedostepny.triggered.connect( self.slStatusNiedostepny )
        self.ui.actionZapiszRozmoweHtml.triggered.connect( self.slZapiszRozmoweJakoHTML )
        self.ui.actionZapiszRozmoweTekst.triggered.connect( self.slZapiszRozmoweJakoTXT )
        self.ui.actionWyczyscOknoRozmowy.triggered.connect( self.slCzyscOnkoRozmowy )
        self.ui.actionSkopiuj.triggered.connect( self.slSkopiujTekst )
        self.ui.actionPreferencje.triggered.connect( self.slPreferencje )
        
        # odbieranie pakietów co 400 msek.
        self.timer = QtCore.QTimer( self )
        self.timer.connect( self.timer, QtCore.SIGNAL('timeout()'), self.odswiezWiadomosci )
        self.timer.setInterval( 400 )
        
        # wysylanie zapytania o nazwę uzytkownika
        self.timerUpdateUser = QtCore.QTimer( self )
        self.timerUpdateUser.connect( self.timerUpdateUser, \
                                      QtCore.SIGNAL('timeout()'), \
                                      self.ZapytajOStatus )
        self.timerUpdateUser.setInterval( 15000 )
        
        # odswierzenie listy uzytkowników
        self.timerUserList = QtCore.QTimer( self )
        self.timerUserList.connect( self.timerUserList, \
                                    QtCore.SIGNAL('timeout()'), \
                                    self.odswiezListeUzytkownikow )
        self.timerUserList.setInterval( 1500 )
        
        # proba wyslania pakietu z odpowiedzia na zapytanie czy się jest
        self.timerRequest = QtCore.QTimer( self )
        self.timerRequest.connect( self.timerRequest, \
                                   QtCore.SIGNAL('timeout()'), \
                                   self.wyslijMojStatus )
        self.timerRequest.setInterval( 5000 )
        
        # sprawdza czy nie zmienila sie data
        self.timerDiffDay = QtCore.QTimer( self )
        self.timerDiffDay.connect( self.timerDiffDay, \
                                   QtCore.SIGNAL('timeout()'), \
                                   self.slPorownajDzien )
        self.timerDiffDay.setInterval( 1000 )
        
        # startujemy wszystkie timery
        self.startTimers()
        # status początkowy
        self.poczatkowyStatus()
        
        self.ZapytajOStatus()
        self.wyslijMojStatus()
        self.odswiezListeUzytkownikow()
        
        # kontekstowe menu okna rozmowy
        self.ui.teKonwersacja.setContextMenuPolicy( QtCore.Qt.CustomContextMenu )
        self.connect( self.ui.teKonwersacja, \
                      QtCore.SIGNAL('customContextMenuRequested(QPoint)'), \
                      self.slMenuKontekstoweRozmowy )
        
        self.connect( self.ui.leWyslij, \
                      QtCore.SIGNAL('customContextMenuRequested(QPoint)'), \
                      self.slMenuKontekstoweEdytora )
        
        self.dodajDoKonferencji( 'Witaj ' + self.cfg.getNick() + \
            ' w programie Komunikator!', tw.MSG_OTHER )
    
    def activate( self, reason ):
        u"""Funkcja obsługi przysków myszki dla ikonki w zasobniku systemowym.""" 
        #print reason 
        if reason == 2: # podwójne kliknięcie
            self.show()
        elif reason == 1: # prawy przycisk
            self.slMenuKontekstoweTraya()
    
    def startTimers( self ):
        u"Funkcja uruchamia wszystkie timery jeżeli były zatrzymane."
        if not self.timer.isActive():
            self.timer.start()
        
        if not self.timerUpdateUser.isActive():
            self.timerUpdateUser.start()
        
        if not self.timerUserList.isActive():
            self.timerUserList.start()
        
        if not self.timerRequest.isActive():
            self.timerRequest.start()
        
        if not self.timerDiffDay.isActive():
            self.timerDiffDay.start()
    
    def stopTimers( self ):
        u"Funkcja zatrzymuje wszystkie timery."
        self.timer.stop()
        self.timerUpdateUser.stop()
        self.timerUserList.stop()
        self.timerRequest.stop()
        self.timerDiffDay.stop()
    
    def ZapytajOStatus( self ):
        u"""Funkcja odswierza listę użytkowników wraz z zapytaniem kto jest obecny."""
        pass
        # wysylamy pakiet z zapytaniem
        #self.send.send( {'hello':"", 'user':""} )
        
        #print u"ZapytajOStatus():" # DEBUG
    
    def odswiezWiadomosci( self ):
        u"""Funkcja dopisuje do QTextEdit wartość zmiennej globalnej message."""
        
        if siec.message != None:
            if siec.message.has_key( 'msg' ) and siec.message[ 'user' ] != self.cfg.getNick():
                msg = "<b>:: " + siec.message[ 'user' ] + " ::</b> " \
                    + time.strftime( "%d-%m-%Y %H:%M:%S" ) + "<br/>" \
                    + siec.message[ 'msg' ]
                
                self.dodajDoKonferencji( msg, tw.MSG_NETWORK )
                siec.message = None
        
        #print u"odswiezWiadomosci():" # DEBUG
    
    def odswiezListeUzytkownikow( self ):
        u"""Funkcja uaktualnia listę użytkowników."""
        
        # print "infoUser:", siec.infoUser # DEBUG
        # print "Users:", siec.Users # DEBUG
        
        if len( siec.Users ) != 0:
            self.dodajUzytkownikow( siec.Users.values() )
        
        #print u"odswiezListeUzytkownikow():" # DEBUG
    
    def wyslijMojStatus( self ):
        u"""Funkcja odpowiada na polecenie żądania nazwy użytkownika."""
        
        if self.status == ts.STS_OFFLINE:
            # gdy jesteśmy nie widoczni bądź offline nie wysyłamy
            # informacji o swoim statusie
            self.slStatusNiedostepny()
            return
        
        if self.send.network:
            #print u"Sieć dostępna!" # DEBUG
            #if siec.infoUser != None:
                #if siec.infoUser[ 'hello' ] == '':
            self.send.send( {'hello':self.status, 'user':self.cfg.getNick()} )
                    #self.send.network = False
        
        #print u"wyslijMojStatus():" # DEBUG
    
    def dodajUzytkownikow( self, uzytkownicy=[] ):
        u"""odświerza listę użytkowników."""
        self.ui.lvUzytkownicy.clear()
        
        #print "dd dodaje uzytkownikow" # DEBUG
        
        for item in uzytkownicy:
            if item[ 'user' ] == self.cfg.getNick():
                continue
            
            self.ui.lvUzytkownicy.addItem( \
                QtGui.QListWidgetItem( QtGui.QIcon( \
                    os.path.join('icons', item[ 'status' ] + '.png')), \
                                 item[ 'user' ] ))
        
        self.ui.lvUzytkownicy.addItem( \
            QtGui.QListWidgetItem( QtGui.QIcon( \
                os.path.join('icons', self.status + '.png')), \
                             unicode(self.cfg.getNick()) ) )
    
    def zmienMojStatus( self ):
        items = self.ui.lvUzytkownicy.findItems( self.cfg.getNick(), \
                                                 QtCore.Qt.MatchFixedString )
        items[ 0 ].setIcon( QtGui.QIcon(os.path.join("icons", \
                                                     self.status + ".png")) )
    
    def zmienMojNick( self, staryNick ):
        items = self.ui.lvUzytkownicy.findItems( staryNick, \
                                                 QtCore.Qt.MatchFixedString )
        items[ 0 ].setText( unicode(self.cfg.getNick()) )
        
        if len( siec.Users ) != 0:
            for user in siec.Users.values():
                if user[ 'user' ] == staryNick:
                    user[ 'user' ] = self.cfg.getNick()
    
    def dodajDoKonferencji( self, msg, rodzaj ):
        u"""Funkcja dodaje tekst do okna rozmowy."""
        
        # zapis rozmowy, zezeli włączono opcje zapisu do pliku
        if self.cfg.getLogsSave():
            # odczytujemy tylko wiadomość
            wiadomosc = unicode( msg )
            pos = wiadomosc.find( '<br/>' )
            
            if pos != -1:
                dane = win.windowUi._fromUtf8( '[' \
                    + time.strftime( '%H:%M:%S' ) + '] <' \
                    + self.cfg.getNick() + '>\n' \
                    + wiadomosc[ pos + len('<br/>') : ] + '\n' )
                
                self.log.dopisz( unicode(dane) )
            elif self.cfg.getLogsSaveInfo():
                dane = win.windowUi._fromUtf8( '[' \
                    + time.strftime( '%H:%M:%S' ) + '] ' \
                    + wiadomosc + '\n' )
                
                self.log.dopisz( unicode(dane) )
        
        msg.replace( '\n', '<br/>' )
        
        if rodzaj == tw.MSG_LOCAL:
            msg = '<span style="color:' + self.cfg.getColorMsgLocal() \
                + ';">' + msg + '</span>'
        elif rodzaj == tw.MSG_NETWORK:
            msg = '<span style="color:' + self.cfg.getColorMsgNetwork() \
                + ';">' + msg + '</span>'
            
            if self.cfg.getSoundOn():
                self.snd.graj()
            
            if self.cfg.getBeepOn():
                self.snd.beep()
            
        elif rodzaj == tw.MSG_INFO:
            msg = '<span style="color:' + self.cfg.getColorMsgInfo() \
                + ';">' + msg + '</span>'
            self.snd.beep()
        elif rodzaj == tw.MSG_OTHER:
            msg = '<span style="color:' + self.cfg.getColorMsgInfo() \
                + ';">' + msg + '</span>'
        
        self.ui.teKonwersacja.append( QtCore.QString(msg) )
    
    def odbierz( self ):
        msg, addr = self.rcvsock.recvfrom( 1024 )
        self.ui.teKonwersacja.append( msg )
        
        if DEBUG:
            print 'odebrano od:', addr, 'wiadomość:', msg
    
    def wyslijStatus( self ):
        u"""Wysyla status z nazwą użytkownika do w sieć."""
        self.send.send( {'hello':self.status, 'user':self.cfg.getNick()} )
    
    def odznaczWszystkieStatusy( self ):
        u"""Funkcja odznacza wszystkie statusy w menu."""
        self.ui.actionDostepny.setChecked( False )
        self.ui.actionZarazWracam.setChecked( False )
        self.ui.actionZajety.setChecked( False )
        self.ui.actionNiedostepny.setChecked( False )
    
    def wypelnijOknoPreferencji( self ):
        # ogólne
        status = {'available' : 0, 'away' : 1, 'busy' : 2, 'offline' : 3}
        self.prefDialog.ui.leNick.setText( QtCore.QString(unicode(self.cfg.getNick())) )
        self.prefDialog.ui.cbStatus.setCurrentIndex( status[ self.cfg.getStatus() ] )
        self.prefDialog.ui.chbEnterSend.setChecked( self.cfg.getEnterSend() )
        # historia
        self.prefDialog.ui.chbZapiszRozmowe.setChecked( self.cfg.getLogsSave() )
        self.prefDialog.ui.chbZapiszPowiadomienia.setChecked( self.cfg.getLogsSaveInfo() )
        self.prefDialog.ui.leKatalogHistorii.setText( self.cfg.getLogsDir() )
        self.prefDialog.ui.leNazwaPliku.setText( self.cfg.getLogsFilename() )
        # dźwięk
        self.prefDialog.ui.chbGlosnik.setChecked( self.cfg.getBeepOn() )
        self.prefDialog.ui.chbDzwiek.setChecked( self.cfg.getSoundOn() )
        self.prefDialog.ui.leDzwiekPrzychodzacej.setText( self.cfg.getSoundMsg() )
        self.prefDialog.ui.leDzwiekDolaczenia.setText( self.cfg.getSoundJoin() )
        # kolory
        self.prefDialog.ui.frmKolorPrzychodzacej.setStyleSheet( \
            'QFrame { background-color:%s }' % self.cfg.getColorMsgNetwork() )
        self.prefDialog.ui.frmKolorWyslanej.setStyleSheet( \
            'QFrame { background-color:%s }' % self.cfg.getColorMsgLocal() )
        self.prefDialog.ui.frmKolorKomunikatu.setStyleSheet( \
            'QFrame { background-color:%s }' % self.cfg.getColorMsgInfo() )
        self.slUkryjOpcjeHistorii()
        self.slUkryjOpcjeDzwieku()
    
    def zmienPreferencje( self ):
        nick = self.cfg.getNick()
        # ogólne
        status = {0 : 'available', 1 : 'away', 2 : 'busy', 3 : 'offline'}
        self.cfg.setNick( str(self.prefDialog.ui.leNick.text()) )
        self.cfg.setStatus( status[ self.prefDialog.ui.cbStatus.currentIndex() ] )
        self.cfg.setEnterSend( self.prefDialog.ui.chbEnterSend.isChecked() )
        # historia
        self.cfg.setLogsSave( self.prefDialog.ui.chbZapiszRozmowe.isChecked() )
        self.cfg.setLogsSaveInfo( self.prefDialog.ui.chbZapiszPowiadomienia.isChecked() )
        self.cfg.setLogsDir( str(self.prefDialog.ui.leKatalogHistorii.text()) )
        self.cfg.setLogsFilename( str(self.prefDialog.ui.leNazwaPliku.text()) )
        # dźwięk
        self.cfg.setBeepOn( self.prefDialog.ui.chbGlosnik.isChecked() )
        self.cfg.setSoundOn( self.prefDialog.ui.chbDzwiek.isChecked() )
        self.cfg.setSoundMsg( str(self.prefDialog.ui.leDzwiekPrzychodzacej.text()) )
        self.cfg.setSoundJoin( str(self.prefDialog.ui.leDzwiekDolaczenia.text()) )
        # kolory
        cssKolor = str( self.prefDialog.ui.frmKolorPrzychodzacej.styleSheet() )
        reg = re.compile( r'#[a-fA-F0-9]{6}' )
        self.cfg.setColorMsgNetwork( reg.search( cssKolor ).group() )
        
        cssKolor = str( self.prefDialog.ui.frmKolorWyslanej.styleSheet() )
        self.cfg.setColorMsgLocal( reg.search( cssKolor ).group() )
        
        cssKolor = str( self.prefDialog.ui.frmKolorKomunikatu.styleSheet() )
        self.cfg.setColorMsgInfo( reg.search( cssKolor ).group() )
        
        # zmiana opcji programu
        self.zmienMojNick( nick )
        self.WlWylHistorie( self.cfg.getLogsSave() )
        
        # zamykamy okno
        self.prefDialog.close()
    
    def rgbToHtml( self, r, g, b ):
        u"""Konwertuje kolor z wartości RGB 0, 0, 0 na HTML '#000000'.""" 
        if r < 10: rStr = '0' + hex( r )[ 2 : ]
        else: rStr = hex( r )[ 2 : ]
        
        if g < 10: gStr = '0' + hex( g )[ 2 : ]
        else: gStr = hex( g )[ 2 : ]
        
        if b < 10:  bStr = '0' + hex( b )[ 2 : ]
        else: bStr = hex( b )[ 2 : ]
        
        if DEBUG:
            print '#' + rStr + gStr + bStr # DEBUG
        
        return '#' + rStr + gStr + bStr
    
    def htmlToRgb( self, htmlKolor ):
        u"""Konwertuje kolor z wartości HTML '#000000' na RGB (0,0,0)."""
        if DEBUG:
            print htmlKolor # DEBUG
        
        if htmlKolor[ 0 ] != '#':
            raise TypeError
        
        if len( htmlKolor ) == 7:
            print u'Dlugość koloru 7!'
            return (int(htmlKolor[ 1 : 3 ], 16), int(htmlKolor[ 3 : 5 ], 16), \
                    int(htmlKolor[ 5 : ], 16))
        elif len( htmlKolor ) == 4:
            print u'Długość koloru 4!'
            return (int(htmlKolor[ 1 : 2 ]*2, 16), \
                    int(htmlKolor[ 2 : 3 ]*2, 16), int(htmlKolor[ 3 ]*2, 16))
        else:
            raise AttributeError
        
        return (0, 0, 0)
    
    def pobierzKolor( self, defaultColor=(0,0,0) ):
        clr = QtGui.QColor( defaultColor[0], defaultColor[1], defaultColor[2] )
        dlg = QtGui.QColorDialog( self )
        dlg.setCurrentColor( clr )
        kolor = QtGui.QColor( clr )
        
        if DEBUG:
            print u"Domyślny kolor:", defaultColor
        
        if dlg.exec_() == QtGui.QDialog.Accepted:
            kolor = dlg.currentColor()
        #else:
        #    print u"Przyciśnięto 'Cancel' w QColorDialog."
        
        if DEBUG:
            print "Pobrany kolor: ", kolor.red(), kolor.green(), kolor.blue()
        
        return self.rgbToHtml( kolor.red(), kolor.green(), kolor.blue() )
    
    def WlWylHistorie( self, zapisz ):
        if zapisz:
            try:
                os.stat( self.cfg.getLogsDir() )
            except OSError:
                try:
                    os.mkdir( self.cfg.getLogsDir() )
                except:
                    self.cfg.setLogsSave( False )
                    print 'Nie mogę utworzyć kotalogu zapisu dziennika!'
                    print 'Sprawdź prawa dostępu lub czy jest miejsce na dysku!'
                    print 'Wyłączyłem zapisywanie do dziennika.'
            
            self.log = log.Log( os.path.join( self.cfg.getLogsDir(), \
                                    time.strftime(self.cfg.getLogsFilename())) )
            self.dzien = time.strftime('%d')
        else:
            if self.cfg.getLogsSave():
                try:
                    self.log.close()
                except TypeError:
                    pass
            #self.log = None
    
    def wybierzPlikDzwiekowy( self ):
        return QtGui.QFileDialog.getOpenFileName( self, \
            u'Otwórz plik dźwiękuwy', '.', 'Pliki Wave (*.wav *.WAV)' )
    
    def zapisz( self, nazwaPliku, dane ):
        u"""Funkcja zapisująca rozmowe do pliku tekstowego."""
        try:
            plik = open( nazwaPliku, "w" )
            plik.write( dane )
        finally:
            plik.close()
    
    def poczatkowyStatus( self ):
        u"""Początkowy status po właczeniu komunikatora.
            Odczytywany z opcji."""
        self.status = self.cfg.getStatus()
        if self.status == ts.STS_AVAILABLE:
            self.slStatusDostepny()
        elif self.status == ts.STS_AWAY:
            self.slStatusZarazWracam()
        elif self.status == ts.STS_BUSY:
            self.slStatusZajety()
        elif self.status == ts.STS_OFFLINE:
            # aby nie wyslac informacji podczas wlaczenia programu,
            # że jesteśmy offline
            self.status = ts.STS_OFFLINE
            self.odznaczWszystkieStatusy()
            self.ui.actionNiedostepny.setChecked( True )
            
            # blokujemy wysylanie pakietow
            self.send.network = False
            self.recv.network = False
            
            # zatrzymujemy pobieranie pakietów
            if self.recv.isRunning():
                self.recv.exit()
        self.zmienMojStatus()
    
    def initPreferencje( self ):
        u"""Wypełnienie aktualnymi opcjami okna preferecji."""
        self.prefDialog = QtGui.QDialog( self )
        self.prefDialog.ui = Ui_Dialog()
        self.prefDialog.ui.setupUi( self.prefDialog )
        self.prefDialog.connect( self.prefDialog.ui.pbOK, \
                                 QtCore.SIGNAL('clicked()'), \
                                 self.zmienPreferencje )
        self.prefDialog.connect( self.prefDialog.ui.pbAnuluj, \
                                 QtCore.SIGNAL('clicked()'), \
                                 self.prefDialog.close )
        self.prefDialog.connect( self.prefDialog.ui.pbKolorPrzychodzacej, \
                                 QtCore.SIGNAL('clicked()'), \
                                 self.slKolorWiadomosciPrzychodzacej )
        self.prefDialog.connect( self.prefDialog.ui.pbKolorWyslanej, \
                                 QtCore.SIGNAL('clicked()'), \
                                 self.slKolorWiadomosciWyslanej )
        self.prefDialog.connect( self.prefDialog.ui.pbKolorKomunikatu, \
                                 QtCore.SIGNAL('clicked()'), \
                                 self.slKolorKomunikatu )
        self.prefDialog.connect( self.prefDialog.ui.pbKatalogHistorii, \
                                 QtCore.SIGNAL('clicked()'), \
                                 self.slWybierzKatalog )
        self.prefDialog.connect( self.prefDialog.ui.pbDzwiekPrzychodzacej, \
                                 QtCore.SIGNAL('clicked()'), \
                                 self.slWybierzDzwiekPrzychodzacej )
        self.prefDialog.connect( self.prefDialog.ui.pbDzwiekDolaczenia, \
                                 QtCore.SIGNAL('clicked()'), \
                                 self.slWybierzDzwiekDolaczenia )
        self.prefDialog.connect( self.prefDialog.ui.chbZapiszRozmowe, \
                                 QtCore.SIGNAL('clicked()'), \
                                 self.slUkryjOpcjeHistorii )
        self.prefDialog.connect( self.prefDialog.ui.chbDzwiek, \
                                 QtCore.SIGNAL('clicked()'), \
                                 self.slUkryjOpcjeDzwieku )
    
    ########################### SLOTY ##########################
    
    def slWyslij( self ):
        u"""Funkcja dodaje do pola tekstowego tekst i wysyla w sieć."""
        
        if self.status == ts.STS_OFFLINE:
            self.dodajDoKonferencji( u'Masz ustawiony status niedostępny!', \
                                     tw.MSG_INFO )
            return
        
        if not self.send.network:
            self.dodajDoKonferencji( u'Sieć jest niedostępna!', tw.MSG_INFO )
            return
        
        if len(siec.Users) == 1:
            self.dodajDoKonferencji( u'Nie ma innych użytkowników do rozmowy!',\
                                      tw.MSG_INFO )
            return
        
        doc = self.ui.leWyslij.document()
        message = doc.toPlainText()
        
        if message != "":
            self.ui.leWyslij.clear()
            msg = '<b>:: ' + \
                    self.cfg.getNick() + " ::</b> " + \
                    time.strftime( '%d-%m-%Y %H:%M:%S' ) + '<br/>' + message
            self.dodajDoKonferencji( msg, tw.MSG_LOCAL )
            self.ui.leWyslij.setFocus();
            
            # wysylamy przez sieć
            self.send.send( {'msg':message, 'user':self.cfg.getNick(), \
                'host':self.cfg.nazwaHosta} )
    
    def slStatusDostepny( self ):
        u"""Zmiania status na dostępny."""
        self.status = ts.STS_AVAILABLE
        self.odznaczWszystkieStatusy()
        self.ui.actionDostepny.setChecked( True )
        
        # odblokowujemy wysylanie pakietow
        self.send.network = True
        self.recv.network = True
        
        # uruchomiamy odbieranie pakietów
        if not self.recv.isRunning():
            self.recv.start()
        
        self.startTimers()
        
        # wysylamy przez siec
        self.wyslijStatus()
    
    def slStatusZarazWracam( self ):
        u"""Zmiania status na zaraz wracam."""
        self.status = ts.STS_AWAY
        self.odznaczWszystkieStatusy()
        self.ui.actionZarazWracam.setChecked( True )
        
        # odblokowujemy wysylanie pakietow
        self.send.network = True
        self.recv.network = True
        
        # uruchomiamy odbieranie pakietów
        if not self.recv.isRunning():
            self.recv.start()
        
        self.startTimers()
        
        # wysylamy przez siec
        self.wyslijStatus()
    
    def slStatusZajety( self ):
        u"""Zmiania status na zajęty."""
        self.status = ts.STS_BUSY
        self.odznaczWszystkieStatusy()
        self.ui.actionZajety.setChecked( True )
        
        # odblokowujemy wysylanie pakietow
        self.send.network = True
        self.recv.network = True
        
        # uruchomiamy odbieranie pakietów
        if not self.recv.isRunning():
            self.recv.start()
        
        self.startTimers()
        
        # wysylamy przez siec
        self.wyslijStatus()
    
    def slStatusNiedostepny( self ):
        u"""Zmiania status na niedostępny."""
        self.status = ts.STS_OFFLINE
        self.odznaczWszystkieStatusy()
        self.ui.actionNiedostepny.setChecked( True )
        
        # wysylamy przez siec
        self.wyslijStatus()
        
        # uruchomiamy odbieranie pakietów
        if self.recv.isRunning():
            self.recv.exit()
        
        # blokujemy wysylanie pakietow
        self.send.network = False
        self.recv.network = False
        
        self.stopTimers()
        
        # usuwamy innych uzytkowników z listy
        listItem = QtGui.QListWidgetItem( QtGui.QIcon( \
                os.path.join('icons', self.status + '.png')), self.cfg.getNick() )
        self.ui.lvUzytkownicy.clear()
        self.ui.lvUzytkownicy.addItem( listItem )

    def slCzyscOnkoRozmowy( self ):
        u"""Slot czyści okno rozmowy"""
        self.ui.teKonwersacja.clear()
        
    def slZapiszRozmoweJakoTXT( self ):
        u"""Slot zapisujący rozmowę w formacie czystego tekstu."""
        nazwaPliku = unicode( QtGui.QFileDialog.getSaveFileName( self, \
            'Zapisz do TXT', self.cfg.getHomeDir(), 'Pliki tekstowe (*.txt)' ) )
        
        dane = self.ui.teKonwersacja.toPlainText()
        self.zapisz( nazwaPliku, dane )
    
    def slZapiszRozmoweJakoHTML( self ):
        u"""Slot zapisujący rozmowę w formacie HTML."""
        nazwaPliku = unicode( QtGui.QFileDialog.getSaveFileName( self, \
            'Zapisz do HTML', self.cfg.getHomeDir(), 'HTML (*.html, *.htm)' ) )
        
        dane = self.ui.teKonwersacja.toHtml()
        self.zapisz( nazwaPliku, dane )
    
    def slWybierzKatalog( self ):
        u"""Slot zmieniający katalog historii wskazany przez użytkownika."""
        dir = QtGui.QFileDialog.getExistingDirectory( self, \
            "Wybierz katalog", ".", QtGui.QFileDialog.ShowDirsOnly | \
            QtGui.QFileDialog.DontResolveSymlinks )
        
        if not dir.isEmpty():
            self.prefDialog.ui.leKatalogHistorii.setText( dir )
    
    def slWybierzDzwiekPrzychodzacej( self ):
        u"""Ustawia dźwięk wiadomości przychodzącej podany przez użytkownika."""
        wave = self.wybierzPlikDzwiekowy()
        
        if not wave.isEmpty():
            self.prefDialog.ui.leDzwiekPrzychodzacej.setText( wave )
    
    def slWybierzDzwiekDolaczenia( self ):
        u"""Ustawia dźwięk dołączenia nowej osoby."""
        wave = self.wybierzPlikDzwiekowy()
        
        if not wave.isEmpty():
            self.prefDialog.ui.leDzwiekDolaczenia.setText( wave )
    
    def slSkopiujTekst( self ):
        u"""Kopiuje zaznaczony tekst do schowka.""" 
        selection =  self.ui.teKonwersacja.createMimeDataFromSelection()
        clipboard = QtGui.QApplication.clipboard()
        clipboard.setText( selection.text() ) 
        
    def slUaktywnijOpcje( self ):
        u"""Uaktuwnia opcje kopiowania gdy zostanie zaznaczony tekst."""
        selection =  self.ui.teKonwersacja.createMimeDataFromSelection()
        
        if len( selection.text() ) > 0:
            self.ui.actionSkopiuj.setEnabled( True )
        else:
            self.ui.actionSkopiuj.setEnabled( False )
    
    def slPorownajDzien( self ):
        u"""Porównuje aktualny dzień, w którym był program uruchomiony
            z dniem bierzącym.
            Jeżeli dzień się zmienił to zamyka plik z bierzącym logiem
            i tworzy nowy plik i do niego zapisuje dalszą rozmowę.
        """
        if not self.cfg.getLogsSave():
            return
        
        if self.dzien != time.strftime( '%d' ):
            self.log.zamknij()
            self.log.setNazwaPliku( os.path.join(self.cfg.getLogsDir(), \
                time.strftime(self.cfg.getLogsFilename())) )
            self.log.otworz()
            self.dzien = time.strftime( '%d' )
    
    def slPreferencje( self ):
        u"""Wyświetla okno preferencji.""" 
        geo = self.geometry()
        self.prefDialog.move( geo.getRect()[ 0 ] + 50, geo.getRect()[ 1 ] )
        self.wypelnijOknoPreferencji()
        self.prefDialog.exec_()
        self.prefDialog.close()
    
    def slKolorKomunikatu( self ):
        u"""Zmienia kolor komunikatu."""
        tmpKolor = self.htmlToRgb( self.cfg.getColorMsgInfo() )
        kolor = self.pobierzKolor( tmpKolor )
        self.prefDialog.ui.frmKolorKomunikatu.setStyleSheet( \
                                    'QFrame { background-color:%s }' % kolor )
    
    def slKolorWiadomosciPrzychodzacej( self ):
        u"""Zmienia kolor wiadomości przychodzącej."""
        tmpKolor = self.htmlToRgb( self.cfg.getColorMsgNetwork() )
        kolor = self.pobierzKolor( tmpKolor )
        self.prefDialog.ui.frmKolorPrzychodzacej.setStyleSheet( \
                                    'QFrame { background-color:%s }' % kolor )
    
    def slKolorWiadomosciWyslanej( self ):
        u"""Zmienia kolor wiadomości wysłaniej."""
        tmpKolor = self.htmlToRgb( self.cfg.getColorMsgLocal() )
        kolor = self.pobierzKolor( tmpKolor )
        self.prefDialog.ui.frmKolorWyslanej.setStyleSheet( \
                                    'QFrame { background-color:%s }' % kolor )
    
    def slMenuKontekstoweRozmowy( self, pt ):
        u"""Wyświetla menu kontekstowe pola rozmowy"""
        menu = self.ui.teKonwersacja.createStandardContextMenu();
        menu.clear()
        menu.addAction( self.ui.actionSkopiuj )
        menu.addSeparator()
        menu.addAction( self.ui.actionWyczyscOknoRozmowy )
        menu.exec_( self.ui.teKonwersacja.mapToGlobal(pt) )
    
    def slMenuKontekstoweEdytora( self, pt ):
        u"""Wyświetla menu kontekstowe edytora wpisaywanie wiadomości."""
        menu = QtGui.QMenu( self )
        menu.addAction( win.windowUi._fromUtf8('Cofnij'), \
                        self.ui.leWyslij.undo, QtGui.QKeySequence("Ctrl+Z") )
        menu.addAction( win.windowUi._fromUtf8('Ponów'), \
                        self.ui.leWyslij.redo, QtGui.QKeySequence("Ctrl+Shift+Z") )
        menu.addSeparator()
        menu.addAction( win.windowUi._fromUtf8('Wytnij'), \
                        self.ui.leWyslij.cut, QtGui.QKeySequence("Ctrl+X") )
        menu.addAction( win.windowUi._fromUtf8('Skopiuj'), \
                        self.ui.leWyslij.copy, QtGui.QKeySequence("Ctrl+C") )
        menu.addAction( win.windowUi._fromUtf8('Wklej'), \
                        self.ui.leWyslij.paste, QtGui.QKeySequence("Ctrl+V") )
        menu.addSeparator()
        menu.addAction( win.windowUi._fromUtf8('Zaznacz wszystko'), \
                        self.ui.leWyslij.selectAll, QtGui.QKeySequence("Ctrl+A") )
        menu.exec_( self.ui.leWyslij.mapToGlobal(pt) )
    
    def slMenuKontekstoweTraya( self ):
        u"""Wyświetla menu kontekstowe ikonki w zasobniku systemowym."""
        self.komunikatWyjscia = True
        menu = QtGui.QMenu( self )
        menu.addAction( win.windowUi._fromUtf8('Wyjście'), self.close )
        menu.setTitle( win.windowUi._fromUtf8('Komunikator') )
        self.tray.setContextMenu( menu )
        
    def slUkryjOpcjeHistorii( self ):
        u"""Uaktywnia i dezaktywuje opcje historii w zależności czy włączona
        czy wyłączona jest historia rozmów."""
        checked = not self.prefDialog.ui.chbZapiszRozmowe.isChecked()
        self.prefDialog.ui.chbZapiszPowiadomienia.setDisabled( checked )
        self.prefDialog.ui.lbKatalogHistorii.setDisabled( checked )
        self.prefDialog.ui.leKatalogHistorii.setDisabled( checked )
        self.prefDialog.ui.pbKatalogHistorii.setDisabled( checked )
        self.prefDialog.ui.lbNazwaPliku.setDisabled( checked )
        self.prefDialog.ui.leNazwaPliku.setDisabled( checked )
        self.prefDialog.ui.gbZmienne.setDisabled( checked )
        
    def slUkryjOpcjeDzwieku( self ):
        u"""Uaktywnia i dezaktywuje opcje historii w zależności czy włączone
        czy wyłączone jest powiadomienie plikiem dźwiękowym."""
        checked = not self.prefDialog.ui.chbDzwiek.isChecked()
        self.prefDialog.ui.lbDzwiekPrzychodzacej.setDisabled( checked )
        self.prefDialog.ui.leDzwiekPrzychodzacej.setDisabled( checked )
        self.prefDialog.ui.pbDzwiekPrzychodzacej.setDisabled( checked )
        self.prefDialog.ui.lbDzwiekDolaczenia.setDisabled( checked )
        self.prefDialog.ui.leDzwiekDolaczenia.setDisabled( checked )
        self.prefDialog.ui.pbDzwiekDolaczenia.setDisabled( checked )
    
    ####################### ZDARZENIA ##########################
    
    def closeEvent( self, event ):
        u"""Zdarzenie zamknięcia okna aplikacji"""
        if self.komunikatWyjscia:
                # wysylamy przez siec
                self.send.send( {'hello':ts.STS_OFFLINE, 'user':self.cfg.getNick()} )
                self.cfg.saveConfig()
                
                if self.log != None:
                    self.log.zamknij()
                
                event.accept()
        else:
            self.hide()
            event.ignore()
            #self.komunikatWyjscia = False
    
    def resizeEvent( self, event ):
        QtGui.QWidget.resizeEvent( self, event )
        self.cfg.setWindowSize( event.size().width(), event.size().height() )
    
    def moveEvent( self, event ):
        QtGui.QWidget.moveEvent( self, event )
        self.cfg.setWindowPosition( event.pos().x(), event.pos().y() )
    
    def eventFilter( self, obj, ev ):
        if ev.type() == QtCore.QEvent.KeyPress:
            if not self.cfg.getEnterSend():
                return False
            
            if obj == self.ui.leWyslij:
                if ev.key() == QtCore.Qt.Key_Return or ev.key() == QtCore.Qt.Key_Enter:
                    if ev.modifiers() == QtCore.Qt.ShiftModifier:
                        self.ui.leWyslij.insertPlainText( '\n' )
                        return True
                    
                    self.slWyslij()
                    return True 
        
        return QtGui.QWidget.eventFilter(self, obj, ev)
# end class Main

def main():
    app = QtGui.QApplication( sys.argv )
    window = Main()
    window.show()
    sys.exit( app.exec_() )

if __name__ == "__main__":
    main()
