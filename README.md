# Proyecto ANN - LIESE

## Integrantes

## Requerimientos
##### Python 3.12
##### Openvino 2023
Instalar las librerias necesarias con los siguientes comandos:
```bash
git clone https://github.com/openvinotoolkit/openvino.git
cd openvino
git submodule update --init --recursive
chmod +x install_build_dependencies.sh
chmod +x install_build_dependencies.sh
mkdir build && cd build
cmake -DCMAKE_BUILD_TYPE=Release ..
make --jobs=$(nproc --all)
pip install -r requirements-dev.txt
-DPython3_EXECUTABLE=/usr/bin/python3.8
pip install -r <openvino source tree>/src/bindings/python/wheel/requirements-dev.txt
export PYTHONPATH=<openvino_repo>/bin/intel64/Release/python:$PYTHONPATH
export LD_LIBRARY_PATH=<openvino_repo>/bin/intel64/Release:$LD_LIBRARY_PATH
pip install <openvino_repo>/build/wheel/openvino-2022.2.0-000-cp37-cp37-manylinux_2_35_x86_64.whl
```
Más información en:
https://docs.openvino.ai/2024/get-started/install-openvino.html?PACKAGE=OPENVINO_BASE&VERSION=v_2023_3_0&OP_SYSTEM=LINUX&DISTRIBUTION=GITHUB


