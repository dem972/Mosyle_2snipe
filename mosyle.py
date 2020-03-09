import requests

class Mosyle:
	
	# Create Mosyle instance
	def __init__(self, key):
		# Attribute the variable to the instance
		self.url = "https://businessapi.mosyle.com/v1"
		self.request = requests.Session()
		self.request.headers["accesstoken"] = key
		
	# Create variables requests
	def list(self, start, end):
		params = {
			"operation": "list",
			"options": {
				"os": "mac",
				"enrolldate_start": start,
				"enrolldate_end": end	
			}
		}
		# Concatanate url and send the request
		return self.request.post(self.url + "/devices", json = params )
		

	


