from twilio.rest import TwilioRestClient

class Twilio(object):
	"""Twilio wrapper for notification"""
	def __init__(self):
		super(Twilio, self).__init__()
		self.account = "ACed768cc712214eeb18dbc683d4f86b5b"
		self.token = "be7e3671967e3c5d8a00b81e12c853ff"
		self.client = TwilioRestClient(self.account, self.token)
		# self.from_number = "+1 567-245-0765"
		self.from_number = "forced error"

	def send_sms(self,to_number,sms_text):
		message = self.client.sms.messages.create(to=to_number, from_=self.from_number,body=sms_text)







