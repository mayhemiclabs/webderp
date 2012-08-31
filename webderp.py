#!/usr/bin/env python
#
# WebDERP
#
# webderp.py
#
# Monitoring Script
#
# All code Copyright (c) 2012, Ben Jackson and Mayhemic Labs -
# bbj@mayhemiclabs.com. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# * Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution.
# * Neither the name of the author nor the names of contributors may be
# used to endorse or promote products derived from this software without
# specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import os, urllib2, hashlib, smtplib, email.utils
from email.mime.text import MIMEText

def send_email(subject, text):
        server = smtplib.SMTP('kuroshio.innismir.net',587)

        msg = MIMEText(text)
        msg['To'] = email.utils.formataddr(('Your Name', 'you@yourdomain.com'))
        msg['From'] = email.utils.formataddr(('WebDERP', 'webderp@mayhemiclabs.com'))
        msg['Subject'] = subject

        try:
                server.ehlo()

                if server.has_extn('STARTTLS'):
                        server.starttls()
                        server.ehlo()
                        server.login('username', 'password')

                server.sendmail('claymore@mayhemiclabs.com', ['you@yourdomain.com'], msg.as_string())

        finally:
                server.quit()

        return 0

url_file = open('urls.txt')
urls = url_file.readlines()
url_file.close()

for url in urls:

	#Generate a hash for the URL
	url_sha1 = hashlib.sha1(url).hexdigest()

	#Hash the contents of the old page, if the page isn't cached, make something up
	if os.path.exists('/tmp/' + url_sha1):
		old_page_sha1 = hashlib.sha1(open('/tmp/' + url_sha1).read()).hexdigest()
	else:
		old_page_sha1 = 'deaddeadbeef'

	#Grab the URL
	opener = urllib2.build_opener()
	opener.addheaders = [('User-agent', 'Mozilla/5.0 (compatible; WebDERP; Rainbow Puking Unicorns)')]
	response = opener.open(url)

	#Store the contents
	text = response.read()

	#Hash the contents 
	new_page_sha1 = hashlib.sha1(text).hexdigest()

	#Alert and update the cached file if the contents have changed
	if new_page_sha1 != old_page_sha1:
		cached_file = open('/tmp/' + url_sha1, 'w')
		cached_file.write(text)
		cached_file.close()

		send_email('WebDERP Alert! - ' + url, "DERP Alert!\nURL: " + url + "\nOld SHA1: " + old_page_sha1 + "\nNew SHA1: " + new_page_sha1)
