# Executive Summary

This four-source space-weather scan is exploratory. It ranks lagged associations after calendar/autocorrelation controls, negative controls, FDR, and reverse-lag comparison. It does not imply earthquake prediction or causality.
- Metric rows: 35640
- Strict candidate rows: 1660
- Near-miss rows: 2037
- Modeled rows by source group: {'kp_dst': 5060, 'omni': 30250, 'combined': 330}

# Data Coverage

- kp_dst / gfz_kp_kyoto_dst: 2020-01-01..2024-12-31 days=1827 status=features_ok Dst included
- omni / nasa_cdaweb_omni2_h0_mrg1hr: 2020-01-01..2024-12-31 days=1827 status=features_ok 
- glotec / noaa_swpc_glotec: .. days=0 status=modeled_not_reached Global GloTEC public coverage starts in 2025; requested period has insufficient coverage.
- intermagnet / intermagnet_gin: .. days=0 status=modeled_not_reached Probe implemented; bulk IAGA/CDF parser deferred.
- jma_geomag / jma_kakioka_geomag: .. days=0 status=modeled_not_reached Metadata reachable; file-selection parser deferred.
- combined / combined_space_weather_features: 2020-01-01..2024-12-31 days=1827 status=features_ok PCA-like proxy features from overlapping fetched source features.
- excel / 気象庁_地震月報_カタログ編: 2020-01-01..2024-12-31 days=1827 status=modeled_ok 

# Strict Candidate Precursors

## 1. omni:plasma_beta_rolling_max_3d x 地震月報（カタログ編）:m3_flag
- lag: 30D (external_precedes_target)
- adjustment: derived
- n: 1797
- corr / partial: -0.10148545829384044 / -0.10148545829384044
- AUC / AP / Brier: 0.2322728956402531 / 0.7170645376061304 / 0.30955359936469323
- poisson_rate_ratio: None
- negative control: -0.06098401490316889 pass=True
- reverse best / pre-minus-reverse: 0.09178853162934936 / 0.009696926664491082
- FDR: 0.00028272059247941566

## 2. omni:plasma_beta_rolling_max_3d x 地震月報（カタログ編）:m3_flag
- lag: 3D (external_precedes_target)
- adjustment: derived
- n: 1824
- corr / partial: -0.09107934183462293 / -0.09107934183462293
- AUC / AP / Brier: 0.2351188468371225 / 0.7225328898425027 / 0.3090177746974423
- poisson_rate_ratio: None
- negative control: -0.07290243571562141 pass=True
- reverse best / pre-minus-reverse: 0.09178853162934936 / 0.009696926664491082
- FDR: 0.0012675666399319667

## 3. omni:plasma_beta_rolling_max_3d x 地震月報（カタログ編）:m3_flag
- lag: 7D (external_precedes_target)
- adjustment: derived
- n: 1820
- corr / partial: -0.09262168457343432 / -0.09262168457343432
- AUC / AP / Brier: 0.23544245758826227 / 0.7222421527187586 / 0.30880038916069014
- poisson_rate_ratio: None
- negative control: -0.073056637815401 pass=True
- reverse best / pre-minus-reverse: 0.09178853162934936 / 0.009696926664491082
- FDR: 0.0010245589911027015

## 4. omni:plasma_beta_rolling_max_7d x 地震月報（カタログ編）:m3_flag
- lag: 30D (external_precedes_target)
- adjustment: derived
- n: 1797
- corr / partial: -0.12708245769332419 / -0.12708245769332419
- AUC / AP / Brier: 0.23747389001538913 / 0.724933385892197 / 0.31926127050740594
- poisson_rate_ratio: None
- negative control: -0.09585888779135399 pass=True
- reverse best / pre-minus-reverse: 0.11349035332254871 / 0.013592104370775474
- FDR: 1.8490336855601184e-06

## 5. omni:plasma_beta_rolling_max_3d x 地震月報（カタログ編）:m3_flag
- lag: 1D (external_precedes_target)
- adjustment: derived
- n: 1826
- corr / partial: -0.08928083000767408 / -0.08928083000767408
- AUC / AP / Brier: 0.23792387154727151 / 0.7233545600604124 / 0.3090927774734107
- poisson_rate_ratio: None
- negative control: -0.07387397646195079 pass=True
- reverse best / pre-minus-reverse: 0.09178853162934936 / 0.009696926664491082
- FDR: 0.0016210674571269304

## 6. omni:plasma_beta_rolling_max_3d x 地震月報（カタログ編）:m3_flag
- lag: 14D (external_precedes_target)
- adjustment: derived
- n: 1813
- corr / partial: -0.09598365534793125 / -0.09598365534793125
- AUC / AP / Brier: 0.23901155962401954 / 0.7225948474891192 / 0.30898860876398837
- poisson_rate_ratio: None
- negative control: -0.07128547477250766 pass=True
- reverse best / pre-minus-reverse: 0.09178853162934936 / 0.009696926664491082
- FDR: 0.0006298879391825078

## 7. omni:plasma_beta_rolling_max_7d x 地震月報（カタログ編）:m3_flag
- lag: 1D (external_precedes_target)
- adjustment: derived
- n: 1826
- corr / partial: -0.11232437197091522 / -0.11232437197091522
- AUC / AP / Brier: 0.24163298151059212 / 0.730605605321584 / 0.3183487597198789
- poisson_rate_ratio: None
- negative control: -0.10901334031497212 pass=True
- reverse best / pre-minus-reverse: 0.11349035332254871 / 0.013592104370775474
- FDR: 3.334984184017482e-05

