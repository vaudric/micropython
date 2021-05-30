import gc
import uasyncio as asyncio
import picoweb


class WebApp(picoweb.WebApp):
    def serve(self, loop, host, port, main_loop=True):
        # Actually serve client connections. Subclasses may override this
        # to e.g. catch and handle exceptions when dealing with server socket
        # (which are otherwise unhandled and will terminate a Picoweb app).
        # Note: name and signature of this method may change.
        loop.create_task(asyncio.start_server(self._handle, host, port))
        if main_loop:
            loop.run_forever()

    def run(self, host="127.0.0.1", port=8081, debug=False, lazy_init=False, log=None, main_loop=True):
        if log is None and debug >= 0:
            import ulogging
            log = ulogging.getLogger("picoweb")
            if debug > 0:
                log.setLevel(ulogging.DEBUG)
        self.log = log
        gc.collect()
        self.debug = int(debug)
        self.init()
        if not lazy_init:
            for app in self.mounts:
                app.init()
        
        loop = asyncio.get_event_loop()
        if debug > 0:
            print("Picoweb Running on http://%s:%s/" % (host, port))
        self.serve(loop, host, port, main_loop=main_loop)
        if main_loop:
            loop.close()
        

if __name__ == "__main__":
    app = picoweb.WebApp(__name__)

    @app.route("/")
    def index(req, resp):
        yield from picoweb.start_response(resp)
        yield from resp.awrite("This is a webapp")

    app.run(debug=True)
