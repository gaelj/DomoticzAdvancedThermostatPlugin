"""Wrapper for the Domoticz plugin API.
Based on information in https://www.domoticz.com/wiki/Developing_a_Python_plugin as of git commit dates
"""

from enum import Enum, IntEnum
from typing import List, Dict
from datetime import datetime, timedelta
import time


class DomoticzDebugLevel(IntEnum):
    """Domoticz debug level mask values

    Arguments:
    - Enum {ShowNone} -- All Python and framework debugging is disabled.
    - Enum {ShowAll} -- Very verbose log from plugin framework and plugin debug messages.
    - Enum {DebugFuncCalls} -- Mask value. Shows messages from Plugin Domoticz.Debug() calls only.
    - Enum {DebugHighLevelMessages} -- Mask Value. Shows high level framework messages only about major the plugin.
    - Enum {DebugDevices} -- Mask value. Shows plugin framework debug messages related to Devices objects.
    - Enum {DebugConnections} -- Mask value. Shows plugin framework debug messages related to Connections objects.
    - Enum {DebugImages} -- Mask value. Shows plugin framework debug messages related to Images objects.
    - Enum {DumpData} -- Mask value. Dumps contents of inbound and outbound data from Connection objects.
    - Enum {DebugMessageQueue} -- Mask value. Shows plugin framework debug messages related to the message queue.
    """
    ShowNone = 0
    ShowAll = 1
    DebugFuncCalls = 2
    DebugHighLevelMessages = 4
    DebugDevices = 8
    DebugConnections = 16
    DebugImages = 32
    DumpData = 64
    DebugMessageQueue = 128


class DomoticzPluginParameters:
    """Domoticz parameter values

    Arguments:
    - Enum {Key} -- Unique short name for the plugin, matches python filename.
    - Enum {HomeFolder} -- Folder or directory where the plugin was run from.
    - Enum {Author} -- Plugin Author.
    - Enum {Version} -- Plugin version.
    - Enum {Address} -- IP Address, used during connection.
    - Enum {Port} -- IP Port, used during connection.
    - Enum {Username} -- Username.
    - Enum {Password} -- Password.
    - Enum {Mode1} -- General Parameter 1
    - Enum {Mode2} -- General Parameter 2
    - Enum {Mode3} -- General Parameter 3
    - Enum {Mode4} -- General Parameter 4
    - Enum {Mode5} -- General Parameter 5
    - Enum {Mode6} -- General Parameter 6
    - Enum {SerialPort} -- SerialPort, used when connecting to Serial Ports.
    """

    def __init__(self, parameters: Dict[str, str]):
        self.Key = ''
        self.HomeFolder = ''
        self.Author = ''
        self.Version = ''
        self.Address = ''
        self.Port = ''
        self.Username = ''
        self.Password = ''
        self.Mode1 = ''
        self.Mode2 = ''
        self.Mode3 = ''
        self.Mode4 = ''
        self.Mode5 = ''
        self.Mode6 = ''
        self.SerialPort = ''
        for x in parameters:
            try:
                setattr(self, x, parameters[x])
            except:
                pass

    @property
    def Modes(self):
        return {
            1: self.Mode1,
            2: self.Mode2,
            3: self.Mode3,
            4: self.Mode4,
            5: self.Mode5,
            6: self.Mode6,
        }
        # if modeIndex == 1:
        #     return self.Mode1
        # elif modeIndex == 2:
        #     return self.Mode2
        # elif modeIndex == 3:
        #     return self.Mode3
        # elif modeIndex == 4:
        #     return self.Mode4
        # elif modeIndex == 5:
        #     return self.Mode5
        # elif modeIndex == 6:
        #     return self.Mode6


class DomoticzTypeName(Enum):
    AirQuality = "AirQuality"
    Alert = "Alert"
    Barometer = "Barometer"
    CounterIncremental = "CounterIncremental"
    Contact = "Contact"
    CurrentAmpere = "CurrentAmpere"
    CurrentSingle = "CurrentSingle"
    Custom = "Custom"
    Dimmer = "Dimmer"
    Distance = "Distance"
    Gas = "Gas"
    Humidity = "Humidity"
    Illumination = "Illumination"
    kWh = "kWh"
    LeafWetness = "LeafWetness"
    Motion = "Motion"
    Percentage = "Percentage"
    PushOn = "PushOn"
    PushOff = "PushOff"
    Pressure = "Pressure"
    Rain = "Rain"
    SelectorSwitch = "SelectorSwitch"
    SoilMoisture = "SoilMoisture"
    SolarRadiation = "SolarRadiation"
    SoundLevel = "SoundLevel"
    Switch = "Switch"
    Temperature = "Temperature"
    TempHum = "TempHum"
    TempHumBaro = "TempHumBaro"
    Text = "Text"
    Usage = "Usage"
    UV = "UV"
    Visibility = "Visibility"
    Voltage = "Voltage"
    Waterflow = "Waterflow"
    Wind = "Wind"
    WindTempChill = "WindTempChill"


class DomoticzDevice:
    pass


class DomoticzConnection:
    pass


class DomoticzImage:
    pass


class DomoticzDeviceType:
    """Domoticz Device Type definition"""

    def __init__(self,
                 type_id: int,
                 subtype_id: int = None,
                 switchtype_id: int = None):
        self.type_id = type_id
        self.subtype_id = subtype_id
        self.switchtype_id = switchtype_id


class DomoticzDeviceTypes:
    pass


