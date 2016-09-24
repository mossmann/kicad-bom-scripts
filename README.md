# kicad-bom-scripts
scripts for bill of materials generation from KiCad

These are minor modifications of scripts provided with the KiCad source.

bom.py is for general purpose xml->csv
dkbom.py is for Digi-Key orders

Parts with "DNP" in the "Note" field are ignored.

Usage:

1) First step is to generate a BOM in kicad using no plugins. This will generate a .xml file in the project directory

2) Next give the command to convert the .xml file to a .csv file.

	 $: ~/kicad-bom-scripts/bom.py(or dkbom.py for digikey friendly BOM) <file.xml> <file.csv> <quantity>

3) Open the new .csv file in Libreoffice, Excel, etc.. Veryify that all fields appear to be in the right places. 

4) If you are using Digikey you will need to save this .csv file as a .xls file

5) Upload to the website of your favorite purveyor of electronic components.
