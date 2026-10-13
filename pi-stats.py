#!/usr/bin/env python3
"""Kleiner Helfer für das Smarthome-Dashboard (nur Python-Standardbibliothek).

  http://localhost:8765/stats                    -> CPU, RAM, Disk, Temperatur, Netzwerk, Laufzeit als JSON
  http://localhost:8765/snapshot?entity=camera.x -> aktuelles Kamerabild aus Home Assistant (für die Türklingel)

Start:   HA_URL=http://homeassistant.local:8123 HA_TOKEN=dein_token python3 pi-stats.py
Ohne HA_URL/HA_TOKEN laufen nur die Systemwerte, der Kamera-Snapshot ist dann aus.
"""
import json, os, shutil, threading, time, urllib.error, urllib.parse, urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HA_URL = os.environ.get("HA_URL", "").rstrip("/")
HA_TOKEN = os.environ.get("HA_TOKEN", "")
HOST = os.environ.get("STATS_HOST", "127.0.0.1")
PORT = int(os.environ.get("STATS_PORT", "8765"))

stats = {"cpu": 0.0, "ram": 0.0, "disk": 0.0, "temp": None, "load": 0.0, "rx": 0.0, "tx": 0.0, "uptime": 0}


def read_cpu():
    with open("/proc/stat") as f:
        v = [int(x) for x in f.readline().split()[1:]]
    return sum(v), v[3] + v[4]  # gesamt, idle + iowait


def read_net():
    rx = tx = 0
    with open("/proc/net/dev") as f:
        for line in list(f)[2:]:
            name, data = line.split(":", 1)
            if name.strip() == "lo":
                continue
            d = data.split()
            rx, tx = rx + int(d[0]), tx + int(d[8])
    return rx, tx


def sampler():
    last_cpu, last_net, last_t = read_cpu(), read_net(), time.time()
    while True:
        time.sleep(1)
        now = time.time()
        try:
            cpu, net = read_cpu(), read_net()
            dt = max(now - last_t, 0.001)
            dtot, didle = cpu[0] - last_cpu[0], cpu[1] - last_cpu[1]
            stats["cpu"] = round(100 * (dtot - didle) / dtot, 1) if dtot else 0.0
            stats["rx"] = round((net[0] - last_net[0]) / 1024 / dt, 1)  # kB/s
            stats["tx"] = round((net[1] - last_net[1]) / 1024 / dt, 1)
            last_cpu, last_net, last_t = cpu, net, now
            mem = {}
            with open("/proc/meminfo") as f:
                for line in f:
                    k, v = line.split(":")
                    mem[k] = int(v.split()[0])
            stats["ram"] = round(100 * (1 - mem["MemAvailable"] / mem["MemTotal"]), 1)
            du = shutil.disk_usage("/")
            stats["disk"] = round(100 * du.used / du.total, 1)
            stats["load"] = os.getloadavg()[0]
            with open("/proc/uptime") as f:
                stats["uptime"] = int(float(f.read().split()[0]))
            try:
                with open("/sys/class/thermal/thermal_zone0/temp") as f:
                    stats["temp"] = int(f.read()) / 1000
            except OSError:
                stats["temp"] = None
        except Exception as e:  # nie abstürzen, nur weiter messen
            print("Messfehler:", e)


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body, ctype="application/json"):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self._send(204, b"")

    def do_GET(self):
        url = urllib.parse.urlparse(self.path)
        if url.path == "/stats":
            return self._send(200, json.dumps(stats).encode())
        if url.path == "/snapshot":
            entity = urllib.parse.parse_qs(url.query).get("entity", [""])[0]
            if not (HA_URL and HA_TOKEN and entity.startswith("camera.")):
                return self._send(400, b'{"error":"HA_URL, HA_TOKEN oder camera.* fehlt"}')
            req = urllib.request.Request(
                f"{HA_URL}/api/camera_proxy/{urllib.parse.quote(entity)}",
                headers={"Authorization": f"Bearer {HA_TOKEN}"},
            )
            try:
                with urllib.request.urlopen(req, timeout=8) as r:
                    return self._send(200, r.read(), r.headers.get("Content-Type", "image/jpeg"))
            except (urllib.error.URLError, TimeoutError) as e:
                return self._send(502, json.dumps({"error": str(e)}).encode())
        self._send(404, b'{"error":"nicht gefunden"}')

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    threading.Thread(target=sampler, daemon=True).start()
    print(f"pi-stats läuft auf http://{HOST}:{PORT}  (Kamera-Snapshot: {'an' if HA_URL and HA_TOKEN else 'aus'})")
    ThreadingHTTPServer((HOST, PORT), Handler).serve_forever()
