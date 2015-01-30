#!/usr/bin/python
# -*- coding: utf-8 -*-

import bint
import sys
import random

#rashirenniy algoritm evklida , tut ispol'zuetsya dlya vozvedeniya v -1 stepen' po modulu
def xgcd(a, b):
	
	if a == bint.bint(0): # -> esli a = 0 , gde 0 formata bol'shogo chisla
		return 0, 1, b

	if b == bint.bint(0): # esli b = 0 , gde 0 formata bol'shogo chisla
		return 1, 0, a

	#matritsa E
	px = bint.bint(0)
	ppx = bint.bint(1)
	py = bint.bint(1)
	ppy = bint.bint(0)

	while b > bint.bint(0):
		q = a / b
		a, b = b, a % b
		x = ppx - q * px
		y = ppy - q * py
		ppx, px = px, x
		ppy, py = py, y

	return ppx, ppy, a


def inverse(a, p): #vozvedenie v -1 stepen'
	x, y, g = xgcd(a, p)

	return (x % p + p) % p


def gen_keys():
	
	#schitivaem prostoe p

	f = open("p.txt") 

	p = int(f.read())

	f.close()
	#vibiraem primitivniy element g
	while True:
		g = random.randint(2, p - 1)

		if ((p - 1) % g) != 1:
			break
	# vibiraem sluchaynoe  x  1 < x < p-1
	x = random.randint(2, p - 1)

	p = bint.bint(str(p)) # privodim P k formatu bol'shogo chisla i vse ostal'noe tozhe

	g = bint.bint(str(g))

	x = bint.bint(str(x))

	y = p.powmod(g, x, p) # vichislyaem y = g^x mod p

	return p, g, y, x


def elgamal(msg, p, g, y, x):# shifr / deshifr v odnoy functsii

	msg = bint.bint(str(msg))  #sozdaem bol'shoe chislo ot parametra - stroki vhodnogo soobsheniya

	if msg > p: #esli dlinna ishodnogo soobsheniya bolshe modulya - oshibka
		raise ValueError("Неверная длина сообщения")

	pp = str(p) # bol'shoe chislo P privodim k formatu stroki

	pp = int(pp) # ego zhe privodim k tselochislennomu tipu

	k = random.randint(2, pp - 1) #vibiraem sluchainoe chislo k 1 < k < p-1

	k = bint.bint(str(k)) # privodim K k bol'shiomu chislu

	a = p.powmod(g, k, p)# a = g^k mod p                                               # Кодирование

	b = p.powmod(y, k, p)# b = y^k mod p                                               # Кодирование
	b = (msg * b) % p # b = y^k * M mod p, gde M ishodniy tekst

	print "\ncode: ("+str(a)+","+str(b)+")"

	decode_msg = p.powmod(a, x, p)  #a^x mod p                                    # Декодирование
	decode_msg = inverse(decode_msg, p) #(a^x)^-1 mod p
	decode_msg = (decode_msg * b) % p # b*(a^x)^-1 mod p chto sootvetstvuet decodirovannomu soobsheniu
	
	

	return decode_msg


def usage():
	print "\nИспользование: python ElGamal.py msg.txt\n"

	sys.exit(-1)


def main():
	if len(sys.argv) != 2:
		usage()
	try:
		f = open(sys.argv[1]) # otkrivaem vhodnoy file

		msg = int(f.read()) # chitaem ego
	
		print "\ntext: "+ str(msg) #vivodim na ekran

		f.close()

	except IOError:
		print 'no such file',sys.argv[1]
		sys.exit(-2)
	p, g, y, x = gen_keys() #generiruem kluchi
	
	decode_msg = elgamal(msg, p, g, y, x) #poluchaem decodirovannoe soobshenie


	print " \ndecode: " +str(decode_msg)	

main()
