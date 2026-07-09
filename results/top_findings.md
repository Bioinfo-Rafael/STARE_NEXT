# Top Findings

探索結果は仮説生成用です。地震予測を断定するものではありません。正のラグは外部信号が先、負のラグは地震側が先の反応方向です。

## 1. wikimedia:pageviews_宏観異常現象 × 気象庁_最近の地震活動_速報値:max_magnitude
- ラグ: 3D (external_precedes_target)
- モデル: correlation+ols+logistic_probe
- 効果量: correlation=-0.9510173499085024, coefficient=-0.046382884869872076
- p値/FDR: p=0.0196078431372549, q=0.5912518853695324
- 検証性能: AUC=None, rate_ratio=0.7111111111753086
- 解釈: 多重検定込みの探索的シグナル。前兆方向か反応方向かを必ず確認してください。
- 注意点: 公開APIの取得範囲、欠測、報道量・投稿量バイアス、地震後反応の混入に注意。
- データ取得状況: status=ok

## 2. wikimedia:pageviews_地震 × 気象庁_最近の地震活動_速報値:energy
- ラグ: 1D (external_precedes_target)
- モデル: correlation+ols+logistic_probe
- 効果量: correlation=0.8706289351719358, coefficient=24378255.633409303
- p値/FDR: p=0.0392156862745098, q=0.5912518853695324
- 検証性能: AUC=None, rate_ratio=825.6853546515649
- 解釈: 多重検定込みの探索的シグナル。前兆方向か反応方向かを必ず確認してください。
- 注意点: 公開APIの取得範囲、欠測、報道量・投稿量バイアス、地震後反応の混入に注意。
- データ取得状況: status=ok

## 3. wikimedia:pageviews_防災 × 気象庁_最近の地震活動_速報値:m4_flag
- ラグ: 3D (external_precedes_target)
- モデル: correlation+ols+logistic_probe
- 効果量: correlation=-0.8790166598768162, coefficient=-2.4516692571250887
- p値/FDR: p=0.11764705882352941, q=0.6317485898468976
- 検証性能: AUC=0.0, rate_ratio=9.99999999e-10
- 解釈: 多重検定込みの探索的シグナル。前兆方向か反応方向かを必ず確認してください。
- 注意点: 公開APIの取得範囲、欠測、報道量・投稿量バイアス、地震後反応の混入に注意。
- データ取得状況: status=ok

## 4. wikimedia:pageviews_total × 気象庁_最近の地震活動_速報値:m4_flag
- ラグ: 3D (external_precedes_target)
- モデル: correlation+ols+logistic_probe
- 効果量: correlation=-0.8382081162256706, coefficient=-2.2612669726611707
- p値/FDR: p=0.058823529411764705, q=0.5912518853695324
- 検証性能: AUC=0.0, rate_ratio=1.3333333315555557e-09
- 解釈: 多重検定込みの探索的シグナル。前兆方向か反応方向かを必ず確認してください。
- 注意点: 公開APIの取得範囲、欠測、報道量・投稿量バイアス、地震後反応の混入に注意。
- データ取得状況: status=ok

## 5. wikimedia:pageviews_地震 × 気象庁_最近の地震活動_速報値:count
- ラグ: 1D (external_precedes_target)
- モデル: correlation+ols+logistic_probe
- 効果量: correlation=0.8254672133676271, coefficient=0.025456153931217515
- p値/FDR: p=0.058823529411764705, q=0.5912518853695324
- 検証性能: AUC=None, rate_ratio=2.333333333037037
- 解釈: 多重検定込みの探索的シグナル。前兆方向か反応方向かを必ず確認してください。
- 注意点: 公開APIの取得範囲、欠測、報道量・投稿量バイアス、地震後反応の混入に注意。
- データ取得状況: status=ok

## 6. wikimedia:pageviews_津波 × 気象庁_最近の地震活動_速報値:energy
- ラグ: -1D (target_precedes_external)
- モデル: correlation+ols+logistic_probe
- 効果量: correlation=-0.9062522753134401, coefficient=-78691496.48566146
- p値/FDR: p=0.0196078431372549, q=0.5912518853695324
- 検証性能: AUC=None, rate_ratio=0.004026280204133883
- 解釈: 多重検定込みの探索的シグナル。前兆方向か反応方向かを必ず確認してください。
- 注意点: 公開APIの取得範囲、欠測、報道量・投稿量バイアス、地震後反応の混入に注意。
- データ取得状況: status=ok

## 7. wikimedia:pageviews_津波 × 気象庁_最近の地震活動_速報値:energy
- ラグ: -12H (target_precedes_external)
- モデル: correlation+ols+logistic_probe
- 効果量: correlation=-0.9062522753134401, coefficient=-78691496.48566146
- p値/FDR: p=0.0392156862745098, q=0.5912518853695324
- 検証性能: AUC=None, rate_ratio=0.004026280204133883
- 解釈: 多重検定込みの探索的シグナル。前兆方向か反応方向かを必ず確認してください。
- 注意点: 公開APIの取得範囲、欠測、報道量・投稿量バイアス、地震後反応の混入に注意。
- データ取得状況: status=ok

