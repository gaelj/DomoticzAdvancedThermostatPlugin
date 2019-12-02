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


import Domoticz
from datetime import datetime, timedelta
import time
global z
global d
z = None
d = None


def onStart():
    global z
    global d

    from DomoticzWrapperClass import \
        DomoticzTypeName, DomoticzDebugLevel, DomoticzPluginParameters, \
        DomoticzWrapper, DomoticzDevice, DomoticzConnection, DomoticzImage

    from DomoticzPluginHelper import DomoticzPluginHelper, DeviceParam, ParseCSV

    d = DomoticzWrapper(Domoticz, Settings, Parameters, Devices, Images)
    z = DomoticzPluginHelper(d, {})
    z.onStart()


def onStop():
    global z
    global d
    z.onStop()


def onCommand(Unit, Command, Level, Color):
    global z
    global d
    z.onCommand(Unit, Command, Level, Color)


def onHeartbeat():
    global z
    z.onHeartbeat()
