from threading import Thread
import portscanner
import random
import time
import sys
import os 

def clean_address_list(address_list, verbose):
	addr = []
	for line in open(address_list, 'rb').readlines():
		ln = line.replace('\n', '')
		if len(ln.split(':'))>1:
			ip = ln.split(':')[0]
			addr.append(ip)
		else:
			ip = ln.split(' ')[-1]
			addr.append(ip)
	clean_list = list(set(addr))
	if verbose:
		print('[*] %d Unique IP Addresses Loaded' % len(clean_list))
	return clean_list

def setup_folders():
	if not os.path.isdir(os.getcwd()+'/ScanData'):
		os.mkdir(os.getcwd()+'/ScanData')

def parse_scan(scan_file):
	results = {'open':[],'closed':[]}
	for line in open(scan_file,'rb').readlines():
		ln = line.replace('\n', '')
		o = ln.split(' open ')
		if len(o) == 2:
			try:
				port = int(o[0].split('/')[0])	
				prot = o[1].split(' ')[1].replace(' ','')
				if len(o[1].split(' ')[1])>1:
					prot = o[1].split(' ')[1]
				elif len(o[1].split(' ')[4])>1:
					prot = o[1].split(' ')[4]
				if len(o[1].split(' '))>5:
					n = len(o[1].split(' '))
					version = ''.join(o[1].split(' ')[5:n])
				else:
					version = ''
				results['open'].append([port, prot, version])
			except:
				pass
			
	return results

def run_scan(address):
	# TODO: do this legit no NMAP!!
	os.system('nmap -sV %s >> ScanData/%s' % (address, address))

def run_scanner(targ):
	n_threads=10; timeout=25
	# Clean up list
	ip_list = clean_address_list(targ, True)
	setup_folders()
	threads = 0
	random.shuffle(ip_list)
	start = time.time()
	try:
		for ip in ip_list:
			if ip not in os.listdir(os.getcwd()+'/ScanData'):
				print('[*] Scanning %s [%d/%d]' % (ip,len(os.listdir(os.getcwd()+'/ScanData')), len(ip_list)))
				Thread(target=run_scan, args=(ip,)).start()
				threads += 1; time.sleep(2)
				# wait for scans to finish 
				if threads >= n_threads:
					print '[~] Letting Threads catch up...'
					time.sleep(timeout) 
					threads = 0
	except KeyboardInterrupt:
		print '[!!] Killing Scanner'
		print '[ %d/%d Scans Completed]' % (len(os.listdir(os.getcwd()+'/ScanData')), len(ip_list))
		pass
	print '[%ss elapsed]' % str(time.time() - start)

def main():
	targets = 'unique.txt'
	
	if '-t' in sys.argv and len(sys.argv) > 2:
		targets = sys.argv[2]
	
	if '-scan' in sys.argv:
		run_scanner(targets)

	if '-parse' in sys.argv:
		ssh = 0;  	vnc = 0;  	rdp = 0
		ftp = 0;  	irc = 0;	svn = 0  	
		proxy = 0;	unkn = 0; 	upnp = 0;	
		https = 0;	http = 0;	pop3 = 0;
		sproxy = 0; telnet = 0; domain = 0
		database = {}
		for f in os.listdir(os.getcwd()+'/ScanData/'):
			data = parse_scan(os.getcwd()+'/ScanData/'+f)
			for sock in data['open']:
				port = sock[0]
				protocol = sock[1]
				if protocol == 'ssh':
					ssh += 1
				elif protocol == 'ftp':
					ftp += 1
				elif protocol == 'irc':
					irc += 1
				elif protocol == 'vnc':
					vnc += 1
				elif protocol == 'rdp':
					rdp += 1
				elif protocol == 'upnp':
					upnp += 1
				elif protocol == 'svn' or protocol == 'svn?':
					svn += 1
				elif protocol == 'telnet' or protocol == 'telnetd' or protocol == 'telnet?':
					telnet += 1
				elif protocol == 'pop3':
					pop3 += 1
				elif protocol == 'http' or protocol == 'http?':
					http += 1
				elif protocol == 'http-proxy':
					proxy += 1
				elif protocol == 'https' or protocol == 'https?':
					sproxy += 1
				elif protocol == 'domain':
					domain += 1
				elif protocol == 'unknown':
					unkn += 1
				# else:
				# 	print protocol
		counts = {'irc': irc, 'ftp': ftp, 'ssh': ssh, 'svn':svn, 'vnc': vnc, 'rdp':rdp,
				   'pop3':pop3,'http': http, 'https': sproxy, 'domain': domain,
				   'upnp':upnp, 'proxy':proxy, 'uknown':unkn, 'telnet': telnet,
				   }
		database['counts'] = counts
		for key in counts.keys():
			print('[*] %s Ports Open: \t%d' % (key.upper(), counts[key]))



if __name__ == '__main__':
	main()
