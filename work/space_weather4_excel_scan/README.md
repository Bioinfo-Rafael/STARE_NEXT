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



はい。結果として精密に書くなら、**「何を入力にして、何を目的変数にして、どの検定をして、どこまで見つかって、何は未検証か」**をかなり明確に分けた方がいい。
以下はそのまま `README` や結果報告に使える粒度で書く。

---

# 結果の要約

本解析では、公開されている宇宙天気・地磁気関連の連続観測データを説明変数とし、STAR-E/NEXTのExcelに整理された地震・測地データのうち、まず取得・整形可能だった **気象庁 地震月報（カタログ編）/ JMA hypocenter catalog** を目的変数として、日次ラグ付き関連を網羅的に探索した。JMA側は「Hypocenters」として年別データが公開されており、JMAページ上では2023年、2022年、2021年、2020年などの年別ファイルが列挙されている。([気象庁データ提供サービス][1])

外部データとしては、Kp/Dst、NASA OMNI、GloTEC、INTERMAGNET/JMA地磁気観測所の4系統を対象にした。ただし、2020–2024の解析期間で実際にモデル化まで到達したのは **Kp/Dst**、**NASA OMNI**、およびそれらから作成した **combined proxy features** であり、GloTEC、INTERMAGNET、JMA地磁気観測所はcoverage不足またはparser未実装により未モデル化である。結果ファイル上でも、Kp/DstとOMNIは2020-01-01から2024-12-31まで1827日分のfeatures_ok、combinedもfeatures_okである一方、GloTECは2025年以降のcoverage問題、INTERMAGNET/JMA地磁気はparser deferredとして modeled_not_reached になっている。

---

# 入力データ

## 説明変数側：宇宙天気・地磁気データ

### 1. Kp/Dst

Kp/Dstは地磁気擾乱の代表的な指標として用いた。KpはGFZ Kp API、DstはKyoto WDCのDst monthly tableから取得する設計である。Kyoto WDCのDstページでは、2020年1月の例として “Hourly Equatorial Dst Values (FINAL)” がnT単位で24時間値として提供されている。([WDC for Geomagnetism][2])

このデータから、Kp平均、Kp最大、Kp rolling mean/max、Dst平均、Dst最小値、Dst storm flag、Kp×Dst interactionなどの日次特徴量を作成した。今回の最終結果では、Kp/Dst群は5,060行のmetricを生成した。

### 2. NASA OMNI / CDAWeb

NASA CDAWebのHAPIサーバー経由で、OMNI2の1時間値データセット `OMNI2_H0_MRG1HR` を取得した。CDAWeb HAPIは時系列データ配信用のREST-like APIで、catalog endpointで利用可能データセットを列挙し、info endpointで各データセットの変数定義を返し、data endpointで時間範囲を指定したデータを取得できる。([CDAWeb][3])

OMNIからは、plasma beta、solar wind speed、Alfvén Mach number、IMF成分、proton density、flow pressure、F10.7、AE/AL/AU系指標などを取得・加工した。各変数について、daily mean/max/min/std、rolling mean/max、差分、anomaly、valid count、missing ratioなどの特徴量を作成した。今回の最終結果では、OMNI群が30,250行のmetricを生成し、最も多くの候補を出した。

### 3. NOAA GloTEC

GloTECは電離圏TECを扱う候補データとしてprobeしたが、指定期間である2020–2024については公開coverage不足のため、モデル化には到達しなかった。結果ファイルでは、GloTECは “Global GloTEC public coverage starts in 2025; requested period has insufficient coverage.” と記録され、modeled_not_reachedである。

### 4. INTERMAGNET / JMA地磁気観測所

INTERMAGNETおよび気象庁地磁気観測所データは、ローカル地磁気観測値として候補に入れたが、今回のMVPではprobeまでで、bulk IAGA/CDF parserやJMA観測所ファイル選択parserは未実装である。そのため、これらも modeled_not_reached であり、結果の主解析にはまだ入っていない。

---

# 目的変数側：JMA地震月報カタログ

目的変数としては、Excel内の地震・測地データ一覧から、まず取得・整形可能だった **気象庁 地震月報（カタログ編）** を用いた。JMAのhypocenter catalogから日次に集約し、以下のようなターゲット変数を作成した。

* `count`: 日次地震数
* `m3_flag`: その日にM3以上の地震があったか
* `m4_flag`: その日にM4以上の地震があったか
* `m5_flag`
* `m6_flag`
* `max_magnitude`
* `energy`
* `mean_depth`
* `shallow_count`
* `deep_count`

今回の結果では、Excel側で実際にmodeled_okになっているのは **気象庁_地震月報_カタログ編** であり、期間は2020-01-01から2024-12-31、1827日分として扱われている。

