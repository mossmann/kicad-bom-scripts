#!/usr/bin/python
#
# adapted from bom_csv_grouped_by_value.py

from __future__ import print_function

# Import the KiCad python helper module and the csv formatter
import kicad_netlist_reader
import csv
import sys
import re
import os
import argparse

# override csv.writer's writerow() to support utf8 encoding:
def writerow( acsvwriter, columns ):
    utf8row = []
    for col in columns:
        utf8row.append( unicode(col).encode('utf-8') )
    acsvwriter.writerow( utf8row )


def ref_cmp(a, b):
    ai = int(re.split('[A-Z]+', a)[1])
    bi = int(re.split('[A-Z]+', b)[1])
    return cmp(ai, bi)


def main():
    # Set up a simple argument parser.
    parser = argparse.ArgumentParser(description="KiCad BOM script")
    parser.add_argument('-d', dest='digikey', action='store_true', 
                        help="Truncate references for Digi-Key orders")
    parser.add_argument('infile', metavar='<filename>', type=str,
                        help='input xml BOM file from KiCad')
    parser.add_argument('-q', dest='quantity', type=int, default=1,
                        help='Number of boards')
    args = parser.parse_args()

    # Generate an instance of a generic netlist, and load the netlist tree from
    # the command line option. If the file doesn't exist, execution will stop
    net = kicad_netlist_reader.netlist(args.infile)

    # Open a file to write to, if the file cannot be opened output to stdout
    # instead
    filename, file_extension = os.path.splitext(args.infile)
    outfile = filename + ".csv"
    try:
        f = open(outfile, 'w')
    except IOError:
        e = "Can't open output file for writing: " + outfile
        print(__file__, ":", e, file=sys.stderr)
        f = sys.stdout

    # subset the components to those wanted in the BOM, controlled
    # by <configure> block in kicad_netlist_reader.py
    components = net.getInterestingComponents()

    compfields = net.gatherComponentFieldUnion(components)
    partfields = net.gatherLibPartFieldUnion()

    # remove Reference, Value, Datasheet, and Footprint, they will come from 'columns' below
    partfields -= set( ['Reference', 'Value', 'Datasheet', 'Footprint'] )

    columnset = compfields | partfields     # union

    # prepend an initial 'hard coded' list and put the enchillada into list 'columns'
    columns = ['Item', 'Qty', 'Reference(s)', 'Value', 'LibPart', 'Footprint', 'Datasheet'] + sorted(list(columnset))

    # Create a new csv writer object to use as the output formatter
    out = csv.writer(f, lineterminator='\n', delimiter=',', quotechar='\"', quoting=csv.QUOTE_MINIMAL)

    row = []

    # Get all of the components in groups of matching parts + values
    # (see kicad_netlist_reader.py)
    grouped = net.groupComponents(components)

    # Output header row
    writerow( out, columns )

    # Output component information organized by group, aka as collated:
    item = 0
    for group in grouped:
        del row[:]
        refs = []

        # Add the reference of every component in the group and keep a reference
        # to the component so that the other data can be filled in once per group
        for component in group:
            refs.append(component.getRef())
            c = component
        refs.sort(cmp=ref_cmp)

        ref_string = ", ".join(refs)
        if args.digikey and len(ref_string) > 48:
                ref_string = ref_string[:45] + "..."

        # Fill in the component groups common data
        # columns = ['Item', 'Qty', 'Reference(s)', 'Value', 'LibPart', 'Footprint', 'Datasheet'] + sorted(list(columnset))
        item += 1
        row.append( item )
        row.append( len(group) * args.quantity )
        row.append( ref_string )
        row.append( c.getValue() )
        row.append( c.getLibName() + ":" + c.getPartName() )
        row.append( net.getGroupFootprint(group) )
        row.append( net.getGroupDatasheet(group) )

        # from column 7 upwards, use the fieldnames to grab the data
        for field in columns[7:]:
            row.append( net.getGroupField(group, field) );

        writerow( out,  row  )

    f.close()

if __name__ == "__main__":
    main()