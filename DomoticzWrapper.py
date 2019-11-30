"""Wrapper for the Domoticz plugin API.
Based on information in https://www.domoticz.com/wiki/Developing_a_Python_plugin as of git commit dates
"""


# DomoticzWrapper.Debugging([DomoticzDebugLevel.ShowNone])
# DomoticzWrapper.Parameters(DomoticzParameter.Mode4)

from enum import Enum
from typing import List, Dict
from datetime import datetime


class DomoticzDebugLevel(Enum):
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


class DomoticzPluginParameter(Enum):
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
    Key = 'Key'
    HomeFolder = 'HomeFolder'
    Author = 'Author'
    Version = 'Version'
    Address = 'Address'
    Port = 'Port'
    Username = 'Username'
    Password = 'Password'
    Mode1 = 'Mode1'
    Mode2 = 'Mode2'
    Mode3 = 'Mode3'
    Mode4 = 'Mode4'
    Mode5 = 'Mode5'
    Mode6 = 'Mode6'
    SerialPort = 'SerialPort'


class DomoticzTypeName(Enum):
    AirQuality = "Air Quality"
    Alert = "Alert"
    Barometer = "Barometer"
    CounterIncremental = "Counter Incremental"
    Contact = "Contact"
    CurrentAmpere = "Current/Ampere"
    CurrentSingle = "Current (Single)"
    Custom = "Custom"
    Dimmer = "Dimmer"
    Distance = "Distance"
    Gas = "Gas"
    Humidity = "Humidity"
    Illumination = "Illumination"
    kWh = "kWh"
    LeafWetness = "Leaf Wetness"
    Motion = "Motion"
    Percentage = "Percentage"
    PushOn = "Push On"
    PushOff = "Push Off"
    Pressure = "Pressure"
    Rain = "Rain"
    SelectorSwitch = "Selector Switch"
    SoilMoisture = "Soil Moisture"
    SolarRadiation = "Solar Radiation"
    SoundLevel = "Sound Level"
    Switch = "Switch"
    Temperature = "Temperature"
    TempHum = "Temp+Hum"
    TempHumBaro = "Temp+Hum+Baro"
    Text = "Text"
    Usage = "Usage"
    UV = "UV"
    Visibility = "Visibility"
    Voltage = "Voltage"
    Waterflow = "Waterflow"
    Wind = "Wind"
    WindTempChill = "Wind+Temp+Chill"


class DomoticzDevice:
    """A Domoticz Device"""

    def __init__(self, Name: str, Unit: int, TypeName: DomoticzTypeName = None, Type: int = None, Subtype: int = None, Switchtype: int = None, Image: int = None, Options: Dict[str, str] = None, Used: bool = False, DeviceID: str = None):
        """Creator

        Arguments:
        - Name {str} -- Is appended to the Hardware name to set the initial Domoticz Device name.
        This should not be used in Python because it can be changed in the Web UI.
        - Unit {int} -- Plugin index for the Device. This can not change and should be used reference Domoticz devices associated with the plugin. This is also the key for the Devices Dictionary that Domoticz prepopulates for the plugin.
        Unit numbers must be less than 256.

            Keyword Arguments:
        - TypeName {DomoticzTypeName} -- Common device types, this will set the values for Type, Subtype and Switchtype. (default: {None})
        - Type {int} -- Directly set the numeric Type value. Should only be used if the Device to be created is not supported by TypeName. (default: {None})
        - Subtype {int} -- Directly set the numeric Subtype value. Should only be used if the Device to be created is not supported by TypeName. (default: {None})
        - Switchtype {int} -- Directly set the numeric Switchtype value. Should only be used if the Device to be created is not supported by TypeName. (default: {None})
        - Image {int} -- Set the image number to be used with the device. Only required to override the default.
        All images available by JSON API call "/json.htm?type=custom_light_icons" (default: {None})
        - Options {Dict[str, str]} -- Set the Device Options field. A few devices, like Selector Switches, require additional details to be set in this field. It is a Python dictionary consisting of key values pairs, where the keys and values must be strings. See the example to the right. (default: {None})
        - Used {bool} -- Values
        0 (default) Unused
        1 Used.
        Set the Device Used field. Used devices appear in the appropriate tab(s), unused devices appear only in the Devices page and must be manually marked as Used. (default: {False})
        - DeviceID {str} -- Set the DeviceID to be used with the device. Only required to override the default which is and eight digit number dervice from the HardwareID and the Unit number in the format "000H000U".
        Field type is Varchar(25) (default: {None})
        """
        self._Device = Domoticz.Device(Name=Name, Unit=Unit, TypeName=TypeName, Type=Type, Subtype=Subtype,
                                       Switchtype=Switchtype, Image=Image, Options=Options, Used=1 if Used else 0, DeviceID=DeviceID)

    def Create(self):
        """Creates the device in Domoticz from the object."""
        self._Device.Create()

    def Update(self, nValue: float, sValue: str, Image: int = None, SignalLevel: int = 12, BatteryLevel: int = 255, Options: Dict[str, str] = {}, TimedOut: int = 0, Name: str = None, TypeName: DomoticzTypeName = None, Type: int = None, Subtype: int = None, Switchtype: int = None, Used: bool = False, Description: str = None, Color: str = None, SuppressTriggers: bool = False):
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
        self._Device.Update(nValue, sValue, Image, SignalLevel, BatteryLevel, Options, TimedOut, Name,
                            TypeName, Type, Subtype, Switchtype, 1 if Used else 0, Description, Color, SuppressTriggers)

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

