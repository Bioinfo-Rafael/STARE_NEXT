# Top Findings

探索結果は仮説生成用です。地震予測を断定するものではありません。正のラグは外部信号が先、負のラグは地震側が先の反応方向です。

# Raw Count Strong Signals

## 1. inaturalist:inaturalist_observations__raw_count × 気象庁_地震月報_カタログ編:count
- ラグ: -14D (target_precedes_external)
- 特徴量調整: raw_count
- 交絡調整: month,day_of_week,weekend_or_holiday,year_trend
- モデル: calendar_adjusted_correlation+ols+logistic_probe
- 効果量: correlation=-0.32696708518909046, coefficient=-0.27261469891970325
- p値/FDR: p=0.0196078431372549, q=0.09914077990746861
- 検証性能: AUC=None, rate_ratio=-1.2577833125475915
- Negative control: corr=0.2752994787020767, pass=True
- 解釈: 多重検定込みの探索的シグナル。前兆方向か反応方向かを必ず確認してください。
- 注意点: 季節性、曜日、休日、投稿量バイアス、地震後反応の混入に注意。
- データ取得状況: status=ok

## 2. wikimedia:pageviews_余震__raw_count × 気象庁_地震月報_カタログ編:energy
- ラグ: -1D (target_precedes_external)
- 特徴量調整: raw_count
- 交絡調整: month,day_of_week,weekend_or_holiday,year_trend
- モデル: calendar_adjusted_correlation+ols+logistic_probe
- 効果量: correlation=0.21325005496905383, coefficient=2743311.7597033787
- p値/FDR: p=0.0196078431372549, q=0.09914077990746861
- 検証性能: AUC=None, rate_ratio=-2.637450199203187
- Negative control: corr=0.0006787589194271026, pass=True
- 解釈: 多重検定込みの探索的シグナル。前兆方向か反応方向かを必ず確認してください。
- 注意点: 季節性、曜日、休日、投稿量バイアス、地震後反応の混入に注意。
- データ取得状況: status=ok

## 3. wikimedia:pageviews_地震雲__raw_count × 気象庁_地震月報_カタログ編:m4_flag
- ラグ: 14D (external_precedes_target)
- 特徴量調整: raw_count
- 交絡調整: month,day_of_week,weekend_or_holiday,year_trend
- モデル: calendar_adjusted_correlation+ols+logistic_probe
- 効果量: correlation=-0.06446268799172311, coefficient=-0.057506542412053406
- p値/FDR: p=0.0196078431372549, q=0.09914077990746861
- 検証性能: AUC=0.30153520501275555, rate_ratio=-2.057335522489638
- Negative control: corr=0.0794531994253604, pass=False
- 解釈: 多重検定込みの探索的シグナル。前兆方向か反応方向かを必ず確認してください。
- 注意点: 季節性、曜日、休日、投稿量バイアス、地震後反応の混入に注意。
- データ取得状況: status=ok

## 4. wikimedia:pageviews_耳鳴り__raw_count × 気象庁_地震月報_カタログ編:m5_flag
- ラグ: -7D (target_precedes_external)
- 特徴量調整: raw_count
- 交絡調整: month,day_of_week,weekend_or_holiday,year_trend
- モデル: calendar_adjusted_correlation+ols+logistic_probe
- 効果量: correlation=-0.10563836861413181, coefficient=-0.12515817724909992
- p値/FDR: p=0.0196078431372549, q=0.09914077990746861
- 検証性能: AUC=0.4198861980644469, rate_ratio=-1.2441429853209327
- Negative control: corr=0.10751522900534202, pass=False
- 解釈: 多重検定込みの探索的シグナル。前兆方向か反応方向かを必ず確認してください。
- 注意点: 季節性、曜日、休日、投稿量バイアス、地震後反応の混入に注意。
- データ取得状況: status=ok

## 5. inaturalist:inaturalist_observations__raw_count × 気象庁_地震月報_カタログ編:max_magnitude
- ラグ: 3D (external_precedes_target)
- 特徴量調整: raw_count
- 交絡調整: month,day_of_week,weekend_or_holiday,year_trend
- モデル: calendar_adjusted_correlation+ols+logistic_probe
- 効果量: correlation=-0.3061013643802362, coefficient=-0.0013682415717540725
- p値/FDR: p=0.0196078431372549, q=0.09914077990746861
- 検証性能: AUC=None, rate_ratio=-1.2714819370577926
- Negative control: corr=0.3309003568242445, pass=False
- 解釈: 多重検定込みの探索的シグナル。前兆方向か反応方向かを必ず確認してください。
- 注意点: 季節性、曜日、休日、投稿量バイアス、地震後反応の混入に注意。
- データ取得状況: status=ok

## 6. inaturalist:inaturalist_observations__raw_count × 気象庁_地震月報_カタログ編:count
- ラグ: -7D (target_precedes_external)
- 特徴量調整: raw_count
- 交絡調整: month,day_of_week,weekend_or_holiday,year_trend
- モデル: calendar_adjusted_correlation+ols+logistic_probe
- 効果量: correlation=-0.2988063161345955, coefficient=-0.24773162517561037
- p値/FDR: p=0.0196078431372549, q=0.09914077990746861
- 検証性能: AUC=None, rate_ratio=-1.277847309102032
- Negative control: corr=0.2632509035548715, pass=True
- 解釈: 多重検定込みの探索的シグナル。前兆方向か反応方向かを必ず確認してください。
- 注意点: 季節性、曜日、休日、投稿量バイアス、地震後反応の混入に注意。
- データ取得状況: status=ok

## 7. wikimedia:pageviews_宏観異常現象__raw_count × 気象庁_地震月報_カタログ編:energy
- ラグ: -1D (target_precedes_external)
- 特徴量調整: raw_count
- 交絡調整: month,day_of_week,weekend_or_holiday,year_trend
- モデル: calendar_adjusted_correlation+ols+logistic_probe
- 効果量: correlation=0.17239819753294722, coefficient=6563587.169588903
- p値/FDR: p=0.0392156862745098, q=0.16866961838498842
- 検証性能: AUC=None, rate_ratio=-2.2433392539964476
- Negative control: corr=0.014513094139263603, pass=True
- 解釈: 多重検定込みの探索的シグナル。前兆方向か反応方向かを必ず確認してください。
- 注意点: 季節性、曜日、休日、投稿量バイアス、地震後反応の混入に注意。
- データ取得状況: status=ok

## 8. wikimedia:pageviews_地震雲__raw_count × 気象庁_地震月報_カタログ編:m4_flag
- ラグ: -7D (target_precedes_external)
- 特徴量調整: raw_count
- 交絡調整: month,day_of_week,weekend_or_holiday,year_trend
- モデル: calendar_adjusted_correlation+ols+logistic_probe
- 効果量: correlation=-0.05506543322473773, coefficient=-0.04859974606215174
- p値/FDR: p=0.058823529411764705, q=0.23529411764705882
- 検証性能: AUC=0.30315072890240186, rate_ratio=-2.0132449704241866
- Negative control: corr=0.043418509309820115, pass=True
- 解釈: 多重検定込みの探索的シグナル。前兆方向か反応方向かを必ず確認してください。
- 注意点: 季節性、曜日、休日、投稿量バイアス、地震後反応の混入に注意。
- データ取得状況: status=ok

## 9. wikimedia:pageviews_地震雲__raw_count × 気象庁_地震月報_カタログ編:m5_flag
- ラグ: 1D (external_precedes_target)
- 特徴量調整: raw_count
- 交絡調整: month,day_of_week,weekend_or_holiday,year_trend
- モデル: calendar_adjusted_correlation+ols+logistic_probe
- 効果量: correlation=-0.020041417831980077, coefficient=-0.023586752127430485
- p値/FDR: p=0.3333333333333333, q=0.7237635705669482
- 検証性能: AUC=0.42091905760310155, rate_ratio=-1.9262819338897947
- Negative control: corr=0.0714940279642752, pass=False
- 解釈: 多重検定込みの探索的シグナル。前兆方向か反応方向かを必ず確認してください。
- 注意点: 季節性、曜日、休日、投稿量バイアス、地震後反応の混入に注意。
- データ取得状況: status=ok

