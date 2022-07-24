#!/usr/bin/env python3
import sys
import os
import multiprocessing
import subprocess
import time
import datetime
from colorama import init, Fore, Back, Style
# ip address asic
ip_ant = ["192.168.31.189", "192.168.31.150", "192.168.31.207", "192.168.31.51",
			"192.168.31.99", "192.168.31.126", "192.168.31.173",
			"192.168.31.199", "192.168.31.101", "192.168.31.231", "192.168.31.233",
			"192.168.31.54", "192.168.31.43", "192.168.31.6", "192.168.31.127"]
# , "192.168.31.43"

DNULL = open(os.devnull, 'w')
init(autoreset=True)

# play sound if ip not ping
def ip_err():
	os.system('paplay sounds/appear.ogg')

# play sound if not connect os
def device_err():
	os.system('paplay sounds/gobble.ogg')

# test ping device
def ping(host,mp_queue):
	response = subprocess.call(["ping", "-c", "2", "-w", '2', host], stdout=DNULL)
	if response == 0:
		#print(host, 'is up!')
		result = True
	else:
		print('\n')
		print(Fore.RED + host, 'is down!')
		ip_err()
		result = False
	mp_queue.put((result,host))

def worker(ip):
	mp_queue = multiprocessing.Queue()
	processes = []
	device = ip
	p = multiprocessing.Process(target=ping, args=(device, mp_queue))
	processes.append(p)
	p.start()
	key, value =  mp_queue.get()
	results = key
	return results, value

# get status asic
def getstat(status, nant):

	st = status.split(",")
	if st > []:
		for a in st:
			para = a.split("=")
			st_cod = para[0].strip()
			st_value = para[1].strip()
			slovo[st_cod] = st_value
		
		print(nant, " ", ip, "------------", slovo["Type"])
		model_asic = slovo["Type"]
			
		start_GHS5s = slovo["GHS 5s"]
		ghs5s = float(start_GHS5s)
		# if hash < 450
		if ghs5s < 450:
			print(Back.RED + "!!!XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX!!! ", ghs5s, end='  ')
			device_err()
		else:
			print("GHS5s: ", Back.GREEN + start_GHS5s, end='  ')
		
		start_GHSav = slovo["GHS av"]
		print("    GHSav: ", Back.GREEN + start_GHSav)
		
		start_fan1 =  slovo["fan1"]
		fan1 = int(start_fan1)
		# Check Fan speed
		if fan1 > 3000 and fan1 < 3500:
			print(Fore.YELLOW + "		FAN1: ", fan1, end='  ')
		elif fan1 > 3500:
			print(Fore.RED + "		FAN1: ", fan1, end='  ')
		elif fan1 < 800:
			device_err()
		else:
			print(Fore.CYAN + "		FAN1:  ", fan1, end='  ')
		
		start_fan2 =  slovo["fan2"]
		fan2 = int(start_fan2)
		if fan2 > 3000 and fan2 < 3500:
			print(Fore.YELLOW + "		FAN2: ", fan2, end='  ')
		elif fan2 > 3499:
			print(Fore.RED + "		FAN2: ", fan2, end='  ')
		elif fan2 < 800:
			device_err()
		else:
			print(Fore.CYAN + "		FAN2:  ", fan2, end='  ')
		
		if model_asic.find("T17") != -1:
			start_fan3 =  slovo["fan3"]
			fan3 = int(start_fan3)
			if fan3 > 3000 and fan2 < 3500:
				print(Fore.YELLOW + "		FAN3: ", fan3, end='  ')
			elif fan3 > 3499:
				print(Fore.RED + "		FAN3: ", fan3, end='  ')
			elif fan3 < 800:
				device_err()
			else:
				print(Fore.CYAN + "		FAN3:  ", fan3, end='  ')
		if model_asic.find("T17") != -1:
			start_fan4 =  slovo["fan4"]
			fan4 = int(start_fan4)
			if fan4 > 3000 and fan4 < 3500:
				print(Fore.YELLOW + "		FAN2: ", fan4, end='  ')
			elif fan4 > 3499:
				print(Fore.RED + "		FAN4: ", fan4, end='  ')
			elif fan4 < 800:
				device_err()
			else:
				print(Fore.CYAN + "		FAN4:  ", fan4)
		
		
		fan1 = 0
		fan2 = 0
		fan3 = 0
		fan4 = 0
		return nant

slovo = {}
#def stat_ant():


while True:	
	nant = 1
	ant = iter(ip_ant)
	
	for ip in ant:
		results, value = worker(ip)
		if results == True:
		
			cmd = "echo -n 'stats' | nc " + ip + " 4028"
			stat_asic = subprocess.run(cmd, 
				shell=True,
				stdout = subprocess.PIPE,
				stderr=subprocess.PIPE,
				universal_newlines = True)
				
			print(stat_asic.stderr)
			
			getstat(stat_asic.stdout, nant)
			nant = nant + 1

	print('\033[39m')	
	print(Fore.GREEN + '{0:%d-%m-%Y %H:%M:%S}'.format(datetime.datetime.now()), "\n")

	#time.sleep(3)
	time.sleep(300)
