"""
# Domoticz Advanced Thermostat Python Plugin

This thermostat plugin allows precise temperature management and regulation per individual room

## Installation

```bash
cd ~
git clone https://github.com/gaelj/DomoticzAdvancedThermostatPlugin.git domoticz/plugins/DAT
chmod +x domoticz/plugins/DAT/plugin.py
sudo systemctl restart domoticz.service
```

For more details, see [Using Python Plugins](https://www.domoticz.com/wiki/Using_Python_plugins)
"""

"""
<plugin
    key="AdvancedThermostat"
    name="Advanced Thermostat"
    author="gaelj"
    version="1.0.0"
    wikilink="https://github.com/gaelj/DomoticzAdvancedThermostatPlugin/blob/master/README.md"
    externallink="https://github.com/gaelj/DomoticzAdvancedThermostatPlugin">

    <description>
        <h2>Domoticz Advanced Thermostat</h2><br/>
        This thermostat plugin allows precise temperature management and regulation per individual room

        <h3>Modes</h3>
        <ul style="list-style-type:square">
            <li>off</li>
            <li>away</li>
            <li>night</li>
            <li>eco</li>
            <li>comfort</li>
        </ul>

        <h3>Features</h3>
        <ul style="list-style-type:square">
            <li>individual room temperature management</li>
            <li>global presence management</li>
            <li>room presence management</li>
            <li>control thermostat radiator valves temperature settings</li>
            <li>read thermostat radiator valves temperature measurements</li>
        </ul>

        <h3>Devices</h3>
        <ul style="list-style-type:square">
            <li>Device Type - What it does...</li>
        </ul>

        <h3>Configuration</h3>
        Configuration options...
    </description>

    <params>
        <param field="Address"  label="Domoticz IP Address"                        width="200px" required="true"  default="localhost" />
        <param field="Port"     label="Port"                                       width="40px"  required="true"  default="8080"      />
        <param field="Username" label="Username"                                   width="200px" required="false" default=""          />
        <param field="Password" label="Password"                                   width="200px" required="false" default=""          />
        <param field="Mode1"    label="Inside Temperature Sensors (idx1, idx2...)" width="100px" required="true"  default="0"         />
    </params>
</plugin>
"""

# Plugin event functions ---------------------------------------------------




import Domoticz
import json
import urllib.parse as parse
import urllib.request as request
from datetime import datetime, timedelta
import time
import base64
import itertools
from distutils.version import LooseVersion

from DomoticzWrapper.DomoticzWrapper import \
    DeviceParam, DomoticzTypeName, DomoticzPluginParameter, DomoticzDebugLevel, DomoticzWrapper #, \
    #     DomoticzDevice as D, \
    #     DomoticzWrapper as Domoticz, \
    #     DomoticzParameters as Parameters, \
    #     DomoticzSettings as settings, \
    #     DomoticzDevices as Devices, \
    #     DomoticzImage as Image, \
    #     DomoticzImages as Images

d = DomoticzWrapper(Domoticz, Settings, Parameters, Images)

def onStart():
    d.DomoticzInstance.Debugging(DomoticzDebugLevel.ShowAll)  # (DL.ShowAll)
    d.DomoticzInstance.Status("Hello, World !")
    DumpConfigToLog()



# Plugin utility functions ---------------------------------------------------
def parseCSV(strCSV):
    listValues = []
    for value in strCSV.split(","):
        try:
            val = int(value)
        except:
            pass
        else:
            listValues.append(val)
    return listValues


def DomoticzAPI(APICall):
    resultJson = None
    url = "http://{}:{}/json.htm?{}".format(
        d.DomoticzParameters[DomoticzPluginParameter.Address], d.DomoticzParameters[DomoticzPluginParameter.Port], parse.quote(APICall, safe="&="))
    d.DomoticzInstance.Debug("Calling domoticz API: {}".format(url))
    try:
        req = request.Request(url)
        if d.DomoticzParameters[DomoticzPluginParameter.Username] != "":
            d.DomoticzInstance.Debug("Add authentication for user {}".format(
                d.DomoticzParameters["Username"]))
            credentials = ('%s:%s' %
                           (d.DomoticzParameters[DomoticzPluginParameter.Username], d.DomoticzParameters[DomoticzPluginParameter.Password]))
            encoded_credentials = base64.b64encode(credentials.encode('ascii'))
            req.add_header('Authorization', 'Basic %s' %
                           encoded_credentials.decode("ascii"))

        response = request.urlopen(req)
        if response.status == 200:
            resultJson = json.loads(response.read().decode('utf-8'))
            if resultJson["status"] != "OK":
                d.DomoticzInstance.Error("Domoticz API returned an error: status = {}".format(
                    resultJson["status"]))
                resultJson = None
        else:
            d.DomoticzInstance.Error(
                "Domoticz API: http error = {}".format(response.status))
    except:
        d.DomoticzInstance.Error("Error calling '{}'".format(url))
    return resultJson


def CheckParam(name, value, default):
    try:
        param = int(value)
    except ValueError:
        param = default
        d.DomoticzInstance.Error("Parameter '{}' has an invalid value of '{}' ! default of '{}' is instead used.".format(name, value, default))
    return param


# Generic helper functions
def DumpConfigToLog():
    for x in d.DomoticzParameters:
        if d.DomoticzParameters[x] != "":
            d.DomoticzInstance.Debug("'" + x + "':'" + str(d.DomoticzParameters[x]) + "'")
    d.DomoticzInstance.Debug("Device count: " + str(len(d.DomoticzDevices)))
    for x in d.DomoticzDevices:
        d.DomoticzInstance.Debug("Device:           " + str(x) + " - " + str(d.DomoticzDevices[x]))
        d.DomoticzInstance.Debug("Device ID:       '" + str(d.DomoticzDevices[x].ID) + "'")
        d.DomoticzInstance.Debug("Device Name:     '" + d.DomoticzDevices[x].Name + "'")
        d.DomoticzInstance.Debug("Device nValue:    " + str(d.DomoticzDevices[x].nValue))
        d.DomoticzInstance.Debug("Device sValue:   '" + d.DomoticzDevices[x].sValue + "'")
        d.DomoticzInstance.Debug("Device LastLevel: " + str(d.DomoticzDevices[x].LastLevel))
    return
