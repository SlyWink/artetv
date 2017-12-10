#!/usr/bin/python3
# coding: utf8

import argparse
import requests
import sys

URL = 'https://www.arte.tv/papi/tvguide/videos/ARTE_PLUS_SEVEN/F.json?includeLongRights=true'
QUALITE = [ 'LQ','MQ','EQ','SQ' ]

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument('-o', action='store_true', help='Version originale')
parser.add_argument('-q', type=int, nargs='?', choices=range(0,4), default=1, help='Qualité (0=basse à 3=haute)')
parser.add_argument('keyword', nargs='?')

opt = parser.parse_args()

if opt.keyword is None:
  parser.print_help()

else:
  langue = 3 if opt.o else 1
  js = requests.get(URL).json()

  liste = [] 
  for emission in js['paginatedCollectionWrapper']['collection']:
    if emission['VTI'].lower().find(opt.keyword.lower()) != -1:
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
      nomfich = js2['VST']['VNA'] + '_ARTE'
      nomfich += '_VO.mp4' if opt.o else '.mp4'
      url = js2['VSR']['HTTP_MP4_{0}_{1}'.format(QUALITE[opt.q],langue)]['url']
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
