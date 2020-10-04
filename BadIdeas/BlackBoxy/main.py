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
	content = header+body+enc+dec+hide+see
	open(os.getcwd()+'/utils.py', 'wb').write(content)


def main():
	create_utils()
	import utils # THIS IS SO SKETCHY BUT LETS TEST IT LOL!
	if '-e' in sys.argv and len(sys.argv) > 2:
		fname = sys.argv[2]
		if os.path.isfile(fname):
			utils.fencrypt(fname,True)
	if '-run' in sys.argv:
		open('hi.mkv','wb').write(utils.fdecrypt('omg.lol'))
		if os.name == 'posix' or os.name != 'nt':
			os.system('vlc hi.mkv')
		elif os.name == 'nt':
			os.system('hi.mkv')
		os.remove('rm hi.mkv utils.py *.pyc')

if __name__ == '__main__':
	main()
