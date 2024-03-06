#!usr/bin/python
# -*- coding:utf-8 -*-
"""small game of recognizing a word with syllables mixed up"""

import codecs, unicodedata, re
from itertools import islice
import random

def normalise_unicode(s,diac=True):
	"""normalise a string toward a standard unicode string, w/ or w/o diacritics

	normalise une chaine vers une unicode string standard, avec ou sans diacritiques

	:param arg1: string to normalise
	:type arg1: str or unicode
	:param arg2: True to keep diacritics, False to delete them. Default : keep them
	:type arg2: bool

	:example:
	>>> fun.normalise_unicode(u"\\xc3\\xa9ternel",True)
	u"\\xe9ternel"
	"""
	#note : if you look at the code of the example above, the double backslashes are escaped single backslashes. those are to be read as single backslashes

	

	if diac:
		nf=unicodedata.normalize('NFKC',s)
	else:
		nf=unicodedata.normalize('NFKD',s)
	nf=nf.replace(u'\u0153','oe')

	if False : #normaliser les whitespaces
		nf2=""
		for char in nf:
			if not re.match(u"\s",char,re.UNICODE) or char in ["\n"," "]:
				nf2+=char
		return u''.join(c for c in nf2 if not unicodedata.combining(c))

	if diac:
		return nf
	else:
		return u''.join(c for c in nf if not unicodedata.combining(c))
	

def lexique_parseur(fname,maxi=1000):
	"""takes lexicon files from lexique.org and convert them in a list of words, where each word is a list of syllabes
	maxi : maximum amount of words to extract"""
	with open(fname,mode="r",encoding="iso-8859-15") as f:
		lexique=set()
		for l in f:
			if l[0]=="<": #header of the file
				continue
			l=l.rstrip()
			l=l.split("\t")
			forme=l[0]
			lemme=l[1]
			if forme == lemme: #le mot n'est pas fléchi
				syllabes=l[-1]
				syllabes=normalise_unicode(syllabes,False)
				if syllabes.count("-")>2: #word is at least 3 syllabes long
					if syllabes.count("-")<6: #max 5 syllabes
						lexique.add(syllabes)

			if len(lexique)>maxi:
				break
	return lexique

def random_chunk(li, min_chunk=1, max_chunk=3):
	"""shuffles the letters of a word, ignoring the syllabes"""
	it = iter(li)
	while True:
		nxt= list(islice(it,random.randint(min_chunk,max_chunk)))
		if nxt:
			yield nxt
		else:
			break

def lier_lexiques(fnames,maxi=2000):
	"""warp around lexique_parseur() to put together several lexicon files
	maxi : maximum number of words to get"""
	maxi2=maxi/len(fnames)
	lextot=set()
	for fname in fnames:
		lexique=lexique_parseur(fname,maxi2)
		lextot.update(lexique)
	return lextot



def display(lexique,mode="syllabe",debug=False):
	"""run during the game itself
	mode : syllabe for normal use, the words are cut at the syllabes. random is to mix up letters randomly, but doesn't work very well"""
	if mode not in ["syllabe","random"]:
		raise TypeError("mode must be syllabe or random")
	
	print("Essayez de deviner le mot dont les syllabes ont été mélangées ")
	print("Tapez ? pour donner votre langue au chat")
	print("Tapez exit pour quitter le jeu")
	print("Les syllabes sont données sans leurs accents, mais vous pouvez mettre des accents dans votre réponse si vous voulez")

	while True:
		answer=random.sample(lexique,1)[0]
		if mode=="syllabe":
			answer=answer.split("-")
		elif mode=="random":
			#doesn't work well :(
			answer1=re.sub("-","",answer)
			answer1=list(random_chunk(answer1))
			answer=[]
			for part in answer1:
				part="".join(part)
				answer.append(part)

		mystery=list(answer)
		answer="".join(answer)
		random.shuffle(mystery)
		while "".join(mystery)==answer:
			random.shuffle(mystery)
		while True:
			print("\t".join(mystery))
			prop=input()
			prop=normalise_unicode(prop,False)
			
			if debug:
				print("answer",answer)
				print("prop",prop)

			if prop.startswith("?"):
				print("La réponse était",answer)
				break

			if prop.lower().startswith("exit"):
				exit()

			if prop == answer:
				print("Bravo !")
				print("Nouveau mot :")
				break
			else:
				print("Non, essayez encore")

if __name__=="__main__":
	#lexique=lexique_parseur("lexique.txt") #this takes all words no matter their part of speech
	#lexicons from lexique.org
	lexique=lier_lexiques(["lexique.nom.txt","lexique.adj.txt","lexique.ver.txt"]) #this takes an equal amount of names, adjectives and verbs
	display(lexique,"syllabe")





