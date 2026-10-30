"""Helpers shared by the tests: temporary workspaces and an in-process web server."""
import json
import os
import shutil
import tempfile
import threading
import urllib.error
import urllib.parse
import urllib.request
from http.server import ThreadingHTTPServer
from pathlib import Path

from ecv import config

FIXTURES = Path(__file__).parent / "fixtures"


class TemporaryWorkspace:
    """A copy of a real domain (definition and inventories, phase 0 accepted) in a temporary folder of domains,
    with its own global queue and log folder; the ECV_CAMINHO_* variables point there while it is active."""

    VARIABLES = ("DOMINIOS", "PEDIDOSGLOBAIS", "REGISTOS")

    def __init__(self, domain_id="iot"):
        self.domain_id = domain_id

    def __enter__(self):
        self.root = Path(tempfile.mkdtemp(prefix="ecv-test-"))
        source = config.path("dominios") / self.domain_id
        target = self.root / "dominios" / self.domain_id
        target.mkdir(parents=True)
        shutil.copy(source / "dominio.json", target / "dominio.json")
        shutil.copytree(source / "inventario", target / "inventario")
        (target / "estado.json").write_text(json.dumps({"dominio": self.domain_id, "passos": {"0": {"estado": "aceite"}}}), encoding="utf-8")
        self._saved = {v: os.environ.get(f"ECV_CAMINHO_{v}") for v in self.VARIABLES}
        os.environ["ECV_CAMINHO_DOMINIOS"] = str(self.root / "dominios")
        os.environ["ECV_CAMINHO_PEDIDOSGLOBAIS"] = str(self.root / "pedidos")
        os.environ["ECV_CAMINHO_REGISTOS"] = str(self.root / "registos")
        return self

    def __exit__(self, *exc):
        for v, value in self._saved.items():
            if value is None:
                os.environ.pop(f"ECV_CAMINHO_{v}", None)
            else:
                os.environ[f"ECV_CAMINHO_{v}"] = value
        shutil.rmtree(self.root, ignore_errors=True)

    @property
    def domain_folder(self):
        return self.root / "dominios" / self.domain_id


class TestServer:
    """The web application on a free port, in a thread."""

    def __init__(self, scope="exemplos"):
        from ecv.webapp.routes import ROUTES
        from ecv.webapp.server import EcvRequestHandler, Router, make_app
        self.app = make_app("memoria", scope, log_file=False, echo=False)
        EcvRequestHandler.app = self.app
        EcvRequestHandler.router = Router(ROUTES)
        self.httpd = ThreadingHTTPServer(("127.0.0.1", 0), EcvRequestHandler)
        self.base = f"http://127.0.0.1:{self.httpd.server_address[1]}"
        threading.Thread(target=self.httpd.serve_forever, daemon=True).start()

    def close(self):
        self.httpd.shutdown()
        self.httpd.server_close()

    def upload(self, path, fields, files):
        """POST multipart/form-data: fields {name: value}, files [(field, file name, bytes)]. (status, text, final url)"""
        boundary = "ecvtestboundary"
        parts = [f'--{boundary}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode() for k, v in fields.items()]
        parts += [f'--{boundary}\r\nContent-Disposition: form-data; name="{k}"; filename="{n}"\r\nContent-Type: application/octet-stream\r\n\r\n'.encode()
                  + data + b"\r\n" for k, n, data in files]
        body = b"".join(parts) + f"--{boundary}--\r\n".encode()
        req = urllib.request.Request(self.base + path, body, {"Content-Type": f"multipart/form-data; boundary={boundary}"})
        try:
            with urllib.request.urlopen(req) as r:
                return r.status, r.read().decode("utf-8"), r.url
        except urllib.error.HTTPError as e:
            return e.code, e.read().decode("utf-8"), e.url

    def request(self, path, data=None, json_body=None):
        """(status, text, final url). data: form fields (POST); json_body: JSON (POST)."""
        body, headers = None, {}
        if json_body is not None:
            body, headers = json.dumps(json_body).encode("utf-8"), {"Content-Type": "application/json"}
        elif data is not None:
            body = urllib.parse.urlencode(data).encode("utf-8")
        req = urllib.request.Request(self.base + path, body, headers)
        try:
            with urllib.request.urlopen(req) as r:
                return r.status, r.read().decode("utf-8"), r.url
        except urllib.error.HTTPError as e:
            return e.code, e.read().decode("utf-8"), e.url

    def json(self, path, json_body=None):
        status, text, _ = self.request(path, json_body=json_body)
        return status, json.loads(text)
