1. cmake -S . -B build
cmake --build build

2. pip3 install -r requirements.txt

# Check the path if necessary
# Build in the current path (Recommend)
python3 setup.py build_ext -i
# or install
python3 setup.py install