## 8. wikimedia:pageviews_津波 × 気象庁_最近の地震活動_速報値:energy
- ラグ: -6H (target_precedes_external)
- モデル: correlation+ols+logistic_probe
- 効果量: correlation=-0.9062522753134401, coefficient=-78691496.48566146
- p値/FDR: p=0.0196078431372549, q=0.5912518853695324
- 検証性能: AUC=None, rate_ratio=0.004026280204133883
- 解釈: 多重検定込みの探索的シグナル。前兆方向か反応方向かを必ず確認してください。
- 注意点: 公開APIの取得範囲、欠測、報道量・投稿量バイアス、地震後反応の混入に注意。
- データ取得状況: status=ok

## 9. wikimedia:pageviews_津波 × 気象庁_最近の地震活動_速報値:energy
- ラグ: -1H (target_precedes_external)
- モデル: correlation+ols+logistic_probe
- 効果量: correlation=-0.9062522753134401, coefficient=-78691496.48566146
- p値/FDR: p=0.0196078431372549, q=0.5912518853695324
- 検証性能: AUC=None, rate_ratio=0.004026280204133883
- 解釈: 多重検定込みの探索的シグナル。前兆方向か反応方向かを必ず確認してください。
- 注意点: 公開APIの取得範囲、欠測、報道量・投稿量バイアス、地震後反応の混入に注意。
- データ取得状況: status=ok

## 10. wikimedia:pageviews_南海トラフ巨大地震 × 気象庁_最近の地震活動_速報値:count
- ラグ: 1H (external_precedes_target)
- モデル: correlation+ols+logistic_probe
- 効果量: correlation=0.8045199357375111, coefficient=0.04120922517968565
- p値/FDR: p=0.0196078431372549, q=0.5912518853695324
- 検証性能: AUC=None, rate_ratio=1.9736842103725762
- 解釈: 多重検定込みの探索的シグナル。前兆方向か反応方向かを必ず確認してください。
- 注意点: 公開APIの取得範囲、欠測、報道量・投稿量バイアス、地震後反応の混入に注意。
- データ取得状況: status=ok

# Failed or Skipped Sources

