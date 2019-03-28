# import python dbus module
import dbus
# import python dbus GLib mainloop support
import dbus.mainloop.glib

class wifiController:
    def __init__(self):
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
        bus = self.bus = dbus.SystemBus()
        remote_object = bus.get_object("org.freedesktop.NetworkManager", "/org/freedesktop/NetworkManager")
        self.nm = dbus.Interface(remote_object, "org.freedesktop.NetworkManager")
        
    def filter_wifi(self, dev):
        remote_object = self.bus.get_object("org.freedesktop.NetworkManager", dev)
        iface = dbus.Interface(remote_object, 'org.freedesktop.DBus.Properties')
        m = iface.get_dbus_method("Get", dbus_interface=None)("org.freedesktop.NetworkManager.Device", "DeviceType")
        
        return m==2

    def devices(self):
        devices = self.nm.GetDevices()
        self.wifi = list(filter( self.filter_wifi , devices))
        print(wifi)
        
        
if __name__ == "__main__":
    wifiController().devices()