---

# 解析方法

解析は、外部データ特徴量とJMA地震月報由来ターゲットの全組み合わせについて、日次ラグ付きの探索的スクリーニングとして実施した。

対象ラグは、外部データが地震ターゲットに先行する `external_precedes_target`、同日、逆方向の `target_precedes_external` を含む。結果ファイルでも、`external_precedes_target` は外部宇宙天気特徴量がExcelターゲットに先行すること、`target_precedes_external` は逆ラグ・post-reaction比較であることが明記されている。

各組み合わせについて、主に以下を計算した。

* Pearson correlation
* partial correlation
* logistic regression
* AUC
* average precision
* Brier score
* Poisson regression
* FDR補正
* negative control
* reverse-lag comparison

結果全体では、35,640行のmetricが生成され、strict candidateが1,660行、near-missが2,037行、post-reactionが16,200行、lag asymmetryが3,240行になった。

---

# 発見された主な結果

## 1. OMNIを入れると、多数のstrict candidateが出た

最も大きな変化は、Kp/Dst単独ではほぼ堅牢な前兆候補が残らなかったのに対し、NASA OMNIを加えると **M3 flagを中心に多数のstrict candidateが抽出された**ことである。

特に、OMNIの `plasma_beta_rolling_max_3d` や `plasma_beta_rolling_max_7d`、`plasma_beta_rolling_mean_14d` が、JMA地震月報の `m3_flag` に対して、1日、3日、7日、14日、30日など複数の前兆方向ラグで候補化した。たとえば、`plasma_beta_rolling_max_3d × m3_flag` は30日ラグで external_precedes_target、FDR=0.00028、negative control pass=Trueである。

また、`plasma_beta_rolling_mean_14d × m3_flag` は30日ラグで correlation=-0.270、FDR=6.7e-29、negative control pass=Trueとなっており、今回の中では統計的に非常に強く見える候補の一つである。

## 2. ただし、plasma betaの効果方向は「高いほど地震が増える」ではない

重要なのは、上位のOMNI候補の多くでAUCが0.5未満である点である。たとえば、`plasma_beta_rolling_max_3d × m3_flag` のAUCは0.232であり、そのままの向きでは分類性能が低い。これは、特徴量の符号を反転すると分類性能が高くなる可能性を示している。

したがって、この結果は、

**plasma betaが高いとM3地震が増える**

という意味ではない。むしろ、

**plasma beta系rolling特徴量が、符号付きでM3発生日と対応しており、低い側または反転方向でM3 flagと関連している可能性がある**

と書くべきである。

## 3. M3 flagへの偏りが強い

strict candidateの上位は、ほぼJMA地震月報の `m3_flag` に集中している。Top Findingsの上位10件も、すべてOMNIのplasma beta系特徴量と `m3_flag` の組み合わせである。

これは重要なlimitationである。M3以上の地震は日次ターゲットとして頻度が高く、average precisionやAUCがベースレート・自己相関・カタログ構造の影響を受けやすい可能性がある。そのため、M4/M5以上、地震数、最大マグニチュード、energyなどでも同様に残るかを別途確認する必要がある。

## 4. M4 flagについてはcombined proxyで弱い候補が出た

M4 flagに関しては、combined特徴量 `space_weather_activity_pc1_proxy` が14日ラグで候補として出ている。この結果は、correlation=0.0586、AUC=0.614、FDR=0.0686、negative control pass=Trueであり、効果量は小さいが、M4 targetに対して前兆方向で残った例である。

ただし、combined特徴量は本格的なmultivariate modelではなく、Kp/DstとOMNIのoverlapから作ったproxyである。したがって、これは「4系統統合モデルが成功した」という意味ではなく、**combined proxyがM4 flagに弱く関連した**という限定的な結果である。

## 5. Kp/Dst単独は主役ではなかった

Kp/Dstの上位結果には、Dst storm flag系が高いAUCを示すものがある。しかし、これらはraw featureであり、negative control pass=False、FDRも高い。たとえば、`storm_flag_dst_le_minus100 × m3_flag` はAUC=0.844程度に見えるが、negative control pass=False、FDR=0.533であり、strictな候補としては弱い。

したがって、Kp/Dst単独については、前回の結論と同様に、JMA地震月報に対する堅牢な前兆候補としては現時点で弱い。

---

# 何を発見したと言えるか

現時点で言える発見は、次のように限定して書くのがよい。

