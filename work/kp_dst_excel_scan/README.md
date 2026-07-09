# Kp/Dst Excel Scan

Focused exploratory pipeline for Kp/Dst geomagnetic indices against earthquake/geodetic datasets listed in the STAR-E Excel workbook.

Run:

```bash
python -m src.main \
  --excel "../../資料3_地震・測地データの一覧.xlsx" \
  --start-date 2020-01-01 \
  --end-date 2024-12-31 \
  --spatial-unit national \
  --lags "-30D,-14D,-7D,-3D,-1D,0D,1D,3D,7D,14D,30D" \
  --output-dir results \
  --cleanup-raw true
```

Other modes:

```bash
python -m src.main --probe-only
python -m src.main --dataset 気象庁_地震月報_カタログ編
python -m src.main --dataset all --kp-only
python -m src.main --dataset all --include-dst
python -m src.main --resume
python -m src.main --force
python -m src.main --keep-raw
```

The pipeline writes stage status, per-pair metrics, candidate precursor filters, reverse-lag signals, static interaction placeholders, probe reports, and top findings into `results/`.

Interpretation guardrail: all outputs are hypothesis-generating only. Passing controls or FDR filters is not evidence of earthquake prediction or causality.
