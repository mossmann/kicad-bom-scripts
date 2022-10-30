# kicad-bom-scripts
scripts for bill of materials generation from KiCad

These are minor modifications of scripts provided with the KiCad source.

## bom.py usage

This script generates a bill of materials file in .csv format useful for ordering parts.

Parts with "DNP" in the "DNP" or "Note" field are ignored.

1) Generate a BOM in KiCad's eeschema using the kicad_netlist_reader plugin (if you are using a version of KiCad that is older than KiCad 5, generate the BOM without using a plugin). This will generate a .xml file in the project directory.

2) Convert the .xml file to a .csv file:

```
$ bom.py <file.xml>
```

### options

* `-q` allows you to specify a quantity in number of boards
* `-d` truncates lists of reference designators for Digi-Key order compatibility
* `-s` outputs a single reference designator per row, required for validate-pos.sh

## validate-pos.sh usage

This script checks for discrepancies between a footprint position file and a bill of materials.

1) Generate the footprint position file from the Fabrication Outputs menu of KiCad's PCB Editor.
2) Generate the bill of materials file with `bom.py -s` (see above).
3) Check the files for discrepancies:

```
$ validate-pos.sh <file.pos> <bom.csv>
```
