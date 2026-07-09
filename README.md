# STARE_NEXT

研究用の地震関連データ探索パイプラインです。公開外部データと、Excel
`資料3_地震・測地データの一覧.xlsx` に含まれる地震・測地データ候補を総当たりに近い形で組み合わせ、ラグ付き相関や単純モデルで「関連があれば面白い外部信号」をスクリーニングします。

このコードは地震予測を断定するものではありません。多重検定、API制限、欠測、地震後の社会的反応を必ず考慮してください。

## データ候補

Excelの全シートを検査し、`results/metadata/dataset_registry.csv` に以下を正規化して保存します。

- `dataset_id`
- `name`
- `category`
- `provider`
- `description`
- `url`
- `access_type`
- `notes`
- `usable_status`

外部データAdapterはS/Aランク候補を実装しています。

- S: Google Trends, Wikimedia Pageviews, GDELT, NOAA GloTEC/TEC, NOAA Kp/Dst, AIST Well Web
- A: Movebank, eBird, iNaturalist, GBIF, OpenAQ, NASA FIRMS, TEPCO, OpenSky

認証、申請、利用規約確認、安定した機械可読エンドポイントが必要なものは無理に取得せず、`results/failures.jsonl` と `results/metadata/probe_reports/*.json` にskip理由を残します。

## 使い方

依存関係を入れる場合:

```bash
python -m pip install -r requirements.txt
```

probeだけ実行:

```bash
python -m src.main --probe-only
```

MVP実行例:

```bash
python -m src.main \
  --excel "資料3_地震・測地データの一覧.xlsx" \
  --start-date 2026-07-01 \
  --end-date 2026-07-09 \
  --external-source wikimedia \
  --excel-dataset auto \
  --output-dir results \
  --cleanup-raw true
```

仕様書の長期例:

```bash
python -m src.main \
  --excel "資料3_地震・測地データの一覧.xlsx" \
  --start-date 2020-01-01 \
  --end-date 2024-12-31 \
  --spatial-unit prefecture \
  --time-freq 1D \
  --lags "-14D,-7D,-3D,-1D,-12H,-6H,-1H,1H,6H,12H,1D,3D,7D,14D" \
  --output-dir results \
  --cleanup-raw true
```

`--excel-dataset auto` では、長期探索用に気象庁の地震月報（カタログ編）震源データを優先します。年別ZIPを取得して固定長フォーマットをパースし、日次の件数、M4/M5フラグ、エネルギー和、最大Mへ集約します。公開済みZIPがない年はfailureとして記録し、その年はゼロ埋めします。

## 必要なAPIキー

- `EBIRD_API_KEY`: eBird API
- `NASA_FIRMS_MAP_KEY`: NASA FIRMS
- `OPENAQ_API_KEY`: OpenAQ v3

`.env` に上記キーを置くこともできます。Google Trendsは `pytrends` が利用でき、かつアクセス制限にかからない場合のみ取得します。Movebank等の申請・ログインが必要なデータはskipします。

## 出力

- `results/summary.csv`
- `results/summary.parquet`（pandas/pyarrow がある場合）
- `results/per_pair_metrics.csv`
- `results/per_pair_metrics.parquet`（pandas/pyarrow がある場合）
- `results/top_findings.md`
- `results/run_log.jsonl`
- `results/failures.jsonl`
- `results/source_pipeline_status.csv`
- `results/figures/`
- `results/metadata/dataset_registry.csv`
- `results/metadata/excel_inspection.json`
- `results/metadata/probe_reports/`

raw downloadは `cache/raw/` または `tmp/` 配下に置き、通常はAdapter終了時に削除します。`--keep-raw` を指定した場合だけ残します。

## 失敗・skipの扱い

各Adapterは最初に `probe()` を実行し、HTTPステータス、Content-Type、レスポンス先頭、サンプルキーなどをJSONで保存します。APIレスポンスやデータ形式が想定と違う場合、全体を止めず、そのソースまたはペアだけ `failures.jsonl` に記録して次へ進みます。

`results/source_pipeline_status.csv` には各外部ソースの `probe_ok` / `fetch_ok` / `aggregate_ok` / `modeled_ok` 到達状況と、未到達理由を保存します。GDELTは年単位に分割し、1 request / 5 secを守るsleep/retry/cacheを実装しています。rate limitやtimeoutが続く場合は全体探索を止めずskipします。

外部特徴量はraw countに加え、7日/30日移動平均との差、day-of-year平均との差、month fixed effect除去後の残差、`log1p(count)` の前年差を生成します。モデル評価ではmonth、day-of-week、weekend/holiday、year trendを残差化してから相関・回帰・AUCを計算します。日次データではsub-daily lagを無効化し、比較用の反応方向を含めて `±1D/±3D/±7D/±14D` のみを使います。

## 解釈上の注意

ラグは正方向と負方向を分けて記録します。正のラグは外部データが先、地震側ターゲットが後です。負のラグで強い関連が出た場合は、前兆ではなく地震後の検索・報道・観測反応である可能性が高いです。
