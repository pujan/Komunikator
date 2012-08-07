#-*- coding: utf-8 -*-

u"""
Author: Łukasz 'Pujan' Pelc
Email: pujan8@o2.pl
Wyprodukowane w Polsce - 2011-2012

Moduł zapisuje tekst na końcu pliku. Po wierszu.
"""
import codecs, sys

DEBUG = True

class Log( object ):
    def __init__( self, nazwa='', kodowanie='UTF-8' ):
        self.kodowanie = kodowanie
        #sys.setdefaultencoding = self.kodowanie
        self.nazwaPliku = nazwa.encode( sys.getdefaultencoding() )
        self.otworz( self.nazwaPliku )
    
    def setNazwaPliku( self, nazwa ):
        self.nazwaPliku = nazwa.encode( sys.getdefaultencoding() )
    
    def getNazwaPliku( self ):
        return self.nazwaPliku
    
    def setKodowanie( self, kodowanie ):
        self.kodowanie = kodowanie
    
    def getKodowanie( self ):
        return self.kodowanie
    
    def otworz( self, nazwa='' ):
        if nazwa != '':
            self.plik = codecs.open( nazwa, encoding = self.kodowanie, mode = 'a', errors='ignore' )
        elif self.nazwaPliku != '':
            self.plik = codecs.open( self.nazwaPliku, encoding = self.kodowanie, mode = 'a', errors='ignore' )
        else:
            self.plik = None
    
    def dopisz( self, linia ):
        if self.plik != None:
            self.plik.write( linia )
        else:
            if DEBUG:
                print "Log: Błąd we/wy!"
            
            raise IOError
    
    def zamknij( self ):
        self.plik.close()
    
# end class Log

def main():
    log = Log('test.txt')
    print log.getKodowanie()
    print log.getNazwaPliku()
    log.dopisz('\nłukasz pelc\n')
    log.dopisz('żółć\n')
    log.dopisz('źdźbło\n')
    log.zamknij()
    

if __name__ == "__main__":
    main()