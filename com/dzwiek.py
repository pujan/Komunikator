#-*- coding: utf-8 -*-

u"""
Author: Łukasz 'Pujan' Pelc
Email: pujan8@o2.pl
Wyprodukowane w Polsce - 2011-2012

Moduł odgrywający dźwięki.
Karta dźwiękowowa i podany dźwięk lub głośnik systemowy.
"""

import platform

class Dzwiek( object ):
    u"""Odgrywa dźwięk pliku wav lub piszczy głośnikiem systemowym.
    Domyślnie używa beepania."""
    def __init__( self, sound=False, dzwiek='' ):
        self.dzwiek = sound
        self.plik = dzwiek
        
    def setPlik( self, nazwaPliku ):
        self.plik = nazwaPliku
    
    def getPlik( self ):
        return self.plik
    
    def beep( self ):
        print chr(7),
    
    def graj( self ):
        if self.dzwiek and self.plik != '':
            if platform.system() == 'Windows':
                from winsound import PlaySound, SND_FILENAME, SND_ASYNC
                PlaySound(self.plik, SND_FILENAME|SND_ASYNC)
            elif platform.system() == 'Linux':
                from wave import open as waveOpen
                from ossaudiodev import open as ossOpen
                s = waveOpen(self.plik,'rb')
                (nc, sw, fr, nf, comptype, compname) = s.getparams()
                
                try:
                    dsp = ossOpen('/dev/dsp','w')
                    
                    try:
                        from ossaudiodev import AFMT_S16_NE
                    except ImportError:
                        if byteorder == "little":
                            AFMT_S16_NE = ossaudiodev.AFMT_S16_LE
                        else:
                            AFMT_S16_NE = ossaudiodev.AFMT_S16_BE
                    
                    dsp.setparameters(AFMT_S16_NE, nc, fr)
                    data = s.readframes(nf)
                    dsp.write(data)
                    s.close()
                    dsp.close()
                except IOError:
                    print "Błąd pisania do użądzenia /dev/dsp !"
                    print "Sprawdź czy masz możliwość zapisywania lub czy w Twoim systemie \
jest załadowany moduł snd-pcm-oss, jeżeli nie jest załaduj go jako root poleceniem"
                    print "\n\tmodprobe snd-pcm-oss"
    
# end class Dzwiek