## 10. inaturalist:inaturalist_observations__raw_count × 気象庁_地震月報_カタログ編:max_magnitude
- ラグ: -14D (target_precedes_external)
- 特徴量調整: raw_count
- 交絡調整: month,day_of_week,weekend_or_holiday,year_trend
- モデル: calendar_adjusted_correlation+ols+logistic_probe
- 効果量: correlation=-0.3009350391079465, coefficient=-0.0013269475795541247
- p値/FDR: p=0.0196078431372549, q=0.09914077990746861
- 検証性能: AUC=None, rate_ratio=-1.2577833067794382
- Negative control: corr=0.3212237685833662, pass=False
- 解釈: 多重検定込みの探索的シグナル。前兆方向か反応方向かを必ず確認してください。
- 注意点: 季節性、曜日、休日、投稿量バイアス、地震後反応の混入に注意。
- データ取得状況: status=ok

# Seasonal Adjusted Anomaly Strong Signals

## 1. inaturalist:inaturalist_observations__month_residual × 気象庁_地震月報_カタログ編:count
- ラグ: -14D (target_precedes_external)
- 特徴量調整: month_residual
- 交絡調整: month,day_of_week,weekend_or_holiday,year_trend
- モデル: calendar_adjusted_correlation+ols+logistic_probe
- 効果量: correlation=-0.34440569921173136, coefficient=-0.2873789794114833
- p値/FDR: p=0.0196078431372549, q=0.09914077990746861
- 検証性能: AUC=None, rate_ratio=-1.2577833125482467
- Negative control: corr=0.2820480355930595, pass=True
- 解釈: 多重検定込みの探索的シグナル。前兆方向か反応方向かを必ず確認してください。
- 注意点: 季節性、曜日、休日、投稿量バイアス、地震後反応の混入に注意。
- データ取得状況: status=ok

## 2. wikimedia:pageviews_余震__month_residual × 気象庁_地震月報_カタログ編:energy
- ラグ: -1D (target_precedes_external)
- 特徴量調整: month_residual
- 交絡調整: month,day_of_week,weekend_or_holiday,year_trend
- モデル: calendar_adjusted_correlation+ols+logistic_probe
- 効果量: correlation=0.21327927658158127, coefficient=2746105.517960486
- p値/FDR: p=0.0196078431372549, q=0.09914077990746861
- 検証性能: AUC=None, rate_ratio=-2.5803921568627453
- Negative control: corr=0.000699791399426825, pass=True
- 解釈: 多重検定込みの探索的シグナル。前兆方向か反応方向かを必ず確認してください。
- 注意点: 季節性、曜日、休日、投稿量バイアス、地震後反応の混入に注意。
- データ取得状況: status=ok

## 3. wikimedia:pageviews_地震雲__doy_anomaly × 気象庁_地震月報_カタログ編:m4_flag
- ラグ: 3D (external_precedes_target)
- 特徴量調整: doy_anomaly
- 交絡調整: month,day_of_week,weekend_or_holiday,year_trend
- モデル: calendar_adjusted_correlation+ols+logistic_probe
- 効果量: correlation=-0.07640442355552486, coefficient=-0.06822289470578666
- p値/FDR: p=0.0196078431372549, q=0.09914077990746861
- 検証性能: AUC=0.30587478697064213, rate_ratio=-1.3749999504043584
- Negative control: corr=0.07322877116453881, pass=True
- 解釈: 多重検定込みの探索的シグナル。前兆方向か反応方向かを必ず確認してください。
- 注意点: 季節性、曜日、休日、投稿量バイアス、地震後反応の混入に注意。
- データ取得状況: status=ok

## 4. wikimedia:pageviews_地震雲__doy_anomaly × 気象庁_地震月報_カタログ編:m5_flag
- ラグ: 3D (external_precedes_target)
- 特徴量調整: doy_anomaly
- 交絡調整: month,day_of_week,weekend_or_holiday,year_trend
- モデル: calendar_adjusted_correlation+ols+logistic_probe
- 効果量: correlation=-0.055140366554098035, coefficient=-0.06585551248037493
- p値/FDR: p=0.058823529411764705, q=0.23529411764705882
- 検証性能: AUC=0.42015975560897434, rate_ratio=-1.3749999199496667
- Negative control: corr=0.03900519023168501, pass=True
- 解釈: 多重検定込みの探索的シグナル。前兆方向か反応方向かを必ず確認してください。
- 注意点: 季節性、曜日、休日、投稿量バイアス、地震後反応の混入に注意。
- データ取得状況: status=ok

## 5. inaturalist:inaturalist_observations__doy_anomaly × 気象庁_地震月報_カタログ編:max_magnitude
- ラグ: -14D (target_precedes_external)
- 特徴量調整: doy_anomaly
- 交絡調整: month,day_of_week,weekend_or_holiday,year_trend
- モデル: calendar_adjusted_correlation+ols+logistic_probe
- 効果量: correlation=-0.32968862934946663, coefficient=-0.0015790105888272702
- p値/FDR: p=0.0196078431372549, q=0.09914077990746861
- 検証性能: AUC=None, rate_ratio=-1.2029161551069143
- Negative control: corr=0.34151291416082086, pass=False
- 解釈: 多重検定込みの探索的シグナル。前兆方向か反応方向かを必ず確認してください。
- 注意点: 季節性、曜日、休日、投稿量バイアス、地震後反応の混入に注意。
- データ取得状況: status=ok

## 6. inaturalist:inaturalist_observations__doy_anomaly × 気象庁_地震月報_カタログ編:count
- ラグ: -7D (target_precedes_external)
- 特徴量調整: doy_anomaly
- 交絡調整: month,day_of_week,weekend_or_holiday,year_trend
- モデル: calendar_adjusted_correlation+ols+logistic_probe
- 効果量: correlation=-0.3431149828120227, coefficient=-0.3104992763972257
- p値/FDR: p=0.0196078431372549, q=0.09914077990746861
- 検証性能: AUC=None, rate_ratio=-1.2033898304809596
- Negative control: corr=0.29750724013710456, pass=True
- 解釈: 多重検定込みの探索的シグナル。前兆方向か反応方向かを必ず確認してください。
- 注意点: 季節性、曜日、休日、投稿量バイアス、地震後反応の混入に注意。
- データ取得状況: status=ok

## 7. wikimedia:pageviews_余震__ma30_anomaly × 気象庁_地震月報_カタログ編:energy
- ラグ: -1D (target_precedes_external)
- 特徴量調整: ma30_anomaly
- 交絡調整: month,day_of_week,weekend_or_holiday,year_trend
- モデル: calendar_adjusted_correlation+ols+logistic_probe
- 効果量: correlation=0.1999135057375744, coefficient=2610119.447142849
- p値/FDR: p=0.0196078431372549, q=0.09914077990746861
- 検証性能: AUC=None, rate_ratio=-1.3530927835051547
- Negative control: corr=-0.0006674652525958336, pass=True
- 解釈: 多重検定込みの探索的シグナル。前兆方向か反応方向かを必ず確認してください。
- 注意点: 季節性、曜日、休日、投稿量バイアス、地震後反応の混入に注意。
- データ取得状況: status=ok

## 8. wikimedia:pageviews_地震雲__month_residual × 気象庁_地震月報_カタログ編:m4_flag
- ラグ: -1D (target_precedes_external)
- 特徴量調整: month_residual
- 交絡調整: month,day_of_week,weekend_or_holiday,year_trend
- モデル: calendar_adjusted_correlation+ols+logistic_probe
- 効果量: correlation=-0.055350820260851565, coefficient=-0.049027357691355515
- p値/FDR: p=0.0196078431372549, q=0.09914077990746861
- 検証性能: AUC=0.30921637573576816, rate_ratio=-1.8620689045024745
- Negative control: corr=0.06463886951045429, pass=False
- 解釈: 多重検定込みの探索的シグナル。前兆方向か反応方向かを必ず確認してください。
- 注意点: 季節性、曜日、休日、投稿量バイアス、地震後反応の混入に注意。
- データ取得状況: status=ok

## 9. wikimedia:pageviews_地震雲__month_residual × 気象庁_地震月報_カタログ編:m5_flag
- ラグ: 1D (external_precedes_target)
- 特徴量調整: month_residual
- 交絡調整: month,day_of_week,weekend_or_holiday,year_trend
- モデル: calendar_adjusted_correlation+ols+logistic_probe
- 効果量: correlation=-0.020269252611850676, coefficient=-0.023857097689407445
- p値/FDR: p=0.5490196078431373, q=0.8753191267649665
- 検証性能: AUC=0.4209662357268831, rate_ratio=-1.8938192278649597
- Negative control: corr=0.07188341045325598, pass=False
- 解釈: 多重検定込みの探索的シグナル。前兆方向か反応方向かを必ず確認してください。
- 注意点: 季節性、曜日、休日、投稿量バイアス、地震後反応の混入に注意。
- データ取得状況: status=ok

