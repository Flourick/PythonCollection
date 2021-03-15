import imaplib, re, sys, os, shutil
from imap_tools.imap_utf7 import decode as decodeUTF7

##############################
########### CONFIG ###########
##############################
HOST = "imap.example.com" # imap server address
USERNAME = "example@example.com" # email account username
PASSWORD = "password" # email account password
PORT = "993" # port, usually 143 or 993 if SSL on
SSL = True # True for encrypted, False for not
AUTO_CLOSE = False # True to automatically close after download is finished, False for prompt to close
SKIP_EXISTING = True # True to skip existing email files, False to overwrite them
ZIP_AFTER = False # True to zip the entire output directory (and remove the original), False not to
##############################
##############################
##############################

def version_check():
	if sys.version_info < (3, 5):
		raise Exception("You must use Python 3.5 or higher.")

def die(autoclose: bool = True):
	if not autoclose:
		print()
		input("Press enter...")
	exit()


class IMAPConnection:
	def __init__(self, host: str, username: str, password: str, port: int, ssl: bool):
		self.host = host
		self.username = username
		self.password = password
		self.port = port
		self.ssl = ssl
		self.connection = None

	def connect(self):
		if self.ssl:
			self.connection = imaplib.IMAP4_SSL(self.host, self.port)
		else:
			self.connection = imaplib.IMAP4(self.host, self.port)

		self.connection.login(self.username, self.password)
	
	def reconnect(self, mailbox: str = None):
		self.quiet_close()
		self.connect()
		
		if mailbox != None:
			self.connection.select(mailbox, readonly=True)

	def quiet_close(self):
		try:
			self.connection.close()
			self.connection.logout()
		except:
			pass

	def close(self):
		self.connection.close()
		self.connection.logout()

	def get_all_mailboxes(self) -> list:
		code, data = self.connection.list()

		mailboxes = []

		if code == "OK":
			response_pattern = re.compile(r'\((?P<flags>.*?)\) "(?P<delimiter>.*)" (?P<name>.*)')
			directoryPattern = re.compile(r'[^\w\-_\. ]')

			for dir_bytes in data:
				delimiter, mailbox_decoded = response_pattern.match(decodeUTF7(dir_bytes)).groups()[1:]
				mailbox = response_pattern.match(dir_bytes.decode()).groups()[2]
				mailbox_decoded = mailbox_decoded.strip('"')

				directory_path = os.sep.join([directoryPattern.sub('_', x) for x in mailbox_decoded.split(delimiter.strip('"'))])

				mailboxes.append([mailbox, mailbox_decoded, directory_path])
		
		return mailboxes

	def get_all_email_ids_in_mailbox(self, mailbox: str) -> tuple[int, list]:
		code, data = self.connection.select(mailbox, readonly=True)

		emails = []
		email_count = 0

		if code == "OK":
			email_count = int(data[0])

			code, data = self.connection.search(None, 'ALL')

			if code == "OK":
				for id in data[0].split():
					emails.append(id)

		return email_count, emails

	def fetch_email(self, id: int, mailbox: str = None) -> list:
		if mailbox != None:
			code = self.connection.select(mailbox, readonly=True)[0]

			if code != "OK":
				return []

		code, email = self.connection.fetch(id, '(RFC822)')

		if code == "OK":
			return email
		else:
			return []
		

if __name__ == "__main__":
	version_check()

	connection = IMAPConnection(HOST, USERNAME, PASSWORD, PORT, SSL)
	root_directory = os.path.join(os.getcwd(), USERNAME)

	try:
		connection.connect()
		print("CONNECTED!")
		print()

		mailboxes = connection.get_all_mailboxes()

		if not mailboxes:
			print("ERROR: Could not get any mailboxes!")
		else:
			if not os.path.exists(root_directory):
				os.makedirs(root_directory)

		wrong_count = 0

		for mailbox, mailbox_decoded, directory in mailboxes:
			email_count, email_ids = connection.get_all_email_ids_in_mailbox(mailbox)
			current_directory = os.path.join(root_directory, directory)

			if not os.path.exists(current_directory):
				os.makedirs(current_directory)

			print("In mailbox (" + str(email_count) + " emails):", mailbox_decoded)

			if email_count > len(email_ids):
				print("  -> WARNING: Received amount of emails does not equal with the amount of emails in mailbox! Some emails might be missing.")
				wrong_count += email_count - len(email_ids)

			cur_email_num = 0
			for id in email_ids:
				cur_email_path = os.path.join(current_directory, '%s.eml' %(id.decode()))
				cur_email_num += 1

				if SKIP_EXISTING and os.path.exists(cur_email_path):
					print("  -> (" + str(cur_email_num) + "/" + str(email_count) + ") Skipped existing email:", id.decode())
					continue

				retry_count = 3

				while retry_count > 0:
					try:
						data = connection.fetch_email(id)

						if not data:
							print("  -> (" + str(cur_email_num) + "/" + str(email_count) +") ERROR: could not download email:", id.decode())
							wrong_count += 1
						else:
							with open(cur_email_path, 'wb') as file:
								file.write(data[0][1])

							print("  -> (" + str(cur_email_num) + "/" + str(email_count) +") Downloaded email:", id.decode())
						
						retry_count = 0
					
					except imaplib.IMAP4.abort:
						connection.reconnect(mailbox)
						print("  -> (" + str(cur_email_num) + "/" + str(email_count) +") Retrying to download email:", id.decode())
						retry_count -= 1

						if retry_count == 0:
							print("  -> (" + str(cur_email_num) + "/" + str(email_count) +") ERROR: could not download email:", id.decode())
							wrong_count += 1

		print()
		if wrong_count > 0:
			print("FINISHED! Could not download", wrong_count, "emails due to errors!")
		else:
			print("FINISHED! Downloaded all emails successfully!")

		if ZIP_AFTER:
			print()
			print("Zipping...")
			shutil.make_archive(root_directory, "zip", root_directory)
			shutil.rmtree(root_directory)
			print("ZIPPED!")

	except Exception as e:
		print("ERROR:", e)

	finally:
		connection.quiet_close()
		die(AUTO_CLOSE)