## 8. omni:plasma_beta_rolling_max_7d x 地震月報（カタログ編）:m3_flag
- lag: 3D (external_precedes_target)
- adjustment: derived
- n: 1824
- corr / partial: -0.11404201259415911 / -0.11404201259415911
- AUC / AP / Brier: 0.24172082424460486 / 0.7301332499891692 / 0.31830400137155923
- poisson_rate_ratio: None
- negative control: -0.10765062929821614 pass=True
- reverse best / pre-minus-reverse: 0.11349035332254871 / 0.013592104370775474
- FDR: 2.3856511150240207e-05

## 9. omni:plasma_beta_rolling_mean_14d x 地震月報（カタログ編）:m3_flag
- lag: 30D (external_precedes_target)
- adjustment: derived
- n: 1797
- corr / partial: -0.27039709087859404 / -0.27039709087859404
- AUC / AP / Brier: 0.24176413757813903 / 0.7265604764060877 / 0.35042362631426216
- poisson_rate_ratio: None
- negative control: 0.12576704468378738 pass=True
- reverse best / pre-minus-reverse: 0.24016294064543336 / 0.030234150233160673
- FDR: 6.726285451974403e-29

## 10. omni:plasma_beta_rolling_mean_14d x 地震月報（カタログ編）:m3_flag
- lag: 14D (external_precedes_target)
- adjustment: derived
- n: 1813
- corr / partial: -0.2570088392644402 / -0.2570088392644402
- AUC / AP / Brier: 0.24732157355901224 / 0.7266364969636477 / 0.34892414098370667
- poisson_rate_ratio: None
- negative control: -0.14294789322552273 pass=True
- reverse best / pre-minus-reverse: 0.24016294064543336 / 0.030234150233160673
- FDR: 3.0584359111355385e-26

# Near-Miss Candidate Precursors

## 1. omni:plasma_beta_rolling_max_3d x 地震月報（カタログ編）:m3_flag
- lag: 30D (external_precedes_target)
- adjustment: derived
- n: 1797
- corr / partial: -0.10148545829384044 / -0.10148545829384044
- AUC / AP / Brier: 0.2322728956402531 / 0.7170645376061304 / 0.30955359936469323
- poisson_rate_ratio: None
- negative control: -0.06098401490316889 pass=True
- reverse best / pre-minus-reverse: 0.09178853162934936 / 0.009696926664491082
- FDR: 0.00028272059247941566

## 2. omni:plasma_beta_rolling_max_3d x 地震月報（カタログ編）:m3_flag
- lag: 3D (external_precedes_target)
- adjustment: derived
- n: 1824
- corr / partial: -0.09107934183462293 / -0.09107934183462293
- AUC / AP / Brier: 0.2351188468371225 / 0.7225328898425027 / 0.3090177746974423
- poisson_rate_ratio: None
- negative control: -0.07290243571562141 pass=True
- reverse best / pre-minus-reverse: 0.09178853162934936 / 0.009696926664491082
- FDR: 0.0012675666399319667

## 3. omni:plasma_beta_rolling_max_3d x 地震月報（カタログ編）:m3_flag
- lag: 7D (external_precedes_target)
- adjustment: derived
- n: 1820
- corr / partial: -0.09262168457343432 / -0.09262168457343432
- AUC / AP / Brier: 0.23544245758826227 / 0.7222421527187586 / 0.30880038916069014
- poisson_rate_ratio: None
- negative control: -0.073056637815401 pass=True
- reverse best / pre-minus-reverse: 0.09178853162934936 / 0.009696926664491082
- FDR: 0.0010245589911027015

## 4. omni:plasma_beta_rolling_max_7d x 地震月報（カタログ編）:m3_flag
- lag: 30D (external_precedes_target)
- adjustment: derived
- n: 1797
- corr / partial: -0.12708245769332419 / -0.12708245769332419
- AUC / AP / Brier: 0.23747389001538913 / 0.724933385892197 / 0.31926127050740594
- poisson_rate_ratio: None
- negative control: -0.09585888779135399 pass=True
- reverse best / pre-minus-reverse: 0.11349035332254871 / 0.013592104370775474
- FDR: 1.8490336855601184e-06

## 5. omni:plasma_beta_rolling_max_3d x 地震月報（カタログ編）:m3_flag
- lag: 1D (external_precedes_target)
- adjustment: derived
- n: 1826
- corr / partial: -0.08928083000767408 / -0.08928083000767408
- AUC / AP / Brier: 0.23792387154727151 / 0.7233545600604124 / 0.3090927774734107
- poisson_rate_ratio: None
- negative control: -0.07387397646195079 pass=True
- reverse best / pre-minus-reverse: 0.09178853162934936 / 0.009696926664491082
- FDR: 0.0016210674571269304

## 6. omni:plasma_beta_rolling_max_3d x 地震月報（カタログ編）:m3_flag
- lag: 14D (external_precedes_target)
- adjustment: derived
- n: 1813
- corr / partial: -0.09598365534793125 / -0.09598365534793125
- AUC / AP / Brier: 0.23901155962401954 / 0.7225948474891192 / 0.30898860876398837
- poisson_rate_ratio: None
- negative control: -0.07128547477250766 pass=True
- reverse best / pre-minus-reverse: 0.09178853162934936 / 0.009696926664491082
- FDR: 0.0006298879391825078