class DomoticzWrapper:
    def __init__(self, _Domoticz, _Settings, _Parameters, _Devices, _Images):
        self.__Domoticz = _Domoticz
        self.__Settings = _Settings
        self.__Parameters = _Parameters
        self.__Devices = _Devices
        self.__Images = _Images

    @property
    def Domoticz(self):
        return self.__Domoticz

    @property
    def Settings(self) -> Dict[str, str]:
        """Contents of the Domoticz Settings page as found in the Preferences database table. These are always available and will be updated if the user changes any settings. The plugin is not restarted. They can be accessed by name for example: Settings["Language"]

        Returns:
            Dict[str, str] -- Contents of the Domoticz Settings page as found in the Preferences database table. These are always available and will be updated if the user changes any settings. The plugin is not restarted. They can be accessed by name for example: Settings["Language"]
        """
        return self.__Settings

    @property
    def ParametersDict(self) -> Dict[str, str]:
        """These are always available and remain static for the lifetime of the plugin. They can be accessed by name for example: Parameters["SerialPort"]

        Returns:
            Dict[str, str] -- These are always available and remain static for the lifetime of the plugin. They can be accessed by name for example: Parameters["SerialPort"]
        """
        # return dict([(str(k), self.__Parameters[k]) for k in self.__Parameters])
        return self.__Parameters

    @property
    def Parameters(self) -> DomoticzPluginParameters:
        return DomoticzPluginParameters(self.__Parameters)

    @property
    def Devices(self) -> Dict[int, DomoticzDevice]:
        """Dictionary of device ids to device objects

        Returns:
            Dict[int, DomoticzDevice] -- Dictionary of device ids to device objects
        """
        return dict([(k, DomoticzDevice(Device=self.__Devices[k])) for k in self.__Devices])

    @property
    def Images(self) -> Dict[str, DomoticzImage]:
        """Available images"""
        return dict([(k, DomoticzImage(Image=self.__Images[k])) for k in self.__Images])

    # @property
    # def x(self) -> str:
    #     return Domoticz.x

    # @x.setter
    # def x(self, val):
    #     Domoticz.x = val

    def Debug(self, val: str):
        """Write a message to Domoticz log only if verbose logging is turned on.

        Arguments:
            val {str} -- Message to log
        """
        self.__Domoticz.Debug(val)

    def Log(self, val: str):
        """Write a message to Domoticz log

        Arguments:
            val {str} -- Message to log
        """
        self.__Domoticz.Log(val)

    def Status(self, val: str):
        """Write a status message to Domoticz log

        Arguments:
            val {str} -- Message to log
        """
        self.__Domoticz.Status(val)

    def Error(self, val: str):
        """Write an error message to Domoticz log

        Arguments:
            val {str} -- Message to log
        """
        self.__Domoticz.Error(val)

    def Debugging(self, values: List[DomoticzDebugLevel]):
        """Set logging level and type for debugging. Multiple values are supported.
        Mask values can be added together, for example to see debugging details around the plugin and its objects use: Domoticz.Debugging(62) # 2+4+8+16+32

        Arguments:
            values {List[DomoticzDebugLevel]} -- List of debug levels to logically-OR together
        """
        if values is int:
            self.__Domoticz.Debugging(values)
        elif values is DomoticzDebugLevel:
            self.__Domoticz.Debugging(values.value)
        elif DomoticzDebugLevel.ShowNone in values:
            self.__Domoticz.Debugging(0)
        elif DomoticzDebugLevel.ShowNone in values:
            self.__Domoticz.Debugging(1)
        else:
            self.__Domoticz.Debugging(sum([v.value for v in values]))

    def Heartbeat(self, val: int):
        """Set the heartbeat interval in seconds, default 10 seconds.
        Values greater than 30 seconds will cause a message to be regularly logged about the plugin not responding. The plugin will actually function correctly with values greater than 30 though.

        Arguments:
            val {int} -- Heartbeat interval in seconds
        """
        self.__Domoticz.Heartbeat(val)

    def Notifier(self, name: str):
        """Informs the plugin framework that the plugin's external hardware can consume Domoticz Notifications.
        When the plugin is active the supplied Name will appear as an additional target for Notifications in the standard Domoticz device notification editing page. The plugin framework will then call the onNotification callback when a notifiable event occurs.

        Arguments:
            name {str} -- Domoticz Notifications target name
        """
        self.__Domoticz.Notifier(name)

    def Trace(self, val: bool = False):
        """When True, Domoticz will log line numbers of the lines being executed by the plugin. Calling Trace again with False will suppress line level logging. Usage:
        ```
        def onHeartBeat():
        Domoticz.Trace(True)
        Domoticz.Log("onHeartBeat called")
        ...
        Domoticz.Trace(False)
        ```

        Keyword Arguments:
            val {bool} -- Trace setting (default: {False})
        """
        self.__Domoticz.Trace(val)

    def Configuration(self, val: Dict[str, str] = None) -> Dict[str, str]:
        """Returns a dictionary containing the plugin's configuration data that was previously stored. If a Dictionary paramater is supplied the database will be updated with the new configuration data.
        Values in the dictionary can be of types: String, Long, Float, Boolean, Bytes, ByteArray, List or Dictionary. Tuples can be specified but will be returned as a List.
        Configuration should not be confused with the Parameters dictionary. Parameters are set via the Hardware page and are read-only to the plugin, Configuration allows the plugin store structured data in the database rather than writing files or creating Domoticz variables to hold it.
        Usage:

        ```
        # Configuration Helpers
        def getConfigItem(Key=None, Default={}):
            Value = Default
            try:
                Config = Domoticz.Configuration()
                if (Key != None):
                    Value = Config[Key] # only return requested key if there was one
                else:
                    Value = Config      # return the whole configuration if no key
            except KeyError:
                Value = Default
            except Exception as inst:
                Domoticz.Error("Domoticz.Configuration read failed: '"+str(inst)+"'")
            return Value

        def setConfigItem(Key=None, Value=None):
            Config = {}
            try:
                Config = Domoticz.Configuration()
                if (Key != None):
                    Config[Key] = Value
                else:
                    Config = Value  # set whole configuration if no key specified
                Config = Domoticz.Configuration(Config)
            except Exception as inst:
                Domoticz.Error("Domoticz.Configuration operation failed: '"+str(inst)+"'")
            return Config
        ```

        Keyword Arguments:
            val {Dict[str, str]} -- Configuration to write (default: {None})

        Returns:
            Dict[str, str] -- Resulting configuration object
        """
        return self.__Domoticz.Configuration(val)


