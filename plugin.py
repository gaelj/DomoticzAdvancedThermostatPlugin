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
    name="DAT"
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
        <param field="Mode1" label="Apply minimum heating per cycle" width="200px">
            <options>
				<option label="ony when heating required" value="Normal"  default="true" />
                <option label="always" value="Forced"/>
            </options>
        </param>
        <param field="Mode2" label="Calculation cycle, Minimum Heating time per cycle, Pause On delay, Pause Off delay, Forced mode duration (all in minutes)" width="200px" required="true" default="30,0,2,1,60"/>
        <param field="Mode3" label="Logging Level" width="200px">
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

# <param field="Mode1"    label="Inside Temperature Sensors, grouped by room (idx1, idx2...)"  width="300px" required="true"  default=""          />
# <param field="Mode2"    label="Outside Temperature Sensors (idx1, idx2...)"                  width="300px" required="true"  default=""          />
# <param field="Mode3"    label="Heating switch + Inside Radiator Setpoints, grouped by room (idx1, idx2...)"   width="300px" required="true"  default=""          />


import Domoticz
from datetime import datetime, timedelta
import time
from enum import IntEnum
global z
z = None


# 		116	AccuWeather	    0001	1	AccuWeather THB	Temp + Humidity + Baro	THB1 - BTHR918, BTHGN129	3.8 C, 79 %, 1017 hPa	-	-

# 		73	OpenZWave USB	1201	1	Temperature Vanne TV	    Temp	LaCrosse TX3	16.4 C	-
# 		45	OpenZWave USB	0E01	1	Temperature Vanne chambre	Temp	LaCrosse TX3	17.2 C	-
# 		37	OpenZWave USB	1001	1	Temperature Vanne rue	    Temp	LaCrosse TX3	14.3 C	-
# 		18	OpenZWave USB	0A01	1	Temperature Vanne palier	Temp	LaCrosse TX3	18.6 C	-
# 		6	OpenZWave USB	0801	1	Temperature Vanne bureau	Temp	LaCrosse TX3	21.5 C	-

#   	53	OpenZWave USB	0011201	1	Heating Vanne Canapé	Thermostat	SetPoint	16.0	-
# 		36	OpenZWave USB	0011001	1	Heating Vanne rue	    Thermostat	SetPoint	14.0	-
# 		34	OpenZWave USB	0000F01	1	Heating Vanne TV	    Thermostat	SetPoint	15.0	-	-
# 		32	OpenZWave USB	0000E01	1	Heating Vanne chambre	Thermostat	SetPoint	16.0	-
# 		17	OpenZWave USB	0000A01	1	Heating Vanne palier	Thermostat	SetPoint	17.5	-
# 		5	OpenZWave USB	0000801	1	Heating Vanne bureau	Thermostat	SetPoint	22.5	-

class PluginConfig:
    """Plugin configuration (singleton)"""

    def __init__(self):
        self.InsideTempSensorIdxs = {
            Rooms.Bedroom: [18, 45],     # palier , chambre
            Rooms.LivingRoom: [73, 37],  # Canapé, rue, (TV)
            Rooms.Desk: [6],             # Bureau
        }
        self.RadiatorSetpointsIdxs = {
            Rooms.Bedroom: [17, 32],
            Rooms.LivingRoom: [34, 36, 53],
            Rooms.Desk: [5],
        }
        self.ExteriorTempSensorsIdx = 116
        self.BoilerRelayIdx = 50


class DeviceUnits(IntEnum):
    """Unit numbers of each virtual switch"""
    ThermostatControl = 1
    ThermostatMode = 2
    Room1Presence = 3
    Room2Presence = 4


class Rooms(IntEnum):
    """Room types, each with a different heating configuration"""
    Bedroom = 0
    LivingRoom = 1
    Desk = 2


class VirtualSwitch:
    def __init__(self, pluginDeviceUnit: DeviceUnits):
        self.pluginDeviceUnit = pluginDeviceUnit
        self.value = None

    def SetValue(self, value):
        d.Devices[self.pluginDeviceUnit.value].Update(
            nValue=int(value), sValue=value)
        self.value = value

    def Read(self):
        self.sValue = d.Devices[self.pluginDeviceUnit.value].sValue


