# PadFinder

## Deutsch
### Setup
`settings.py.template` in `settings.py` umbenennen und die richtigen Werte hinzufügen.

Mit `pip3 install -r requirements.txt` die benötigten Pakete installieren.

### Benutzung
Um FFF-Pads zu finden muss `baseurl = "https://pad.fridaysforfuture.is/p/"` sein
In `padnames` muss mindestens ein Padname eingetragen sein, also `padnames = ['Name des Pads']`, bei weiteren Pads mit Komma erweitern, also `padnames = ['Name des Pads', 'Anderer Name']`
Die RegEx muss `regex = "http[s]?\:\/\/pad\.fridaysforfuture\.(?:is|de)\/p\/[\w\.\-\%]+"` sein, um eine URL auf ein Pad zu erkennen
`filepath` kann auf eine Textdatei zeigen, die nach Pad-URLs durchsucht wird
`filepath_export` ist ein Ordner, in dem die Ergebnisse als Textdateien gespeichert werden
## English
### Setup
rename `settings.py.template` to `settings.py` and add the correct values.  
`pip3 install -r requirements.txt`