## 7. omni:plasma_beta_rolling_max_7d x 地震月報（カタログ編）:m3_flag
- lag: 1D (external_precedes_target)
- adjustment: derived
- n: 1826
- corr / partial: -0.11232437197091522 / -0.11232437197091522
- AUC / AP / Brier: 0.24163298151059212 / 0.730605605321584 / 0.3183487597198789
- poisson_rate_ratio: None
- negative control: -0.10901334031497212 pass=True
- reverse best / pre-minus-reverse: 0.11349035332254871 / 0.013592104370775474
- FDR: 3.334984184017482e-05

## 8. omni:plasma_beta_rolling_max_7d x 地震月報（カタログ編）:m3_flag
- lag: 3D (external_precedes_target)
- adjustment: derived
- n: 1824
- corr / partial: -0.11404201259415911 / -0.11404201259415911
- AUC / AP / Brier: 0.24172082424460486 / 0.7301332499891692 / 0.31830400137155923
- poisson_rate_ratio: None
- negative control: -0.10765062929821614 pass=True
- reverse best / pre-minus-reverse: 0.11349035332254871 / 0.013592104370775474
- FDR: 2.3856511150240207e-05

## 9. omni:plasma_beta_rolling_mean_14d x 地震月報（カタログ編）:m3_flag
- lag: 30D (external_precedes_target)
- adjustment: derived
- n: 1797
- corr / partial: -0.27039709087859404 / -0.27039709087859404
- AUC / AP / Brier: 0.24176413757813903 / 0.7265604764060877 / 0.35042362631426216
- poisson_rate_ratio: None
- negative control: 0.12576704468378738 pass=True
- reverse best / pre-minus-reverse: 0.24016294064543336 / 0.030234150233160673
- FDR: 6.726285451974403e-29

## 10. omni:plasma_beta_rolling_mean_14d x 地震月報（カタログ編）:m3_flag
- lag: 14D (external_precedes_target)
- adjustment: derived
- n: 1813
- corr / partial: -0.2570088392644402 / -0.2570088392644402
- AUC / AP / Brier: 0.24732157355901224 / 0.7266364969636477 / 0.34892414098370667
- poisson_rate_ratio: None
- negative control: -0.14294789322552273 pass=True
- reverse best / pre-minus-reverse: 0.24016294064543336 / 0.030234150233160673
- FDR: 3.0584359111355385e-26

# Kp/Dst Results

## 1. kp_dst:storm_flag_dst_le_minus100 x 地震月報（カタログ編）:m3_flag
- lag: -30D (target_precedes_external)
- adjustment: raw
- n: 1797
- corr / partial: -0.034387951942013974 / -0.034387951942013974
- AUC / AP / Brier: 0.8745579511749942 / 0.9352052426490388 / 0.25976704444202964
- poisson_rate_ratio: None
- negative control: 0.062256662604219776 pass=False
- reverse best / pre-minus-reverse: 0.034387951942013974 / 0.018842579252896917
- FDR: 0.45589782946806967

## 2. kp_dst:storm_flag_dst_le_minus100 x 地震月報（カタログ編）:m3_flag
- lag: 0D (same_day)
- adjustment: raw
- n: 1827
- corr / partial: -0.03084398565557024 / -0.03084398565557024
- AUC / AP / Brier: 0.8536521508211682 / 0.9261263843494517 / 0.2590021637210477
- poisson_rate_ratio: None
- negative control: 0.06453597253600188 pass=False
- reverse best / pre-minus-reverse: 0.034387951942013974 / 0.018842579252896917
- FDR: 0.5404808857493418

## 3. kp_dst:storm_flag_dst_le_minus100 x 地震月報（カタログ編）:m3_flag
- lag: 1D (external_precedes_target)
- adjustment: raw
- n: 1826
- corr / partial: -0.03115226191194855 / -0.03115226191194855
- AUC / AP / Brier: 0.8443521221648327 / 0.9232849784696656 / 0.25904661997969064
- poisson_rate_ratio: None
- negative control: 0.0616405501681688 pass=False
- reverse best / pre-minus-reverse: 0.034387951942013974 / 0.018842579252896917
- FDR: 0.5326694431878215

## 4. kp_dst:storm_flag_dst_le_minus100 x 地震月報（カタログ編）:m3_flag
- lag: -7D (target_precedes_external)
- adjustment: raw
- n: 1820
- corr / partial: -0.03088522115747841 / -0.03088522115747841
- AUC / AP / Brier: 0.8442113331007304 / 0.9245429900592962 / 0.2592507870724357
- poisson_rate_ratio: None
- negative control: 0.04743036832886733 pass=False
- reverse best / pre-minus-reverse: 0.034387951942013974 / 0.018842579252896917
- FDR: 0.540812645770445

## 5. kp_dst:storm_flag_dst_le_minus100 x 地震月報（カタログ編）:m3_flag
- lag: -1D (target_precedes_external)
- adjustment: raw
- n: 1826
- corr / partial: -0.031050635588112538 / -0.031050635588112538
- AUC / AP / Brier: 0.8430217621632772 / 0.923045944540951 / 0.25909136775894526
- poisson_rate_ratio: None
- negative control: 0.06394957832536807 pass=False
- reverse best / pre-minus-reverse: 0.034387951942013974 / 0.018842579252896917
- FDR: 0.5351516424837365

## 6. kp_dst:storm_flag_dst_le_minus100 x 地震月報（カタログ編）:m3_flag
- lag: 30D (external_precedes_target)
- adjustment: raw
- n: 1797
- corr / partial: -0.05323053119491089 / -0.05323053119491089
- AUC / AP / Brier: 0.8398231203675064 / 0.918785295258458 / 0.259053441801167
- poisson_rate_ratio: None
- negative control: -0.06405624870080891 pass=False
- reverse best / pre-minus-reverse: 0.034387951942013974 / 0.018842579252896917
- FDR: 0.11610037034445514

