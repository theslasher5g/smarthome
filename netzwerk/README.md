# Netzwerk: 4 Netze mit einem Cisco-Layer-3-Switch

Dieser Ordner gehört zum Smarthome-Dashboard, enthält aber keinen Dashboard-Code. Er beschreibt, wie du dein Haus in vier Netze aufteilst, damit Gäste, Smart-Home-Geräte, deine eigenen Geräte und das Homelab voneinander getrennt sind.

- [`cisco-muster.txt`](cisco-muster.txt) ist ein Konfigurationsmuster für den Switch.

> **Wichtig:** Das Muster ist **ungetestet** und für Cisco IOS geschrieben. Befehle und Schnittstellennamen unterscheiden sich je nach Modell. Mach vor jeder Änderung ein Backup der Konfiguration und teste an einem Port, bevor du alles umstellst. Wer sich dabei aussperrt, braucht Zugang zur Konsole des Switches.

## Die vier Netze

| VLAN | Netz | Inhalt | Darf wohin? |
|---|---|---|---|
| 10 | 192.168.10.0/24 | **Privat**: PC, Laptop, Handy | Überall hin, nur nicht ins Gäste-Netz |
| 20 | 192.168.20.0/24 | **IoT**: Home Assistant (Raspberry Pi), Wand-Display, Smart-Home-Geräte | Internet, dazu Home Assistant gezielt ins Homelab |
| 30 | 192.168.30.0/24 | **Homelab**: 3× Proxmox, Synology | Internet, aber nicht aktiv in andere Netze |
| 40 | 192.168.40.0/24 | **Gäste**: Gäste-WLAN | Nur Internet |

Beispiel-Adressen: Home Assistant `192.168.20.10`, Proxmox `192.168.30.11` bis `.13`, Synology `192.168.30.20`. Gib Home Assistant und den Servern feste Adressen oder DHCP-Reservierungen.

## Wie der Verkehr fließen soll

- **Dein Handy und Laptop (Privat)** erreichen Home Assistant und das Dashboard (Port 8123) im IoT-Netz, das Homelab und das Internet. Zurück dürfen nur Antworten.
- **Home Assistant (IoT)** darf aktiv nur in das Homelab und dort nur auf diese Ports: Proxmox (8006), Synology DSM (5001), Glances (61208) und die USV (NUT, 3493). Das reicht für die Homelab-Seite des Dashboards.
- **Smart-Home-Geräte (IoT)** können das Internet nutzen, sehen aber weder deine Geräte noch das Homelab.
- **Homelab** kann ins Internet (Updates), sonst nur Antworten.
- **Gäste** sehen nur das Internet.

Das Wand-Display (Raspberry Pi mit `index.html`) gehört ins **IoT-Netz**, dann spricht es mit Home Assistant im selben Netz, ohne dass der Switch dazwischen filtern muss. Auch `pi-stats.py` läuft dort.

## Stolperstellen

- **ACLs auf dem Switch sind zustandslos.** Der Switch merkt sich keine Verbindungen. Das Muster nutzt deshalb `established` bei TCP, um Antworten zuzulassen. Das ist weniger streng als eine echte Firewall: ein Gerät kann gezielt Pakete mit gesetztem ACK-Bit schicken. Für ein Zuhause reicht das meist. Willst du echte, zustandsbehaftete Trennung, setze eine Firewall (z. B. OPNsense) davor und lass den Switch nur noch routen.
- **UDP-Antworten** (z. B. mDNS, manche Smart-Home-Protokolle, Casting) funktionieren zwischen den Netzen nicht von selbst. Entweder erlaubst du gezielt Ports oder hältst die betreffenden Geräte im selben Netz.
- **Internet:** Der Switch braucht einen Router oder eine Firewall, die ins Internet übersetzt (NAT). Eine Fritz!Box braucht dafür Routen zu den vier Netzen, und ob sie diese Netze auch ins Internet übersetzt, hängt vom Modell ab. Prüfe das vorab. Am sichersten ist ein eigener Router oder eine Firewall, die die vier Netze kennt.
- **Gäste-WLAN** braucht einen WLAN-Zugangspunkt mit VLAN-Unterstützung, der pro WLAN-Name (SSID) ein VLAN verteilt. Fritz!Box und Repeater können das nicht (UniFi, TP-Link Omada oder ähnliches können es).
- **Home Assistant (Raspberry Pi) im IoT-Netz:** Die Geräte-Entdeckung per mDNS (Chromecast, Hue, …) funktioniert nur im selben Netz. Smart-Home-Geräte gehören deshalb ins IoT-Netz, bei Geräten in anderen Netzen musst du die Adresse von Hand eintragen.
- **Companion-App am Handy** (Anwesenheit): Im Heimnetz erreicht sie Home Assistant über Privat nach IoT. Unterwegs brauchst du einen Fernzugriff (z. B. VPN oder Nabu Casa).
- **Handy-Steuerung des Dashboards:** Das Handy (Privat) darf die Seite vom Pi (IoT) laden und mit Home Assistant sprechen. Das erlaubt das Muster.

## Dashboard und Netzwerk

Zurzeit zeigt das Dashboard den Netzwerkverkehr des Pi oder, wenn du die Entitäten einträgst, deines Routers (`CONFIG.net`). Cisco-Switches sprechen **SNMP**: Home Assistant kann damit den Durchsatz der VLAN-Schnittstellen und Ports lesen. Die Anbindung beschreibe ich, sobald du dein Switch-Modell und den Router festgelegt hast. Eine Anzeige pro Netz kommt danach.
