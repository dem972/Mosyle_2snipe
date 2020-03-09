import requests

class Snipe:
    def __init__(self, snipetoken):
        self.url = "https://snipe.vctools.team/api/v1"
        self._snipetoken = snipetoken

    @property
    def headers(self):
        return {
            "authorization": "Bearer " + self._snipetoken,
            "accept": "application/json",
            "content-type": "application/json",
        }    

    #@property
    def listHardware(self, serial):
        return requests.request("GET", self.url + "/hardware/byserial/" + serial, headers = self.headers)

    def searchModel(self, model):
        return requests.request("GET", self.url + "/models", params = {"limit": "50", "offset": "0", "search": model, "sort": "created_at", "order": "asc"}, headers = self.headers )
    
    def createModel(self, model):
        payload = {
			"name": model,
            "category_id": 2,
            "manufacturer_id": 1,
            "model_number": model
        }

        return requests.request("POST", self.url + "/models", json = payload, headers = self.headers)

    def createAsset(self, asset, model, serial):
        payload = {
            "asset_tag": asset,
            "status_id": 2,
            "model_id": model,
            "name": asset
        }
        asset = requests.request("POST", self.url + "/hardware", json = payload, headers = self.headers).json()
        
        payload = {
            "serial": serial
        }
        return requests.request("PATCH", self.url + "/hardware/" + str(asset['payload']['id']), json = payload, headers = self.headers)


    def assignAsset(self, user, asset_id):
        payload = {
            "search": user,
            "limit": 2
        }
        response = requests.request("GET", self.url + "/users", params = payload, headers = self.headers).json()

        if response['total'] == 0:
            return

        payload = {
            "assigned_user": response['rows'][0]['id'],
            "checkout_to_type": "user"
        }
        return requests.request("POST", self.url + "/hardware/" + str(asset_id) + "/checkout", json = payload, headers = self.headers )

    def unasigneAsset(self, asset_id):
        return requests.request("POST", self.url + "/hardware/" + str(asset_id) + "/checkin", headers = self.headers )

    def updateAsset(self, asset_id, mac_adress, available_disk, osversion, percentdisk):
        payload = {
            "_snipeit_mac_address_1": mac_adress,
            "_snipeit_available_disk_5": available_disk + " GB",
            "_snipeit_osversion_4": osversion,
            "_snipeit_percent_disk_3": percentdisk + " GB"
        }
        return requests.request("PATCH", self.url + "/hardware/" + str(asset_id), json = payload, headers = self.headers)



    






#if __name__ == "__main__":
    #token_snipe = Snipe("Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjI0N2RjNDA3YzI4NTZjMzIxZDlmNTdlMDU0MzY4ZDBhYWRjN2M4OWZhM2QwMGEwNDE0ZTA2YTFhZjI1OWY2MjFkMTBjNzlhZmEyOTA2NmU0In0.eyJhdWQiOiIxIiwianRpIjoiMjQ3ZGM0MDdjMjg1NmMzMjFkOWY1N2UwNTQzNjhkMGFhZGM3Yzg5ZmEzZDAwYTA0MTRlMDZhMWFmMjU5ZjYyMWQxMGM3OWFmYTI5MDY2ZTQiLCJpYXQiOjE1ODM0OTI3OTIsIm5iZiI6MTU4MzQ5Mjc5MiwiZXhwIjoxNjE1MDI4NzkyLCJzdWIiOiI2MDgiLCJzY29wZXMiOltdfQ.j61X413QH9Hzp2w2_P0Y9tB2aKC3eEmwJT4pkKWF9Rm9YyFEIQEi9YOxroRm_D6lmEVowLtHAPRHwMlzqtxkhpDTbam3ZYO4MUOdhqkKLoM-h3Dj2gi-LLz57T-A0nyRiA2Lu2_ju8CWp-7qddkDdmio11uEPXAMzggaYU8Q4g8oe_SvuRkaBCjRyxgKIWZNJpjVPDDJRIvMngBgoZ4SLdv0y6ocdqvFIyGUQl0i7yfPP7fdHo7RiNqbM18o-r4hVun030rC1Yr7qKOZU59F48WfALkgvKENFZBF9LgOIaDcj7tvAezvOugIVTYkXV125lyq9cQvcqTl8XqeA_64Cj_ew6n9mCptQZGGky0jwmjq_1fgubbGgSAMprVcb8CgRA2XMs5AJiaJqvUv1bduanI-8H7EMQui5_XXwcmwLm9c-bMe-1XybBNibeLdlRVE-ENR94vY9tcr3byF52hx4QPNofC-PhW7MLqpxy88gkDKNK-3K8CHRf6oGW70kZsvLekoG9CeIfhPMD5cMwBsG48Vf9UICimWP4jYT-8z38vqr4saYKQgg05vsOmvyzBIQh3nSa6N7SARHFOyKNx4CrXInOUBO8xPf5cPeU4tNPhM7ZXJDMAS1mPFSEzhv5pqe39WNR1HAGgGOhHJ2-14aRF4i_kY4Jj-M8dVd8fFON0")
    #test2 = token_snipe.list
    #print(test2.text)