## 7. kp_dst:storm_flag_dst_le_minus100 x 地震月報（カタログ編）:m3_flag
- lag: -14D (target_precedes_external)
- adjustment: raw
- n: 1813
- corr / partial: -0.03058852481295218 / -0.03058852481295218
- AUC / AP / Brier: 0.8381109607367307 / 0.9238229874034711 / 0.25946908501887356
- poisson_rate_ratio: None
- negative control: 0.059759944417903506 pass=False
- reverse best / pre-minus-reverse: 0.034387951942013974 / 0.018842579252896917
- FDR: 0.5490732708614766

## 8. kp_dst:storm_flag_dst_le_minus100 x 地震月報（カタログ編）:m3_flag
- lag: -3D (target_precedes_external)
- adjustment: raw
- n: 1824
- corr / partial: -0.030818867476425423 / -0.030818867476425423
- AUC / AP / Brier: 0.8372223259286914 / 0.9222755285247569 / 0.2591230508120076
- poisson_rate_ratio: None
- negative control: 0.06623242284484546 pass=False
- reverse best / pre-minus-reverse: 0.034387951942013974 / 0.018842579252896917
- FDR: 0.5415127841846846

## 9. kp_dst:storm_flag_dst_le_minus100 x 地震月報（カタログ編）:m3_flag
- lag: 7D (external_precedes_target)
- adjustment: raw
- n: 1820
- corr / partial: -0.03119106425349902 / -0.03119106425349902
- AUC / AP / Brier: 0.825196743860915 / 0.9168566998915925 / 0.2590649304631521
- poisson_rate_ratio: None
- negative control: 0.05780761714442742 pass=False
- reverse best / pre-minus-reverse: 0.034387951942013974 / 0.018842579252896917
- FDR: 0.5330444238698357

## 10. kp_dst:storm_flag_dst_le_minus100 x 地震月報（カタログ編）:m3_flag
- lag: 14D (external_precedes_target)
- adjustment: raw
- n: 1813
- corr / partial: -0.031428605174130486 / -0.031428605174130486
- AUC / AP / Brier: 0.8250308722399085 / 0.9173474731035227 / 0.2590719133552055
- poisson_rate_ratio: None
- negative control: 0.06850587252954601 pass=False
- reverse best / pre-minus-reverse: 0.034387951942013974 / 0.018842579252896917
- FDR: 0.5284577826736875

# NOAA GloTEC / TEC Results

No rows matched this section.

# NASA OMNI / CDAWeb Results

## 1. omni:F10_7_missing_ratio x 地震月報（カタログ編）:m3_flag
- lag: 30D (external_precedes_target)
- adjustment: quality
- n: 1797
- corr / partial: -8.463996594212132e-05 / -8.463996594212132e-05
- AUC / AP / Brier: 0.18202143787255654 / 0.6357942358933362 / 0.2563307887053635
- poisson_rate_ratio: None
- negative control: 0.03437719913925492 pass=False
- reverse best / pre-minus-reverse: 0.000523779531032664 / -0.00010434833583385284
- FDR: 0.9999632851926542

## 2. omni:F10_7_valid_count x 地震月報（カタログ編）:m3_flag
- lag: 30D (external_precedes_target)
- adjustment: quality
- n: 1797
- corr / partial: 8.46399659421246e-05 / 8.46399659421246e-05
- AUC / AP / Brier: 0.8179785621274435 / 0.902480313725448 / 0.24522460619195297
- poisson_rate_ratio: None
- negative control: -0.03437719913925492 pass=False
- reverse best / pre-minus-reverse: 0.0005237795310326661 / -0.00010434833583384173
- FDR: 0.9999632851926542

## 3. omni:F10_7_missing_ratio x 地震月報（カタログ編）:m3_flag
- lag: -14D (target_precedes_external)
- adjustment: quality
- n: 1813
- corr / partial: 0.0004955725549440567 / 0.0004955725549440567
- AUC / AP / Brier: 0.18289348827079832 / 0.6474998699115797 / 0.2561325842201817
- poisson_rate_ratio: None
- negative control: -0.04492105751049033 pass=False
- reverse best / pre-minus-reverse: 0.000523779531032664 / -0.00010434833583385284
- FDR: 0.9999632851926542

## 4. omni:F10_7_valid_count x 地震月報（カタログ編）:m3_flag
- lag: -14D (target_precedes_external)
- adjustment: quality
- n: 1813
- corr / partial: -0.0004955725549440592 / -0.0004955725549440592
- AUC / AP / Brier: 0.8171065117292017 / 0.9062419778254737 / 0.2454153193421225
- poisson_rate_ratio: None
- negative control: 0.044921057510490324 pass=False
- reverse best / pre-minus-reverse: 0.0005237795310326661 / -0.00010434833583384173
- FDR: 0.9999632851926542

## 5. omni:F10_7_missing_ratio x 地震月報（カタログ編）:m3_flag
- lag: 0D (same_day)
- adjustment: quality
- n: 1827
- corr / partial: -2.2575830100672322e-05 / -2.2575830100672322e-05
- AUC / AP / Brier: 0.18591390730953797 / 0.6401148778924723 / 0.2562220786284723
- poisson_rate_ratio: None
- negative control: 0.022138846969674292 pass=False
- reverse best / pre-minus-reverse: 0.000523779531032664 / -0.00010434833583385284
- FDR: 0.9999632851926542

