# Space Weather 4 Excel Scan

Exploratory pipeline for four public continuous space-weather and geomagnetic data families against earthquake, geodetic, ocean, groundwater, intensity, and related datasets listed in `資料3_地震・測地データの一覧.xlsx`.

External source groups:

- `kp_dst`: GFZ Kp and Kyoto WDC Dst
- `glotec`: NOAA GloTEC / TEC probe and coverage tracking
- `omni`: NASA CDAWeb HAPI OMNI hourly solar wind / IMF / geomagnetic indices
- `intermagnet` / `jma_geomag`: observatory metadata probes
- `combined`: lightweight combined proxy features from available fetched groups

Run:

```bash
python -m src.main \
  --excel "../../資料3_地震・測地データの一覧.xlsx" \
  --start-date 2020-01-01 \
  --end-date 2024-12-31 \
  --spatial-unit national \
  --lags "-30D,-14D,-7D,-3D,-1D,0D,1D,3D,7D,14D,30D" \
  --source all \
  --dataset 気象庁_地震月報_カタログ編 \
  --output-dir results \
  --cleanup-raw true
```

Other modes:

```bash
python -m src.main --probe-only
python -m src.main --source kp_dst
python -m src.main --source glotec
python -m src.main --source omni
python -m src.main --source intermagnet
python -m src.main --source jma_geomag
python -m src.main --source combined
python -m src.main --source all --dataset all
python -m src.main --combined-models
python -m src.main --resume
python -m src.main --force
python -m src.main --keep-raw
```

Outputs are written to `results/space_weather4_*.csv`, `results/metadata/`, and `results/figures/`.

Interpretation guardrail: this is a multiple-comparison, hypothesis-generating screen. It does not claim earthquake prediction or causality.
