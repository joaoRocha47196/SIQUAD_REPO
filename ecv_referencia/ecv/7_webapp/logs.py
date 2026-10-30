"""The server log: one line per request (method, path, status, time, size, what was done) and the
events of the actions (a request to the LLM created, operations applied, the database rebuilt).

Each entry goes to the console, to registos/servidor.log and to a buffer shown in the Registo tab.
"""
import sys
import threading
import time
from collections import deque
from dataclasses import asdict, dataclass

from ecv import config


@dataclass
class LogEntry:
    time: str
    kind: str              # "pedido" | "evento" | "erro"
    text: str
    method: str = ""
    path: str = ""
    status: int = 0
    ms: float = 0.0
    size: int = 0

    def line(self):
        if self.kind == "pedido":
            return f"{self.time} {self.method:4} {self.path} -> {self.status} ({self.ms:.0f} ms, {self.size} B){'  ' + self.text if self.text else ''}"
        return f"{self.time} [{self.kind}] {self.text}"


class ServerLog:
    def __init__(self, file=None, capacity=None, echo=True):
        self.entries = deque(maxlen=capacity or config.SERVER["linhasRegistoEmMemoria"])
        self.file = file
        self.echo = echo
        self._lock = threading.Lock()
        if file:
            file.parent.mkdir(parents=True, exist_ok=True)

    def _add(self, entry):
        with self._lock:
            self.entries.append(entry)
            line = entry.line()
            if self.echo:
                print(line, file=sys.stderr, flush=True)
            if self.file:
                with open(self.file, "a", encoding="utf-8") as f:
                    f.write(line + "\n")

    @staticmethod
    def _now():
        return time.strftime("%Y-%m-%d %H:%M:%S")

    def request(self, method, path, status, ms, size, text=""):
        self._add(LogEntry(self._now(), "pedido", text, method, path, status, ms, size))

    def event(self, text):
        self._add(LogEntry(self._now(), "evento", text))

    def error(self, text):
        self._add(LogEntry(self._now(), "erro", text))

    def recent(self, n=200, kind=None):
        items = [e for e in self.entries if kind is None or e.kind == kind]
        return [asdict(e) for e in reversed(items[-n:])]
