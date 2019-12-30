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
    key="GaelJDomoticzAdvancedThermostat"
    name="GDAT"
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
            <li>Normal</li>
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
            <li>Thermostat Control: Off|Away|Night|Normal|Comfort</li>
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
z = None
pluginDevices = None


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
            Rooms.Bedroom: [45],         # chambre
            Rooms.Landing: [18],         # palier
            Rooms.LivingRoom: [73, 37],  # Canapé, rue, (TV)
            Rooms.Desk: [6],             # Bureau
        }
        self.RadiatorSetpointsIdxs = {
            Rooms.Bedroom: [32],
            Rooms.Landing: [17],
            Rooms.LivingRoom: [34, 36, 53],
            Rooms.Desk: [5],
        }
        self.RoomIndexes = {
            Rooms.Bedroom: 0,         # chambre
            Rooms.Landing: 2,         # palier
            Rooms.LivingRoom: 1,  # Canapé, rue, (TV)
            Rooms.Desk: 2,
        }
        self.ExteriorTempSensorsIdx = 116
        self.BoilerRelayIdx = 50

        self.ExpectedTemps = {
            ThermostatControlValues.Off: {
                Rooms.Bedroom: [15],
                Rooms.Landing: [17],
                Rooms.LivingRoom: [14, 13, 14],
                Rooms.Desk: [15], },
            ThermostatControlValues.Away: {
                Rooms.Bedroom: [15],
                Rooms.Landing: [17],
                Rooms.LivingRoom: [14, 13, 14],
                Rooms.Desk: [15], },
            ThermostatControlValues.Night: {
                Rooms.Bedroom: [16],
                Rooms.Landing: [16],
                Rooms.LivingRoom: [15, 14, 15],
                Rooms.Desk: [16], },
            ThermostatControlValues.Normal: {
                Rooms.Bedroom: [16],
                Rooms.Landing: [18],
                Rooms.LivingRoom: [19, 17, 19],
                Rooms.Desk: [21], },
            ThermostatControlValues.Comfort: {
                Rooms.Bedroom: [16],
                Rooms.Landing: [18],
                Rooms.LivingRoom: [20, 17, 20],
                Rooms.Desk: [22], },
        }


class DeviceUnits(IntEnum):
    """Unit numbers of each virtual switch"""
    ThermostatControl = 1
    Room1Presence = 2
    Room2Presence = 3


class Rooms(IntEnum):
    """Room types, each with a different heating configuration"""
    Bedroom = 0
    LivingRoom = 1
    Desk = 2
    Landing = 3


class ThermostatControlValues(IntEnum):
    Off = 0
    Away = 10
    Night = 20
    Normal = 30
    Comfort = 40


class PresenceValues(IntEnum):
    Absent = 0
    Present = 10


class VirtualSwitch:
    """Virtual switch, On/Off or multi-position"""

    def __init__(self, pluginDeviceUnit: DeviceUnits):
        global z
        global pluginDevices
        self.pluginDeviceUnit = pluginDeviceUnit
        self.value = None

    def SetValue(self, value):
        global z
        global pluginDevices
        nValue = 1 if int(value) > 0 else 0
        if value in (0, 1):
            sValue = ""
        else:
            sValue = str(value)
        z.Devices[self.pluginDeviceUnit.value].Update(
            nValue=nValue, sValue=sValue)
        self.value = value

    def Read(self):
        global z
        global pluginDevices
        d = z.Devices[self.pluginDeviceUnit.value]
        self.value = int(d.sValue) if d.sValue is not None and d.sValue != "" else int(
            d.nValue) if d.nValue is not None else None
        return self.value


class Radiator:
    """Radiator thermostat setpoint and temperature readout"""

    def __init__(self, radiatorType: Rooms, idxTemp, idxSetPoint, expectedTemps):
        global z
        global pluginDevices
        self.radiatorType = radiatorType
        self.idxTemp = idxTemp
        self.idxSetPoint = idxSetPoint
        self.measuredTemperature = None
        self.setPointTemperature = None
        self.expectedTemps = expectedTemps

    def SetValue(self, setPoint):
        global z
        global pluginDevices
        if self.setPointTemperature != setPoint:
            self.setPointTemperature = setPoint
            z.DomoticzAPI("type=setused&idx={}&setpoint={}&used=true".format(
                self.idxSetPoint, setPoint))

    @classmethod
    def ReadAll(cls):
        global z
        global pluginDevices
        radiators = pluginDevices.radiators
        devicesAPI = z.DomoticzAPI(
            "type=devices&filter=temp&used=true&order=Name")
        if devicesAPI:
            for device in devicesAPI["result"]:
                idx = int(device["idx"])
                if idx in [r.idxTemp for r in radiators]:
                    radiator = [r for r in radiators if r.idxTemp == idx][0]
                    if "Temp" in device:
                        Domoticz.Debug(
                            "device: {}-{} = {}".format(device["idx"], device["Name"], device["Temp"]))
                        # check temp sensor is not timed out
                        if not z.SensorTimedOut(idx, device["Name"], device["LastUpdate"]):
                            radiator.measuredTemperature = device["Temp"]
                            z.WriteLog(
                                "Radiator temp " + device["Name"] + ": " + str(device["Temp"]))
                    else:
                        Domoticz.Error(
                            "device: {}-{} is not a Temperature sensor".format(device["idx"], device["Name"]))


