"""Request and response objects, independent of http.server (the handlers only see these)."""
import email.parser
import email.policy
import json
import urllib.parse
from dataclasses import dataclass, field


class HttpError(Exception):
    def __init__(self, status, message):
        super().__init__(message)
        self.status = status
        self.message = message


def not_found(message="não existe"):
    return HttpError(404, message)


def bad_request(message):
    return HttpError(400, message)


@dataclass
class Request:
    method: str
    path: str
    query: dict = field(default_factory=dict)
    headers: dict = field(default_factory=dict)
    body: bytes = b""
    params: dict = field(default_factory=dict)        # filled by the router from the route pattern

    @classmethod
    def parse(cls, method, raw_path, headers, body):
        url = urllib.parse.urlparse(raw_path)
        query = {k: v[-1] for k, v in urllib.parse.parse_qs(url.query, keep_blank_values=True).items()}
        return cls(method, urllib.parse.unquote(url.path), query, dict(headers), body)

    @property
    def is_json(self):
        return "application/json" in self.headers.get("Content-Type", "")

    @property
    def wants_json(self):
        return self.path.startswith("/api/") or "application/json" in self.headers.get("Accept", "")

    def text(self):
        return self.body.decode("utf-8")

    @property
    def is_multipart(self):
        return "multipart/form-data" in self.headers.get("Content-Type", "")

    def _parts(self):
        """The parts of a multipart/form-data body: (field name, file name or None, bytes)."""
        head = f"Content-Type: {self.headers.get('Content-Type')}\r\nMIME-Version: 1.0\r\n\r\n".encode()
        message = email.parser.BytesParser(policy=email.policy.HTTP).parsebytes(head + self.body)
        for part in message.iter_parts():
            yield part.get_param("name", header="content-disposition"), part.get_filename(), part.get_payload(decode=True) or b""

    def form(self):
        """The form fields of a POST (application/x-www-form-urlencoded or multipart/form-data, without the files)."""
        if self.is_multipart:
            return {name: data.decode("utf-8") for name, filename, data in self._parts() if filename is None}
        return {k: v[-1] for k, v in urllib.parse.parse_qs(self.text(), keep_blank_values=True).items()}

    def files(self):
        """The files of a multipart/form-data POST: [(field name, file name, bytes)] (empty file fields left out)."""
        if not self.is_multipart:
            return []
        return [(name, filename, data) for name, filename, data in self._parts() if filename]

    def json(self):
        try:
            return json.loads(self.text() or "{}")
        except ValueError as e:
            raise bad_request(f"JSON inválido: {e}") from e

    def data(self):
        """The fields of the request: JSON body or form, plus the query string."""
        fields = dict(self.query)
        if self.method == "POST":
            body = self.json() if self.is_json else self.form()
            if isinstance(body, dict):
                fields.update(body)
            else:
                fields["corpo"] = body
        return fields

    def get(self, name, default=None):
        return self.params.get(name) or self.query.get(name) or default


@dataclass
class Response:
    status: int = 200
    body: bytes = b""
    content_type: str = "text/html; charset=utf-8"
    headers: dict = field(default_factory=dict)
    note: str = ""                                     # short text for the request log

    @classmethod
    def html(cls, text, status=200, note=""):
        return cls(status, text.encode("utf-8"), note=note)

    @classmethod
    def json(cls, data, status=200, note=""):
        text = json.dumps(data, ensure_ascii=False, indent=1, default=str)
        return cls(status, text.encode("utf-8"), "application/json; charset=utf-8", note=note)

    @classmethod
    def text(cls, text, content_type="text/plain; charset=utf-8", status=200, filename=None):
        headers = {"Content-Disposition": f'inline; filename="{filename}"'} if filename else {}
        return cls(status, text.encode("utf-8"), content_type, headers)

    @classmethod
    def redirect(cls, location, note=""):
        return cls(303, b"", headers={"Location": location}, note=note)


def url(path, **query):
    query = {k: v for k, v in query.items() if v not in (None, "")}
    if not query:
        return path
    return path + ("&" if "?" in path else "?") + urllib.parse.urlencode(query)