## 10. inaturalist:inaturalist_observations__doy_anomaly × 気象庁_地震月報_カタログ編:max_magnitude
- ラグ: 3D (external_precedes_target)
- 特徴量調整: doy_anomaly
- 交絡調整: month,day_of_week,weekend_or_holiday,year_trend
- モデル: calendar_adjusted_correlation+ols+logistic_probe
- 効果量: correlation=-0.3263868261349169, coefficient=-0.0015670215172915597
- p値/FDR: p=0.0196078431372549, q=0.09914077990746861
- 検証性能: AUC=None, rate_ratio=-1.2055622681056761
- Negative control: corr=0.36449979794372067, pass=False
- 解釈: 多重検定込みの探索的シグナル。前兆方向か反応方向かを必ず確認してください。
- 注意点: 季節性、曜日、休日、投稿量バイアス、地震後反応の混入に注意。
- データ取得状況: status=ok

# Signals Beating Negative Control

## 1. inaturalist:inaturalist_observations__month_residual × 気象庁_地震月報_カタログ編:count
- ラグ: -14D (target_precedes_external)
- 特徴量調整: month_residual
- 交絡調整: month,day_of_week,weekend_or_holiday,year_trend
- モデル: calendar_adjusted_correlation+ols+logistic_probe
- 効果量: correlation=-0.34440569921173136, coefficient=-0.2873789794114833
- p値/FDR: p=0.0196078431372549, q=0.09914077990746861
- 検証性能: AUC=None, rate_ratio=-1.2577833125482467
- Negative control: corr=0.2820480355930595, pass=True
- 解釈: 多重検定込みの探索的シグナル。前兆方向か反応方向かを必ず確認してください。
- 注意点: 季節性、曜日、休日、投稿量バイアス、地震後反応の混入に注意。
- データ取得状況: status=ok

## 2. wikimedia:pageviews_余震__month_residual × 気象庁_地震月報_カタログ編:energy
- ラグ: -1D (target_precedes_external)
- 特徴量調整: month_residual
- 交絡調整: month,day_of_week,weekend_or_holiday,year_trend
- モデル: calendar_adjusted_correlation+ols+logistic_probe
- 効果量: correlation=0.21327927658158127, coefficient=2746105.517960486
- p値/FDR: p=0.0196078431372549, q=0.09914077990746861
- 検証性能: AUC=None, rate_ratio=-2.5803921568627453
- Negative control: corr=0.000699791399426825, pass=True
- 解釈: 多重検定込みの探索的シグナル。前兆方向か反応方向かを必ず確認してください。
- 注意点: 季節性、曜日、休日、投稿量バイアス、地震後反応の混入に注意。
- データ取得状況: status=ok

## 3. wikimedia:pageviews_地震雲__raw_count × 気象庁_地震月報_カタログ編:m4_flag
- ラグ: -7D (target_precedes_external)
- 特徴量調整: raw_count
- 交絡調整: month,day_of_week,weekend_or_holiday,year_trend
- モデル: calendar_adjusted_correlation+ols+logistic_probe
- 効果量: correlation=-0.05506543322473773, coefficient=-0.04859974606215174
- p値/FDR: p=0.058823529411764705, q=0.23529411764705882
- 検証性能: AUC=0.30315072890240186, rate_ratio=-2.0132449704241866
- Negative control: corr=0.043418509309820115, pass=True
- 解釈: 多重検定込みの探索的シグナル。前兆方向か反応方向かを必ず確認してください。
- 注意点: 季節性、曜日、休日、投稿量バイアス、地震後反応の混入に注意。
- データ取得状況: status=ok

## 4. wikimedia:pageviews_地震雲__doy_anomaly × 気象庁_地震月報_カタログ編:m5_flag
- ラグ: 3D (external_precedes_target)
- 特徴量調整: doy_anomaly
- 交絡調整: month,day_of_week,weekend_or_holiday,year_trend
- モデル: calendar_adjusted_correlation+ols+logistic_probe
- 効果量: correlation=-0.055140366554098035, coefficient=-0.06585551248037493
- p値/FDR: p=0.058823529411764705, q=0.23529411764705882
- 検証性能: AUC=0.42015975560897434, rate_ratio=-1.3749999199496667
- Negative control: corr=0.03900519023168501, pass=True
- 解釈: 多重検定込みの探索的シグナル。前兆方向か反応方向かを必ず確認してください。
- 注意点: 季節性、曜日、休日、投稿量バイアス、地震後反応の混入に注意。
- データ取得状況: status=ok

## 5. kp_dst:kp_mean__doy_anomaly × 気象庁_地震月報_カタログ編:max_magnitude
- ラグ: 14D (external_precedes_target)
- 特徴量調整: doy_anomaly
- 交絡調整: month,day_of_week,weekend_or_holiday,year_trend
- モデル: calendar_adjusted_correlation+ols+logistic_probe
- 効果量: correlation=0.17682000398542388, coefficient=0.3347056644217084
- p値/FDR: p=0.0196078431372549, q=0.09914077990746861
- 検証性能: AUC=None, rate_ratio=-1.205596116109073
- Negative control: corr=-0.07976410992801235, pass=True
- 解釈: 多重検定込みの探索的シグナル。前兆方向か反応方向かを必ず確認してください。
- 注意点: 季節性、曜日、休日、投稿量バイアス、地震後反応の混入に注意。
- データ取得状況: status=ok

## 6. inaturalist:inaturalist_observations__doy_anomaly × 気象庁_地震月報_カタログ編:count
- ラグ: -7D (target_precedes_external)
- 特徴量調整: doy_anomaly
- 交絡調整: month,day_of_week,weekend_or_holiday,year_trend
- モデル: calendar_adjusted_correlation+ols+logistic_probe
- 効果量: correlation=-0.3431149828120227, coefficient=-0.3104992763972257
- p値/FDR: p=0.0196078431372549, q=0.09914077990746861
- 検証性能: AUC=None, rate_ratio=-1.2033898304809596
- Negative control: corr=0.29750724013710456, pass=True
- 解釈: 多重検定込みの探索的シグナル。前兆方向か反応方向かを必ず確認してください。
- 注意点: 季節性、曜日、休日、投稿量バイアス、地震後反応の混入に注意。
- データ取得状況: status=ok

## 7. wikimedia:pageviews_余震__raw_count × 気象庁_地震月報_カタログ編:energy
- ラグ: -1D (target_precedes_external)
- 特徴量調整: raw_count
- 交絡調整: month,day_of_week,weekend_or_holiday,year_trend
- モデル: calendar_adjusted_correlation+ols+logistic_probe
- 効果量: correlation=0.21325005496905383, coefficient=2743311.7597033787
- p値/FDR: p=0.0196078431372549, q=0.09914077990746861
- 検証性能: AUC=None, rate_ratio=-2.637450199203187
- Negative control: corr=0.0006787589194271026, pass=True
- 解釈: 多重検定込みの探索的シグナル。前兆方向か反応方向かを必ず確認してください。
- 注意点: 季節性、曜日、休日、投稿量バイアス、地震後反応の混入に注意。
- データ取得状況: status=ok

## 8. wikimedia:pageviews_地震雲__doy_anomaly × 気象庁_地震月報_カタログ編:m4_flag
- ラグ: 3D (external_precedes_target)
- 特徴量調整: doy_anomaly
- 交絡調整: month,day_of_week,weekend_or_holiday,year_trend
- モデル: calendar_adjusted_correlation+ols+logistic_probe
- 効果量: correlation=-0.07640442355552486, coefficient=-0.06822289470578666
- p値/FDR: p=0.0196078431372549, q=0.09914077990746861
- 検証性能: AUC=0.30587478697064213, rate_ratio=-1.3749999504043584
- Negative control: corr=0.07322877116453881, pass=True
- 解釈: 多重検定込みの探索的シグナル。前兆方向か反応方向かを必ず確認してください。
- 注意点: 季節性、曜日、休日、投稿量バイアス、地震後反応の混入に注意。
- データ取得状況: status=ok

