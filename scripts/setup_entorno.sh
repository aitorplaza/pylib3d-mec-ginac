#!/usr/bin/env bash
set -euo pipefail

# ===== Config =====
PY_VER=3.12.10
PY_SHORT=3.12
VTK_TAG=v9.0.1
RUN_PYLIB3D_INSTALL=1   # pon 0 si quieres que se detenga tras clonar/parchear

# ===== Paquetes base =====
sudo apt update
sudo apt install -y git build-essential zlib1g-dev libncurses5-dev libgdbm-dev \
  libnss3-dev libssl-dev libreadline-dev libffi-dev libsqlite3-dev libbz2-dev \
  wget pkg-config uuid-dev xz-utils liblzma-dev curl ca-certificates \
  libncursesw5-dev tk-dev tcl-dev tk8.6 tcl8.6 libx11-dev libxext-dev \
  libxrender-dev libxss-dev libgl1-mesa-glx libglu1-mesa freeglut3-dev \
  libxi-dev libxmu-dev libxrandr-dev libxinerama-dev libxcursor-dev \
  libglfw3-dev cmake cmake-curses-gui || true

sudo apt install -y mesa-utils=8.4.0-1 libsm6=2:1.2.2-1 libxrender1=1:0.9.10-1 libfontconfig1=2.12.6-0ubuntu2 || true

# Opcional; si no existe en tu distro, se ignora sin fallar
sudo apt install -y libnsl-dev || true

# ===== Compilar e instalar Python ${PY_VER} =====
cd ~/Escritorio
wget -q https://www.python.org/ftp/python/${PY_VER}/Python-${PY_VER}.tgz
tar xzf Python-${PY_VER}.tgz
cd Python-${PY_VER}

export TCLTK_CFLAGS="-I/usr/include/tcl8.6 -I/usr/include/tk -I/usr/include/tcl"
export TCLTK_LIBS="-L/usr/lib/x86_64-linux-gnu -ltk8.6 -ltcl8.6"
export CPPFLAGS="${TCLTK_CFLAGS} ${CPPFLAGS:-}"
export LDFLAGS="${TCLTK_LIBS} ${LDFLAGS:-} -L/usr/lib/x86_64-linux-gnu -Wl,-rpath,/usr/local/lib"
export PKG_CONFIG_PATH="/usr/lib/x86_64-linux-gnu/pkgconfig:${PKG_CONFIG_PATH:-}"

./configure --enable-optimizations --enable-shared --with-ensurepip=install \
  --prefix=/usr --libdir=/usr/lib --includedir=/usr/include --with-lto
make -j$(nproc)
sudo make altinstall
cd ..

