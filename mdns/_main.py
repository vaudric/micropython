"""
mDNS (slimDNS) + WebServer (Picoweb)

Not pretty but it works...

- picoweb > mpy-cross
- slimDNS > mpy-cross
extend slimDNSServer to add "virtual" asyncio "support"

Run and go to http://esp8266-upy.local
"""

import uasyncio as asyncio
import picoweb
from mdns import SlimDNSServer
from httpd import WebApp

mdns_server = None
while True:
    try:
        from mdns import SlimDNSServer    
        mdns_server = SlimDNSServer(wlan.ifconfig()[0], "esp8266-upy")
        break
    except OSError:
        continue

app = WebApp(__name__)


@app.route("/")
def index(req, resp):
    yield from picoweb.start_response(resp)
    yield from resp.awrite("This is a webapp")


async def check_free_mem():
    while True:
        gc.collect()
        print('Free MEM: {}'.format(gc.mem_free()))
        gc.collect()
        await asyncio.sleep(5)

def run():
    loop = asyncio.get_event_loop()
    loop.create_task(mdns_server.serve())
    app.run(debug=True, host="0.0.0.0", port=80, main_loop=False)
    loop.create_task(check_free_mem())
    loop.run_forever()


try:
    run()
except KeyboardInterrupt:
    print('Program ends!')
finally:
    del mdns_server, app
    _ = asyncio.new_event_loop()
