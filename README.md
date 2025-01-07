gPodder PPA Scripts
======================

* Adapted from https://github.com/quodlibet/ppa-scripts
* Only works for Ubuntu 24.04 and up.
* No debian or rpm repos


# Usage

	# git clone git@github.com:gpodder/ppa-scripts.git gpodder-ppa-scripts
	# cd gpodder-ppa-scripts

Edit `gpodder.py` for newer **PPA_VERSION** and **RELEASE_VERSION**.

Create the docker image with devscripts:

	# docker build -t ubuntu:24.04-devscripts .

Run an interactive shell in a new container from this image:

	# docker run --rm -it --name ppa -v $(pwd):/root/gpodder-ppa-scripts ubuntu:24.04-devscripts


Import your gpg keys in the container

	# gpg --keyserver keyserver.ubuntu.com --recv-key 409CB5A228133CC6

Inside, run `gpodder.py` to build `*.changes` files for unstable build and `gpodder.py --release` for stable build:

	# cd /root/gpodder-ppa-scripts/
	# ./gpodder.py  # snapshot release
	# ./gpodder.py -r # stable release

Take note of last two lines:
 - first (signing) must be run on your host, where you have your gpg key
 - second (dput) must be run in the container to upload packages

Wait about 1/2 hour for builds to finish (mail notification / status on the ppa page).

# Links
https://help.launchpad.net/Packaging/PPA/BuildingASourcePackage
https://help.launchpad.net/Packaging/PPA/Uploading
