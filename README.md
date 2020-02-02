gPodder PPA Scripts
======================

* Adapted from https://github.com/quodlibet/ppa-scripts
* Only works for Ubuntu 18.04 and up.
* No debian or rpm repos


# Usage

	# git clone git@github.com:gpodder/ppa-scripts.git gpodder-ppa-scripts
	# cd gpodder-ppa-scripts

Edit `gpodder.py` for newer **PPA_VERSION** and **RELEASE_VERSION**.

Create the docker image with devscripts:

	# docker build -t ubuntu:18.04-devscripts .

Run an interactive shell in a new container from this image:

	# docker run --rm -it --name ppa -v $(pwd)/gpodder-ppa-scripts:/root/gpodder-ppa-scripts ubuntu:18.04-devscript

Inside, run `gpodder.py` to build `*.changes` files for unstable build and `gpodder.py --release` for stable build:

	# cd /root/gpodder-ppa-scripts/
	# ./gpodder.py

Take note of last two lines:
 - first (signing) must be run on your host, where you have your gpg key
 - second (dput) must be run in the container to upload packages