## 9. wikimedia:pageviews_耳鳴り__doy_anomaly × 気象庁_地震月報_カタログ編:m5_flag
- ラグ: -14D (target_precedes_external)
- 特徴量調整: doy_anomaly
- 交絡調整: month,day_of_week,weekend_or_holiday,year_trend
- モデル: calendar_adjusted_correlation+ols+logistic_probe
- 効果量: correlation=-0.1162760590885084, coefficient=-0.13738845091779592
- p値/FDR: p=0.0196078431372549, q=0.09914077990746861
- 検証性能: AUC=0.42402393812432343, rate_ratio=-1.1583332797764334
- Negative control: corr=0.09667814428503868, pass=True
- 解釈: 多重検定込みの探索的シグナル。前兆方向か反応方向かを必ず確認してください。
- 注意点: 季節性、曜日、休日、投稿量バイアス、地震後反応の混入に注意。
- データ取得状況: status=ok

## 10. kp_dst:kp_mean__month_residual × 気象庁_地震月報_カタログ編:max_magnitude
- ラグ: 14D (external_precedes_target)
- 特徴量調整: month_residual
- 交絡調整: month,day_of_week,weekend_or_holiday,year_trend
- モデル: calendar_adjusted_correlation+ols+logistic_probe
- 効果量: correlation=0.15962734728959588, coefficient=0.27418494029853957
- p値/FDR: p=0.0196078431372549, q=0.09914077990746861
- 検証性能: AUC=None, rate_ratio=-1.3514915805571488
- Negative control: corr=-0.07869690298709063, pass=True
- 解釈: 多重検定込みの探索的シグナル。前兆方向か反応方向かを必ず確認してください。
- 注意点: 季節性、曜日、休日、投稿量バイアス、地震後反応の混入に注意。
- データ取得状況: status=ok

# Precursor Direction Only

## 1. inaturalist:inaturalist_observations__doy_anomaly × 気象庁_地震月報_カタログ編:count
- ラグ: 14D (external_precedes_target)
- 特徴量調整: doy_anomaly
- 交絡調整: month,day_of_week,weekend_or_holiday,year_trend
- モデル: calendar_adjusted_correlation+ols+logistic_probe
- 効果量: correlation=-0.31643322884900243, coefficient=-0.28587587415062143
- p値/FDR: p=0.0196078431372549, q=0.09914077990746861
- 検証性能: AUC=None, rate_ratio=-1.2109756097270041
- Negative control: corr=0.3271065560392698, pass=False
- 解釈: 多重検定込みの探索的シグナル。前兆方向か反応方向かを必ず確認してください。
- 注意点: 季節性、曜日、休日、投稿量バイアス、地震後反応の混入に注意。
- データ取得状況: status=ok

## 2. gbif:gbif_occurrences__ma30_anomaly × 気象庁_地震月報_カタログ編:energy
- ラグ: 1D (external_precedes_target)
- 特徴量調整: ma30_anomaly
- 交絡調整: month,day_of_week,weekend_or_holiday,year_trend
- モデル: calendar_adjusted_correlation+ols+logistic_probe
- 効果量: correlation=0.08494947413932082, coefficient=1088510.9513912254
- p値/FDR: p=0.0196078431372549, q=0.09914077990746861
- 検証性能: AUC=None, rate_ratio=-1.1061130334486735
- Negative control: corr=0.012160092180919164, pass=True
- 解釈: 多重検定込みの探索的シグナル。前兆方向か反応方向かを必ず確認してください。
- 注意点: 季節性、曜日、休日、投稿量バイアス、地震後反応の混入に注意。
- データ取得状況: status=ok

## 3. wikimedia:pageviews_地震雲__raw_count × 気象庁_地震月報_カタログ編:m4_flag
- ラグ: 14D (external_precedes_target)
- 特徴量調整: raw_count
- 交絡調整: month,day_of_week,weekend_or_holiday,year_trend
- モデル: calendar_adjusted_correlation+ols+logistic_probe
- 効果量: correlation=-0.06446268799172311, coefficient=-0.057506542412053406
- p値/FDR: p=0.0196078431372549, q=0.09914077990746861
- 検証性能: AUC=0.30153520501275555, rate_ratio=-2.057335522489638
- Negative control: corr=0.0794531994253604, pass=False
- 解釈: 多重検定込みの探索的シグナル。前兆方向か反応方向かを必ず確認してください。
- 注意点: 季節性、曜日、休日、投稿量バイアス、地震後反応の混入に注意。
- データ取得状況: status=ok

## 4. wikimedia:pageviews_地震雲__doy_anomaly × 気象庁_地震月報_カタログ編:m5_flag
- ラグ: 3D (external_precedes_target)
- 特徴量調整: doy_anomaly
- 交絡調整: month,day_of_week,weekend_or_holiday,year_trend
- モデル: calendar_adjusted_correlation+ols+logistic_probe
- 効果量: correlation=-0.055140366554098035, coefficient=-0.06585551248037493
- p値/FDR: p=0.058823529411764705, q=0.23529411764705882
- 検証性能: AUC=0.42015975560897434, rate_ratio=-1.3749999199496667
- Negative control: corr=0.03900519023168501, pass=True
- 解釈: 多重検定込みの探索的シグナル。前兆方向か反応方向かを必ず確認してください。
- 注意点: 季節性、曜日、休日、投稿量バイアス、地震後反応の混入に注意。
- データ取得状況: status=ok

## 5. inaturalist:inaturalist_observations__doy_anomaly × 気象庁_地震月報_カタログ編:max_magnitude
- ラグ: 3D (external_precedes_target)
- 特徴量調整: doy_anomaly
- 交絡調整: month,day_of_week,weekend_or_holiday,year_trend
- モデル: calendar_adjusted_correlation+ols+logistic_probe
- 効果量: correlation=-0.3263868261349169, coefficient=-0.0015670215172915597
- p値/FDR: p=0.0196078431372549, q=0.09914077990746861
- 検証性能: AUC=None, rate_ratio=-1.2055622681056761
- Negative control: corr=0.36449979794372067, pass=False
- 解釈: 多重検定込みの探索的シグナル。前兆方向か反応方向かを必ず確認してください。
- 注意点: 季節性、曜日、休日、投稿量バイアス、地震後反応の混入に注意。
- データ取得状況: status=ok

## 6. inaturalist:inaturalist_observations__doy_anomaly × 気象庁_地震月報_カタログ編:count
- ラグ: 3D (external_precedes_target)
- 特徴量調整: doy_anomaly
- 交絡調整: month,day_of_week,weekend_or_holiday,year_trend
- モデル: calendar_adjusted_correlation+ols+logistic_probe
- 効果量: correlation=-0.3128002823350736, coefficient=-0.2828049611166066
- p値/FDR: p=0.0196078431372549, q=0.09914077990746861
- 検証性能: AUC=None, rate_ratio=-1.2055622732485591
- Negative control: corr=0.3142136138062292, pass=False
- 解釈: 多重検定込みの探索的シグナル。前兆方向か反応方向かを必ず確認してください。
- 注意点: 季節性、曜日、休日、投稿量バイアス、地震後反応の混入に注意。
- データ取得状況: status=ok

## 7. gbif:gbif_occurrences__ma7_anomaly × 気象庁_地震月報_カタログ編:energy
- ラグ: 1D (external_precedes_target)
- 特徴量調整: ma7_anomaly
- 交絡調整: month,day_of_week,weekend_or_holiday,year_trend
- モデル: calendar_adjusted_correlation+ols+logistic_probe
- 効果量: correlation=0.06822960587539319, coefficient=951053.0923763736
- p値/FDR: p=0.0196078431372549, q=0.09914077990746861
- 検証性能: AUC=None, rate_ratio=-0.9783315276273024
- Negative control: corr=0.02242785740577772, pass=True
- 解釈: 多重検定込みの探索的シグナル。前兆方向か反応方向かを必ず確認してください。
- 注意点: 季節性、曜日、休日、投稿量バイアス、地震後反応の混入に注意。
- データ取得状況: status=ok

