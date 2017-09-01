# Program to split an aseq file into single files per dataset
# This programm is in a quick and dirty state so no warranty at all
# Version: 0.1
# Author: Stefan Schuh
# Email: stefan.schuh@uni-graz.at


from sys import argv
import re
import os

# if len(argv) == 2:
#     script, infile = argv
# else:
#     infile = input("Bitte Dateinamen eingeben!\n>>> ")

infile = "../infiles/" + os.listdir("../infiles/")[0]

fh = open("../infiles/" + infile, encoding="utf-8", errors="replace")
cur_ds = None

ds = []
count = 0
fname = ""
titles = []

# make the necessary dirs, empty them out if they exist
if "outfiles" in os.listdir("../"):
    for file in os.listdir("../outfiles"):
        os.remove("../outfiles/" + file)
else:
    os.mkdir("../outfiles")

def write_ds(ds, fname):
    with open(f"../outfiles/{fname}.seq", "w", encoding="utf-8", errors="replace") as fh_o:
        for line in ds:
            fh_o.write(line)

def prettyprint(line):
    line = line[10:16] + line[18:]
    if "$$" in line:
        elements = line.split("$$")
        if len(elements) > 1:
            outl = elements[0] + "$$" + elements[1]
            for sf in elements[2:]:
                outl = outl + f"\n      $${sf}"
        else:
            outl = line[10:16] + "$$" + line[18:]
    else:
        outl = line

    outl = outl[:3] + outl[3:5].replace(" ", "#") + outl[5:]
    return outl

def set_title(line):
    if line[10:13] == "001":
        fname = line[18:].strip()
        print(fname)
    else:
        pass


for line in fh:
    if line[10:13] == "001":
        # sets the filename
        fname = line[18:].strip()

    if line[10:13] == "245":
        titles.append(fname + "     " + line[21:].replace("$$b", " : ")
                                                 .replace("$$c", " / ")
                                                 .replace("$$n", ". ")
                                                 .replace("$$p", ", ") )

    if line[:9] == cur_ds or cur_ds == None:
        cur_ds = line[:9]
        ds.append(prettyprint(line))

    else:
        write_ds(ds, fname)
        ds = [line[10:16] + line[18:]]
        count += 1
        cur_ds = line[:9]

write_ds(ds, fname)

with open("../outfiles/titles.txt", "w", encoding="utf-8", errors="replace") as titfile:
    for title in titles:
        titfile.write(title)

fh.close()