class RelayActuator:
    """On/Off relay actuator"""

    def __init__(self, idx):
        global z
        global pluginDevices
        self.idx = idx
        self.state = None

    def SetValue(self, state: bool):
        global z
        global pluginDevices
        if self.Read() != state:
            command = "On" if state else "Off"
            self.state = state
            z.DomoticzAPI(
                "type=command&param=switchlight&idx={}&switchcmd={}".format(self.idx, command))

    def Read(self):
        global z
        global pluginDevices
        devicesAPI = z.DomoticzAPI(
            "type=devices&filter=light&used=true&order=Name")
        if devicesAPI:
            for device in devicesAPI["result"]:
                idx = int(device["idx"])
                if idx != self.idx:
                    continue
                if "Status" in device:
                    self.state = device["Status"] == "On"
        return self.state


class OutsideWeather:
    def __init__(self, idx):
        self.idx = idx
        self.temperature = None

    def Read(self):
        return self.temperature


class PluginDevices:
    def __init__(self):
        self.config = PluginConfig()
        self.exterior = OutsideWeather(self.config.ExteriorTempSensorsIdx)
        self.boiler = RelayActuator(self.config.BoilerRelayIdx)
        self.radiators = []
        expectedTemps = self.config.ExpectedTemps
        for radType in self.config.InsideTempSensorIdxs:
            tempIdxs = self.config.InsideTempSensorIdxs[radType]
            setPointIdxs = self.config.RadiatorSetpointsIdxs[radType]
            for i, tempIdx in enumerate(tempIdxs):
                setPointIdx = setPointIdxs[i]
                radiatorExpectedTemps = {}
                for controlValue in expectedTemps:
                    radiatorExpectedTemps[controlValue] = expectedTemps[controlValue][radType][i]
                self.radiators.append(Radiator(
                    radType, tempIdx, setPointIdx, radiatorExpectedTemps))
        self.switches = dict([(du, VirtualSwitch(du)) for du in DeviceUnits])
        self.thermostatControlSwitch = self.switches[DeviceUnits.ThermostatControl]
        self.room1PresenceSwitch = self.switches[DeviceUnits.Room1Presence]
        self.room2PresenceSwitch = self.switches[DeviceUnits.Room2Presence]

    def ReadTemperatures(self):
        global z
        global pluginDevices
        Radiator.ReadAll()
        self.exterior.Read()


def ApplySetPoints():
    global z
    global pluginDevices

    thermostatControlValue = pluginDevices.thermostatControlSwitch.Read()
    room1PresenceValue = pluginDevices.room1PresenceSwitch.Read()
    room2PresenceValue = pluginDevices.room2PresenceSwitch.Read()

    z.WriteLog("thermostatControlValue: " + str(thermostatControlValue))
    z.WriteLog("room1PresenceValue: " + str(room1PresenceValue))
    z.WriteLog("room2PresenceValue: " + str(room2PresenceValue))

    thermostatControlValue = ThermostatControlValues(
        thermostatControlValue) if thermostatControlValue is not None else None
    room1PresenceValue = PresenceValues(
        room1PresenceValue) if room1PresenceValue is not None else None
    room2PresenceValue = PresenceValues(
        room2PresenceValue) if room2PresenceValue is not None else None

    if thermostatControlValue is not None:
        for radiator in pluginDevices.radiators:
            ri = pluginDevices.config.RoomIndexes[radiator.radiatorType]
            if ri == 1:
                if room1PresenceValue or int(thermostatControlValue) < 30:
                    setPoint = radiator.expectedTemps[thermostatControlValue]
                else:
                    setPoint = radiator.expectedTemps[ThermostatControlValues.Away]
            elif ri == 2:
                if room2PresenceValue or int(thermostatControlValue) < 30:
                    setPoint = radiator.expectedTemps[thermostatControlValue]
                else:
                    setPoint = radiator.expectedTemps[ThermostatControlValues.Away]
            else:
                setPoint = radiator.expectedTemps[thermostatControlValue]
            radiator.SetValue(setPoint)
    else:
        z.WriteLog("thermostatControlValue is None")


