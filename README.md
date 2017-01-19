## Build libSCOTCH 6.0.4

```
sudo apt-get install bison libbison-dev flex

# Download and unpack
mkdir scotch/
cd scotch/
wget http://gforge.inria.fr/frs/download.php/latestfile/298/scotch_6.0.4.tar.gz
tar -xvzf scotch_6.0.4.tar.gz
cd scotch_6.0.4/src/

# Creating the "Makefile.inc" file - see INSTALL.txt
ln -s Make.inc/Makefile.inc.i686_pc_linux2.shlib.debug Makefile.inc

# Build the library
cd libscotch
make VERSION=6 RELEASE=0 PATCHLEVEL=4 libscotcherr.so
make VERSION=6 RELEASE=0 PATCHLEVEL=4 libscotch.so

```

## Build SCOTCH

```
cd scotch_6.0.4/src/
make scotch

```

