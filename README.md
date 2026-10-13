# Smarthome Dashboard

Ein modernes Wand-Dashboard für Home Assistant. Es besteht aus **einer einzigen Datei** (`index.html`), die direkt im Browser läuft. Es braucht kein Build und keinen Webserver.

**Das Dashboard zeigt:**

- Räume mit Temperatur, Luftfeuchte, CO₂, Licht und Bewegung
- Einen Grundriss mit allen **Lampen** (an/aus), **Fenstern** (offen/zu) und dem, was gerade **läuft** (Musik)
- **Läuft gerade:** Musik mit Titel und Cover sowie laufende Geräte (Waschmaschine usw.)
- **Fenster-Warnung:** Steht ein Fenster offen und es regnet, schneit oder ist zu kalt, wird die Anzeige rot, und es kommt ein Hinweis
- **Anwesenheit:** Wer ist zu Hause. Sind alle unterwegs, warnt das Dashboard vor offenen Fenstern und eingeschalteten Lichtern
- **Wetter-Vorschau:** Die nächsten Stunden mit Temperatur und Regenwahrscheinlichkeit. Kündigt sich Regen an, warnt die Fensterwarnung schon vorher („Regen bald“)
- **Batterie-Warnung:** Findet alle Batterie-Sensoren in Home Assistant selbst und warnt unter 20 %
- **Lüften-Empfehlung:** Bei hohem CO₂ oder hoher Luftfeuchte, wenn es draußen passt und im Raum kein Fenster offen ist
- **Display aus bei Abwesenheit:** Sind alle länger als 10 Minuten unterwegs, schaltet der Pi den Bildschirm wirklich aus und bei Heimkehr oder Bewegung wieder an
- **Bildschirm dimmen:** Nachts ohne Bewegung dunkelt das Display ab und wird bei Bewegung, Alarm, Klingel oder Berührung sofort wieder hell
- **Müll am Vorabend:** Ab 19 Uhr erinnert das Dashboard an die Tonne, wenn morgen abgeholt wird
- **Daten veraltet:** Kommt nichts mehr von Home Assistant, wird die Anzeige abgedunkelt und „Keine Daten seit …“ erscheint, statt alte Werte als aktuell zu zeigen
- **Seiten-Wechsel:** Die Hauptseite wechselt mit einer ruhigen Ansicht (große Uhr, Wetter, Termine, Müll)
- **Wartung:** Neustart der Seite jede Nacht und Burn-in-Schutz (Inhalt wandert minimal)
- **Steuerung vom Handy:** Knöpfe für Licht, Szenen, Skripte, Schloss und Saugroboter (nur auf Touch-Geräten)
- **Saugroboter:** Zustand und Akku von `vacuum.*`-Geräten (z. B. Dreame) unter „Läuft gerade“, mit Fehlermeldung
- **Gäste-WLAN als QR-Code:** Gäste scannen ihn mit der Handy-Kamera und sind verbunden, ohne das Passwort zu tippen
- **Homelab-Seite:** Hypervisoren, Synology-Speicher, Dienste, Backup und USV auf einer eigenen Seite, mit roter Warnzeile auf der Hauptseite bei Problemen
- Alarme (Rauch, Wasser, Tür) mit rotem Banner und pulsierendem Rand
- Türklingel mit Kamerabild im Vordergrund
- Luftqualität, Termine, Müllabfuhr, Pi-hole, Netzwerkverkehr und Pi-Systemwerte
- **Tag-/Nacht-Design:** Ab 18:00 Uhr blendet das Design über eine Stunde langsam in den Dunkelmodus und morgens wieder zurück

## Voraussetzungen

