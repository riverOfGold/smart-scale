def send_email(user, pwd, recipient, subject, body):
	import smtplib

	FROM = user
	TO = recipient if isinstance(recipient, list) else [recipient]
	SUBJECT = subject
	TEXT = body

	#prepare actual message
	message = """From: %s\nTo: %s\nSubject: %s\n\n%s""" % (FROM, ', '.join(TO), SUBJECT, TEXT)
	try:
		server = smtplib.SMTP('smtp.gmail.com', 587)
		server.ehlo()
		server.starttls()
		server.login(user, pwd)
		server.sendmail(FROM, TO, message)
		server.close()
		print('succesfully sent the email')
	except:
		print('email send failed')

send_email('pihatchery19@gmail.com', '23rdbday', 'kirk.mcmillan@griegseafood.com', 'test#1', 'this is a test of the email send')

