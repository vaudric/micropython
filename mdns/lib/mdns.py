"""
mDNS (slimDNS)

Special thanks to @nickovs, @peterhinch (pythoncoder), @ameersohail0
* https://forum.micropython.org/viewtopic.php?t=3027
* https://forum.micropython.org/viewtopic.php?f=15&t=4398
* https://github.com/nickovs/slimDNS/blob/master/slimDNS.py

Ideally slimDNS should be asyncio ready at the core...
Not pretty but it works...

"""

from select import select
import network
import uasyncio as asyncio
from slimDNS import SlimDNSServer as SlimDNSServerBase


class SlimDNSServer(SlimDNSServerBase):
    async def serve(self):
        while True:
            readers, _, _ = select([self.sock], [], [], None)
            self.process_waiting_packets()
            await asyncio.sleep_ms(100) # Adding a delay 100ms instead of 0 significantly improved connection perf on Picoweb...

    def run(self):
        loop = asyncio.get_event_loop()
        loop.create_task(self.serve())
        loop.run_forever()

if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
        local_addr = wlan.ifconfig()[0]
        mdns_server = SlimDNSServer(wlan.ifconfig()[0], "esp8266-upy")
        mdns_server.run()
        print('mDNS running...')
    except KeyboardInterrupt:
        del mdns_server
        loop.stop()
        loop.close()
        del loop
        print('Program ends!')
    finally:
        _ = asyncio.new_event_loop()