- {"status": "fetch_error", "article": "地震雲", "sample_http": {"url": "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/ja.wikipedia/all-access/all-agents/%E5%9C%B0%E9%9C%87%E9%9B%B2/daily/20260701/20260709", "final_url": "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/ja.wikipedia/all-access/all-agents/%E5%9C%B0%E9%9C%87%E9%9B%B2/daily/20260701/20260709", "status_code": 404, "content_type": "application/problem+json", "text_head": "{\"detail\":\"The date(s) you used are valid, but we either do not have data for those date(s), or the project you asked for is not loaded yet. Please check documentation for more information\",\"method\":\"get\",\"status\":404,\"title\":\"Not Found\",\"type\":\"about:blank\",\"uri\":\"/metrics/pageviews/per-article/ja.wikipedia/all-access/all-agents/%E5%9C%B0%E9%9C%87%E9%9B%B2/daily/20260701/20260709\"}", "error": null}, "source_id": "wikimedia"}
- {"status": "fetch_error", "query": "animal strange behavior", "sample_http": {"url": "https://api.gdeltproject.org/api/v2/doc/doc", "final_url": "https://api.gdeltproject.org/api/v2/doc/doc", "status_code": null, "content_type": null, "text_head": "", "error": "ReadTimeout(ReadTimeoutError(\"HTTPSConnectionPool(host='api.gdeltproject.org', port=443): Read timed out. (read timeout=45)\"))"}, "source_id": "gdelt"}
- {"status": "fetch_error", "query": "unusual animal behavior", "sample_http": {"url": "https://api.gdeltproject.org/api/v2/doc/doc", "final_url": "https://api.gdeltproject.org/api/v2/doc/doc?query=unusual+animal+behavior&mode=timelinevol&format=json&startdatetime=20260701000000&enddatetime=20260709235959", "status_code": 429, "content_type": null, "text_head": "Please limit requests to one every 5 seconds or contact kalev.leetaru5@gmail.com for larger queries. All high-traffic users should switch to our ngrams dataset: https://blog.gdeltproject.org/using-the-new-web-ngrams-dataset-to-find-relevant-coverage/. For trend analysis, please see our daily newsletter briefings: https://blog.gdeltproject.org/announcing-our-new-daily-todays-trends-on-capitol-hill-todays-media-trends-newsletter-briefings/.\n\n", "error": null}, "source_id": "gdelt"}
- {"status": "fetch_error", "query": "well water", "sample_http": {"url": "https://api.gdeltproject.org/api/v2/doc/doc", "final_url": "https://api.gdeltproject.org/api/v2/doc/doc?query=well+water&mode=timelinevol&format=json&startdatetime=20260701000000&enddatetime=20260709235959", "status_code": 429, "content_type": null, "text_head": "Please limit requests to one every 5 seconds or contact kalev.leetaru5@gmail.com for larger queries. All high-traffic users should switch to our ngrams dataset: https://blog.gdeltproject.org/using-the-new-web-ngrams-dataset-to-find-relevant-coverage/. For trend analysis, please see our daily newsletter briefings: https://blog.gdeltproject.org/announcing-our-new-daily-todays-trends-on-capitol-hill-todays-media-trends-newsletter-briefings/.\n\n", "error": null}, "source_id": "gdelt"}
- {"status": "fetch_error", "query": "radio interference", "sample_http": {"url": "https://api.gdeltproject.org/api/v2/doc/doc", "final_url": "https://api.gdeltproject.org/api/v2/doc/doc?query=radio+interference&mode=timelinevol&format=json&startdatetime=20260701000000&enddatetime=20260709235959", "status_code": 429, "content_type": null, "text_head": "Please limit requests to one every 5 seconds or contact kalev.leetaru5@gmail.com for larger queries. All high-traffic users should switch to our ngrams dataset: https://blog.gdeltproject.org/using-the-new-web-ngrams-dataset-to-find-relevant-coverage/. For trend analysis, please see our daily newsletter briefings: https://blog.gdeltproject.org/announcing-our-new-daily-todays-trends-on-capitol-hill-todays-media-trends-newsletter-briefings/.\n\n", "error": null}, "source_id": "gdelt"}
- {"status": "fetch_error", "query": "earthquake cloud", "sample_http": {"url": "https://api.gdeltproject.org/api/v2/doc/doc", "final_url": "https://api.gdeltproject.org/api/v2/doc/doc?query=earthquake+cloud&mode=timelinevol&format=json&startdatetime=20260701000000&enddatetime=20260709235959", "status_code": 429, "content_type": null, "text_head": "Please limit requests to one every 5 seconds or contact kalev.leetaru5@gmail.com for larger queries. All high-traffic users should switch to our ngrams dataset: https://blog.gdeltproject.org/using-the-new-web-ngrams-dataset-to-find-relevant-coverage/. For trend analysis, please see our daily newsletter briefings: https://blog.gdeltproject.org/announcing-our-new-daily-todays-trends-on-capitol-hill-todays-media-trends-newsletter-briefings/.\n\n", "error": null}, "source_id": "gdelt"}
- {"status": "fetch_error", "query": "animal strange behavior", "sample_http": {"url": "https://api.gdeltproject.org/api/v2/doc/doc", "final_url": "https://api.gdeltproject.org/api/v2/doc/doc?query=animal+strange+behavior&mode=timelinevol&format=json&startdatetime=20260701000000&enddatetime=20260709235959", "status_code": 429, "content_type": null, "text_head": "Please limit requests to one every 5 seconds or contact kalev.leetaru5@gmail.com for larger queries. All high-traffic users should switch to our ngrams dataset: https://blog.gdeltproject.org/using-the-new-web-ngrams-dataset-to-find-relevant-coverage/. For trend analysis, please see our daily newsletter briefings: https://blog.gdeltproject.org/announcing-our-new-daily-todays-trends-on-capitol-hill-todays-media-trends-newsletter-briefings/.\n\n", "error": null}, "source_id": "gdelt"}
- {"status": "fetch_error", "query": "unusual animal behavior", "sample_http": {"url": "https://api.gdeltproject.org/api/v2/doc/doc", "final_url": "https://api.gdeltproject.org/api/v2/doc/doc?query=unusual+animal+behavior&mode=timelinevol&format=json&startdatetime=20260701000000&enddatetime=20260709235959", "status_code": 429, "content_type": null, "text_head": "Please limit requests to one every 5 seconds or contact kalev.leetaru5@gmail.com for larger queries. All high-traffic users should switch to our ngrams dataset: https://blog.gdeltproject.org/using-the-new-web-ngrams-dataset-to-find-relevant-coverage/. For trend analysis, please see our daily newsletter briefings: https://blog.gdeltproject.org/announcing-our-new-daily-todays-trends-on-capitol-hill-todays-media-trends-newsletter-briefings/.\n\n", "error": null}, "source_id": "gdelt"}
- {"external_source_id": "gdelt", "status": "skip", "error_message": "No GDELT rows fetched; API may have timed out or returned a new schema"}
- {"status": "fetch_error", "article": "地震雲", "sample_http": {"url": "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/ja.wikipedia/all-access/all-agents/%E5%9C%B0%E9%9C%87%E9%9B%B2/daily/20260701/20260709", "final_url": "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/ja.wikipedia/all-access/all-agents/%E5%9C%B0%E9%9C%87%E9%9B%B2/daily/20260701/20260709", "status_code": 404, "content_type": "application/problem+json", "text_head": "{\"detail\":\"The date(s) you used are valid, but we either do not have data for those date(s), or the project you asked for is not loaded yet. Please check documentation for more information\",\"method\":\"get\",\"status\":404,\"title\":\"Not Found\",\"type\":\"about:blank\",\"uri\":\"/metrics/pageviews/per-article/ja.wikipedia/all-access/all-agents/%E5%9C%B0%E9%9C%87%E9%9B%B2/daily/20260701/20260709\"}", "error": null}, "source_id": "wikimedia"}