class Radiator:
    def __init__(self, radiatorType: Rooms, idxTemp, idxSetPoint):
        self.radiatorType = radiatorType
        self.idxTemp = idxTemp
        self.idxSetPoint = idxSetPoint
        self.measuredTemperature = None
        self.setPointTemperature = None

    def SetSetPoint(self, setPoint):
        self.setPointTemperature = setPoint

    def Read(self):
        pass


class RelayActuator:
    def __init__(self, idx):
        self.idx = idx
        self.state = None

    def SetState(self, state: bool):
        if self.state != state:
            command = "On" if state else "Off"
            self.state = state
            z.DomoticzAPI(
                "type=command&param=switchlight&idx={}&switchcmd={}".format(self.idx, command))

    def Read(self):
        pass


class OutsideWeather:
    def __init__(self, idx):
        self.idx = idx
        self.temperature = None

    def Read(self):
        pass


class PluginDevices:
    def __init__(self):
        self.config = PluginConfig()
        self.exterior = OutsideWeather(self.config.ExteriorTempSensorsIdx)
        self.boiler = RelayActuator(self.config.BoilerRelayIdx)
        self.radiators = []
        for radType in self.config.InsideTempSensorIdxs:
            tempIdxs = self.config.InsideTempSensorIdxs[radType]
            setPointIdxs = self.config.RadiatorSetpointsIdxs[radType]
            for i, tempIdx in enumerate(tempIdxs):
                setPointIdx = setPointIdxs[i]
                self.radiators.append(Radiator(radType, tempIdx, setPointIdx))

    def ReadTemperatures(self):
        global z
        devicesAPI = z.DomoticzAPI(
            "type=devices&filter=temp&used=true&order=Name")


def onStart():
    global z

    # dev
    # from DomoticzWrapper.DomoticzWrapperClass import \
    # prod
    from DomoticzWrapperClass import \
        DomoticzTypeName, DomoticzDebugLevel, DomoticzPluginParameters, \
        DomoticzWrapper, DomoticzDevice, DomoticzConnection, DomoticzImage, \
        DomoticzDeviceType, DomoticzDeviceTypes

    # dev
    # from DomoticzWrapper.DomoticzPluginHelper import \
    # prod
    from DomoticzPluginHelper import \
        DomoticzPluginHelper, DeviceParam, ParseCSV


    z = DomoticzPluginHelper(
        Domoticz, Settings, Parameters, Devices, Images, {})
    z.onStart()

    z.InitDevice('Thermostat Control', DeviceUnits.ThermostatControl,
                 DeviceType=DomoticzDeviceTypes.LightSwitch_Switch_Selector(),
                 Used=True,
                 Options={"LevelActions": "||||",
                          "LevelNames": "Off|Away|Night|Auto|Forced",
                          "LevelOffHidden": "false",
                          "SelectorStyle": "0"},
                 defaultNValue=0,
                 defaultSValue="0")

    z.InitDevice('Thermostat Mode', DeviceUnits.ThermostatMode,
                 DeviceType=DomoticzDeviceTypes.LightSwitch_Switch_Selector(),
                 Used=True,
                 Options={"Leve__dActions": "||",
                          "LevelNames": "Off|Normal|Comfort",
                          "LevelOffHidden": "false",
                          "SelectorStyle": "0"},
                 defaultNValue=0,
                 defaultSValue="10")

    z.InitDevice('Room 1 Presence', DeviceUnits.Room1Presence,
                 DeviceType=DomoticzDeviceTypes.LightSwitch_Switch_Selector(),
                 Used=True,
                 Options={"LevelActions": "|",
                          "LevelNames": "Absent|Present",
                          "LevelOffHidden": "false",
                          "SelectorStyle": "0"},
                 defaultNValue=0,
                 defaultSValue="0")

    z.InitDevice('Room 2 Presence', DeviceUnits.Room2Presence,
                 DeviceType=DomoticzDeviceTypes.LightSwitch_Switch_Selector(),
                 Used=True,
                 Options={"LevelActions": "|",
                          "LevelNames": "Absent|Present",
                          "LevelOffHidden": "false",
                          "SelectorStyle": "0"},
                 defaultNValue=0,
                 defaultSValue="0")


def onStop():
    global z
    z.onStop()


def onCommand(Unit, Command, Level, Color):
    global z
    z.onCommand(Unit, Command, Level, Color)


def onHeartbeat():
    global z
    z.onHeartbeat()
    now = datetime.now()