## 6. omni:F10_7_valid_count x 地震月報（カタログ編）:m3_flag
- lag: 0D (same_day)
- adjustment: quality
- n: 1827
- corr / partial: 2.2575830100662226e-05 / 2.2575830100662226e-05
- AUC / AP / Brier: 0.8140860926904621 / 0.9033383046357867 / 0.2452692429737805
- poisson_rate_ratio: None
- negative control: -0.022138846969674383 pass=False
- reverse best / pre-minus-reverse: 0.0005237795310326661 / -0.00010434833583384173
- FDR: 0.9999632851926542

## 7. omni:F10_7_missing_ratio x 地震月報（カタログ編）:m3_flag
- lag: 14D (external_precedes_target)
- adjustment: quality
- n: 1813
- corr / partial: 0.0002749922925676739 / 0.0002749922925676739
- AUC / AP / Brier: 0.18604725812968984 / 0.6382475926014703 / 0.25618743879859823
- poisson_rate_ratio: None
- negative control: 0.03326122599555669 pass=False
- reverse best / pre-minus-reverse: 0.000523779531032664 / -0.00010434833583385284
- FDR: 0.9999632851926542

## 8. omni:F10_7_valid_count x 地震月報（カタログ編）:m3_flag
- lag: 14D (external_precedes_target)
- adjustment: quality
- n: 1813
- corr / partial: -0.00027499229256768676 / -0.00027499229256768676
- AUC / AP / Brier: 0.8139527418703102 / 0.9026877448158891 / 0.24530810797435307
- poisson_rate_ratio: None
- negative control: -0.033261225995556684 pass=False
- reverse best / pre-minus-reverse: 0.0005237795310326661 / -0.00010434833583384173
- FDR: 0.9999632851926542

## 9. omni:F10_7_missing_ratio x 地震月報（カタログ編）:m3_flag
- lag: 7D (external_precedes_target)
- adjustment: quality
- n: 1820
- corr / partial: 0.00011116126304112208 / 0.00011116126304112208
- AUC / AP / Brier: 0.18605542652265092 / 0.6391914969555422 / 0.25620467382377876
- poisson_rate_ratio: None
- negative control: 0.038161660056208184 pass=False
- reverse best / pre-minus-reverse: 0.000523779531032664 / -0.00010434833583385284
- FDR: 0.9999632851926542

## 10. omni:F10_7_valid_count x 地震月報（カタログ編）:m3_flag
- lag: 7D (external_precedes_target)
- adjustment: quality
- n: 1820
- corr / partial: -0.00011116126304113537 / -0.00011116126304113537
- AUC / AP / Brier: 0.813944573477349 / 0.9029982936870591 / 0.24528860207199094
- poisson_rate_ratio: None
- negative control: -0.038161660056208184 pass=False
- reverse best / pre-minus-reverse: 0.0005237795310326661 / -0.00010434833583384173
- FDR: 0.9999632851926542

# INTERMAGNET / JMA Geomagnetic Results

No rows matched this section.

# Combined Space Weather Feature Results

## 1. combined:space_weather_activity_pc1_proxy x 地震月報（カタログ編）:m3_flag
- lag: 14D (external_precedes_target)
- adjustment: derived
- n: 1813
- corr / partial: 0.04954915215522806 / 0.04954915215522806
- AUC / AP / Brier: 0.6164440466614552 / 0.8264176383928427 / 0.272133280509461
- poisson_rate_ratio: None
- negative control: 0.04550842572005759 pass=True
- reverse best / pre-minus-reverse: 0.04448985943610531 / 0.005059292719122747
- FDR: 0.15620823081014895

## 2. combined:space_weather_activity_pc1_proxy x 地震月報（カタログ編）:m3_flag
- lag: 30D (external_precedes_target)
- adjustment: derived
- n: 1797
- corr / partial: 0.04735845901612796 / 0.04735845901612796
- AUC / AP / Brier: 0.6139330897037877 / 0.8213594999612308 / 0.272498490845233
- poisson_rate_ratio: None
- negative control: -0.055379867343366376 pass=False
- reverse best / pre-minus-reverse: 0.04448985943610531 / 0.005059292719122747
- FDR: 0.19044653437026227

## 3. combined:space_weather_activity_pc1_proxy x 地震月報（カタログ編）:m4_flag
- lag: 14D (external_precedes_target)
- adjustment: derived
- n: 1813
- corr / partial: 0.058622529234319015 / 0.058622529234319015
- AUC / AP / Brier: 0.6138794073123215 / 0.788366806689615 / 0.26741170532855274
- poisson_rate_ratio: None
- negative control: 0.045325289754688615 pass=True
- reverse best / pre-minus-reverse: 0.04788873574144859 / 0.010733793492870423
- FDR: 0.06859332029979176

## 4. combined:space_weather_activity_pc1_proxy x 地震月報（カタログ編）:m3_flag
- lag: 7D (external_precedes_target)
- adjustment: derived
- n: 1820
- corr / partial: 0.04923333888499758 / 0.04923333888499758
- AUC / AP / Brier: 0.6126570004735382 / 0.826434607768134 / 0.27262596535833167
- poisson_rate_ratio: None
- negative control: 0.05245775579979896 pass=False
- reverse best / pre-minus-reverse: 0.04448985943610531 / 0.005059292719122747
- FDR: 0.15923896551737146

