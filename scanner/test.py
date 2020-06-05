import scan
import gi
gi.require_version("Libinsane", "1.0")
from gi.repository import Libinsane

api = Libinsane.Api.new_safebet()

dev = scan.get_devices(api)
source = scan.get_source(dev, "flatbed")
scan.scan(source, "C:\\Users\\Technician\\out.png")