class DomoticzDevice:
    """A Domoticz Device"""

    def __init__(self, d: DomoticzWrapper = None,
                 Name: str = None, Unit: int = None,
                 DeviceType: DomoticzDeviceType = None,
                 TypeName: DomoticzTypeName = None,
                 Used: bool = False,
                 Options: Dict[str, str] = None,
                 Image: int = None,
                 Device=None):
        """Creator

        Arguments:
        - Name {str} -- Is appended to the Hardware name to set the initial Domoticz Device name.
        This should not be used in Python because it can be changed in the Web UI.
        - Unit {int} -- Plugin index for the Device. This can not change and should be used reference Domoticz devices associated with the plugin. This is also the key for the Devices Dictionary that Domoticz prepopulates for the plugin.
        Unit numbers must be less than 256.

            Keyword Arguments:
        - DeviceType {DomoticzDeviceType} -- DomoticzDeviceType
        - TypeName {DomoticzTypeName} -- Common device types, this will set the values for Type, Subtype and Switchtype. (default: {None})
        - Image {int} -- Set the image number to be used with the device. Only required to override the default.
        All images available by JSON API call "/json.htm?type=custom_light_icons" (default: {None})
        - Options {Dict[str, str]} -- Set the Device Options field. A few devices, like Selector Switches, require additional details to be set in this field. It is a Python dictionary consisting of key values pairs, where the keys and values must be strings. See the example to the right. (default: {None})
        - Used {bool} -- Set the Device Used field. Used devices appear in the appropriate tab(s), unused devices appear only in the Devices page and must be manually marked as Used. (default: {False})
        - DeviceID {str} -- Set the DeviceID to be used with the device. Only required to override the default which is an eight digit number dervice from the HardwareID and the Unit number in the format "000H000U".
        Field type is Varchar(25) (default: {None})
        """
        if Device is not None:
            self._Device = Device
        elif DeviceType is None and TypeName is not None:
            if Image is None:
                self._Device = d.Domoticz.Device(Name=Name, Unit=Unit, TypeName=TypeName.value,
                                                 Options=Options, Used=1 if Used else 0)
            else:
                self._Device = d.Domoticz.Device(Name=Name, Unit=Unit, TypeName=TypeName.value,
                                                 Image=Image, Options=Options, Used=1 if Used else 0)
        else:
            if DeviceType.subtype_id is None:
                if Image is None:
                    self._Device = d.Domoticz.Device(Name=Name, Unit=Unit,
                                                     Type=DeviceType.type_id,
                                                     Options=Options, Used=1 if Used else 0)
                else:
                    self._Device = d.Domoticz.Device(Name=Name, Unit=Unit,
                                                     Type=DeviceType.type_id,
                                                     Image=Image, Options=Options, Used=1 if Used else 0)
            elif DeviceType.switchtype_id is None:
                if Image is None:
                    self._Device = d.Domoticz.Device(Name=Name, Unit=Unit,
                                                     Type=DeviceType.type_id, Subtype=DeviceType.subtype_id,
                                                     Options=Options, Used=1 if Used else 0)
                else:
                    self._Device = d.Domoticz.Device(Name=Name, Unit=Unit,
                                                     Type=DeviceType.type_id, Subtype=DeviceType.subtype_id,
                                                     Image=Image, Options=Options, Used=1 if Used else 0)
            else:
                if Image is None:
                    self._Device = d.Domoticz.Device(Name=Name, Unit=Unit,
                                                     Type=DeviceType.type_id, Subtype=DeviceType.subtype_id, Switchtype=DeviceType.switchtype_id,
                                                     Options=Options, Used=1 if Used else 0)
                else:
                    self._Device = d.Domoticz.Device(Name=Name, Unit=Unit,
                                                     Type=DeviceType.type_id, Subtype=DeviceType.subtype_id, Switchtype=DeviceType.switchtype_id,
                                                     Image=Image, Options=Options, Used=1 if Used else 0)

    # def __init__(self, d: DomoticzWrapper,
    #              Name: str, Unit: int,
    #              Type: int = None, Subtype: int = None, Switchtype: int = None,
    #              Image: int = None,
    #              Options: Dict[str, str] = None,
    #              Used: bool = False,
    #              DeviceID: str = None):
    #     """Creator

    #     Arguments:
    #     - Name {str} -- Is appended to the Hardware name to set the initial Domoticz Device name.
    #     This should not be used in Python because it can be changed in the Web UI.
    #     - Unit {int} -- Plugin index for the Device. This can not change and should be used reference Domoticz devices associated with the plugin. This is also the key for the Devices Dictionary that Domoticz prepopulates for the plugin.
    #     Unit numbers must be less than 256.

    #         Keyword Arguments:
    #     - Type {int} -- Directly set the numeric Type value. Should only be used if the Device to be created is not supported by TypeName. (default: {None})
    #     - Subtype {int} -- Directly set the numeric Subtype value. Should only be used if the Device to be created is not supported by TypeName. (default: {None})
    #     - Switchtype {int} -- Directly set the numeric Switchtype value. Should only be used if the Device to be created is not supported by TypeName. (default: {None})
    #     - Image {int} -- Set the image number to be used with the device. Only required to override the default.
    #     All images available by JSON API call "/json.htm?type=custom_light_icons" (default: {None})
    #     - Options {Dict[str, str]} -- Set the Device Options field. A few devices, like Selector Switches, require additional details to be set in this field. It is a Python dictionary consisting of key values pairs, where the keys and values must be strings. See the example to the right. (default: {None})
    #     - Used {bool} -- Values
    #     0 (default) Unused
    #     1 Used.
    #     Set the Device Used field. Used devices appear in the appropriate tab(s), unused devices appear only in the Devices page and must be manually marked as Used. (default: {False})
    #     - DeviceID {str} -- Set the DeviceID to be used with the device. Only required to override the default which is and eight digit number dervice from the HardwareID and the Unit number in the format "000H000U".
    #     Field type is Varchar(25) (default: {None})
    #     """
    #     self._Device = d.Domoticz.Device(Name=Name, Unit=Unit, Type=Type, Subtype=Subtype,
    #                                      Switchtype=Switchtype, Image=Image, Options=Options, Used=1 if Used else 0)

    def __str__(self):
        return str(self._Device)

    def Create(self):
        """Creates the device in Domoticz from the object."""
        self._Device.Create()

    def Update(self, nValue: int, sValue: str, **kvargs):
        """Updates the current values in Domoticz.

        Arguments:
        - nValue {float} -- The Numerical device value
        - sValue {str} -- The string device value

        Keyword Arguments:
        - Image {int} -- Numeric custom image number (default: {None})
        - SignalLevel {int} -- Device signal strength, default 12  (default: {12})
        - BatteryLevel {int} -- Device battery strength, default 255  (default: {255})
        - Options {Dict[str, str]} -- Dictionary of device options, default is empty {}  (default: {{}})
        - TimedOut {int} -- Numeric field where 0 (false) is not timed out and other value marks the device as timed out, default is 0.
        - Timed out devices show with a red header in the Domoticz web UI.  (default: {0})
        - Name {str} -- Is appended to the Hardware name to set the initial Domoticz Device name.
        - This should not be used in Python because it can be changed in the Web UI.  (default: {None})
        - TypeName {DomoticzTypeName} -- Common device types, this will set the values for Type, Subtype and Switchtype. (default: {None})
        - Type {int} -- Directly set the numeric Type value. Should only be used if the Device to be created is not supported by TypeName.  (default: {None})
        - Subtype {int} -- Directly set the numeric Subtype value. Should only be used if the Device to be created is not supported by TypeName.  (default: {None})
        - Switchtype {int} -- Directly set the numeric Switchtype value. Should only be used if the Device to be created is not supported by TypeName.  (default: {None})
        - Used {bool} -- Set the Device Used field. Used devices appear in the appropriate tab(s), unused devices appear only in the Devices page and must be manually marked as Used.  (default: {False})
        - Description {str} -- Device description (default: {None})
        - Color {str} -- Current color, see documentation of onCommand callback for details on the format.  (default: {None})
        - SuppressTriggers {bool} -- Default: False Boolean flag that allows device attributes to be updated without notifications, scene or MQTT, event triggers. nValue and sValue are not written to the database and will be overwritten with current database values.  (default: {False})
        """
        self._Device.Update(nValue, sValue, **kvargs)

    def Delete(self):
        """Deletes the device in Domoticz"""
        self._Device.Delete()

    def Refresh(self):
        """Refreshes the values for the device from the Domoticz database.

        Not normally required because device values are updated when callbacks are invoked. """
        self._Device.Delete()

    def Touch(self):
        """Updates the Device's 'last seen' time and nothing else. No events or notifications are triggered as a result of touching a Device.

        After the call the Device's LastUpdate field will reflect the new value. """
        self._Device.Touch()

    @property
    def ID(self) -> int:
        """The Domoticz Device ID

        Returns:
            int -- The Domoticz Device ID
        """
        return self._Device.ID

    @property
    def Name(self) -> str:
        """Current Name in Domoticz

        Returns:
            str -- Current Name in Domoticz
        """
        return self._Device.Name

    @property
    def DeviceID(self) -> str:
        """External device identifier

        Returns:
            str -- External device identifier
        """
        return self._Device.DeviceID

    @property
    def nValue(self) -> float:
        """Current numeric value

        Returns:
            float -- Current numeric value
        """
        return self._Device.nValue

    @property
    def sValue(self) -> str:
        """Current string value

        Returns:
            str -- Current string value
        """
        return self._Device.sValue

    @property
    def SignalLevel(self) -> float:
        """Numeric signal level

        Returns:
            float -- Numeric signal level
        """
        return self._Device.SignalLevel

    @property
    def BatteryLevel(self) -> float:
        """Numeric battery level

        Returns:
            float -- Numeric battery level
        """
        return self._Device.BatteryLevel

    @property
    def Image(self) -> int:
        """Current image number

        Returns:
            int -- Current image number
        """
        return self._Device.Image

    @property
    def Type(self) -> int:
        """Numeric device type

        Returns:
            int -- Numeric device type
        """
        return self._Device.Type

    @property
    def SubType(self) -> int:
        """Numeric device subtype

        Returns:
            int -- Numeric device subtype
        """
        return self._Device.SubType

    @property
    def Switchtype(self) -> int:
        """Numeric device switchtype

        Returns:
            int -- Numeric device switchtype
        """
        return self._Device.Switchtype

    @property
    def Used(self) -> bool:
        """Device Used flag

        Returns:
            bool -- Device Used flag
        """
        return self._Device.Used == 1

    @property
    def Options(self) -> Dict[str, str]:
        """Current Device options dictionary

        Returns:
            Dict[str, str] -- Current Device options dictionary
        """
        return self._Device.Options

    @property
    def TimedOut(self) -> bool:
        """Device TimedOut flag

        Returns:
            bool -- Device TimedOut flag
        """
        return self._Device.TimedOut == 1

    @property
    def LastLevel(self) -> float:
        """Last level as reported by Domoticz

        Returns:
            float -- Last level as reported by Domoticz
        """
        return self._Device.LastLevel

    @property
    def LastUpdate(self) -> datetime:
        """Timestamp of the last update, e.g: 2017-01-22 01:21:11

        Returns:
            datetime -- Timestamp of the last update, e.g: 2017-01-22 01:21:11
        """
        return self._Device.LastUpdate

    @property
    def Description(self) -> str:
        """Description of the device, visible in "Edit" dialog in Domoticz Web UI.

        Returns:
            str -- Description of the device, visible in "Edit" dialog in Domoticz Web UI.
        """
        return self._Device.Description

    @property
    def Color(self) -> str:
        """Current color, see documentation of onCommand callback for details on the format.

        Returns:
            str -- Current color, see documentation of onCommand callback for details on the format.
        """
        return self._Device.Color


