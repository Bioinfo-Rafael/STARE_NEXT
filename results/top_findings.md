# Top Findings

探索結果は仮説生成用です。地震予測を断定するものではありません。正のラグは外部信号が先、負のラグは地震側が先の反応方向です。

## 1. inaturalist:inaturalist_observations × 気象庁_地震月報_カタログ編:max_magnitude
- ラグ: 3D (external_precedes_target)
- モデル: correlation+ols+logistic_probe
- 効果量: correlation=-0.4833641205999488, coefficient=-0.0016817720903906212
- p値/FDR: p=0.0196078431372549, q=0.04084967320261438
- 検証性能: AUC=None, rate_ratio=0.6588364034856977
- 解釈: 多重検定込みの探索的シグナル。前兆方向か反応方向かを必ず確認してください。
- 注意点: 公開APIの取得範囲、欠測、報道量・投稿量バイアス、地震後反応の混入に注意。
- データ取得状況: status=ok

## 2. inaturalist:inaturalist_observations × 気象庁_地震月報_カタログ編:max_magnitude
- ラグ: 1H (external_precedes_target)
- モデル: correlation+ols+logistic_probe
- 効果量: correlation=-0.48298513292697287, coefficient=-0.0016809173507694095
- p値/FDR: p=0.0196078431372549, q=0.04084967320261438
- 検証性能: AUC=None, rate_ratio=0.656216204226025
- 解釈: 多重検定込みの探索的シグナル。前兆方向か反応方向かを必ず確認してください。
- 注意点: 公開APIの取得範囲、欠測、報道量・投稿量バイアス、地震後反応の混入に注意。
- データ取得状況: status=ok

## 3. inaturalist:inaturalist_observations × 気象庁_地震月報_カタログ編:max_magnitude
- ラグ: 6H (external_precedes_target)
- モデル: correlation+ols+logistic_probe
- 効果量: correlation=-0.48298513292697287, coefficient=-0.0016809173507694095
- p値/FDR: p=0.0196078431372549, q=0.04084967320261438
- 検証性能: AUC=None, rate_ratio=0.656216204226025
- 解釈: 多重検定込みの探索的シグナル。前兆方向か反応方向かを必ず確認してください。
- 注意点: 公開APIの取得範囲、欠測、報道量・投稿量バイアス、地震後反応の混入に注意。
- データ取得状況: status=ok

## 4. inaturalist:inaturalist_observations × 気象庁_地震月報_カタログ編:max_magnitude
- ラグ: 12H (external_precedes_target)
- モデル: correlation+ols+logistic_probe
- 効果量: correlation=-0.48298513292697287, coefficient=-0.0016809173507694095
- p値/FDR: p=0.0196078431372549, q=0.04084967320261438
- 検証性能: AUC=None, rate_ratio=0.656216204226025
- 解釈: 多重検定込みの探索的シグナル。前兆方向か反応方向かを必ず確認してください。
- 注意点: 公開APIの取得範囲、欠測、報道量・投稿量バイアス、地震後反応の混入に注意。
- データ取得状況: status=ok

## 5. inaturalist:inaturalist_observations × 気象庁_地震月報_カタログ編:max_magnitude
- ラグ: 1D (external_precedes_target)
- モデル: correlation+ols+logistic_probe
- 効果量: correlation=-0.48074955690859833, coefficient=-0.0016730732369915715
- p値/FDR: p=0.0196078431372549, q=0.04084967320261438
- 検証性能: AUC=None, rate_ratio=0.6593101414643197
- 解釈: 多重検定込みの探索的シグナル。前兆方向か反応方向かを必ず確認してください。
- 注意点: 公開APIの取得範囲、欠測、報道量・投稿量バイアス、地震後反応の混入に注意。
- データ取得状況: status=ok

## 6. inaturalist:inaturalist_observations × 気象庁_地震月報_カタログ編:max_magnitude
- ラグ: 7D (external_precedes_target)
- モデル: correlation+ols+logistic_probe
- 効果量: correlation=-0.48068651262963585, coefficient=-0.001671538523690739
- p値/FDR: p=0.0196078431372549, q=0.04084967320261438
- 検証性能: AUC=None, rate_ratio=0.6560420716440742
- 解釈: 多重検定込みの探索的シグナル。前兆方向か反応方向かを必ず確認してください。
- 注意点: 公開APIの取得範囲、欠測、報道量・投稿量バイアス、地震後反応の混入に注意。
- データ取得状況: status=ok