## 8. wikimedia:pageviews_地震雲__doy_anomaly × 気象庁_地震月報_カタログ編:m4_flag
- ラグ: 3D (external_precedes_target)
- 特徴量調整: doy_anomaly
- 交絡調整: month,day_of_week,weekend_or_holiday,year_trend
- モデル: calendar_adjusted_correlation+ols+logistic_probe
- 効果量: correlation=-0.07640442355552486, coefficient=-0.06822289470578666
- p値/FDR: p=0.0196078431372549, q=0.09914077990746861
- 検証性能: AUC=0.30587478697064213, rate_ratio=-1.3749999504043584
- Negative control: corr=0.07322877116453881, pass=True
- 解釈: 多重検定込みの探索的シグナル。前兆方向か反応方向かを必ず確認してください。
- 注意点: 季節性、曜日、休日、投稿量バイアス、地震後反応の混入に注意。
- データ取得状況: status=ok

## 9. wikimedia:pageviews_地震雲__raw_count × 気象庁_地震月報_カタログ編:m5_flag
- ラグ: 1D (external_precedes_target)
- 特徴量調整: raw_count
- 交絡調整: month,day_of_week,weekend_or_holiday,year_trend
- モデル: calendar_adjusted_correlation+ols+logistic_probe
- 効果量: correlation=-0.020041417831980077, coefficient=-0.023586752127430485
- p値/FDR: p=0.3333333333333333, q=0.7237635705669482
- 検証性能: AUC=0.42091905760310155, rate_ratio=-1.9262819338897947
- Negative control: corr=0.0714940279642752, pass=False
- 解釈: 多重検定込みの探索的シグナル。前兆方向か反応方向かを必ず確認してください。
- 注意点: 季節性、曜日、休日、投稿量バイアス、地震後反応の混入に注意。
- データ取得状況: status=ok

## 10. inaturalist:inaturalist_observations__doy_anomaly × 気象庁_地震月報_カタログ編:max_magnitude
- ラグ: 1D (external_precedes_target)
- 特徴量調整: doy_anomaly
- 交絡調整: month,day_of_week,weekend_or_holiday,year_trend
- モデル: calendar_adjusted_correlation+ols+logistic_probe
- 効果量: correlation=-0.32429799001198695, coefficient=-0.0015560640530045363
- p値/FDR: p=0.0196078431372549, q=0.09914077990746861
- 検証性能: AUC=None, rate_ratio=-1.2026537943012
- Negative control: corr=0.3534992007694905, pass=False
- 解釈: 多重検定込みの探索的シグナル。前兆方向か反応方向かを必ず確認してください。
- 注意点: 季節性、曜日、休日、投稿量バイアス、地震後反応の混入に注意。
- データ取得状況: status=ok

# Post-Earthquake Reaction Stronger

## 1. inaturalist:inaturalist_observations__month_residual × 気象庁_地震月報_カタログ編:count
- ラグ: -14D (target_precedes_external)
- 特徴量調整: month_residual
- 交絡調整: month,day_of_week,weekend_or_holiday,year_trend
- モデル: calendar_adjusted_correlation+ols+logistic_probe
- 効果量: correlation=-0.34440569921173136, coefficient=-0.2873789794114833
- p値/FDR: p=0.0196078431372549, q=0.09914077990746861
- 検証性能: AUC=None, rate_ratio=-1.2577833125482467
- Negative control: corr=0.2820480355930595, pass=True
- 解釈: 多重検定込みの探索的シグナル。前兆方向か反応方向かを必ず確認してください。
- 注意点: 季節性、曜日、休日、投稿量バイアス、地震後反応の混入に注意。
- データ取得状況: status=ok

## 2. wikimedia:pageviews_余震__month_residual × 気象庁_地震月報_カタログ編:energy
- ラグ: -1D (target_precedes_external)
- 特徴量調整: month_residual
- 交絡調整: month,day_of_week,weekend_or_holiday,year_trend
- モデル: calendar_adjusted_correlation+ols+logistic_probe
- 効果量: correlation=0.21327927658158127, coefficient=2746105.517960486
- p値/FDR: p=0.0196078431372549, q=0.09914077990746861
- 検証性能: AUC=None, rate_ratio=-2.5803921568627453
- Negative control: corr=0.000699791399426825, pass=True
- 解釈: 多重検定込みの探索的シグナル。前兆方向か反応方向かを必ず確認してください。
- 注意点: 季節性、曜日、休日、投稿量バイアス、地震後反応の混入に注意。
- データ取得状況: status=ok

## 3. wikimedia:pageviews_地震雲__raw_count × 気象庁_地震月報_カタログ編:m4_flag
- ラグ: -7D (target_precedes_external)
- 特徴量調整: raw_count
- 交絡調整: month,day_of_week,weekend_or_holiday,year_trend
- モデル: calendar_adjusted_correlation+ols+logistic_probe
- 効果量: correlation=-0.05506543322473773, coefficient=-0.04859974606215174
- p値/FDR: p=0.058823529411764705, q=0.23529411764705882
- 検証性能: AUC=0.30315072890240186, rate_ratio=-2.0132449704241866
- Negative control: corr=0.043418509309820115, pass=True
- 解釈: 多重検定込みの探索的シグナル。前兆方向か反応方向かを必ず確認してください。
- 注意点: 季節性、曜日、休日、投稿量バイアス、地震後反応の混入に注意。
- データ取得状況: status=ok

## 4. wikimedia:pageviews_耳鳴り__raw_count × 気象庁_地震月報_カタログ編:m5_flag
- ラグ: -7D (target_precedes_external)
- 特徴量調整: raw_count
- 交絡調整: month,day_of_week,weekend_or_holiday,year_trend
- モデル: calendar_adjusted_correlation+ols+logistic_probe
- 効果量: correlation=-0.10563836861413181, coefficient=-0.12515817724909992
- p値/FDR: p=0.0196078431372549, q=0.09914077990746861
- 検証性能: AUC=0.4198861980644469, rate_ratio=-1.2441429853209327
- Negative control: corr=0.10751522900534202, pass=False
- 解釈: 多重検定込みの探索的シグナル。前兆方向か反応方向かを必ず確認してください。
- 注意点: 季節性、曜日、休日、投稿量バイアス、地震後反応の混入に注意。
- データ取得状況: status=ok

## 5. inaturalist:inaturalist_observations__doy_anomaly × 気象庁_地震月報_カタログ編:max_magnitude
- ラグ: -14D (target_precedes_external)
- 特徴量調整: doy_anomaly
- 交絡調整: month,day_of_week,weekend_or_holiday,year_trend
- モデル: calendar_adjusted_correlation+ols+logistic_probe
- 効果量: correlation=-0.32968862934946663, coefficient=-0.0015790105888272702
- p値/FDR: p=0.0196078431372549, q=0.09914077990746861
- 検証性能: AUC=None, rate_ratio=-1.2029161551069143
- Negative control: corr=0.34151291416082086, pass=False
- 解釈: 多重検定込みの探索的シグナル。前兆方向か反応方向かを必ず確認してください。
- 注意点: 季節性、曜日、休日、投稿量バイアス、地震後反応の混入に注意。
- データ取得状況: status=ok

## 6. inaturalist:inaturalist_observations__doy_anomaly × 気象庁_地震月報_カタログ編:count
- ラグ: -7D (target_precedes_external)
- 特徴量調整: doy_anomaly
- 交絡調整: month,day_of_week,weekend_or_holiday,year_trend
- モデル: calendar_adjusted_correlation+ols+logistic_probe
- 効果量: correlation=-0.3431149828120227, coefficient=-0.3104992763972257
- p値/FDR: p=0.0196078431372549, q=0.09914077990746861
- 検証性能: AUC=None, rate_ratio=-1.2033898304809596
- Negative control: corr=0.29750724013710456, pass=True
- 解釈: 多重検定込みの探索的シグナル。前兆方向か反応方向かを必ず確認してください。
- 注意点: 季節性、曜日、休日、投稿量バイアス、地震後反応の混入に注意。
- データ取得状況: status=ok

## 7. wikimedia:pageviews_余震__raw_count × 気象庁_地震月報_カタログ編:energy
- ラグ: -1D (target_precedes_external)
- 特徴量調整: raw_count
- 交絡調整: month,day_of_week,weekend_or_holiday,year_trend
- モデル: calendar_adjusted_correlation+ols+logistic_probe
- 効果量: correlation=0.21325005496905383, coefficient=2743311.7597033787
- p値/FDR: p=0.0196078431372549, q=0.09914077990746861
- 検証性能: AUC=None, rate_ratio=-2.637450199203187
- Negative control: corr=0.0006787589194271026, pass=True
- 解釈: 多重検定込みの探索的シグナル。前兆方向か反応方向かを必ず確認してください。
- 注意点: 季節性、曜日、休日、投稿量バイアス、地震後反応の混入に注意。
- データ取得状況: status=ok

