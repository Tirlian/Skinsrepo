# Verwendung der Dateien

1. ZIP in einen neuen Ordner entpacken, nicht über die bisherige Kopie.
2. Für den NPC die einzelne Datei aus `skins/` verwenden. Die Bilder aus `previews/` und die Kontrolltafeln sind keine Skins.
3. Das klassische Spieler-Modell / Classic (4 Pixel breite Arme) verwenden. Grundkörper und zweite Ebene sind dafür angelegt.
4. Bei einem Skin-Upload auf GitHub bleiben die vorhandenen Root-Dateinamen bestehen: zum Beispiel `gym_fire.png`, **nicht** eine normale GitHub-HTML-Seite als Bildinhalt. `SKIN_ZUORDNUNG.json` enthält beide Pfade (lokal und GitHub).
5. Diese Ausgabe selbst installiert keine Mods und verändert keine Serverdateien, NPC-Daten, Questfortschritte oder GitHub-Dateien.

## Windows-Kontrolle ohne Installation

`SKINS_ANSEHEN.html` lokal im Browser öffnen. Keine PowerShell-Freigaben, Git-DLLs, Tokens, Node.js oder zusätzlichen Bibliotheken erforderlich. Die 45 Skin-PNGs und ihre V4-Vergleichstexturen sind in der Datei eingebettet. Die Seite arbeitet ohne Netzabfragen.

## Feuer-Arenaleiter

Kaels neues Haar wurde auf Grund- und Außenschicht neu aufgebaut. Die Haarfarben lauten RGB (87,19,36), (137,24,42), (190,39,46), (226,61,33), (249,111,35). Die hellen Flächen des Gesichts sind Haut, keine verbliebene blonde Haarlage. `qa/FEUER_HAARPRUEFUNG.png` zeigt Vorderseite, Rückseite, beide Seiten und Scheitel jeweils mit und ohne äußere Ebene.

Die konkrete Menüführung deiner EasyNPC-Version wurde nicht im laufenden Spiel getestet. Das Paket behauptet keinen abgeschlossenen Ingame-Test.
