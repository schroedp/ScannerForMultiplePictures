import sys
import traceback

from PIL import Image
import numpy
import gi


gi.require_version("Libinsane", "1.0")

from gi.repository import Libinsane


class scanner:

    def init_api(self):
        return Libinsane.Api.new_safebet()  # Initialisieren der API, returns api object

    # def list_devices(api):
    #     print("Looking for scan devices ...")
    #     devs = api.list_devices(Libinsane.DeviceLocations.ANY)
    #     print("Found {} devices".format(len(devs)))
    #     devices = []
    #     for dev in devs:
    #         devices.append(dev.to_string())
    #     return devices


     # def get_devices(api, dev_id=None):
     #     if dev_id is None:
     #         print("Looking for scan devices ...")
     #         devs = api.list_devices(Libinsane.DeviceLocations.ANY)
     #         print("Found {} devices".format(len(devs)))
     #         for dev in devs:
     #             print("[{}] : [{}]".format(dev.get_dev_id(), dev.to_string()))
     #         dev_id = devs[0].get_dev_id()
     #     print("Will use device {}".format(dev_id))
     #     dev = api.get_device(dev_id)
     #     print("Using device {}".format(dev.get_name()))
     #     return dev

    # def get_devices(api, dev_id=None):
    #     if dev_id is None:
    #         print("Looking for scan devices ...")
    #         dev_objects = api.list_devices(Libinsane.DeviceLocations.ANY)
    #         print("Found {} devices".format(len(dev_objects)))
    #         devs = []
    #         for dev_object in dev_objects:
    #             print("[{}] : [{}]".format(dev_object.get_dev_id(), dev_object.to_string()))
    #             devs.append(api.get_device(dev_object.get_dev_id()))
    #         return devs

    def get_device_descriptors(self, api):
        return api.list_devices(Libinsane.DeviceLocations.ANY)

    def get_device_name(self, device_descriptor):
        return device_descriptor.get_dev_vendor() + " " + device_descriptor.get_dev_model()

    def get_device_object(self, api, device_descriptor):
        return api.get_device(device_descriptor.get_dev_id())

    def get_scan_sources(self, device_object):
        return device_object.get_children()

    def get_options(self, scan_source):
        return scan_source.get_options()


    # def get_source(dev, source_name):
    #     print("Looking for scan sources ...")
    #     sources = dev.get_children()
    #     print("Available scan sources:")
    #     for src in sources:
    #         print("- {}".format(src.get_name()))
    #         if src.get_name() == source_name:
    #             source = src
    #             break
    #         else:
    #             if source_name is None:
    #                 source = sources[0] if len(sources) > 0 else dev
    #             elif source_name == "root":
    #                 source = dev
    #             else:
    #                 print("Source '{}' not found".format(source_name))
    #                 sys.exit(2)
    #         print("Will use scan source {}".format(source.get_name()))
    #         return source


    # def list_opts(item):
    #     opts = item.get_options()
    #     print("Options:")
    #     for opt in opts:
    #         try:
    #             print("- {}={} ({})".format(
    #                 opt.get_name(), opt.get_value(), opt.get_constraint()
    #             ))
    #         except Exception as exc:
    #             print("Failed to read option {}: {}".format(
    #                 opt.get_name(), str(exc)
    #             ))
    #     print("")


    def set_option(self, item, opt_name, opt_value):
        try:
            print("Setting {} to {}".format(opt_name, opt_value))
            opts = item.get_options()
            opts = {opt.get_name(): opt for opt in opts}
            if opt_name not in opts:
                print("Option '{}' not found".format(opt_name))
                return
            print("- Old {}: {}".format(opt_name, opts[opt_name].get_value()))
            print("- Allowed values: {}".format(opts[opt_name].get_constraint()))
            set_flags = opts[opt_name].set_value(opt_value)
            print("- Set flags: {}".format(set_flags))
            opts = item.get_options()
            opts = {opt.get_name(): opt for opt in opts}
            print("- New {}: {}".format(opt_name, opts[opt_name].get_value()))
        except Exception as exc:
            print("Failed to set {} to {}: {}".format(
                opt_name, opt_value, str(exc)
            ))
            traceback.print_exc()
        finally:
            print("")


    def scan(self, source, output_file):
        session = source.scan_start()
        try:
            page_nb = 0
            while not session.end_of_feed() and page_nb < 20:
                # Do not assume that all the pages will have the same size !
                scan_params = session.get_scan_parameters()
                print("Expected scan parameters: {} ; {}x{} = {} bytes".format(
                    scan_params.get_format(),
                    scan_params.get_width(), scan_params.get_height(),
                    scan_params.get_image_size()))
                total = scan_params.get_image_size()
                img = []
                r = 0
                if output_file is not None:
                    out = output_file.format(page_nb)
                else:
                    out = None
                print("Scanning page {} --> {}".format(page_nb, out))
                while not session.end_of_page():
                    data = session.read_bytes(128 * 1024)
                    data = data.get_data()
                    img.append(data)
                    r += len(data)
                    print("Got {} bytes => {}/{} bytes".format(
                        len(data), r, total)
                    )
                img = b"".join(img)
                print("Got {} bytes".format(len(img)))
                if out is not None:
                    print("Saving page as {} ...".format(out))
                    if scan_params.get_format() == Libinsane.ImgFormat.RAW_RGB_24:
                        print("Reached Extraction:")
                        img = self.raw_to_img(scan_params, img)
                        img.save(out, format="PNG")
                    else:
                        print("Warning: output format is {}".format(
                            scan_params.get_format()
                        ))
                        with open(out, 'wb') as fd:
                            fd.write(img)
                page_nb += 1
                print("Page {} scanned".format(page_nb))
            if page_nb == 0:
                print("No page in feeder ?")
        finally:
            session.cancel()

    def raw_to_img(self, params, img_bytes):
        fmt = params.get_format()
        assert (fmt == Libinsane.ImgFormat.RAW_RGB_24)
        (w, h) = (
            params.get_width(),
            int(len(img_bytes) / 3 / params.get_width())
        )
        print("Mode: RGB : Size: {}x{}".format(w, h))

        return Image.frombuffer("RGB", (w, h), img_bytes, "raw", "RGB", 0, 1)


# scanner = scanner()
# api = scanner.init_api()
# device_descriptors = scanner.get_device_descriptors(api) #gibt device descriptors zurück != dev bzw. item
# print(scanner.get_device_name(device_descriptors[0]))
# device_object = scanner.get_device_object(api, device_descriptors[0]) # gibt device-object/item zurück
# scan_sources = scanner.get_scan_sources(device_object)
# for scan_source in scan_sources:
#     print(scan_source.get_name())
#     options = scanner.get_options(scan_source)
#     for option in options:
#         try:
#             print("- {}={} ({})".format(option.get_name(), option.get_value(), option.get_constraint()))
#         except Exception as exc:
#             print("Failed to read option {}: {}".format(option.get_name(), str(exc)))
#
# scanner.scan(scan_sources[0], "C:\\Users\\Technician\\out.png")