## 5. combined:space_weather_activity_pc1_proxy x 地震月報（カタログ編）:m3_flag
- lag: -3D (target_precedes_external)
- adjustment: derived
- n: 1824
- corr / partial: 0.04448985943610531 / 0.04448985943610531
- AUC / AP / Brier: 0.6106218051336588 / 0.8261421267494484 / 0.2734989454707243
- poisson_rate_ratio: None
- negative control: 0.0517656284693516 pass=False
- reverse best / pre-minus-reverse: 0.04448985943610531 / 0.005059292719122747
- FDR: 0.2314705567520595

## 6. combined:space_weather_activity_pc1_proxy x 地震月報（カタログ編）:m3_flag
- lag: 1D (external_precedes_target)
- adjustment: derived
- n: 1826
- corr / partial: 0.04421880153462649 / 0.04421880153462649
- AUC / AP / Brier: 0.6097705666591811 / 0.8251693693163191 / 0.27328566448035835
- poisson_rate_ratio: None
- negative control: 0.054907601881806246 pass=False
- reverse best / pre-minus-reverse: 0.04448985943610531 / 0.005059292719122747
- FDR: 0.23583552375524527

## 7. combined:space_weather_activity_pc1_proxy x 地震月報（カタログ編）:m3_flag
- lag: 3D (external_precedes_target)
- adjustment: derived
- n: 1824
- corr / partial: 0.04448773071889515 / 0.04448773071889515
- AUC / AP / Brier: 0.6096306790498249 / 0.8253705050970688 / 0.27316712701016493
- poisson_rate_ratio: None
- negative control: -0.06121774679519083 pass=False
- reverse best / pre-minus-reverse: 0.04448985943610531 / 0.005059292719122747
- FDR: 0.2314705567520595

## 8. combined:space_weather_activity_pc1_proxy x 地震月報（カタログ編）:m3_flag
- lag: -1D (target_precedes_external)
- adjustment: derived
- n: 1826
- corr / partial: 0.041318235719233466 / 0.041318235719233466
- AUC / AP / Brier: 0.608776124440944 / 0.8248200746197275 / 0.2735899199018844
- poisson_rate_ratio: None
- negative control: 0.05245622423127762 pass=False
- reverse best / pre-minus-reverse: 0.04448985943610531 / 0.005059292719122747
- FDR: 0.291277936070369

## 9. combined:space_weather_activity_pc1_proxy x 地震月報（カタログ編）:m3_flag
- lag: 0D (same_day)
- adjustment: derived
- n: 1827
- corr / partial: 0.041268155668303226 / 0.041268155668303226
- AUC / AP / Brier: 0.6086575180559763 / 0.8246060895278967 / 0.2736127848043393
- poisson_rate_ratio: None
- negative control: 0.05452545855691827 pass=False
- reverse best / pre-minus-reverse: 0.04448985943610531 / 0.005059292719122747
- FDR: 0.29182434900656634

## 10. combined:space_weather_activity_pc1_proxy x 地震月報（カタログ編）:m3_flag
- lag: -7D (target_precedes_external)
- adjustment: derived
- n: 1820
- corr / partial: 0.04191121688143646 / 0.04191121688143646
- AUC / AP / Brier: 0.6073395754806015 / 0.8268359667211297 / 0.27426574917063373
- poisson_rate_ratio: None
- negative control: 0.05403850579079726 pass=False
- reverse best / pre-minus-reverse: 0.04448985943610531 / 0.005059292719122747
- FDR: 0.2808772398211941

# Results by Excel Dataset Category

## 1. kp_dst:storm_flag_dst_le_minus100 x 地震月報（カタログ編）:m3_flag
- lag: -30D (target_precedes_external)
- adjustment: raw
- n: 1797
- corr / partial: -0.034387951942013974 / -0.034387951942013974
- AUC / AP / Brier: 0.8745579511749942 / 0.9352052426490388 / 0.25976704444202964
- poisson_rate_ratio: None
- negative control: 0.062256662604219776 pass=False
- reverse best / pre-minus-reverse: 0.034387951942013974 / 0.018842579252896917
- FDR: 0.45589782946806967

## 2. kp_dst:storm_flag_dst_le_minus100 x 地震月報（カタログ編）:m3_flag
- lag: 0D (same_day)
- adjustment: raw
- n: 1827
- corr / partial: -0.03084398565557024 / -0.03084398565557024
- AUC / AP / Brier: 0.8536521508211682 / 0.9261263843494517 / 0.2590021637210477
- poisson_rate_ratio: None
- negative control: 0.06453597253600188 pass=False
- reverse best / pre-minus-reverse: 0.034387951942013974 / 0.018842579252896917
- FDR: 0.5404808857493418

## 3. kp_dst:storm_flag_dst_le_minus100 x 地震月報（カタログ編）:m3_flag
- lag: 1D (external_precedes_target)
- adjustment: raw
- n: 1826
- corr / partial: -0.03115226191194855 / -0.03115226191194855
- AUC / AP / Brier: 0.8443521221648327 / 0.9232849784696656 / 0.25904661997969064
- poisson_rate_ratio: None
- negative control: 0.0616405501681688 pass=False
- reverse best / pre-minus-reverse: 0.034387951942013974 / 0.018842579252896917
- FDR: 0.5326694431878215

