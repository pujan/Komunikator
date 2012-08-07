#-*- coding: utf-8 -*-

u"""
Author: Łukasz 'Pujan' Pelc
Email: pujan8@o2.pl
Wyprodukowane w Polsce - 2011-2012

Moduł obsługujący plik konfiguracyjny

Domyślny plik config.ini:
[Window]
position-x = 392
position-y = 306
width = 496
height = 437

[General]
; dostępne statusy:
; available
; away
; busy
; offline
status = available
nick = %username%
enter-send = 1

[Sound]
sound = 0
file-join = sound/join.wav
file-msg = sound/msg.wav
beep = 1

[Logs]
save = 1
save-info = 1
filename = %d-%m-%Y.log
directory = logs

[Colors]
msg-local = #0000ff
msg-info = #ff0000
msg-network = #000000
"""

from ConfigParser import ConfigParser
import ConfigParser as cp
import os, re

# Domyślne kolory komunikatów
COLOR_INFO = '#ff0000'
COLOR_NETWORK = '#000000'
COLOR_LOCAL = '#0000ff'

class Konfiguracja( object ):
    u"""Klaca przechowująca konfigurację programu Komunikator"""
    def __init__( self ):
        self.parser = ConfigParser()
        self.nazwaPliku = 'config.ini'
        
        # pobranie zmiennych środowiskowych:
        #
        # pobranie nazwy użytkownika
        try:
            self.nazwaUzytkownika = os.environ[ 'USER' ]
        except KeyError:
            # pobieranie zmiennych windows
            try:
                self.nazwaUzytkownika = os.environ[ 'USERNAME' ]
            except KeyError:
                import random
                self.nazwaUzytkownika = 'user_' + str( random.randint(1, 100) )
        
        # pobieranie katalogu domowego
        try:
            self.katalogDomowy = os.environ[ 'HOME' ]
        except KeyError:
            try:
                self.katalogDomowy = os.environ[ 'HOMEPATH' ]
            except KeyError:
                self.katalogDomowy = None
        
        # pobieranie nazwy hosta
        try:
            self.nazwaHosta = os.environ[ 'HOSTNAME' ]
        except KeyError:
            try:
                self.nazwaHosta = os.environ[ 'COMPUTERNAME' ]
            except KeyError:
                self.nazwaHosta = 'host'
        
        self.loadConfig()
        
        # wyrazenie regularne dla kolorow
        self.colorRegex = re.compile( '#[a-fA-f0-9]{6}' )
    
    def defaultConfig( self ):
        u"""defaultConfig()
            Tworzy domyślną konfigurację."""
        self.parser.add_section( 'Window' )
        self.parser.set( 'Window', 'position-x', '392' )
        self.parser.set( 'Window', 'position-y', '306' )
        self.parser.set( 'Window', 'width', '496' )
        self.parser.set( 'Window', 'height', '437' )
        self.parser.add_section( 'General' )
        self.parser.set( 'General', 'status', 'available' )
        self.parser.set( 'General', 'nick', self.nazwaUzytkownika )
        self.parser.set( 'General', 'enter-send', '1' )
        self.parser.add_section( 'Sound' )
        self.parser.set( 'Sound', 'sound', '0' )
        self.parser.set( 'Sound', 'file-join', os.path.join('sound', 'join.wav') )
        self.parser.set( 'Sound', 'file-msg', os.path.join('sound', 'msg.wav') )
        self.parser.set( 'Sound', 'beep', '1' )
        self.parser.add_section( 'Logs' )
        self.parser.set( 'Logs', 'save', '1' )
        self.parser.set( 'Logs', 'save-info', '1' )
        self.parser.set( 'Logs', 'filename', '%d-%m-%Y.log' )
        self.parser.set( 'Logs', 'directory', 'logs' )
        self.parser.add_section( 'Colors' )
        self.parser.set( 'Colors', 'msg-local', '#0000ff' )
        self.parser.set( 'Colors', 'msg-info', '#ff0000' )
        self.parser.set( 'Colors', 'msg-network', '#000000' )
        
        #self.saveConfig()
    
    # funkcje odczytujace konfiguracje
    
    def getWindowPosition( self ):
        u"""getWindowPosition() -> (int,int)
            Zwraca współrzędne okna na ekranie monitora."""
        try:
            result = ( self.parser.getint('Window', 'position-x'), self.parser.getint('Window', 'position-y') )
        except cp.NoSectionError:
            self.parser.add_section( 'Window' )
            self.parser.set( 'Window', 'position-x', '392' )
            self.parser.set( 'Window', 'position-y', '306' )
            result = ( self.parser.getint('Window', 'position-x'), self.parser.getint('Window', 'position-y') )
        except cp.NoOptionError:
            self.parser.set( 'Window', 'position-x', '392' )
            self.parser.set( 'Window', 'position-y', '306' )
            result = ( self.parser.getint('Window', 'position-x'), self.parser.getint('Window', 'position-y') )
        
        return result
    
    def getWindowSize( self ):
        u"""getWindowSize() -> (int,int)
            Zwraca wielkość okna w pikselach."""
        try:
            result = ( self.parser.getint('Window', 'width'), self.parser.getint('Window', 'height') )
        except cp.NoSectionError:
            self.parser.add_section( 'Window' )
            self.parser.set( 'Window', 'width', '496' )
            self.parser.set( 'Window', 'height', '437' )
            result = ( self.parser.getint('Window', 'width'), self.parser.getint('Window', 'height') )
        except cp.NoOptionError:
            self.parser.set( 'Window', 'width', '496' )
            self.parser.set( 'Window', 'height', '437' )
            result = ( self.parser.getint('Window', 'width'), self.parser.getint('Window', 'height') )
        
        return result
    
    def getStatus( self ):
        u"""getStatus() -> str
            Zwraca status w postaci tekstowej."""
        try:
            result = self.parser.get( 'General', 'status' )
        except cp.NoSectionError:
            self.parser.add_section( 'General' )
            self.parser.set( 'General', 'status', 'available' )
            result = self.parser.get( 'General', 'status' )
        except cp.NoOptionError:
            self.parser.set( 'General', 'status', 'available' )
            result = self.parser.get( 'General', 'status' )
        
        return result
    
    def getNick( self ):
        u"""getNick() -> str
            Zwraca nick."""
        try:
            result = self.parser.get( 'General', 'nick' )
        except cp.NoSectionError:
            self.parser.add_section( 'General' )
            self.parser.set( 'General', 'nick', self.nazwaUzytkownika )
            result = self.parser.get( 'General', 'nick' )
        except cp.NoOptionError:
            self.parser.set( 'General', 'nick', self.nazwaUzytkownika )
            result = self.parser.get( 'General', 'nick' )
        
        return result
    
    def getEnterSend( self ):
        u"""getEnterSend() -> Boolean
            Zwraca czy została włączona opcja wysyłania za pomocą
            klawisza ENTER."""
        try:
            result = self.parser.getboolean( 'General', 'enter-send' )
        except cp.NoSectionError:
            self.parser.add_section( 'General' )
            self.parser.set( 'General', 'enter-send', '1' )
            result = self.parser.getboolean( 'General', 'enter-send' )
        except cp.NoOptionError:
            self.parser.set( 'General', 'enter-send', '1' )
            result = self.parser.getboolean( 'General', 'enter-send' )
        
        return result
    
    def getHost( self ):
        u"""getHost() -> str
            Zwraca nazwę hosta."""
        return self.nazwaHosta
    
    def getHomeDir( self ):
        u"""getHomeDir() -> str
            Zwraca ścieżkę do katalogu fdomowego użytkownika."""
        return self.katalogDomowy
    
    def getSoundOn( self ):
        try:
            result = self.parser.getboolean( 'Sound', 'sound' )
        except cp.NoSectionError:
            self.parser.add_section( 'Sound' )
            self.parser.set( 'Sound', 'sound', '0' )
            result = self.parser.getboolean( 'Sound', 'sound' )
        except cp.NoOptionError:
            self.parser.set( 'Sound', 'sound', '0' )
            result = self.parser.getboolean( 'Sound', 'sound' )
        
        return result
    
    def getSoundJoin( self ):
        u"""getSoundJoin() -> str
            Zwraca nazwę kliku dźwiękowego wraz ze ścieżką, jeżeli jest
            zapisana, do pliku dźwiękowe odpowiedzialnego za zdarzenie
            przyłączenia się nowego użytkownika."""
        try:
            result = self.parser.get( 'Sound', 'file-join' )
        except cp.NoSectionError:
            self.parser.add_section( 'Sound' )
            self.parser.set( 'Sound', 'file-join', os.path.join('sound', 'join.wav') )
            result = self.parser.get( 'Sound', 'file-join' )
        except cp.NoOptionError:
            self.parser.set( 'Sound', 'file-join', os.path.join('sound', 'join.wav') )
            result = self.parser.get( 'Sound', 'file-join' )
        
        return result
    
    def getSoundMsg( self ):
        u"""getSoundMsg() -> str
            Zwraca nazwę kliku dźwiękowego wraz ze ścieżką, jeżeli jest
            zapisana, do pliku dźwiękowe odpowiedzialnego za zdarzenie
            przyjścia nowej wiadomości."""
        try:
            result = self.parser.get( 'Sound', 'file-msg' )
        except cp.NoSectionError:
            self.parser.add_section( 'Sound' )
            self.parser.set( 'Sound', 'file-msg', os.path.join('sound', 'msg.wav') )
            result = self.parser.get( 'Sound', 'file-msg' )
        except cp.NoOptionError:
            self.parser.set( 'Sound', 'file-msg', os.path.join('sound', 'msg.wav') )
            result = self.parser.get( 'Sound', 'file-msg' )
        
        return result
    
    def getBeepOn( self ):
        u"""getBeepOn() -> Boolean
            Zwraca czy opcja powiadamiania głośnikiem systemowym
            jest włączona (True) lub nie (False)."""
        try:
            result = self.parser.getboolean( 'Sound', 'beep' )
        except cp.NoSectionError:
            self.parser.add_section( 'Sound' )
            self.parser.set( 'Sound', 'beep', '1' )
            result = self.parser.getboolean( 'Sound', 'beep' )
        except cp.NoOptionError:
            self.parser.set( 'Sound', 'beep', '1' )
            result = self.parser.getboolean( 'Sound', 'beep' )
        
        return result
    
    def getLogsSave( self ):
        u"""getLogsSave() -> Boolean
            Zwraca wartość True gdy opcja zapisu logów jest włączona
            lun False gdy opcja nie jest włączona."""
        try:
            result = self.parser.getboolean( 'Logs', 'save' )
        except cp.NoSectionError:
            self.parser.add_section( 'Logs' )
            self.parser.set( 'Logs', 'save', '1' )
            result = self.parser.getboolean( 'Logs', 'save' )
        except cp.NoOptionError:
            self.parser.set( 'Logs', 'save', '1' )
            result = self.parser.getboolean( 'Logs', 'save' )
        
        return result
    
    def getLogsSaveInfo( self ):
        u"""getLogsSaveInfo() -> Boolean
            Zwraca True jeżeli opcja zapisu do logów informacji programu
            w przeciwnym wypadku False."""
        try:
            result = self.parser.getboolean( 'Logs', 'save-info' )
        except cp.NoSectionError:
            self.parser.add_section( 'Logs' )
            self.parser.set( 'Logs', 'save-info', '1' )
            result = self.parser.getboolean( 'Logs', 'save-info' )
        except cp.NoOptionError:
            self.parser.set( 'Logs', 'save-info', '1' )
            result = self.parser.getboolean( 'Logs', 'save-info' )
        
        return result
    
    def getLogsFilename( self ):
        u"""getLogsFilename() -> str
            Zwraca format nazwy pliku."""
        try:
            result = self.parser.get( 'Logs', 'filename' )
        except cp.NoSectionError:
            self.parser.add_section( 'Logs' )
            self.parser.set( 'Logs', 'filename', '%d-%m-%Y.log' )
            result = self.parser.get( 'Logs', 'filename' )
        except cp.NoOptionError:
            self.parser.set( 'Logs', 'filename', '%d-%m-%Y.log' )
            result = self.parser.get( 'Logs', 'filename' )
        
        return result
    
    def getLogsDir( self ):
        try:
            result = self.parser.get( 'Logs', 'directory' )
        except cp.NoSectionError:
            self.parser.add_section( 'Logs' )
            self.parser.set( 'Logs', 'directory', 'logs' )
            result = self.parser.get( 'Logs', 'directory' )
        except cp.NoOptionError:
            self.parser.set( 'Logs', 'directory', 'logs' )
            result = self.parser.get( 'Logs', 'directory' )
        
        return result
    
    def getColorMsgLocal( self ):
        try:
            color = self.parser.get( 'Colors', 'msg-local' )
        except cp.NoSectionError:
            self.parser.add_section( 'Colors' )
            self.parser.set( 'Colors', 'msg-local', '#0000ff' )
            color = self.parser.get( 'Colors', 'msg-local' )
        except cp.NoOptionError:
            self.parser.set( 'Colors', 'msg-local', '#0000ff' )
            color = self.parser.get( 'Colors', 'msg-local' )
        
        if self.colorRegex.search( color ):
            return color
        else:
            return COLOR_LOCAL
    
    def getColorMsgNetwork( self ):
        try:
            color = self.parser.get( 'Colors', 'msg-network' )
        except cp.NoSectionError:
            self.parser.add_section( 'Colors' )
            self.parser.set( 'Colors', 'msg-network', '#000000' )
            color = self.parser.get( 'Colors', 'msg-network' )
        except cp.NoOptionError:
            self.parser.set( 'Colors', 'msg-network', '#000000' )
            color = self.parser.get( 'Colors', 'msg-network' )
        
        if self.colorRegex.search( color ):
            return color
        else:
            return COLOR_NETWORK
    
    def getColorMsgInfo( self ):
        try:
            color = self.parser.get( 'Colors', 'msg-info' )
        except cp.NoSectionError:
            self.parser.add_section( 'Colors' )
            self.parser.set( 'Colors', 'msg-info', '#ff0000' )
            color = self.parser.get( 'Colors', 'msg-info' )
        except cp.NoOptionError:
            self.parser.set( 'Colors', 'msg-info', '#ff0000' )
            color = self.parser.get( 'Colors', 'msg-info' )
        
        if self.colorRegex.search( color ):
            return color
        else:
            return COLOR_INFO
    
    # funkcje zmieniajace konfiguracje
    
    def setWindowPosition( self, x, y ):
        self.parser.set( 'Window', 'position-x', str(x) )
        self.parser.set( 'Window', 'position-y', str(y) )
    
    def setWindowSize( self, w, h ):
        self.parser.set( 'Window', 'width', str(w) )
        self.parser.set( 'Window', 'height', str(h) )
    
    def setStatus( self, status ):
        if status == 'available' or status == 'away' or \
        status == 'busy' or status == 'offline':
            self.parser.set( 'General', 'status', status )
            return True
        
        return False
    
    def setNick( self, nick ):
        self.parser.set( 'General', 'nick', nick )
    
    def setEnterSend( self, enter ):
        if enter or enter == '1':
            self.parser.set( 'General', 'enter-send', '1' )
            return True
        elif not enter or enter == '0':
            self.parser.set( 'General', 'enter-send', '0' )
            return True
        
        return False
    
    def setSoundOn( self, snd ):
        if snd or snd == '1':
            self.parser.set( 'Sound', 'sound', '1' )
            return True
        elif not snd or snd == '0':
            self.parser.set( 'Sound', 'sound', '0' )
            return True
        
        return False
    
    def setSoundJoin( self, joinwave ):
        self.parser.set( 'Sound', 'file-join', joinwave )
    
    def setSoundMsg( self, msgwave ):
        self.parser.set( 'Sound', 'file-msg', msgwave )
    
    def setBeepOn( self, beep ):
        if beep or beep == '1':
            self.parser.set( 'Sound', 'beep', '1' )
            return True
        elif not beep or beep == '0':
            self.parser.set( 'Sound', 'beep', '0' )
            return True
        
        return False
    
    def setLogsSave( self, save ):
        if save or save == '1':
            self.parser.set( 'Logs', 'save', '1' )
            return True
        elif not save or save == '0':
            self.parser.set( 'Logs', 'save', '0' )
            return True
        
        return False
    
    def setLogsSaveInfo( self, save ):
        if save or save == '1':
            self.parser.set( 'Logs', 'save-info', '1' )
            return True
        elif not save or save == '0':
            self.parser.set( 'Logs', 'save-info', '0' )
            return True
        
        return False
    
    def setLogsFilename( self, filename ):
        self.parser.set( 'Logs', 'filename', filename )
    
    def setLogsDir( self, logdir ):
        self.parser.set( 'Logs', 'directory', logdir )
    
    def setColorMsgLocal( self, msgcolor ):
        if self.colorRegex.search( msgcolor ):
            self.parser.set( 'Colors', 'msg-local', msgcolor )
        else:
            self.parser.set( 'Colors', 'msg-local', COLOR_LOCAL )
    
    def setColorMsgNetwork( self, msgcolor ):
        if self.colorRegex.search( msgcolor ):
            self.parser.set( 'Colors', 'msg-network', msgcolor )
        else:
            self.parser.set( 'Colors', 'msg-network', COLOR_NETWORK )
    
    def setColorMsgInfo( self, msgcolor ):
        if self.colorRegex.search( msgcolor ):
            self.parser.set( 'Colors', 'msg-info', msgcolor )
        else:
            self.parser.set( 'Colors', 'msg-info', COLOR_INFO )
    
    def saveConfig( self ):
        try:
            fp = open( self.nazwaPliku, 'w' )
            self.parser.write( fp )
            fp.close()
        except:
            print "Bład zapisu pliku konfigurayjnego!"
            print "Sprawdź czy masz możliwość zapisu do katalogu '" + os.getcwd() + "'!"
    
    def loadConfig( self ):
        try:
            if self.parser.read( self.nazwaPliku ) == []:
                print u"Nie ma pliku", self.nazwaPliku
                print u"Tworze nowy..."
                self.defaultConfig()
                self.saveConfig()
            else:
                self.nazwaUzytkownika = self.getNick()
        except:
            os.unlink( self.nazwaPliku )
            #self.domyslnaKonfiguracja()
    
# end class Konfiguracja
        