class DomoticzConnection:
    """Defines the connection type that will be used by the object"""

    def __init__(self, d: DomoticzWrapper = None, Name: str = None, Transport: str = None, Protocol: str = None, Address: str = None, Port: str = None, Baud: int = 115200, Connection=None):
        """Defines the connection type that will be used by the object

        Arguments:
            Name {str} -- Required.

        Name of the Connection. For incoming connections Domoticz will assign a unique name.
                    Transport {str} -- Required.

        Valid values:

            TCP/IP: Connect over an IP network then send or receive messages

        See HTTP/HTTPS Client example that uses GET and POST over HTTP or HTTPS
        See HTTP Listener example that acts as a lightweight webserver

            TLS/IP: Connect over an IP network using TLS security then send or receive messages

        See HTTP/HTTPS Client example

            UDP/IP: Send or receive UDP messages, useful for discovering hardware on a network.

        See UDP Discovery example
        See UDP broadcast example (onNotification function)

            ICMP/IP: Send or receive ICMP messages, useful for discovering or pinging hardware on a network.

        See Pinger example

            Serial: Connect to serial ports, see RAVEn power monitoring example
                    Protocol {str} -- Required.

        The protocol that will be used to talk to the external hardware. This is used to allow Domoticz to break incoming data into single messages to pass to the plugin. Valid values:

            None (default)
            Line
            JSON
            XML
            HTTP
            HTTPS
            MQTT
            MQTTS
            ICMP
                    Address {str} -- Required.
        TCP/IP or UDP/IP Address or SerialPort to connect to.
                    Port {str} -- Optional.
        TCP/IP & UDP/IP connections only, string containing the port number.
                    Baud {int} -- Optional.
        Serial connections only, the required baud rate.

        Default: 115200

                Returns:
                    [type] -- [description]
        """
        if Connection is not None:
            self._Connection = Connection
        else:
            self._Connection = d.Domoticz.Connection(
                Name=Name, Transport=Transport, Protocol=Protocol, Address=Address, Port=Port, Baud=Baud)

    def __str__(self):
        return str(self._Connection)

    @property
    def Name(self) -> str:
        """Returns the Name of the Connection

        Returns:
            str -- Returns the Name of the Connection
        """
        return self._Connection.Name

    @property
    def Address(self) -> str:
        """Returns the Address associated with the Connection.

        Returns:
            str -- Returns the Address associated with the Connection.
        """
        return self._Connection.Address

    @property
    def Port(self) -> str:
        """Returns the Port associated with the Connection.

        Returns:
            str -- Returns the Port associated with the Connection.
        """
        return self._Connection.Port

    @property
    def Baud(self) -> int:
        """Returns the Baud Rate of the Connection.

        Returns:
            str -- Returns the Baud Rate of the Connection.
        """
        return self._Connection.Baud

    @property
    def Parent(self) -> str:
        """Normally 'None' but for incoming connections this will hold the Connection object that is 'Listening' for the connection.

        Returns:
            str -- Normally 'None' but for incoming connections this will hold the Connection object that is 'Listening' for the connection.
        """
        return self._Connection.Parent

    def Connecting(self) -> bool:
        """Returns True if a connection has been requested but has yet to complete (or fail), otherwise False.

        Returns:
            bool -- Returns True if a connection has been requested but has yet to complete (or fail), otherwise False.
        """
        return self._Connection.Connecting()

    def Listen(self):
        """Start listening on specified Port using the specified TCP/IP, UDP/IP or ICMP/IP transport. Connection objects will be created for each client that connects and onConnect will be called.
        If a Listen request is unsuccessful the plugin's onConnect callback will be called with failure details. If it is successful then onConnect will be called when incoming Connections are made."""
        return self._Connection.Listen()

    def Send(self, Message, Delay):
        """Send the specified message to the external hardware

        Arguments:
            Message {[type]} -- Mandatory.
        Message text to send.

        For simple Protocols this can be of type String, ByteArray or Bytes.
        For structured Protocols (such as HTTP) it should be a Dictionary.
                    Delay {[type]} -- Optional.
        Number of seconds to delay message send.
        Note that Domoticz will send the message sometime after this period. Other events will be processed in the intervening period so delayed sends will be processed out of order. This feature may be useful during delays when physical devices turn on.
        """
        return self._Connection.Send(Message=Message, Delay=Delay)

    def Disconnect(self):
        """Terminate the connection to the external hardware for the connection.
        Disconnect also terminates listening connections for all transports (including connectionless ones e.g UDP/IP)."""
        return self._Connection.Disconnect()


