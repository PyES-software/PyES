#!/bin/sh
for filename in src/main/python/pyes/ui/*.ui; do
    poetry run pyside6-uic $filename -o ${filename%%.*}.py
done
for filename in src/main/python/pyes/ui/widgets/*.ui; do
    poetry run pyside6-uic $filename -o ${filename%%.*}.py
done
poetry run pyside6-rcc src/main/resources/base/resources.qrc -o src/main/python/pyes/resources_rc.py
echo "Qt files compiled!"

poetry run python scripts/icon_creator.py
echo "Icons updated!"
