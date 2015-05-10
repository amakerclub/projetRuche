#!/usr/bin/python
import sys
import Adafruit_DHT
from time import strftime

#Type de sonde DHT22 
sensor = 22

#Reference des ports GPIO pour les sondes DHT
#Sonde devant
gpiodhtdevant=18
#Sonde 1, 2 et 3
gpiodht1=23
gpiodht2=24
gpiodht3=25

#cles des sondes DS18B20 
#Sonde Exterieur
W1IDTEMPEXTR='28-04146dc1dfff'
#Sonde Devant
W1IDTEMPFRNT='28-04146dcfbbff'
#Sonde Dos
W1IDTEMPBACK='28-04146dcde9ff'
#Sonde droite
W1IDTEMPRGHT='28-04146dceb1ff'
#Sonde Gauche
W1IDTEMPLEFT='28-04146e15fdff'




#champs annee;mois;jour;heure;minute;seconde  (pour le CSV)
strd=strftime("%Y;%m;%d;%H;%M;%S")

#ecrit une ligne csv
def stat (label,value):
	print label+";"+str(value)+";"+strd


#recuperation de la valeur de d'une sonde DS18B20
#TODO: remplacer ca par une regexp :)
def getTemp(id):
    try:
        t=''
        filename='w1_slave'
        f = open ('/sys/bus/w1/devices/'+id+'/'+filename, 'r')
        line=f.readline()
        crc=line.rsplit(' ',1)
        crc=crc[1].replace('\n','')
        if crc=='YES':
            line=f.readline()
            t=line.rsplit('t=',1)
            t=t[1].replace('\n','')
        else:
            t=99999
        f.close()
        return int(t)
    except:
        return -1







# recuperation des valeurs des sondes
# NB: la valeur ecrite est en centieme d'unite. Ex: 21,3 Celcius => 2130

h, t = Adafruit_DHT.read_retry(22, gpiodhtdevant)
if h is not None and t is not None:
	stat ('ruche.temperature.milieu', '{0:0.0f}'.format(t*100))
	stat( 'ruche.humidite.milieu','{0:0.0f}'.format(h*100))

h, t = Adafruit_DHT.read_retry(22, gpiodht1)
if h is not None and t is not None:
        stat( 'ruche.temperature.hausse1', '{0:0.0f}'.format(t*100))
        stat( 'ruche.humidite.hausse1', '{0:0.0f}'.format(h*100))


h, t = Adafruit_DHT.read_retry(22, gpiodht2)
if h is not None and t is not None:
        stat ( 'ruche.temperature.hausse2', '{0:0.0f}'.format(t*100))
        stat ( 'ruche.humidite.hausse2', '{0:0.0f}'.format(h*100))


h, t = Adafruit_DHT.read_retry(22, gpiodht3)
if h is not None and t is not None:
        stat ('ruche.temperature.hausse3', '{0:0.0f}'.format(t*100))
        stat ('ruche.humidite.hausse3', '{0:0.0f}'.format(h*100))

#Now, let's care about 1w sensors

stat ('ruche.temperature.exterieur', '{0:0.0f}'.format(getTemp(W1IDTEMPEXTR)/10) )
stat ('ruche.temperature.devant'   , '{0:0.0f}'.format(getTemp(W1IDTEMPFRNT)/10) )
stat ('ruche.temperature.fond'     , '{0:0.0f}'.format(getTemp(W1IDTEMPBACK)/10) )
stat ('ruche.temperature.gauche'   , '{0:0.0f}'.format(getTemp(W1IDTEMPLEFT)/10) )
stat ('ruche.temperature.droite'   , '{0:0.0f}'.format(getTemp(W1IDTEMPRGHT)/10) )
