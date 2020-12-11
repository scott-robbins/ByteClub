from threading import Thread
import portscanner
import random
import time
import sys
import os 

lookup = {21:'ftp',22:'ssh', 23:'telnet', 25:'smtp', 110:'pop3',
		  113: 'irc', 139:'NetBIOS', 443:'https', 445:'microsoft-ds', 
		  587: 'smtp',1723:'pptp',1900:'upnp', 3309:'msql', 3389:'rdp', 3690: 'svn', 
		  5900:'vnc', 8080:'http-proxy', 8081:'https-proxy', 8082:'https-proxy?'}


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
	results = {'open':[],'filtered':[]}
	for line in open(scan_file,'rb').readlines():
		ln = line.replace('\n', '')
		o = ln.split(' open ')
		f = ln.split(' filtered ')
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
		# now check for filtered 
		elif len(f)==2:
		
			try:
				port = int(f[0].split('/')[0].replace(' ',''))	
				prot = f[1].split(' ')[0].replace(' ','')
				
				if len(f[1].split(' '))>5:
					n = len(f[1].split(' '))
					version = ''.join(f[1].split(' ')[5:n])
				else:
					version = ''
				results['filtered'].append([port, prot, version])
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

def count_scans(display):
	ssh = 0;  	vnc = 0;  	rdp = 0
	ftp = 0;  	irc = 0;	svn = 0 
	pptp= 0;	smtp = 0;	msql = 0
	proxy = 0;	unkn = 0; 	upnp = 0;	
	https = 0;	http = 0;	pop3 = 0;
	sproxy = 0; telnet = 0; domain = 0
	database = {}; 
	ssh_versions = {};	smtp_versions = {}
	ftp_versions = {};	http_versions = {}
	rdp_versions = {};	msql_versions = {}
	for a in os.listdir(os.getcwd()+'/ScanData/'): database[a] = {}
	for f in os.listdir(os.getcwd()+'/ScanData/'):
		data = parse_scan(os.getcwd()+'/ScanData/'+f)
		database[f]['open'] = []
		database[f]['filtered'] = []
		for sock in data['open']:
			port = sock[0]
			protocol = sock[1]
			extra = sock[-1]
			if protocol == 'ssh':
				ssh += 1
				database[f]['open'].append([port, protocol, extra])
				if extra not in ssh_versions.keys():
					ssh_versions[extra] = [f]
				else:
					ssh_versions[extra].append(f)
			elif protocol == 'ftp':
				ftp += 1
				database[f]['open'].append([port, protocol, extra])
				if extra not in ftp_versions.keys():
					ftp_versions[extra] = [f]
				else:
					ftp_versions[extra].append(f)
			elif protocol == 'irc':
				irc += 1
				database[f]['open'].append([port, protocol, extra])
			elif protocol == 'vnc':
				vnc += 1
				database[f]['open'].append([port, protocol, extra])
			elif protocol == 'microsoft-ds':
				rdp += 1
				database[f]['open'].append([port, protocol, extra])
				if extra not in rdp_versions.keys():
					rdp_versions[extra] = [f]
				else:
					rdp_versions[extra].append(f)
			elif protocol == 'upnp':
				upnp += 1
				database[f]['open'].append([port, protocol, extra])
			elif protocol == 'svn' or protocol == 'svn?':
				svn += 1
				database[f]['open'].append([port, protocol, extra])
			elif protocol == 'pptp':
				pptp += 1
				database[f]['open'].append([port, protocol, extra])
			elif protocol == 'smtp':
				smtp += 1
				database[f]['open'].append([port, protocol, extra])
				if extra not in smtp_versions.keys():
					smtp_versions[extra] = [f]
				else:
					smtp_versions[extra].append(f)
			elif protocol == 'telnet' or protocol == 'telnetd' or protocol == 'telnet?':
				telnet += 1
				database[f]['open'].append([port, protocol, extra])
			elif protocol == 'pop3':
				pop3 += 1
				database[f]['open'].append([port, protocol, extra])
			elif protocol == 'http' or protocol == 'http?':
				http += 1
				database[f]['open'].append([port, 'http', extra])
				if extra not in http_versions.keys():
					http_versions[extra] = [f]
				else:
					http_versions[extra].append(f)
			elif protocol == 'http-proxy':
				proxy += 1
				database[f]['open'].append([port, protocol, extra])
			elif protocol == 'https' or protocol == 'https?':
				sproxy += 1
				database[f]['open'].append([port, protocol, extra])
			elif protocol == 'domain':
				domain += 1
				database[f]['open'].append([port, protocol, extra])
			elif protocol == 'mysql':
				msql += 1
				database[f]['open'].append([port, protocol, extra])
			elif protocol == 'unknown':
				unkn += 1
				database[f]['open'].append([port, protocol, extra])
		for sock in data['filtered']:
			port = sock[0]
			protocol = sock[1]
			extra = sock[-1]
			if protocol == 'ssh':
				ssh += 1
				database[f]['filtered'].append([port, protocol, extra])
				if extra not in ssh_versions.keys():
					ssh_versions[extra] = [f]
				else:
					ssh_versions[extra].append(f)
			elif protocol == 'ftp':
				ftp += 1
				database[f]['filtered'].append([port, protocol, extra])
				if extra not in ftp_versions.keys():
					ftp_versions[extra] = [f]
				else:
					ftp_versions[extra].append(f)
			elif protocol == 'irc':
				irc += 1
				database[f]['filtered'].append([port, protocol, extra])
			elif protocol == 'vnc':
				vnc += 1
				database[f]['filtered'].append([port, protocol, extra])
			elif protocol == 'microsoft-ds':
				rdp += 1
				database[f]['filtered'].append([port, protocol, extra])
				if extra not in rdp_versions.keys():
					rdp_versions[extra] = [f]
				else:
					rdp_versions[extra].append(f)
			elif protocol == 'upnp':
				upnp += 1
				database[f]['filtered'].append([port, protocol, extra])
			elif protocol == 'svn' or protocol == 'svn?':
				svn += 1
				database[f]['filtered'].append([port, protocol, extra])
			elif protocol == 'pptp':
				pptp += 1
				database[f]['filtered'].append([port, protocol, extra])
			elif protocol == 'smtp':
				smtp += 1
				database[f]['filtered'].append([port, protocol, extra])
				if extra not in smtp_versions.keys():
					smtp_versions[extra] = [f]
				else:
					smtp_versions[extra].append(f)
			elif protocol == 'telnet' or protocol == 'telnetd' or protocol == 'telnet?':
				telnet += 1
				database[f]['filtered'].append([port, protocol, extra])
			elif protocol == 'pop3':
				pop3 += 1
				database[f]['filtered'].append([port, protocol, extra])
			elif protocol == 'http' or protocol == 'http?':
				http += 1
				database[f]['filtered'].append([port, 'http', extra])
				if extra not in http_versions.keys():
					http_versions[extra] = [f]
				else:
					http_versions[extra].append(f)
			elif protocol == 'http-proxy':
				proxy += 1
				database[f]['filtered'].append([port, protocol, extra])
			elif protocol == 'https' or protocol == 'https?':
				sproxy += 1
				database[f]['filtered'].append([port, protocol, extra])
			elif protocol == 'domain':
				domain += 1
				database[f]['filtered'].append([port, protocol, extra])
			elif protocol == 'mysql':
				msql += 1
				database[f]['filtered'].append([port, protocol, extra])
			elif protocol == 'unknown':
				unkn += 1
				database[f]['filtered'].append([port, protocol, extra])
	counts = {'irc': irc, 'ftp': ftp, 'ssh': ssh, 'svn':svn, 'vnc': vnc, 'rdp':rdp,
			  'pop3':pop3,'http': http,'pptp':pptp,'upnp': upnp, 'smtp':smtp,
			  'proxy': proxy, 'uknown': unkn, 'telnet': telnet, 'mysql':msql,
			   'https': sproxy, 'domain': domain,}
	database['counts'] = counts
	if display:
		for key in counts.keys():
			print('[*] %s Ports Open/Filtered:\t%d' % (key.upper(), counts[key]))
	
	print '- %d versions of FTP found' % len(ftp_versions.keys())
	print '- %d versions of RDP found' % len(rdp_versions.keys())
	print '- %d versions of SSH found' % len(ssh_versions.keys())
	print '- %d versions of SMTP found' % len(smtp_versions.keys())
	print '- %d versions of HTTP found' % len(http_versions.keys())	

	versions = {'ssh': ssh_versions,
				'ftp': ftp_versions,
				'smtp': smtp_versions}
	return database, versions

