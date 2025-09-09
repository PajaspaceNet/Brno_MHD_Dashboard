# Brno_MHD_Dashboard


---



Tento projekt je interaktivní vizualizace vybraných linek MHD Brno z GTFS dat.  
Cílem je ukázat vytíženost linek a zastávek a připravit praktický dashboard, alternativu Power BI v Pythonu.

---

## Funkce

1. **Mapa linek `/`**  
   - Zobrazuje vybrané linky: 1, 44, 37, 26   
   - Velikost markeru = počet spojů na zastávce  
   - Barva markeru = linka  
   - Popup s názvem zastávky, linkou a počtem spojů

2. **Statistiky `/stats`**  
   - Tabulky s počtem spojů na zastávkách a linkách  
   - Top 5 zastávek a top 5 linek  
   - Možnost filtrovat podle linky, např. `/stats?line=1`

---

## Praktické využití

- Vizualizace vytíženosti linek a zastávek MHD  
- Dashboard je **alternativa Power BI**, plně interaktivní v Pythonu  
- Ukazuje schopnosti práce s daty, vizualizace a nasazení webové aplikace  

---

## Požadavky

- Python 3.x  
- Knihovny: pandas, flask, folium, matplotlib  
- GTFS data (nutno stahnout)  

---

## Instalace a spuštění

1. Naklonujte repozitář:

```bash
git clone <repo_url>
cd <repo>
````

2. Nainstalujte potřebné knihovny:

```bash
pip install -r requirements.txt
```

3. Spusťte Flask aplikaci:

```bash
python app.py
```

4. Otevřete v prohlížeči:

* Mapa: [http://localhost:5000/](http://localhost:5000/)
* Statistiky: [http://localhost:5000/stats](http://localhost:5000/stats)
* Statistiky s filtrem linky: [http://localhost:5000/stats?line=1](http://localhost:5000/stats?line=1)

---

## Struktura projektu

```
Brno_MHD_Dasboard
│
├─ app.py              # Flask aplikace
├─ requirements.txt    # Seznam knihoven
├─ gtfs/               # Složka s GTFS daty (stops.txt, trips.txt, routes.txt, stop_times.txt)
└─ README.md           # Tento soubor
```

---

## Co projekt ukazuje 

* Práce s Pythonem a reálnými daty
* Tvorbu interaktivních vizualizací a map
* Analýzu a agregaci dat (Počet spojů na zastávkách a linkách)
* Nasazení webové aplikace (Flask + interaktivní dashboard)

---

## Poznámky

* Projekt je připravený k nasazení na VPS nebo lokálně
* Může být snadno rozšířen o časové filtry, další linky, interaktivní mapy

### pokud to jede na serveru jako v tomoto pripade tak doporucuju dat jako servicu <br>

zde:
```
/etc/systemd/system/flask.service
```
a nasledne:

```
[Unit]
Description=Flask server for MHD Brno map
After=network.target

[Service]
User=user
WorkingDirectory=/home/user/mhd_brno_flask
ExecStart=/home/user/mhd_brno_flask/venv/bin/python /home/user/mhd_brno_f>
Restart=always

[Install]
WantedBy=multi-user.target
```

* enablovani status atd

```
sudo systemctl stop flask.service      # zastaví Flask
sudo systemctl restart flask.service   # restartuje Flask
sudo systemctl status flask.service    # zkontroluje stav služby
```

### GTFS data

Projekt vyžaduje GTFS data MHD Brno.  
Stáhněte je z oficiálního zdroje  vytvorte si slozku   - 'gtfs'  podle struktury vložte do složky .





