#/bin/sh

PYTHONPATH="." poetry run pyinstrument -o benchmark/profile.html benchmark/test.py mockup/urine_silvia_modelA_solid_var_error.json
xdg-open benchmark/profile.html > /dev/null