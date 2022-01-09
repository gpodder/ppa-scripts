#!/usr/bin/env python3

import os
from _util import *

##########################################################

PACKAGE= "gpodder"
PPA_VERSION = "3.10.21.99"
RELEASE_VERSION = "3.10.21"

##########################################################

args = parse_args()

if args.dist == "ubuntu":
    dput_cfg = os.path.join(os.getcwd(), "dput.cf")
else:
    raise Exception("Debian repo unsupported")
    dput_cfg = os.path.join(os.getcwd(), "dput_debian.cf")

start_dir = os.getcwd()
clean(start_dir, PACKAGE)

git_dir = "gpodder-git"
if not os.path.isdir(git_dir):
    p("git clone https://github.com/gpodder/gpodder.git %s" % git_dir)
cd(git_dir)


p("git reset HEAD --hard")
p("git clean -xfd")
p("git checkout master")
p("git pull --all")
if args.release:
    fail(p("git checkout %s" % RELEASE_VERSION))

rev_num = p("git rev-list --count HEAD")[1]
rev_hash = p("git rev-parse --short HEAD")[1]
rev = rev_num  +"~" + rev_hash
date = p("date -R")[1]

if not args.release:
   p("echo 'BUILD_INFO = u\"%s\"' >> 'src/gpodder/build_info.py'" % rev_hash)

if not args.release:
    UPSTREAM_VERSION = PPA_VERSION + "+" + rev_num + "~" + rev_hash
else:
    UPSTREAM_VERSION = RELEASE_VERSION
if args.version != 0:
    UPSTREAM_VERSION += "+%s" % args.version
p("tar -pczf ../%s_%s.orig.tar.gz --exclude .git --strip-components=1 --transform='s,^./,gpodder/,' %s" % (PACKAGE, UPSTREAM_VERSION, "."))

if args.release:
    debian_dir = "debian_gpodder_stable"
else:
    debian_dir = "debian_gpodder"

if args.dist == "debian":
    if args.release:
        releases = {"gpodder-stable": debian_dir}
    else:
        releases = {"gpodder-unstable": debian_dir}
else:
    releases = {
        "bionic": debian_dir,
        "focal": debian_dir,
        "hirsute": debian_dir,
        "impish": debian_dir,
    }

for release, debian_dir in releases.items():
    p("rm -R debian")
    p("cp -R ../%s ." % debian_dir)
    p("mv %s debian" % debian_dir)

    debian_version = "%s-0~ppa%s~%s" % (UPSTREAM_VERSION, args.version, release.replace("-", "~"))

    changelog = "debian/changelog"
    t = open(changelog).read()
    t = t.replace("%version%", debian_version)
    t = t.replace("%dist%", release)
    t = t.replace("%date%", date)
    with open(changelog, "w") as h:
        h.write(t)

    if args.dist == "debian":
        if args.release:
            fail(p("pdebuild --use-pdebuild-internal --debbuildopts '-uc -us' --buildresult .."))
        else:
            fail(p("dpkg-buildpackage -uc -us -tc -I -rfakeroot"))
    else:
        fail(p("dpkg-buildpackage -uc -us -S -tc -I -rfakeroot"))

p("rm -R debian")

print("RUN ON YOUR HOST debsign -k '9FCE 0930 7C7D A5B0 6E3C AC79 409C B5A2 2813 3CC6' %s*.changes" % (PACKAGE,))
dput = "dput --config '%s'" % dput_cfg
if args.dist == "debian":
    fail(p("%s local %s*.changes" % (dput, PACKAGE)))
else:
    if args.release:
        print("RUN IN CONTAINER %s stable %s*.changes" % (dput, PACKAGE))
    else:
        print("RUN IN CONTAINER %s unstable %s*.changes" % (dput, PACKAGE))
