# tempkit — analysis toolkit for *V16 Temperaturmessung*

`tempkit` is a small, dependency-free Python package that turns the raw
temperature readings recorded during the *V16 Temperaturmessung* lab into the
numbers that appear in the written report (`main.tex` / `V16_Temperaturmessung.pdf`).

It is deliberately self-contained: only the Python standard library is used at
runtime, so it runs inside CI without an install step. `pytest` is the only
development dependency.

## Package layout

| Module | Responsibility |
| ------ | -------------- |
| `tempkit.units` | Temperature unit conversions (°C ↔ K ↔ °F). |
| `tempkit.models` | Typed containers: `Measurement`, `MeasurementSeries`, `Sensor`. |
| `tempkit.statistics` | Mean, variance, standard error, ordinary least squares `linear_regression`. |
| `tempkit.io` | Reading/writing the CSV measurement logs. |
| `tempkit.analysis` | Newton-cooling fit (`fit_cooling`) and raw `regression_line`. |
| `tempkit.report` | Human-readable dataset summaries. |
| `tempkit.cli` | `python -m tempkit.cli …` command line entry point. |

## The physical model

The experiment is described by Newton's law of cooling,

```
T(t) = T_ambient + (T0 - T_ambient) · exp(-t / τ)
```

which linearises to

```
ln(T(t) - T_ambient) = ln(T0 - T_ambient) - t / τ.
```

`fit_cooling` fits a straight line to `ln(delta)` against `t` and reports the
time constant `τ = -1/slope` together with its uncertainty.

## The dataset

`data/` contains the measurement logs as CSV files with the columns:

```
measurement_id,run_id,sensor_id,t_seconds,temperature_c,ambient_c
```

The data is a large, deterministically generated set of cooling runs (see
`data/README.md` for the exact generation parameters) so results are fully
reproducible.

## Usage

Summarise the whole dataset:

```bash
python -m tempkit.cli summary data
```

Fit a single run and print its time constant:

```bash
python -m tempkit.cli fit data --run 1
```

From Python:

```python
from tempkit.io import load_dataset
from tempkit.analysis import cooling_fits_by_run

series = load_dataset("data")
for run_id, fit in cooling_fits_by_run(series).items():
    print(run_id, fit.tau_s, fit.r_squared)
```

## Running the tests

```bash
pip install pytest
pytest
```
