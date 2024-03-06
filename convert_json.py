#!/usr/bin/python
# -*- coding:utf-8 -*-
""" converts lexique.org files into a json that the app can read easier """

import json

def lexique_parseur(maxi=1000):
	"""takes lexicon files from lexique.org and convert them in a list of words, where each word is a list of syllabes
	maxi : maximum amount of words to extract"""

	lexique=set()
	for fname in ["lexique.nom.txt","lexique.adj.txt","lexique.ver.txt"]:

		with open(fname,mode="r",encoding="iso-8859-15") as f:
			for l in f:
				if l[0]=="<": #header of the file
					continue
				l=l.rstrip()
				l=l.split("\t")
				forme=l[0]
				lemme=l[1]
				if forme == lemme: #le mot n'est pas fléchi
					syllabes=l[-1]
					#syllabes=normalise_unicode(syllabes,False)
					if syllabes.count("-")>2: #word is at least 3 syllabes long
						if syllabes.count("-")<6: #max 5 syllabes
							lexique.add(syllabes)

				if len(lexique)>maxi:
					break
	lexique=list(lexique)
	
	with open("lexique.json",mode="w",encoding="utf-8") as f:
		f.write(json.dumps(lexique,indent=1))

lexique_parseur()
