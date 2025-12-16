#!/bin/sh
mkdir -p benchmark/benchmark_results
mkdir -p benchmark/profiles

hyperfine --show-output -r 5  --export-json "benchmark/benchmark_results/results.json"\
            --setup "source /home/lorenzo/.cache/pypoetry/virtualenvs/pyes-YsROe161-py3.10/bin/activate"\
            --parameter-list file_name ac,phoenix_var,urine_silvia_modelA_solid_var,urine_silvia_modelA_solid_var_error,artici\
            "PYTHONPATH="." python benchmark/test.py mockup/{file_name}.json"\
            --cleanup "PYTHONPATH="." poetry run pyinstrument -o benchmark/profiles/profile_{file_name}.html benchmark/test.py mockup/{file_name}.json & (deactivate  || true)"

poetry run python benchmark/benchmark_viz/advanced_statistics.py benchmark/benchmark_results/results.json > benchmark/benchmark_results/advanced_statistics.log
poetry run python benchmark/benchmark_viz/plot_whisker.py benchmark/benchmark_results/results.json --output benchmark/benchmark_results/whisker_plt_results.png