#!/usr/bin/python3
# coding: utf8

import requests
import sys
import os

URL1 = 'https://www.arte.tv/papi/tvguide/videos/ARTE_PLUS_SEVEN/F.json?includeLongRights=true'

if len(sys.argv) != 2:
  print('Syntaxe : {0} <émission à rechercher>'.format(os.path.basename(sys.argv[0])))

else:

  js = requests.get(URL1).json()

  liste = [] 
  for emission in js['paginatedCollectionWrapper']['collection']:
    if emission['VTI'].lower().find(sys.argv[1].lower()) != -1:
      liste.append(emission)

  for cpt in range(len(liste)):
    em = liste[cpt]
    print(u'{0}) [{1}] : {2}'.format(cpt+1,em['VDA'][:19],em['VTI']))
  print("0) QUITTER")

  while True:
    indice = int(input("Choix => "))
    if indice == 0:
      break
    if indice <= len(liste):
      js = requests.get(liste[indice-1]['videoPlayerUrl']).json()
      js2 = js['videoJsonPlayer']
      nomfich = js2['VST']['VNA'] + '_ARTE.mp4'
      url = js2['VSR']['HTTP_MP4_EQ_1']['url']
      r = requests.get(url, stream=True)
      with open(nomfich, 'wb') as fd:
        print('> {0} '.format(nomfich),end='')
        sys.stdout.flush()
        for chunk in r.iter_content(chunk_size=1024*1024*2):
          if chunk:
            print('.',end='')
            sys.stdout.flush()
            fd.write(chunk)
        print(' OK')