echo "/usr/lib" | sudo tee /etc/ld.so.conf.d/python${PY_SHORT//./}.conf >/dev/null
sudo ldconfig

sudo update-alternatives --install /usr/bin/pip pip /usr/bin/pip${PY_SHORT} 10
sudo update-alternatives --install /usr/bin/python python /usr/bin/python${PY_SHORT} 10

pip --version && python --version
python - <<'PY'
# Test rápido de tkinter (no abre ventana, sólo verifica disponibilidad)
import tkinter as tk; print("tkinter OK, version:", tk.TkVersion)
PY

# ===== Paquetes Python =====
pip install setuptools wheel
pip install testresources pyglet==1.3.2 Cython==0.29.36

# Opcional de tu lista
sudo snap install openscad || true

# ===== Compilar VTK =====
cd ~/Escritorio
git clone --branch ${VTK_TAG} --depth 1 https://github.com/Kitware/VTK.git
cd VTK
git checkout "${VTK_TAG}"
mkdir build && cd build

# Rutas dinámicas de Python (sin hardcodear)
PY_EXE=$(which python)
PY_INC=$(${PY_EXE} -c "from sysconfig import get_paths as gp; print(gp()['include'])")
PY_LIB=$(${PY_EXE} -c "import sysconfig; print(sysconfig.get_config_var('LIBDIR') + '/' + sysconfig.get_config_var('LDLIBRARY'))")
VTK_PY_SPKG_SUFFIX="python${PY_SHORT}/site-packages"

cmake .. \
  -DCMAKE_INSTALL_PREFIX=/usr/lib \
  -DCMAKE_INSTALL_LIBDIR=. \
  -DCMAKE_BUILD_TYPE=Release \
  -DBUILD_SHARED_LIBS=ON \
  -DVTK_WRAP_PYTHON=ON \
  -DVTK_PYTHON_VERSION=3 \
  -DPython3_EXECUTABLE="${PY_EXE}" \
  -DPython3_INCLUDE_DIR="${PY_INC}" \
  -DPython3_LIBRARY="${PY_LIB}" \
  -DVTK_GROUP_ENABLE_Qt=NO \
  -DVTK_GROUP_ENABLE_StandAlone=YES \
  -DVTK_GROUP_ENABLE_Rendering=YES \
  -DVTK_USE_TK=ON \
  -DVTK_PYTHON_SITE_PACKAGES_SUFFIX="${VTK_PY_SPKG_SUFFIX}"

make -j$(nproc)
sudo make install

echo "/usr/lib" | sudo tee /etc/ld.so.conf.d/vtk.conf >/dev/null
sudo ldconfig

# Comprobación: VTK en Python (usa importlib; crea shim si falta 'vtk')
python - <<'PY'
import os, importlib.util
def spec(name):
    return importlib.util.find_spec(name)
print("vtk spec:", spec("vtk"))
print("vtkmodules spec:", spec("vtkmodules"))
if spec("vtk") is None and spec("vtkmodules") is not None:
    root = os.path.dirname(spec("vtkmodules").submodule_search_locations[0])
    vtk_dir = os.path.join(root, "vtk")
    os.makedirs(vtk_dir, exist_ok=True)
    init_py = os.path.join(vtk_dir, "__init__.py")
    if not os.path.exists(init_py):
        with open(init_py, "w") as f:
            f.write("from vtkmodules.all import *\n")
    import importlib; importlib.invalidate_caches()
import vtk
from vtk import vtkRenderWindow
print("VTK OK:", vtk.vtkVersion.GetVTKVersion(), "->", vtk.__file__)
PY

# ===== Clonar y parchear pylib3d-mec-ginac =====
cd ~/Escritorio
if [ ! -d pylib3d-mec-ginac ]; then
  git clone https://github.com/aitorplaza/pylib3d-mec-ginac.git
fi
cd pylib3d-mec-ginac
 
# --- Parche 1: comprobar versión de Python
sed -i 's/\"\$PYTHON_VERSION\" != \"3\.7\"/\"\$PYTHON_VERSION\" >= \"3.7\"/' install.sh || true

# --- Parche 2: no atar el "Location" de pip a 3.7
sed -i 's/grep Location | grep 3\.7/grep Location/' install.sh || true

# --- Parche 3: eliminar dependencia de VTK y eliminar el enlace a la dependencia
sed -i '/if INSTALL_GUI:/{
N
/DEPENDENCIES\.append('"'"'vtk-tk>=9\.0\.0'"'"')/d
/DEPENDENCY_LINKS\.append('"'"'https:\/\/vtk-tk-support\.herokuapp\.com\/'"'"')/d
}' setup.py

# --- Parche 4: añadir 'import sys' en el editor (para evitar el NameError)
#   Lo parcheamos en el repo antes de instalar, para que se instale ya bien.
EDITOR_PY="src/gui/idle/editor.py"
if [ -f "${EDITOR_PY}" ]; then
  if ! head -n 5 "${EDITOR_PY}" | grep -q '^import sys'; then
    sed -i '1i import sys' "${EDITOR_PY}"
  fi
fi

# --- Parche 5: añadir 'import re' en el editor (para evitar el NameError)
#   Lo parcheamos en el repo antes de instalar, para que se instale ya bien.
if [ -f "${EDITOR_PY}" ]; then
  if ! head -n 5 "${EDITOR_PY}" | grep -q '^import re'; then
    sed -i '2i import re' "${EDITOR_PY}"
  fi
fi

# ===== Instalar el proyecto (opcional) =====
if [ "${RUN_PYLIB3D_INSTALL}" = "1" ]; then
  chmod +x install.sh || true
  ./install.sh || true    # si hace cosas específicas del entorno
  sudo pip install .
fi

echo "Todo listo. Si instalaste el proyecto, prueba:"
echo "  python -m lib3d_mec_ginac examples/four_bar"

python -m lib3d_mec_ginac /~/Escritorio/pylib3d-mec-ginac/examples/four_bar