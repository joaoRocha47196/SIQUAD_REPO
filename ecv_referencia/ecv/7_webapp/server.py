"""The HTTP server: routing, logging and error handling around the handlers.

Each request: the AppContext refreshes the database if the declaration files changed, the router finds
the route (routes.py), the handler returns a Response, and one line goes to the log. Errors the user
can fix (EcvError, HttpError) become a page or a JSON {"erro": ...}; anything else is logged with
its traceback and answered with 500.
"""
import re
import time
import traceback
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from ecv import config
from ecv.shared.errors import EcvError

from .context import AppContext
from .http import HttpError, Request, Response
from .logs import ServerLog
from .pages.layout import error_page
from .routes import ROUTES


class Router:
    def __init__(self, routes):
        self.routes = [(r, re.compile("^" + re.sub(r"<(\w+)>", r"(?P<\1>[^/]+)", r.path) + "$")) for r in routes]

    def match(self, method, path):
        """(route, parameters), or (None, None) when no route has this path, or (None, {}) for a wrong method."""
        path_exists = False
        for route, pattern in self.routes:
            m = pattern.match(path)
            if m:
                path_exists = True
                if route.method == method:
                    return route, m.groupdict()
        return None, ({} if path_exists else None)


class EcvRequestHandler(BaseHTTPRequestHandler):
    app = None            # AppContext
    router = None
    server_version = "ECV"

    def log_message(self, fmt, *args):     # the ServerLog replaces the default stderr lines
        pass

    def do_GET(self):
        self._handle("GET")

    def do_POST(self):
        self._handle("POST")

    def _handle(self, method):
        start = time.time()
        length = int(self.headers.get("Content-Length") or 0)
        request = Request.parse(method, self.path, self.headers, self.rfile.read(length) if length else b"")
        response = self._dispatch(request)
        self._send(response)
        self.app.log.request(method, self.path, response.status, (time.time() - start) * 1000, len(response.body), response.note)

    def _dispatch(self, request):
        route, params = self.router.match(request.method, request.path)
        try:
            if route is None:
                raise HttpError(405 if params == {} else 404, f"{request.method} {request.path} não existe (ver /rotas)")
            request.params = params
            self.app.refresh()
            return route.handler(self.app, request)
        except (EcvError, HttpError, KeyError, ValueError) as e:
            status = e.status if isinstance(e, HttpError) else 400
            message = e.message if isinstance(e, HttpError) else str(e)
            return self._error(request, status, message)
        except Exception as e:  # noqa: BLE001 - logged with the traceback and shown as 500
            self.app.log.error(f"{request.method} {request.path}: {e!r}\n{traceback.format_exc()}")
            return self._error(request, 500, repr(e))

    def _error(self, request, status, message):
        if request.wants_json:
            return Response.json({"erro": message}, status, note=message[:120])
        return Response.html(error_page(self.app, status, message), status, note=message[:120])

    def _send(self, response):
        self.send_response(response.status)
        self.send_header("Content-Type", response.content_type)
        self.send_header("Content-Length", str(len(response.body)))
        for key, value in response.headers.items():
            self.send_header(key, value)
        self.end_headers()
        self.wfile.write(response.body)


def make_app(backend="memoria", scope="exemplos", log_file=None, echo=True, **neo4j):
    from ecv.graph.database import GraphDatabase
    if log_file is None:
        log_file = config.path("registos") / "servidor.log"
    log = ServerLog(log_file or None, echo=echo)
    database = GraphDatabase(backend, **neo4j)
    return AppContext(database, log, scope)


def serve(app, host=None, port=None):
    host = host or config.SERVER["endereco"]
    port = port or config.SERVER["porta"]
    EcvRequestHandler.app = app
    EcvRequestHandler.router = Router(ROUTES)
    httpd = ThreadingHTTPServer((host, port), EcvRequestHandler)
    app.log.event(f"servidor em http://{host}:{port}/ — backend {app.database.backend}, âmbito {app.scope_name}, {len(ROUTES)} rotas")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()
        app.database.close()
