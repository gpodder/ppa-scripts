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
	# ./gpodder.py --try-build  # try building the snapshot release
	# ./gpodder.py  # snapshot release
	# ./gpodder.py -r --try-build  # try building the release
	# ./gpodder.py -r # stable release

Take note of last two lines:
 - first (signing) must be run on your host, where you have your gpg key
 - second (dput) must be run in the container to upload packages

Wait about 1/2 hour for builds to finish (mail notification / status on the ppa page).

## Building for newer ubuntu releases

When a newer ubunut release is out, we need to upload a new version, even if no new gPodder
version is out.

[Copying packages](https://documentation.ubuntu.com/launchpad/user/reference/packaging/ppas/copying-packages/#copying-packages) doesn't work.


1. check https://launchpad.net/~gpodder/+archive/ubuntu/ppa/+packages for the latest `+X` version.
   Eg to rebuild for questing I had to use the `-v 5` flag, resulting in version  `3.11.5+5-0~ppa5~questing`
   of the package.

2. increment the version: `./gpodder.py -r -v 6`

# Links
https://help.launchpad.net/Packaging/PPA/BuildingASourcePackage
https://help.launchpad.net/Packaging/PPA/Uploading