def display_host_result(data, addr):
	print '[*] %s has the following ports OPEN:' % addr
	print 'PORT\tSERVICE\tVERSION'
	for port in data[addr]['open']:
		ports_n = port[0]
		service = port[1]
		version = ''
		if port[2] != port[1] and port[2] !='':
			version = port[2]
		print '%d\t%s\t%s' % (ports_n, service.encode('utf-8'), version.encode('utf-8'))

def query_term(search_term, data):
	print 'Showing Machines with Open %s' % search_term
	for machine in data.keys():
		if 'open' in data[machine].keys():
			for spot in data[machine]['open']:
				if spot[1] == search_term:
					print '[*] %s has %s OPEN' % (machine, search_term.upper())

		if 'filtered' in data[machine].keys():
			for spot in data[machine]['filtered']:
				if spot[1] == search_term:
					print '[*] %s has %s FILTERED' % (machine, search_term.upper())

def main():
	verbosity = False
	targets = 'unique.txt'
	
	if '-t' in sys.argv and len(sys.argv) > 2:
		targets = sys.argv[2]
	
	if '-scan' in sys.argv:
		run_scanner(targets)

	if '-parse' in sys.argv:
		data = count_scans(True)

	if '-search' in sys.argv and len(sys.argv)  > 2:
		search = sys.argv[2]
		
		database, types = count_scans(verbosity)
		if 'version' in sys.argv:
			opts = {}; i = 0
			if search in types.keys():
				for ver in types.keys():
					
					if ver == search:
						for k in types[ver].keys():
							i += 1
							print '[%d] %s' % (i,k)
							opts[i] = k
						opt = int(input('Enter # to view one of these: '))
						if opt not in opts.keys():
							print '!! Illegal Selection'
						else:
							for addr in types[ver][opts[opt]]:
								print addr
					elif search == 'rdp':
						for k in types['microsoft-ds'].keys():
							i += 1
							print '- %s' % k
							opts[i] = 'microsoft-ds'

						opt = int(input('Enter # to view one of these: '))
						if opt not in opts.keys():
							print '!! Illegal Selection'
						else:
							for addr in types[ver][opts[opt]]:
								print addr
			
		elif search in database['counts'].keys():
			query_term(search, database)
			
		else: # check if they provided a port number
			is_port = False
			try:
				port = int(search)
				is_port = True
			except:
				pass
			if is_port:
				search = lookup[port]
				query_term(search, database)
				
			else: # check if they provided an ip
				if len(search.split('.'))>=4:
					if search in database.keys():
						print '[*] Revtrieving Scan results for %s' % search
						display_host_result(database, search)

if __name__ == '__main__':
	main()