## 8. wikimedia:pageviews_地震雲__raw_count × 気象庁_地震月報_カタログ編:m4_flag
- ラグ: -1D (target_precedes_external)
- 特徴量調整: raw_count
- 交絡調整: month,day_of_week,weekend_or_holiday,year_trend
- モデル: calendar_adjusted_correlation+ols+logistic_probe
- 効果量: correlation=-0.05587627953238396, coefficient=-0.049491067938340835
- p値/FDR: p=0.0196078431372549, q=0.09914077990746861
- 検証性能: AUC=0.3059927424035603, rate_ratio=-1.9309790728689609
- Negative control: corr=0.06355818026138035, pass=False
- 解釈: 多重検定込みの探索的シグナル。前兆方向か反応方向かを必ず確認してください。
- 注意点: 季節性、曜日、休日、投稿量バイアス、地震後反応の混入に注意。
- データ取得状況: status=ok

## 9. wikimedia:pageviews_耳鳴り__month_residual × 気象庁_地震月報_カタログ編:m5_flag
- ラグ: -7D (target_precedes_external)
- 特徴量調整: month_residual
- 交絡調整: month,day_of_week,weekend_or_holiday,year_trend
- モデル: calendar_adjusted_correlation+ols+logistic_probe
- 効果量: correlation=-0.10491623599173233, coefficient=-0.12424220188889058
- p値/FDR: p=0.0196078431372549, q=0.09914077990746861
- 検証性能: AUC=0.42169598625787946, rate_ratio=-1.2524751990625784
- Negative control: corr=0.10896805064109472, pass=False
- 解釈: 多重検定込みの探索的シグナル。前兆方向か反応方向かを必ず確認してください。
- 注意点: 季節性、曜日、休日、投稿量バイアス、地震後反応の混入に注意。
- データ取得状況: status=ok

## 10. inaturalist:inaturalist_observations__doy_anomaly × 気象庁_地震月報_カタログ編:max_magnitude
- ラグ: -3D (target_precedes_external)
- 特徴量調整: doy_anomaly
- 交絡調整: month,day_of_week,weekend_or_holiday,year_trend
- モデル: calendar_adjusted_correlation+ols+logistic_probe
- 効果量: correlation=-0.32265875884890693, coefficient=-0.0015496243532606686
- p値/FDR: p=0.0196078431372549, q=0.09914077990746861
- 検証性能: AUC=None, rate_ratio=-1.1949458431131026
- Negative control: corr=0.3544519584621152, pass=False
- 解釈: 多重検定込みの探索的シグナル。前兆方向か反応方向かを必ず確認してください。
- 注意点: 季節性、曜日、休日、投稿量バイアス、地震後反応の混入に注意。
- データ取得状況: status=ok

# Non-Max-Magnitude Ranking

## 1. inaturalist:inaturalist_observations__month_residual × 気象庁_地震月報_カタログ編:count
- ラグ: -14D (target_precedes_external)
- 特徴量調整: month_residual
- 交絡調整: month,day_of_week,weekend_or_holiday,year_trend
- モデル: calendar_adjusted_correlation+ols+logistic_probe
- 効果量: correlation=-0.34440569921173136, coefficient=-0.2873789794114833
- p値/FDR: p=0.0196078431372549, q=0.09914077990746861
- 検証性能: AUC=None, rate_ratio=-1.2577833125482467
- Negative control: corr=0.2820480355930595, pass=True
- 解釈: 多重検定込みの探索的シグナル。前兆方向か反応方向かを必ず確認してください。
- 注意点: 季節性、曜日、休日、投稿量バイアス、地震後反応の混入に注意。
- データ取得状況: status=ok

## 2. wikimedia:pageviews_余震__month_residual × 気象庁_地震月報_カタログ編:energy
- ラグ: -1D (target_precedes_external)
- 特徴量調整: month_residual
- 交絡調整: month,day_of_week,weekend_or_holiday,year_trend
- モデル: calendar_adjusted_correlation+ols+logistic_probe
- 効果量: correlation=0.21327927658158127, coefficient=2746105.517960486
- p値/FDR: p=0.0196078431372549, q=0.09914077990746861
- 検証性能: AUC=None, rate_ratio=-2.5803921568627453
- Negative control: corr=0.000699791399426825, pass=True
- 解釈: 多重検定込みの探索的シグナル。前兆方向か反応方向かを必ず確認してください。
- 注意点: 季節性、曜日、休日、投稿量バイアス、地震後反応の混入に注意。
- データ取得状況: status=ok

## 3. wikimedia:pageviews_地震雲__raw_count × 気象庁_地震月報_カタログ編:m4_flag
- ラグ: 14D (external_precedes_target)
- 特徴量調整: raw_count
- 交絡調整: month,day_of_week,weekend_or_holiday,year_trend
- モデル: calendar_adjusted_correlation+ols+logistic_probe
- 効果量: correlation=-0.06446268799172311, coefficient=-0.057506542412053406
- p値/FDR: p=0.0196078431372549, q=0.09914077990746861
- 検証性能: AUC=0.30153520501275555, rate_ratio=-2.057335522489638
- Negative control: corr=0.0794531994253604, pass=False
- 解釈: 多重検定込みの探索的シグナル。前兆方向か反応方向かを必ず確認してください。
- 注意点: 季節性、曜日、休日、投稿量バイアス、地震後反応の混入に注意。
- データ取得状況: status=ok

## 4. wikimedia:pageviews_耳鳴り__raw_count × 気象庁_地震月報_カタログ編:m5_flag
- ラグ: -7D (target_precedes_external)
- 特徴量調整: raw_count
- 交絡調整: month,day_of_week,weekend_or_holiday,year_trend
- モデル: calendar_adjusted_correlation+ols+logistic_probe
- 効果量: correlation=-0.10563836861413181, coefficient=-0.12515817724909992
- p値/FDR: p=0.0196078431372549, q=0.09914077990746861
- 検証性能: AUC=0.4198861980644469, rate_ratio=-1.2441429853209327
- Negative control: corr=0.10751522900534202, pass=False
- 解釈: 多重検定込みの探索的シグナル。前兆方向か反応方向かを必ず確認してください。
- 注意点: 季節性、曜日、休日、投稿量バイアス、地震後反応の混入に注意。
- データ取得状況: status=ok

## 5. inaturalist:inaturalist_observations__doy_anomaly × 気象庁_地震月報_カタログ編:count
- ラグ: -7D (target_precedes_external)
- 特徴量調整: doy_anomaly
- 交絡調整: month,day_of_week,weekend_or_holiday,year_trend
- モデル: calendar_adjusted_correlation+ols+logistic_probe
- 効果量: correlation=-0.3431149828120227, coefficient=-0.3104992763972257
- p値/FDR: p=0.0196078431372549, q=0.09914077990746861
- 検証性能: AUC=None, rate_ratio=-1.2033898304809596
- Negative control: corr=0.29750724013710456, pass=True
- 解釈: 多重検定込みの探索的シグナル。前兆方向か反応方向かを必ず確認してください。
- 注意点: 季節性、曜日、休日、投稿量バイアス、地震後反応の混入に注意。
- データ取得状況: status=ok

## 6. wikimedia:pageviews_余震__raw_count × 気象庁_地震月報_カタログ編:energy
- ラグ: -1D (target_precedes_external)
- 特徴量調整: raw_count
- 交絡調整: month,day_of_week,weekend_or_holiday,year_trend
- モデル: calendar_adjusted_correlation+ols+logistic_probe
- 効果量: correlation=0.21325005496905383, coefficient=2743311.7597033787
- p値/FDR: p=0.0196078431372549, q=0.09914077990746861
- 検証性能: AUC=None, rate_ratio=-2.637450199203187
- Negative control: corr=0.0006787589194271026, pass=True
- 解釈: 多重検定込みの探索的シグナル。前兆方向か反応方向かを必ず確認してください。
- 注意点: 季節性、曜日、休日、投稿量バイアス、地震後反応の混入に注意。
- データ取得状況: status=ok

