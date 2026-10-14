# Nachvollziehbare Quelldateien

Die fertigen PNGs und der Offline-Viewer benötigen diese Skripte nicht.

`designs.py` enthält die 45 individuell ausgearbeiteten Front-/Rücken-Kleidungsmasken, Haarprofile und Paletten. `build.py` schreibt das native Skinlayout, `render.py` erstellt Modellvorschauen, `package.py` erstellt Prüfung und Offline-Viewer.

Für eine Neuerstellung: Python 3.11+ sowie Pillow und NumPy installieren. Das ursprüngliche V4-Paket in einen separaten Ordner entpacken. `NOVORIAMON_V4_DIR` auf diesen Ordner setzen. `NOVORIAMON_OUTPUT` auf einen neuen Ausgabeordner setzen (nicht auf den einzigen vorhandenen Stand). Die Original-Zuordnung ist zusätzlich als `ORIGINAL_ZUORDNUNG.json` enthalten.

Dann nacheinander `python build.py`, `python render.py`, `python package.py` in diesem Quellordner ausführen. Das V4-Paket wird nur für Vorher-Nachher-Vergleich und Änderungsprüfungen gelesen. Die Skripte greifen weder auf GitHub noch auf Minecraft zu. Schriftarten werden nicht mitgeliefert; Vorschauen nutzen lokal vorhandene Schriften.
