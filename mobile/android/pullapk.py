#!/usr/bin/python
import sys
import subprocess
from optparse import OptionParser


def get_path(options, pkgname):
    if options.serial:
        p = subprocess.Popen(["adb", "-s", options.serial, "shell", "pm", "path", pkgname], stdout=subprocess.PIPE)
    else:
        p = subprocess.Popen(["adb", "shell", "pm", "path", pkgname], stdout=subprocess.PIPE)
    path = p.stdout.read()
    p.wait()

    path = path.split("package:")[1].strip()
    print("Package at: {}".format(path))

    return path


def pull_apk(options, path, pkgname):
    if not options.output:
        output = "{}.apk".format(pkgname)
    else:
        output = options.output
    if options.serial:
        p = subprocess.Popen(["adb", "-s", options.serial, "pull", path, output])
    else:
        p = subprocess.Popen(["adb", "pull", path, output])
    p.wait()

    print("File saved as: {}\n".format(output))


parser = OptionParser()
parser.add_option("-s", "--serial", dest="serial",
                  help="(adb) use device with given serial number (overrides $ANDROID_SERIAL)", metavar="SERIAL")
parser.add_option("-f", "--filter",
                  dest="filter", default="",
                  help="filter packages by name")
parser.add_option("-o", "--output",
                  dest="output", default="",
                  help="output file name, default is pkg.apk")
parser.add_option("-i", "--input-list",
                  dest="input_list", default=None,
                  help="input list of the packages to pull")
parser.add_option("-a", "--auto",
                  dest="auto_pull", default=False, action="store_true",
                  help="autopull all found apks")

(options, args) = parser.parse_args()

# list packages
if options.serial:
    p = subprocess.Popen(["adb", "-s", options.serial, "shell", "pm", "list", "packages"], stdout=subprocess.PIPE)
else:
    p = subprocess.Popen(["adb", "shell", "pm", "list", "packages"], stdout=subprocess.PIPE)
packages = p.stdout.read()
p.wait()

# load packages
input_list = []

if options.input_list:
    with open(options.input_list, "r") as f:
        for l in f:
            input_list.append(l.strip())

# parse packages
pkgnames = []
i = 0

for pkg in packages.split("\n"):
    try:
        pkgname = pkg.split(":")[1].strip()
    except Exception:
        pass
    if options.input_list:
        if pkg.startswith("package:") and pkgname in input_list:
            pkgnames.append(pkgname)

            print ("{}: {}".format(i, pkgnames[i]))
            i += 1
    else:
        if pkg.startswith("package:") and (options.filter in pkgname):
            pkgnames.append(pkgname)

            print ("{}: {}".format(i, pkgnames[i]))
            i += 1

if len(pkgnames) == 0:
    print("No packages found.")
    sys.exit(1)

if options.auto_pull:
    if "Y" != raw_input("Download all found apks? [Y/n] "):
        sys.exit(1)
else:
    topull = int(raw_input("\nType index of the package to pull: "))
    pkgnames = pkgnames[topull]

for pkg in pkgnames:
    path = get_path(options, pkg)
    pull_apk(options, path, pkg)
