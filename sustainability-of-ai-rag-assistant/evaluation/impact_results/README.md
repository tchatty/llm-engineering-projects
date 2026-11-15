# Impact results

Generated local-compute measurement results live in `codecarbon/` and are excluded from source control
(they contain machine-specific hardware, geographic and operating-system metadata). Only this README is committed.

Layout: `codecarbon/<experiment>/<experiment_id>/` holds CodeCarbon's native `emissions.csv` and a sanitized `manifest.json`
(`detect` holds `hardware_detect.txt`). `codecarbon/summary.json` and `summary.csv` hold descriptive statistics.

Native units: duration in seconds, energy in kWh, emissions in kg CO2eq. Missing values stay empty/null.

Commands (run from `sustainability-of-ai-rag-assistant/`, one repetition per process):

    uv run python evaluation/measure_local_compute.py detect
    uv run python evaluation/measure_local_compute.py smoke --repetition 1
    uv run python evaluation/measure_local_compute.py coldstart --repetition 1
    uv run python evaluation/measure_local_compute.py retrieval --operations 100 --repetition 1
    uv run python evaluation/summarize_codecarbon_results.py
