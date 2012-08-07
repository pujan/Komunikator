#-*- coding: utf-8 -*-

u"""
Author: Łukasz 'Pujan' Pelc
Email: pujan8@o2.pl
Wyprodukowane w Polsce - 2011-2012

Moduł sieciowy."""

from PyQt4 import QtCore
import socket, pickle, time

# słowniki pośredniczący pomiędzy klasami
message = None    # wiadomość wysyłana przez sieć z nazwą użytkownika i hosta
Users = {}        # informacja o użytkownikach
PORT = 12080
BROADCAST_ADDR = "255.255.255.255"
RECEIVED_ADDR = ""
SIZE_BUFF = 1024

DEBUG = True

class Odbieranie( QtCore.QThread ):
    u"""Odbiera z sieci pakiety udp"""
    def __init__( self, parent=None ):
        self.outaddr = (RECEIVED_ADDR, PORT)
        
        self.rcvsock = socket.socket( socket.AF_INET, socket.SOCK_DGRAM, 0 )
        self.rcvsock.setsockopt( socket.SOL_SOCKET, socket.SO_BROADCAST, 1 )
        self.rcvsock.setsockopt( socket.SOL_SOCKET, socket.SO_RCVBUF, SIZE_BUFF )
        
        self.network = True
        
        # łączymy adres z gniazdem
        self.rcvsock.bind( self.outaddr )
        QtCore.QThread.__init__( self, parent )
        
    def run( self ):
        global message
        global Users
        
        while self.network:
            # odbieramy pakiet
            msg, address = self.rcvsock.recvfrom( SIZE_BUFF )
            message = pickle.loads( msg )
            ip = address[ 0 ]
            
            if DEBUG:
                print 'Odbieranie.run():', message
                print u"Odbieranie.run(): lista użytkowników:", Users
            
            try:
                if message.has_key( 'hello' ):
                    if message[ 'hello' ] != '' and message[ 'user' ] != '':
                        if message[ 'hello' ] == 'offline':
                            try:
                                # uzytkownik offline mozemy usunac
                                del( Users[ ip ] )
                                continue
                            except KeyError:
                                pass
                        else:
                            # sprawdzamy czy użytkownik jest na liście
                            if Users.has_key( ip ):
                                # jeżeli jest uaktualniemyczas
                                Users[ ip ][ 'czas' ] = int( time.time() ) + 60
                                
                                # być może zmienił status
                                Users[ ip ][ 'status' ] = message[ 'hello' ]
                            else:
                                # jeżeli nie ma dodajemy do listy
                                Users[ ip ] = {'user':message[ 'user' ],
                                                     'status':message[ 'hello' ],
                                                     'czas':int( time.time() ) + 60} # dajemy mu 1 min :)
                        
                        
                        # jeżli użytkownicy nie wysłali pakietu przez 300s
                        # to go usuwamy, bo prawdopodobnie są offline
                        tmp = Users.copy() # kopia listy dla pętli for
                        
                        for key,value in tmp.iteritems():
                            if ( value[ 'czas' ] - int( time.time() ) ) <= 0:
                                # nie wysłał pakietu przez 5 min.
                                if DEBUG:
                                    print "Odbieranie.run(): kasujemy delikwenta",Users[ key ]
                                # kasujemy z listy
                                del( Users[ key ] )
                        
                else:       
                    message[ 'ip' ] = ip
            except AttributeError:
                pass
            #except TypeError:
            #    print "Odbieranie.run(): TypeError!", type(Users[ip]['czas'])
# end class Odbieranie

class Wysylanie( object ):
    u"""Pobiera dane i wysyła je przez sieć."""
    def __init__( self, dane=None ):
        self.init()
        self.dane = dane # dane do wysłania
        self.network = True # czy jest połączenie z siecią
    
    def init( self ):
        self.sndsock = socket.socket( socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP )
        self.sndsock.setsockopt( socket.SOL_SOCKET, socket.SO_BROADCAST, 1 )
        self.sndsock.setsockopt( socket.SOL_SOCKET, socket.SO_SNDBUF, SIZE_BUFF )
        
        self.toaddr = (BROADCAST_ADDR, PORT)
    
    def send( self, dane=None ):
        u"""Wysyła nane w zmiennej globalnej, jeśli nie podano w parametrze, jeżeli
        parametr dane jest podany, to wysyła te dane
        """
        
        if dane != None:
            pakiet = pickle.dumps( dane )
        elif self.dane != None:
            pakiet = pickle.dumps( self.dane )
        else:
            # chyba nie ma danych do wysłania
            return
        
        try:
            if not self.network:
                self.init()
                self.network = True
            
            self.sndsock.sendto( pakiet, self.toaddr )
        except:
            #self.network = False
            self.network = False
            
            if DEBUG:
                print u"Wysylanie.send(): wystąpił wyjątek - self.network = False"
            #send = False
            #print u"Send: False" # DEBUG
    
    def setData( self, dane ):
        u"""Zmienia dane do wysłania."""
        self.dane = dane
    
# end class Wysylanie
