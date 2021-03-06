# Import all the things
import json
import datetime
import configparser

from mosyle import Mosyle
from snipe import Snipe

# Converts datetime to timestamp for Mosyle
ts = datetime.datetime.now().timestamp() - 200

# Set some Variables from the settings.conf:
config = configparser.ConfigParser()
config.read('settings.ini')

# This is the address, cname, or FQDN for your snipe-it instance.
apiKey = config['snipe-it']['apiKey']
defaultStatus = config['snipe-it']['defaultStatus']
apple_manufacturer_id = config['snipe-it']['manufacturer_id']

# Set the token for the Mosyle Api
mosyle = Mosyle(config['mosyle']['token'])

# Set the call type for Mosyle
calltype = config['mosyle']['calltype']

mosyle_response = mosyle.list().json()
mosyle_test = mosyle.list()
if calltype == "timestamp":
    mosyle_response = mosyle.listTimestamp(ts, ts).json()



# Set the token for Snipe It
snipe = Snipe(apiKey)


# Return Mosyle hardware and search them in snipe
for sn in mosyle_response['response'][0]['devices']:
   
    asset = snipe.listHardware(sn['serial_number']).json()
    model = snipe.searchModel(sn['device_model']).json()

    print(sn['device_model'])

    if sn['CurrentConsoleManagedUser'] != None and "userid" in sn:
        mosyle_user = sn['userid']

    else:
        continue

    
    print("Mosyle devices found:", sn['serial_number'],sn['device_name'], sn['device_model'])

    if mosyle_response['response'] == "status":
        exit(1)

    
    # Create the asset model if is not exist
    if model['total'] == 0:
        if sn['os'] == "mac":
            model = snipe.createModel(sn['device_model']).json()
            model = model['payload']['id']
        if sn['os'] == "ios":
            model = snipe.createMobileModel(sn['device_model']).json()
            model = model['payload']['id']

    else:
        model = model['rows'][0]['id']

    # If asset doesnt exist create and assign it
    if asset['total'] == 0:
        asset = snipe.createAsset(sn['device_name'], model, sn['serial_number']).json()
        if mosyle_user == "users":
            snipe.assignAsset(mosyle_user['response'][0]['users'][0]['identifier'], asset['payload']['id'])
        continue

    # Update existing Devices

    if asset['total'] == 1:
        #f"{x:.2f}"
        print(asset['rows'][0]['name'])
        snipe.updateAsset(asset['rows'][0]['id'], sn['device_name'], sn['wifi_mac_address'], str(float(sn['available_disk'])), sn['osversion'], str(float(sn['total_disk'])))

    # Check the asset assignement state

    if asset['rows'][0]['assigned_to'] == None and sn['userid'] != None:
            snipe.assignAsset(sn['userid'], asset['rows'][0]['id'])
            continue

    elif sn['userid'] == None:
        snipe.unasigneAsset(asset['rows'][0]['id'])
        continue

    elif asset['rows'][0]['assigned_to']['username'] == sn['userid']:
        continue

    elif asset['rows'][0]['assigned_to']['username'] != sn['userid']:
        snipe.unasigneAsset(asset['rows'][0]['id'])
        snipe.assignAsset(sn['userid'], asset['rows'][0]['id'])