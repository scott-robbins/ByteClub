from threading import Thread
import random
import socket 
import time 
import sys 
import os


class PortScanner():
	target = ''
	ports = []
	results = {}
	n_threads = 5
	verbose = False
	
	def __init__(self, ip_address, prange, verbosity):
		self.target = ip_address
		self.verbose = verbosity
		self.set_port_space(prange)
		self.run()

	def set_port_space(self, pran):
		if len(pran)>1:
			for port in pran:
				self.ports.append(port)
		else:
			# Default port space
			self.ports = [21,22,23,25,80,110,139,443,445,1433,1729,3389,5900,8080]
		for point in self.ports:
			self.results[point] = {'state':False,'banner':''}

	def scan_port(self, sock_num):
		state = False; banner = ''
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		except socket.error:
			pass
		try:
			s.connect((self.target, sock_num))
			state = True
			blocked = True; t0 = time.time()
			while blocked and (time.time()-t0<1.5):
				banner = s.recv(1028)
				recv = False
		except socket.error:
			pass
		s.close()
		self.results[sock_num]['state'] = state
		self.results[sock_num]['banner'] = banner
		# show whats happening as it happens if verbose
		if self.verbose and state:
			print('%d\tOPEN\t%s' % (sock_num, banner))
		return state, banner


	def run(self):
		if self.target == '':
			print('[!!] No Target Specified')
			exit()
		for sock in self.ports:
			Thread(target=self.scan_port, args=(sock,)).start()
	
	def summary(self):
		print '\033[1m\033[3mStarting Scan on %s \033[0m' % self.target
		print 'PORT\tSTATE\tBANNER'
		for p in self.results.keys():
			# show whats happening as it happens if verbose
			if self.results[p]['state']:
				print('%d\tOPEN\t%s' % (p, self.results[p]['banner']))

def ascii():
	head = "(  _`\\              ( )_        (  _`\\\n"                                    
	head += "| (_) ) _ __  _   _ | ,_)   __  | (_) )   _ _   ___    ___     __   _ __ \n"\
	"|  _ <'( '__)( ) ( )| |   /'__`\\|  _ <' /'_` )/' _ `\\/' _ `\\ /'__`\\( '__)\n"\
	"| (_) )| |   | (_) || |_ (  ___/| (_) )( (_| || ( ) || ( ) |(  ___/| |   \n"\
	"(____/'(_)   `\\___/'`\\__)`\\____)(____/'`\\__,_)(_) (_)(_) (_)`\\____)(_)   "
	return head

def main():
	target = '127.0.0.1'
	verb = False
	if len(sys.argv)>=2:
		target = sys.argv[1]

	if '-v' in sys.argv:
		div = '='*80
		print '\033[1m%s\033[0m' % div
		print '\033[1m\033[32m' + ascii() + '\033[0m'
		print '\033[1m%s\033[0m' % div
		print '\033[1m\033[3m\t\t\tStarting Scan on %s \033[0m' % target
		print 'PORT\tSTATE\tBANNER'
		verb = True



	# Run It
	test = PortScanner(target, [], verb)

	if not verb:
		time.sleep(3)
		test.summary()

if __name__ == '__main__':
	main()
