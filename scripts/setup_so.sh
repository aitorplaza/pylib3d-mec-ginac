#!/usr/bin/env bash
set -euo pipefail

# ===== Config =====
PY_VER=3.12.10
PY_SHORT=3.12
VTK_TAG=v9.0.1

# ===== Paquetes base =====
sudo apt update
sudo apt install -y git python3.7 make
sudo apt install -y python3-pip
sudo python3.7 -m pip install --upgrade pip
sudo apt remove -y python3-pip

sudo apt-get install -y build-essential python3.7-dev

sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.7 10
sudo update-alternatives --install /usr/bin/pip pip /usr/local/bin/pip3.7 10

sudo apt install -y make-guile

sudo apt-get install -y autoconf automake libtool

sudo apt install -y libfreetype6-dev libexpat1-dev
sudo apt install -y gperf pkg-config

sudo apt install -y mesa-utils=8.4.0-1 libsm6=2:1.2.2-1 libxrender1=1:0.9.10-1 libfontconfig1=2.12.6-0ubuntu2 

sudo apt-get install -y libgl1-mesa-dev 
sudo apt-get install -y texinfo
sudo apt-get install -y bison flex

sudo apt install -y libreadline-dev
sudo apt install -y transfig
sudo apt install -y doxygen
sudo apt install -y texlive-latex-base texlive-latex-extra texlive-fonts-recommended
sudo apt install -y texlive-fonts-extra dvipng


# ===== Paquetes Python =====
pip install setuptools wheel
pip install testresources pyglet==1.3.2 Cython==0.29.36

# ===== Compilar e instalar CLN en la versión 1.3.4 =====
cd ~/Escritorio
git clone git://www.ginac.de/cln.git
cd cln
git checkout 9b86a7f
autoreconf -i
./configure
make
sudo make install
cd ..

# ===== Compilar e instalar GiNaC en la versión 1.7.7 =====
git clone git://www.ginac.de/ginac.git
cd ginac
git checkout d3ed101
autoreconf -i
./configure
make
sudo make install
cd ..

# ===== Compilar e instalar Fontconfig en la versión 2.12.6 =====
wget https://www.freedesktop.org/software/fontconfig/release/fontconfig-2.12.6.tar.gz
tar -xf fontconfig-2.12.6.tar.gz
cd fontconfig-2.12.6
./configure
make
sudo make install
cd ..

# Librerías necearias
sudo apt install -y libgmp-dev

# ===== Compilar e instalar la librería mpfr en la versión 3.1.6 =====
wget https://www.mpfr.org/mpfr-3.1.6/mpfr-3.1.6.tar.gz
tar -xzf mpfr-3.1.6.tar.gz
cd mpfr-3.1.6
./configure --prefix=/opt/mpfr-3.1.6
make
sudo make install
cd ..

# ===== Compilar e instalar la librería mpc en la versión 1.0.3 =====
wget https://ftp.gnu.org/gnu/mpc/mpc-1.0.3.tar.gz
tar -xzf mpc-1.0.3.tar.gz
cd mpc-1.0.3
./configure --prefix=/opt/mpc-1.0.3 --with-mpfr=/opt/mpfr-3.1.6
make
sudo make install
cd ..

# ===== Compilar e instalar la librería isl en la versión 0.18 =====
wget https://libisl.sourceforge.io/isl-0.18.tar.gz
tar -xzf isl-0.18.tar.gz
cd isl-0.18
./configure --prefix=/opt/isl-0.18
make
sudo make install
cd ..

# Rutas necesarias para la instalación de GCC 7.4.0
echo 'export LD_LIBRARY_PATH=/opt/mpfr-3.1.6/lib:/opt/mpc-1.0.3/lib:/opt/isl-0.18/lib:${LD_LIBRARY_PATH:-}' | tee -a ~/.bashrc
echo 'export CPATH=/opt/mpfr-3.1.6/include:/opt/mpc-1.0.3/include:/opt/isl-0.18/include:${CPATH:-}' | tee -a ~/.bashrc
echo 'export PKG_CONFIG_PATH=/opt/mpfr-3.1.6/lib/pkgconfig:/opt/mpc-1.0.3/lib/pkgconfig:/opt/isl-0.18/lib/pkgconfig:${PKG_CONFIG_PATH:-}' | tee -a ~/.bashrc

# Dependencias de 32 bits
sudo apt install -y libc6-dev-i386 lib32gcc-7-dev

# ===== Compilar e instalar GCC 7.4.0 =====
wget https://ftp.gnu.org/gnu/gcc/gcc-7.4.0/gcc-7.4.0.tar.gz
tar -xzf gcc-7.4.0.tar.gz
cd gcc-7.4.0
./configure --with-mpfr=/opt/mpfr-3.1.6 --with-mpc=/opt/mpc-1.0.3
make
sudo make install
cd ..

sudo update-alternatives --install /usr/bin/python python /usr/bin/python2.7 1

# ===== Comandos posiblemente inútiles =====
echo "-I/usr/local/include" | sudo tee /etc/g++-include.conf
export CPLUS_INCLUDE_PATH=/usr/local/include
echo "/usr/local/lib" | sudo tee /etc/ld.so.conf.d/local.conf
sudo ldconfig
export LIBRARY_PATH=/usr/local/lib
export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH

# ===== Instalar pylib3d-mec-ginac =====
cd ~/Escritorio
git clone --depth 1 https://github.com/aitorplaza/pylib3d-mec-ginac.git

# ===== Generar el archivo so =====
make doSoFile

# ===== Instalar pylib3d-mec-ginac =====
cd pylib3d-mec-ginac
./install.sh
sudo pip install .