class DomoticzImage:
    """Developers can ship custom images with plugins in the standard Domoticz format as
    described [here](https://www.domoticz.com/wiki/Custom_icons_for_webinterface#Creating_simple_home_made_icons).
    Resultant zip file(s) should be placed in the folder with the plugin itself"""

    def __init__(self, d: DomoticzWrapper = None, filename: str = None, Image=None):
        if Image is not None:
            self._Image = Image
        else:
            self._Image = d.Domoticz.Image(filename)

    def __str__(self):
        return str(self._Image)

    @property
    def ID(self) -> int:
        """Image ID in CustomImages table

        Returns:
            int -- The Domoticz Image ID
        """
        return self._Image.ID

    @property
    def Name(self) -> str:
        """Name as specified in upload file

        Returns:
            str -- The Domoticz Image Name
        """
        return self._Image.Name

    @property
    def Base(self) -> str:
        """This MUST start with (or be) the plugin key as defined in the XML definition.
        If not the image will not be loaded into the Images dictionary

        Returns:
            str -- The Domoticz Image Base
        """
        return self._Image.Base

    @property
    def Description(self) -> str:
        """Description as specified in upload file

        Returns:
            str -- The Domoticz Image Description
        """
        return self._Image.Description

    def Create(self):
        """Creates the image in Domoticz from the object. E.g:
        ```
        myImg = Domoticz.Image(Filename="Plugin Icons.zip")
        myImg.Create()
        ```
        or
        ```
        Domoticz.Image(Filename="Plugin Icons.zip").Create()
        ```
        Successfully created images are immediately added to the Images dictionary.
        """
        return self._Image.Create()

    def Delete(self):
        """Deletes the image in Domoticz. E.g:
        ```
        Images['myPlugin'].Delete()
        ```
        or
        ```
        myImg = Images['myPlugin']
        myImg.Delete()
        ```
        Deleted images are immediately removed from the Images dictionary but local instances of the object are unchanged.
        """
        return self._Image.Delete()


