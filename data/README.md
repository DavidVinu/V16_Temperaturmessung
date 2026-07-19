# Measurement dataset

This directory holds the temperature measurement logs analysed by `tempkit`.

## File format

Each `run_data_*.csv` file is a plain comma-separated file with a single
header row and one reading per line:

```
measurement_id,run_id,sensor_id,t_seconds,temperature_c,ambient_c
```

| Column | Unit | Description |
| ------ | ---- | ----------- |
| `measurement_id` | – | Globally unique, monotonically increasing reading id. |
| `run_id` | – | Identifier of the cooling run the reading belongs to. |
| `sensor_id` | – | Identifier of the thermocouple that took the reading. |
| `t_seconds` | s | Elapsed time since the start of the run. |
| `temperature_c` | °C | Measured temperature. |
| `ambient_c` | °C | Ambient (room) temperature at the time of the reading. |

## How the data was generated

The logs are produced deterministically by `scripts/generate_dataset.py`
(seed `20260719`) so the analysis is fully reproducible. Every run follows
Newton's law of cooling,

```
T(t) = T_ambient + (T0 - T_ambient) · exp(-t / τ)
```

with a small amount of Gaussian sensor noise added on top. The per-run
parameters (`T0`, `T_ambient`, `τ`) are drawn from physically plausible
ranges matching the conditions of the *V16 Temperaturmessung* experiment.

To regenerate the dataset from scratch:

```bash
python scripts/generate_dataset.py
```
