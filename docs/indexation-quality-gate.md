# China EV Mart Indexation Quality Gate

> 生成：2026-10-24 ｜ 车辆总数：517 ｜ 工具：scripts/quality-gate.mjs（`npm run quality:gate`）
> 本报告仅产出不完整清单，**不自动 noindex**（无既有政策支持）。

## 五门槛通过率

| Gate | 通过 | 未通过 | 说明 |
|---|---|---|---|
| identity | 517 | 0 | vehicle_id/model/slug/title/publishedDate 完整 |
| brand | 517 | 0 | brand 在 brand-master 且品牌页存在 |
| powertrain | 516 | 1 | 受控词表内且非 Unknown |
| specs | 444 | 73 | price/range/battery/body_type/motor_power 有效 |
| source | 517 | 0 | master source/source_url + md data_source 存在 |

## 不完整记录清单（73 台）

- [aeolus-huge](https://chinaevmart.com/vehicles/aeolus-huge/) (aeolus)
  - specs: range 全空
- [aeolus-mage](https://chinaevmart.com/vehicles/aeolus-mage/) (aeolus)
  - specs: range 全空; battery_kwh 空
- [changan-cs75](https://chinaevmart.com/vehicles/changan-cs75/) (changan)
  - specs: range 全空; battery_kwh 空
- [changan-nevo-lamore](https://chinaevmart.com/vehicles/changan-nevo-lamore/) (changan)
  - specs: range 全空; battery_kwh 空; motor_power_kw 空
- [changan-x5-plus](https://chinaevmart.com/vehicles/changan-x5-plus/) (changan)
  - specs: range 全空; battery_kwh 空; motor_power_kw 空
- [gac-motor-emkoo](https://chinaevmart.com/vehicles/gac-motor-emkoo/) (gac-motor)
  - specs: range 全空; battery_kwh 空
- [gac-motor-empow](https://chinaevmart.com/vehicles/gac-motor-empow/) (gac-motor)
  - specs: range 全空
- [gac-motor-gs8](https://chinaevmart.com/vehicles/gac-motor-gs8/) (gac-motor)
  - specs: range 全空; battery_kwh 空
- [geely-galaxy-xingrui-l](https://chinaevmart.com/vehicles/geely-galaxy-xingrui-l/) (geely-galaxy)
  - specs: range 全空; battery_kwh 空
- [haval-jolion-pro](https://chinaevmart.com/vehicles/haval-jolion-pro/) (haval)
  - specs: range 全空; battery_kwh 空
- [haval-shenshou](https://chinaevmart.com/vehicles/haval-shenshou/) (haval)
  - specs: range 全空
- [hongqi-guoya](https://chinaevmart.com/vehicles/hongqi-guoya/) (hongqi)
  - powertrain: Unknown（无法索引分类）
  - specs: range 全空; battery_kwh 空
- [wuling-asta](https://chinaevmart.com/vehicles/wuling-asta/) (wuling)
  - specs: range 全空; battery_kwh 空
- [wuling-jiachen](https://chinaevmart.com/vehicles/wuling-jiachen/) (wuling)
  - specs: range 全空; battery_kwh 空
- [wuling-nebula](https://chinaevmart.com/vehicles/wuling-nebula/) (wuling)
  - specs: range 全空; battery_kwh 空
- [wuling-victory](https://chinaevmart.com/vehicles/wuling-victory/) (wuling)
  - specs: range 全空; battery_kwh 空
- [byd-qin-max-ev](https://chinaevmart.com/vehicles/byd-qin-max-ev/) (byd)
  - specs: range 全空; battery_kwh 空
- [byd-qin-max-dm-i](https://chinaevmart.com/vehicles/byd-qin-max-dm-i/) (byd)
  - specs: battery_kwh 空; motor_power_kw 空
- [geely-galaxy-starshine-7](https://chinaevmart.com/vehicles/geely-galaxy-starshine-7/) (geely-galaxy)
  - specs: battery_kwh 空; motor_power_kw 空
- [geely-galaxy-starship-7-ev](https://chinaevmart.com/vehicles/geely-galaxy-starship-7-ev/) (geely-galaxy)
  - specs: battery_kwh 空
- [chery-fulwin-a8l](https://chinaevmart.com/vehicles/chery-fulwin-a8l/) (chery-fulwin)
  - specs: motor_power_kw 空
- [chery-fulwin-t6](https://chinaevmart.com/vehicles/chery-fulwin-t6/) (chery-fulwin)
  - specs: range 全空; battery_kwh 空; motor_power_kw 空
- [chery-fulwin-t9l](https://chinaevmart.com/vehicles/chery-fulwin-t9l/) (chery-fulwin)
  - specs: battery_kwh 空
- [chery-fulwin-x3](https://chinaevmart.com/vehicles/chery-fulwin-x3/) (chery-fulwin)
  - specs: range 全空; battery_kwh 空; motor_power_kw 空
- [chery-fulwin-x3-plus](https://chinaevmart.com/vehicles/chery-fulwin-x3-plus/) (chery-fulwin)
  - specs: battery_kwh 空; motor_power_kw 空
- [chery-new-energy-qq3](https://chinaevmart.com/vehicles/chery-new-energy-qq3/) (chery-new-energy)
  - specs: battery_kwh 空
- [exeed-et5](https://chinaevmart.com/vehicles/exeed-et5/) (exeed)
  - specs: battery_kwh 空
- [jetour-shanhai-l9](https://chinaevmart.com/vehicles/jetour-shanhai-l9/) (jetour)
  - specs: motor_power_kw 空
- [icaur-03t](https://chinaevmart.com/vehicles/icaur-03t/) (icaur)
  - specs: range 全空; battery_kwh 空; motor_power_kw 空
- [changan-cs55-plus-hev](https://chinaevmart.com/vehicles/changan-cs55-plus-hev/) (changan)
  - specs: range 全空
- [changan-cs75-plus-hev](https://chinaevmart.com/vehicles/changan-cs75-plus-hev/) (changan)
  - specs: range 全空; battery_kwh 空
- [changan-eado-hev](https://chinaevmart.com/vehicles/changan-eado-hev/) (changan)
  - specs: range 全空; battery_kwh 空
- [changan-uni-v-hev](https://chinaevmart.com/vehicles/changan-uni-v-hev/) (changan)
  - specs: range 全空
- [xpeng-g9l](https://chinaevmart.com/vehicles/xpeng-g9l/) (xpeng)
  - specs: battery_kwh 空; motor_power_kw 空
- [xpeng-mona-l03](https://chinaevmart.com/vehicles/xpeng-mona-l03/) (xpeng)
  - specs: battery_kwh 空
- [leapmotor-d99](https://chinaevmart.com/vehicles/leapmotor-d99/) (leapmotor)
  - specs: motor_power_kw 空
- [xiaomi-skynomad-n90](https://chinaevmart.com/vehicles/xiaomi-skynomad-n90/) (xiaomi)
  - specs: motor_power_kw 空
- [aito-m6](https://chinaevmart.com/vehicles/aito-m6/) (aito)
  - specs: motor_power_kw 空
- [aito-m9-ultimate](https://chinaevmart.com/vehicles/aito-m9-ultimate/) (aito)
  - specs: battery_kwh 空; motor_power_kw 空
- [dongfeng-epi-m8](https://chinaevmart.com/vehicles/dongfeng-epi-m8/) (dongfeng-e)
  - specs: range 全空; battery_kwh 空; motor_power_kw 空
- [dongfeng-epi-007-plus](https://chinaevmart.com/vehicles/dongfeng-epi-007-plus/) (dongfeng-e)
  - specs: range 全空; battery_kwh 空; motor_power_kw 空
- [forthing-xinghai-v6-plus](https://chinaevmart.com/vehicles/forthing-xinghai-v6-plus/) (forthing)
  - specs: range 全空; battery_kwh 空; motor_power_kw 空
- [forthing-thunder](https://chinaevmart.com/vehicles/forthing-thunder/) (forthing)
  - specs: battery_kwh 空
- [voyah-passion-l](https://chinaevmart.com/vehicles/voyah-passion-l/) (voyah)
  - specs: motor_power_kw 空
- [hongqi-tiangong-06](https://chinaevmart.com/vehicles/hongqi-tiangong-06/) (hongqi)
  - specs: battery_kwh 空
- [haval-xiaolong-max](https://chinaevmart.com/vehicles/haval-xiaolong-max/) (haval)
  - specs: battery_kwh 空
- [ora-5](https://chinaevmart.com/vehicles/ora-5/) (ora)
  - specs: battery_kwh 空; motor_power_kw 空
- [jac-ieva50](https://chinaevmart.com/vehicles/jac-ieva50/) (jac)
  - specs: range 全空
- [jmc-yichi-ev3](https://chinaevmart.com/vehicles/jmc-yichi-ev3/) (jmc)
  - specs: range 全空; battery_kwh 空; motor_power_kw 空
- [jmc-yi-chi-05s](https://chinaevmart.com/vehicles/jmc-yi-chi-05s/) (jmc)
  - specs: battery_kwh 空; motor_power_kw 空
- [jmc-yi-chi-06](https://chinaevmart.com/vehicles/jmc-yi-chi-06/) (jmc)
  - specs: range 全空; battery_kwh 空; motor_power_kw 空
- [aion-v-plus](https://chinaevmart.com/vehicles/aion-v-plus/) (aion)
  - specs: range 全空; battery_kwh 空
- [hyptec-s600](https://chinaevmart.com/vehicles/hyptec-s600/) (hyptec)
  - specs: battery_kwh 空
- [gac-motor-xiangwang-s7](https://chinaevmart.com/vehicles/gac-motor-xiangwang-s7/) (gac-motor)
  - specs: motor_power_kw 空
- [gac-motor-xiangwang-m8](https://chinaevmart.com/vehicles/gac-motor-xiangwang-m8/) (gac-motor)
  - specs: range 全空; battery_kwh 空; motor_power_kw 空
- [roewe-r7](https://chinaevmart.com/vehicles/roewe-r7/) (roewe)
  - specs: range 全空
- [roewe-imax8-dmh](https://chinaevmart.com/vehicles/roewe-imax8-dmh/) (roewe)
  - specs: range 全空; battery_kwh 空; motor_power_kw 空
- [im-ls8](https://chinaevmart.com/vehicles/im-ls8/) (im)
  - specs: range 全空; battery_kwh 空; motor_power_kw 空
- [maxus-mifa-7-phev](https://chinaevmart.com/vehicles/maxus-mifa-7-phev/) (maxus)
  - specs: range 全空
- [maxus-mifa-9-phev](https://chinaevmart.com/vehicles/maxus-mifa-9-phev/) (maxus)
  - specs: range 全空; battery_kwh 空; motor_power_kw 空
- [wuling-starlight-560](https://chinaevmart.com/vehicles/wuling-starlight-560/) (wuling)
  - specs: motor_power_kw 空
- [geometry-e](https://chinaevmart.com/vehicles/geometry-e/) (geometry)
  - specs: range 全空
- [dayun-y7](https://chinaevmart.com/vehicles/dayun-y7/) (dayun)
  - specs: battery_kwh 空
- [cowin-kunlun-ihd](https://chinaevmart.com/vehicles/cowin-kunlun-ihd/) (cowin)
  - specs: range 全空; battery_kwh 空
- [seres-sf5](https://chinaevmart.com/vehicles/seres-sf5/) (seres)
  - specs: range 全空; motor_power_kw 空
- [landian-e5](https://chinaevmart.com/vehicles/landian-e5/) (landian)
  - specs: battery_kwh 空
- [jac-x8-ejia](https://chinaevmart.com/vehicles/jac-x8-ejia/) (jac)
  - specs: motor_power_kw 空
- [chery-tiggo-8-pro-new-energy](https://chinaevmart.com/vehicles/chery-tiggo-8-pro-new-energy/) (chery)
  - specs: battery_kwh 空
- [chery-explore-06-c-dm](https://chinaevmart.com/vehicles/chery-explore-06-c-dm/) (chery)
  - specs: motor_power_kw 空
- [kaicene-changxing-ev](https://chinaevmart.com/vehicles/kaicene-changxing-ev/) (kaicene)
  - specs: range 全空; battery_kwh 空
- [oshan-keshan-ev](https://chinaevmart.com/vehicles/oshan-keshan-ev/) (oshan)
  - specs: range 全空
- [mg-pilot-phev](https://chinaevmart.com/vehicles/mg-pilot-phev/) (mg)
  - specs: motor_power_kw 空
- [jac-ieva60](https://chinaevmart.com/vehicles/jac-ieva60/) (jac)
  - specs: motor_power_kw 空

## 建议（非阻塞）

- **specs**: range 全空的车辆建议补充 CLTC/WLTP 数据或标注 Unknown
- **powertrain**: Unknown powertrain 车辆标注需人工查证（如 Hongqi Guoya）

## P2 发布前检查（⑤ conflict / ⑥ canonical / ⑦ structured data）

- ⑤ conflict 未解决（无 note）：**10**
- ⑤ conflict 已标注（有 note，仍待人工）：**6**
- ⑥ canonical 域异常：**0**
- ⑦ JSON-LD 虚构字段：**0**
- conflict 未解决项：denza-z9-gt-dm-i.type、denza-n8l.range、ora-lightning-cat.range、ora-lightning-cat.battery、zeekr-007-gt.type、geometry-a.battery、geometry-a.motor、lynk-co-07.motor、aion-lx-plus.range、avatr-06t.type
