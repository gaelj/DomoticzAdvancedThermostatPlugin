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
            <li>forced</li>
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
            <li>Thermostat Control: Off|Away|Night|Auto|Forced</li>
            <li>Thermostat Mode: Off|Normal|Comfort</li>
            <li>Room 1 Presence: Absent|Present</li>
            <li>Room 2 Presence: Absent|Present</li>
        </ul>

        <h3>Configuration</h3>
        Configuration options...
    </description>

    <params>
        <param field="Address"  label="Domoticz IP Address"                                          width="200px" required="true"  default="localhost" />
        <param field="Port"     label="Port"                                                         width="40px"  required="true"  default="8080"      />
        <param field="Username" label="Username"                                                     width="200px" required="false" default=""          />
        <param field="Password" label="Password"                                                     width="200px" required="false" default=""          />
        <param field="Mode1"    label="Inside Temperature Sensors, grouped by room (idx1, idx2...)"                   width="300px" required="true"  default=""          />
        <param field="Mode2"    label="Outside Temperature Sensors (idx1, idx2...)"                  width="300px" required="true"  default=""          />
        <param field="Mode3"    label="Heating switch + Inside Radiator Setpoints, grouped by room (idx1, idx2...)"   width="300px" required="true"  default=""          />
        <param field="Mode4" label="Apply minimum heating per cycle" width="200px">
            <options>
				<option label="ony when heating required" value="Normal"  default="true" />
                <option label="always" value="Forced"/>
            </options>
        </param>
        <param field="Mode5" label="Calculation cycle, Minimum Heating time per cycle, Pause On delay, Pause Off delay, Forced mode duration (all in minutes)" width="200px" required="true" default="30,0,2,1,60"/>
        <param field="Mode6" label="Logging Level" width="200px">
            <options>
                <option label="Normal" value="Normal" default="true"/>
                <option label="Verbose" value="Verbose"/>
                <option label="Debug - Python Only" value="2"/>
                <option label="Debug - Basic" value="62"/>
                <option label="Debug - Basic+Messages" value="126"/>
                <option label="Debug - Connections Only" value="16"/>
                <option label="Debug - Connections+Queue" value="144"/>
                <option label="Debug - All" value="-1"/>
            </options>
        </param>
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
        DomoticzWrapper, DomoticzDevice, DomoticzConnection, DomoticzImage, \
        DomoticzDeviceType, DomoticzDeviceTypes

    from DomoticzPluginHelper import DomoticzPluginHelper, DeviceParam, ParseCSV

    d = DomoticzWrapper(Domoticz, Settings, Parameters, Devices, Images)
    z = DomoticzPluginHelper(d, {})
    z.onStart()
    z.InitDevice('Thermostat Control', 1,
                 DeviceType=DomoticzDeviceTypes.LightSwitch_Switch_Selector(),
                 Used=True,
                 Options={"LevelActions": "||||",
                          "LevelNames": "Off|Away|Night|Auto|Forced",
                          "LevelOffHidden": "false",
                          "SelectorStyle": "0"})
    z.InitDevice('Thermostat Mode', 2,
                 DeviceType=DomoticzDeviceTypes.LightSwitch_Switch_Selector(),
                 Used=True,
                 Options={"LevelActions": "||",
                          "LevelNames": "Off|Normal|Comfort",
                          "LevelOffHidden": "false",
                          "SelectorStyle": "0"})
    z.InitDevice('Room 1 Presence', 3,
                 DeviceType=DomoticzDeviceTypes.LightSwitch_Switch_Selector(),
                 Used=True,
                 Options={"LevelActions": "|",
                          "LevelNames": "Absent|Present",
                          "LevelOffHidden": "false",
                          "SelectorStyle": "0"})
    z.InitDevice('Room 2 Presence', 4,
                 DeviceType=DomoticzDeviceTypes.LightSwitch_Switch_Selector(),
                 Used=True,
                 Options={"LevelActions": "|",
                          "LevelNames": "Absent|Present",
                          "LevelOffHidden": "false",
                          "SelectorStyle": "0"})


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
    global d
    z.onHeartbeat()
