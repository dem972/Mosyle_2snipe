# Import all the things
import json
import datetime
import configparser

from mosyle import Mosyle
from snipe import Snipe

# Set some Variables from the settings.conf:
config = configparser.ConfigParser()
config.read('settings.ini')

# This is the address, cname, or FQDN for your snipe-it instance.
apiKey = config['snipe-it']['apiKey']
defaultStatus = config['snipe-it']['defaultStatus']
apple_manufacturer_id = config['snipe-it']['manufacturer_id']

# Set the token for the Mosyle Api
mosyle = Mosyle(config['mosyle']['token'])
mosyle_response = mosyle.list("1579534718", "1579534718").json()

# Set the token for Snipe It 
snipe = Snipe(apiKey)

# Return Mosyle hardware and search them in snipe
for sn in mosyle_response['response'][0]['devices']:
    asset = snipe.listHardware(sn['serial_number']).json()
    model = snipe.searchModel(sn['device_model']).json()

    if model['total'] == 0:
        model = snipe.createModel(sn['device_model']).json()
        model = model['payload']['id']
    else:
        model = model['rows'][0]['id']

    # If asset doesnt exist create and assign it 
    if asset['total'] == 0:
        asset = snipe.createAsset(sn['device_name'], model, sn['serial_number']).json()
        snipe.assignAsset(sn['CurrentConsoleManagedUser'], asset['payload']['id'])
        continue

    # Update the existing Device
    if asset['total'] == 1:
        snipe.updateAsset(asset['rows'][0]['id'], sn['ethernet_mac_address'], str(float(sn['available_disk'])), sn['osversion'], str(float(sn['total_disk'])))
        

    # Check the asset assignement state 
    if asset['rows'][0]['assigned_to'] == None:
            snipe.assignAsset(sn['CurrentConsoleManagedUser'], asset['rows'][0]['id'])
            
    elif asset['rows'][0]['assigned_to']['username'] == sn['CurrentConsoleManagedUser']:
        continue

    elif sn['CurrentConsoleManagedUser'] == None:
        continue

    elif asset['rows'][0]['assigned_to']['username'] != sn['CurrentConsoleManagedUser']:
        snipe.unasigneAsset(asset['rows'][0]['id'])
        snipe.assignAsset(sn['CurrentConsoleManagedUser'], asset['rows'][0]['id'])

   
   



       



    





            
  


            





    