## 4. kp_dst:storm_flag_dst_le_minus100 x 地震月報（カタログ編）:m3_flag
- lag: -7D (target_precedes_external)
- adjustment: raw
- n: 1820
- corr / partial: -0.03088522115747841 / -0.03088522115747841
- AUC / AP / Brier: 0.8442113331007304 / 0.9245429900592962 / 0.2592507870724357
- poisson_rate_ratio: None
- negative control: 0.04743036832886733 pass=False
- reverse best / pre-minus-reverse: 0.034387951942013974 / 0.018842579252896917
- FDR: 0.540812645770445

## 5. kp_dst:storm_flag_dst_le_minus100 x 地震月報（カタログ編）:m3_flag
- lag: -1D (target_precedes_external)
- adjustment: raw
- n: 1826
- corr / partial: -0.031050635588112538 / -0.031050635588112538
- AUC / AP / Brier: 0.8430217621632772 / 0.923045944540951 / 0.25909136775894526
- poisson_rate_ratio: None
- negative control: 0.06394957832536807 pass=False
- reverse best / pre-minus-reverse: 0.034387951942013974 / 0.018842579252896917
- FDR: 0.5351516424837365

## 6. kp_dst:storm_flag_dst_le_minus100 x 地震月報（カタログ編）:m3_flag
- lag: 30D (external_precedes_target)
- adjustment: raw
- n: 1797
- corr / partial: -0.05323053119491089 / -0.05323053119491089
- AUC / AP / Brier: 0.8398231203675064 / 0.918785295258458 / 0.259053441801167
- poisson_rate_ratio: None
- negative control: -0.06405624870080891 pass=False
- reverse best / pre-minus-reverse: 0.034387951942013974 / 0.018842579252896917
- FDR: 0.11610037034445514

## 7. kp_dst:storm_flag_dst_le_minus100 x 地震月報（カタログ編）:m3_flag
- lag: -14D (target_precedes_external)
- adjustment: raw
- n: 1813
- corr / partial: -0.03058852481295218 / -0.03058852481295218
- AUC / AP / Brier: 0.8381109607367307 / 0.9238229874034711 / 0.25946908501887356
- poisson_rate_ratio: None
- negative control: 0.059759944417903506 pass=False
- reverse best / pre-minus-reverse: 0.034387951942013974 / 0.018842579252896917
- FDR: 0.5490732708614766

## 8. kp_dst:storm_flag_dst_le_minus100 x 地震月報（カタログ編）:m3_flag
- lag: -3D (target_precedes_external)
- adjustment: raw
- n: 1824
- corr / partial: -0.030818867476425423 / -0.030818867476425423
- AUC / AP / Brier: 0.8372223259286914 / 0.9222755285247569 / 0.2591230508120076
- poisson_rate_ratio: None
- negative control: 0.06623242284484546 pass=False
- reverse best / pre-minus-reverse: 0.034387951942013974 / 0.018842579252896917
- FDR: 0.5415127841846846

## 9. kp_dst:storm_flag_dst_le_minus100 x 地震月報（カタログ編）:m3_flag
- lag: 7D (external_precedes_target)
- adjustment: raw
- n: 1820
- corr / partial: -0.03119106425349902 / -0.03119106425349902
- AUC / AP / Brier: 0.825196743860915 / 0.9168566998915925 / 0.2590649304631521
- poisson_rate_ratio: None
- negative control: 0.05780761714442742 pass=False
- reverse best / pre-minus-reverse: 0.034387951942013974 / 0.018842579252896917
- FDR: 0.5330444238698357

## 10. kp_dst:storm_flag_dst_le_minus100 x 地震月報（カタログ編）:m3_flag
- lag: 14D (external_precedes_target)
- adjustment: raw
- n: 1813
- corr / partial: -0.031428605174130486 / -0.031428605174130486
- AUC / AP / Brier: 0.8250308722399085 / 0.9173474731035227 / 0.2590719133552055
- poisson_rate_ratio: None
- negative control: 0.06850587252954601 pass=False
- reverse best / pre-minus-reverse: 0.034387951942013974 / 0.018842579252896917
- FDR: 0.5284577826736875

# Reverse-Lag / Post-Reaction Signals

## 1. kp_dst:storm_flag_dst_le_minus100 x 地震月報（カタログ編）:m3_flag
- lag: -30D (target_precedes_external)
- adjustment: raw
- n: 1797
- corr / partial: -0.034387951942013974 / -0.034387951942013974
- AUC / AP / Brier: 0.8745579511749942 / 0.9352052426490388 / 0.25976704444202964
- poisson_rate_ratio: None
- negative control: 0.062256662604219776 pass=False
- reverse best / pre-minus-reverse: 0.034387951942013974 / 0.018842579252896917
- FDR: 0.45589782946806967

## 2. kp_dst:storm_flag_dst_le_minus100 x 地震月報（カタログ編）:m3_flag
- lag: -7D (target_precedes_external)
- adjustment: raw
- n: 1820
- corr / partial: -0.03088522115747841 / -0.03088522115747841
- AUC / AP / Brier: 0.8442113331007304 / 0.9245429900592962 / 0.2592507870724357
- poisson_rate_ratio: None
- negative control: 0.04743036832886733 pass=False
- reverse best / pre-minus-reverse: 0.034387951942013974 / 0.018842579252896917
- FDR: 0.540812645770445

## 3. kp_dst:storm_flag_dst_le_minus100 x 地震月報（カタログ編）:m3_flag
- lag: -1D (target_precedes_external)
- adjustment: raw
- n: 1826
- corr / partial: -0.031050635588112538 / -0.031050635588112538
- AUC / AP / Brier: 0.8430217621632772 / 0.923045944540951 / 0.25909136775894526
- poisson_rate_ratio: None
- negative control: 0.06394957832536807 pass=False
- reverse best / pre-minus-reverse: 0.034387951942013974 / 0.018842579252896917
- FDR: 0.5351516424837365

