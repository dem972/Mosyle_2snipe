import requests

class Mosyle:
	
	# Create Mosyle instance
	def __init__(self, key):
		# Attribute the variable to the instance
		self.url = "https://businessapi.mosyle.com/v1"
		self.request = requests.Session()
		self.request.headers["accesstoken"] = key
		
	# Create variables requests
	def list(self):
		params = {
			"operation": "list",
			"options": {
				"os": "mac, ios"	
			}
		}
		# Concatanate url and send the request
		return self.request.post(self.url + "/devices", json = params )

	def listTimestamp(self, start, end):
		params = {
			"operation": "list",
			"options": {
				"os": "mac, ios",
				"enrolldate_start": start,
				"enrolldate_end": end	
			}
		}
		return self.request.post(self.url + "/devices", json = params )

	def listmobile(self):
		params = {
			"operation": "list",
			"options": {
				"os": "ios"
			}
		}
		return self.request.post(self.url + "/devices", json = params )

	def listuser(self, iduser):
		params = {
			"operation": "list_users",
			"options": { "identifiers": [iduser]
				}
		}
		return self.request.post(self.url + "/users", json = params )


