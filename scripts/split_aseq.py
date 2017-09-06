# Program to split an aseq file into single files per dataset This script is in
# a quick and dirty state so no warranty is given at all
# Version: 0.2 Author:
# Stefan Schuh Email: stefan.schuh@uni-graz.at

import os


class ToC (object):

    def __init__(self):
        self.entries = []

    def add_entry(self, fname, line):
        self.entries.append(fname[:10] + "   " + line[:9] + "   " + line[21:].replace("$$b", " : ")
                                            .replace("$$c", " / ")
                                            .replace("$$n", ". ")
                                            .replace("$$p", ", "))

    def write_to_file(self, fname):
        print(f'### Schreibe Inhaltsverzeichnis in "{fname.rsplit("/")[-1]}".')
        with open(fname, "w", encoding="utf-8", errors="replace") as tocfile:
            tocfile.write("""AC-Nummer  | Sys.-Nnr  |  Titel
-----------+-----------+------------------------------------------------------------------------\n""")
            for entry in self.entries:
                tocfile.write(entry)


# setting the stage
if "outfiles" in os.listdir("../"):
    for file in os.listdir("../outfiles"):
        os.remove("../outfiles/" + file)
else:
    os.mkdir("../outfiles")

infiles = ["../infiles/" + file for file in os.listdir("../infiles/")]
if len(infiles) < 1:
    print("Das Input-Verzeichnis ist leer! Bitte speichern Sie mindestens eine Datei in ./infiles/")
    input("Drücken Sie die ENTER-Taste um dieses Fenster zu schließen.")
    quit()

def write_ds(ds, fname):
    print(f'  ...\tSchreibe {fname}.seq')
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

    if not (outl.startswith("LDR") or outl.startswith("00")):
        # replace indicator <space> with # for readability
        outl = outl[:3] + outl[3:5].replace(" ", "#") + outl[5:]
    return outl

def set_title(line):
    if line[10:13] == "001":
        fname = line[18:].strip()
        print(fname)
    else:
        pass

def process_infile(file, toc):
    fh = open(file, "r", encoding="utf-8", errors="replace")

    toc = toc
    cur_ds = None
    ds = []
    fname = ""
    infile_name = file.rsplit("/")[-1]
    print(f"### Verarbeite {infile_name}")
    if infile_name.startswith("m2m_") and len(infile_name) > 28:
        konverterstand = file.rsplit("/")[-1][11:27]

    for line in fh:
        if line[10:13] == "001":
            # sets the filename
            if "konverterstand" in locals():
                fname = line[18:].strip() + "_" + konverterstand
            else:
                fname = line[18:].strip()

        if line[10:13] == "245":
            toc.add_entry(fname, line)

        if line[:9] == cur_ds or cur_ds == None:
            cur_ds = line[:9]
            ds.append(prettyprint(line))

        else:
            write_ds(ds, fname)
            ds = [line[10:16] + line[18:]]
            cur_ds = line[:9]

    write_ds(ds, fname)
    fh.close()
    print("\n")

toc = ToC()
for file in infiles:
    process_infile(file, toc)

toc.write_to_file("../outfiles/ToC.txt")
print('''\n### Vorgang abgeschlossen. Sie finden die einzelnen Dateien und
    das Inhaltsverzeichnis im Ordner "./outfiles/"''')

input("\nDrücken Sie die ENTER-Taste, um dieses Fenster zu schließen.")