def Regulate():
    global z
    global pluginDevices

    now = datetime.now()
    pluginDevices.ReadTemperatures()
    boilerCommand = pluginDevices.boiler.state

    if boilerCommand is None:
        boilerCommand = False

    # radiator: Radiator
    thermostatControlValue = pluginDevices.thermostatControlSwitch.Read()
    z.WriteLog("ThermostatControlValue: " + str(thermostatControlValue))
    thermostatControlValue = ThermostatControlValues(
        int(thermostatControlValue))
    if thermostatControlValue == ThermostatControlValues.Off:
        pluginDevices.boiler.SetValue(False)
    else:
        underTempRads = [
            r for r in pluginDevices.radiators if r.measuredTemperature is not None and r.setPointTemperature is not None and int(r.measuredTemperature) < (int(r.setPointTemperature) - 1)]
        overTempRads = [r for r in pluginDevices.radiators if r.measuredTemperature is not None and r.setPointTemperature is not None and int(r.measuredTemperature) >= int(
            r.setPointTemperature)]
        for rad in underTempRads:
            z.WriteLog("Under-temp radiator: " + rad.radiatorType.name)
        for rad in overTempRads:
            z.WriteLog("Over-temp radiator: " + rad.radiatorType.name)
        if not boilerCommand and len(underTempRads) > 0:
            pluginDevices.boiler.SetValue(True)
        elif boilerCommand and len(overTempRads) > 0 and len(underTempRads) == 0:
            pluginDevices.boiler.SetValue(False)


def onStart():
    global z
    global pluginDevices
    # prod
    # from DomoticzWrapperClass import \
    # dev
    # from DomoticzWrapper.DomoticzWrapperClass import \
    #     DomoticzTypeName, DomoticzDebugLevel, DomoticzPluginParameters, \
    #     DomoticzWrapper, DomoticzDevice, DomoticzConnection, DomoticzImage, \
    #     DomoticzDeviceType

    # dev
    # from DomoticzWrapper.DomoticzPluginHelper import \
    # prod
    from DomoticzPluginHelper import \
        DomoticzPluginHelper, DeviceParam, ParseCSV, DomoticzDeviceTypes

    z = DomoticzPluginHelper(
        Domoticz, Settings, Parameters, Devices, Images, {})
    z.onStart(3)

    LightSwitch_Switch_Selector = DomoticzDeviceTypes.LightSwitch_Switch_Selector()

    z.InitDevice('Thermostat Control', DeviceUnits.ThermostatControl,
                 DeviceType=LightSwitch_Switch_Selector,
                 Used=True,
                 Options={"LevelActions": "||||",
                          "LevelNames": "Off|Away|Night|Normal|Comfort",
                          "LevelOffHidden": "false",
                          "SelectorStyle": "0"},
                 defaultNValue=0,
                 defaultSValue="0")

    z.InitDevice('Room 1 Presence', DeviceUnits.Room1Presence,
                 DeviceType=LightSwitch_Switch_Selector,
                 Used=True,
                 Options={"LevelActions": "|",
                          "LevelNames": "Absent|Present",
                          "LevelOffHidden": "false",
                          "SelectorStyle": "0"},
                 defaultNValue=0,
                 defaultSValue="0")

    z.InitDevice('Room 2 Presence', DeviceUnits.Room2Presence,
                 DeviceType=LightSwitch_Switch_Selector,
                 Used=True,
                 Options={"LevelActions": "|",
                          "LevelNames": "Absent|Present",
                          "LevelOffHidden": "false",
                          "SelectorStyle": "0"},
                 defaultNValue=0,
                 defaultSValue="0")

    pluginDevices = PluginDevices()
    ApplySetPoints()


def onStop():
    global z
    global pluginDevices
    z.onStop()


def onCommand(Unit, Command, Level, Color):
    global z
    global pluginDevices
    z.onCommand(Unit, Command, Level, Color)
    if Command == "On":
        value = 1
    elif Command == "Off":
        value = 0
    else:
        value = Level
    du = DeviceUnits(Unit)
    pluginDevices.switches[du].SetValue(value)
    ApplySetPoints()
    Regulate()


def onHeartbeat():
    global z
    global pluginDevices
    z.onHeartbeat()
    Regulate()