# @dataclass
# class DomoticzDeviceType:
#     """Domoticz Device Type definition"""
#     type_id: int
#     type_name: str
#     subtype_id: int
#     subtype_name: str
#     switchtype_id: int
#     switchtype_name: str
#     description: str


class DomoticzConnection:
    """Defines the connection type that will be used by the object

    Returns:
        [type] -- [description]
    """

    def __init__(self, Name: str, Transport: str, Protocol: str, Address: str, Port: str = None, Baud: int = 115200):
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
        self._Connection = Domoticz.Connection(
            Name=Name, Transport=Transport, Protocol=Protocol, Address=Address, Port=Port, Baud=Baud)

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

    def __init__(self, filename):
        self._image = Domoticz.Image(filename)

    @property
    def ID(self) -> int:
        """Image ID in CustomImages table

        Returns:
            int -- The Domoticz Image ID
        """
        return self._image.ID

    @property
    def Name(self) -> str:
        """Name as specified in upload file

        Returns:
            str -- The Domoticz Image Name
        """
        return self._image.ID

    @property
    def Base(self) -> str:
        """This MUST start with (or be) the plugin key as defined in the XML definition.
        If not the image will not be loaded into the Images dictionary

        Returns:
            str -- The Domoticz Image Base
        """
        return self._image.ID

    @property
    def Description(self) -> str:
        """Description as specified in upload file

        Returns:
            str -- The Domoticz Image Description
        """
        return self._image.ID

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
        return self._image.Create()

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
        return self._image.Delete()


class DomoticzWrapper:
    # @property
    # def x(self) -> str:
    #     return Domoticz.x

    # @x.setter
    # def x(self, val):
    #     Domoticz.x = val

    @classmethod
    def Debug(cls, val: str):
        """Write a message to Domoticz log only if verbose logging is turned on.

        Arguments:
            val {str} -- Message to log
        """
        Domoticz.Debug(val)

    @classmethod
    def Log(cls, val: str):
        """Write a message to Domoticz log

        Arguments:
            val {str} -- Message to log
        """
        Domoticz.Log(val)

    @classmethod
    def Status(cls, val: str):
        """Write a status message to Domoticz log

        Arguments:
            val {str} -- Message to log
        """
        Domoticz.Status(val)

    @classmethod
    def Error(cls, val: str):
        """Write an error message to Domoticz log

        Arguments:
            val {str} -- Message to log
        """
        Domoticz.Error(val)

    @classmethod
    def Debugging(cls, values: List[DomoticzDebugLevel]):
        """Set logging level and type for debugging. Multiple values are supported.
        Mask values can be added together, for example to see debugging details around the plugin and its objects use: Domoticz.Debugging(62) # 2+4+8+16+32

        Arguments:
            values {List[DomoticzDebugLevel]} -- List of debug levels to logically-OR together
        """
        if values is int:
            Domoticz.Debugging(values)
        elif DomoticzDebugLevel.ShowNone in values:
            Domoticz.Debugging(0)
        elif DomoticzDebugLevel.ShowNone in values:
            Domoticz.Debugging(1)
        else:
            Domoticz.Debugging(sum(values))

    @classmethod
    def Heartbeat(cls, val: int):
        """Set the heartbeat interval in seconds, default 10 seconds.
        Values greater than 30 seconds will cause a message to be regularly logged about the plugin not responding. The plugin will actually function correctly with values greater than 30 though.

        Arguments:
            val {int} -- Heartbeat interval in seconds
        """
        Domoticz.Heartbeat(val)

    @classmethod
    def Notifier(cls, name: string):
        """Informs the plugin framework that the plugin's external hardware can consume Domoticz Notifications.
        When the plugin is active the supplied Name will appear as an additional target for Notifications in the standard Domoticz device notification editing page. The plugin framework will then call the onNotification callback when a notifiable event occurs.

        Arguments:
            name {string} -- Domoticz Notifications target name
        """
        Domoticz.Notifier(name)

    @classmethod
    def Trace(cls, val: bool = False):
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
        Domoticz.Trace(val)

    @classmethod
    def Configuration(cls, val: Dict[str, str] = None) -> Dict[str, str]:
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
        return Domoticz.Configuration(val)


# DomoticzImages: Dict[str, DomoticzImage] = Images


# DomoticzSettings: Dict[str, str] = Settings
# """Contents of the Domoticz Settings page as found in the Preferences database table. These are always available and will be updated if the user changes any settings. The plugin is not restarted. They can be accessed by name for example: Settings["Language"]

#     Returns:
#         Dict[str, str] -- Contents of the Domoticz Settings page as found in the Preferences database table. These are always available and will be updated if the user changes any settings. The plugin is not restarted. They can be accessed by name for example: Settings["Language"]
#     """


# DomoticzParameters: Dict[DomoticzPluginParameter, str] = Parameters
# """These are always available and remain static for the lifetime of the plugin. They can be accessed by name for example: Parameters["SerialPort"]

#     Returns:
#         Dict[DomoticzPluginParameter, str] -- These are always available and remain static for the lifetime of the plugin. They can be accessed by name for example: Parameters["SerialPort"]
#     """


# DomoticzDevices: Dict[int, DomoticzDevice] = Devices
# """Dictionary of device ids to device objects

#     Returns:
#         Dict[int, DomoticzDevice] -- Dictionary of device ids to device objects
#     """


class DeviceParam:
    """The string and numeric values, and unit name of a measurement"""

    def __init__(self, unit, nValue, sValue):
        self.unit = unit
        self.nValue = nValue
        self.sValue = sValue