## 7. wikimedia:pageviews_地震雲__raw_count × 気象庁_地震月報_カタログ編:m4_flag
- ラグ: -7D (target_precedes_external)
- 特徴量調整: raw_count
- 交絡調整: month,day_of_week,weekend_or_holiday,year_trend
- モデル: calendar_adjusted_correlation+ols+logistic_probe
- 効果量: correlation=-0.05506543322473773, coefficient=-0.04859974606215174
- p値/FDR: p=0.058823529411764705, q=0.23529411764705882
- 検証性能: AUC=0.30315072890240186, rate_ratio=-2.0132449704241866
- Negative control: corr=0.043418509309820115, pass=True
- 解釈: 多重検定込みの探索的シグナル。前兆方向か反応方向かを必ず確認してください。
- 注意点: 季節性、曜日、休日、投稿量バイアス、地震後反応の混入に注意。
- データ取得状況: status=ok

## 8. wikimedia:pageviews_地震雲__doy_anomaly × 気象庁_地震月報_カタログ編:m5_flag
- ラグ: 3D (external_precedes_target)
- 特徴量調整: doy_anomaly
- 交絡調整: month,day_of_week,weekend_or_holiday,year_trend
- モデル: calendar_adjusted_correlation+ols+logistic_probe
- 効果量: correlation=-0.055140366554098035, coefficient=-0.06585551248037493
- p値/FDR: p=0.058823529411764705, q=0.23529411764705882
- 検証性能: AUC=0.42015975560897434, rate_ratio=-1.3749999199496667
- Negative control: corr=0.03900519023168501, pass=True
- 解釈: 多重検定込みの探索的シグナル。前兆方向か反応方向かを必ず確認してください。
- 注意点: 季節性、曜日、休日、投稿量バイアス、地震後反応の混入に注意。
- データ取得状況: status=ok

## 9. inaturalist:inaturalist_observations__doy_anomaly × 気象庁_地震月報_カタログ編:count
- ラグ: -14D (target_precedes_external)
- 特徴量調整: doy_anomaly
- 交絡調整: month,day_of_week,weekend_or_holiday,year_trend
- モデル: calendar_adjusted_correlation+ols+logistic_probe
- 効果量: correlation=-0.33749985809908, coefficient=-0.3056461231903623
- p値/FDR: p=0.0196078431372549, q=0.09914077990746861
- 検証性能: AUC=None, rate_ratio=-1.2029161603611016
- Negative control: corr=0.30788439947607876, pass=True
- 解釈: 多重検定込みの探索的シグナル。前兆方向か反応方向かを必ず確認してください。
- 注意点: 季節性、曜日、休日、投稿量バイアス、地震後反応の混入に注意。
- データ取得状況: status=ok

## 10. wikimedia:pageviews_余震__ma30_anomaly × 気象庁_地震月報_カタログ編:energy
- ラグ: -1D (target_precedes_external)
- 特徴量調整: ma30_anomaly
- 交絡調整: month,day_of_week,weekend_or_holiday,year_trend
- モデル: calendar_adjusted_correlation+ols+logistic_probe
- 効果量: correlation=0.1999135057375744, coefficient=2610119.447142849
- p値/FDR: p=0.0196078431372549, q=0.09914077990746861
- 検証性能: AUC=None, rate_ratio=-1.3530927835051547
- Negative control: corr=-0.0006674652525958336, pass=True
- 解釈: 多重検定込みの探索的シグナル。前兆方向か反応方向かを必ず確認してください。
- 注意点: 季節性、曜日、休日、投稿量バイアス、地震後反応の混入に注意。
- データ取得状況: status=ok

# Wikimedia M4/M5 AUC: 防災・耳鳴り・地震雲・南海トラフ巨大地震

## 1. wikimedia:pageviews_地震雲__raw_count × 気象庁_地震月報_カタログ編:m4_flag
- ラグ: 14D (external_precedes_target)
- 特徴量調整: raw_count
- 交絡調整: month,day_of_week,weekend_or_holiday,year_trend
- モデル: calendar_adjusted_correlation+ols+logistic_probe
- 効果量: correlation=-0.06446268799172311, coefficient=-0.057506542412053406
- p値/FDR: p=0.0196078431372549, q=0.09914077990746861
- 検証性能: AUC=0.30153520501275555, rate_ratio=-2.057335522489638
- Negative control: corr=0.0794531994253604, pass=False
- 解釈: 多重検定込みの探索的シグナル。前兆方向か反応方向かを必ず確認してください。
- 注意点: 季節性、曜日、休日、投稿量バイアス、地震後反応の混入に注意。
- データ取得状況: status=ok

## 2. wikimedia:pageviews_耳鳴り__raw_count × 気象庁_地震月報_カタログ編:m5_flag
- ラグ: -7D (target_precedes_external)
- 特徴量調整: raw_count
- 交絡調整: month,day_of_week,weekend_or_holiday,year_trend
- モデル: calendar_adjusted_correlation+ols+logistic_probe
- 効果量: correlation=-0.10563836861413181, coefficient=-0.12515817724909992
- p値/FDR: p=0.0196078431372549, q=0.09914077990746861
- 検証性能: AUC=0.4198861980644469, rate_ratio=-1.2441429853209327
- Negative control: corr=0.10751522900534202, pass=False
- 解釈: 多重検定込みの探索的シグナル。前兆方向か反応方向かを必ず確認してください。
- 注意点: 季節性、曜日、休日、投稿量バイアス、地震後反応の混入に注意。
- データ取得状況: status=ok

## 3. wikimedia:pageviews_地震雲__raw_count × 気象庁_地震月報_カタログ編:m4_flag
- ラグ: -7D (target_precedes_external)
- 特徴量調整: raw_count
- 交絡調整: month,day_of_week,weekend_or_holiday,year_trend
- モデル: calendar_adjusted_correlation+ols+logistic_probe
- 効果量: correlation=-0.05506543322473773, coefficient=-0.04859974606215174
- p値/FDR: p=0.058823529411764705, q=0.23529411764705882
- 検証性能: AUC=0.30315072890240186, rate_ratio=-2.0132449704241866
- Negative control: corr=0.043418509309820115, pass=True
- 解釈: 多重検定込みの探索的シグナル。前兆方向か反応方向かを必ず確認してください。
- 注意点: 季節性、曜日、休日、投稿量バイアス、地震後反応の混入に注意。
- データ取得状況: status=ok

## 4. wikimedia:pageviews_地震雲__doy_anomaly × 気象庁_地震月報_カタログ編:m5_flag
- ラグ: 3D (external_precedes_target)
- 特徴量調整: doy_anomaly
- 交絡調整: month,day_of_week,weekend_or_holiday,year_trend
- モデル: calendar_adjusted_correlation+ols+logistic_probe
- 効果量: correlation=-0.055140366554098035, coefficient=-0.06585551248037493
- p値/FDR: p=0.058823529411764705, q=0.23529411764705882
- 検証性能: AUC=0.42015975560897434, rate_ratio=-1.3749999199496667
- Negative control: corr=0.03900519023168501, pass=True
- 解釈: 多重検定込みの探索的シグナル。前兆方向か反応方向かを必ず確認してください。
- 注意点: 季節性、曜日、休日、投稿量バイアス、地震後反応の混入に注意。
- データ取得状況: status=ok

## 5. wikimedia:pageviews_地震雲__doy_anomaly × 気象庁_地震月報_カタログ編:m4_flag
- ラグ: 3D (external_precedes_target)
- 特徴量調整: doy_anomaly
- 交絡調整: month,day_of_week,weekend_or_holiday,year_trend
- モデル: calendar_adjusted_correlation+ols+logistic_probe
- 効果量: correlation=-0.07640442355552486, coefficient=-0.06822289470578666
- p値/FDR: p=0.0196078431372549, q=0.09914077990746861
- 検証性能: AUC=0.30587478697064213, rate_ratio=-1.3749999504043584
- Negative control: corr=0.07322877116453881, pass=True
- 解釈: 多重検定込みの探索的シグナル。前兆方向か反応方向かを必ず確認してください。
- 注意点: 季節性、曜日、休日、投稿量バイアス、地震後反応の混入に注意。
- データ取得状況: status=ok

