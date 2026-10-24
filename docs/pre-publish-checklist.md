# China EV Mart — 发布前检查单 (Pre-publish Checklist)

> 生成：2026-10-24 ｜ 工具：`npm run gate`（scripts/pre-publish-gate.mjs）
> 单一真源：`src/content/vehicles/*.md` frontmatter（**不读** 陈旧的 `src/data/*-master.json`）。
> 纪律：未知/未核验数值**一律 N/A 或 待核验**，绝不静默填充。

## 检查项

| # | 检查 | 判定 |
|---|---|---|
| ① | 车型版本/trim 一致性 | trim 有值必须可定位年款；trim 不得横跨与 powertrain 字段矛盾的动力形式 |
| ② | 参数单位规范 | 数值字段必须为裸数字，单位由字段名承载（kg/kWh/mm/kW/Nm 枚举）；未知数值字段告警 |
| ③ | 测试标准标注 | 续航值必须归属 CLTC/WLTP/EPA/NEDC；range_long_km 无标准字段 = 阻断 |
| ④ | 来源与价格日期 | data_source + data_updated 必填；data_updated 须 YYYY-MM-DD 且非未来 |
| ⑤ | conflict 拦截 | parameter-verification.json 的 conflict 必须人工处理或带 note 明确标注 |
| ⑥ | canonical 域 | 四处 canonical 来源统一为 https://chinaevmart.com |
| ⑦ | 结构化数据 | JSON-LD 无虚构字段（rating/review/award/sku 等一律禁止） |
| ⑧ | 高风险字段人工审核 | 价格/续航/认证/HS Code：有值必须带来源+日期+核验状态；否则 N/A |

## 基线结果

- 车型总数：**517**
- PASS（零阻断）：**517**
- BLOCK（≥1 阻断）：**0**
- 仅 WARN（可发布但待复核）：**89**
- 完全 clean：**428**
- 阻断项合计：**0** ｜ 告警项合计：**334**

## 待人工清单（conflict + 高风险未核验）

- conflict 单元：**16**（已带 note 16 / 未带 note 0）
- 高风险字段未核验（unverifiable/partial）：**237**
- 高风险字段缺来源/日期：**0**

## 阻断 (block)（0）


## 告警 (warn)（334）