## 4. kp_dst:storm_flag_dst_le_minus100 x 地震月報（カタログ編）:m3_flag
- lag: -14D (target_precedes_external)
- adjustment: raw
- n: 1813
- corr / partial: -0.03058852481295218 / -0.03058852481295218
- AUC / AP / Brier: 0.8381109607367307 / 0.9238229874034711 / 0.25946908501887356
- poisson_rate_ratio: None
- negative control: 0.059759944417903506 pass=False
- reverse best / pre-minus-reverse: 0.034387951942013974 / 0.018842579252896917
- FDR: 0.5490732708614766

## 5. kp_dst:storm_flag_dst_le_minus100 x 地震月報（カタログ編）:m3_flag
- lag: -3D (target_precedes_external)
- adjustment: raw
- n: 1824
- corr / partial: -0.030818867476425423 / -0.030818867476425423
- AUC / AP / Brier: 0.8372223259286914 / 0.9222755285247569 / 0.2591230508120076
- poisson_rate_ratio: None
- negative control: 0.06623242284484546 pass=False
- reverse best / pre-minus-reverse: 0.034387951942013974 / 0.018842579252896917
- FDR: 0.5415127841846846

## 6. kp_dst:storm_joint_flag x 地震月報（カタログ編）:m3_flag
- lag: -30D (target_precedes_external)
- adjustment: raw
- n: 1797
- corr / partial: 0.019128970972951145 / 0.019128970972951145
- AUC / AP / Brier: 0.8244882826505003 / 0.9204608840156624 / 0.27339645160976067
- poisson_rate_ratio: None
- negative control: 0.05754429999871384 pass=False
- reverse best / pre-minus-reverse: 0.025262400731832196 / 0.0008243464239609012
- FDR: 0.8257988766740998

## 7. kp_dst:storm_flag_kp_ge_6 x 地震月報（カタログ編）:m3_flag
- lag: -30D (target_precedes_external)
- adjustment: raw
- n: 1797
- corr / partial: -0.030701352352802212 / -0.030701352352802212
- AUC / AP / Brier: 0.8241664222157036 / 0.9200731574617868 / 0.2664744288874291
- poisson_rate_ratio: None
- negative control: 0.05801963900877014 pass=False
- reverse best / pre-minus-reverse: 0.030701352352802212 / -0.0020556245254774105
- FDR: 0.5494590331904533

## 8. kp_dst:storm_joint_flag x 地震月報（カタログ編）:m3_flag
- lag: -7D (target_precedes_external)
- adjustment: raw
- n: 1820
- corr / partial: 0.025262400731832196 / 0.025262400731832196
- AUC / AP / Brier: 0.8203466546170727 / 0.9171101045888903 / 0.2719568272560676
- poisson_rate_ratio: None
- negative control: 0.0150593616640398 pass=True
- reverse best / pre-minus-reverse: 0.025262400731832196 / 0.0008243464239609012
- FDR: 0.6819631693902096

## 9. omni:F10_7_missing_ratio x 地震月報（カタログ編）:m3_flag
- lag: -14D (target_precedes_external)
- adjustment: quality
- n: 1813
- corr / partial: 0.0004955725549440567 / 0.0004955725549440567
- AUC / AP / Brier: 0.18289348827079832 / 0.6474998699115797 / 0.2561325842201817
- poisson_rate_ratio: None
- negative control: -0.04492105751049033 pass=False
- reverse best / pre-minus-reverse: 0.000523779531032664 / -0.00010434833583385284
- FDR: 0.9999632851926542

## 10. omni:F10_7_valid_count x 地震月報（カタログ編）:m3_flag
- lag: -14D (target_precedes_external)
- adjustment: quality
- n: 1813
- corr / partial: -0.0004955725549440592 / -0.0004955725549440592
- AUC / AP / Brier: 0.8171065117292017 / 0.9062419778254737 / 0.2454153193421225
- poisson_rate_ratio: None
- negative control: 0.044921057510490324 pass=False
- reverse best / pre-minus-reverse: 0.0005237795310326661 / -0.00010434833583384173
- FDR: 0.9999632851926542

# Failed or Skipped Datasets

- kp_dst / gfz_kp_kyoto_dst: features_ok Dst included
- omni / nasa_cdaweb_omni2_h0_mrg1hr: features_ok 
- glotec / noaa_swpc_glotec: modeled_not_reached Global GloTEC public coverage starts in 2025; requested period has insufficient coverage.
- intermagnet / intermagnet_gin: modeled_not_reached Probe implemented; bulk IAGA/CDF parser deferred.
- jma_geomag / jma_kakioka_geomag: modeled_not_reached Metadata reachable; file-selection parser deferred.
- combined / combined_space_weather_features: features_ok PCA-like proxy features from overlapping fetched source features.

# Interpretation Notes

- external_precedes_target means the external space-weather feature leads the Excel target by the lag.
- target_precedes_external is a reverse-lag/post-reaction comparison.
- Candidate rows are strict filters over a broad multiple-comparison screen; absence of candidates is not a pipeline failure.

# What to Verify Next

- Implement archival GloTEC/US-TEC access for periods before global GloTEC coverage.
- Add robust IAGA/CDF parsing for INTERMAGNET and JMA Kakioka observatory files.
- Add multivariate Ridge/GLM source-group models after univariate coverage is stable.