## 7. gbif:gbif_occurrences × 気象庁_地震月報_カタログ編:max_magnitude
- ラグ: 1H (external_precedes_target)
- モデル: correlation+ols+logistic_probe
- 効果量: correlation=-0.4606887512036605, coefficient=-0.000897085335179547
- p値/FDR: p=0.0196078431372549, q=0.04084967320261438
- 検証性能: AUC=None, rate_ratio=0.6203354725549312
- 解釈: 多重検定込みの探索的シグナル。前兆方向か反応方向かを必ず確認してください。
- 注意点: 公開APIの取得範囲、欠測、報道量・投稿量バイアス、地震後反応の混入に注意。
- データ取得状況: status=ok

## 8. gbif:gbif_occurrences × 気象庁_地震月報_カタログ編:max_magnitude
- ラグ: 6H (external_precedes_target)
- モデル: correlation+ols+logistic_probe
- 効果量: correlation=-0.4606887512036605, coefficient=-0.000897085335179547
- p値/FDR: p=0.0196078431372549, q=0.04084967320261438
- 検証性能: AUC=None, rate_ratio=0.6203354725549312
- 解釈: 多重検定込みの探索的シグナル。前兆方向か反応方向かを必ず確認してください。
- 注意点: 公開APIの取得範囲、欠測、報道量・投稿量バイアス、地震後反応の混入に注意。
- データ取得状況: status=ok

## 9. gbif:gbif_occurrences × 気象庁_地震月報_カタログ編:max_magnitude
- ラグ: 12H (external_precedes_target)
- モデル: correlation+ols+logistic_probe
- 効果量: correlation=-0.4606887512036605, coefficient=-0.000897085335179547
- p値/FDR: p=0.0196078431372549, q=0.04084967320261438
- 検証性能: AUC=None, rate_ratio=0.6203354725549312
- 解釈: 多重検定込みの探索的シグナル。前兆方向か反応方向かを必ず確認してください。
- 注意点: 公開APIの取得範囲、欠測、報道量・投稿量バイアス、地震後反応の混入に注意。
- データ取得状況: status=ok

## 10. gbif:gbif_occurrences × 気象庁_地震月報_カタログ編:max_magnitude
- ラグ: 3D (external_precedes_target)
- モデル: correlation+ols+logistic_probe
- 効果量: correlation=-0.4568350251737442, coefficient=-0.0008923302342626259
- p値/FDR: p=0.0196078431372549, q=0.04084967320261438
- 検証性能: AUC=None, rate_ratio=0.6274343777755621
- 解釈: 多重検定込みの探索的シグナル。前兆方向か反応方向かを必ず確認してください。
- 注意点: 公開APIの取得範囲、欠測、報道量・投稿量バイアス、地震後反応の混入に注意。
- データ取得状況: status=ok

# Failed or Skipped Sources

