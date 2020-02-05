#!/bin/bash
#
# validate-pos.sh:
#   check for discrepancies between footprint position file and bill of materials
#
# The footprint position file is generated from the Fabrication Outputs
# menu of KiCad's pcbnew.
#
# The bill of materials file should be generated with ./bom.py -s.

POS=${1}
BOM=${2}

if [ $# -ne 2 ]; then
		echo "usage: validate-pos.sh <file.pos> <bom.csv>"
		exit 1
fi

POSREFS=/tmp/posrefs.$$
BOMREFS=/tmp/bomrefs.$$

grep -v '^#' ${POS} | awk '{print $1}' | sort -V > ${POSREFS}
tail +2 ${BOM} | awk -F, '{print $3}' | sort -V > ${BOMREFS}

echo
echo "Reference designators in POS that do not appear in BOM:"
diff ${POSREFS} ${BOMREFS} | grep '^<' | awk '{print $2}'

echo
echo "Reference designators in BOM that do not appear in POS:"
diff ${POSREFS} ${BOMREFS} | grep '^>' | awk '{print $2}'

rm ${POSREFS} ${BOMREFS}