- Eine laufende [Home Assistant](https://www.home-assistant.io/)-Instanz im selben Netzwerk
- Ein Browser (Chrome, Chromium, Firefox, Safari)
- Optional: ein Raspberry Pi mit Bildschirm als Wand-Display

## Installation

### 1. Repository holen

```bash
git clone https://github.com/theslasher5g/smarthome.git
cd smarthome
```

### 2. Home-Assistant-Token erstellen

In Home Assistant: **Profil** (unten links) → **Sicherheit** → **Langzeit-Zugriffstoken** → **Token erstellen**. Kopiere den Token sofort, er wird nur einmal angezeigt.

### 3. `index.html` anpassen

Öffne `index.html` in einem Editor und suche den Block `HIER ANPASSEN` (ganz oben im `<script>`).

| Einstellung | Bedeutung |
|---|---|
| `url` | `ws://homeassistant.local:8123/api/websocket` (bei HTTPS: `wss://…`) |
| `token` | Dein Langzeit-Zugriffstoken |
| `rooms` | Räume mit Temperatur-, Feuchte-, Bewegungs-, Licht- und CO₂-Sensor |
| `lights` | Lampen mit Position im Grundriss |
| `windows` | Fenster- und Türkontakte mit Position im Grundriss |
| `windowWarn` | Warnung bei offenem Fenster: Regen/Schnee, Kälte unter `coldBelow` °C, Wiederholung alle `repeatMin` Minuten |
| `people` | Personen (`person.*`) für die Anwesenheit |
| `forecast` | Wetter-Vorschau: Anzahl der Stunden und Aktualisierung |
| `battery` | Schwellwert `warn` in %, `exclude` (z. B. Handy-Akkus) und `extra` für Sensoren von Hand |
| `ventilate` | Lüften-Empfehlung, `minOutside` = kälteste Außentemperatur dafür |
| `dim` | Bildschirm dimmen: `afterMin`, `level` (0 bis 1), `onlyNight` |
| `garbageEveningHour` | Ab dieser Uhrzeit (Stunde) Müll-Erinnerung am Vorabend |
| `staleSec` | Nach so vielen Sekunden ohne Daten gilt die Anzeige als veraltet |
| `maintenance` | Nächtlicher Neustart (`reloadAt`) und `burnIn` |
| `pages` | Seiten-Wechsel: `mainSec` Hauptseite, `ambientSec` ruhige Ansicht |
| `controls` | Knöpfe für die Steuerung vom Handy |
| `guestWifi` | Gäste-WLAN: `ssid`, `password`, `encryption` (`WPA`, `WEP`, `nopass`), `hidden`, `showPassword` |
| `homelab` | Homelab-Seite: `servers`, `nas`, `services`, `backup`, `ups` und `warn` |
| `media` / `devices` | Musikplayer und Geräte für „Läuft gerade“ |
| `alarms` | Rauch-, Wasser- und Türmelder |
| `pihole`, `weather`, `calendars`, `garbage` | Optionale Info-Kacheln |
| `theme` | Tag-/Nacht-Verhalten (siehe unten) |

Die Entity-IDs findest du in Home Assistant unter **Einstellungen → Geräte & Dienste → Entitäten**. Nicht benötigte Einträge lässt du weg oder löschst sie. Die jeweilige Karte oder Kachel verschwindet dann.

### 4. Lampen und Fenster im Grundriss platzieren

Jede Lampe und jedes Fenster hat `x` und `y`. Das sind Punkte im Grundriss:

1. Öffne das Dashboard.
2. **Klicke auf die gewünschte Stelle im Grundriss.** Unten rechts erscheint ein Hinweis mit den Koordinaten, z. B. `x: 230, y: 120`.
3. Trage die Werte in `lights` oder `windows` ein.

Bei Fenstern gibt `dir` die Richtung der Wand an: `'v'` für eine senkrechte Wand und `'h'` für eine waagerechte. Mit `plan: 'wohnen'` bei einer Lampe wird zusätzlich der ganze Raum getönt, wenn sie an ist. Mögliche Raum-Kürzel sind `z1`, `z2`, `z3`, `bad`, `wc`, `flur`, `wohnen`, `kueche`, `reduit` und `balkon`.

### 5. Starten

Die Datei kann direkt geöffnet werden: Doppelklick auf `index.html` oder

```bash
chromium-browser --kiosk --noerrdialogs --disable-infobars file:///home/pi/smarthome/index.html
```

Alternativ mit einem kleinen Webserver:

```bash
python3 -m http.server 8080      # dann http://localhost:8080 öffnen
```

> **Hinweis:** Läuft die Seite über `https://`, muss auch Home Assistant über `wss://` erreichbar sein, sonst blockt der Browser die Verbindung.

## Steuerung vom Handy

Das Wand-Display ist reine Anzeige. Auf einem **Handy oder Tablet** (Touch-Gerät) erscheint oben zusätzlich die Karte **Steuerung** mit den Knöpfen aus `CONFIG.controls`. Am Wand-Display ohne Touch bleibt sie unsichtbar. Mit `?control` an der Adresse siehst du sie auf jedem Gerät.

| Entity | Knopf macht |
|---|---|
| `light.*`, `switch.*`, `input_boolean.*` | Umschalten |
| `scene.*`, `script.*`, `button.*` | Ausführen |
| `lock.*` | Ver- und Aufschließen (Aufschließen mit Rückfrage) |
| `cover.*` | Auf / Zu |
| `vacuum.*` | Start / Zurück zur Station |

**Einrichtung:** Das Handy muss die Seite erreichen. Der einfachste Weg ist ein kleiner Webserver auf dem Pi, im Ordner des Dashboards:

```bash
python3 -m http.server 8080
```

Dann öffnest du auf dem Handy `http://<IP-des-Pi>:8080/` (oder `…/?control`). Auf dem Startbildschirm ablegen geht über „Zum Home-Bildschirm“.

> **Sicherheit:** Das Token steht in `index.html`. Wer die Datei abrufen kann, hat vollen Zugriff auf dein Home Assistant. Stelle sie deshalb **nur im Heimnetz** bereit, nie ins Internet. Von außen nutzt du besser die Home-Assistant-App.

## Homelab

Die Seite **Homelab** erscheint im Seiten-Wechsel (`pages.labSec`, Standard 15 Sekunden) und mit `P`. Sie zeigt pro Hypervisor CPU, RAM, Temperatur, laufende VMs und Laufzeit, dazu den Speicher des NAS mit Festplatten-Temperaturen, den Status deiner Dienste, das letzte Backup und die USV. **Bei Problemen** (Server offline, CPU/RAM/Temperatur zu hoch, NAS fast voll, Platte zu heiß, Dienst nicht erreichbar, Backup zu alt, Stromausfall) erscheint zusätzlich eine rote Zeile „Homelab: …“ auf der Hauptseite und ein Hinweis. Schwellen stehen in `homelab.warn`.

Das Dashboard liest alles aus Home Assistant. Damit die Werte dort ankommen:

| Was | Wie |
|---|---|
| **Synology NAS** | Integration **Synology DSM** (Einstellungen → Geräte & Dienste). Legt in DSM dafür einen eigenen Benutzer an. Sie liefert Speicher-Belegung, CPU, RAM, Temperatur, Festplatten und den Sicherheitsstatus. Die Entity-IDs prüfst du unter Entitäten und trägst sie in `homelab.nas` ein. |
| **Proxmox** | Über HACS die Integration **Proxmox VE** hinzufügen (Zugang per API-Token mit Leserechten). Bei einem Cluster reicht ein Knoten, sie zeigt alle. Sie liefert pro Knoten CPU, RAM und Laufzeit, sowie VMs und Container. Alternativ **Glances** auf jedem Host mit der Home-Assistant-Integration **Glances**. Die genauen Entity-IDs findest du unter Einstellungen → Entitäten und trägst sie in `homelab.servers` ein. Gibt es keinen Sensor für die Zahl der laufenden VMs, lässt du `vms` weg. |
| **Dienste** | **Uptime Kuma** (HACS-Integration) oder einfache **Ping**- und **HTTP**-Sensoren in Home Assistant. `on` bedeutet „läuft“. |
| **Backup** | Der Zeitstempel-Sensor des letzten erfolgreichen Backups, z. B. von der Backup-Integration in Home Assistant oder einem eigenen Sensor deines Backup-Jobs. |
| **USV** | Integration **NUT**. Synology kann selbst als NUT-Server dienen (DSM → Hardware & Energie → USV → Netzwerk-USV-Server aktivieren). |

Alle Felder sind optional. Was du weglässt, erscheint nicht. Zum Probieren der Anzeige: `P` drücken, bis die Homelab-Seite erscheint.

## Weitere Geräte (Saugroboter, Waschmaschine, …)

Alles, was in Home Assistant als Entity auftaucht, kann das Dashboard anzeigen. Du brauchst nur die Entity-ID.

- **Dreame-Saugroboter:** Die Integration dafür gibt es über [HACS](https://hacs.xyz/) („Dreame Vacuum“). Danach gibt es eine `vacuum.*`-Entity. Trage sie unter `devices` (Anzeige) und `controls` (Start/Zurück) ein.
- **Roborock, Xiaomi, Ecovacs und andere:** Die offiziellen Integrationen liefern ebenfalls `vacuum.*`. Das Dashboard behandelt sie gleich.
- **Waschmaschine, Trockner:** Eine Steckdose mit Leistungsmessung als `sensor.*` in `devices` mit `above: 5` (Watt) eintragen.
- **Beliebige Sensoren:** Wenn du etwas Eigenes anzeigen willst, sag Bescheid oder schau dir `devices` und `controls` an.

## Gäste-WLAN (QR-Code)

Trage in `CONFIG.guestWifi` den Namen (SSID) und das Passwort deines Gäste-WLANs ein. Der QR-Code erscheint dann:
- in der **ruhigen Ansicht** (rechts unten),
- auf dem **Handy** als Karte „Gäste-WLAN“ (praktisch, um den Code einem Gast zu zeigen),
- mit der Taste **`W`** groß im Vollbild.

Gäste öffnen die Kamera, halten sie auf den Code, tippen auf den Vorschlag und sind verbunden. Das funktioniert mit iPhone und Android ohne App. Der Code ist immer schwarz auf weiß, auch im Dunkelmodus, damit er sich zuverlässig lesen lässt.

> **Sicherheit:** Das Passwort steht im Klartext in `index.html` und, wenn `showPassword: true` ist, auf dem Display. Nutze dafür nur das **getrennte Gäste-Netz** (siehe [`netzwerk/`](netzwerk/README.md)), nie das Passwort deines privaten WLANs. Mit `showPassword: false` zeigt das Display nur den QR-Code.

Die Erzeugung des Codes übernimmt die kleine Bibliothek *QR Code Generator for JavaScript* von Kazuhiko Arase (MIT-Lizenz), die komplett in `index.html` eingebettet ist. Es werden keine Daten ins Internet geschickt.

## Seiten der Wanddarstellung

Die **Hauptseite** zeigt nur das Wichtigste: Räume mit Temperatur, den Grundriss mit Lampen und Fenstern, höchstens drei Hinweiszeilen (Warnungen zuerst) und unten eine Zeile mit Personen, Wetter und dem, was gerade läuft. Alles andere wechselt automatisch durch:

| Seite | Inhalt |
|---|---|
| Hauptseite | Räume, Grundriss, wichtigste Hinweise |
| Ruhige Ansicht | Große Uhr, Wetter, Vorschau, Termin, Müll, Gäste-WLAN-QR-Code |
| Übersicht | Alle Hinweise, Heute-Kacheln, Anwesenheit, Wetter-Vorschau, Läuft gerade, Netzwerk, System, Aktivität |
| Homelab | Hypervisoren, NAS, Dienste, Backup, USV |

Die Dauer steht in `pages` (`mainSec`, `ambientSec`, `infoSec`, `labSec`, jeweils Sekunden, `0` blendet eine Seite aus). Mit `P` springst du zur nächsten Seite. Auf Handy und Tablet bleibt alles auf einer Seite.

## Tag-/Nacht-Design

Standardmäßig ist das Design am Tag hell. Ab **18:00 Uhr** blendet es über **60 Minuten** langsam in den Dunkelmodus (fertig um 19:00 Uhr). Ab **07:00 Uhr** blendet es über eine Stunde wieder zurück. Einstellbar in `CONFIG.theme`:

```js
theme: { mode: 'auto', darkFrom: '18:00', lightFrom: '07:00', fadeMin: 60 }
```

- `mode`: `'auto'` (Tag/Nacht), `'dark'` oder `'light'` (fest)
- `darkFrom` / `lightFrom`: Beginn des Übergangs
- `fadeMin`: Dauer des Übergangs in Minuten

Zum Ausprobieren hängst du die Uhrzeit an die Adresse an, z. B. `index.html?time=18:30`. Mit `?theme=dark` erzwingst du den Dunkelmodus.

## Tastenkürzel

| Taste | Funktion |
|---|---|
| `F` | Vollbild |
| `T` | Design wechseln: Automatisch, Dunkel, Hell |
| `D` | Türklingel testen |
| `A` | Testalarm |
| `L` | Lüften-Hinweis testen |
| `P` | Nächste Seite: Hauptseite, ruhige Ansicht, Übersicht, Homelab |
| `W` | Gäste-WLAN-QR-Code groß im Vollbild (schließt nach 60 Sekunden oder mit `Esc`) |
| `Esc` | Klingel-Anzeige schließen |

## Anwesenheit und Display aus

**So erkennt das Dashboard, ob du da bist:** Es liest die `person.*`-Einträge aus Home Assistant (`CONFIG.people`). Eine Person ist `home` oder `not_home`. Home Assistant leitet das vom Handy ab, am besten kombiniert:

1. **Companion-App** (iOS/Android) auf dem Handy installieren, mit Standort-Freigabe „Immer“ und aktivierter Standortermittlung in der App.
2. In Home Assistant unter **Einstellungen → Personen** der Person das Handy als Gerät zuordnen. Mit einem zweiten Tracker, z. B. dem Router (Fritz!Box) oder dem Handy im WLAN, wird die Erkennung zuverlässiger.
3. Die Entity-ID (z. B. `person.timo`) in `CONFIG.people` eintragen.

Das Display geht erst aus, wenn **alle** eingetragenen Personen weg sind (Status `unknown` oder `unavailable` zählt nicht als weg). Es muss außerdem die eingestellte Zeit `awayMin` (Standard 10 Minuten) ohne Bewegung und Berührung vergangen sein. Es geht sofort wieder an bei Heimkehr, Bewegung, Alarm, Klingel oder Berührung.

**Einrichtung:**

1. `pi-stats.py` läuft auf dem Pi (siehe unten). Es schaltet den Bildschirm über einen Befehl.
2. Standard ist `xset dpms force off` (X11). Je nach System setzt du `DISPLAY_OFF_CMD` und `DISPLAY_ON_CMD`:

| System | Aus / An |
|---|---|
| Raspberry Pi OS Bookworm (Wayland) | `wlr-randr --output HDMI-A-1 --off` / `--on` (Ausgang mit `wlr-randr` prüfen) |
| Ältere Pi-Systeme | `vcgencmd display_power 0` / `1` |
| Fernseher per HDMI-CEC | `sh -c 'echo "standby 0" \| cec-client -s -d 1'` / `... "on 0" ...` |

3. Abschalten kannst du es in `index.html` mit `dim.screenOff.enabled: false`.

## Optional: `pi-stats.py` (Pi-Werte, Klingel-Kamera, Display)

`pi-stats.py` ist ein kleiner Helfer auf dem Pi ohne zusätzliche Pakete. Er liefert:

- CPU, RAM, Temperatur, Disk und Netzwerkverkehr für die Karten **System** und **Netzwerk**
- das Kamerabild für die **Türklingel**
- das Ein- und Ausschalten des **Displays** bei Abwesenheit

```bash
HA_URL=http://homeassistant.local:8123 HA_TOKEN=dein_token python3 pi-stats.py
```

Ohne `HA_URL` und `HA_TOKEN` liefert er nur die Systemwerte. Läuft er nicht, zeigt das Netzwerkdiagramm eine Simulation. Wenn du den Helfer nicht nutzt, setze in `index.html` `stats: ''`.

**Autostart mit systemd** (`/etc/systemd/system/pi-stats.service`):

```ini
[Unit]
Description=Smarthome pi-stats
After=network-online.target

[Service]
Environment=HA_URL=http://homeassistant.local:8123
Environment=HA_TOKEN=dein_token
ExecStart=/usr/bin/python3 /home/pi/smarthome/pi-stats.py
Restart=always
User=pi

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable --now pi-stats
```

## Raspberry Pi als Wand-Display (Kiosk)

Autostart des Browsers im Vollbild (`~/.config/autostart/dashboard.desktop`):

```ini
[Desktop Entry]
Type=Application
Name=Dashboard
Exec=chromium-browser --kiosk --noerrdialogs --disable-infobars --check-for-update-interval=31536000 file:///home/pi/smarthome/index.html
```

Bildschirm-Abschaltung verhinderst du in `raspi-config` unter *Display Options → Screen Blanking*.

## Weitere Ordner

| Ordner | Inhalt |
|---|---|
| [`netzwerk/`](netzwerk/README.md) | Aufteilung in 4 Netze (Privat, IoT, Homelab, Gäste) mit einem Cisco-Layer-3-Switch, inklusive Konfigurationsmuster |

## Fehlersuche

| Problem | Lösung |
|---|---|
| Oben steht „Kein Token“ | Token in `CONFIG.token` eintragen |
| „Token ungültig“ | Token neu erstellen und ohne Leerzeichen einfügen |
| „Offline“ | `url` prüfen (Adresse, Port 8123, `ws://` vs. `wss://`) |
| Werte zeigen `–` | Entity-ID falsch geschrieben, in Home Assistant prüfen |
| Lampe oder Fenster erscheint nicht im Grundriss | `x`/`y` prüfen, im Grundriss klicken liefert die Koordinaten |
| Kein Klingel-Kamerabild | `pi-stats.py` mit `HA_URL` und `HA_TOKEN` starten, `doorbell.camera` prüfen |
| Wetter-Vorschau bleibt leer | Die Wetter-Entity muss `weather.get_forecasts` unterstützen (stündlich oder täglich), `weather.entity` muss gesetzt sein |
| Batterie fehlt in der Warnung | Der Sensor hat keine Geräteklasse `battery`: bei `battery.extra` von Hand eintragen. Wird er ausgeblendet, prüfe `exclude` |
| „Keine Daten seit …“ | Home Assistant antwortet nicht mehr: Adresse, Netzwerk und Token prüfen. Die Seite verbindet sich selbst neu |
| Steuerung fehlt am Handy | Die Seite mit `?control` öffnen und prüfen, ob `controls` Einträge hat |
| Homelab zeigt `–` | Entity-IDs in `homelab` prüfen. Die Seite warnt „offline“ nur, wenn Home Assistant `unavailable` meldet |
| Display geht nie aus | Prüfen, ob alle Personen in `people` `not_home` sind, ob `pi-stats.py` läuft und ob der Befehl passt: `curl 'localhost:8765/display?state=off'` |
| Bildschirm dimmt nie | Es braucht mindestens einen Bewegungsmelder in `rooms` oder eine Person in `people`. Mit `onlyNight: false` dimmt es auch tagsüber |
| Lüften-Empfehlung fehlt | Bei den Fenstern in `windows` den passenden Raum als `plan` angeben, damit offene Fenster erkannt werden |
| Keine Regen-Warnung | `weather.entity` muss gesetzt sein, optional `windowWarn.rainSensor` (z. B. ein Regensensor) |
| Cover im „Läuft gerade“ fehlt | Der Player liefert kein `entity_picture`, dann erscheint ein Notensymbol |
