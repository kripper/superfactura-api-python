import httplib, urllib
import zlib
import json
import base64

class SuperFacturaAPI:
	version = '1.4-ruby'
	user = ''
	password = ''

	def __init__(self, user, password):
		self.user = user
		self.password = password

	def SendDTE(self, data, ambiente, options):
		options['ambiente'] = ambiente
		options['encoding'] = 'UTF-8'
		options['version'] = self.version

		if options['savePDF']:
			options['getPDF'] = 1

		if options['saveXML']:
			options['getXML'] = 1

		output = self.SendRequest(data, options)
		obj = json.loads(output)
		if obj['ack'] != 'ok':
			text = obj['response']['title'] + " - " if obj['response']['title'] != "" else "" + obj['response']['message']
			raise ValueError("ERROR: " + text)

		appRes = obj['response']

		folio = appRes['folio']
		if appRes['ok'] == "1":
			savePDF = options['savePDF']
			if savePDF:
				self.WriteFile(savePDF + ".pdf", self.DecodeBase64(appRes['pdf']));

				if appRes['pdfCedible']:
					self.WriteFile(savePDF + "-cedible.pdf", self.DecodeBase64(appRes['pdfCedible']));

			saveXML = options['saveXML']
			if saveXML:
				self.WriteFile(saveXML + ".xml", appRes['xml'].encode('latin-1'));
		else:
			raise ValueError(output)

		return appRes

	def SendRequest(self, data, options):
		params = urllib.urlencode({
			'user': self.user,
			'pass': self.password,
			'content': json.dumps(data, encoding='latin1'),
			'options': json.dumps(options, encoding='latin1')
		})

		headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
		conn = httplib.HTTPSConnection("superfactura.cl")
		conn.request("POST", "/?a=json", params, headers)
		response = conn.getresponse()
		body = response.read();
		conn.close()
		return self.Decompress(body)

	def Decompress(self, gzip):
		return zlib.decompress(gzip, 16+zlib.MAX_WBITS)

	def DecodeBase64(self, b64):
		return b64.decode('base64')
		# return base64.decodebytes(b64)
		# return base64.standard_b64decode(b64)
		#return binascii.a2b_base64(b64)

	def WriteFile(self, filename, content):
		f = open(filename, "wb")
		f.write(content)
		f.close()