- [① trim/version] **aion-lx**: trim present but model_year missing (version unpinned)
- [① trim/version] **aion-rt**: trim present but model_year missing (version unpinned)
- [① trim/version] **aion-y**: trim present but model_year missing (version unpinned)
- [① trim/version] **aito-m7**: trim present but model_year missing (version unpinned)
- [① trim/version] **aito-m8-erev**: trim present but model_year missing (version unpinned)
- [① trim/version] **aito-m8**: trim present but model_year missing (version unpinned)
- [① trim/version] **aito-m9-erev**: trim present but model_year missing (version unpinned)
- [① trim/version] **aito-m9-ultimate**: trim present but model_year missing (version unpinned)
- [① trim/version] **aito-m9**: trim present but model_year missing (version unpinned)
- [① trim/version] **byd-atto-3**: trim present but model_year missing (version unpinned)
- [① trim/version] **byd-dolphin**: trim present but model_year missing (version unpinned)
- [① trim/version] **byd-e2**: trim present but model_year missing (version unpinned)
- [① trim/version] **byd-han**: trim present but model_year missing (version unpinned)
- [① trim/version] **byd-qin-l**: trim present but model_year missing (version unpinned)
- [① trim/version] **byd-qin-plus**: trim present but model_year missing (version unpinned)
- [① trim/version] **byd-seagull**: trim present but model_year missing (version unpinned)
- [① trim/version] **byd-seal**: trim present but model_year missing (version unpinned)
- [① trim/version] **byd-song-plus**: trim present but model_year missing (version unpinned)
- [① trim/version] **byd-tang**: trim present but model_year missing (version unpinned)
- [① trim/version] **byd-yuan-up**: trim present but model_year missing (version unpinned)
- [① trim/version] **changan-nevo-a07**: trim present but model_year missing (version unpinned)
- [① trim/version] **changan-nevo-lumin**: trim present but model_year missing (version unpinned)
- [① trim/version] **denza-d9-dm-i**: trim present but model_year missing (version unpinned)
- [① trim/version] **denza-d9**: trim present but model_year missing (version unpinned)
- [① trim/version] **denza-n9**: trim present but model_year missing (version unpinned)
- [① trim/version] **denza-z9-gt**: trim present but model_year missing (version unpinned)
- [① trim/version] **denza-z9**: trim present but model_year missing (version unpinned)
- [① trim/version] **fangchengbao-bao-5**: trim present but model_year missing (version unpinned)
- [① trim/version] **fangchengbao-bao-8**: trim present but model_year missing (version unpinned)
- [① trim/version] **geely-galaxy-e5**: trim present but model_year missing (version unpinned)
- [① trim/version] **geely-galaxy-l6**: trim present but model_year missing (version unpinned)
- [① trim/version] **geely-galaxy-l7**: trim present but model_year missing (version unpinned)
- [① trim/version] **geely-galaxy-starshine-6**: trim present but model_year missing (version unpinned)
- [① trim/version] **hongqi-e-hs9**: trim present but model_year missing (version unpinned)
- [① trim/version] **hongqi-guoya**: trim present but model_year missing (version unpinned)
- [① trim/version] **hongqi-hq9**: trim present but model_year missing (version unpinned)
- [① trim/version] **leapmotor-c11**: trim present but model_year missing (version unpinned)
- [① trim/version] **leapmotor-c16**: trim present but model_year missing (version unpinned)
- [① trim/version] **leapmotor-t03**: trim present but model_year missing (version unpinned)
- [① trim/version] **li-auto-i8**: trim present but model_year missing (version unpinned)
- [① trim/version] **li-auto-l7**: trim present but model_year missing (version unpinned)
- [① trim/version] **li-auto-l8**: trim present but model_year missing (version unpinned)
- [① trim/version] **li-auto-l9**: trim present but model_year missing (version unpinned)
- [① trim/version] **li-auto-mega**: trim present but model_year missing (version unpinned)
- [① trim/version] **mg-4**: trim present but model_year missing (version unpinned)
- [① trim/version] **nio-ec6**: trim present but model_year missing (version unpinned)
- [① trim/version] **nio-ec7**: trim present but model_year missing (version unpinned)
- [① trim/version] **nio-es6**: trim present but model_year missing (version unpinned)
- [① trim/version] **nio-es7**: trim present but model_year missing (version unpinned)
- [① trim/version] **nio-es8**: trim present but model_year missing (version unpinned)
- [① trim/version] **nio-es9**: trim present but model_year missing (version unpinned)
- [① trim/version] **nio-et5**: trim present but model_year missing (version unpinned)
- [① trim/version] **nio-et7**: trim present but model_year missing (version unpinned)
- [① trim/version] **nio-et9**: trim present but model_year missing (version unpinned)
- [① trim/version] **tank-300**: trim present but model_year missing (version unpinned)
- [① trim/version] **tank-400**: trim present but model_year missing (version unpinned)
- [① trim/version] **tank-500**: trim present but model_year missing (version unpinned)
- [① trim/version] **tank-700**: trim present but model_year missing (version unpinned)
- [① trim/version] **voyah-dream-phev**: trim present but model_year missing (version unpinned)
- [① trim/version] **voyah-dream**: trim present but model_year missing (version unpinned)
- [① trim/version] **voyah-titan**: trim present but model_year missing (version unpinned)
- [① trim/version] **wuling-hongguang-mini-ev**: trim present but model_year missing (version unpinned)
- [① trim/version] **wuling-starlight-s**: trim present but model_year missing (version unpinned)
- [① trim/version] **wuling-starlight**: trim present but model_year missing (version unpinned)
- [① trim/version] **xiaomi-su7-ultra**: trim present but model_year missing (version unpinned)
- [① trim/version] **xiaomi-su7**: trim present but model_year missing (version unpinned)
- [① trim/version] **xiaomi-yu7-gt**: trim present but model_year missing (version unpinned)
- [① trim/version] **xiaomi-yu7**: trim present but model_year missing (version unpinned)
- [① trim/version] **xpeng-g9**: trim present but model_year missing (version unpinned)
- [① trim/version] **xpeng-p7**: trim present but model_year missing (version unpinned)
- [① trim/version] **xpeng-x9**: trim present but model_year missing (version unpinned)
- [① trim/version] **yangwang-u7**: trim present but model_year missing (version unpinned)
- [① trim/version] **yangwang-u8**: trim present but model_year missing (version unpinned)
- [① trim/version] **yangwang-u8l**: trim present but model_year missing (version unpinned)
- [① trim/version] **zeekr-001**: trim present but model_year missing (version unpinned)
- [① trim/version] **zeekr-007-gt**: trim present but model_year missing (version unpinned)
- [① trim/version] **zeekr-007**: trim present but model_year missing (version unpinned)
- [① trim/version] **zeekr-009**: trim present but model_year missing (version unpinned)
- [① trim/version] **zeekr-8x**: trim present but model_year missing (version unpinned)
- [① trim/version] **zeekr-9x**: trim present but model_year missing (version unpinned)
- [① trim/version] **zeekr-mix**: trim present but model_year missing (version unpinned)
- [⑤ conflict] **hongqi-guoya**: param motor: conflict documented (note present) — still pending manual resolution
- [⑤ conflict] **yangwang-u8l**: param range: conflict documented (note present) — still pending manual resolution
- [⑤ conflict] **yangwang-u8l**: param battery: conflict documented (note present) — still pending manual resolution
- [⑤ conflict] **nio-et9**: param battery: conflict documented (note present) — still pending manual resolution
- [⑤ conflict] **nio-et9**: param type: conflict documented (note present) — still pending manual resolution
- [⑤ conflict] **maextro-s800**: param battery: conflict documented (note present) — still pending manual resolution
- [⑤ conflict] **denza-z9-gt-dm-i**: param type: conflict documented (note present) — still pending manual resolution
- [⑤ conflict] **denza-n8l**: param range: conflict documented (note present) — still pending manual resolution
- [⑤ conflict] **ora-lightning-cat**: param range: conflict documented (note present) — still pending manual resolution
- [⑤ conflict] **ora-lightning-cat**: param battery: conflict documented (note present) — still pending manual resolution
- [⑤ conflict] **zeekr-007-gt**: param type: conflict documented (note present) — still pending manual resolution
- [⑤ conflict] **geometry-a**: param battery: conflict documented (note present) — still pending manual resolution
- [⑤ conflict] **geometry-a**: param motor: conflict documented (note present) — still pending manual resolution
- [⑤ conflict] **lynk-co-07**: param motor: conflict documented (note present) — still pending manual resolution
- [⑤ conflict] **aion-lx-plus**: param range: conflict documented (note present) — still pending manual resolution
- [⑤ conflict] **avatr-06t**: param type: conflict documented (note present) — still pending manual resolution
- [⑧ high-risk] **aion-y.price_usd**: Price marked partial — 待核验 (pending manual review)
- [⑧ high-risk] **aion-y.price_type**: Price marked partial — 待核验 (pending manual review)
- [⑧ high-risk] **aion-y.currency**: Price marked partial — 待核验 (pending manual review)
- [⑧ high-risk] **aion-y.range_cltc_km**: Range marked partial — 待核验 (pending manual review)
- [⑧ high-risk] **aion-y.certification_notes**: Certification marked partial — 待核验 (pending manual review)
- [⑧ high-risk] **aion-y.hs_code**: HS Code marked partial — 待核验 (pending manual review)
- [⑧ high-risk] **avatr-12.price_usd**: Price marked partial — 待核验 (pending manual review)
- [⑧ high-risk] **avatr-12.price_type**: Price marked partial — 待核验 (pending manual review)
- [⑧ high-risk] **avatr-12.currency**: Price marked partial — 待核验 (pending manual review)
- [⑧ high-risk] **avatr-12.range_cltc_km**: Range marked partial — 待核验 (pending manual review)
- [⑧ high-risk] **avatr-12.certification_notes**: Certification marked partial — 待核验 (pending manual review)
- [⑧ high-risk] **avatr-12.hs_code**: HS Code marked partial — 待核验 (pending manual review)
- [⑧ high-risk] **bestune-pony.price_usd**: Price marked partial — 待核验 (pending manual review)
- [⑧ high-risk] **bestune-pony.price_type**: Price marked partial — 待核验 (pending manual review)
- [⑧ high-risk] **bestune-pony.currency**: Price marked partial — 待核验 (pending manual review)
- [⑧ high-risk] **bestune-pony.range_cltc_km**: Range marked partial — 待核验 (pending manual review)
- [⑧ high-risk] **bestune-pony.certification_notes**: Certification marked partial — 待核验 (pending manual review)
- [⑧ high-risk] **bestune-pony.hs_code**: HS Code marked partial — 待核验 (pending manual review)
- [⑧ high-risk] **byd-atto-3.price_usd**: Price marked partial — 待核验 (pending manual review)
- [⑧ high-risk] **byd-atto-3.price_type**: Price marked partial — 待核验 (pending manual review)
- [⑧ high-risk] **byd-atto-3.currency**: Price marked partial — 待核验 (pending manual review)
- [⑧ high-risk] **byd-atto-3.range_cltc_km**: Range marked partial — 待核验 (pending manual review)
- [⑧ high-risk] **byd-atto-3.range_wltp_km**: Range marked partial — 待核验 (pending manual review)
- [⑧ high-risk] **byd-atto-3.certification_notes**: Certification marked partial — 待核验 (pending manual review)
- [⑧ high-risk] **byd-atto-3.hs_code**: HS Code marked partial — 待核验 (pending manual review)
- [⑧ high-risk] **byd-dolphin.price_usd**: Price marked partial — 待核验 (pending manual review)
- [⑧ high-risk] **byd-dolphin.price_type**: Price marked partial — 待核验 (pending manual review)
- [⑧ high-risk] **byd-dolphin.currency**: Price marked partial — 待核验 (pending manual review)
- [⑧ high-risk] **byd-dolphin.range_cltc_km**: Range marked partial — 待核验 (pending manual review)
- [⑧ high-risk] **byd-dolphin.range_wltp_km**: Range marked partial — 待核验 (pending manual review)
- [⑧ high-risk] **byd-dolphin.certification_notes**: Certification marked partial — 待核验 (pending manual review)
- [⑧ high-risk] **byd-dolphin.hs_code**: HS Code marked partial — 待核验 (pending manual review)
- [⑧ high-risk] **byd-han.price_usd**: Price marked partial — 待核验 (pending manual review)
- [⑧ high-risk] **byd-han.price_type**: Price marked partial — 待核验 (pending manual review)
- [⑧ high-risk] **byd-han.currency**: Price marked partial — 待核验 (pending manual review)
- [⑧ high-risk] **byd-han.range_cltc_km**: Range marked partial — 待核验 (pending manual review)
- [⑧ high-risk] **byd-han.range_wltp_km**: Range marked partial — 待核验 (pending manual review)
- [⑧ high-risk] **byd-han.range_long_km**: Range marked partial — 待核验 (pending manual review)
- [⑧ high-risk] **byd-han.certification_notes**: Certification marked partial — 待核验 (pending manual review)
- [⑧ high-risk] **byd-han.hs_code**: HS Code marked partial — 待核验 (pending manual review)
- [⑧ high-risk] **byd-qin-l-dm-i.price_usd**: Price marked unverifiable — 待核验 (pending manual review)
- [⑧ high-risk] **byd-qin-l-dm-i.price_type**: Price marked unverifiable — 待核验 (pending manual review)
- [⑧ high-risk] **byd-qin-l-dm-i.currency**: Price marked unverifiable — 待核验 (pending manual review)
- [⑧ high-risk] **byd-qin-l-dm-i.range_cltc_km**: Range marked unverifiable — 待核验 (pending manual review)
- [⑧ high-risk] **byd-qin-l-dm-i.certification_notes**: Certification marked unverifiable — 待核验 (pending manual review)
- [⑧ high-risk] **byd-qin-l-dm-i.hs_code**: HS Code marked unverifiable — 待核验 (pending manual review)
- [⑧ high-risk] **byd-seagull.price_usd**: Price marked partial — 待核验 (pending manual review)
- [⑧ high-risk] **byd-seagull.price_type**: Price marked partial — 待核验 (pending manual review)
- [⑧ high-risk] **byd-seagull.currency**: Price marked partial — 待核验 (pending manual review)
- [⑧ high-risk] **byd-seagull.range_cltc_km**: Range marked partial — 待核验 (pending manual review)
- [⑧ high-risk] **byd-seagull.range_wltp_km**: Range marked partial — 待核验 (pending manual review)
- [⑧ high-risk] **byd-seagull.certification_notes**: Certification marked partial — 待核验 (pending manual review)
- [⑧ high-risk] **byd-seagull.hs_code**: HS Code marked partial — 待核验 (pending manual review)
- [⑧ high-risk] **byd-seal.price_usd**: Price marked partial — 待核验 (pending manual review)
- [⑧ high-risk] **byd-seal.price_type**: Price marked partial — 待核验 (pending manual review)
- [⑧ high-risk] **byd-seal.currency**: Price marked partial — 待核验 (pending manual review)
- [⑧ high-risk] **byd-seal.range_cltc_km**: Range marked partial — 待核验 (pending manual review)
- [⑧ high-risk] **byd-seal.range_wltp_km**: Range marked partial — 待核验 (pending manual review)
- [⑧ high-risk] **byd-seal.certification_notes**: Certification marked partial — 待核验 (pending manual review)
- [⑧ high-risk] **byd-seal.hs_code**: HS Code marked partial — 待核验 (pending manual review)
- [⑧ high-risk] **byd-sealion-07.price_usd**: Price marked partial — 待核验 (pending manual review)
- [⑧ high-risk] **byd-sealion-07.price_type**: Price marked partial — 待核验 (pending manual review)
- [⑧ high-risk] **byd-sealion-07.currency**: Price marked partial — 待核验 (pending manual review)
- [⑧ high-risk] **byd-sealion-07.range_cltc_km**: Range marked partial — 待核验 (pending manual review)
- [⑧ high-risk] **byd-sealion-07.range_wltp_km**: Range marked partial — 待核验 (pending manual review)
- [⑧ high-risk] **byd-sealion-07.certification_notes**: Certification marked partial — 待核验 (pending manual review)
- [⑧ high-risk] **byd-sealion-07.hs_code**: HS Code marked partial — 待核验 (pending manual review)
- [⑧ high-risk] **byd-song-plus-dm-i.price_usd**: Price marked partial — 待核验 (pending manual review)
- [⑧ high-risk] **byd-song-plus-dm-i.price_type**: Price marked partial — 待核验 (pending manual review)
- [⑧ high-risk] **byd-song-plus-dm-i.currency**: Price marked partial — 待核验 (pending manual review)
- [⑧ high-risk] **byd-song-plus-dm-i.range_cltc_km**: Range marked partial — 待核验 (pending manual review)
- [⑧ high-risk] **byd-song-plus-dm-i.certification_notes**: Certification marked partial — 待核验 (pending manual review)
- [⑧ high-risk] **byd-song-plus-dm-i.hs_code**: HS Code marked partial — 待核验 (pending manual review)
- [⑧ high-risk] **changan-nevo-lamore.price_usd**: Price marked partial — 待核验 (pending manual review)
- [⑧ high-risk] **changan-nevo-lamore.price_type**: Price marked partial — 待核验 (pending manual review)
- [⑧ high-risk] **changan-nevo-lamore.currency**: Price marked partial — 待核验 (pending manual review)
- [⑧ high-risk] **changan-nevo-lamore.certification_notes**: Certification marked partial — 待核验 (pending manual review)
- [⑧ high-risk] **changan-nevo-lamore.hs_code**: HS Code marked partial — 待核验 (pending manual review)
- [⑧ high-risk] **chery-explore-06-c-dm.price_usd**: Price marked unverifiable — 待核验 (pending manual review)
- [⑧ high-risk] **chery-explore-06-c-dm.price_type**: Price marked unverifiable — 待核验 (pending manual review)
- [⑧ high-risk] **chery-explore-06-c-dm.currency**: Price marked unverifiable — 待核验 (pending manual review)
- [⑧ high-risk] **chery-explore-06-c-dm.range_cltc_km**: Range marked unverifiable — 待核验 (pending manual review)
- [⑧ high-risk] **chery-explore-06-c-dm.certification_notes**: Certification marked unverifiable — 待核验 (pending manual review)
- [⑧ high-risk] **chery-explore-06-c-dm.hs_code**: HS Code marked unverifiable — 待核验 (pending manual review)
- [⑧ high-risk] **chery-fulwin-a9.price_usd**: Price marked partial — 待核验 (pending manual review)
- [⑧ high-risk] **chery-fulwin-a9.price_type**: Price marked partial — 待核验 (pending manual review)
- [⑧ high-risk] **chery-fulwin-a9.currency**: Price marked partial — 待核验 (pending manual review)
- [⑧ high-risk] **chery-fulwin-a9.range_cltc_km**: Range marked partial — 待核验 (pending manual review)
- [⑧ high-risk] **chery-fulwin-a9.certification_notes**: Certification marked partial — 待核验 (pending manual review)
- [⑧ high-risk] **chery-fulwin-a9.hs_code**: HS Code marked partial — 待核验 (pending manual review)
- [⑧ high-risk] **chery-new-energy-eq1.price_usd**: Price marked partial — 待核验 (pending manual review)
- [⑧ high-risk] **chery-new-energy-eq1.price_type**: Price marked partial — 待核验 (pending manual review)
- [⑧ high-risk] **chery-new-energy-eq1.currency**: Price marked partial — 待核验 (pending manual review)
- [⑧ high-risk] **chery-new-energy-eq1.range_cltc_km**: Range marked partial — 待核验 (pending manual review)
- [⑧ high-risk] **chery-new-energy-eq1.certification_notes**: Certification marked partial — 待核验 (pending manual review)
- [⑧ high-risk] **chery-new-energy-eq1.hs_code**: HS Code marked partial — 待核验 (pending manual review)
- [⑧ high-risk] **chery-tiggo-9.price_usd**: Price marked partial — 待核验 (pending manual review)
- [⑧ high-risk] **chery-tiggo-9.price_type**: Price marked partial — 待核验 (pending manual review)
- [⑧ high-risk] **chery-tiggo-9.currency**: Price marked partial — 待核验 (pending manual review)
- [⑧ high-risk] **chery-tiggo-9.range_cltc_km**: Range marked partial — 待核验 (pending manual review)
- [⑧ high-risk] **chery-tiggo-9.certification_notes**: Certification marked partial — 待核验 (pending manual review)
- [⑧ high-risk] **chery-tiggo-9.hs_code**: HS Code marked partial — 待核验 (pending manual review)
- [⑧ high-risk] **denza-z9-gt.price_usd**: Price marked partial — 待核验 (pending manual review)
- … 及另外 134 项

