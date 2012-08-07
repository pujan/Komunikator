#-*- coding: utf-8 -*-

u"""
Author: Łukasz 'Pujan' Pelc
Email: pujan8@o2.pl
Wyprodukowane w Polsce - 2011-2012

Moduł poleceń
Pierwszy parametr pobiera obiekt klasy Konfiguracja
drugi parametr jest rodzicem typu QWidget,
"""

from PyQt4 import QtGui
import sys
from com.konfiguracja import Konfiguracja

DEBUG = False

class Polecenia(object):
    def __init__( self, cfg, parent=None ):
        # główne okno programu
        if parent == sys.modules[QtGui.QWidget.__module__] or None:
            self.mainWindow = parent
        
        # klasa konfiguracja
        if cfg == sys.modules[Konfiguracja.__module__]:
            self.cfg = cfg
        
        # polecenia
        self.cmds = (
            'beep', # r'^/beep[\ \t]*(0|1){0,1}[\ \t]*$'
            'help', # r'^/help[\ \t]*(beep|log|nick|send|sound|status|theme|save|load){0,1}[\ \t]*$'
            'log',
            'nick', # r'^/nick[\ \t]*[a-zA-Z0-9ąćęłńóśźżĄĆĘŁÓŚŹŻ]+[\ \t]*$'
            'send', # r'^/send[\ \t]*(0|1){0,1}[\ \t]*$'
            'sound',
            'status', # r'^/status[\ \t]*(available|away|busy|offline){0,1}[\ \t]*(now){0,1}[\ \t]*$'
            'theme',
            'save',
            'load'
        )
    
    def exec_( self, command ):
        if command[ 0 ] == '/':
            for c in self.cmds:
                if command[ 1 : ] == c:
                    if DEBUG:
                        print u"Polecenie:", command # DEBUG
                    
                    return True
            else: # for
                if DEBUG:
                    print u"Nie ma polecenia:", command # DEBUG
        
        return False
    
# end class Polecenia