> NASA OMNIの太陽風・プラズマ関連特徴量を追加したところ、JMA地震月報カタログの日次M3 flagに対して、plasma beta系のrolling特徴量が複数の前兆方向ラグでstrict candidateとして抽出された。特にplasma_beta_rolling_max_3d、plasma_beta_rolling_max_7d、plasma_beta_rolling_mean_14dは、negative control、FDR補正、reverse-lag比較を通過する候補を多く含んだ。ただし、多くの候補はAUC<0.5の反転方向シグナルであり、M3 flagへの偏り、feature/lag重複、reverse-lagとの差の小ささがあるため、地震予測や因果関係は主張できない。

より短く書くなら、

> 本解析では、Kp/Dst単独では堅牢な前兆候補は得られなかったが、NASA OMNI由来のplasma beta系rolling特徴量が、JMA地震月報のM3 flagに対して前兆方向ラグで多数抽出された。これは太陽風プラズマ状態と日本の小〜中規模地震活動指標の間に統計的同期が存在する可能性を示す探索的結果である。ただし、M3 flagへの偏り、AUC反転、未投入データの存在から、地震予測や因果的解釈はできない。

---

# 今回の結果の限界

最も重要な限界は5つある。

第一に、解析対象のExcel側データは、現時点では **気象庁地震月報カタログ編のみ**である。GNSS、地下水、潮位、地磁気観測所、震度データベースなど、Excelに含まれる他データはまだ本格的にモデル化されていない。

第二に、外部データ4系統を掲げているが、実際にモデル化されたのはKp/Dst、OMNI、combined proxyのみである。GloTEC、INTERMAGNET、JMA地磁気観測所は未検証である。

第三に、strict candidateは1,660行と多いが、これは独立した1,660個の発見ではない。同じ物理量に対するrolling window、lag、targetの違いが大量に含まれている。したがって、次はfeature family単位で集約する必要がある。

第四に、上位候補はM3 flagに偏っている。M4/M5以上やenergy、max_magnitudeでも同じ傾向が残るかはまだ不十分である。

第五に、上位候補の多くはAUCが0.5未満であり、効果方向の解釈に注意が必要である。AUC<0.5の候補は、特徴量の値が高いほどtargetが増えるのではなく、逆方向に効いている可能性がある。

---

# 報告用の完成版文章

以下の文章が一番バランスが良い。

> 本研究では、STAR-E/NEXTの地震・測地データ一覧に対して、公開宇宙天気データを用いたラグ付き相関探索パイプラインを構築した。説明変数として、GFZ/Kyoto由来のKp/Dst、NASA CDAWeb HAPIから取得したOMNI2 1-hour data、NOAA GloTEC、INTERMAGNET/JMA地磁気観測所データを対象とした。現時点でモデル化まで到達したのはKp/Dst、OMNI、およびそれらのcombined proxyであり、GloTECと地磁気観測所データはcoverage不足またはparser未実装のため未検証である。目的変数には、気象庁地震月報カタログ編から日次に集約した地震数、M3/M4/M5/M6発生フラグ、最大マグニチュード、エネルギー、深さ関連指標を用いた。
>
> 解析では、各外部特徴量と各地震ターゲットの組み合わせについて、1日、3日、7日、14日、30日などの前兆方向・同日・逆方向ラグを評価し、相関、partial correlation、logistic/Poissonモデル、AUC、average precision、FDR補正、negative control、reverse-lag comparisonを計算した。その結果、35,640個の組み合わせのうち1,660件がstrict candidateとして抽出された。特にNASA OMNI由来のplasma beta系rolling特徴量が、JMA地震月報のM3 flagに対して複数の前兆方向ラグで抽出された。たとえば、plasma_beta_rolling_max_3dおよびplasma_beta_rolling_mean_14dは、negative controlおよびFDR補正を通過した。ただし、多くの候補はM3 flagに偏っており、AUC<0.5の反転方向シグナルを含む。また、GloTECや地磁気観測所データは未検証であり、Excel内のGNSS・地下水・潮位・震度データも未モデル化である。したがって、本結果は地震予測や因果関係を示すものではなく、太陽風プラズマ状態と日本の地震活動指標との間に探索的な統計的関連が見られた、という段階の結果である。

これならかなり正確。
「発見」としては **OMNI plasma beta系rolling特徴量がM3 flagに多数残った**、でも「結論」としては **地震予測ではなく探索的関連**に留めるのが安全。

[1]: https://www.data.jma.go.jp/eqev/data/bulletin/hypo_e.html "Japan Meteorological Agency | Hypocenters"
[2]: https://wdc.kugi.kyoto-u.ac.jp/dst_final/202001/index.html "Final Dst Index Monthly Plot and Table"
[3]: https://cdaweb.gsfc.nasa.gov/hapi "cdaweb.gsfc.nasa.gov"

