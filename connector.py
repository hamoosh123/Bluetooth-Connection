import asyncio
import logging
import platform
from bleak import discover, BleakClient
from bleak import _logger as logger
from bleak.uuids import uuid16_dict

SERVICE = "fe84"
RECEIVE = "2d30c082f39f4ce6923f3484ea480596"
SEND = "2d30c083f39f4ce6923f3484ea480596"
DISCONNECT = "2d30c084f39f4ce6923f3484ea480596"


# Discover devices
async def run():
    devices = await discover()
    nb_devices = len(devices)
    if nb_devices < 1:
        print("No BLE devices found. Check connectivity.")
        return ""
    else:
        for d in devices:
            print(d)


loop = asyncio.get_event_loop()
loop.run_until_complete(run())

# Ganglion = FC:CE:40:31:60:1C: Ganglion-87f1

# Add notifications to characteristic / handle responses
CHARACTERISTIC_UUID = (
    "2d30c082-f39f-4ce6-923f-3484ea480596"
)  # From OpenBCI ganglion.py


def notification_handler(sender, data):
    print("{0}: {1}".format(sender, data))


async def run(address, loop, debug=False):
    if debug:
        import sys
        l = logging.getLogger("asyncio")
        l.setLevel(logging.DEBUG)
        h = logging.StreamHandler(sys.stdout)
        h.setLevel(logging.DEBUG)
        l.addHandler(h)
        logger.addHandler(h)
    async with BleakClient(address, loop=loop) as client:
        x = await client.is_connected()
        logger.info("Connected: {0}".format(x))
        await client.start_notify(CHARACTERISTIC_UUID, notification_handler)
        await asyncio.sleep(5.0, loop=loop)
        await client.stop_notify(CHARACTERISTIC_UUID)

if __name__ == "__main__":
    import os
    os.environ["PYTHONASYNCIODEBUG"] = str(1)
    address = (
        "FC:CE:40:31:60:1C"
    )
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(address, loop, True))