- {"external_source_id": "google_trends", "status": "skip", "error_message": "pytrends is unavailable or blocked: ModuleNotFoundError(\"No module named 'pytrends'\")"}
- {"status": "fetch_error", "dataset_id": "気象庁_地震月報_カタログ編", "year": 2024, "sample_http": {"url": "https://www.data.jma.go.jp/eqev/data/bulletin/data/hypo/h2024.zip", "final_url": "https://www.data.jma.go.jp/eqev/data/bulletin/data/hypo/h2024.zip", "status_code": 404, "content_type": "text/html", "text_head": "<!DOCTYPE html>\r\n<html lang=\"ja\">\r\n  <head>\r\n    <meta charset=\"utf-8\" />\r\n    <meta name=\"robots\" content=\"noindex\">\r\n    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\r\n    <link rel=\"icon\" href=\"/favicon.ico\" type=\"image/x-icon\">\r\n    <meta name=\"Author\" content=\"æ°è±¡åº Japan Meteorological Agency\"/>\r\n    <style type=\"text/css\">\r\n      body {background-color: #FFFFFF;}\r\n      \r\n      :host,html {\r\n          line-height: 1.5;\r\n          font-family: ui-sans-serif,system-ui,sans-serif,Apple Color Emoji,Segoe UI Emoji,Segoe UI Symbol,Noto Color Emoji;\r\n          font-feature-settings: normal;\r\n      }\r\n      \r\n      a { text-decoration-line: underline; }\r\n      a { color: black;}\r\n      \r\n      p {font-size: 20px; color: black;}\r\n      \r\n      .flex {display: flex; }\r\n      .items-center {align-items: center;}\r\n      .h-20 {height: 5rem;}\r\n      .px-6 {padding-left: 1.5rem;padding-right: 1.5rem;}\r\n      .px-10 {padding-left: 2.5rem;padding-right: 2.5rem;}\r\n      .pb-10 {padding-bottom: 2.5rem}\r\n      .text-std-32B-5,.text-std-45B-4 {letter-spacing: .02em;font-weight: 700;}\r\n      .mt-8 {margin-top: 2rem;}\r\n    </style>\r\n    <title>404ï½æ°è±¡åº</title>\r\n    <meta name=\"description\" content=\"æå®ããããã¼ã¸ãè¦ã¤ããã¾ãã\">\r\n  </head>\r\n  <body>\r\n    <header>\r\n      <div>\r\n        <h1><a href=\"https://www.jma.go.jp/\">æ°è±¡åº</a></h1>\r\n      </div>\r\n    </header>\r\n    <main>\r\n      <div class=\"px-10 pb-10\">\r\n        <h1 class=\"text-std-45B-4\">404 Not Found</h1>\r\n        <div class=\"lg:flex lg:gap-8\">\r\n          <h2 class=\"text-std-32B-5\">æå®ããããã¼ã¸ã¯å­å¨ãã¾ãã</h2>\r\n            <p class=\"mt-8\">\r\n              æå®ããããã¼ã¸ã¯ãåé¤ãããã¯ç§»åããå¯è½æ§ãããã¾ããã¢ãã¬ã¹ï¼URLï¼ããç¢ºèªã®ä¸ååº¦ã¢ã¯ã»ã¹ãããã\r\n              <a href=\"https://www.jma.go.jp/\">ããããã¼ã¸</a>ãããå©ç¨ãã ããã\r\n            </p>\r\n        </div>\r\n   ", "error": null}, "source_id": "excel_dataset"}
- {"status": "fetch_error", "query": "earthquake cloud", "attempt": 0, "sample_http": {"url": "https://api.gdeltproject.org/api/v2/doc/doc", "final_url": "https://api.gdeltproject.org/api/v2/doc/doc", "status_code": null, "content_type": null, "text_head": "", "error": "ConnectTimeout(MaxRetryError(\"HTTPSConnectionPool(host='api.gdeltproject.org', port=443): Max retries exceeded with url: /api/v2/doc/doc?query=earthquake+cloud&mode=timelinevol&format=json&startdatetime=20200101000000&enddatetime=20241231235959 (Caused by ConnectTimeoutError(<HTTPSConnection(host='api.gdeltproject.org', port=443) at 0x10d965310>, 'Connection to api.gdeltproject.org timed out. (connect timeout=5)'))\"))"}, "source_id": "gdelt"}
- {"external_source_id": "gdelt", "status": "skip", "error_message": "No GDELT rows fetched; API may have timed out or returned a new schema"}
- {"external_source_id": "glotec", "status": "skip", "error_message": "GloTEC products are typically NetCDF/space-weather grids; add a stable product URL and netCDF parser before automated fetch. Probe report records this as a planned adapter instead of guessing a raw endpoint."}
- {"external_source_id": "aist_well", "status": "skip", "error_message": "AIST groundwater/well data requires source-specific access checks; do not scrape until terms and download endpoints are confirmed."}
- {"external_source_id": "movebank", "status": "skip", "error_message": "Movebank generally requires account/API credentials or per-study permission; public-only unauthenticated endpoint was not configured."}
- {"external_source_id": "ebird", "status": "skip", "error_message": "eBird API requires EBIRD_API_KEY; Basic Dataset also requires request/approval."}
- {"external_source_id": "openaq", "status": "skip", "error_message": "OpenAQ v3 requires OPENAQ_API_KEY in .env or environment."}
- {"external_source_id": "firms", "status": "skip", "error_message": "NASA FIRMS area CSV API requires NASA_FIRMS_MAP_KEY."}