## 6. wikimedia:pageviews_地震雲__raw_count × 気象庁_地震月報_カタログ編:m5_flag
- ラグ: 1D (external_precedes_target)
- 特徴量調整: raw_count
- 交絡調整: month,day_of_week,weekend_or_holiday,year_trend
- モデル: calendar_adjusted_correlation+ols+logistic_probe
- 効果量: correlation=-0.020041417831980077, coefficient=-0.023586752127430485
- p値/FDR: p=0.3333333333333333, q=0.7237635705669482
- 検証性能: AUC=0.42091905760310155, rate_ratio=-1.9262819338897947
- Negative control: corr=0.0714940279642752, pass=False
- 解釈: 多重検定込みの探索的シグナル。前兆方向か反応方向かを必ず確認してください。
- 注意点: 季節性、曜日、休日、投稿量バイアス、地震後反応の混入に注意。
- データ取得状況: status=ok

## 7. wikimedia:pageviews_地震雲__raw_count × 気象庁_地震月報_カタログ編:m4_flag
- ラグ: -1D (target_precedes_external)
- 特徴量調整: raw_count
- 交絡調整: month,day_of_week,weekend_or_holiday,year_trend
- モデル: calendar_adjusted_correlation+ols+logistic_probe
- 効果量: correlation=-0.05587627953238396, coefficient=-0.049491067938340835
- p値/FDR: p=0.0196078431372549, q=0.09914077990746861
- 検証性能: AUC=0.3059927424035603, rate_ratio=-1.9309790728689609
- Negative control: corr=0.06355818026138035, pass=False
- 解釈: 多重検定込みの探索的シグナル。前兆方向か反応方向かを必ず確認してください。
- 注意点: 季節性、曜日、休日、投稿量バイアス、地震後反応の混入に注意。
- データ取得状況: status=ok

## 8. wikimedia:pageviews_地震雲__month_residual × 気象庁_地震月報_カタログ編:m5_flag
- ラグ: 1D (external_precedes_target)
- 特徴量調整: month_residual
- 交絡調整: month,day_of_week,weekend_or_holiday,year_trend
- モデル: calendar_adjusted_correlation+ols+logistic_probe
- 効果量: correlation=-0.020269252611850676, coefficient=-0.023857097689407445
- p値/FDR: p=0.5490196078431373, q=0.8753191267649665
- 検証性能: AUC=0.4209662357268831, rate_ratio=-1.8938192278649597
- Negative control: corr=0.07188341045325598, pass=False
- 解釈: 多重検定込みの探索的シグナル。前兆方向か反応方向かを必ず確認してください。
- 注意点: 季節性、曜日、休日、投稿量バイアス、地震後反応の混入に注意。
- データ取得状況: status=ok

## 9. wikimedia:pageviews_地震雲__raw_count × 気象庁_地震月報_カタログ編:m4_flag
- ラグ: -3D (target_precedes_external)
- 特徴量調整: raw_count
- 交絡調整: month,day_of_week,weekend_or_holiday,year_trend
- モデル: calendar_adjusted_correlation+ols+logistic_probe
- 効果量: correlation=-0.05232098628646676, coefficient=-0.046173780674648654
- p値/FDR: p=0.0392156862745098, q=0.16866961838498842
- 検証性能: AUC=0.30770497865873847, rate_ratio=-1.975530118739572
- Negative control: corr=0.05086232573975705, pass=True
- 解釈: 多重検定込みの探索的シグナル。前兆方向か反応方向かを必ず確認してください。
- 注意点: 季節性、曜日、休日、投稿量バイアス、地震後反応の混入に注意。
- データ取得状況: status=ok

## 10. wikimedia:pageviews_耳鳴り__month_residual × 気象庁_地震月報_カタログ編:m5_flag
- ラグ: -7D (target_precedes_external)
- 特徴量調整: month_residual
- 交絡調整: month,day_of_week,weekend_or_holiday,year_trend
- モデル: calendar_adjusted_correlation+ols+logistic_probe
- 効果量: correlation=-0.10491623599173233, coefficient=-0.12424220188889058
- p値/FDR: p=0.0196078431372549, q=0.09914077990746861
- 検証性能: AUC=0.42169598625787946, rate_ratio=-1.2524751990625784
- Negative control: corr=0.10896805064109472, pass=False
- 解釈: 多重検定込みの探索的シグナル。前兆方向か反応方向かを必ず確認してください。
- 注意点: 季節性、曜日、休日、投稿量バイアス、地震後反応の混入に注意。
- データ取得状況: status=ok

# Failed or Skipped Sources

- {"external_source_id": "google_trends", "status": "skip", "error_message": "pytrends is unavailable or blocked: ModuleNotFoundError(\"No module named 'pytrends'\")"}
- {"status": "year_unavailable", "dataset_id": "気象庁_地震月報_カタログ編", "year": 2024, "reason": "JMA hypocenter ZIP is not linked from hypo_e.html", "source_id": "excel_dataset"}
- {"status": "fetch_error", "query": "earthquake cloud", "start_date": "2020-01-01", "attempt": 0, "sample_http": {"url": "https://api.gdeltproject.org/api/v2/doc/doc", "final_url": "https://api.gdeltproject.org/api/v2/doc/doc", "status_code": null, "content_type": null, "text_head": "", "error": "ReadTimeout(ReadTimeoutError(\"HTTPSConnectionPool(host='api.gdeltproject.org', port=443): Read timed out. (read timeout=5)\"))"}, "source_id": "gdelt"}
- {"status": "fetch_error", "query": "earthquake cloud", "start_date": "2021-01-01", "attempt": 0, "sample_http": {"url": "https://api.gdeltproject.org/api/v2/doc/doc", "final_url": "https://api.gdeltproject.org/api/v2/doc/doc", "status_code": null, "content_type": null, "text_head": "", "error": "ReadTimeout(ReadTimeoutError(\"HTTPSConnectionPool(host='api.gdeltproject.org', port=443): Read timed out. (read timeout=5)\"))"}, "source_id": "gdelt"}
- {"status": "fetch_error", "query": "earthquake cloud", "start_date": "2022-01-01", "attempt": 0, "sample_http": {"url": "https://api.gdeltproject.org/api/v2/doc/doc", "final_url": "https://api.gdeltproject.org/api/v2/doc/doc", "status_code": null, "content_type": null, "text_head": "", "error": "ReadTimeout(ReadTimeoutError(\"HTTPSConnectionPool(host='api.gdeltproject.org', port=443): Read timed out. (read timeout=5)\"))"}, "source_id": "gdelt"}
- {"status": "fetch_error", "query": "earthquake cloud", "start_date": "2023-01-01", "attempt": 0, "sample_http": {"url": "https://api.gdeltproject.org/api/v2/doc/doc", "final_url": "https://api.gdeltproject.org/api/v2/doc/doc", "status_code": null, "content_type": null, "text_head": "", "error": "ReadTimeout(ReadTimeoutError(\"HTTPSConnectionPool(host='api.gdeltproject.org', port=443): Read timed out. (read timeout=5)\"))"}, "source_id": "gdelt"}
- {"status": "fetch_error", "query": "earthquake cloud", "start_date": "2024-01-01", "attempt": 0, "sample_http": {"url": "https://api.gdeltproject.org/api/v2/doc/doc", "final_url": "https://api.gdeltproject.org/api/v2/doc/doc", "status_code": null, "content_type": null, "text_head": "", "error": "ReadTimeout(ReadTimeoutError(\"HTTPSConnectionPool(host='api.gdeltproject.org', port=443): Read timed out. (read timeout=5)\"))"}, "source_id": "gdelt"}
- {"external_source_id": "gdelt", "status": "skip", "error_message": "No GDELT rows fetched; API may have timed out or returned a new schema"}
- {"external_source_id": "glotec", "status": "skip", "error_message": "GloTEC products are typically NetCDF/space-weather grids; add a stable product URL and netCDF parser before automated fetch. Probe report records this as a planned adapter instead of guessing a raw endpoint."}
- {"external_source_id": "aist_well", "status": "skip", "error_message": "AIST groundwater/well data requires source-specific access checks; do not scrape until terms and download endpoints are confirmed."}
- {"external_source_id": "movebank", "status": "skip", "error_message": "Movebank generally requires account/API credentials or per-study permission; public-only unauthenticated endpoint was not configured."}
- {"external_source_id": "ebird", "status": "skip", "error_message": "eBird API requires EBIRD_API_KEY; Basic Dataset also requires request/approval."}
- {"external_source_id": "openaq", "status": "skip", "error_message": "OpenAQ v3 requires OPENAQ_API_KEY in .env or environment."}
- {"external_source_id": "firms", "status": "skip", "error_message": "NASA FIRMS area CSV API requires NASA_FIRMS_MAP_KEY."}