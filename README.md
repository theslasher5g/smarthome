# Smarthome Dashboard

Ein modernes Wand-Dashboard für Home Assistant. Es besteht aus **einer einzigen Datei** (`index.html`), die direkt im Browser läuft. Es braucht kein Build und keinen Webserver.

**Das Dashboard zeigt:**

- Räume mit Temperatur, Luftfeuchte, CO₂, Licht und Bewegung
- Einen Grundriss mit allen **Lampen** (an/aus), **Fenstern** (offen/zu) und dem, was gerade **läuft** (Musik)
- **Läuft gerade:** Musik mit Titel und Cover sowie laufende Geräte (Waschmaschine usw.)
- **Fenster-Warnung:** Steht ein Fenster offen und es regnet, schneit oder ist zu kalt, wird die Anzeige rot, und es kommt ein Hinweis
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
| `Esc` | Klingel-Anzeige schließen |

## Optional: `pi-stats.py` (Pi-Werte und Klingel-Kamera)

`pi-stats.py` ist ein kleiner Helfer auf dem Pi ohne zusätzliche Pakete. Er liefert:

- CPU, RAM, Temperatur, Disk und Netzwerkverkehr für die Karten **System** und **Netzwerk**
- das Kamerabild für die **Türklingel**

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

## Fehlersuche

| Problem | Lösung |
|---|---|
| Oben steht „Kein Token“ | Token in `CONFIG.token` eintragen |
| „Token ungültig“ | Token neu erstellen und ohne Leerzeichen einfügen |
| „Offline“ | `url` prüfen (Adresse, Port 8123, `ws://` vs. `wss://`) |
| Werte zeigen `–` | Entity-ID falsch geschrieben, in Home Assistant prüfen |
| Lampe oder Fenster erscheint nicht im Grundriss | `x`/`y` prüfen, im Grundriss klicken liefert die Koordinaten |
| Kein Klingel-Kamerabild | `pi-stats.py` mit `HA_URL` und `HA_TOKEN` starten, `doorbell.camera` prüfen |
| Keine Regen-Warnung | `weather.entity` muss gesetzt sein, optional `windowWarn.rainSensor` (z. B. ein Regensensor) |
| Cover im „Läuft gerade“ fehlt | Der Player liefert kein `entity_picture`, dann erscheint ein Notensymbol |