class DomoticzDeviceTypes:
    @staticmethod
    def Lighting2() -> DomoticzDeviceType:
        """Behaves the same as Light/Switch, Preferable to use Type 244 instead"""
        return DomoticzDeviceType(17)

    @staticmethod
    def Temp() -> DomoticzDeviceType:
        """Temperature sensor"""
        return DomoticzDeviceType(80, 5)

    @staticmethod
    def Humidity() -> DomoticzDeviceType:
        """Humidity sensor"""
        return DomoticzDeviceType(81, 1)

    @staticmethod
    def TempHum() -> DomoticzDeviceType:
        """Temperature + Humidity sensor"""
        return DomoticzDeviceType(82, 1)

    @staticmethod
    def TempHumBaro_THB1() -> DomoticzDeviceType:
        """Temperature + Humidity + Barometer sensor
        Device.Update(nValue, sValue)
        nValue is always 0,
        sValue is string with values separated by semicolon: Temperature;Humidity;Humidity Status;Barometer;Forecast
        Humidity status: 0 - Normal, 1 - Comfort, 2 - Dry, 3 - Wet
        Forecast: 0 - None, 1 - Sunny, 2 - PartlyCloudy, 3 - Cloudy, 4 - Rain"""
        return DomoticzDeviceType(84, 1)

    @staticmethod
    def TempHumBaro_THB2() -> DomoticzDeviceType:
        """Temperature + Humidity + Barometer sensor
        Device.Update(nValue, sValue)
        nValue is always 0,
        sValue is string with values separated by semicolon: Temperature;Humidity;Humidity Status;Barometer;Forecast
        Humidity status: 0 - Normal, 1 - Comfort, 2 - Dry, 3 - Wet
        Forecast: 0 - None, 1 - Sunny, 2 - PartlyCloudy, 3 - Cloudy, 4 - Rain"""
        return DomoticzDeviceType(84, 2)

    @staticmethod
    def TempHumBaro_WeatherStation() -> DomoticzDeviceType:
        """Temperature + Humidity + Barometer sensor
        Device.Update(nValue, sValue)
        nValue is always 0,
        sValue is string with values separated by semicolon: Temperature;Humidity;Humidity Status;Barometer;Forecast
        Humidity status: 0 - Normal, 1 - Comfort, 2 - Dry, 3 - Wet
        Forecast: 0 - None, 1 - Sunny, 2 - PartlyCloudy, 3 - Cloudy, 4 - Rain"""
        return DomoticzDeviceType(84, 16)

    @staticmethod
    def Rain() -> DomoticzDeviceType:
        """Rain sensor (sValue: "<RainLastHour_mm*100>;<Rain_mm>", Rain_mm is everincreasing counter)"""
        return DomoticzDeviceType(85, 1)

    @staticmethod
    def Wind() -> DomoticzDeviceType:
        """Wind sensor (sValue: "<WindDirDegrees>;<WindDirText>;<WindAveMeterPerSecond*10>;<WindGustMeterPerSecond*10>;<Temp_c>;<WindChill_c>")"""
        return DomoticzDeviceType(86, 1)

    @staticmethod
    def UV() -> DomoticzDeviceType:
        """UV sensor (sValue: "<UV>;<Temp>")"""
        return DomoticzDeviceType(87, 1)

    @staticmethod
    def Ampere_3_Phase() -> DomoticzDeviceType:
        """Ampere (3 Phase)"""
        return DomoticzDeviceType(89, 1)

    @staticmethod
    def Scale() -> DomoticzDeviceType:
        """Weight"""
        return DomoticzDeviceType(93, 1)

    @staticmethod
    def Counter() -> DomoticzDeviceType:
        """Counter"""
        return DomoticzDeviceType(113, 0)

    @staticmethod
    def ColorSwitch_RGBW() -> DomoticzDeviceType:
        """RGB + white, either RGB or white can be lit"""
        return DomoticzDeviceType(241, 1)

    @staticmethod
    def ColorSwitch_RGB() -> DomoticzDeviceType:
        """RGB Color Switch"""
        return DomoticzDeviceType(241, 2)

    @staticmethod
    def ColorSwitch_White() -> DomoticzDeviceType:
        """Monochrome White Color Switch"""
        return DomoticzDeviceType(241, 3)

    @staticmethod
    def ColorSwitch_RGBWW() -> DomoticzDeviceType:
        """RGB + cold white + warm white, either RGB or white can be lit"""
        return DomoticzDeviceType(241, 4)

    @staticmethod
    def ColorSwitch_RGBWZ() -> DomoticzDeviceType:
        """Like RGBW, but allows combining RGB and white"""
        return DomoticzDeviceType(241, 6)

    @staticmethod
    def ColorSwitch_RGBWWZ() -> DomoticzDeviceType:
        """Like RGBWW, but allows combining RGB and white"""
        return DomoticzDeviceType(241, 7)

    @staticmethod
    def ColorSwitch_ColdWhiteWarmWhite() -> DomoticzDeviceType:
        """Cold white + Warm white"""
        return DomoticzDeviceType(241, 8)

    @staticmethod
    def ThermostatSetpoint() -> DomoticzDeviceType:
        """Thermostat Setpoint"""
        return DomoticzDeviceType(242, 1)

    @staticmethod
    def General_Visibility() -> DomoticzDeviceType:
        """Visibility"""
        return DomoticzDeviceType(243, 1)

    @staticmethod
    def General_SolarRadiation() -> DomoticzDeviceType:
        """sValue: "float" """
        return DomoticzDeviceType(243, 2)

    @staticmethod
    def General_SoilMoisture() -> DomoticzDeviceType:
        """Soil Moisture"""
        return DomoticzDeviceType(243, 3)

    @staticmethod
    def General_LeafWetness() -> DomoticzDeviceType:
        """Leaf Wetness"""
        return DomoticzDeviceType(243, 4)

    @staticmethod
    def General_Percentage() -> DomoticzDeviceType:
        """Percentage"""
        return DomoticzDeviceType(243, 6)

    @staticmethod
    def General_Voltage() -> DomoticzDeviceType:
        """Voltage"""
        return DomoticzDeviceType(243, 8)

    @staticmethod
    def General_Pressure() -> DomoticzDeviceType:
        """Pressure"""
        return DomoticzDeviceType(243, 9)

    @staticmethod
    def General_Text() -> DomoticzDeviceType:
        """Text"""
        return DomoticzDeviceType(243, 19)

    @staticmethod
    def General_Alert() -> DomoticzDeviceType:
        """Alert"""
        return DomoticzDeviceType(243, 22)

    @staticmethod
    def General_Ampere_1_Phase() -> DomoticzDeviceType:
        """Ampere (1 Phase)"""
        return DomoticzDeviceType(243, 23)

    @staticmethod
    def General_SoundLevel() -> DomoticzDeviceType:
        """Sound Level"""
        return DomoticzDeviceType(243, 24)

    @staticmethod
    def General_Barometer() -> DomoticzDeviceType:
        """nValue: 0, sValue: "pressure;forecast"
        Forecast:
        0 - Stable
        1 - Clear/Sunny
        2 - Cloudy/Rain
        3 - Not stable
        4 - Thunderstorm
        5 - Unknown """
        return DomoticzDeviceType(243, 26)

    @staticmethod
    def General_Distance() -> DomoticzDeviceType:
        """Distance"""
        return DomoticzDeviceType(243, 27)

    @staticmethod
    def General_CounterIncremental() -> DomoticzDeviceType:
        """Counter Incremental"""
        return DomoticzDeviceType(243, 28)

    @staticmethod
    def General_kWh() -> DomoticzDeviceType:
        """Electric (Instant+Counter)"""
        return DomoticzDeviceType(243, 29)

    @staticmethod
    def General_Waterflow() -> DomoticzDeviceType:
        """Waterflow"""
        return DomoticzDeviceType(243, 30)

    @staticmethod
    def General_CustomSensor() -> DomoticzDeviceType:
        """nValue: 0, sValue: "floatValue", Options: {'Custom': '1;<axisUnits>'}"""
        return DomoticzDeviceType(243, 31)

    @staticmethod
    def General_ManagedCounter_Energy() -> DomoticzDeviceType:
        """nValue is always 0

        sValue must be a single value to update Dashboard, for instance "1234"
        sValue must be a value followed by a space and a date ("%Y-%m-%d" format) to update last week/month/year history, for instance "1234 2019-09-24"
        sValue must be a value followed by a space a date a space and a time ("%Y-%m-%d %H:%M:%S" format) to update last days history, for instance "1234 2019-10-03 14:55:00" """
        return DomoticzDeviceType(243, 33, 0)

    @staticmethod
    def General_ManagedCounter_Gas() -> DomoticzDeviceType:
        """nValue is always 0

        sValue must be a single value to update Dashboard, for instance "1234"
        sValue must be a value followed by a space and a date ("%Y-%m-%d" format) to update last week/month/year history, for instance "1234 2019-09-24"
        sValue must be a value followed by a space a date a space and a time ("%Y-%m-%d %H:%M:%S" format) to update last days history, for instance "1234 2019-10-03 14:55:00" """
        return DomoticzDeviceType(243, 33, 1)

    @staticmethod
    def General_ManagedCounter_Water() -> DomoticzDeviceType:
        """nValue is always 0

        sValue must be a single value to update Dashboard, for instance "1234"
        sValue must be a value followed by a space and a date ("%Y-%m-%d" format) to update last week/month/year history, for instance "1234 2019-09-24"
        sValue must be a value followed by a space a date a space and a time ("%Y-%m-%d %H:%M:%S" format) to update last days history, for instance "1234 2019-10-03 14:55:00" """
        return DomoticzDeviceType(243, 33, 2)

    @staticmethod
    def General_ManagedCounter_Counter() -> DomoticzDeviceType:
        """nValue is always 0

        sValue must be a single value to update Dashboard, for instance "1234"
        sValue must be a value followed by a space and a date ("%Y-%m-%d" format) to update last week/month/year history, for instance "1234 2019-09-24"
        sValue must be a value followed by a space a date a space and a time ("%Y-%m-%d %H:%M:%S" format) to update last days history, for instance "1234 2019-10-03 14:55:00" """
        return DomoticzDeviceType(243, 33, 3)

    @staticmethod
    def General_ManagedCounter_EnergyGenerated() -> DomoticzDeviceType:
        """nValue is always 0

        sValue must be a single value to update Dashboard, for instance "1234"
        sValue must be a value followed by a space and a date ("%Y-%m-%d" format) to update last week/month/year history, for instance "1234 2019-09-24"
        sValue must be a value followed by a space a date a space and a time ("%Y-%m-%d %H:%M:%S" format) to update last days history, for instance "1234 2019-10-03 14:55:00" """
        return DomoticzDeviceType(243, 33, 4)

    @staticmethod
    def General_ManagedCounter_Time() -> DomoticzDeviceType:
        """nValue is always 0

        sValue must be a single value to update Dashboard, for instance "1234"
        sValue must be a value followed by a space and a date ("%Y-%m-%d" format) to update last week/month/year history, for instance "1234 2019-09-24"
        sValue must be a value followed by a space a date a space and a time ("%Y-%m-%d %H:%M:%S" format) to update last days history, for instance "1234 2019-10-03 14:55:00" """
        return DomoticzDeviceType(243, 33, 5)

    @staticmethod
    def LightSwitch_Selector_OnOff() -> DomoticzDeviceType:
        """"""
        return DomoticzDeviceType(244, 62, 0)

    @staticmethod
    def LightSwitch_Selector_Doorbell() -> DomoticzDeviceType:
        """"""
        return DomoticzDeviceType(244, 62, 1)

    @staticmethod
    def LightSwitch_Selector_Contact() -> DomoticzDeviceType:
        """Statuses:
        Open: nValue = 1
        Closed: nValue = 0"""
        return DomoticzDeviceType(244, 62, 2)

    @staticmethod
    def LightSwitch_Selector_Blinds() -> DomoticzDeviceType:
        """"""
        return DomoticzDeviceType(244, 62, 3)

    @staticmethod
    def LightSwitch_Selector_X10_Siren() -> DomoticzDeviceType:
        """"""
        return DomoticzDeviceType(244, 62, 4)

    @staticmethod
    def LightSwitch_Selector_SmokeDetector() -> DomoticzDeviceType:
        """"""
        return DomoticzDeviceType(244, 62, 5)

    @staticmethod
    def LightSwitch_Selector_Blinds_Inverted() -> DomoticzDeviceType:
        """"""
        return DomoticzDeviceType(244, 62, 6)

    @staticmethod
    def LightSwitch_Selector_Dimmer() -> DomoticzDeviceType:
        """"""
        return DomoticzDeviceType(244, 62, 7)

    @staticmethod
    def LightSwitch_Selector_MotionSensor() -> DomoticzDeviceType:
        """Statuses:
        Motion: nValue = 1
        Off: nValue = 0"""
        return DomoticzDeviceType(244, 62, 8)

    @staticmethod
    def LightSwitch_Selector_Push_On_Button() -> DomoticzDeviceType:
        """"""
        return DomoticzDeviceType(244, 62, 9)

    @staticmethod
    def LightSwitch_Selector_Push_Off_Button() -> DomoticzDeviceType:
        """"""
        return DomoticzDeviceType(244, 62, 10)

    @staticmethod
    def LightSwitch_Selector_Door_Contact() -> DomoticzDeviceType:
        """Statuses:
        Open: nValue = 1
        Closed: nValue = 0"""
        return DomoticzDeviceType(244, 62, 11)

    @staticmethod
    def LightSwitch_Selector_DuskSensor() -> DomoticzDeviceType:
        """"""
        return DomoticzDeviceType(244, 62, 12)

    @staticmethod
    def LightSwitch_Selector_BlindsPercentage() -> DomoticzDeviceType:
        """Statuses:
        Closed: nValue = 1 and sValue = 100
        partially opened: nValue = 2 and sValue = 1-99
        Open: nValue = 0 and sValue = 0"""
        return DomoticzDeviceType(244, 62, 13)

    @staticmethod
    def LightSwitch_Selector_Venetian_Blinds_US() -> DomoticzDeviceType:
        """"""
        return DomoticzDeviceType(244, 62, 14)

    @staticmethod
    def LightSwitch_Selector_Venetian_Blinds_EU() -> DomoticzDeviceType:
        """"""
        return DomoticzDeviceType(244, 62, 15)

    @staticmethod
    def LightSwitch_Selector_Blinds_Percentage_Inverted() -> DomoticzDeviceType:
        """Statuses:
        Closed: nValue = 0 and sValue = 0
        partially opened: nValue = 2 and sValue = 1-99
        Open: nValue = 1 and sValue = 100"""
        return DomoticzDeviceType(244, 62, 16)

    @staticmethod
    def LightSwitch_Selector_Media_Player() -> DomoticzDeviceType:
        """"""
        return DomoticzDeviceType(244, 62, 17)

    @staticmethod
    def LightSwitch_Selector_Selector() -> DomoticzDeviceType:
        """"""
        return DomoticzDeviceType(244, 62, 18)

    @staticmethod
    def LightSwitch_Selector_Door_Lock() -> DomoticzDeviceType:
        """"""
        return DomoticzDeviceType(244, 62, 19)

    @staticmethod
    def LightSwitch_Selector_Door_Lock_Inverted() -> DomoticzDeviceType:
        """"""
        return DomoticzDeviceType(244, 73, 20)

    @staticmethod
    def LightSwitch_Switch_OnOff() -> DomoticzDeviceType:
        """"""
        return DomoticzDeviceType(244, 73, 0)

    @staticmethod
    def LightSwitch_Switch_Doorbell() -> DomoticzDeviceType:
        """"""
        return DomoticzDeviceType(244, 73, 1)

    @staticmethod
    def LightSwitch_Switch_Contact() -> DomoticzDeviceType:
        """Statuses:
        Open: nValue = 1
        Closed: nValue = 0"""
        return DomoticzDeviceType(244, 73, 2)

    @staticmethod
    def LightSwitch_Switch_Blinds() -> DomoticzDeviceType:
        """"""
        return DomoticzDeviceType(244, 73, 3)

    @staticmethod
    def LightSwitch_Switch_X10_Siren() -> DomoticzDeviceType:
        """"""
        return DomoticzDeviceType(244, 73, 4)

    @staticmethod
    def LightSwitch_Switch_SmokeDetector() -> DomoticzDeviceType:
        """"""
        return DomoticzDeviceType(244, 73, 5)

    @staticmethod
    def LightSwitch_Switch_Blinds_Inverted() -> DomoticzDeviceType:
        """"""
        return DomoticzDeviceType(244, 73, 6)

    @staticmethod
    def LightSwitch_Switch_Dimmer() -> DomoticzDeviceType:
        """"""
        return DomoticzDeviceType(244, 73, 7)

    @staticmethod
    def LightSwitch_Switch_MotionSensor() -> DomoticzDeviceType:
        """Statuses:
        Motion: nValue = 1
        Off: nValue = 0"""
        return DomoticzDeviceType(244, 73, 8)

    @staticmethod
    def LightSwitch_Switch_Push_On_Button() -> DomoticzDeviceType:
        """"""
        return DomoticzDeviceType(244, 73, 9)

    @staticmethod
    def LightSwitch_Switch_Push_Off_Button() -> DomoticzDeviceType:
        """"""
        return DomoticzDeviceType(244, 73, 10)

    @staticmethod
    def LightSwitch_Switch_Door_Contact() -> DomoticzDeviceType:
        """Statuses:
        Open: nValue = 1
        Closed: nValue = 0"""
        return DomoticzDeviceType(244, 73, 11)

    @staticmethod
    def LightSwitch_Switch_DuskSensor() -> DomoticzDeviceType:
        """"""
        return DomoticzDeviceType(244, 73, 12)

    @staticmethod
    def LightSwitch_Switch_BlindsPercentage() -> DomoticzDeviceType:
        """Statuses:
        Closed: nValue = 1 and sValue = 100
        partially opened: nValue = 2 and sValue = 1-99
        Open: nValue = 0 and sValue = 0"""
        return DomoticzDeviceType(244, 73, 13)

    @staticmethod
    def LightSwitch_Switch_Venetian_Blinds_US() -> DomoticzDeviceType:
        """"""
        return DomoticzDeviceType(244, 73, 14)

    @staticmethod
    def LightSwitch_Switch_Venetian_Blinds_EU() -> DomoticzDeviceType:
        """"""
        return DomoticzDeviceType(244, 73, 15)

    @staticmethod
    def LightSwitch_Switch_Blinds_Percentage_Inverted() -> DomoticzDeviceType:
        """Statuses:
        Closed: nValue = 0 and sValue = 0
        partially opened: nValue = 2 and sValue = 1-99
        Open: nValue = 1 and sValue = 100"""
        return DomoticzDeviceType(244, 73, 16)

    @staticmethod
    def LightSwitch_Switch_Media_Player() -> DomoticzDeviceType:
        """"""
        return DomoticzDeviceType(244, 73, 17)

    @staticmethod
    def LightSwitch_Switch_Selector() -> DomoticzDeviceType:
        """"""
        return DomoticzDeviceType(244, 73, 18)

    @staticmethod
    def LightSwitch_Switch_Door_Lock() -> DomoticzDeviceType:
        """"""
        return DomoticzDeviceType(244, 73, 19)

    @staticmethod
    def LightSwitch_Switch_Door_Lock_Inverted() -> DomoticzDeviceType:
        """"""
        return DomoticzDeviceType(244, 73, 20)

    @staticmethod
    def Lux() -> DomoticzDeviceType:
        """Illumination (sValue: "float")"""
        return DomoticzDeviceType(246, 1)

    @staticmethod
    def TempBaro() -> DomoticzDeviceType:
        """Temperature + Barometer sensor"""
        return DomoticzDeviceType(247, 1)

    @staticmethod
    def ElectricUsage() -> DomoticzDeviceType:
        """Electric Usage"""
        return DomoticzDeviceType(248, 1)

    @staticmethod
    def AirQuality() -> DomoticzDeviceType:
        """Air Quality"""
        return DomoticzDeviceType(249, 1)

    @staticmethod
    def P1_SmartMeter_Energy() -> DomoticzDeviceType:
        """P1 SmartMeter: Energy"""
        return DomoticzDeviceType(250, 1)

    @staticmethod
    def P1_SmartMeter_Gas() -> DomoticzDeviceType:
        """P1 SmartMeter: Gas"""
        return DomoticzDeviceType(251, 2)
