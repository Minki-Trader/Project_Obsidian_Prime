# MT5 Validation Leaderboard

- generated_at_utc: `2026-03-31T16:19:51.345748+00:00`
- scan_root: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages`
- split: `validation`
- sort_by: `return_pct`
- bundle_count: `140`

## Summary

```text
Rank | Stage                            | Run                                                 | LatestAttempt | AttemptStatus | Return% | PF     | MaxDD% | Trades | Ready% | ReadyGap | UnexpectedSkips
-----+----------------------------------+-----------------------------------------------------+---------------+---------------+---------+--------+--------+--------+--------+----------+----------------
1    | 05_optimization                  | 05I_mt5_validation_margin_lightgbm_modelswap_0001   | att_0002      | completed     | 1308.56 | 15.290 | 1.93   | 1554   | 22.26  | 0        | 0              
2    | 05_optimization                  | 05K_mt5_validation_margin_xgboost_modelswap_0001    | att_0002      | completed     | 816.88  | 4.562  | 8.15   | 1394   | 22.26  | 0        | 0              
3    | 05_optimization                  | 05L_rf_margin_swap_0001                             | att_0001      | completed     | 593.44  | 8.435  | 1.63   | 850    | 22.26  | 0        | 0              
4    | 05_optimization                  | 05GK_05dp_dirsplit_l14_s20_riskpct300_0001          | att_0001      | completed     | 522.00  | 1.329  | 34.50  | 425    | 22.26  | 0        | 0              
5    | 05_optimization                  | 05GI_05dp_dirsplit_l13_s17_riskpct300_0001          | att_0001      | completed     | 455.31  | 1.258  | 39.89  | 430    | 22.26  | 0        | 0              
6    | 05_optimization                  | 05M_et_margin_swap_0001                             | att_0001      | completed     | 422.01  | 11.584 | 2.10   | 449    | 22.26  | 0        | 0              
7    | 05_optimization                  | 05GJ_05dp_dirsplit_l12_s18_riskpct300_0001          | att_0001      | completed     | 413.41  | 1.238  | 42.83  | 431    | 22.26  | 0        | 0              
8    | 05_optimization                  | 05GC_05dp_fixed_stop10_riskpct300_brokersl_0001     | att_0001      | completed     | 401.00  | 1.153  | 53.39  | 455    | 22.26  | 0        | 0              
9    | 05_optimization                  | 05GE_05dp_fixed_stop20_riskpct300_brokersl_0001     | att_0001      | completed     | 388.41  | 1.312  | 37.00  | 417    | 22.26  | 0        | 0              
10   | 05_optimization                  | 05GF_05dp_regime085_115_100_150_200_riskpct300_0001 | att_0001      | completed     | 347.49  | 1.242  | 41.02  | 428    | 22.26  | 0        | 0              
11   | 05_optimization                  | 05GG_05dp_regime090_110_090_140_180_riskpct300_0001 | att_0001      | completed     | 339.02  | 1.209  | 38.35  | 435    | 22.26  | 0        | 0              
12   | 05_optimization                  | 05GH_05dp_regime085_120_110_150_220_riskpct300_0001 | att_0001      | completed     | 286.89  | 1.235  | 40.69  | 426    | 22.26  | 0        | 0              
13   | 05_optimization                  | 05GB_05dp_riskpct300_atr14x15_brokersl_0001         | att_0001      | completed     | 264.39  | 1.190  | 39.03  | 432    | 22.26  | 0        | 0              
14   | 05_optimization                  | 05GD_05dp_fixed_stop15_riskpct300_brokersl_0001     | att_0001      | completed     | 264.39  | 1.190  | 39.03  | 432    | 22.26  | 0        | 0              
15   | 06_segmented_risk_validation     | 06A_dirsplit2pct_0001                               | att_0002      | completed     | 249.09  | 1.390  | 24.28  | 425    | 22.26  | 0        | 0              
16   | 05_optimization                  | 05FB_05ca_temp090_margin0675_hold5_0001             | att_0003      | completed     | 124.45  | 1.487  | 13.36  | 475    | 22.26  | 0        | 0              
17   | 05_optimization                  | 05DP_05ca_margin0675_hold5_0001                     | att_0003      | completed     | 122.57  | 1.555  | 12.60  | 405    | 22.26  | 0        | 0              
18   | 05_optimization                  | 05FR_05dp_flatexit052_hold1_0001                    | att_0004      | completed     | 122.57  | 1.555  | 12.60  | 405    | 22.26  | 0        | 0              
19   | 05_optimization                  | 05FS_05dp_flatexit055_hold1_0001                    | att_0004      | completed     | 122.57  | 1.555  | 12.60  | 405    | 22.26  | 0        | 0              
20   | 05_optimization                  | 05FT_05dp_flatexit055_hold2_0001                    | att_0002      | completed     | 122.57  | 1.555  | 12.60  | 405    | 22.26  | 0        | 0              
21   | 05_optimization                  | 05FU_05dp_flatexit058_hold1_0001                    | att_0002      | completed     | 122.57  | 1.555  | 12.60  | 405    | 22.26  | 0        | 0              
22   | 05_optimization                  | 05FV_05dp_flatexit060_hold2_0001                    | att_0002      | completed     | 122.57  | 1.555  | 12.60  | 405    | 22.26  | 0        | 0              
23   | 05_optimization                  | 05FY_05dp_flatexit048_hold1_0001                    | att_0001      | completed     | 122.57  | 1.555  | 12.60  | 405    | 22.26  | 0        | 0              
24   | 05_optimization                  | 05FZ_05dp_flatexit050_hold1_0001                    | att_0001      | completed     | 122.57  | 1.555  | 12.60  | 405    | 22.26  | 0        | 0              
25   | 05_optimization                  | 05FX_05dp_flatexit045_hold1_0001                    | att_0001      | completed     | 122.40  | 1.554  | 12.60  | 405    | 22.26  | 0        | 0              
26   | 05_optimization                  | 05DJ_05bf_margin_hold5_0001                         | att_0002      | completed     | 119.44  | 1.565  | 12.47  | 386    | 22.26  | 0        | 0              
27   | 05_optimization                  | 05EA_05ca_margin0675_hold4_0001                     | att_0003      | completed     | 115.17  | 1.535  | 11.50  | 453    | 22.26  | 0        | 0              
28   | 05_optimization                  | 05DY_05ca_margin06625_hold5_0001                    | att_0003      | completed     | 114.88  | 1.500  | 12.79  | 417    | 22.26  | 0        | 0              
29   | 05_optimization                  | 05DZ_05ca_margin06875_hold5_0001                    | att_0001      | completed     | 114.54  | 1.525  | 12.60  | 396    | 22.26  | 0        | 0              
30   | 05_optimization                  | 05DN_05ca_margin_hold5_0001                         | att_0003      | completed     | 109.31  | 1.502  | 13.22  | 388    | 22.26  | 0        | 0              
31   | 05_optimization                  | 05EM_05dp_short_bias_margin_hold5_0001              | att_0002      | completed     | 109.20  | 1.529  | 13.06  | 356    | 22.26  | 0        | 0              
32   | 05_optimization                  | 05DE_05bb_margin_hold2_0001                         | att_0002      | completed     | 107.68  | 1.476  | 11.34  | 580    | 22.26  | 0        | 0              
33   | 05_optimization                  | 05DX_05ca_margin0650_hold5_0001                     | att_0001      | completed     | 106.70  | 1.445  | 14.81  | 433    | 22.26  | 0        | 0              
34   | 05_optimization                  | 05DQ_05ca_margin0725_hold5_0001                     | att_0003      | completed     | 106.64  | 1.502  | 15.84  | 375    | 22.26  | 0        | 0              
35   | 05_optimization                  | 05EH_05ca_plus_leader_session_margin0675_hold5_0001 | att_0003      | completed     | 106.02  | 1.465  | 14.44  | 406    | 22.26  | 0        | 0              
36   | 05_optimization                  | 05EE_05ca_plus_downside_margin0675_hold5_0001       | att_0003      | completed     | 105.41  | 1.459  | 14.72  | 408    | 22.26  | 0        | 0              
37   | 05_optimization                  | 05DI_05bf_margin_hold4_0001                         | att_0001      | completed     | 104.54  | 1.506  | 11.54  | 427    | 22.26  | 0        | 0              
38   | 05_optimization                  | 05EL_05dp_combo_loose_hold5_0001                    | att_0002      | completed     | 103.33  | 1.458  | 13.75  | 395    | 22.26  | 0        | 0              
39   | 05_optimization                  | 05EF_05ca_plus_leader_margin0675_hold5_0001         | att_0001      | completed     | 102.85  | 1.450  | 14.29  | 405    | 22.26  | 0        | 0              
40   | 05_optimization                  | 05ER_05dp_short_bias_margin_hold4_0001              | att_0002      | completed     | 102.63  | 1.507  | 12.66  | 397    | 22.26  | 0        | 0              
41   | 05_optimization                  | 05DH_05bf_margin_hold2_0001                         | att_0001      | completed     | 102.28  | 1.450  | 12.45  | 576    | 22.26  | 0        | 0              
42   | 05_optimization                  | 05DR_05cc_margin0675_hold5_0001                     | att_0001      | completed     | 102.06  | 1.444  | 14.27  | 408    | 22.26  | 0        | 0              
43   | 05_optimization                  | 05EB_05ca_margin0675_hold6_0001                     | att_0001      | completed     | 100.70  | 1.437  | 14.16  | 373    | 22.26  | 0        | 0              
44   | 05_optimization                  | 05DG_05bb_margin_hold5_0001                         | att_0001      | completed     | 99.73   | 1.449  | 14.83  | 390    | 22.26  | 0        | 0              
45   | 05_optimization                  | 05DL_05cc_margin_hold5_0001                         | att_0003      | completed     | 99.68   | 1.445  | 14.92  | 393    | 22.26  | 0        | 0              
46   | 05_optimization                  | 05ED_05ca_plus_breakout_margin0675_hold5_0001       | att_0001      | completed     | 99.01   | 1.431  | 14.87  | 401    | 22.26  | 0        | 0              
47   | 05_optimization                  | 05ES_05dp_stronger_long_suppression_hold5_0001      | att_0002      | completed     | 96.93   | 1.532  | 13.46  | 309    | 22.26  | 0        | 0              
48   | 05_optimization                  | 05EP_05dp_balanced_tight_margin_hold5_0001          | att_0001      | completed     | 95.91   | 1.521  | 10.79  | 289    | 22.26  | 0        | 0              
49   | 05_optimization                  | 05EC_05ca_plus_volatility_margin0675_hold5_0001     | att_0001      | completed     | 95.75   | 1.413  | 14.79  | 404    | 22.26  | 0        | 0              
50   | 05_optimization                  | 05EG_05ca_plus_session_margin0675_hold5_0001        | att_0001      | completed     | 94.99   | 1.408  | 15.41  | 404    | 22.26  | 0        | 0              
51   | 05_optimization                  | 05FA_05ca_temp115_margin0675_hold5_0001             | att_0003      | completed     | 92.76   | 1.472  | 12.47  | 338    | 22.26  | 0        | 0              
52   | 05_optimization                  | 05EK_05dp_diff_only_hold5_0001                      | att_0001      | completed     | 92.64   | 1.437  | 12.68  | 371    | 22.26  | 0        | 0              
53   | 05_optimization                  | 05DT_05ca_margin0700_hold6_0001                     | att_0001      | completed     | 92.63   | 1.400  | 14.88  | 358    | 22.26  | 0        | 0              
54   | 05_optimization                  | 05DM_05cc_margin_hold4_0001                         | att_0001      | completed     | 92.45   | 1.419  | 14.50  | 435    | 22.26  | 0        | 0              
55   | 05_optimization                  | 05BQ_frontier_vote_w_bf_0001                        | att_0002      | completed     | 92.29   | 1.416  | 10.97  | 491    | 22.26  | 0        | 0              
56   | 05_optimization                  | 05EO_05dp_short_bias_combo_hold5_0001               | att_0001      | completed     | 91.69   | 1.435  | 15.51  | 350    | 22.26  | 0        | 0              
57   | 05_optimization                  | 05DU_05cc_margin0700_hold6_0001                     | att_0001      | completed     | 91.59   | 1.401  | 15.42  | 360    | 22.26  | 0        | 0              
58   | 05_optimization                  | 05ET_05dp_stronger_long_suppression_hold4_0001      | att_0001      | completed     | 91.33   | 1.509  | 13.17  | 346    | 22.26  | 0        | 0              
59   | 05_optimization                  | 05W_no_trend_strength_0001                          | att_0002      | completed     | 91.17   | 1.409  | 11.15  | 493    | 22.26  | 0        | 0              
60   | 05_optimization                  | 05EW_05dp_balanced_tight_combo_hold5_0001           | att_0001      | completed     | 90.54   | 1.499  | 10.66  | 282    | 22.26  | 0        | 0              
61   | 05_optimization                  | 05EV_05dp_short_bias_combo_hold4_0001               | att_0001      | completed     | 90.09   | 1.442  | 13.91  | 384    | 22.26  | 0        | 0              
62   | 05_optimization                  | 05BF_trend_proxy_persistence_volatility_0001        | att_0002      | completed     | 89.42   | 1.401  | 11.95  | 487    | 22.26  | 0        | 0              
63   | 05_optimization                  | 05S_no_price_return_0001                            | att_0001      | completed     | 89.29   | 1.376  | 9.71   | 514    | 22.26  | 0        | 0              
64   | 05_optimization                  | 05BR_frontier_vote_w_bb_bf_0001                     | att_0002      | completed     | 87.63   | 1.394  | 12.17  | 487    | 22.26  | 0        | 0              
65   | 05_optimization                  | 05AI_trend_proxy_light_pb_0001                      | att_0002      | completed     | 86.87   | 1.388  | 11.72  | 485    | 22.26  | 0        | 0              
66   | 05_optimization                  | 05AW_05aj_thr_margin_0001                           | att_0002      | completed     | 86.63   | 1.708  | 10.88  | 245    | 22.26  | 0        | 0              
67   | 05_optimization                  | 05AX_05aj_thr_combo_0001                            | att_0002      | completed     | 86.63   | 1.708  | 10.88  | 245    | 22.26  | 0        | 0              
68   | 05_optimization                  | 05DS_05cc_margin0725_hold5_0001                     | att_0001      | completed     | 86.43   | 1.377  | 16.01  | 382    | 22.26  | 0        | 0              
69   | 05_optimization                  | 05DF_05bb_margin_hold4_0001                         | att_0001      | completed     | 86.25   | 1.401  | 14.66  | 428    | 22.26  | 0        | 0              
70   | 05_optimization                  | 05AP_05w_thr_margin_0001                            | att_0002      | completed     | 86.15   | 1.702  | 10.89  | 250    | 22.26  | 0        | 0              
71   | 05_optimization                  | 05AQ_05w_thr_combo_0001                             | att_0001      | completed     | 86.15   | 1.702  | 10.89  | 250    | 22.26  | 0        | 0              
72   | 05_optimization                  | 05AS_05ai_thr_margin_0001                           | att_0001      | completed     | 85.75   | 1.701  | 10.95  | 244    | 22.26  | 0        | 0              
73   | 05_optimization                  | 05AT_05ai_thr_combo_0001                            | att_0001      | completed     | 85.75   | 1.701  | 10.95  | 244    | 22.26  | 0        | 0              
74   | 05_optimization                  | 05BK_05w_long_bias_margin_0001                      | att_0002      | completed     | 85.58   | 1.861  | 12.07  | 220    | 22.26  | 0        | 0              
75   | 05_optimization                  | 05CA_trend_proxy_persistence_riskoff_0001           | att_0003      | completed     | 84.15   | 1.376  | 12.05  | 488    | 22.26  | 0        | 0              
76   | 05_optimization                  | 05AO_05w_combo_loose_0001                           | att_0001      | completed     | 82.79   | 1.359  | 12.88  | 500    | 22.26  | 0        | 0              
77   | 05_optimization                  | 05EN_05dp_short_bias_diff_hold5_0001                | att_0001      | completed     | 82.05   | 1.409  | 13.97  | 332    | 22.26  | 0        | 0              
78   | 05_optimization                  | 05T_no_ma_trend_0001                                | att_0001      | completed     | 81.25   | 1.532  | 12.39  | 325    | 22.26  | 0        | 0              
79   | 05_optimization                  | 05AV_05ai_combo_loose_0001                          | att_0001      | completed     | 80.51   | 1.350  | 12.90  | 492    | 22.26  | 0        | 0              
80   | 05_optimization                  | 05CC_trend_proxy_persistence_downside_riskoff_0001  | att_0003      | completed     | 78.51   | 1.341  | 12.01  | 495    | 22.26  | 0        | 0              
81   | 05_optimization                  | 05BZ_trend_proxy_persistence_downside_0001          | att_0001      | completed     | 78.35   | 1.339  | 12.27  | 494    | 22.26  | 0        | 0              
82   | 05_optimization                  | 05Z_no_leader_rel_0001                              | att_0001      | completed     | 77.97   | 1.335  | 11.80  | 523    | 22.26  | 0        | 0              
83   | 05_optimization                  | 05BM_05w_balanced_tight_margin_0001                 | att_0002      | completed     | 77.30   | 1.420  | 11.06  | 355    | 22.26  | 0        | 0              
84   | 05_optimization                  | 05AD_drop_di_spread14_0001                          | att_0002      | completed     | 76.55   | 1.309  | 11.15  | 524    | 22.26  | 0        | 0              
85   | 05_optimization                  | 05BB_trend_proxy_persistence_only_0001              | att_0002      | completed     | 75.68   | 1.331  | 12.35  | 490    | 22.26  | 0        | 0              
86   | 05_optimization                  | 05X_no_session_ctx_0001                             | att_0001      | completed     | 75.38   | 1.320  | 11.60  | 499    | 22.26  | 0        | 0              
87   | 05_optimization                  | 05AJ_trend_proxy_light_vb_0001                      | att_0002      | completed     | 75.36   | 1.324  | 12.06  | 492    | 22.26  | 0        | 0              
88   | 05_optimization                  | 05R_semantic_interact_0001                          | att_0002      | completed     | 75.15   | 1.191  | 21.81  | 847    | 22.26  | 0        | 0              
89   | 05_optimization                  | 05BC_trend_proxy_breakout_only_0001                 | att_0001      | completed     | 74.41   | 1.322  | 11.88  | 493    | 22.26  | 0        | 0              
90   | 05_optimization                  | 05BD_trend_proxy_volatility_only_0001               | att_0001      | completed     | 74.30   | 1.316  | 12.81  | 491    | 22.26  | 0        | 0              
91   | 05_optimization                  | 05AF_drop_vortex_indicator_0001                     | att_0001      | completed     | 73.57   | 1.293  | 11.86  | 533    | 22.26  | 0        | 0              
92   | 05_optimization                  | 05CD_trend_proxy_persistence_session_riskoff_0001   | att_0001      | completed     | 73.07   | 1.315  | 12.05  | 489    | 22.26  | 0        | 0              
93   | 05_optimization                  | 05BP_frontier_vote_w_bb_0001                        | att_0001      | completed     | 72.71   | 1.315  | 13.09  | 488    | 22.26  | 0        | 0              
94   | 05_optimization                  | 05BS_frontier_vote_w_bb_ah_0001                     | att_0001      | completed     | 70.77   | 1.306  | 13.03  | 488    | 22.26  | 0        | 0              
95   | 05_optimization                  | 05CB_trend_proxy_persistence_leader_drag_0001       | att_0001      | completed     | 69.21   | 1.293  | 12.11  | 489    | 22.26  | 0        | 0              
96   | 05_optimization                  | 05AZ_05aj_combo_loose_0001                          | att_0001      | completed     | 69.17   | 1.291  | 13.31  | 498    | 22.26  | 0        | 0              
97   | 05_optimization                  | 05EU_05dp_near_short_only_hold5_0001                | att_0001      | completed     | 68.95   | 1.460  | 13.68  | 255    | 22.26  | 0        | 0              
98   | 05_optimization                  | 05D_mt5_validation_diff_tightgap_0001               | att_0002      | completed     | 68.66   | 1.301  | 12.77  | 487    | 22.26  | 0        | 0              
99   | 05_optimization                  | 05BI_05w_short_bias_margin_0001                     | att_0001      | completed     | 68.41   | 1.314  | 14.34  | 446    | 22.26  | 0        | 0              
100  | 05_optimization                  | 05AC_drop_adx14_0001                                | att_0001      | completed     | 68.01   | 1.273  | 11.95  | 532    | 22.26  | 0        | 0              
101  | 03_max_probability_margin        | 03E_mt5_validation_baseline_0001                    | att_0005      | completed     | 67.66   | 1.266  | 12.20  | 530    | 22.26  | 0        | 0              
102  | 05_optimization                  | 05H_mt5_validation_diff_07000_0001                  | att_0001      | completed     | 67.62   | 1.251  | 12.54  | 588    | 22.26  | 0        | 0              
103  | 05_optimization                  | 05P_margin_diff_mix_0001                            | att_0002      | completed     | 67.40   | 1.308  | 12.55  | 451    | 22.26  | 0        | 0              
104  | 05_optimization                  | 05AY_05aj_diff_only_0001                            | att_0001      | completed     | 67.05   | 1.316  | 12.47  | 462    | 22.26  | 0        | 0              
105  | 05_optimization                  | 05AE_drop_supertrend103_0001                        | att_0001      | completed     | 65.96   | 1.283  | 12.58  | 523    | 22.26  | 0        | 0              
106  | 05_optimization                  | 05BE_trend_proxy_breadth_only_0001                  | att_0001      | completed     | 65.23   | 1.276  | 13.53  | 490    | 22.26  | 0        | 0              
107  | 05_optimization                  | 05FE_05ca_cls_scale_0001                            | att_0001      | completed     | 65.19   | 1.242  | 16.64  | 440    | 22.26  | 0        | 0              
108  | 05_optimization                  | 05F_mt5_validation_margin_07250_0001                | att_0001      | completed     | 64.84   | 1.265  | 12.54  | 502    | 22.26  | 0        | 0              
109  | 05_optimization                  | 05FD_05ca_flatup_longdown_margin0675_hold5_0001     | att_0002      | completed     | 64.77   | 1.222  | 22.94  | 511    | 22.26  | 0        | 0              
110  | 05_optimization                  | 05G_mt5_validation_diff_07250_0001                  | att_0001      | completed     | 63.62   | 1.245  | 12.99  | 557    | 22.26  | 0        | 0              
111  | 05_optimization                  | 05AU_05ai_diff_only_0001                            | att_0001      | completed     | 63.46   | 1.300  | 12.17  | 457    | 22.26  | 0        | 0              
112  | 05_optimization                  | 05BG_trend_proxy_breakout_breadth_0001              | att_0001      | completed     | 63.41   | 1.271  | 13.14  | 490    | 22.26  | 0        | 0              
113  | 05_optimization                  | 05BN_05w_balanced_tight_diff_0001                   | att_0001      | completed     | 63.28   | 1.359  | 11.15  | 334    | 22.26  | 0        | 0              
114  | 05_optimization                  | 05AN_05w_diff_only_0001                             | att_0001      | completed     | 63.13   | 1.296  | 12.40  | 463    | 22.26  | 0        | 0              
115  | 05_optimization                  | 05U_no_momentum_osc_0001                            | att_0001      | completed     | 62.95   | 1.282  | 12.47  | 461    | 22.26  | 0        | 0              
116  | 05_optimization                  | 05C_mt5_validation_margin_tightgap_0001             | att_0002      | completed     | 62.82   | 1.337  | 12.47  | 378    | 22.26  | 0        | 0              
117  | 05_optimization                  | 05AL_trend_proxy_light_pc_0001                      | att_0001      | completed     | 62.74   | 1.268  | 14.07  | 490    | 22.26  | 0        | 0              
118  | 05_optimization                  | 05FF_05ca_temp_shortbias_0001                       | att_0001      | completed     | 62.43   | 1.154  | 29.94  | 722    | 22.26  | 0        | 0              
119  | 05_optimization                  | 05BL_05w_long_bias_diff_0001                        | att_0001      | completed     | 62.23   | 1.628  | 14.00  | 204    | 22.26  | 0        | 0              
120  | 05_optimization                  | 05AH_trend_proxy_sector_replacement_0001            | att_0002      | completed     | 62.20   | 1.263  | 13.45  | 489    | 22.26  | 0        | 0              
121  | 05_optimization                  | 05AK_trend_proxy_light_core3_0001                   | att_0001      | completed     | 61.83   | 1.256  | 13.91  | 493    | 22.26  | 0        | 0              
122  | 04_probability_difference_filter | 04C_mt5_validation_baseline_0001                    | att_0002      | completed     | 60.65   | 1.283  | 12.67  | 435    | 22.26  | 0        | 0              
123  | 05_optimization                  | 05E_mt5_validation_margin_08250_0001                | att_0001      | completed     | 56.75   | 1.273  | 12.61  | 408    | 22.26  | 0        | 0              
124  | 05_optimization                  | 05V_no_vol_band_0001                                | att_0001      | completed     | 55.98   | 1.270  | 14.47  | 429    | 22.26  | 0        | 0              
125  | 05_optimization                  | 05DA_mt5_validation_margin_regularized_vote_0001    | att_0003      | completed     | 53.24   | 1.222  | 14.15  | 489    | 22.26  | 0        | 0              
126  | 05_optimization                  | 05BJ_05w_short_bias_diff_0001                       | att_0001      | completed     | 53.00   | 1.259  | 13.43  | 416    | 22.26  | 0        | 0              
127  | 05_optimization                  | 05AA_no_breadth_disp_0001                           | att_0001      | completed     | 49.11   | 1.192  | 13.63  | 501    | 22.26  | 0        | 0              
128  | 05_optimization                  | 05FC_05ca_shortup_longdown_margin0675_hold5_0001    | att_0002      | completed     | 49.11   | 1.103  | 31.04  | 840    | 22.26  | 0        | 0              
129  | 05_optimization                  | 05CY_mt5_validation_margin_elasticnet_logreg_0001   | att_0003      | completed     | 42.51   | 1.178  | 14.83  | 477    | 22.26  | 0        | 0              
130  | 05_optimization                  | 05Y_no_risk_proxy_0001                              | att_0001      | completed     | 42.08   | 1.179  | 16.56  | 494    | 22.26  | 0        | 0              
131  | 05_optimization                  | 05O_thr_diff_mix_0001                               | att_0001      | completed     | 41.01   | 1.279  | 16.28  | 247    | 22.26  | 0        | 0              
132  | 05_optimization                  | 05Q_thr_margin_diff_0001                            | att_0001      | completed     | 41.01   | 1.279  | 16.28  | 247    | 22.26  | 0        | 0              
133  | 05_optimization                  | 05CZ_mt5_validation_margin_pca_logreg_0001          | att_0001      | completed     | 37.50   | 1.401  | 21.30  | 168    | 22.26  | 0        | 0              
134  | 05_optimization                  | 05N_thr_margin_mix_0001                             | att_0001      | completed     | 35.61   | 1.220  | 17.16  | 278    | 22.26  | 0        | 0              
135  | 02_individual_thresholds         | 02H_mt5_validation_baseline_0001                    | att_0002      | completed     | 32.40   | 1.075  | 41.10  | 878    | 22.26  | 0        | 0              
136  | 05_optimization                  | 05GA_05dp_riskpct050_atr14x15_0001                  | att_0002      | completed     | 25.08   | 1.311  | 6.56   | 426    | 22.26  | 0        | 0              
137  | 05_optimization                  | 05FN_ovr_proxy_0001                                 | att_0004      | completed     | 8.86    | 1.200  | 9.72   | 70     | 22.26  | 0        | 0              
138  | 05_optimization                  | 05BV_frontier_stack_w_bb_bf_0001                    | att_0002      | completed     | -11.85  | 0.929  | 27.60  | 270    | 22.26  | 0        | 0              
139  | 05_optimization                  | 05BW_frontier_stack_w_bb_ah_0001                    | att_0002      | completed     | -16.90  | 0.930  | 30.37  | 416    | 22.26  | 0        | 0              
140  | 05_optimization                  | 05BU_frontier_stack_w_bf_0001                       | att_0001      | completed     | -20.89  | 0.887  | 30.07  | 301    | 22.26  | 0        | 0              
```

## Runs

### 1. `05_optimization` / `05I_mt5_validation_margin_lightgbm_modelswap_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05I_mt5_validation_margin_lightgbm_modelswap_0001\experiment_bundle.json`
- experiment_id: `exp_stage05_margin_lightgbm_modelswap_validation_0001`
- bundle_status: `completed`
- latest_attempt: `att_0002`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-29T15:23:19.345300+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: max_probability_margin(min_margin=0.07) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=3)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `1308.5559999999998` |
| `profit_factor` | `15.290226056568745` |
| `trade_count` | `1554` |
| `win_rate` | `0.853925353925354` |
| `expectancy_per_trade` | `4.21028314028314` |
| `max_dd_pct` | `1.9298111476412576` |
| `recovery_factor` | `322.94076999012486` |
| `net_profit` | `6542.78` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `1.9298111476412576` |
| `equity_dd_amount` | `20.26000000000022` |
| `max_dd_pct` | `1.4790809117159174` |
| `max_dd_amount` | `12.460000000000036` |
| `ulcer_index` | `0.08406059582529445` |
| `worst_day` | `-0.7299999999999995` |
| `worst_week` | `6.68` |
| `min_free_margin` | `480.17` |
| `consecutive_losses` | `4` |
| `time_under_water` | `9176700.0` |
| `longest_recovery_duration` | `496500.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `3.0` |
| `payoff_ratio` | `2.6155850149518503` |
| `avg_win` | `5.275531273549359` |
| `avg_loss` | `-2.0169603524229074` |
| `long_count` | `782` |
| `short_count` | `772` |
| `long_expectancy` | `4.212800511508951` |
| `short_expectancy` | `4.207733160621761` |
| `mfe_mean` | `6.43453667953668` |
| `mfe_median` | `5.385` |
| `mfe_p90` | `11.454000000000002` |
| `mae_mean` | `2.43993564993565` |
| `mae_median` | `1.7` |
| `mae_p90` | `5.427` |
| `no_trade_rate` | `0.6262334127254168` |
| `hold_distribution` | `{'p50': 3.0, 'p90': 3.0}` |
| `loss_trade_mfe` | `2.4640528634361236` |
| `realized_over_mfe` | `-0.004203394438240282` |
| `rule_pass_rates` | `{'long_signal_rate': 0.18952024498128614, 'short_signal_rate': 0.18424634229329703}` |
| `win_trade_mae` | `2.083112283345893` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0002 | completed | 2026-03-29 15:23:19 UTC | -5.07   | 794    | 6755  | 6720          | 35      
att_0001 | completed | 2026-03-29 15:21:33 UTC | 1308.56 | 1554   | 11756 | 11756         | 0       
```

### 2. `05_optimization` / `05K_mt5_validation_margin_xgboost_modelswap_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05K_mt5_validation_margin_xgboost_modelswap_0001\experiment_bundle.json`
- experiment_id: `exp_stage05_margin_xgboost_modelswap_validation_0001`
- bundle_status: `completed`
- latest_attempt: `att_0002`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-29T15:42:46.031008+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: max_probability_margin(min_margin=0.07) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=3)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `816.8820000000001` |
| `profit_factor` | `4.56166450116414` |
| `trade_count` | `1394` |
| `win_rate` | `0.7159253945480631` |
| `expectancy_per_trade` | `2.929992826398852` |
| `max_dd_pct` | `8.145696668833603` |
| `recovery_factor` | `98.77654171704953` |
| `net_profit` | `4084.41` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `8.145696668833603` |
| `equity_dd_amount` | `41.35000000000002` |
| `max_dd_pct` | `7.303559104801334` |
| `max_dd_amount` | `37.039999999999964` |
| `ulcer_index` | `0.3186107634073605` |
| `worst_day` | `-13.239999999999995` |
| `worst_week` | `-0.42999999999999994` |
| `min_free_margin` | `455.88` |
| `consecutive_losses` | `5` |
| `time_under_water` | `13390200.0` |
| `longest_recovery_duration` | `687900.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `3.0` |
| `payoff_ratio` | `1.810039220902805` |
| `avg_win` | `5.241663326653307` |
| `avg_loss` | `-2.8958838383838383` |
| `long_count` | `660` |
| `short_count` | `734` |
| `long_expectancy` | `3.2180303030303032` |
| `short_expectancy` | `2.6709945504087194` |
| `mfe_mean` | `5.7605021520803446` |
| `mfe_median` | `4.74` |
| `mfe_p90` | `11.387` |
| `mae_mean` | `3.145394548063128` |
| `mae_median` | `2.27` |
| `mae_p90` | `6.6640000000000015` |
| `no_trade_rate` | `0.6833106498809118` |
| `hold_distribution` | `{'p50': 3.0, 'p90': 3.0}` |
| `loss_trade_mfe` | `2.025530303030303` |
| `realized_over_mfe` | `-1.3462570307119397` |
| `rule_pass_rates` | `{'long_signal_rate': 0.15209254848587955, 'short_signal_rate': 0.16459680163320858}` |
| `win_trade_mae` | `2.3869639278557115` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0002 | completed | 2026-03-29 15:42:46 UTC | -0.21   | 780    | 6755  | 6720          | 35      
att_0001 | completed | 2026-03-29 15:41:50 UTC | 816.88  | 1394   | 11756 | 11756         | 0       
```

### 3. `05_optimization` / `05L_rf_margin_swap_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05L_rf_margin_swap_0001\experiment_bundle.json`
- experiment_id: `exp_05L_rf_margin_v1`
- bundle_status: `completed`
- latest_attempt: `att_0001`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-29T15:58:29.264373+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: max_probability_margin(min_margin=0.07) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=3)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `593.442` |
| `profit_factor` | `8.435125789315427` |
| `trade_count` | `850` |
| `win_rate` | `0.7658823529411765` |
| `expectancy_per_trade` | `3.4908352941176473` |
| `max_dd_pct` | `1.6298795777481927` |
| `recovery_factor` | `150.01061678463114` |
| `net_profit` | `2967.21` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `1.6298795777481927` |
| `equity_dd_amount` | `19.779999999999973` |
| `max_dd_pct` | `1.2051925519719884` |
| `max_dd_amount` | `14.829999999999927` |
| `ulcer_index` | `0.2123822657984066` |
| `worst_day` | `-7.079999999999999` |
| `worst_week` | `-1.98` |
| `min_free_margin` | `489.35` |
| `consecutive_losses` | `5` |
| `time_under_water` | `14466900.0` |
| `longest_recovery_duration` | `594300.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `3.0` |
| `payoff_ratio` | `2.5784793119412748` |
| `avg_win` | `5.1709523809523805` |
| `avg_loss` | `-2.0054271356783917` |
| `long_count` | `126` |
| `short_count` | `724` |
| `long_expectancy` | `5.727222222222222` |
| `short_expectancy` | `3.1016298342541435` |
| `mfe_mean` | `5.913541176470589` |
| `mfe_median` | `4.69` |
| `mfe_p90` | `11.645000000000001` |
| `mae_mean` | `2.5683882352941176` |
| `mae_median` | `1.87` |
| `mae_p90` | `5.1850000000000005` |
| `no_trade_rate` | `0.8342973800612453` |
| `hold_distribution` | `{'p50': 3.0, 'p90': 3.0}` |
| `loss_trade_mfe` | `1.9055276381909547` |
| `realized_over_mfe` | `-0.4221747515300449` |
| `rule_pass_rates` | `{'long_signal_rate': 0.02407281388227288, 'short_signal_rate': 0.1416298060564818}` |
| `win_trade_mae` | `2.088940092165899` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0001 | completed | 2026-03-29 15:58:29 UTC | 593.44  | 850    | 11756 | 11756         | 0       
```

### 4. `05_optimization` / `05GK_05dp_dirsplit_l14_s20_riskpct300_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05GK_05dp_dirsplit_l14_s20_riskpct300_0001\experiment_bundle.json`
- experiment_id: `exp_05gk_05dp_dirsplit_l14_s20_riskpct300_v1`
- bundle_status: `completed`
- latest_attempt: `att_0001`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-31T15:54:20.951578+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: max_probability_margin(min_margin=0.0675) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=5)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `521.9960000000001` |
| `profit_factor` | `1.3291452121615674` |
| `trade_count` | `425` |
| `win_rate` | `0.5152941176470588` |
| `expectancy_per_trade` | `6.141129411764706` |
| `max_dd_pct` | `34.503684329017034` |
| `recovery_factor` | `1.913461045007001` |
| `net_profit` | `2609.98` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `34.503684329017034` |
| `equity_dd_amount` | `1364.0100000000002` |
| `max_dd_pct` | `34.32757864417867` |
| `max_dd_amount` | `1353.8900000000003` |
| `ulcer_index` | `15.227082889438064` |
| `worst_day` | `-273.74` |
| `worst_week` | `-603.02` |
| `min_free_margin` | `408.99` |
| `consecutive_losses` | `8` |
| `time_under_water` | `22140300.0` |
| `longest_recovery_duration` | `13237500.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `4.517647058823529` |
| `payoff_ratio` | `1.2502461813026615` |
| `avg_win` | `48.125799086757986` |
| `avg_loss` | `-38.49305825242718` |
| `long_count` | `187` |
| `short_count` | `238` |
| `long_expectancy` | `12.8396256684492` |
| `short_expectancy` | `0.8780252100840338` |
| `mfe_mean` | `46.08901176470589` |
| `mfe_median` | `23.99` |
| `mfe_p90` | `112.786` |
| `mae_mean` | `31.126470588235293` |
| `mae_median` | `18.79` |
| `mae_p90` | `86.73400000000001` |
| `no_trade_rate` | `0.8937563797209935` |
| `hold_distribution` | `{'p50': 5.0, 'p90': 5.0}` |
| `loss_trade_mfe` | `22.289660194174758` |
| `realized_over_mfe` | `-5.285936715492083` |
| `rule_pass_rates` | `{'long_signal_rate': 0.04550867642055121, 'short_signal_rate': 0.06073494385845526}` |
| `win_trade_mae` | `16.458036529680363` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `None` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `None` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': None, 'p90_points': None}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0001 | completed | 2026-03-31 15:54:20 UTC | 522.00  | 425    | 11756 | 11756         | 0       
```

### 5. `05_optimization` / `05GI_05dp_dirsplit_l13_s17_riskpct300_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05GI_05dp_dirsplit_l13_s17_riskpct300_0001\experiment_bundle.json`
- experiment_id: `exp_05gi_05dp_dirsplit_l13_s17_riskpct300_v1`
- bundle_status: `completed`
- latest_attempt: `att_0001`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-31T15:50:52.352935+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: max_probability_margin(min_margin=0.0675) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=5)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `455.3059999999999` |
| `profit_factor` | `1.2583425441951146` |
| `trade_count` | `430` |
| `win_rate` | `0.5093023255813953` |
| `expectancy_per_trade` | `5.294255813953487` |
| `max_dd_pct` | `39.889797683648624` |
| `recovery_factor` | `1.36368156223793` |
| `net_profit` | `2276.5299999999997` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `39.889797683648624` |
| `equity_dd_amount` | `1669.3999999999996` |
| `max_dd_pct` | `39.71393529408947` |
| `max_dd_amount` | `1657.8899999999999` |
| `ulcer_index` | `21.657026591432736` |
| `worst_day` | `-346.45` |
| `worst_week` | `-586.63` |
| `min_free_margin` | `404.1` |
| `consecutive_losses` | `8` |
| `time_under_water` | `22251900.0` |
| `longest_recovery_duration` | `13237500.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `4.355813953488372` |
| `payoff_ratio` | `1.2123756932656127` |
| `avg_win` | `50.63283105022831` |
| `avg_loss` | `-41.76331753554502` |
| `long_count` | `188` |
| `short_count` | `242` |
| `long_expectancy` | `14.951542553191489` |
| `short_expectancy` | `-2.208099173553719` |
| `mfe_mean` | `49.26630232558139` |
| `mfe_median` | `26.77` |
| `mfe_p90` | `122.02800000000002` |
| `mae_mean` | `32.62367441860465` |
| `mae_median` | `20.979999999999997` |
| `mae_p90` | `85.60100000000001` |
| `no_trade_rate` | `0.8937563797209935` |
| `hold_distribution` | `{'p50': 5.0, 'p90': 5.0}` |
| `loss_trade_mfe` | `24.44303317535545` |
| `realized_over_mfe` | `-6.408689942196466` |
| `rule_pass_rates` | `{'long_signal_rate': 0.04550867642055121, 'short_signal_rate': 0.06073494385845526}` |
| `win_trade_mae` | `17.438127853881277` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `None` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `None` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': None, 'p90_points': None}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0001 | completed | 2026-03-31 15:50:52 UTC | 455.31  | 430    | 11756 | 11756         | 0       
```

### 6. `05_optimization` / `05M_et_margin_swap_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05M_et_margin_swap_0001\experiment_bundle.json`
- experiment_id: `exp_05M_et_margin_v1`
- bundle_status: `completed`
- latest_attempt: `att_0001`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-29T16:00:07.017962+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: max_probability_margin(min_margin=0.07) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=3)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `422.01199999999994` |
| `profit_factor` | `11.58363846115263` |
| `trade_count` | `449` |
| `win_rate` | `0.8129175946547884` |
| `expectancy_per_trade` | `4.699465478841871` |
| `max_dd_pct` | `2.096883107651838` |
| `recovery_factor` | `96.48193872885278` |
| `net_profit` | `2110.06` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `2.096883107651838` |
| `equity_dd_amount` | `21.86999999999989` |
| `max_dd_pct` | `1.1427374496706832` |
| `max_dd_amount` | `14.309999999999945` |
| `ulcer_index` | `0.27124063928989617` |
| `worst_day` | `-14.170000000000002` |
| `worst_week` | `-12.850000000000001` |
| `min_free_margin` | `489.33` |
| `consecutive_losses` | `4` |
| `time_under_water` | `12768600.0` |
| `longest_recovery_duration` | `1111200.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `3.0` |
| `payoff_ratio` | `2.665823645854304` |
| `avg_win` | `6.327205479452054` |
| `avg_loss` | `-2.373452380952381` |
| `long_count` | `60` |
| `short_count` | `389` |
| `long_expectancy` | `8.599` |
| `short_expectancy` | `4.097994858611825` |
| `mfe_mean` | `7.507906458797327` |
| `mfe_median` | `6.19` |
| `mfe_p90` | `14.431999999999999` |
| `mae_mean` | `3.105879732739421` |
| `mae_median` | `2.26` |
| `mae_p90` | `6.349999999999998` |
| `no_trade_rate` | `0.9094930248383803` |
| `hold_distribution` | `{'p50': 3.0, 'p90': 3.0}` |
| `loss_trade_mfe` | `2.698571428571429` |
| `realized_over_mfe` | `-0.01774226890652512` |
| `rule_pass_rates` | `{'long_signal_rate': 0.011908812521265737, 'short_signal_rate': 0.07859816264035387}` |
| `win_trade_mae` | `2.6985479452054797` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0001 | completed | 2026-03-29 16:00:07 UTC | 422.01  | 449    | 11756 | 11756         | 0       
```

### 7. `05_optimization` / `05GJ_05dp_dirsplit_l12_s18_riskpct300_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05GJ_05dp_dirsplit_l12_s18_riskpct300_0001\experiment_bundle.json`
- experiment_id: `exp_05gj_05dp_dirsplit_l12_s18_riskpct300_v1`
- bundle_status: `completed`
- latest_attempt: `att_0001`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-31T15:52:37.418119+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: max_probability_margin(min_margin=0.0675) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=5)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `413.408` |
| `profit_factor` | `1.2375629523894898` |
| `trade_count` | `431` |
| `win_rate` | `0.5011600928074246` |
| `expectancy_per_trade` | `4.795916473317865` |
| `max_dd_pct` | `42.82753596300301` |
| `recovery_factor` | `1.0919964076285067` |
| `net_profit` | `2067.04` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `42.82753596300301` |
| `equity_dd_amount` | `1892.8999999999996` |
| `max_dd_pct` | `42.62515256975103` |
| `max_dd_amount` | `1878.8399999999997` |
| `ulcer_index` | `25.733476498813275` |
| `worst_day` | `-371.42` |
| `worst_week` | `-611.6099999999999` |
| `min_free_margin` | `401.55` |
| `consecutive_losses` | `8` |
| `time_under_water` | `22477800.0` |
| `longest_recovery_duration` | `13237500.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `4.334106728538283` |
| `payoff_ratio` | `1.2318334942765756` |
| `avg_win` | `49.85212962962963` |
| `avg_loss` | `-40.469860465116284` |
| `long_count` | `190` |
| `short_count` | `241` |
| `long_expectancy` | `13.921999999999999` |
| `short_expectancy` | `-2.3989211618257262` |
| `mfe_mean` | `47.47515081206497` |
| `mfe_median` | `24.49` |
| `mfe_p90` | `128.14` |
| `mae_mean` | `31.493271461716937` |
| `mae_median` | `19.9` |
| `mae_p90` | `83.28` |
| `no_trade_rate` | `0.8937563797209935` |
| `hold_distribution` | `{'p50': 5.0, 'p90': 5.0}` |
| `loss_trade_mfe` | `23.028186046511628` |
| `realized_over_mfe` | `-6.499098670213103` |
| `rule_pass_rates` | `{'long_signal_rate': 0.04550867642055121, 'short_signal_rate': 0.06073494385845526}` |
| `win_trade_mae` | `16.54449074074074` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `None` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `None` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': None, 'p90_points': None}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0001 | completed | 2026-03-31 15:52:37 UTC | 413.41  | 431    | 11756 | 11756         | 0       
```

### 8. `05_optimization` / `05GC_05dp_fixed_stop10_riskpct300_brokersl_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05GC_05dp_fixed_stop10_riskpct300_brokersl_0001\experiment_bundle.json`
- experiment_id: `exp_05gc_05dp_fixed_stop10_riskpct300_brokersl_v1`
- bundle_status: `completed`
- latest_attempt: `att_0001`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-31T15:40:30.376325+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: max_probability_margin(min_margin=0.0675) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=5)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `401.004` |
| `profit_factor` | `1.1529410149384887` |
| `trade_count` | `455` |
| `win_rate` | `0.42637362637362636` |
| `expectancy_per_trade` | `4.406637362637363` |
| `max_dd_pct` | `53.39323703294507` |
| `recovery_factor` | `0.7356116889549282` |
| `net_profit` | `2005.02` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `53.39323703294507` |
| `equity_dd_amount` | `2725.6499999999996` |
| `max_dd_pct` | `53.17286093024993` |
| `max_dd_amount` | `2705.6000000000004` |
| `ulcer_index` | `31.95900062414713` |
| `worst_day` | `-515.9599999999999` |
| `worst_week` | `-836.2099999999998` |
| `min_free_margin` | `345.65` |
| `consecutive_losses` | `9` |
| `time_under_water` | `22929900.0` |
| `longest_recovery_duration` | `13237500.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `3.6835164835164833` |
| `payoff_ratio` | `1.5511216747368328` |
| `avg_win` | `77.91123711340207` |
| `avg_loss` | `-50.22896551724138` |
| `long_count` | `196` |
| `short_count` | `259` |
| `long_expectancy` | `17.84969387755102` |
| `short_expectancy` | `-5.766486486486486` |
| `mfe_mean` | `67.69602197802197` |
| `mfe_median` | `31.05` |
| `mfe_p90` | `170.48200000000008` |
| `mae_mean` | `38.54916483516483` |
| `mae_median` | `21.85` |
| `mae_p90` | `92.88600000000002` |
| `no_trade_rate` | `0.8937563797209935` |
| `hold_distribution` | `{'p50': 5.0, 'p90': 5.0}` |
| `loss_trade_mfe` | `36.27360153256705` |
| `realized_over_mfe` | `-6.350803007253438` |
| `rule_pass_rates` | `{'long_signal_rate': 0.04550867642055121, 'short_signal_rate': 0.06073494385845526}` |
| `win_trade_mae` | `19.668298969072165` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `None` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `None` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': None, 'p90_points': None}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0001 | completed | 2026-03-31 15:40:30 UTC | 401.00  | 455    | 11756 | 11756         | 0       
```

### 9. `05_optimization` / `05GE_05dp_fixed_stop20_riskpct300_brokersl_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05GE_05dp_fixed_stop20_riskpct300_brokersl_0001\experiment_bundle.json`
- experiment_id: `exp_05ge_05dp_fixed_stop20_riskpct300_brokersl_v1`
- bundle_status: `completed`
- latest_attempt: `att_0001`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-31T15:44:00.283371+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: max_probability_margin(min_margin=0.0675) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=5)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `388.414` |
| `profit_factor` | `1.3120282389838078` |
| `trade_count` | `417` |
| `win_rate` | `0.5347721822541966` |
| `expectancy_per_trade` | `4.657242206235011` |
| `max_dd_pct` | `36.997974757936035` |
| `recovery_factor` | `1.5121975908492762` |
| `net_profit` | `1942.07` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `36.997974757936035` |
| `equity_dd_amount` | `1284.27` |
| `max_dd_pct` | `36.872752875453756` |
| `max_dd_amount` | `1277.8400000000001` |
| `ulcer_index` | `19.304568694545836` |
| `worst_day` | `-219.2` |
| `worst_week` | `-502.21999999999997` |
| `min_free_margin` | `427.45` |
| `consecutive_losses` | `8` |
| `time_under_water` | `22137600.0` |
| `longest_recovery_duration` | `13237500.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `4.661870503597123` |
| `payoff_ratio` | `1.1414057325688733` |
| `avg_win` | `36.61923766816144` |
| `avg_loss` | `-32.08257731958763` |
| `long_count` | `180` |
| `short_count` | `237` |
| `long_expectancy` | `10.41461111111111` |
| `short_expectancy` | `0.2845569620253165` |
| `mfe_mean` | `35.9863309352518` |
| `mfe_median` | `19.02` |
| `mfe_p90` | `84.07400000000007` |
| `mae_mean` | `25.684892086330937` |
| `mae_median` | `14.9` |
| `mae_p90` | `70.20200000000001` |
| `no_trade_rate` | `0.8937563797209935` |
| `hold_distribution` | `{'p50': 5.0, 'p90': 5.0}` |
| `loss_trade_mfe` | `17.86221649484536` |
| `realized_over_mfe` | `-5.284023656195332` |
| `rule_pass_rates` | `{'long_signal_rate': 0.04550867642055121, 'short_signal_rate': 0.06073494385845526}` |
| `win_trade_mae` | `13.831793721973094` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `None` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `None` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': None, 'p90_points': None}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0001 | completed | 2026-03-31 15:44:00 UTC | 388.41  | 417    | 11756 | 11756         | 0       
```

### 10. `05_optimization` / `05GF_05dp_regime085_115_100_150_200_riskpct300_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05GF_05dp_regime085_115_100_150_200_riskpct300_0001\experiment_bundle.json`
- experiment_id: `exp_05gf_05dp_regime085_115_100_150_200_riskpct300_v1`
- bundle_status: `completed`
- latest_attempt: `att_0001`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-31T15:45:41.272480+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: max_probability_margin(min_margin=0.0675) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=5)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `347.492` |
| `profit_factor` | `1.2417786411657965` |
| `trade_count` | `428` |
| `win_rate` | `0.5046728971962616` |
| `expectancy_per_trade` | `4.059485981308411` |
| `max_dd_pct` | `41.018323649174185` |
| `recovery_factor` | `1.2112293127727507` |
| `net_profit` | `1737.46` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `41.018323649174185` |
| `equity_dd_amount` | `1434.46` |
| `max_dd_pct` | `40.86894472592219` |
| `max_dd_amount` | `1426.13` |
| `ulcer_index` | `23.08970703806861` |
| `worst_day` | `-214.5` |
| `worst_week` | `-494.16` |
| `min_free_margin` | `417.69` |
| `consecutive_losses` | `8` |
| `time_under_water` | `22344300.0` |
| `longest_recovery_duration` | `13237500.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `4.383177570093458` |
| `payoff_ratio` | `1.2187827404034668` |
| `avg_win` | `41.31305555555556` |
| `avg_loss` | `-33.896981132075474` |
| `long_count` | `187` |
| `short_count` | `241` |
| `long_expectancy` | `10.232513368983957` |
| `short_expectancy` | `-0.7303734439834026` |
| `mfe_mean` | `39.52035046728972` |
| `mfe_median` | `22.775` |
| `mfe_p90` | `93.797` |
| `mae_mean` | `26.490794392523362` |
| `mae_median` | `16.8` |
| `mae_p90` | `68.991` |
| `no_trade_rate` | `0.8937563797209935` |
| `hold_distribution` | `{'p50': 5.0, 'p90': 5.0}` |
| `loss_trade_mfe` | `19.14872641509434` |
| `realized_over_mfe` | `-5.652909088474744` |
| `rule_pass_rates` | `{'long_signal_rate': 0.04550867642055121, 'short_signal_rate': 0.06073494385845526}` |
| `win_trade_mae` | `14.070972222222222` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `None` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `None` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': None, 'p90_points': None}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0001 | completed | 2026-03-31 15:45:41 UTC | 347.49  | 428    | 11756 | 11756         | 0       
```

### 11. `05_optimization` / `05GG_05dp_regime090_110_090_140_180_riskpct300_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05GG_05dp_regime090_110_090_140_180_riskpct300_0001\experiment_bundle.json`
- experiment_id: `exp_05gg_05dp_regime090_110_090_140_180_riskpct300_v1`
- bundle_status: `completed`
- latest_attempt: `att_0001`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-31T15:47:25.146600+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: max_probability_margin(min_margin=0.0675) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=5)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `339.02400000000006` |
| `profit_factor` | `1.2093911780291942` |
| `trade_count` | `435` |
| `win_rate` | `0.496551724137931` |
| `expectancy_per_trade` | `3.896827586206897` |
| `max_dd_pct` | `38.34527992772001` |
| `recovery_factor` | `1.2639490578840231` |
| `net_profit` | `1695.1200000000001` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `38.34527992772001` |
| `equity_dd_amount` | `1341.13` |
| `max_dd_pct` | `38.150835683334485` |
| `max_dd_amount` | `1331.2200000000003` |
| `ulcer_index` | `21.18686630798551` |
| `worst_day` | `-241.23` |
| `worst_week` | `-518.25` |
| `min_free_margin` | `398.71` |
| `consecutive_losses` | `8` |
| `time_under_water` | `22427400.0` |
| `longest_recovery_duration` | `13237500.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `4.248275862068965` |
| `payoff_ratio` | `1.226188277724044` |
| `avg_win` | `45.32680555555556` |
| `avg_loss` | `-36.965616438356165` |
| `long_count` | `189` |
| `short_count` | `246` |
| `long_expectancy` | `10.39857142857143` |
| `short_expectancy` | `-1.0984146341463414` |
| `mfe_mean` | `43.70542528735632` |
| `mfe_median` | `25.99` |
| `mfe_p90` | `106.33600000000004` |
| `mae_mean` | `28.668735632183907` |
| `mae_median` | `19.11` |
| `mae_p90` | `71.86600000000001` |
| `no_trade_rate` | `0.8937563797209935` |
| `hold_distribution` | `{'p50': 5.0, 'p90': 5.0}` |
| `loss_trade_mfe` | `20.837123287671233` |
| `realized_over_mfe` | `-6.294882687382032` |
| `rule_pass_rates` | `{'long_signal_rate': 0.04550867642055121, 'short_signal_rate': 0.06073494385845526}` |
| `win_trade_mae` | `15.777222222222223` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `None` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `None` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': None, 'p90_points': None}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0001 | completed | 2026-03-31 15:47:25 UTC | 339.02  | 435    | 11756 | 11756         | 0       
```

### 12. `05_optimization` / `05GH_05dp_regime085_120_110_150_220_riskpct300_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05GH_05dp_regime085_120_110_150_220_riskpct300_0001\experiment_bundle.json`
- experiment_id: `exp_05gh_05dp_regime085_120_110_150_220_riskpct300_v1`
- bundle_status: `completed`
- latest_attempt: `att_0001`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-31T15:49:09.831424+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: max_probability_margin(min_margin=0.0675) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=5)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `286.892` |
| `profit_factor` | `1.2346158375421976` |
| `trade_count` | `426` |
| `win_rate` | `0.5093896713615024` |
| `expectancy_per_trade` | `3.3672769953051644` |
| `max_dd_pct` | `40.68831695274549` |
| `recovery_factor` | `1.1713893743160921` |
| `net_profit` | `1434.46` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `40.68831695274549` |
| `equity_dd_amount` | `1224.58` |
| `max_dd_pct` | `40.5396405726064` |
| `max_dd_amount` | `1217.45` |
| `ulcer_index` | `23.282886139019425` |
| `worst_day` | `-181.6` |
| `worst_week` | `-406.72` |
| `min_free_margin` | `404.13` |
| `consecutive_losses` | `8` |
| `time_under_water` | `22345800.0` |
| `longest_recovery_duration` | `13237500.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `4.427230046948357` |
| `payoff_ratio` | `1.1891000462964023` |
| `avg_win` | `34.78589861751152` |
| `avg_loss` | `-29.25397129186603` |
| `long_count` | `186` |
| `short_count` | `240` |
| `long_expectancy` | `8.603118279569893` |
| `short_expectancy` | `-0.6904999999999999` |
| `mfe_mean` | `33.29816901408451` |
| `mfe_median` | `19.564999999999998` |
| `mfe_p90` | `81.08` |
| `mae_mean` | `22.6706338028169` |
| `mae_median` | `15.4` |
| `mae_p90` | `56.415000000000006` |
| `no_trade_rate` | `0.8937563797209935` |
| `hold_distribution` | `{'p50': 5.0, 'p90': 5.0}` |
| `loss_trade_mfe` | `15.763014354066984` |
| `realized_over_mfe` | `-6.481075574417133` |
| `rule_pass_rates` | `{'long_signal_rate': 0.04550867642055121, 'short_signal_rate': 0.06073494385845526}` |
| `win_trade_mae` | `11.934285714285716` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `None` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `None` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': None, 'p90_points': None}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0001 | completed | 2026-03-31 15:49:09 UTC | 286.89  | 426    | 11756 | 11756         | 0       
```

### 13. `05_optimization` / `05GB_05dp_riskpct300_atr14x15_brokersl_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05GB_05dp_riskpct300_atr14x15_brokersl_0001\experiment_bundle.json`
- experiment_id: `exp_05gb_05dp_riskpct300_atr14x15_brokersl_v1`
- bundle_status: `completed`
- latest_attempt: `att_0001`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-31T15:20:30.883952+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: max_probability_margin(min_margin=0.0675) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=5)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `264.392` |
| `profit_factor` | `1.1902733138640325` |
| `trade_count` | `432` |
| `win_rate` | `0.4861111111111111` |
| `expectancy_per_trade` | `3.060092592592593` |
| `max_dd_pct` | `39.03367657046422` |
| `recovery_factor` | `1.1616724371254328` |
| `net_profit` | `1321.96` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `39.03367657046422` |
| `equity_dd_amount` | `1137.98` |
| `max_dd_pct` | `38.84183315687434` |
| `max_dd_amount` | `1129.9399999999998` |
| `ulcer_index` | `21.911449246368328` |
| `worst_day` | `-228.91` |
| `worst_week` | `-453.48999999999995` |
| `min_free_margin` | `367.27` |
| `consecutive_losses` | `8` |
| `time_under_water` | `22275000.0` |
| `longest_recovery_duration` | `13237500.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `4.275462962962963` |
| `payoff_ratio` | `1.2582889317991202` |
| `avg_win` | `39.379285714285714` |
| `avg_loss` | `-31.2959009009009` |
| `long_count` | `184` |
| `short_count` | `248` |
| `long_expectancy` | `9.19483695652174` |
| `short_expectancy` | `-1.491491935483871` |
| `mfe_mean` | `37.407222222222224` |
| `mfe_median` | `21.59` |
| `mfe_p90` | `90.23400000000001` |
| `mae_mean` | `24.926296296296297` |
| `mae_median` | `16.55` |
| `mae_p90` | `61.17700000000001` |
| `no_trade_rate` | `0.8937563797209935` |
| `hold_distribution` | `{'p50': 5.0, 'p90': 5.0}` |
| `loss_trade_mfe` | `18.57846846846847` |
| `realized_over_mfe` | `-6.124922378547494` |
| `rule_pass_rates` | `{'long_signal_rate': 0.04550867642055121, 'short_signal_rate': 0.06073494385845526}` |
| `win_trade_mae` | `13.52304761904762` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `None` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `None` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': None, 'p90_points': None}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0001 | completed | 2026-03-31 15:20:30 UTC | 264.39  | 432    | 11756 | 11756         | 0       
```

### 14. `05_optimization` / `05GD_05dp_fixed_stop15_riskpct300_brokersl_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05GD_05dp_fixed_stop15_riskpct300_brokersl_0001\experiment_bundle.json`
- experiment_id: `exp_05gd_05dp_fixed_stop15_riskpct300_brokersl_v1`
- bundle_status: `completed`
- latest_attempt: `att_0001`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-31T15:42:16.013117+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: max_probability_margin(min_margin=0.0675) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=5)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `264.392` |
| `profit_factor` | `1.1902733138640325` |
| `trade_count` | `432` |
| `win_rate` | `0.4861111111111111` |
| `expectancy_per_trade` | `3.060092592592593` |
| `max_dd_pct` | `39.03367657046422` |
| `recovery_factor` | `1.1616724371254328` |
| `net_profit` | `1321.96` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `39.03367657046422` |
| `equity_dd_amount` | `1137.98` |
| `max_dd_pct` | `38.84183315687434` |
| `max_dd_amount` | `1129.9399999999998` |
| `ulcer_index` | `21.911449246368328` |
| `worst_day` | `-228.91` |
| `worst_week` | `-453.48999999999995` |
| `min_free_margin` | `367.27` |
| `consecutive_losses` | `8` |
| `time_under_water` | `22275000.0` |
| `longest_recovery_duration` | `13237500.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `4.275462962962963` |
| `payoff_ratio` | `1.2582889317991202` |
| `avg_win` | `39.379285714285714` |
| `avg_loss` | `-31.2959009009009` |
| `long_count` | `184` |
| `short_count` | `248` |
| `long_expectancy` | `9.19483695652174` |
| `short_expectancy` | `-1.491491935483871` |
| `mfe_mean` | `37.407222222222224` |
| `mfe_median` | `21.59` |
| `mfe_p90` | `90.23400000000001` |
| `mae_mean` | `24.926296296296297` |
| `mae_median` | `16.55` |
| `mae_p90` | `61.17700000000001` |
| `no_trade_rate` | `0.8937563797209935` |
| `hold_distribution` | `{'p50': 5.0, 'p90': 5.0}` |
| `loss_trade_mfe` | `18.57846846846847` |
| `realized_over_mfe` | `-6.124922378547494` |
| `rule_pass_rates` | `{'long_signal_rate': 0.04550867642055121, 'short_signal_rate': 0.06073494385845526}` |
| `win_trade_mae` | `13.52304761904762` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `None` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `None` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': None, 'p90_points': None}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0001 | completed | 2026-03-31 15:42:16 UTC | 264.39  | 432    | 11756 | 11756         | 0       
```

### 15. `06_segmented_risk_validation` / `06A_dirsplit2pct_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\06_segmented_risk_validation\02_runs\active\06A_dirsplit2pct_0001\experiment_bundle.json`
- experiment_id: `exp_06a_dirsplit2pct_v1`
- bundle_status: `completed`
- latest_attempt: `att_0002`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-31T16:19:51.237044+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: max_probability_margin(min_margin=0.0675) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=5)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `249.08999999999997` |
| `profit_factor` | `1.3903424369879587` |
| `trade_count` | `425` |
| `win_rate` | `0.5152941176470588` |
| `expectancy_per_trade` | `2.9304705882352944` |
| `max_dd_pct` | `24.28395373353725` |
| `recovery_factor` | `2.5383674717211857` |
| `net_profit` | `1245.45` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `24.28395373353725` |
| `equity_dd_amount` | `490.6500000000001` |
| `max_dd_pct` | `24.147879364701677` |
| `max_dd_amount` | `487.1399999999999` |
| `ulcer_index` | `10.178600351759238` |
| `worst_day` | `-95.44` |
| `worst_week` | `-212.49999999999997` |
| `min_free_margin` | `438.31` |
| `consecutive_losses` | `8` |
| `time_under_water` | `22141500.0` |
| `longest_recovery_duration` | `13237500.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `4.517647058823529` |
| `payoff_ratio` | `1.3078106941530567` |
| `avg_win` | `20.256210045662097` |
| `avg_loss` | `-15.488640776699029` |
| `long_count` | `187` |
| `short_count` | `238` |
| `long_expectancy` | `5.5064705882352944` |
| `short_expectancy` | `0.9064705882352941` |
| `mfe_mean` | `19.2712` |
| `mfe_median` | `11.65` |
| `mfe_p90` | `47.234000000000016` |
| `mae_mean` | `12.796000000000001` |
| `mae_median` | `9.7` |
| `mae_p90` | `31.298000000000002` |
| `no_trade_rate` | `0.8937563797209935` |
| `hold_distribution` | `{'p50': 5.0, 'p90': 5.0}` |
| `loss_trade_mfe` | `9.019708737864077` |
| `realized_over_mfe` | `-6.261415354313975` |
| `rule_pass_rates` | `{'long_signal_rate': 0.04550867642055121, 'short_signal_rate': 0.06073494385845526}` |
| `win_trade_mae` | `7.05771689497717` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `None` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `None` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': None, 'p90_points': None}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0002 | completed | 2026-03-31 16:19:51 UTC | 69.83   | 289    | 6755  | 6720          | 35      
att_0001 | completed | 2026-03-31 16:18:47 UTC | 249.09  | 425    | 11756 | 11756         | 0       
```

### 16. `05_optimization` / `05FB_05ca_temp090_margin0675_hold5_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05FB_05ca_temp090_margin0675_hold5_0001\experiment_bundle.json`
- experiment_id: `exp_05fb_05ca_temp090_margin0675_hold5_v1`
- bundle_status: `completed`
- latest_attempt: `att_0003`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-30T16:26:21.971027+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: max_probability_margin(min_margin=0.0675) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=5)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `124.44800000000001` |
| `profit_factor` | `1.486862901585215` |
| `trade_count` | `475` |
| `win_rate` | `0.5368421052631579` |
| `expectancy_per_trade` | `1.3099789473684211` |
| `max_dd_pct` | `13.362705072549637` |
| `recovery_factor` | `4.3623107122826665` |
| `net_profit` | `622.24` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `13.362705072549637` |
| `equity_dd_amount` | `142.6400000000001` |
| `max_dd_pct` | `11.074582300997399` |
| `max_dd_amount` | `139.46000000000004` |
| `ulcer_index` | `6.707307770185801` |
| `worst_day` | `-41.15` |
| `worst_week` | `-49.83` |
| `min_free_margin` | `433.55` |
| `consecutive_losses` | `7` |
| `time_under_water` | `22307400.0` |
| `longest_recovery_duration` | `13237500.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `5.0` |
| `payoff_ratio` | `1.2827836797990093` |
| `avg_win` | `7.452156862745098` |
| `avg_loss` | `-5.809363636363636` |
| `long_count` | `205` |
| `short_count` | `270` |
| `long_expectancy` | `2.389073170731707` |
| `short_expectancy` | `0.49066666666666664` |
| `mfe_mean` | `7.125031578947368` |
| `mfe_median` | `5.21` |
| `mfe_p90` | `14.628000000000002` |
| `mae_mean` | `6.025157894736842` |
| `mae_median` | `4.58` |
| `mae_p90` | `12.41` |
| `no_trade_rate` | `0.871554950663491` |
| `hold_distribution` | `{'p50': 5.0, 'p90': 5.0}` |
| `loss_trade_mfe` | `3.358818181818182` |
| `realized_over_mfe` | `-3.2339567804370515` |
| `rule_pass_rates` | `{'long_signal_rate': 0.054780537597822386, 'short_signal_rate': 0.07366451173868663}` |
| `win_trade_mae` | `3.221725490196078` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0003 | completed | 2026-03-30 16:26:21 UTC | 56.26   | 317    | 6755  | 6720          | 35      
att_0002 | completed | 2026-03-30 16:18:24 UTC | 124.45  | 475    | 11756 | 11756         | 0       
att_0001 | completed | 2026-03-30 16:07:59 UTC | 124.45  | 475    | 11756 | 11756         | 0       
```

### 17. `05_optimization` / `05DP_05ca_margin0675_hold5_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05DP_05ca_margin0675_hold5_0001\experiment_bundle.json`
- experiment_id: `exp_05dp_05ca_margin0675_hold5_v1`
- bundle_status: `completed`
- latest_attempt: `att_0003`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-30T14:06:05.848536+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: max_probability_margin(min_margin=0.0675) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=5)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `122.57000000000001` |
| `profit_factor` | `1.5552837351744633` |
| `trade_count` | `405` |
| `win_rate` | `0.5358024691358024` |
| `expectancy_per_trade` | `1.51320987654321` |
| `max_dd_pct` | `12.603127209868777` |
| `recovery_factor` | `4.173021925643466` |
| `net_profit` | `612.85` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `12.603127209868777` |
| `equity_dd_amount` | `146.86000000000013` |
| `max_dd_pct` | `11.559051851379069` |
| `max_dd_amount` | `144.8800000000001` |
| `ulcer_index` | `7.2871377165059945` |
| `worst_day` | `-36.03` |
| `worst_week` | `-52.25` |
| `min_free_margin` | `434.37` |
| `consecutive_losses` | `10` |
| `time_under_water` | `22097100.0` |
| `longest_recovery_duration` | `13237500.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `5.0` |
| `payoff_ratio` | `1.3474347567410097` |
| `avg_win` | `7.910230414746544` |
| `avg_loss` | `-5.870585106382979` |
| `long_count` | `176` |
| `short_count` | `229` |
| `long_expectancy` | `2.5995454545454546` |
| `short_expectancy` | `0.678296943231441` |
| `mfe_mean` | `7.528320987654321` |
| `mfe_median` | `5.58` |
| `mfe_p90` | `15.896000000000003` |
| `mae_mean` | `6.112839506172839` |
| `mae_median` | `4.57` |
| `mae_p90` | `12.434000000000001` |
| `no_trade_rate` | `0.8937563797209935` |
| `hold_distribution` | `{'p50': 5.0, 'p90': 5.0}` |
| `loss_trade_mfe` | `3.3813829787234044` |
| `realized_over_mfe` | `-4.2330274152032` |
| `rule_pass_rates` | `{'long_signal_rate': 0.04550867642055121, 'short_signal_rate': 0.06073494385845526}` |
| `win_trade_mae` | `3.223410138248848` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0003 | completed | 2026-03-30 14:06:05 UTC | 68.57   | 275    | 6755  | 6720          | 35      
att_0002 | completed | 2026-03-30 14:05:01 UTC | 122.57  | 405    | 11756 | 11756         | 0       
att_0001 | completed | 2026-03-30 13:54:37 UTC | 122.57  | 405    | 11756 | 11756         | 0       
```

### 18. `05_optimization` / `05FR_05dp_flatexit052_hold1_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05FR_05dp_flatexit052_hold1_0001\experiment_bundle.json`
- experiment_id: `exp_05fr_05dp_flatexit052_hold1_v1`
- bundle_status: `completed`
- latest_attempt: `att_0004`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-31T14:06:17.439462+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: max_probability_margin(min_margin=0.0675) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=5) -> flat_exit_guard(min_flat_probability=0.52, min_hold_bars=1)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `122.57000000000001` |
| `profit_factor` | `1.5552837351744633` |
| `trade_count` | `405` |
| `win_rate` | `0.5358024691358024` |
| `expectancy_per_trade` | `1.51320987654321` |
| `max_dd_pct` | `12.603127209868777` |
| `recovery_factor` | `4.173021925643466` |
| `net_profit` | `612.85` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `12.603127209868777` |
| `equity_dd_amount` | `146.86000000000013` |
| `max_dd_pct` | `11.559051851379069` |
| `max_dd_amount` | `144.8800000000001` |
| `ulcer_index` | `7.2871377165059945` |
| `worst_day` | `-36.03` |
| `worst_week` | `-52.25` |
| `min_free_margin` | `434.37` |
| `consecutive_losses` | `10` |
| `time_under_water` | `22097100.0` |
| `longest_recovery_duration` | `13237500.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `5.0` |
| `payoff_ratio` | `1.3474347567410097` |
| `avg_win` | `7.910230414746544` |
| `avg_loss` | `-5.870585106382979` |
| `long_count` | `176` |
| `short_count` | `229` |
| `long_expectancy` | `2.5995454545454546` |
| `short_expectancy` | `0.678296943231441` |
| `mfe_mean` | `7.528320987654321` |
| `mfe_median` | `5.58` |
| `mfe_p90` | `15.896000000000003` |
| `mae_mean` | `6.112839506172839` |
| `mae_median` | `4.57` |
| `mae_p90` | `12.434000000000001` |
| `no_trade_rate` | `0.8937563797209935` |
| `hold_distribution` | `{'p50': 5.0, 'p90': 5.0}` |
| `loss_trade_mfe` | `3.3813829787234044` |
| `realized_over_mfe` | `-4.2330274152032` |
| `rule_pass_rates` | `{'long_signal_rate': 0.04550867642055121, 'short_signal_rate': 0.06073494385845526}` |
| `win_trade_mae` | `3.223410138248848` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0004 | completed | 2026-03-31 14:06:17 UTC | 68.57   | 275    | 6755  | 6720          | 35      
att_0003 | completed | 2026-03-31 13:58:34 UTC | 122.57  | 405    | 11756 | 11756         | 0       
att_0002 | completed | 2026-03-31 13:42:59 UTC | 68.57   | 275    | 6755  | 6720          | 35      
att_0001 | completed | 2026-03-31 13:35:06 UTC | 122.57  | 405    | 11756 | 11756         | 0       
```

### 19. `05_optimization` / `05FS_05dp_flatexit055_hold1_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05FS_05dp_flatexit055_hold1_0001\experiment_bundle.json`
- experiment_id: `exp_05fs_05dp_flatexit055_hold1_v1`
- bundle_status: `completed`
- latest_attempt: `att_0004`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-31T14:07:24.693035+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: max_probability_margin(min_margin=0.0675) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=5) -> flat_exit_guard(min_flat_probability=0.55, min_hold_bars=1)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `122.57000000000001` |
| `profit_factor` | `1.5552837351744633` |
| `trade_count` | `405` |
| `win_rate` | `0.5358024691358024` |
| `expectancy_per_trade` | `1.51320987654321` |
| `max_dd_pct` | `12.603127209868777` |
| `recovery_factor` | `4.173021925643466` |
| `net_profit` | `612.85` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `12.603127209868777` |
| `equity_dd_amount` | `146.86000000000013` |
| `max_dd_pct` | `11.559051851379069` |
| `max_dd_amount` | `144.8800000000001` |
| `ulcer_index` | `7.2871377165059945` |
| `worst_day` | `-36.03` |
| `worst_week` | `-52.25` |
| `min_free_margin` | `434.37` |
| `consecutive_losses` | `10` |
| `time_under_water` | `22097100.0` |
| `longest_recovery_duration` | `13237500.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `5.0` |
| `payoff_ratio` | `1.3474347567410097` |
| `avg_win` | `7.910230414746544` |
| `avg_loss` | `-5.870585106382979` |
| `long_count` | `176` |
| `short_count` | `229` |
| `long_expectancy` | `2.5995454545454546` |
| `short_expectancy` | `0.678296943231441` |
| `mfe_mean` | `7.528320987654321` |
| `mfe_median` | `5.58` |
| `mfe_p90` | `15.896000000000003` |
| `mae_mean` | `6.112839506172839` |
| `mae_median` | `4.57` |
| `mae_p90` | `12.434000000000001` |
| `no_trade_rate` | `0.8937563797209935` |
| `hold_distribution` | `{'p50': 5.0, 'p90': 5.0}` |
| `loss_trade_mfe` | `3.3813829787234044` |
| `realized_over_mfe` | `-4.2330274152032` |
| `rule_pass_rates` | `{'long_signal_rate': 0.04550867642055121, 'short_signal_rate': 0.06073494385845526}` |
| `win_trade_mae` | `3.223410138248848` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0004 | completed | 2026-03-31 14:07:24 UTC | 68.57   | 275    | 6755  | 6720          | 35      
att_0003 | completed | 2026-03-31 14:00:15 UTC | 122.57  | 405    | 11756 | 11756         | 0       
att_0002 | completed | 2026-03-31 13:44:05 UTC | 68.57   | 275    | 6755  | 6720          | 35      
att_0001 | completed | 2026-03-31 13:36:49 UTC | 122.57  | 405    | 11756 | 11756         | 0       
```

### 20. `05_optimization` / `05FT_05dp_flatexit055_hold2_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05FT_05dp_flatexit055_hold2_0001\experiment_bundle.json`
- experiment_id: `exp_05ft_05dp_flatexit055_hold2_v1`
- bundle_status: `completed`
- latest_attempt: `att_0002`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-31T14:01:53.915959+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: max_probability_margin(min_margin=0.0675) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=5) -> flat_exit_guard(min_flat_probability=0.55, min_hold_bars=2)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `122.57000000000001` |
| `profit_factor` | `1.5552837351744633` |
| `trade_count` | `405` |
| `win_rate` | `0.5358024691358024` |
| `expectancy_per_trade` | `1.51320987654321` |
| `max_dd_pct` | `12.603127209868777` |
| `recovery_factor` | `4.173021925643466` |
| `net_profit` | `612.85` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `12.603127209868777` |
| `equity_dd_amount` | `146.86000000000013` |
| `max_dd_pct` | `11.559051851379069` |
| `max_dd_amount` | `144.8800000000001` |
| `ulcer_index` | `7.2871377165059945` |
| `worst_day` | `-36.03` |
| `worst_week` | `-52.25` |
| `min_free_margin` | `434.37` |
| `consecutive_losses` | `10` |
| `time_under_water` | `22097100.0` |
| `longest_recovery_duration` | `13237500.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `5.0` |
| `payoff_ratio` | `1.3474347567410097` |
| `avg_win` | `7.910230414746544` |
| `avg_loss` | `-5.870585106382979` |
| `long_count` | `176` |
| `short_count` | `229` |
| `long_expectancy` | `2.5995454545454546` |
| `short_expectancy` | `0.678296943231441` |
| `mfe_mean` | `7.528320987654321` |
| `mfe_median` | `5.58` |
| `mfe_p90` | `15.896000000000003` |
| `mae_mean` | `6.112839506172839` |
| `mae_median` | `4.57` |
| `mae_p90` | `12.434000000000001` |
| `no_trade_rate` | `0.8937563797209935` |
| `hold_distribution` | `{'p50': 5.0, 'p90': 5.0}` |
| `loss_trade_mfe` | `3.3813829787234044` |
| `realized_over_mfe` | `-4.2330274152032` |
| `rule_pass_rates` | `{'long_signal_rate': 0.04550867642055121, 'short_signal_rate': 0.06073494385845526}` |
| `win_trade_mae` | `3.223410138248848` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0002 | completed | 2026-03-31 14:01:53 UTC | 122.57  | 405    | 11756 | 11756         | 0       
att_0001 | completed | 2026-03-31 13:38:33 UTC | 122.57  | 405    | 11756 | 11756         | 0       
```

### 21. `05_optimization` / `05FU_05dp_flatexit058_hold1_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05FU_05dp_flatexit058_hold1_0001\experiment_bundle.json`
- experiment_id: `exp_05fu_05dp_flatexit058_hold1_v1`
- bundle_status: `completed`
- latest_attempt: `att_0002`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-31T14:03:33.029893+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: max_probability_margin(min_margin=0.0675) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=5) -> flat_exit_guard(min_flat_probability=0.58, min_hold_bars=1)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `122.57000000000001` |
| `profit_factor` | `1.5552837351744633` |
| `trade_count` | `405` |
| `win_rate` | `0.5358024691358024` |
| `expectancy_per_trade` | `1.51320987654321` |
| `max_dd_pct` | `12.603127209868777` |
| `recovery_factor` | `4.173021925643466` |
| `net_profit` | `612.85` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `12.603127209868777` |
| `equity_dd_amount` | `146.86000000000013` |
| `max_dd_pct` | `11.559051851379069` |
| `max_dd_amount` | `144.8800000000001` |
| `ulcer_index` | `7.2871377165059945` |
| `worst_day` | `-36.03` |
| `worst_week` | `-52.25` |
| `min_free_margin` | `434.37` |
| `consecutive_losses` | `10` |
| `time_under_water` | `22097100.0` |
| `longest_recovery_duration` | `13237500.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `5.0` |
| `payoff_ratio` | `1.3474347567410097` |
| `avg_win` | `7.910230414746544` |
| `avg_loss` | `-5.870585106382979` |
| `long_count` | `176` |
| `short_count` | `229` |
| `long_expectancy` | `2.5995454545454546` |
| `short_expectancy` | `0.678296943231441` |
| `mfe_mean` | `7.528320987654321` |
| `mfe_median` | `5.58` |
| `mfe_p90` | `15.896000000000003` |
| `mae_mean` | `6.112839506172839` |
| `mae_median` | `4.57` |
| `mae_p90` | `12.434000000000001` |
| `no_trade_rate` | `0.8937563797209935` |
| `hold_distribution` | `{'p50': 5.0, 'p90': 5.0}` |
| `loss_trade_mfe` | `3.3813829787234044` |
| `realized_over_mfe` | `-4.2330274152032` |
| `rule_pass_rates` | `{'long_signal_rate': 0.04550867642055121, 'short_signal_rate': 0.06073494385845526}` |
| `win_trade_mae` | `3.223410138248848` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0002 | completed | 2026-03-31 14:03:33 UTC | 122.57  | 405    | 11756 | 11756         | 0       
att_0001 | completed | 2026-03-31 13:40:14 UTC | 122.57  | 405    | 11756 | 11756         | 0       
```

### 22. `05_optimization` / `05FV_05dp_flatexit060_hold2_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05FV_05dp_flatexit060_hold2_0001\experiment_bundle.json`
- experiment_id: `exp_05fv_05dp_flatexit060_hold2_v1`
- bundle_status: `completed`
- latest_attempt: `att_0002`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-31T14:05:12.505598+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: max_probability_margin(min_margin=0.0675) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=5) -> flat_exit_guard(min_flat_probability=0.6, min_hold_bars=2)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `122.57000000000001` |
| `profit_factor` | `1.5552837351744633` |
| `trade_count` | `405` |
| `win_rate` | `0.5358024691358024` |
| `expectancy_per_trade` | `1.51320987654321` |
| `max_dd_pct` | `12.603127209868777` |
| `recovery_factor` | `4.173021925643466` |
| `net_profit` | `612.85` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `12.603127209868777` |
| `equity_dd_amount` | `146.86000000000013` |
| `max_dd_pct` | `11.559051851379069` |
| `max_dd_amount` | `144.8800000000001` |
| `ulcer_index` | `7.2871377165059945` |
| `worst_day` | `-36.03` |
| `worst_week` | `-52.25` |
| `min_free_margin` | `434.37` |
| `consecutive_losses` | `10` |
| `time_under_water` | `22097100.0` |
| `longest_recovery_duration` | `13237500.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `5.0` |
| `payoff_ratio` | `1.3474347567410097` |
| `avg_win` | `7.910230414746544` |
| `avg_loss` | `-5.870585106382979` |
| `long_count` | `176` |
| `short_count` | `229` |
| `long_expectancy` | `2.5995454545454546` |
| `short_expectancy` | `0.678296943231441` |
| `mfe_mean` | `7.528320987654321` |
| `mfe_median` | `5.58` |
| `mfe_p90` | `15.896000000000003` |
| `mae_mean` | `6.112839506172839` |
| `mae_median` | `4.57` |
| `mae_p90` | `12.434000000000001` |
| `no_trade_rate` | `0.8937563797209935` |
| `hold_distribution` | `{'p50': 5.0, 'p90': 5.0}` |
| `loss_trade_mfe` | `3.3813829787234044` |
| `realized_over_mfe` | `-4.2330274152032` |
| `rule_pass_rates` | `{'long_signal_rate': 0.04550867642055121, 'short_signal_rate': 0.06073494385845526}` |
| `win_trade_mae` | `3.223410138248848` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0002 | completed | 2026-03-31 14:05:12 UTC | 122.57  | 405    | 11756 | 11756         | 0       
att_0001 | completed | 2026-03-31 13:41:53 UTC | 122.57  | 405    | 11756 | 11756         | 0       
```

### 23. `05_optimization` / `05FY_05dp_flatexit048_hold1_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05FY_05dp_flatexit048_hold1_0001\experiment_bundle.json`
- experiment_id: `exp_05fy_05dp_flatexit048_hold1_v1`
- bundle_status: `completed`
- latest_attempt: `att_0001`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-31T13:55:13.265921+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: max_probability_margin(min_margin=0.0675) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=5) -> flat_exit_guard(min_flat_probability=0.48, min_hold_bars=1)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `122.57000000000001` |
| `profit_factor` | `1.5552837351744633` |
| `trade_count` | `405` |
| `win_rate` | `0.5358024691358024` |
| `expectancy_per_trade` | `1.51320987654321` |
| `max_dd_pct` | `12.603127209868777` |
| `recovery_factor` | `4.173021925643466` |
| `net_profit` | `612.85` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `12.603127209868777` |
| `equity_dd_amount` | `146.86000000000013` |
| `max_dd_pct` | `11.559051851379069` |
| `max_dd_amount` | `144.8800000000001` |
| `ulcer_index` | `7.2871377165059945` |
| `worst_day` | `-36.03` |
| `worst_week` | `-52.25` |
| `min_free_margin` | `434.37` |
| `consecutive_losses` | `10` |
| `time_under_water` | `22097100.0` |
| `longest_recovery_duration` | `13237500.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `5.0` |
| `payoff_ratio` | `1.3474347567410097` |
| `avg_win` | `7.910230414746544` |
| `avg_loss` | `-5.870585106382979` |
| `long_count` | `176` |
| `short_count` | `229` |
| `long_expectancy` | `2.5995454545454546` |
| `short_expectancy` | `0.678296943231441` |
| `mfe_mean` | `7.528320987654321` |
| `mfe_median` | `5.58` |
| `mfe_p90` | `15.896000000000003` |
| `mae_mean` | `6.112839506172839` |
| `mae_median` | `4.57` |
| `mae_p90` | `12.434000000000001` |
| `no_trade_rate` | `0.8937563797209935` |
| `hold_distribution` | `{'p50': 5.0, 'p90': 5.0}` |
| `loss_trade_mfe` | `3.3813829787234044` |
| `realized_over_mfe` | `-4.2330274152032` |
| `rule_pass_rates` | `{'long_signal_rate': 0.04550867642055121, 'short_signal_rate': 0.06073494385845526}` |
| `win_trade_mae` | `3.223410138248848` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0001 | completed | 2026-03-31 13:55:13 UTC | 122.57  | 405    | 11756 | 11756         | 0       
```

### 24. `05_optimization` / `05FZ_05dp_flatexit050_hold1_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05FZ_05dp_flatexit050_hold1_0001\experiment_bundle.json`
- experiment_id: `exp_05fz_05dp_flatexit050_hold1_v1`
- bundle_status: `completed`
- latest_attempt: `att_0001`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-31T13:56:55.354599+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: max_probability_margin(min_margin=0.0675) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=5) -> flat_exit_guard(min_flat_probability=0.5, min_hold_bars=1)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `122.57000000000001` |
| `profit_factor` | `1.5552837351744633` |
| `trade_count` | `405` |
| `win_rate` | `0.5358024691358024` |
| `expectancy_per_trade` | `1.51320987654321` |
| `max_dd_pct` | `12.603127209868777` |
| `recovery_factor` | `4.173021925643466` |
| `net_profit` | `612.85` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `12.603127209868777` |
| `equity_dd_amount` | `146.86000000000013` |
| `max_dd_pct` | `11.559051851379069` |
| `max_dd_amount` | `144.8800000000001` |
| `ulcer_index` | `7.2871377165059945` |
| `worst_day` | `-36.03` |
| `worst_week` | `-52.25` |
| `min_free_margin` | `434.37` |
| `consecutive_losses` | `10` |
| `time_under_water` | `22097100.0` |
| `longest_recovery_duration` | `13237500.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `5.0` |
| `payoff_ratio` | `1.3474347567410097` |
| `avg_win` | `7.910230414746544` |
| `avg_loss` | `-5.870585106382979` |
| `long_count` | `176` |
| `short_count` | `229` |
| `long_expectancy` | `2.5995454545454546` |
| `short_expectancy` | `0.678296943231441` |
| `mfe_mean` | `7.528320987654321` |
| `mfe_median` | `5.58` |
| `mfe_p90` | `15.896000000000003` |
| `mae_mean` | `6.112839506172839` |
| `mae_median` | `4.57` |
| `mae_p90` | `12.434000000000001` |
| `no_trade_rate` | `0.8937563797209935` |
| `hold_distribution` | `{'p50': 5.0, 'p90': 5.0}` |
| `loss_trade_mfe` | `3.3813829787234044` |
| `realized_over_mfe` | `-4.2330274152032` |
| `rule_pass_rates` | `{'long_signal_rate': 0.04550867642055121, 'short_signal_rate': 0.06073494385845526}` |
| `win_trade_mae` | `3.223410138248848` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0001 | completed | 2026-03-31 13:56:55 UTC | 122.57  | 405    | 11756 | 11756         | 0       
```

### 25. `05_optimization` / `05FX_05dp_flatexit045_hold1_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05FX_05dp_flatexit045_hold1_0001\experiment_bundle.json`
- experiment_id: `exp_05fx_05dp_flatexit045_hold1_v1`
- bundle_status: `completed`
- latest_attempt: `att_0001`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-31T13:53:34.359746+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: max_probability_margin(min_margin=0.0675) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=5) -> flat_exit_guard(min_flat_probability=0.45, min_hold_bars=1)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `122.40199999999999` |
| `profit_factor` | `1.5541009135272654` |
| `trade_count` | `405` |
| `win_rate` | `0.5358024691358024` |
| `expectancy_per_trade` | `1.5111358024691357` |
| `max_dd_pct` | `12.603127209868777` |
| `recovery_factor` | `4.143601895734596` |
| `net_profit` | `612.01` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `12.603127209868777` |
| `equity_dd_amount` | `147.70000000000005` |
| `max_dd_pct` | `11.62607009789451` |
| `max_dd_amount` | `145.72000000000003` |
| `ulcer_index` | `7.311649207257284` |
| `worst_day` | `-36.03` |
| `worst_week` | `-52.25` |
| `min_free_margin` | `434.37` |
| `consecutive_losses` | `10` |
| `time_under_water` | `22097100.0` |
| `longest_recovery_duration` | `13237500.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `4.995061728395061` |
| `payoff_ratio` | `1.3464100080328383` |
| `avg_win` | `7.910230414746544` |
| `avg_loss` | `-5.875053191489362` |
| `long_count` | `176` |
| `short_count` | `229` |
| `long_expectancy` | `2.5995454545454546` |
| `short_expectancy` | `0.6746288209606986` |
| `mfe_mean` | `7.528024691358024` |
| `mfe_median` | `5.58` |
| `mfe_p90` | `15.896000000000003` |
| `mae_mean` | `6.112839506172839` |
| `mae_median` | `4.57` |
| `mae_p90` | `12.434000000000001` |
| `no_trade_rate` | `0.8937563797209935` |
| `hold_distribution` | `{'p50': 5.0, 'p90': 5.0}` |
| `loss_trade_mfe` | `3.380744680851064` |
| `realized_over_mfe` | `-4.237369328290852` |
| `rule_pass_rates` | `{'long_signal_rate': 0.04550867642055121, 'short_signal_rate': 0.06073494385845526}` |
| `win_trade_mae` | `3.223410138248848` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0001 | completed | 2026-03-31 13:53:34 UTC | 122.40  | 405    | 11756 | 11756         | 0       
```

### 26. `05_optimization` / `05DJ_05bf_margin_hold5_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05DJ_05bf_margin_hold5_0001\experiment_bundle.json`
- experiment_id: `exp_05dj_05bf_margin_hold5_v1`
- bundle_status: `completed`
- latest_attempt: `att_0002`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-30T13:20:50.514608+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: max_probability_margin(min_margin=0.07) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=5)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `119.43599999999999` |
| `profit_factor` | `1.5645437271343625` |
| `trade_count` | `386` |
| `win_rate` | `0.5414507772020726` |
| `expectancy_per_trade` | `1.5470984455958547` |
| `max_dd_pct` | `12.469552918991115` |
| `recovery_factor` | `4.116779263752931` |
| `net_profit` | `597.18` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `12.469552918991115` |
| `equity_dd_amount` | `145.05999999999995` |
| `max_dd_pct` | `11.556970698480503` |
| `max_dd_amount` | `143.3699999999999` |
| `ulcer_index` | `7.185755376438692` |
| `worst_day` | `-33.45` |
| `worst_week` | `-52.25` |
| `min_free_margin` | `435.05` |
| `consecutive_losses` | `10` |
| `time_under_water` | `22815600.0` |
| `longest_recovery_duration` | `13237500.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `5.0` |
| `payoff_ratio` | `1.3249963622142689` |
| `avg_win` | `7.918612440191388` |
| `avg_loss` | `-5.976327683615819` |
| `long_count` | `165` |
| `short_count` | `221` |
| `long_expectancy` | `2.824242424242424` |
| `short_expectancy` | `0.5935746606334841` |
| `mfe_mean` | `7.588523316062177` |
| `mfe_median` | `5.65` |
| `mfe_p90` | `15.885` |
| `mae_mean` | `6.2386269430051815` |
| `mae_median` | `4.68` |
| `mae_p90` | `12.455` |
| `no_trade_rate` | `0.8989452194624021` |
| `hold_distribution` | `{'p50': 5.0, 'p90': 5.0}` |
| `loss_trade_mfe` | `3.400056497175141` |
| `realized_over_mfe` | `-4.384676534155574` |
| `rule_pass_rates` | `{'long_signal_rate': 0.04363729159578088, 'short_signal_rate': 0.057417488941816947}` |
| `win_trade_mae` | `3.3663636363636367` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0002 | completed | 2026-03-30 13:20:50 UTC | 59.19   | 265    | 6755  | 6720          | 35      
att_0001 | completed | 2026-03-30 13:19:47 UTC | 119.44  | 386    | 11756 | 11756         | 0       
```

### 27. `05_optimization` / `05EA_05ca_margin0675_hold4_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05EA_05ca_margin0675_hold4_0001\experiment_bundle.json`
- experiment_id: `exp_05ea_05ca_margin0675_hold4_v1`
- bundle_status: `completed`
- latest_attempt: `att_0003`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-30T14:25:42.678950+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: max_probability_margin(min_margin=0.0675) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=4)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `115.168` |
| `profit_factor` | `1.5351623126179124` |
| `trade_count` | `453` |
| `win_rate` | `0.5518763796909493` |
| `expectancy_per_trade` | `1.2711699779249448` |
| `max_dd_pct` | `11.50232592974777` |
| `recovery_factor` | `4.1661119953696995` |
| `net_profit` | `575.84` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `11.50232592974777` |
| `equity_dd_amount` | `138.22000000000003` |
| `max_dd_pct` | `11.396315013862399` |
| `max_dd_amount` | `136.87999999999988` |
| `ulcer_index` | `6.529262531443152` |
| `worst_day` | `-30.09` |
| `worst_week` | `-39.69` |
| `min_free_margin` | `452.33` |
| `consecutive_losses` | `8` |
| `time_under_water` | `22476900.0` |
| `longest_recovery_duration` | `13236300.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `4.0` |
| `payoff_ratio` | `1.2465517978457448` |
| `avg_win` | `6.607399999999999` |
| `avg_loss` | `-5.300541871921182` |
| `long_count` | `194` |
| `short_count` | `259` |
| `long_expectancy` | `1.7327319587628864` |
| `short_expectancy` | `0.9254440154440154` |
| `mfe_mean` | `6.644944812362031` |
| `mfe_median` | `5.0` |
| `mfe_p90` | `14.344000000000003` |
| `mae_mean` | `5.7435540838852095` |
| `mae_median` | `3.97` |
| `mae_p90` | `12.06` |
| `no_trade_rate` | `0.8937563797209935` |
| `hold_distribution` | `{'p50': 4.0, 'p90': 4.0}` |
| `loss_trade_mfe` | `2.9901477832512313` |
| `realized_over_mfe` | `-4.283864111632737` |
| `rule_pass_rates` | `{'long_signal_rate': 0.04550867642055121, 'short_signal_rate': 0.06073494385845526}` |
| `win_trade_mae` | `3.3391599999999997` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0003 | completed | 2026-03-30 14:25:42 UTC | 53.74   | 304    | 6755  | 6720          | 35      
att_0002 | completed | 2026-03-30 14:24:38 UTC | 115.17  | 453    | 11756 | 11756         | 0       
att_0001 | completed | 2026-03-30 14:21:11 UTC | 115.17  | 453    | 11756 | 11756         | 0       
```

### 28. `05_optimization` / `05DY_05ca_margin06625_hold5_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05DY_05ca_margin06625_hold5_0001\experiment_bundle.json`
- experiment_id: `exp_05dy_05ca_margin06625_hold5_v1`
- bundle_status: `completed`
- latest_attempt: `att_0003`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-30T14:28:29.684289+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: max_probability_margin(min_margin=0.06625) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=5)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `114.88000000000001` |
| `profit_factor` | `1.500169799984326` |
| `trade_count` | `417` |
| `win_rate` | `0.5251798561151079` |
| `expectancy_per_trade` | `1.3774580335731414` |
| `max_dd_pct` | `12.791048795814937` |
| `recovery_factor` | `3.6649014228290686` |
| `net_profit` | `574.4` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `12.791048795814937` |
| `equity_dd_amount` | `156.73000000000002` |
| `max_dd_pct` | `12.634612715441579` |
| `max_dd_amount` | `154.75` |
| `ulcer_index` | `7.982313017630929` |
| `worst_day` | `-32.99` |
| `worst_week` | `-52.949999999999996` |
| `min_free_margin` | `434.45` |
| `consecutive_losses` | `12` |
| `time_under_water` | `22259700.0` |
| `longest_recovery_duration` | `13237500.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `5.0` |
| `payoff_ratio` | `1.356317901355692` |
| `avg_win` | `7.8667123287671235` |
| `avg_loss` | `-5.800050505050505` |
| `long_count` | `179` |
| `short_count` | `238` |
| `long_expectancy` | `2.4958659217877095` |
| `short_expectancy` | `0.5363025210084033` |
| `mfe_mean` | `7.43537170263789` |
| `mfe_median` | `5.44` |
| `mfe_p90` | `15.874000000000002` |
| `mae_mean` | `6.0919424460431655` |
| `mae_median` | `4.57` |
| `mae_p90` | `12.41` |
| `no_trade_rate` | `0.8906090506975162` |
| `hold_distribution` | `{'p50': 5.0, 'p90': 5.0}` |
| `loss_trade_mfe` | `3.3790404040404036` |
| `realized_over_mfe` | `-4.151613587833123` |
| `rule_pass_rates` | `{'long_signal_rate': 0.046699557672677784, 'short_signal_rate': 0.06269139162980605}` |
| `win_trade_mae` | `3.1750228310502284` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0003 | completed | 2026-03-30 14:28:29 UTC | 54.29   | 285    | 6755  | 6720          | 35      
att_0002 | completed | 2026-03-30 14:27:25 UTC | 114.88  | 417    | 11756 | 11756         | 0       
att_0001 | completed | 2026-03-30 14:17:45 UTC | 114.88  | 417    | 11756 | 11756         | 0       
```

### 29. `05_optimization` / `05DZ_05ca_margin06875_hold5_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05DZ_05ca_margin06875_hold5_0001\experiment_bundle.json`
- experiment_id: `exp_05dz_05ca_margin06875_hold5_v1`
- bundle_status: `completed`
- latest_attempt: `att_0001`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-30T14:19:28.686360+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: max_probability_margin(min_margin=0.06875) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=5)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `114.53799999999998` |
| `profit_factor` | `1.5253988495518391` |
| `trade_count` | `396` |
| `win_rate` | `0.5404040404040404` |
| `expectancy_per_trade` | `1.4461868686868686` |
| `max_dd_pct` | `12.603127209868777` |
| `recovery_factor` | `3.9761855169062006` |
| `net_profit` | `572.6899999999999` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `12.603127209868777` |
| `equity_dd_amount` | `144.02999999999997` |
| `max_dd_pct` | `11.794088507265531` |
| `max_dd_amount` | `142.85000000000014` |
| `ulcer_index` | `7.399184268127321` |
| `worst_day` | `-33.45` |
| `worst_week` | `-52.25` |
| `min_free_margin` | `434.37` |
| `consecutive_losses` | `10` |
| `time_under_water` | `22251000.0` |
| `longest_recovery_duration` | `13237500.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `5.0` |
| `payoff_ratio` | `1.2973018253197883` |
| `avg_win` | `7.769626168224299` |
| `avg_loss` | `-5.989065934065934` |
| `long_count` | `171` |
| `short_count` | `225` |
| `long_expectancy` | `2.623216374269006` |
| `short_expectancy` | `0.5516444444444444` |
| `mfe_mean` | `7.464621212121211` |
| `mfe_median` | `5.495` |
| `mfe_p90` | `15.579999999999998` |
| `mae_mean` | `6.218939393939394` |
| `mae_median` | `4.640000000000001` |
| `mae_p90` | `12.48` |
| `no_trade_rate` | `0.8960530792786662` |
| `hold_distribution` | `{'p50': 5.0, 'p90': 5.0}` |
| `loss_trade_mfe` | `3.364835164835165` |
| `realized_over_mfe` | `-4.945018040385258` |
| `rule_pass_rates` | `{'long_signal_rate': 0.04465804695474651, 'short_signal_rate': 0.05928887376658727}` |
| `win_trade_mae` | `3.3115420560747664` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0001 | completed | 2026-03-30 14:19:28 UTC | 114.54  | 396    | 11756 | 11756         | 0       
```

### 30. `05_optimization` / `05DN_05ca_margin_hold5_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05DN_05ca_margin_hold5_0001\experiment_bundle.json`
- experiment_id: `exp_05dn_05ca_margin_hold5_v1`
- bundle_status: `completed`
- latest_attempt: `att_0003`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-30T13:44:44.133372+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: max_probability_margin(min_margin=0.07) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=5)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `109.31399999999998` |
| `profit_factor` | `1.502371367120719` |
| `trade_count` | `388` |
| `win_rate` | `0.5335051546391752` |
| `expectancy_per_trade` | `1.4086855670103091` |
| `max_dd_pct` | `13.223854796888505` |
| `recovery_factor` | `3.571419236800837` |
| `net_profit` | `546.5699999999999` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `13.223854796888505` |
| `equity_dd_amount` | `153.03999999999996` |
| `max_dd_pct` | `12.63439962601844` |
| `max_dd_amount` | `151.35000000000014` |
| `ulcer_index` | `7.514788686125801` |
| `worst_day` | `-33.45` |
| `worst_week` | `-52.25` |
| `min_free_margin` | `431.21` |
| `consecutive_losses` | `10` |
| `time_under_water` | `22266600.0` |
| `longest_recovery_duration` | `13237500.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `5.0` |
| `payoff_ratio` | `1.3136677171442037` |
| `avg_win` | `7.896376811594203` |
| `avg_loss` | `-6.010939226519337` |
| `long_count` | `167` |
| `short_count` | `221` |
| `long_expectancy` | `2.707904191616766` |
| `short_expectancy` | `0.4269230769230769` |
| `mfe_mean` | `7.477654639175258` |
| `mfe_median` | `5.53` |
| `mfe_p90` | `15.683000000000002` |
| `mae_mean` | `6.3014432989690725` |
| `mae_median` | `4.73` |
| `mae_p90` | `12.560000000000002` |
| `no_trade_rate` | `0.8985199047294998` |
| `hold_distribution` | `{'p50': 5.0, 'p90': 5.0}` |
| `loss_trade_mfe` | `3.388121546961326` |
| `realized_over_mfe` | `-5.064488635468436` |
| `rule_pass_rates` | `{'long_signal_rate': 0.044062606328683224, 'short_signal_rate': 0.057417488941816947}` |
| `win_trade_mae` | `3.3711594202898554` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0003 | completed | 2026-03-30 13:44:44 UTC | 60.94   | 263    | 6755  | 6720          | 35      
att_0002 | completed | 2026-03-30 13:43:39 UTC | 109.31  | 388    | 11756 | 11756         | 0       
att_0001 | completed | 2026-03-30 13:41:55 UTC | 109.31  | 388    | 11756 | 11756         | 0       
```

### 31. `05_optimization` / `05EM_05dp_short_bias_margin_hold5_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05EM_05dp_short_bias_margin_hold5_0001\experiment_bundle.json`
- experiment_id: `exp_05em_05dp_short_bias_margin_hold5_v1`
- bundle_status: `completed`
- latest_attempt: `att_0002`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-30T15:08:30.950548+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3, long_threshold=0.45) | filters: max_probability_margin(min_margin=0.0675) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=5)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `109.204` |
| `profit_factor` | `1.528879030617681` |
| `trade_count` | `356` |
| `win_rate` | `0.5280898876404494` |
| `expectancy_per_trade` | `1.5337640449438201` |
| `max_dd_pct` | `13.0565608779599` |
| `recovery_factor` | `3.4954228282440294` |
| `net_profit` | `546.02` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `13.0565608779599` |
| `equity_dd_amount` | `156.21000000000004` |
| `max_dd_pct` | `12.513122863597806` |
| `max_dd_amount` | `148.99` |
| `ulcer_index` | `7.98816665769608` |
| `worst_day` | `-43.46` |
| `worst_week` | `-51.34` |
| `min_free_margin` | `446.92` |
| `consecutive_losses` | `9` |
| `time_under_water` | `22314000.0` |
| `longest_recovery_duration` | `13839900.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `5.0` |
| `payoff_ratio` | `1.3662323252328212` |
| `avg_win` | `8.395904255319149` |
| `avg_loss` | `-6.14529761904762` |
| `long_count` | `127` |
| `short_count` | `229` |
| `long_expectancy` | `3.076299212598425` |
| `short_expectancy` | `0.678296943231441` |
| `mfe_mean` | `7.8822752808988765` |
| `mfe_median` | `5.8` |
| `mfe_p90` | `16.48` |
| `mae_mean` | `6.533988764044944` |
| `mae_median` | `5.039999999999999` |
| `mae_p90` | `12.6` |
| `no_trade_rate` | `0.905239877509357` |
| `hold_distribution` | `{'p50': 5.0, 'p90': 5.0}` |
| `loss_trade_mfe` | `3.5480357142857146` |
| `realized_over_mfe` | `-4.953017189261499` |
| `rule_pass_rates` | `{'long_signal_rate': 0.03402517863218782, 'short_signal_rate': 0.06073494385845526}` |
| `win_trade_mae` | `3.5055851063829784` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0002 | completed | 2026-03-30 15:08:30 UTC | 64.53   | 229    | 6755  | 6720          | 35      
att_0001 | completed | 2026-03-30 15:02:31 UTC | 109.20  | 356    | 11756 | 11756         | 0       
```

### 32. `05_optimization` / `05DE_05bb_margin_hold2_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05DE_05bb_margin_hold2_0001\experiment_bundle.json`
- experiment_id: `exp_05de_05bb_margin_hold2_v1`
- bundle_status: `completed`
- latest_attempt: `att_0002`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-30T13:21:54.854126+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: max_probability_margin(min_margin=0.07) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=2)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `107.67599999999999` |
| `profit_factor` | `1.4762696720658874` |
| `trade_count` | `580` |
| `win_rate` | `0.5793103448275863` |
| `expectancy_per_trade` | `0.9282413793103448` |
| `max_dd_pct` | `11.33523295340931` |
| `recovery_factor` | `5.743945375013335` |
| `net_profit` | `538.38` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `11.33523295340931` |
| `equity_dd_amount` | `93.73000000000002` |
| `max_dd_pct` | `11.32023595280943` |
| `max_dd_amount` | `92.36999999999989` |
| `ulcer_index` | `4.874134184019687` |
| `worst_day` | `-27.96` |
| `worst_week` | `-43.150000000000006` |
| `min_free_margin` | `478.15` |
| `consecutive_losses` | `5` |
| `time_under_water` | `22071300.0` |
| `longest_recovery_duration` | `12813000.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `2.0` |
| `payoff_ratio` | `1.072052976143085` |
| `avg_win` | `4.966636904761905` |
| `avg_loss` | `-4.632827868852459` |
| `long_count` | `245` |
| `short_count` | `335` |
| `long_expectancy` | `1.4798367346938777` |
| `short_expectancy` | `0.5248358208955224` |
| `mfe_mean` | `5.070465517241379` |
| `mfe_median` | `3.32` |
| `mfe_p90` | `10.931000000000003` |
| `mae_mean` | `4.314086206896552` |
| `mae_median` | `3.0549999999999997` |
| `mae_p90` | `8.433000000000003` |
| `no_trade_rate` | `0.8987750935692412` |
| `hold_distribution` | `{'p50': 2.0, 'p90': 2.0}` |
| `loss_trade_mfe` | `2.079713114754098` |
| `realized_over_mfe` | `-4.20747981520907` |
| `rule_pass_rates` | `{'long_signal_rate': 0.043382102756039466, 'short_signal_rate': 0.05784280367471929}` |
| `win_trade_mae` | `2.4878869047619045` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0002 | completed | 2026-03-30 13:21:54 UTC | 33.05   | 404    | 6755  | 6720          | 35      
att_0001 | completed | 2026-03-30 13:11:39 UTC | 107.68  | 580    | 11756 | 11756         | 0       
```

### 33. `05_optimization` / `05DX_05ca_margin0650_hold5_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05DX_05ca_margin0650_hold5_0001\experiment_bundle.json`
- experiment_id: `exp_05dx_05ca_margin0650_hold5_v1`
- bundle_status: `completed`
- latest_attempt: `att_0001`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-30T14:15:57.595630+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: max_probability_margin(min_margin=0.065) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=5)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `106.70200000000001` |
| `profit_factor` | `1.4447065491918745` |
| `trade_count` | `433` |
| `win_rate` | `0.5265588914549654` |
| `expectancy_per_trade` | `1.2321247113163971` |
| `max_dd_pct` | `14.81034873864302` |
| `recovery_factor` | `3.3575204531151694` |
| `net_profit` | `533.51` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `14.81034873864302` |
| `equity_dd_amount` | `158.89999999999986` |
| `max_dd_pct` | `13.29410078493199` |
| `max_dd_amount` | `157.67999999999984` |
| `ulcer_index` | `8.466105938809523` |
| `worst_day` | `-35.78` |
| `worst_week` | `-60.52` |
| `min_free_margin` | `433.69` |
| `consecutive_losses` | `13` |
| `time_under_water` | `22499400.0` |
| `longest_recovery_duration` | `13237500.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `5.0` |
| `payoff_ratio` | `1.2989686078260274` |
| `avg_win` | `7.601754385964912` |
| `avg_loss` | `-5.852146341463415` |
| `long_count` | `182` |
| `short_count` | `251` |
| `long_expectancy` | `2.2947802197802196` |
| `short_expectancy` | `0.4615936254980079` |
| `mfe_mean` | `7.248614318706697` |
| `mfe_median` | `5.37` |
| `mfe_p90` | `15.604` |
| `mae_mean` | `6.0947113163972295` |
| `mae_median` | `4.57` |
| `mae_p90` | `12.066` |
| `no_trade_rate` | `0.8865260292616536` |
| `hold_distribution` | `{'p50': 5.0, 'p90': 5.0}` |
| `loss_trade_mfe` | `3.46209756097561` |
| `realized_over_mfe` | `-4.027954512265989` |
| `rule_pass_rates` | `{'long_signal_rate': 0.048230690711126234, 'short_signal_rate': 0.06524328002722014}` |
| `win_trade_mae` | `3.173991228070175` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0001 | completed | 2026-03-30 14:15:57 UTC | 106.70  | 433    | 11756 | 11756         | 0       
```

### 34. `05_optimization` / `05DQ_05ca_margin0725_hold5_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05DQ_05ca_margin0725_hold5_0001\experiment_bundle.json`
- experiment_id: `exp_05dq_05ca_margin0725_hold5_v1`
- bundle_status: `completed`
- latest_attempt: `att_0003`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-30T14:08:53.040804+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: max_probability_margin(min_margin=0.0725) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=5)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `106.636` |
| `profit_factor` | `1.5020858248660456` |
| `trade_count` | `375` |
| `win_rate` | `0.5333333333333333` |
| `expectancy_per_trade` | `1.4218133333333332` |
| `max_dd_pct` | `15.840339435845053` |
| `recovery_factor` | `3.8855851916630217` |
| `net_profit` | `533.18` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `15.840339435845053` |
| `equity_dd_amount` | `137.22000000000003` |
| `max_dd_pct` | `13.527999999999999` |
| `max_dd_amount` | `135.97000000000003` |
| `ulcer_index` | `7.528352947112868` |
| `worst_day` | `-32.99` |
| `worst_week` | `-52.25` |
| `min_free_margin` | `417.89` |
| `consecutive_losses` | `10` |
| `time_under_water` | `22814100.0` |
| `longest_recovery_duration` | `13237500.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `5.0` |
| `payoff_ratio` | `1.31432509675779` |
| `avg_win` | `7.975549999999999` |
| `avg_loss` | `-6.0681714285714285` |
| `long_count` | `158` |
| `short_count` | `217` |
| `long_expectancy` | `2.7790506329113924` |
| `short_expectancy` | `0.4335944700460829` |
| `mfe_mean` | `7.536479999999999` |
| `mfe_median` | `5.44` |
| `mfe_p90` | `15.896000000000003` |
| `mae_mean` | `6.37112` |
| `mae_median` | `4.81` |
| `mae_p90` | `12.484000000000002` |
| `no_trade_rate` | `0.903453555631167` |
| `hold_distribution` | `{'p50': 5.0, 'p90': 5.0}` |
| `loss_trade_mfe` | `3.4064` |
| `realized_over_mfe` | `-5.276931978634` |
| `rule_pass_rates` | `{'long_signal_rate': 0.041680843824430075, 'short_signal_rate': 0.05486560054440286}` |
| `win_trade_mae` | `3.4406499999999998` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0003 | completed | 2026-03-30 14:08:53 UTC | 54.48   | 250    | 6755  | 6720          | 35      
att_0002 | completed | 2026-03-30 14:07:48 UTC | 106.64  | 375    | 11756 | 11756         | 0       
att_0001 | completed | 2026-03-30 13:56:22 UTC | 106.64  | 375    | 11756 | 11756         | 0       
```

### 35. `05_optimization` / `05EH_05ca_plus_leader_session_margin0675_hold5_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05EH_05ca_plus_leader_session_margin0675_hold5_0001\experiment_bundle.json`
- experiment_id: `exp_05eh_05ca_plus_leader_session_margin0675_hold5_v1`
- bundle_status: `completed`
- latest_attempt: `att_0003`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-30T14:48:33.142998+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: max_probability_margin(min_margin=0.0675) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=5)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `106.01599999999998` |
| `profit_factor` | `1.4650314068147523` |
| `trade_count` | `406` |
| `win_rate` | `0.5320197044334976` |
| `expectancy_per_trade` | `1.3056157635467978` |
| `max_dd_pct` | `14.44137882862431` |
| `recovery_factor` | `3.6389098647628177` |
| `net_profit` | `530.0799999999999` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `14.44137882862431` |
| `equity_dd_amount` | `145.67000000000007` |
| `max_dd_pct` | `12.28718264453623` |
| `max_dd_amount` | `143.69000000000005` |
| `ulcer_index` | `7.691507979312206` |
| `worst_day` | `-32.99` |
| `worst_week` | `-52.949999999999996` |
| `min_free_margin` | `434.37` |
| `consecutive_losses` | `11` |
| `time_under_water` | `22437600.0` |
| `longest_recovery_duration` | `13237500.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `5.0` |
| `payoff_ratio` | `1.2886850337722358` |
| `avg_win` | `7.731296296296296` |
| `avg_loss` | `-5.999368421052632` |
| `long_count` | `173` |
| `short_count` | `233` |
| `long_expectancy` | `2.3571676300578037` |
| `short_expectancy` | `0.5248497854077253` |
| `mfe_mean` | `7.432019704433498` |
| `mfe_median` | `5.53` |
| `mfe_p90` | `15.885` |
| `mae_mean` | `6.194384236453202` |
| `mae_median` | `4.605` |
| `mae_p90` | `12.43` |
| `no_trade_rate` | `0.8935862538278326` |
| `hold_distribution` | `{'p50': 5.0, 'p90': 5.0}` |
| `loss_trade_mfe` | `3.492578947368421` |
| `realized_over_mfe` | `-4.234378739950423` |
| `rule_pass_rates` | `{'long_signal_rate': 0.04533855052739027, 'short_signal_rate': 0.06107519564477713}` |
| `win_trade_mae` | `3.1985185185185183` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0003 | completed | 2026-03-30 14:48:33 UTC | 54.94   | 280    | 6755  | 6720          | 35      
att_0002 | completed | 2026-03-30 14:47:27 UTC | 106.02  | 406    | 11756 | 11756         | 0       
att_0001 | completed | 2026-03-30 14:45:42 UTC | 106.02  | 406    | 11756 | 11756         | 0       
```

### 36. `05_optimization` / `05EE_05ca_plus_downside_margin0675_hold5_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05EE_05ca_plus_downside_margin0675_hold5_0001\experiment_bundle.json`
- experiment_id: `exp_05ee_05ca_plus_downside_margin0675_hold5_v1`
- bundle_status: `completed`
- latest_attempt: `att_0003`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-30T14:51:23.888698+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: max_probability_margin(min_margin=0.0675) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=5)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `105.41199999999999` |
| `profit_factor` | `1.4590235320757345` |
| `trade_count` | `408` |
| `win_rate` | `0.5367647058823529` |
| `expectancy_per_trade` | `1.291813725490196` |
| `max_dd_pct` | `14.716524503814071` |
| `recovery_factor` | `3.825096160824444` |
| `net_profit` | `527.06` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `14.716524503814071` |
| `equity_dd_amount` | `137.78999999999996` |
| `max_dd_pct` | `11.760696444440605` |
| `max_dd_amount` | `136.30999999999995` |
| `ulcer_index` | `7.601667171654112` |
| `worst_day` | `-32.99` |
| `worst_week` | `-52.25` |
| `min_free_margin` | `434.37` |
| `consecutive_losses` | `10` |
| `time_under_water` | `22111800.0` |
| `longest_recovery_duration` | `13237500.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `5.0` |
| `payoff_ratio` | `1.259157294805086` |
| `avg_win` | `7.6496803652968035` |
| `avg_loss` | `-6.075238095238095` |
| `long_count` | `174` |
| `short_count` | `234` |
| `long_expectancy` | `2.342701149425287` |
| `short_expectancy` | `0.5103846153846153` |
| `mfe_mean` | `7.415294117647059` |
| `mfe_median` | `5.53` |
| `mfe_p90` | `15.683000000000002` |
| `mae_mean` | `6.184485294117647` |
| `mae_median` | `4.5600000000000005` |
| `mae_p90` | `12.422` |
| `no_trade_rate` | `0.8931609390949302` |
| `hold_distribution` | `{'p50': 5.0, 'p90': 5.0}` |
| `loss_trade_mfe` | `3.507671957671958` |
| `realized_over_mfe` | `-4.1640927376590415` |
| `rule_pass_rates` | `{'long_signal_rate': 0.04533855052739027, 'short_signal_rate': 0.061500510377679486}` |
| `win_trade_mae` | `3.1658447488584476` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0003 | completed | 2026-03-30 14:51:23 UTC | 57.08   | 278    | 6755  | 6720          | 35      
att_0002 | completed | 2026-03-30 14:50:17 UTC | 105.41  | 408    | 11756 | 11756         | 0       
att_0001 | completed | 2026-03-30 14:40:31 UTC | 105.41  | 408    | 11756 | 11756         | 0       
```

### 37. `05_optimization` / `05DI_05bf_margin_hold4_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05DI_05bf_margin_hold4_0001\experiment_bundle.json`
- experiment_id: `exp_05di_05bf_margin_hold4_v1`
- bundle_status: `completed`
- latest_attempt: `att_0001`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-30T13:18:10.257566+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: max_probability_margin(min_margin=0.07) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=4)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `104.53599999999999` |
| `profit_factor` | `1.505869941832893` |
| `trade_count` | `427` |
| `win_rate` | `0.550351288056206` |
| `expectancy_per_trade` | `1.2240749414519905` |
| `max_dd_pct` | `11.542344851597191` |
| `recovery_factor` | `3.941482542794657` |
| `net_profit` | `522.68` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `11.542344851597191` |
| `equity_dd_amount` | `132.61000000000013` |
| `max_dd_pct` | `11.421032464818168` |
| `max_dd_amount` | `131.14999999999998` |
| `ulcer_index` | `6.63490771268183` |
| `worst_day` | `-38.519999999999996` |
| `worst_week` | `-39.69` |
| `min_free_margin` | `452.33` |
| `consecutive_losses` | `8` |
| `time_under_water` | `22066200.0` |
| `longest_recovery_duration` | `13236300.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `4.0` |
| `payoff_ratio` | `1.23032778226347` |
| `avg_win` | `6.620893617021277` |
| `avg_loss` | `-5.38140625` |
| `long_count` | `182` |
| `short_count` | `245` |
| `long_expectancy` | `1.72478021978022` |
| `short_expectancy` | `0.8521224489795918` |
| `mfe_mean` | `6.706814988290398` |
| `mfe_median` | `5.14` |
| `mfe_p90` | `14.312000000000005` |
| `mae_mean` | `5.934121779859485` |
| `mae_median` | `4.35` |
| `mae_p90` | `12.476000000000003` |
| `no_trade_rate` | `0.8989452194624021` |
| `hold_distribution` | `{'p50': 4.0, 'p90': 4.0}` |
| `loss_trade_mfe` | `3.0589583333333334` |
| `realized_over_mfe` | `-4.09355619593084` |
| `rule_pass_rates` | `{'long_signal_rate': 0.04363729159578088, 'short_signal_rate': 0.057417488941816947}` |
| `win_trade_mae` | `3.448595744680851` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0001 | completed | 2026-03-30 13:18:10 UTC | 104.54  | 427    | 11756 | 11756         | 0       
```

### 38. `05_optimization` / `05EL_05dp_combo_loose_hold5_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05EL_05dp_combo_loose_hold5_0001\experiment_bundle.json`
- experiment_id: `exp_05el_05dp_combo_loose_hold5_v1`
- bundle_status: `completed`
- latest_attempt: `att_0002`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-30T15:09:34.765669+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: combo_probability_gate(min_margin=0.05, min_probability_diff=0.07) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=5)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `103.32999999999998` |
| `profit_factor` | `1.4582099082959363` |
| `trade_count` | `395` |
| `win_rate` | `0.5265822784810127` |
| `expectancy_per_trade` | `1.3079746835443038` |
| `max_dd_pct` | `13.75110416525106` |
| `recovery_factor` | `3.191167387276099` |
| `net_profit` | `516.65` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `13.75110416525106` |
| `equity_dd_amount` | `161.89999999999986` |
| `max_dd_pct` | `13.613343983141574` |
| `max_dd_amount` | `160.20999999999992` |
| `ulcer_index` | `7.948823490356952` |
| `worst_day` | `-33.45` |
| `worst_week` | `-52.25` |
| `min_free_margin` | `432.39` |
| `consecutive_losses` | `10` |
| `time_under_water` | `22269900.0` |
| `longest_recovery_duration` | `13237500.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `5.0` |
| `payoff_ratio` | `1.3109867925545198` |
| `avg_win` | `7.904759615384616` |
| `avg_loss` | `-6.029625668449198` |
| `long_count` | `171` |
| `short_count` | `224` |
| `long_expectancy` | `2.6025146198830407` |
| `short_expectancy` | `0.3197321428571428` |
| `mfe_mean` | `7.378151898734177` |
| `mfe_median` | `5.37` |
| `mfe_p90` | `15.588000000000001` |
| `mae_mean` | `6.318936708860759` |
| `mae_median` | `4.8` |
| `mae_p90` | `12.620000000000005` |
| `no_trade_rate` | `0.89673358285131` |
| `hold_distribution` | `{'p50': 5.0, 'p90': 5.0}` |
| `loss_trade_mfe` | `3.3162566844919787` |
| `realized_over_mfe` | `-5.101278768184318` |
| `rule_pass_rates` | `{'long_signal_rate': 0.04482817284790745, 'short_signal_rate': 0.05843824430078258}` |
| `win_trade_mae` | `3.356009615384615` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0002 | completed | 2026-03-30 15:09:34 UTC | 56.37   | 270    | 6755  | 6720          | 35      
att_0001 | completed | 2026-03-30 15:00:52 UTC | 103.33  | 395    | 11756 | 11756         | 0       
```

### 39. `05_optimization` / `05EF_05ca_plus_leader_margin0675_hold5_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05EF_05ca_plus_leader_margin0675_hold5_0001\experiment_bundle.json`
- experiment_id: `exp_05ef_05ca_plus_leader_margin0675_hold5_v1`
- bundle_status: `completed`
- latest_attempt: `att_0001`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-30T14:42:15.390358+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: max_probability_margin(min_margin=0.0675) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=5)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `102.84599999999999` |
| `profit_factor` | `1.4496550397425696` |
| `trade_count` | `405` |
| `win_rate` | `0.5333333333333333` |
| `expectancy_per_trade` | `1.2697037037037038` |
| `max_dd_pct` | `14.289169949547304` |
| `recovery_factor` | `3.505078045123034` |
| `net_profit` | `514.23` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `14.289169949547304` |
| `equity_dd_amount` | `146.70999999999992` |
| `max_dd_pct` | `12.534859953924226` |
| `max_dd_amount` | `144.7299999999999` |
| `ulcer_index` | `7.788944921321123` |
| `worst_day` | `-32.99` |
| `worst_week` | `-52.949999999999996` |
| `min_free_margin` | `434.37` |
| `consecutive_losses` | `11` |
| `time_under_water` | `22533900.0` |
| `longest_recovery_duration` | `13237500.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `5.0` |
| `payoff_ratio` | `1.2684481597747483` |
| `avg_win` | `7.6751851851851844` |
| `avg_loss` | `-6.05084656084656` |
| `long_count` | `172` |
| `short_count` | `233` |
| `long_expectancy` | `2.3325` |
| `short_expectancy` | `0.48515021459227464` |
| `mfe_mean` | `7.406567901234568` |
| `mfe_median` | `5.53` |
| `mfe_p90` | `15.588000000000001` |
| `mae_mean` | `6.243382716049383` |
| `mae_median` | `4.65` |
| `mae_p90` | `12.456` |
| `no_trade_rate` | `0.8937563797209935` |
| `hold_distribution` | `{'p50': 5.0, 'p90': 5.0}` |
| `loss_trade_mfe` | `3.492275132275132` |
| `realized_over_mfe` | `-4.229327157233439` |
| `rule_pass_rates` | `{'long_signal_rate': 0.04516842463422933, 'short_signal_rate': 0.06107519564477713}` |
| `win_trade_mae` | `3.26` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0001 | completed | 2026-03-30 14:42:15 UTC | 102.85  | 405    | 11756 | 11756         | 0       
```

### 40. `05_optimization` / `05ER_05dp_short_bias_margin_hold4_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05ER_05dp_short_bias_margin_hold4_0001\experiment_bundle.json`
- experiment_id: `exp_05er_05dp_short_bias_margin_hold4_v1`
- bundle_status: `completed`
- latest_attempt: `att_0002`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-30T15:53:46.488049+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3, long_threshold=0.45) | filters: max_probability_margin(min_margin=0.0675) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=4)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `102.63399999999999` |
| `profit_factor` | `1.5067244648076468` |
| `trade_count` | `397` |
| `win_rate` | `0.5365239294710328` |
| `expectancy_per_trade` | `1.2926196473551637` |
| `max_dd_pct` | `12.658183658864392` |
| `recovery_factor` | `3.538127413127414` |
| `net_profit` | `513.17` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `12.658183658864392` |
| `equity_dd_amount` | `145.03999999999996` |
| `max_dd_pct` | `12.151778822538766` |
| `max_dd_amount` | `138.53999999999996` |
| `ulcer_index` | `7.85856615978448` |
| `worst_day` | `-22.8` |
| `worst_week` | `-40.41` |
| `min_free_margin` | `455.02` |
| `consecutive_losses` | `8` |
| `time_under_water` | `22062300.0` |
| `longest_recovery_duration` | `13839900.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `4.0` |
| `payoff_ratio` | `1.3015835752328968` |
| `avg_win` | `7.163802816901409` |
| `avg_loss` | `-5.503913043478261` |
| `long_count` | `138` |
| `short_count` | `259` |
| `long_expectancy` | `1.9817391304347827` |
| `short_expectancy` | `0.9254440154440154` |
| `mfe_mean` | `7.007783375314862` |
| `mfe_median` | `5.41` |
| `mfe_p90` | `15.628` |
| `mae_mean` | `6.1464483627204025` |
| `mae_median` | `4.78` |
| `mae_p90` | `12.744000000000003` |
| `no_trade_rate` | `0.905239877509357` |
| `hold_distribution` | `{'p50': 4.0, 'p90': 4.0}` |
| `loss_trade_mfe` | `3.102989130434783` |
| `realized_over_mfe` | `-5.012544520220555` |
| `rule_pass_rates` | `{'long_signal_rate': 0.03402517863218782, 'short_signal_rate': 0.06073494385845526}` |
| `win_trade_mae` | `3.560281690140845` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0002 | completed | 2026-03-30 15:53:46 UTC | 49.45   | 249    | 6755  | 6720          | 35      
att_0001 | completed | 2026-03-30 15:44:25 UTC | 102.63  | 397    | 11756 | 11756         | 0       
```

### 41. `05_optimization` / `05DH_05bf_margin_hold2_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05DH_05bf_margin_hold2_0001\experiment_bundle.json`
- experiment_id: `exp_05dh_05bf_margin_hold2_v1`
- bundle_status: `completed`
- latest_attempt: `att_0001`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-30T13:16:32.867076+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: max_probability_margin(min_margin=0.07) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=2)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `102.28399999999999` |
| `profit_factor` | `1.44973838104032` |
| `trade_count` | `576` |
| `win_rate` | `0.5798611111111112` |
| `expectancy_per_trade` | `0.8878819444444443` |
| `max_dd_pct` | `12.447400747497452` |
| `recovery_factor` | `5.248024628014369` |
| `net_profit` | `511.41999999999996` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `12.447400747497452` |
| `equity_dd_amount` | `97.44999999999993` |
| `max_dd_pct` | `11.907923278162663` |
| `max_dd_amount` | `96.08999999999992` |
| `ulcer_index` | `5.160827315177043` |
| `worst_day` | `-27.96` |
| `worst_week` | `-43.150000000000006` |
| `min_free_margin` | `478.15` |
| `consecutive_losses` | `6` |
| `time_under_water` | `22478400.0` |
| `longest_recovery_duration` | `13157100.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `2.0` |
| `payoff_ratio` | `1.0504092461429864` |
| `avg_win` | `4.935838323353293` |
| `avg_loss` | `-4.69896694214876` |
| `long_count` | `246` |
| `short_count` | `330` |
| `long_expectancy` | `1.4034552845528456` |
| `short_expectancy` | `0.5035454545454545` |
| `mfe_mean` | `5.076059027777777` |
| `mfe_median` | `3.32` |
| `mfe_p90` | `10.975` |
| `mae_mean` | `4.358402777777778` |
| `mae_median` | `3.0700000000000003` |
| `mae_p90` | `8.645` |
| `no_trade_rate` | `0.8989452194624021` |
| `hold_distribution` | `{'p50': 2.0, 'p90': 2.0}` |
| `loss_trade_mfe` | `2.0562809917355374` |
| `realized_over_mfe` | `-4.255577981691235` |
| `rule_pass_rates` | `{'long_signal_rate': 0.04363729159578088, 'short_signal_rate': 0.057417488941816947}` |
| `win_trade_mae` | `2.51874251497006` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0001 | completed | 2026-03-30 13:16:32 UTC | 102.28  | 576    | 11756 | 11756         | 0       
```

### 42. `05_optimization` / `05DR_05cc_margin0675_hold5_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05DR_05cc_margin0675_hold5_0001\experiment_bundle.json`
- experiment_id: `exp_05dr_05cc_margin0675_hold5_v1`
- bundle_status: `completed`
- latest_attempt: `att_0001`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-30T13:58:06.204827+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: max_probability_margin(min_margin=0.0675) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=5)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `102.06` |
| `profit_factor` | `1.4440209872353755` |
| `trade_count` | `408` |
| `win_rate` | `0.5318627450980392` |
| `expectancy_per_trade` | `1.250735294117647` |
| `max_dd_pct` | `14.271744132535671` |
| `recovery_factor` | `3.5300221361372452` |
| `net_profit` | `510.3` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `14.271744132535671` |
| `equity_dd_amount` | `144.55999999999995` |
| `max_dd_pct` | `12.414021279189226` |
| `max_dd_amount` | `142.57999999999993` |
| `ulcer_index` | `7.867074205949992` |
| `worst_day` | `-32.99` |
| `worst_week` | `-52.949999999999996` |
| `min_free_margin` | `434.37` |
| `consecutive_losses` | `12` |
| `time_under_water` | `22538700.0` |
| `longest_recovery_duration` | `13237500.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `5.0` |
| `payoff_ratio` | `1.2710046477509527` |
| `avg_win` | `7.64778801843318` |
| `avg_loss` | `-6.017120418848167` |
| `long_count` | `175` |
| `short_count` | `233` |
| `long_expectancy` | `2.2837714285714283` |
| `short_expectancy` | `0.47484978540772527` |
| `mfe_mean` | `7.3674019607843135` |
| `mfe_median` | `5.495` |
| `mfe_p90` | `15.564` |
| `mae_mean` | `6.211397058823529` |
| `mae_median` | `4.605` |
| `mae_p90` | `12.453` |
| `no_trade_rate` | `0.8926505614154474` |
| `hold_distribution` | `{'p50': 5.0, 'p90': 5.0}` |
| `loss_trade_mfe` | `3.4612565445026178` |
| `realized_over_mfe` | `-4.206153464016148` |
| `rule_pass_rates` | `{'long_signal_rate': 0.045933991153453556, 'short_signal_rate': 0.061415447431099016}` |
| `win_trade_mae` | `3.2138709677419355` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0001 | completed | 2026-03-30 13:58:06 UTC | 102.06  | 408    | 11756 | 11756         | 0       
```

### 43. `05_optimization` / `05EB_05ca_margin0675_hold6_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05EB_05ca_margin0675_hold6_0001\experiment_bundle.json`
- experiment_id: `exp_05eb_05ca_margin0675_hold6_v1`
- bundle_status: `completed`
- latest_attempt: `att_0001`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-30T14:22:55.638430+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: max_probability_margin(min_margin=0.0675) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=6)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `100.69999999999999` |
| `profit_factor` | `1.4368157132198567` |
| `trade_count` | `373` |
| `win_rate` | `0.546916890080429` |
| `expectancy_per_trade` | `1.3498659517426272` |
| `max_dd_pct` | `14.158326532365445` |
| `recovery_factor` | `3.055033068381774` |
| `net_profit` | `503.5` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `14.158326532365445` |
| `equity_dd_amount` | `164.80999999999995` |
| `max_dd_pct` | `13.874849578820703` |
| `max_dd_amount` | `161.42000000000007` |
| `ulcer_index` | `9.007362614079081` |
| `worst_day` | `-42.32` |
| `worst_week` | `-53.64` |
| `min_free_margin` | `436.32` |
| `consecutive_losses` | `13` |
| `time_under_water` | `23117700.0` |
| `longest_recovery_duration` | `13237500.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `6.0` |
| `payoff_ratio` | `1.1903032134027245` |
| `avg_win` | `8.11843137254902` |
| `avg_loss` | `-6.820473372781065` |
| `long_count` | `161` |
| `short_count` | `212` |
| `long_expectancy` | `2.1861490683229814` |
| `short_expectancy` | `0.7147641509433962` |
| `mfe_mean` | `8.415656836461126` |
| `mfe_median` | `6.62` |
| `mfe_p90` | `18.668000000000013` |
| `mae_mean` | `6.639571045576408` |
| `mae_median` | `4.92` |
| `mae_p90` | `14.528000000000002` |
| `no_trade_rate` | `0.8937563797209935` |
| `hold_distribution` | `{'p50': 6.0, 'p90': 6.0}` |
| `loss_trade_mfe` | `3.970355029585799` |
| `realized_over_mfe` | `-4.992232073580726` |
| `rule_pass_rates` | `{'long_signal_rate': 0.04550867642055121, 'short_signal_rate': 0.06073494385845526}` |
| `win_trade_mae` | `3.6022058823529415` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0001 | completed | 2026-03-30 14:22:55 UTC | 100.70  | 373    | 11756 | 11756         | 0       
```

### 44. `05_optimization` / `05DG_05bb_margin_hold5_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05DG_05bb_margin_hold5_0001\experiment_bundle.json`
- experiment_id: `exp_05dg_05bb_margin_hold5_v1`
- bundle_status: `completed`
- latest_attempt: `att_0001`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-30T13:14:55.859458+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: max_probability_margin(min_margin=0.07) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=5)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `99.72999999999999` |
| `profit_factor` | `1.4494690919579598` |
| `trade_count` | `390` |
| `win_rate` | `0.5333333333333333` |
| `expectancy_per_trade` | `1.2785897435897435` |
| `max_dd_pct` | `14.833548572248526` |
| `recovery_factor` | `3.469835084545264` |
| `net_profit` | `498.65` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `14.833548572248526` |
| `equity_dd_amount` | `143.71000000000004` |
| `max_dd_pct` | `12.48433542778522` |
| `max_dd_amount` | `142.45999999999992` |
| `ulcer_index` | `7.353205479374556` |
| `worst_day` | `-32.99` |
| `worst_week` | `-52.25` |
| `min_free_margin` | `431.21` |
| `consecutive_losses` | `10` |
| `time_under_water` | `22593900.0` |
| `longest_recovery_duration` | `13237500.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `5.0` |
| `payoff_ratio` | `1.268285455463215` |
| `avg_win` | `7.731105769230769` |
| `avg_loss` | `-6.095714285714286` |
| `long_count` | `165` |
| `short_count` | `225` |
| `long_expectancy` | `2.5375757575757576` |
| `short_expectancy` | `0.3553333333333333` |
| `mfe_mean` | `7.447282051282051` |
| `mfe_median` | `5.62` |
| `mfe_p90` | `15.548` |
| `mae_mean` | `6.315871794871795` |
| `mae_median` | `4.73` |
| `mae_p90` | `12.450999999999999` |
| `no_trade_rate` | `0.8987750935692412` |
| `hold_distribution` | `{'p50': 5.0, 'p90': 5.0}` |
| `loss_trade_mfe` | `3.491043956043956` |
| `realized_over_mfe` | `-4.315625179410949` |
| `rule_pass_rates` | `{'long_signal_rate': 0.043382102756039466, 'short_signal_rate': 0.05784280367471929}` |
| `win_trade_mae` | `3.3310576923076924` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0001 | completed | 2026-03-30 13:14:55 UTC | 99.73   | 390    | 11756 | 11756         | 0       
```

### 45. `05_optimization` / `05DL_05cc_margin_hold5_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05DL_05cc_margin_hold5_0001\experiment_bundle.json`
- experiment_id: `exp_05dl_05cc_margin_hold5_v1`
- bundle_status: `completed`
- latest_attempt: `att_0003`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-30T13:47:35.093845+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: max_probability_margin(min_margin=0.07) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=5)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `99.68199999999999` |
| `profit_factor` | `1.4448341722894575` |
| `trade_count` | `393` |
| `win_rate` | `0.5318066157760815` |
| `expectancy_per_trade` | `1.2682188295165393` |
| `max_dd_pct` | `14.91613058377923` |
| `recovery_factor` | `3.4023482831592595` |
| `net_profit` | `498.40999999999997` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `14.91613058377923` |
| `equity_dd_amount` | `146.49` |
| `max_dd_pct` | `12.666089344914763` |
| `max_dd_amount` | `144.80000000000007` |
| `ulcer_index` | `7.6350328355652985` |
| `worst_day` | `-33.45` |
| `worst_week` | `-52.25` |
| `min_free_margin` | `439.85` |
| `consecutive_losses` | `10` |
| `time_under_water` | `22260900.0` |
| `longest_recovery_duration` | `13237500.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `5.0` |
| `payoff_ratio` | `1.2720071181878478` |
| `avg_win` | `7.745693779904306` |
| `avg_loss` | `-6.089347826086957` |
| `long_count` | `167` |
| `short_count` | `226` |
| `long_expectancy` | `2.589880239520958` |
| `short_expectancy` | `0.29159292035398227` |
| `mfe_mean` | `7.442544529262086` |
| `mfe_median` | `5.58` |
| `mfe_p90` | `15.476000000000003` |
| `mae_mean` | `6.29295165394402` |
| `mae_median` | `4.7` |
| `mae_p90` | `12.458` |
| `no_trade_rate` | `0.8973290234773733` |
| `hold_distribution` | `{'p50': 5.0, 'p90': 5.0}` |
| `loss_trade_mfe` | `3.4875000000000003` |
| `realized_over_mfe` | `-4.3268125574648915` |
| `rule_pass_rates` | `{'long_signal_rate': 0.044147669275263694, 'short_signal_rate': 0.05852330724736305}` |
| `win_trade_mae` | `3.296267942583732` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0003 | completed | 2026-03-30 13:47:35 UTC | 58.85   | 267    | 6755  | 6720          | 35      
att_0002 | completed | 2026-03-30 13:46:30 UTC | 99.68   | 393    | 11756 | 11756         | 0       
att_0001 | completed | 2026-03-30 13:38:25 UTC | 99.68   | 393    | 11756 | 11756         | 0       
```

### 46. `05_optimization` / `05ED_05ca_plus_breakout_margin0675_hold5_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05ED_05ca_plus_breakout_margin0675_hold5_0001\experiment_bundle.json`
- experiment_id: `exp_05ed_05ca_plus_breakout_margin0675_hold5_v1`
- bundle_status: `completed`
- latest_attempt: `att_0001`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-30T14:38:45.157488+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: max_probability_margin(min_margin=0.0675) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=5)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `99.014` |
| `profit_factor` | `1.4313170298220088` |
| `trade_count` | `401` |
| `win_rate` | `0.5336658354114713` |
| `expectancy_per_trade` | `1.2345885286783043` |
| `max_dd_pct` | `14.867446143303786` |
| `recovery_factor` | `2.852278619577115` |
| `net_profit` | `495.07` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `14.867446143303786` |
| `equity_dd_amount` | `173.57000000000005` |
| `max_dd_pct` | `14.728994387077424` |
| `max_dd_amount` | `171.88` |
| `ulcer_index` | `8.060746001771236` |
| `worst_day` | `-36.03` |
| `worst_week` | `-52.949999999999996` |
| `min_free_margin` | `434.37` |
| `consecutive_losses` | `10` |
| `time_under_water` | `22128000.0` |
| `longest_recovery_duration` | `13237500.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `5.0` |
| `payoff_ratio` | `1.2507303017603535` |
| `avg_win` | `7.677009345794392` |
| `avg_loss` | `-6.138021390374331` |
| `long_count` | `171` |
| `short_count` | `230` |
| `long_expectancy` | `2.4555555555555553` |
| `short_expectancy` | `0.3268260869565217` |
| `mfe_mean` | `7.428678304239401` |
| `mfe_median` | `5.53` |
| `mfe_p90` | `15.83` |
| `mae_mean` | `6.263167082294265` |
| `mae_median` | `4.63` |
| `mae_p90` | `12.45` |
| `no_trade_rate` | `0.8941816944538958` |
| `hold_distribution` | `{'p50': 5.0, 'p90': 5.0}` |
| `loss_trade_mfe` | `3.4929946524064173` |
| `realized_over_mfe` | `-4.290934726479657` |
| `rule_pass_rates` | `{'long_signal_rate': 0.045933991153453556, 'short_signal_rate': 0.05988431439265056}` |
| `win_trade_mae` | `3.240934579439253` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0001 | completed | 2026-03-30 14:38:45 UTC | 99.01   | 401    | 11756 | 11756         | 0       
```

### 47. `05_optimization` / `05ES_05dp_stronger_long_suppression_hold5_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05ES_05dp_stronger_long_suppression_hold5_0001\experiment_bundle.json`
- experiment_id: `exp_05es_05dp_stronger_long_suppression_hold5_v1`
- bundle_status: `completed`
- latest_attempt: `att_0002`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-30T15:54:51.204985+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3, long_threshold=0.5) | filters: max_probability_margin(min_margin=0.0675) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=5)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `96.932` |
| `profit_factor` | `1.5315886456368184` |
| `trade_count` | `309` |
| `win_rate` | `0.5145631067961165` |
| `expectancy_per_trade` | `1.5684789644012944` |
| `max_dd_pct` | `13.461997506873768` |
| `recovery_factor` | `3.182898798187433` |
| `net_profit` | `484.65999999999997` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `13.461997506873768` |
| `equity_dd_amount` | `152.26999999999987` |
| `max_dd_pct` | `12.966431989488344` |
| `max_dd_amount` | `146.04999999999984` |
| `ulcer_index` | `8.077650646661342` |
| `worst_day` | `-28.209999999999997` |
| `worst_week` | `-51.34` |
| `min_free_margin` | `456.68` |
| `consecutive_losses` | `9` |
| `time_under_water` | `22762500.0` |
| `longest_recovery_duration` | `13839900.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `5.0` |
| `payoff_ratio` | `1.4448949487139795` |
| `avg_win` | `8.782264150943396` |
| `avg_loss` | `-6.078133333333334` |
| `long_count` | `80` |
| `short_count` | `229` |
| `long_expectancy` | `4.116625` |
| `short_expectancy` | `0.678296943231441` |
| `mfe_mean` | `8.168867313915857` |
| `mfe_median` | `6.04` |
| `mfe_p90` | `16.813999999999993` |
| `mae_mean` | `6.739935275080906` |
| `mae_median` | `5.16` |
| `mae_p90` | `12.849999999999998` |
| `no_trade_rate` | `0.9174889418169445` |
| `hold_distribution` | `{'p50': 5.0, 'p90': 5.0}` |
| `loss_trade_mfe` | `3.693866666666667` |
| `realized_over_mfe` | `-4.909938963407745` |
| `rule_pass_rates` | `{'long_signal_rate': 0.021776114324600204, 'short_signal_rate': 0.06073494385845526}` |
| `win_trade_mae` | `3.6647798742138367` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0002 | completed | 2026-03-30 15:54:51 UTC | 47.79   | 190    | 6755  | 6720          | 35      
att_0001 | completed | 2026-03-30 15:46:05 UTC | 96.93   | 309    | 11756 | 11756         | 0       
```

### 48. `05_optimization` / `05EP_05dp_balanced_tight_margin_hold5_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05EP_05dp_balanced_tight_margin_hold5_0001\experiment_bundle.json`
- experiment_id: `exp_05ep_05dp_balanced_tight_margin_hold5_v1`
- bundle_status: `completed`
- latest_attempt: `att_0001`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-30T15:07:26.859684+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.45, long_threshold=0.45) | filters: max_probability_margin(min_margin=0.0675) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=5)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `95.90799999999999` |
| `profit_factor` | `1.5214318335036863` |
| `trade_count` | `289` |
| `win_rate` | `0.5570934256055363` |
| `expectancy_per_trade` | `1.6593079584775086` |
| `max_dd_pct` | `10.791144139959748` |
| `recovery_factor` | `4.04709258165246` |
| `net_profit` | `479.53999999999996` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `10.791144139959748` |
| `equity_dd_amount` | `118.49000000000001` |
| `max_dd_pct` | `10.32235029158923` |
| `max_dd_amount` | `112.75` |
| `ulcer_index` | `6.412903746977388` |
| `worst_day` | `-43.46` |
| `worst_week` | `-46.2` |
| `min_free_margin` | `446.92` |
| `consecutive_losses` | `6` |
| `time_under_water` | `21824700.0` |
| `longest_recovery_duration` | `13839900.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `5.0` |
| `payoff_ratio` | `1.2095855570712537` |
| `avg_win` | `8.690683229813665` |
| `avg_loss` | `-7.18484375` |
| `long_count` | `127` |
| `short_count` | `162` |
| `long_expectancy` | `3.076299212598425` |
| `short_expectancy` | `0.5484567901234567` |
| `mfe_mean` | `8.511349480968859` |
| `mfe_median` | `6.53` |
| `mfe_p90` | `18.48` |
| `mae_mean` | `7.103633217993079` |
| `mae_median` | `5.35` |
| `mae_p90` | `13.345999999999991` |
| `no_trade_rate` | `0.9262504253147329` |
| `hold_distribution` | `{'p50': 5.0, 'p90': 5.0}` |
| `loss_trade_mfe` | `3.814453125` |
| `realized_over_mfe` | `-4.519628972928074` |
| `rule_pass_rates` | `{'long_signal_rate': 0.03402517863218782, 'short_signal_rate': 0.03972439605307928}` |
| `win_trade_mae` | `3.669875776397516` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0001 | completed | 2026-03-30 15:07:26 UTC | 95.91   | 289    | 11756 | 11756         | 0       
```

### 49. `05_optimization` / `05EC_05ca_plus_volatility_margin0675_hold5_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05EC_05ca_plus_volatility_margin0675_hold5_0001\experiment_bundle.json`
- experiment_id: `exp_05ec_05ca_plus_volatility_margin0675_hold5_v1`
- bundle_status: `completed`
- latest_attempt: `att_0001`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-30T14:37:00.875613+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: max_probability_margin(min_margin=0.0675) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=5)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `95.752` |
| `profit_factor` | `1.4127276959284132` |
| `trade_count` | `404` |
| `win_rate` | `0.5321782178217822` |
| `expectancy_per_trade` | `1.185049504950495` |
| `max_dd_pct` | `14.785106433696452` |
| `recovery_factor` | `3.3446974989520752` |
| `net_profit` | `478.76` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `14.785106433696452` |
| `equity_dd_amount` | `143.14` |
| `max_dd_pct` | `12.627096705082085` |
| `max_dd_amount` | `141.45000000000005` |
| `ulcer_index` | `7.531671984276193` |
| `worst_day` | `-32.99` |
| `worst_week` | `-52.25` |
| `min_free_margin` | `434.37` |
| `consecutive_losses` | `9` |
| `time_under_water` | `22608000.0` |
| `longest_recovery_duration` | `13237500.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `5.0` |
| `payoff_ratio` | `1.2418862071184655` |
| `avg_win` | `7.622093023255814` |
| `avg_loss` | `-6.137513227513227` |
| `long_count` | `171` |
| `short_count` | `233` |
| `long_expectancy` | `2.375906432748538` |
| `short_expectancy` | `0.3110729613733905` |
| `mfe_mean` | `7.385371287128713` |
| `mfe_median` | `5.53` |
| `mfe_p90` | `15.595999999999998` |
| `mae_mean` | `6.280891089108911` |
| `mae_median` | `4.640000000000001` |
| `mae_p90` | `12.437999999999999` |
| `no_trade_rate` | `0.8935862538278326` |
| `hold_distribution` | `{'p50': 5.0, 'p90': 5.0}` |
| `loss_trade_mfe` | `3.5184126984126984` |
| `realized_over_mfe` | `-4.256147422568394` |
| `rule_pass_rates` | `{'long_signal_rate': 0.04559373936713168, 'short_signal_rate': 0.06082000680503573}` |
| `win_trade_mae` | `3.2842790697674418` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0001 | completed | 2026-03-30 14:37:00 UTC | 95.75   | 404    | 11756 | 11756         | 0       
```

### 50. `05_optimization` / `05EG_05ca_plus_session_margin0675_hold5_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05EG_05ca_plus_session_margin0675_hold5_0001\experiment_bundle.json`
- experiment_id: `exp_05eg_05ca_plus_session_margin0675_hold5_v1`
- bundle_status: `completed`
- latest_attempt: `att_0001`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-30T14:43:58.884230+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: max_probability_margin(min_margin=0.0675) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=5)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `94.992` |
| `profit_factor` | `1.4078030016828658` |
| `trade_count` | `404` |
| `win_rate` | `0.5247524752475248` |
| `expectancy_per_trade` | `1.1756435643564356` |
| `max_dd_pct` | `15.413001341881625` |
| `recovery_factor` | `3.2605203542253047` |
| `net_profit` | `474.96` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `15.413001341881625` |
| `equity_dd_amount` | `145.66999999999996` |
| `max_dd_pct` | `12.894975365921507` |
| `max_dd_amount` | `143.68999999999994` |
| `ulcer_index` | `8.01470197055628` |
| `worst_day` | `-36.03` |
| `worst_week` | `-52.949999999999996` |
| `min_free_margin` | `434.37` |
| `consecutive_losses` | `11` |
| `time_under_water` | `22210800.0` |
| `longest_recovery_duration` | `13237500.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `5.0` |
| `payoff_ratio` | `1.2749913977505198` |
| `avg_win` | `7.7341509433962266` |
| `avg_loss` | `-6.066041666666667` |
| `long_count` | `172` |
| `short_count` | `232` |
| `long_expectancy` | `2.3740697674418603` |
| `short_expectancy` | `0.28715517241379307` |
| `mfe_mean` | `7.388044554455446` |
| `mfe_median` | `5.495` |
| `mfe_p90` | `15.766999999999998` |
| `mae_mean` | `6.2690594059405935` |
| `mae_median` | `4.640000000000001` |
| `mae_p90` | `12.437999999999999` |
| `no_trade_rate` | `0.8932460020415107` |
| `hold_distribution` | `{'p50': 5.0, 'p90': 5.0}` |
| `loss_trade_mfe` | `3.49609375` |
| `realized_over_mfe` | `-4.278757393039799` |
| `rule_pass_rates` | `{'long_signal_rate': 0.0452534875808098, 'short_signal_rate': 0.061500510377679486}` |
| `win_trade_mae` | `3.2175471698113207` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0001 | completed | 2026-03-30 14:43:58 UTC | 94.99   | 404    | 11756 | 11756         | 0       
```

### 51. `05_optimization` / `05FA_05ca_temp115_margin0675_hold5_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05FA_05ca_temp115_margin0675_hold5_0001\experiment_bundle.json`
- experiment_id: `exp_05fa_05ca_temp115_margin0675_hold5_v1`
- bundle_status: `completed`
- latest_attempt: `att_0003`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-30T16:27:27.205551+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: max_probability_margin(min_margin=0.0675) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=5)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `92.762` |
| `profit_factor` | `1.4721529424938666` |
| `trade_count` | `338` |
| `win_rate` | `0.5266272189349113` |
| `expectancy_per_trade` | `1.3722189349112426` |
| `max_dd_pct` | `12.466013767265919` |
| `recovery_factor` | `3.383251878328105` |
| `net_profit` | `463.81` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `12.466013767265919` |
| `equity_dd_amount` | `137.09000000000003` |
| `max_dd_pct` | `12.246087170288899` |
| `max_dd_amount` | `134.5` |
| `ulcer_index` | `5.761932448101724` |
| `worst_day` | `-31.310000000000002` |
| `worst_week` | `-51.34` |
| `min_free_margin` | `446.92` |
| `consecutive_losses` | `10` |
| `time_under_water` | `22968000.0` |
| `longest_recovery_duration` | `13158000.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `5.0` |
| `payoff_ratio` | `1.3232835438147117` |
| `avg_win` | `8.124382022471911` |
| `avg_loss` | `-6.1395625` |
| `long_count` | `146` |
| `short_count` | `192` |
| `long_expectancy` | `2.517397260273973` |
| `short_expectancy` | `0.5014062499999999` |
| `mfe_mean` | `7.551479289940828` |
| `mfe_median` | `5.53` |
| `mfe_p90` | `15.564` |
| `mae_mean` | `6.531597633136094` |
| `mae_median` | `4.775` |
| `mae_p90` | `12.913000000000002` |
| `no_trade_rate` | `0.9164681864579789` |
| `hold_distribution` | `{'p50': 5.0, 'p90': 5.0}` |
| `loss_trade_mfe` | `3.4136249999999997` |
| `realized_over_mfe` | `-4.040399682728682` |
| `rule_pass_rates` | `{'long_signal_rate': 0.0363218781898605, 'short_signal_rate': 0.0472099353521606}` |
| `win_trade_mae` | `3.4680337078651684` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0003 | completed | 2026-03-30 16:27:27 UTC | 45.62   | 209    | 6755  | 6720          | 35      
att_0002 | completed | 2026-03-30 16:16:46 UTC | 92.76   | 338    | 11756 | 11756         | 0       
att_0001 | completed | 2026-03-30 16:06:18 UTC | 92.76   | 338    | 11756 | 11756         | 0       
```

### 52. `05_optimization` / `05EK_05dp_diff_only_hold5_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05EK_05dp_diff_only_hold5_0001\experiment_bundle.json`
- experiment_id: `exp_05ek_05dp_diff_only_hold5_v1`
- bundle_status: `completed`
- latest_attempt: `att_0001`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-30T14:59:14.307967+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: probability_difference(min_probability_diff=0.0775) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=5)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `92.64` |
| `profit_factor` | `1.4372368743982327` |
| `trade_count` | `371` |
| `win_rate` | `0.522911051212938` |
| `expectancy_per_trade` | `1.2485175202156333` |
| `max_dd_pct` | `12.684250653499854` |
| `recovery_factor` | `3.314490161001789` |
| `net_profit` | `463.2` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `12.684250653499854` |
| `equity_dd_amount` | `139.75` |
| `max_dd_pct` | `12.571480439321048` |
| `max_dd_amount` | `138.5` |
| `ulcer_index` | `5.908358128428507` |
| `worst_day` | `-31.310000000000002` |
| `worst_week` | `-51.230000000000004` |
| `min_free_margin` | `446.92` |
| `consecutive_losses` | `12` |
| `time_under_water` | `22748100.0` |
| `longest_recovery_duration` | `13237500.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `5.0` |
| `payoff_ratio` | `1.3112934369509648` |
| `avg_win` | `7.848350515463917` |
| `avg_loss` | `-5.985197740112995` |
| `long_count` | `162` |
| `short_count` | `209` |
| `long_expectancy` | `2.218641975308642` |
| `short_expectancy` | `0.4965550239234449` |
| `mfe_mean` | `7.296630727762803` |
| `mfe_median` | `5.33` |
| `mfe_p90` | `14.73` |
| `mae_mean` | `6.338652291105121` |
| `mae_median` | `4.7` |
| `mae_p90` | `12.41` |
| `no_trade_rate` | `0.9083021435862538` |
| `hold_distribution` | `{'p50': 5.0, 'p90': 5.0}` |
| `loss_trade_mfe` | `3.3361016949152544` |
| `realized_over_mfe` | `-4.268615904305608` |
| `rule_pass_rates` | `{'long_signal_rate': 0.039979584892820684, 'short_signal_rate': 0.051718271520925486}` |
| `win_trade_mae` | `3.3878865979381443` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0001 | completed | 2026-03-30 14:59:14 UTC | 92.64   | 371    | 11756 | 11756         | 0       
```

### 53. `05_optimization` / `05DT_05ca_margin0700_hold6_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05DT_05ca_margin0700_hold6_0001\experiment_bundle.json`
- experiment_id: `exp_05dt_05ca_margin0700_hold6_v1`
- bundle_status: `completed`
- latest_attempt: `att_0001`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-30T14:01:34.705526+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: max_probability_margin(min_margin=0.07) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=6)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `92.632` |
| `profit_factor` | `1.4003630548472146` |
| `trade_count` | `358` |
| `win_rate` | `0.5418994413407822` |
| `expectancy_per_trade` | `1.2937430167597765` |
| `max_dd_pct` | `14.884366245725039` |
| `recovery_factor` | `2.749866413346792` |
| `net_profit` | `463.16` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `14.884366245725039` |
| `equity_dd_amount` | `168.42999999999995` |
| `max_dd_pct` | `14.835446619626158` |
| `max_dd_amount` | `167.7800000000001` |
| `ulcer_index` | `9.374105346913131` |
| `worst_day` | `-58.36` |
| `worst_week` | `-53.64` |
| `min_free_margin` | `436.32` |
| `consecutive_losses` | `13` |
| `time_under_water` | `23135400.0` |
| `longest_recovery_duration` | `13237500.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `6.0` |
| `payoff_ratio` | `1.1838120669842431` |
| `avg_win` | `8.350567010309279` |
| `avg_loss` | `-7.053963414634146` |
| `long_count` | `155` |
| `short_count` | `203` |
| `long_expectancy` | `2.271677419354839` |
| `short_expectancy` | `0.5470443349753694` |
| `mfe_mean` | `8.432597765363129` |
| `mfe_median` | `6.605` |
| `mfe_p90` | `18.100000000000012` |
| `mae_mean` | `6.842988826815643` |
| `mae_median` | `5.055` |
| `mae_p90` | `15.231000000000005` |
| `no_trade_rate` | `0.8985199047294998` |
| `hold_distribution` | `{'p50': 6.0, 'p90': 6.0}` |
| `loss_trade_mfe` | `3.9683536585365857` |
| `realized_over_mfe` | `-5.881257122347694` |
| `rule_pass_rates` | `{'long_signal_rate': 0.044062606328683224, 'short_signal_rate': 0.057417488941816947}` |
| `win_trade_mae` | `3.701701030927835` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0001 | completed | 2026-03-30 14:01:34 UTC | 92.63   | 358    | 11756 | 11756         | 0       
```

### 54. `05_optimization` / `05DM_05cc_margin_hold4_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05DM_05cc_margin_hold4_0001\experiment_bundle.json`
- experiment_id: `exp_05dm_05cc_margin_hold4_v1`
- bundle_status: `completed`
- latest_attempt: `att_0001`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-30T13:40:11.121803+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: max_probability_margin(min_margin=0.07) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=4)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `92.44600000000001` |
| `profit_factor` | `1.4194122077144335` |
| `trade_count` | `435` |
| `win_rate` | `0.5448275862068965` |
| `expectancy_per_trade` | `1.0625977011494254` |
| `max_dd_pct` | `14.502909925783541` |
| `recovery_factor` | `3.476720571643474` |
| `net_profit` | `462.23` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `14.502909925783541` |
| `equity_dd_amount` | `132.95000000000005` |
| `max_dd_pct` | `12.100288693157799` |
| `max_dd_amount` | `131.61000000000013` |
| `ulcer_index` | `6.871090236363514` |
| `worst_day` | `-30.09` |
| `worst_week` | `-39.69` |
| `min_free_margin` | `452.33` |
| `consecutive_losses` | `8` |
| `time_under_water` | `22152300.0` |
| `longest_recovery_duration` | `13236300.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `4.0` |
| `payoff_ratio` | `1.1858380469512988` |
| `avg_win` | `6.600506329113924` |
| `avg_loss` | `-5.566111111111111` |
| `long_count` | `184` |
| `short_count` | `251` |
| `long_expectancy` | `1.565` |
| `short_expectancy` | `0.6943027888446215` |
| `mfe_mean` | `6.680689655172413` |
| `mfe_median` | `5.12` |
| `mfe_p90` | `14.220000000000002` |
| `mae_mean` | `5.908459770114942` |
| `mae_median` | `4.27` |
| `mae_p90` | `12.484000000000002` |
| `no_trade_rate` | `0.8973290234773733` |
| `hold_distribution` | `{'p50': 4.0, 'p90': 4.0}` |
| `loss_trade_mfe` | `3.1826262626262625` |
| `realized_over_mfe` | `-4.505805758311793` |
| `rule_pass_rates` | `{'long_signal_rate': 0.044147669275263694, 'short_signal_rate': 0.05852330724736305}` |
| `win_trade_mae` | `3.2553164556962026` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0001 | completed | 2026-03-30 13:40:11 UTC | 92.45   | 435    | 11756 | 11756         | 0       
```

### 55. `05_optimization` / `05BQ_frontier_vote_w_bf_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05BQ_frontier_vote_w_bf_0001\experiment_bundle.json`
- experiment_id: `exp_05bq_frontier_vote_w_bf_v1`
- bundle_status: `completed`
- latest_attempt: `att_0002`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-30T11:55:08.124309+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: max_probability_margin(min_margin=0.07) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=3)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `92.292` |
| `profit_factor` | `1.4156585809636189` |
| `trade_count` | `491` |
| `win_rate` | `0.5498981670061099` |
| `expectancy_per_trade` | `0.9398370672097759` |
| `max_dd_pct` | `10.966047750280698` |
| `recovery_factor` | `3.904721611101707` |
| `net_profit` | `461.46` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `10.966047750280698` |
| `equity_dd_amount` | `118.18000000000006` |
| `max_dd_pct` | `10.537726456439412` |
| `max_dd_amount` | `113.25` |
| `ulcer_index` | `6.491926923352973` |
| `worst_day` | `-30.5` |
| `worst_week` | `-37.67999999999999` |
| `min_free_margin` | `472.48` |
| `consecutive_losses` | `7` |
| `time_under_water` | `22608600.0` |
| `longest_recovery_duration` | `13839900.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `3.0` |
| `payoff_ratio` | `1.1587427644183694` |
| `avg_win` | `5.820925925925926` |
| `avg_loss` | `-5.023484162895928` |
| `long_count` | `206` |
| `short_count` | `285` |
| `long_expectancy` | `2.204271844660194` |
| `short_expectancy` | `0.025894736842105266` |
| `mfe_mean` | `5.937780040733197` |
| `mfe_median` | `4.29` |
| `mfe_p90` | `13.16` |
| `mae_mean` | `5.01183299389002` |
| `mae_median` | `3.4` |
| `mae_p90` | `10.01` |
| `no_trade_rate` | `0.8986049676760803` |
| `hold_distribution` | `{'p50': 3.0, 'p90': 3.0}` |
| `loss_trade_mfe` | `2.8768778280542984` |
| `realized_over_mfe` | `-2.8985339955042395` |
| `rule_pass_rates` | `{'long_signal_rate': 0.04389248043552229, 'short_signal_rate': 0.05750255188839742}` |
| `win_trade_mae` | `2.7367037037037036` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0002 | completed | 2026-03-30 11:55:08 UTC | 34.76   | 335    | 6755  | 6720          | 35      
att_0001 | completed | 2026-03-30 11:54:02 UTC | 92.29   | 491    | 11756 | 11756         | 0       
```

### 56. `05_optimization` / `05EO_05dp_short_bias_combo_hold5_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05EO_05dp_short_bias_combo_hold5_0001\experiment_bundle.json`
- experiment_id: `exp_05eo_05dp_short_bias_combo_hold5_v1`
- bundle_status: `completed`
- latest_attempt: `att_0001`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-30T15:05:49.057451+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3, long_threshold=0.45) | filters: combo_probability_gate(min_margin=0.05, min_probability_diff=0.07) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=5)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `91.69` |
| `profit_factor` | `1.43451681389089` |
| `trade_count` | `350` |
| `win_rate` | `0.5142857142857142` |
| `expectancy_per_trade` | `1.3098571428571428` |
| `max_dd_pct` | `15.513269728074278` |
| `recovery_factor` | `2.6082380383455654` |
| `net_profit` | `458.45` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `15.513269728074278` |
| `equity_dd_amount` | `175.76999999999998` |
| `max_dd_pct` | `14.977512441341617` |
| `max_dd_amount` | `168.83999999999992` |
| `ulcer_index` | `8.705438560617587` |
| `worst_day` | `-40.88` |
| `worst_week` | `-51.34` |
| `min_free_margin` | `446.92` |
| `consecutive_losses` | `10` |
| `time_under_water` | `22490700.0` |
| `longest_recovery_duration` | `13839900.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `5.0` |
| `payoff_ratio` | `1.354821435341396` |
| `avg_win` | `8.4085` |
| `avg_loss` | `-6.20635294117647` |
| `long_count` | `126` |
| `short_count` | `224` |
| `long_expectancy` | `3.0700793650793647` |
| `short_expectancy` | `0.3197321428571428` |
| `mfe_mean` | `7.720085714285715` |
| `mfe_median` | `5.68` |
| `mfe_p90` | `15.990000000000002` |
| `mae_mean` | `6.692428571428571` |
| `mae_median` | `5.245` |
| `mae_p90` | `12.85` |
| `no_trade_rate` | `0.9078768288533515` |
| `hold_distribution` | `{'p50': 5.0, 'p90': 5.0}` |
| `loss_trade_mfe` | `3.475941176470588` |
| `realized_over_mfe` | `-5.855385931791437` |
| `rule_pass_rates` | `{'long_signal_rate': 0.033684926845865944, 'short_signal_rate': 0.05843824430078258}` |
| `win_trade_mae` | `3.6185555555555555` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0001 | completed | 2026-03-30 15:05:49 UTC | 91.69   | 350    | 11756 | 11756         | 0       
```

### 57. `05_optimization` / `05DU_05cc_margin0700_hold6_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05DU_05cc_margin0700_hold6_0001\experiment_bundle.json`
- experiment_id: `exp_05du_05cc_margin0700_hold6_v1`
- bundle_status: `completed`
- latest_attempt: `att_0001`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-30T14:03:18.697255+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: max_probability_margin(min_margin=0.07) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=6)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `91.58800000000001` |
| `profit_factor` | `1.400885916380699` |
| `trade_count` | `360` |
| `win_rate` | `0.55` |
| `expectancy_per_trade` | `1.2720555555555555` |
| `max_dd_pct` | `15.415376676986584` |
| `recovery_factor` | `2.7816315373868674` |
| `net_profit` | `457.94` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `15.415376676986584` |
| `equity_dd_amount` | `164.63` |
| `max_dd_pct` | `14.569565954107242` |
| `max_dd_amount` | `163.3699999999999` |
| `ulcer_index` | `9.217075349898428` |
| `worst_day` | `-58.36` |
| `worst_week` | `-53.64` |
| `min_free_margin` | `436.32` |
| `consecutive_losses` | `13` |
| `time_under_water` | `22952100.0` |
| `longest_recovery_duration` | `13237500.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `6.0` |
| `payoff_ratio` | `1.1461793861296627` |
| `avg_win` | `8.082121212121212` |
| `avg_loss` | `-7.051358024691358` |
| `long_count` | `151` |
| `short_count` | `209` |
| `long_expectancy` | `2.2317218543046358` |
| `short_expectancy` | `0.5787081339712918` |
| `mfe_mean` | `8.32925` |
| `mfe_median` | `6.705` |
| `mfe_p90` | `17.608000000000004` |
| `mae_mean` | `6.919333333333333` |
| `mae_median` | `5.035` |
| `mae_p90` | `14.991000000000003` |
| `no_trade_rate` | `0.8973290234773733` |
| `hold_distribution` | `{'p50': 6.0, 'p90': 6.0}` |
| `loss_trade_mfe` | `3.9655555555555555` |
| `realized_over_mfe` | `-5.181003700788929` |
| `rule_pass_rates` | `{'long_signal_rate': 0.044147669275263694, 'short_signal_rate': 0.05852330724736305}` |
| `win_trade_mae` | `4.113383838383839` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0001 | completed | 2026-03-30 14:03:18 UTC | 91.59   | 360    | 11756 | 11756         | 0       
```

### 58. `05_optimization` / `05ET_05dp_stronger_long_suppression_hold4_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05ET_05dp_stronger_long_suppression_hold4_0001\experiment_bundle.json`
- experiment_id: `exp_05et_05dp_stronger_long_suppression_hold4_v1`
- bundle_status: `completed`
- latest_attempt: `att_0001`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-30T15:47:45.788536+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3, long_threshold=0.5) | filters: max_probability_margin(min_margin=0.0675) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=4)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `91.33` |
| `profit_factor` | `1.5092220884071548` |
| `trade_count` | `346` |
| `win_rate` | `0.5260115606936416` |
| `expectancy_per_trade` | `1.3197976878612716` |
| `max_dd_pct` | `13.174687827574155` |
| `recovery_factor` | `3.1871161362367397` |
| `net_profit` | `456.65` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `13.174687827574155` |
| `equity_dd_amount` | `143.27999999999997` |
| `max_dd_pct` | `12.703456685203317` |
| `max_dd_amount` | `137.51999999999998` |
| `ulcer_index` | `8.04394687012415` |
| `worst_day` | `-22.8` |
| `worst_week` | `-40.41` |
| `min_free_margin` | `466.75` |
| `consecutive_losses` | `8` |
| `time_under_water` | `22068000.0` |
| `longest_recovery_duration` | `13839900.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `4.0` |
| `payoff_ratio` | `1.3599583653778757` |
| `avg_win` | `7.4363186813186815` |
| `avg_loss` | `-5.468048780487805` |
| `long_count` | `87` |
| `short_count` | `259` |
| `long_expectancy` | `2.493793103448276` |
| `short_expectancy` | `0.9254440154440154` |
| `mfe_mean` | `7.248468208092485` |
| `mfe_median` | `5.5649999999999995` |
| `mfe_p90` | `15.74` |
| `mae_mean` | `6.358497109826589` |
| `mae_median` | `4.87` |
| `mae_p90` | `12.995000000000001` |
| `no_trade_rate` | `0.9174889418169445` |
| `hold_distribution` | `{'p50': 4.0, 'p90': 4.0}` |
| `loss_trade_mfe` | `3.238719512195122` |
| `realized_over_mfe` | `-5.156062066724605` |
| `rule_pass_rates` | `{'long_signal_rate': 0.021776114324600204, 'short_signal_rate': 0.06073494385845526}` |
| `win_trade_mae` | `3.716703296703297` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0001 | completed | 2026-03-30 15:47:45 UTC | 91.33   | 346    | 11756 | 11756         | 0       
```

### 59. `05_optimization` / `05W_no_trend_strength_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05W_no_trend_strength_0001\experiment_bundle.json`
- experiment_id: `exp_05w_trend_strength_sector_ablation_v1`
- bundle_status: `completed`
- latest_attempt: `att_0002`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-29T16:59:09.985673+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: max_probability_margin(min_margin=0.07) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=3)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `91.16799999999999` |
| `profit_factor` | `1.4091663899036866` |
| `trade_count` | `493` |
| `win_rate` | `0.5476673427991886` |
| `expectancy_per_trade` | `0.9246247464503042` |
| `max_dd_pct` | `11.147223438038381` |
| `recovery_factor` | `3.808187134502926` |
| `net_profit` | `455.84` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `11.147223438038381` |
| `equity_dd_amount` | `119.69999999999993` |
| `max_dd_pct` | `10.738399185678391` |
| `max_dd_amount` | `114.9899999999999` |
| `ulcer_index` | `6.520512249938508` |
| `worst_day` | `-30.5` |
| `worst_week` | `-37.67999999999999` |
| `min_free_margin` | `472.48` |
| `consecutive_losses` | `7` |
| `time_under_water` | `22608900.0` |
| `longest_recovery_duration` | `13839900.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `3.0` |
| `payoff_ratio` | `1.1638670553648969` |
| `avg_win` | `5.814481481481482` |
| `avg_loss` | `-4.995829596412555` |
| `long_count` | `207` |
| `short_count` | `286` |
| `long_expectancy` | `2.186280193236715` |
| `short_expectancy` | `0.011468531468531473` |
| `mfe_mean` | `5.922150101419878` |
| `mfe_median` | `4.29` |
| `mfe_p90` | `13.144000000000002` |
| `mae_mean` | `5.015882352941176` |
| `mae_median` | `3.41` |
| `mae_p90` | `9.994` |
| `no_trade_rate` | `0.8983497788363389` |
| `hold_distribution` | `{'p50': 3.0, 'p90': 3.0}` |
| `loss_trade_mfe` | `2.889461883408072` |
| `realized_over_mfe` | `-2.8885527293560167` |
| `rule_pass_rates` | `{'long_signal_rate': 0.044232732221844165, 'short_signal_rate': 0.057417488941816947}` |
| `win_trade_mae` | `2.7514814814814814` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0002 | completed | 2026-03-29 16:59:09 UTC | 33.54   | 336    | 6755  | 6720          | 35      
att_0001 | completed | 2026-03-29 16:58:17 UTC | 91.17   | 493    | 11756 | 11756         | 0       
```

### 60. `05_optimization` / `05EW_05dp_balanced_tight_combo_hold5_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05EW_05dp_balanced_tight_combo_hold5_0001\experiment_bundle.json`
- experiment_id: `exp_05ew_05dp_balanced_tight_combo_hold5_v1`
- bundle_status: `completed`
- latest_attempt: `att_0001`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-30T15:52:41.360776+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.45, long_threshold=0.45) | filters: combo_probability_gate(min_margin=0.05, min_probability_diff=0.07) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=5)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `90.542` |
| `profit_factor` | `1.4985079228744782` |
| `trade_count` | `282` |
| `win_rate` | `0.5602836879432624` |
| `expectancy_per_trade` | `1.6053546099290779` |
| `max_dd_pct` | `10.656913771275836` |
| `recovery_factor` | `3.983720520943334` |
| `net_profit` | `452.71` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `10.656913771275836` |
| `equity_dd_amount` | `113.63999999999987` |
| `max_dd_pct` | `10.173390784548502` |
| `max_dd_amount` | `107.89999999999986` |
| `ulcer_index` | `6.2199207963611505` |
| `worst_day` | `-40.88` |
| `worst_week` | `-46.2` |
| `min_free_margin` | `446.92` |
| `consecutive_losses` | `6` |
| `time_under_water` | `22071600.0` |
| `longest_recovery_duration` | `13839900.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `5.0` |
| `payoff_ratio` | `1.1760441926356666` |
| `avg_win` | `8.612911392405064` |
| `avg_loss` | `-7.323629032258064` |
| `long_count` | `126` |
| `short_count` | `156` |
| `long_expectancy` | `3.0700793650793647` |
| `short_expectancy` | `0.42230769230769216` |
| `mfe_mean` | `8.485425531914894` |
| `mfe_median` | `6.585` |
| `mfe_p90` | `18.045` |
| `mae_mean` | `7.208156028368794` |
| `mae_median` | `5.41` |
| `mae_p90` | `14.182000000000002` |
| `no_trade_rate` | `0.9282068730860837` |
| `hold_distribution` | `{'p50': 5.0, 'p90': 5.0}` |
| `loss_trade_mfe` | `3.797661290322581` |
| `realized_over_mfe` | `-5.475391959861719` |
| `rule_pass_rates` | `{'long_signal_rate': 0.033684926845865944, 'short_signal_rate': 0.03810820006805036}` |
| `win_trade_mae` | `3.717658227848101` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0001 | completed | 2026-03-30 15:52:41 UTC | 90.54   | 282    | 11756 | 11756         | 0       
```

### 61. `05_optimization` / `05EV_05dp_short_bias_combo_hold4_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05EV_05dp_short_bias_combo_hold4_0001\experiment_bundle.json`
- experiment_id: `exp_05ev_05dp_short_bias_combo_hold4_v1`
- bundle_status: `completed`
- latest_attempt: `att_0001`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-30T15:51:03.485791+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3, long_threshold=0.45) | filters: combo_probability_gate(min_margin=0.05, min_probability_diff=0.07) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=4)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `90.092` |
| `profit_factor` | `1.4420434919139582` |
| `trade_count` | `384` |
| `win_rate` | `0.5286458333333334` |
| `expectancy_per_trade` | `1.1730729166666667` |
| `max_dd_pct` | `13.90621580214488` |
| `recovery_factor` | `2.9540297724440965` |
| `net_profit` | `450.46` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `13.90621580214488` |
| `equity_dd_amount` | `152.4899999999999` |
| `max_dd_pct` | `13.113070900790227` |
| `max_dd_amount` | `143.03999999999996` |
| `ulcer_index` | `8.382009985763618` |
| `worst_day` | `-31.25` |
| `worst_week` | `-40.41` |
| `min_free_margin` | `455.02` |
| `consecutive_losses` | `8` |
| `time_under_water` | `21979200.0` |
| `longest_recovery_duration` | `13839900.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `4.0` |
| `payoff_ratio` | `1.2857629164355981` |
| `avg_win` | `7.238916256157635` |
| `avg_loss` | `-5.630055248618785` |
| `long_count` | `137` |
| `short_count` | `247` |
| `long_expectancy` | `1.9975182481751828` |
| `short_expectancy` | `0.7157894736842104` |
| `mfe_mean` | `6.984322916666667` |
| `mfe_median` | `5.35` |
| `mfe_p90` | `15.099999999999996` |
| `mae_mean` | `6.269479166666667` |
| `mae_median` | `4.84` |
| `mae_p90` | `12.905999999999999` |
| `no_trade_rate` | `0.9078768288533515` |
| `hold_distribution` | `{'p50': 4.0, 'p90': 4.0}` |
| `loss_trade_mfe` | `3.0784530386740334` |
| `realized_over_mfe` | `-5.229726611616369` |
| `rule_pass_rates` | `{'long_signal_rate': 0.033684926845865944, 'short_signal_rate': 0.05843824430078258}` |
| `win_trade_mae` | `3.574679802955665` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0001 | completed | 2026-03-30 15:51:03 UTC | 90.09   | 384    | 11756 | 11756         | 0       
```

### 62. `05_optimization` / `05BF_trend_proxy_persistence_volatility_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05BF_trend_proxy_persistence_volatility_0001\experiment_bundle.json`
- experiment_id: `exp_05bf_trend_proxy_persistence_volatility_v1`
- bundle_status: `completed`
- latest_attempt: `att_0002`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-30T11:25:00.669343+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: max_probability_margin(min_margin=0.07) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=3)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `89.422` |
| `profit_factor` | `1.4011646164751062` |
| `trade_count` | `487` |
| `win_rate` | `0.5420944558521561` |
| `expectancy_per_trade` | `0.9180903490759754` |
| `max_dd_pct` | `11.94626370657451` |
| `recovery_factor` | `3.4867815643765074` |
| `net_profit` | `447.11` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `11.94626370657451` |
| `equity_dd_amount` | `128.23000000000013` |
| `max_dd_pct` | `11.518950682448786` |
| `max_dd_amount` | `123.30000000000007` |
| `ulcer_index` | `7.150574039547822` |
| `worst_day` | `-30.5` |
| `worst_week` | `-37.67999999999999` |
| `min_free_margin` | `472.48` |
| `consecutive_losses` | `10` |
| `time_under_water` | `22616100.0` |
| `longest_recovery_duration` | `13839900.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `3.0` |
| `payoff_ratio` | `1.183559505583139` |
| `avg_win` | `5.915303030303031` |
| `avg_loss` | `-4.997892376681614` |
| `long_count` | `204` |
| `short_count` | `283` |
| `long_expectancy` | `2.1679411764705883` |
| `short_expectancy` | `0.017137809187279147` |
| `mfe_mean` | `5.966324435318275` |
| `mfe_median` | `4.31` |
| `mfe_p90` | `13.338000000000013` |
| `mae_mean` | `5.051088295687885` |
| `mae_median` | `3.41` |
| `mae_p90` | `10.058000000000003` |
| `no_trade_rate` | `0.8989452194624021` |
| `hold_distribution` | `{'p50': 3.0, 'p90': 3.0}` |
| `loss_trade_mfe` | `2.861928251121076` |
| `realized_over_mfe` | `-2.942517359515616` |
| `rule_pass_rates` | `{'long_signal_rate': 0.04363729159578088, 'short_signal_rate': 0.057417488941816947}` |
| `win_trade_mae` | `2.743333333333333` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0002 | completed | 2026-03-30 11:25:00 UTC | 40.46   | 331    | 6755  | 6720          | 35      
att_0001 | completed | 2026-03-30 11:23:57 UTC | 89.42   | 487    | 11756 | 11756         | 0       
```

### 63. `05_optimization` / `05S_no_price_return_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05S_no_price_return_0001\experiment_bundle.json`
- experiment_id: `exp_05s_price_return_sector_ablation_v1`
- bundle_status: `completed`
- latest_attempt: `att_0001`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-29T16:45:40.060133+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: max_probability_margin(min_margin=0.07) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=3)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `89.294` |
| `profit_factor` | `1.3757405911263718` |
| `trade_count` | `514` |
| `win_rate` | `0.5505836575875487` |
| `expectancy_per_trade` | `0.8686186770428015` |
| `max_dd_pct` | `9.71093254060415` |
| `recovery_factor` | `7.118463010204078` |
| `net_profit` | `446.46999999999997` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `9.71093254060415` |
| `equity_dd_amount` | `62.72000000000003` |
| `max_dd_pct` | `9.441373742392258` |
| `max_dd_amount` | `60.81000000000006` |
| `ulcer_index` | `2.3986372338498922` |
| `worst_day` | `-25.83` |
| `worst_week` | `-27.200000000000003` |
| `min_free_margin` | `469.42` |
| `consecutive_losses` | `5` |
| `time_under_water` | `22441500.0` |
| `longest_recovery_duration` | `11413500.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `3.0` |
| `payoff_ratio` | `1.122954334099618` |
| `avg_win` | `5.776360424028269` |
| `avg_loss` | `-5.143896103896104` |
| `long_count` | `253` |
| `short_count` | `261` |
| `long_expectancy` | `1.0382608695652173` |
| `short_expectancy` | `0.704176245210728` |
| `mfe_mean` | `5.731322957198444` |
| `mfe_median` | `3.935` |
| `mfe_p90` | `12.423999999999998` |
| `mae_mean` | `4.701750972762645` |
| `mae_median` | `3.245` |
| `mae_p90` | `10.535999999999996` |
| `no_trade_rate` | `0.8941816944538958` |
| `hold_distribution` | `{'p50': 3.0, 'p90': 3.0}` |
| `loss_trade_mfe` | `2.627316017316017` |
| `realized_over_mfe` | `-4.584370665175615` |
| `rule_pass_rates` | `{'long_signal_rate': 0.05180333446750596, 'short_signal_rate': 0.054014971078598165}` |
| `win_trade_mae` | `2.4231448763250882` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0001 | completed | 2026-03-29 16:45:40 UTC | 89.29   | 514    | 11756 | 11756         | 0       
```

### 64. `05_optimization` / `05BR_frontier_vote_w_bb_bf_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05BR_frontier_vote_w_bb_bf_0001\experiment_bundle.json`
- experiment_id: `exp_05br_frontier_vote_w_bb_bf_v1`
- bundle_status: `completed`
- latest_attempt: `att_0002`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-30T11:58:03.950021+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: max_probability_margin(min_margin=0.07) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=3)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `87.628` |
| `profit_factor` | `1.3943760857628917` |
| `trade_count` | `487` |
| `win_rate` | `0.5462012320328542` |
| `expectancy_per_trade` | `0.8996714579055441` |
| `max_dd_pct` | `12.169843175508376` |
| `recovery_factor` | `3.3768015414258157` |
| `net_profit` | `438.14` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `12.169843175508376` |
| `equity_dd_amount` | `129.7500000000001` |
| `max_dd_pct` | `11.760943584341323` |
| `max_dd_amount` | `125.04000000000008` |
| `ulcer_index` | `7.249302500971241` |
| `worst_day` | `-30.5` |
| `worst_week` | `-37.67999999999999` |
| `min_free_margin` | `472.48` |
| `consecutive_losses` | `10` |
| `time_under_water` | `22844400.0` |
| `longest_recovery_duration` | `13839900.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `3.0` |
| `payoff_ratio` | `1.1584853945624025` |
| `avg_win` | `5.823721804511278` |
| `avg_loss` | `-5.027013574660634` |
| `long_count` | `203` |
| `short_count` | `284` |
| `long_expectancy` | `2.158374384236453` |
| `short_expectancy` | `-3.5211267605638114e-05` |
| `mfe_mean` | `5.955790554414784` |
| `mfe_median` | `4.31` |
| `mfe_p90` | `13.338000000000013` |
| `mae_mean` | `5.047967145790555` |
| `mae_median` | `3.41` |
| `mae_p90` | `10.058000000000003` |
| `no_trade_rate` | `0.8989452194624021` |
| `hold_distribution` | `{'p50': 3.0, 'p90': 3.0}` |
| `loss_trade_mfe` | `2.874027149321267` |
| `realized_over_mfe` | `-2.941763014752389` |
| `rule_pass_rates` | `{'long_signal_rate': 0.04372235454236135, 'short_signal_rate': 0.057332425995236476}` |
| `win_trade_mae` | `2.7700375939849624` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0002 | completed | 2026-03-30 11:58:03 UTC | 38.27   | 332    | 6755  | 6720          | 35      
att_0001 | completed | 2026-03-30 11:56:57 UTC | 87.63   | 487    | 11756 | 11756         | 0       
```

### 65. `05_optimization` / `05AI_trend_proxy_light_pb_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05AI_trend_proxy_light_pb_0001\experiment_bundle.json`
- experiment_id: `exp_05ai_trend_proxy_light_pb_v1`
- bundle_status: `completed`
- latest_attempt: `att_0002`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-29T17:51:32.653195+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: max_probability_margin(min_margin=0.07) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=3)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `86.868` |
| `profit_factor` | `1.3884313041611889` |
| `trade_count` | `485` |
| `win_rate` | `0.5422680412371134` |
| `expectancy_per_trade` | `0.8955463917525772` |
| `max_dd_pct` | `11.717263510635284` |
| `recovery_factor` | `3.508967523024719` |
| `net_profit` | `434.34` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `11.717263510635284` |
| `equity_dd_amount` | `123.78000000000009` |
| `max_dd_pct` | `11.303291216145665` |
| `max_dd_amount` | `119.07000000000005` |
| `ulcer_index` | `6.844386501971849` |
| `worst_day` | `-23.57` |
| `worst_week` | `-37.67999999999999` |
| `min_free_margin` | `472.48` |
| `consecutive_losses` | `10` |
| `time_under_water` | `22611600.0` |
| `longest_recovery_duration` | `13839900.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `3.0` |
| `payoff_ratio` | `1.1719838384934749` |
| `avg_win` | `5.9031558935361215` |
| `avg_loss` | `-5.036891891891893` |
| `long_count` | `202` |
| `short_count` | `283` |
| `long_expectancy` | `2.2049009900990097` |
| `short_expectancy` | `-0.03904593639575972` |
| `mfe_mean` | `5.9787010309278354` |
| `mfe_median` | `4.38` |
| `mfe_p90` | `13.412000000000008` |
| `mae_mean` | `5.0631546391752575` |
| `mae_median` | `3.45` |
| `mae_p90` | `10.142` |
| `no_trade_rate` | `0.8997958489282069` |
| `hold_distribution` | `{'p50': 3.0, 'p90': 3.0}` |
| `loss_trade_mfe` | `2.8896396396396398` |
| `realized_over_mfe` | `-3.1966866705923516` |
| `rule_pass_rates` | `{'long_signal_rate': 0.04321197686287853, 'short_signal_rate': 0.056992174208914594}` |
| `win_trade_mae` | `2.76212927756654` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0002 | completed | 2026-03-29 17:51:32 UTC | 37.27   | 330    | 6755  | 6720          | 35      
att_0001 | completed | 2026-03-29 17:50:30 UTC | 86.87   | 485    | 11756 | 11756         | 0       
```

### 66. `05_optimization` / `05AW_05aj_thr_margin_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05AW_05aj_thr_margin_0001\experiment_bundle.json`
- experiment_id: `exp_05aw_05aj_thr_margin_v1`
- bundle_status: `completed`
- latest_attempt: `att_0002`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-30T10:48:24.432236+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.535, long_threshold=0.4) | filters: max_probability_margin(min_margin=0.07) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=3)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `86.626` |
| `profit_factor` | `1.7084232908079817` |
| `trade_count` | `245` |
| `win_rate` | `0.6163265306122448` |
| `expectancy_per_trade` | `1.7678775510204081` |
| `max_dd_pct` | `10.879626140046742` |
| `recovery_factor` | `6.001524179021748` |
| `net_profit` | `433.13` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `10.879626140046742` |
| `equity_dd_amount` | `72.17000000000007` |
| `max_dd_pct` | `6.803506745760936` |
| `max_dd_amount` | `56.629999999999995` |
| `ulcer_index` | `1.5008729974843673` |
| `worst_day` | `-26.080000000000005` |
| `worst_week` | `-22.940000000000005` |
| `min_free_margin` | `458.1` |
| `consecutive_losses` | `4` |
| `time_under_water` | `20259600.0` |
| `longest_recovery_duration` | `8626800.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `3.0` |
| `payoff_ratio` | `1.0635217836817898` |
| `avg_win` | `6.917417218543046` |
| `avg_loss` | `-6.504255319148936` |
| `long_count` | `195` |
| `short_count` | `50` |
| `long_expectancy` | `2.1416410256410257` |
| `short_expectancy` | `0.3102` |
| `mfe_mean` | `7.447469387755102` |
| `mfe_median` | `4.97` |
| `mfe_p90` | `16.573999999999995` |
| `mae_mean` | `6.01534693877551` |
| `mae_median` | `3.96` |
| `mae_p90` | `12.991999999999999` |
| `no_trade_rate` | `0.9487921061585574` |
| `hold_distribution` | `{'p50': 3.0, 'p90': 3.0}` |
| `loss_trade_mfe` | `3.2658510638297873` |
| `realized_over_mfe` | `-2.4054327478774735` |
| `rule_pass_rates` | `{'long_signal_rate': 0.04159578087784961, 'short_signal_rate': 0.009612112963593059}` |
| `win_trade_mae` | `3.2427814569536424` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0002 | completed | 2026-03-30 10:48:24 UTC | 2.38    | 161    | 6755  | 6720          | 35      
att_0001 | completed | 2026-03-30 10:42:33 UTC | 86.63   | 245    | 11756 | 11756         | 0       
```

### 67. `05_optimization` / `05AX_05aj_thr_combo_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05AX_05aj_thr_combo_0001\experiment_bundle.json`
- experiment_id: `exp_05ax_05aj_thr_combo_v1`
- bundle_status: `completed`
- latest_attempt: `att_0002`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-30T10:49:30.397548+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.535, long_threshold=0.4) | filters: combo_probability_gate(min_margin=0.05, min_probability_diff=0.07) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=3)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `86.626` |
| `profit_factor` | `1.7084232908079817` |
| `trade_count` | `245` |
| `win_rate` | `0.6163265306122448` |
| `expectancy_per_trade` | `1.7678775510204081` |
| `max_dd_pct` | `10.879626140046742` |
| `recovery_factor` | `6.001524179021748` |
| `net_profit` | `433.13` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `10.879626140046742` |
| `equity_dd_amount` | `72.17000000000007` |
| `max_dd_pct` | `6.803506745760936` |
| `max_dd_amount` | `56.629999999999995` |
| `ulcer_index` | `1.5008729974843673` |
| `worst_day` | `-26.080000000000005` |
| `worst_week` | `-22.940000000000005` |
| `min_free_margin` | `458.1` |
| `consecutive_losses` | `4` |
| `time_under_water` | `20259600.0` |
| `longest_recovery_duration` | `8626800.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `3.0` |
| `payoff_ratio` | `1.0635217836817898` |
| `avg_win` | `6.917417218543046` |
| `avg_loss` | `-6.504255319148936` |
| `long_count` | `195` |
| `short_count` | `50` |
| `long_expectancy` | `2.1416410256410257` |
| `short_expectancy` | `0.3102` |
| `mfe_mean` | `7.447469387755102` |
| `mfe_median` | `4.97` |
| `mfe_p90` | `16.573999999999995` |
| `mae_mean` | `6.01534693877551` |
| `mae_median` | `3.96` |
| `mae_p90` | `12.991999999999999` |
| `no_trade_rate` | `0.9487921061585574` |
| `hold_distribution` | `{'p50': 3.0, 'p90': 3.0}` |
| `loss_trade_mfe` | `3.2658510638297873` |
| `realized_over_mfe` | `-2.4054327478774735` |
| `rule_pass_rates` | `{'long_signal_rate': 0.04159578087784961, 'short_signal_rate': 0.009612112963593059}` |
| `win_trade_mae` | `3.2427814569536424` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0002 | completed | 2026-03-30 10:49:30 UTC | 2.38    | 161    | 6755  | 6720          | 35      
att_0001 | completed | 2026-03-30 10:44:09 UTC | 86.63   | 245    | 11756 | 11756         | 0       
```

### 68. `05_optimization` / `05DS_05cc_margin0725_hold5_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05DS_05cc_margin0725_hold5_0001\experiment_bundle.json`
- experiment_id: `exp_05ds_05cc_margin0725_hold5_v1`
- bundle_status: `completed`
- latest_attempt: `att_0001`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-30T13:59:50.269804+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: max_probability_margin(min_margin=0.0725) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=5)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `86.43399999999998` |
| `profit_factor` | `1.3771116928446772` |
| `trade_count` | `382` |
| `win_rate` | `0.5235602094240838` |
| `expectancy_per_trade` | `1.1313350785340313` |
| `max_dd_pct` | `16.0091370165318` |
| `recovery_factor` | `2.86451912242328` |
| `net_profit` | `432.16999999999996` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `16.0091370165318` |
| `equity_dd_amount` | `150.8699999999999` |
| `max_dd_pct` | `13.83078046570961` |
| `max_dd_amount` | `149.62` |
| `ulcer_index` | `7.727964873788136` |
| `worst_day` | `-32.99` |
| `worst_week` | `-52.25` |
| `min_free_margin` | `432.45` |
| `consecutive_losses` | `10` |
| `time_under_water` | `22523700.0` |
| `longest_recovery_duration` | `13237500.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `5.0` |
| `payoff_ratio` | `1.2531716404886564` |
| `avg_win` | `7.89085` |
| `avg_loss` | `-6.2967032967032965` |
| `long_count` | `161` |
| `short_count` | `221` |
| `long_expectancy` | `2.410186335403727` |
| `short_expectancy` | `0.199683257918552` |
| `mfe_mean` | `7.386465968586387` |
| `mfe_median` | `5.57` |
| `mfe_p90` | `15.171000000000017` |
| `mae_mean` | `6.4986910994764395` |
| `mae_median` | `4.95` |
| `mae_p90` | `12.745000000000001` |
| `no_trade_rate` | `0.9022626743790405` |
| `hold_distribution` | `{'p50': 5.0, 'p90': 5.0}` |
| `loss_trade_mfe` | `3.4491758241758244` |
| `realized_over_mfe` | `-5.378332562238386` |
| `rule_pass_rates` | `{'long_signal_rate': 0.0421912215039129, 'short_signal_rate': 0.055546104117046614}` |
| `win_trade_mae` | `3.39685` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0001 | completed | 2026-03-30 13:59:50 UTC | 86.43   | 382    | 11756 | 11756         | 0       
```

### 69. `05_optimization` / `05DF_05bb_margin_hold4_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05DF_05bb_margin_hold4_0001\experiment_bundle.json`
- experiment_id: `exp_05df_05bb_margin_hold4_v1`
- bundle_status: `completed`
- latest_attempt: `att_0001`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-30T13:13:18.078805+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: max_probability_margin(min_margin=0.07) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=4)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `86.25` |
| `profit_factor` | `1.4009949323538984` |
| `trade_count` | `428` |
| `win_rate` | `0.544392523364486` |
| `expectancy_per_trade` | `1.0075934579439252` |
| `max_dd_pct` | `14.65569569029473` |
| `recovery_factor` | `3.403709550118392` |
| `net_profit` | `431.25` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `14.65569569029473` |
| `equity_dd_amount` | `126.69999999999993` |
| `max_dd_pct` | `11.647224495233017` |
| `max_dd_amount` | `122.40999999999997` |
| `ulcer_index` | `6.632263256934764` |
| `worst_day` | `-38.519999999999996` |
| `worst_week` | `-39.69` |
| `min_free_margin` | `447.13` |
| `consecutive_losses` | `7` |
| `time_under_water` | `22068600.0` |
| `longest_recovery_duration` | `13236300.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `4.0` |
| `payoff_ratio` | `1.1725064884506873` |
| `avg_win` | `6.466523605150215` |
| `avg_loss` | `-5.515128205128206` |
| `long_count` | `180` |
| `short_count` | `248` |
| `long_expectancy` | `1.4348333333333332` |
| `short_expectancy` | `0.6975` |
| `mfe_mean` | `6.600630841121496` |
| `mfe_median` | `5.08` |
| `mfe_p90` | `14.190000000000001` |
| `mae_mean` | `5.991892523364487` |
| `mae_median` | `4.359999999999999` |
| `mae_p90` | `12.560000000000002` |
| `no_trade_rate` | `0.8987750935692412` |
| `hold_distribution` | `{'p50': 4.0, 'p90': 4.0}` |
| `loss_trade_mfe` | `3.193589743589744` |
| `realized_over_mfe` | `-4.0908343893135495` |
| `rule_pass_rates` | `{'long_signal_rate': 0.043382102756039466, 'short_signal_rate': 0.05784280367471929}` |
| `win_trade_mae` | `3.3705150214592274` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0001 | completed | 2026-03-30 13:13:18 UTC | 86.25   | 428    | 11756 | 11756         | 0       
```

### 70. `05_optimization` / `05AP_05w_thr_margin_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05AP_05w_thr_margin_0001\experiment_bundle.json`
- experiment_id: `exp_05ap_05w_thr_margin_v1`
- bundle_status: `completed`
- latest_attempt: `att_0002`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-29T18:00:40.570531+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.535, long_threshold=0.4) | filters: max_probability_margin(min_margin=0.07) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=3)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `86.15` |
| `profit_factor` | `1.7020846576369535` |
| `trade_count` | `250` |
| `win_rate` | `0.616` |
| `expectancy_per_trade` | `1.723` |
| `max_dd_pct` | `10.891447715919888` |
| `recovery_factor` | `5.968546487460167` |
| `net_profit` | `430.75` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `10.891447715919888` |
| `equity_dd_amount` | `72.16999999999996` |
| `max_dd_pct` | `6.809941674110666` |
| `max_dd_amount` | `56.629999999999995` |
| `ulcer_index` | `1.4256370535559624` |
| `worst_day` | `-26.080000000000005` |
| `worst_week` | `-22.940000000000005` |
| `min_free_margin` | `458.1` |
| `consecutive_losses` | `4` |
| `time_under_water` | `20259300.0` |
| `longest_recovery_duration` | `8626800.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `3.0` |
| `payoff_ratio` | `1.06103978657888` |
| `avg_win` | `6.781038961038961` |
| `avg_loss` | `-6.3909375` |
| `long_count` | `200` |
| `short_count` | `50` |
| `long_expectancy` | `2.1153999999999997` |
| `short_expectancy` | `0.15339999999999995` |
| `mfe_mean` | `7.31468` |
| `mfe_median` | `4.9` |
| `mfe_p90` | `16.253999999999998` |
| `mae_mean` | `5.94116` |
| `mae_median` | `3.8899999999999997` |
| `mae_p90` | `12.857` |
| `no_trade_rate` | `0.948196665532494` |
| `hold_distribution` | `{'p50': 3.0, 'p90': 3.0}` |
| `loss_trade_mfe` | `3.2451041666666662` |
| `realized_over_mfe` | `-2.35426435876459` |
| `rule_pass_rates` | `{'long_signal_rate': 0.04227628445049336, 'short_signal_rate': 0.00952705001701259}` |
| `win_trade_mae` | `3.2136363636363634` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0002 | completed | 2026-03-29 18:00:40 UTC | 5.75    | 163    | 6755  | 6720          | 35      
att_0001 | completed | 2026-03-29 17:58:28 UTC | 86.15   | 250    | 11756 | 11756         | 0       
```

### 71. `05_optimization` / `05AQ_05w_thr_combo_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05AQ_05w_thr_combo_0001\experiment_bundle.json`
- experiment_id: `exp_05aq_05w_thr_combo_v1`
- bundle_status: `completed`
- latest_attempt: `att_0001`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-29T17:59:47.773656+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.535, long_threshold=0.4) | filters: combo_probability_gate(min_margin=0.05, min_probability_diff=0.07) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=3)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `86.15` |
| `profit_factor` | `1.7020846576369535` |
| `trade_count` | `250` |
| `win_rate` | `0.616` |
| `expectancy_per_trade` | `1.723` |
| `max_dd_pct` | `10.891447715919888` |
| `recovery_factor` | `5.968546487460167` |
| `net_profit` | `430.75` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `10.891447715919888` |
| `equity_dd_amount` | `72.16999999999996` |
| `max_dd_pct` | `6.809941674110666` |
| `max_dd_amount` | `56.629999999999995` |
| `ulcer_index` | `1.4256370535559624` |
| `worst_day` | `-26.080000000000005` |
| `worst_week` | `-22.940000000000005` |
| `min_free_margin` | `458.1` |
| `consecutive_losses` | `4` |
| `time_under_water` | `20259300.0` |
| `longest_recovery_duration` | `8626800.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `3.0` |
| `payoff_ratio` | `1.06103978657888` |
| `avg_win` | `6.781038961038961` |
| `avg_loss` | `-6.3909375` |
| `long_count` | `200` |
| `short_count` | `50` |
| `long_expectancy` | `2.1153999999999997` |
| `short_expectancy` | `0.15339999999999995` |
| `mfe_mean` | `7.31468` |
| `mfe_median` | `4.9` |
| `mfe_p90` | `16.253999999999998` |
| `mae_mean` | `5.94116` |
| `mae_median` | `3.8899999999999997` |
| `mae_p90` | `12.857` |
| `no_trade_rate` | `0.948196665532494` |
| `hold_distribution` | `{'p50': 3.0, 'p90': 3.0}` |
| `loss_trade_mfe` | `3.2451041666666662` |
| `realized_over_mfe` | `-2.35426435876459` |
| `rule_pass_rates` | `{'long_signal_rate': 0.04227628445049336, 'short_signal_rate': 0.00952705001701259}` |
| `win_trade_mae` | `3.2136363636363634` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0001 | completed | 2026-03-29 17:59:47 UTC | 86.15   | 250    | 11756 | 11756         | 0       
```

### 72. `05_optimization` / `05AS_05ai_thr_margin_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05AS_05ai_thr_margin_0001\experiment_bundle.json`
- experiment_id: `exp_05as_05ai_thr_margin_v1`
- bundle_status: `completed`
- latest_attempt: `att_0001`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-30T10:36:04.294160+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.535, long_threshold=0.4) | filters: max_probability_margin(min_margin=0.07) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=3)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `85.75399999999999` |
| `profit_factor` | `1.70129211645404` |
| `trade_count` | `244` |
| `win_rate` | `0.6147540983606558` |
| `expectancy_per_trade` | `1.7572540983606557` |
| `max_dd_pct` | `10.951607763395494` |
| `recovery_factor` | `5.941111265068591` |
| `net_profit` | `428.77` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `10.951607763395494` |
| `equity_dd_amount` | `72.16999999999996` |
| `max_dd_pct` | `6.8426610348468895` |
| `max_dd_amount` | `56.629999999999995` |
| `ulcer_index` | `1.505226891760692` |
| `worst_day` | `-26.080000000000005` |
| `worst_week` | `-22.940000000000005` |
| `min_free_margin` | `458.1` |
| `consecutive_losses` | `4` |
| `time_under_water` | `20259000.0` |
| `longest_recovery_duration` | `8626800.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `3.0` |
| `payoff_ratio` | `1.0661430596445318` |
| `avg_win` | `6.934466666666667` |
| `avg_loss` | `-6.504255319148936` |
| `long_count` | `195` |
| `short_count` | `49` |
| `long_expectancy` | `2.1416410256410257` |
| `short_expectancy` | `0.22755102040816325` |
| `mfe_mean` | `7.455819672131148` |
| `mfe_median` | `4.965` |
| `mfe_p90` | `16.638000000000012` |
| `mae_mean` | `6.0231557377049185` |
| `mae_median` | `3.96` |
| `mae_p90` | `13.019000000000005` |
| `no_trade_rate` | `0.9492174208914597` |
| `hold_distribution` | `{'p50': 3.0, 'p90': 3.0}` |
| `loss_trade_mfe` | `3.2658510638297873` |
| `realized_over_mfe` | `-2.4187578421519595` |
| `rule_pass_rates` | `{'long_signal_rate': 0.0413405920381082, 'short_signal_rate': 0.009441987070432119}` |
| `win_trade_mae` | `3.237` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0001 | completed | 2026-03-30 10:36:04 UTC | 85.75   | 244    | 11756 | 11756         | 0       
```

### 73. `05_optimization` / `05AT_05ai_thr_combo_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05AT_05ai_thr_combo_0001\experiment_bundle.json`
- experiment_id: `exp_05at_05ai_thr_combo_v1`
- bundle_status: `completed`
- latest_attempt: `att_0001`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-30T10:37:44.681099+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.535, long_threshold=0.4) | filters: combo_probability_gate(min_margin=0.05, min_probability_diff=0.07) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=3)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `85.75399999999999` |
| `profit_factor` | `1.70129211645404` |
| `trade_count` | `244` |
| `win_rate` | `0.6147540983606558` |
| `expectancy_per_trade` | `1.7572540983606557` |
| `max_dd_pct` | `10.951607763395494` |
| `recovery_factor` | `5.941111265068591` |
| `net_profit` | `428.77` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `10.951607763395494` |
| `equity_dd_amount` | `72.16999999999996` |
| `max_dd_pct` | `6.8426610348468895` |
| `max_dd_amount` | `56.629999999999995` |
| `ulcer_index` | `1.505226891760692` |
| `worst_day` | `-26.080000000000005` |
| `worst_week` | `-22.940000000000005` |
| `min_free_margin` | `458.1` |
| `consecutive_losses` | `4` |
| `time_under_water` | `20259000.0` |
| `longest_recovery_duration` | `8626800.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `3.0` |
| `payoff_ratio` | `1.0661430596445318` |
| `avg_win` | `6.934466666666667` |
| `avg_loss` | `-6.504255319148936` |
| `long_count` | `195` |
| `short_count` | `49` |
| `long_expectancy` | `2.1416410256410257` |
| `short_expectancy` | `0.22755102040816325` |
| `mfe_mean` | `7.455819672131148` |
| `mfe_median` | `4.965` |
| `mfe_p90` | `16.638000000000012` |
| `mae_mean` | `6.0231557377049185` |
| `mae_median` | `3.96` |
| `mae_p90` | `13.019000000000005` |
| `no_trade_rate` | `0.9492174208914597` |
| `hold_distribution` | `{'p50': 3.0, 'p90': 3.0}` |
| `loss_trade_mfe` | `3.2658510638297873` |
| `realized_over_mfe` | `-2.4187578421519595` |
| `rule_pass_rates` | `{'long_signal_rate': 0.0413405920381082, 'short_signal_rate': 0.009441987070432119}` |
| `win_trade_mae` | `3.237` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0001 | completed | 2026-03-30 10:37:44 UTC | 85.75   | 244    | 11756 | 11756         | 0       
```

### 74. `05_optimization` / `05BK_05w_long_bias_margin_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05BK_05w_long_bias_margin_0001\experiment_bundle.json`
- experiment_id: `exp_05bk_05w_long_bias_margin_v1`
- bundle_status: `completed`
- latest_attempt: `att_0002`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-30T11:37:16.269475+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.575, long_threshold=0.375) | filters: max_probability_margin(min_margin=0.07) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=3)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `85.58200000000001` |
| `profit_factor` | `1.860639581657281` |
| `trade_count` | `220` |
| `win_rate` | `0.6454545454545455` |
| `expectancy_per_trade` | `1.9450454545454547` |
| `max_dd_pct` | `12.074400071366979` |
| `recovery_factor` | `5.269178672577267` |
| `net_profit` | `427.91` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `12.074400071366979` |
| `equity_dd_amount` | `81.21000000000004` |
| `max_dd_pct` | `8.974721820863062` |
| `max_dd_amount` | `60.25` |
| `ulcer_index` | `0.9020190671765489` |
| `worst_day` | `-25.309999999999995` |
| `worst_week` | `-8.69` |
| `min_free_margin` | `478.52` |
| `consecutive_losses` | `4` |
| `time_under_water` | `20484300.0` |
| `longest_recovery_duration` | `8037600.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `3.0` |
| `payoff_ratio` | `1.022041460346957` |
| `avg_win` | `6.514859154929577` |
| `avg_loss` | `-6.374358974358974` |
| `long_count` | `209` |
| `short_count` | `11` |
| `long_expectancy` | `1.6814354066985646` |
| `short_expectancy` | `6.953636363636364` |
| `mfe_mean` | `7.253318181818182` |
| `mfe_median` | `4.9` |
| `mfe_p90` | `16.858999999999998` |
| `mae_mean` | `5.369863636363636` |
| `mae_median` | `3.465` |
| `mae_p90` | `11.921` |
| `no_trade_rate` | `0.953980945899966` |
| `hold_distribution` | `{'p50': 3.0, 'p90': 3.0}` |
| `loss_trade_mfe` | `3.717564102564103` |
| `realized_over_mfe` | `-2.2918475898996333` |
| `rule_pass_rates` | `{'long_signal_rate': 0.044232732221844165, 'short_signal_rate': 0.0017863218781898605}` |
| `win_trade_mae` | `3.163591549295775` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0002 | completed | 2026-03-30 11:37:16 UTC | 6.72    | 159    | 6755  | 6720          | 35      
att_0001 | completed | 2026-03-30 11:32:14 UTC | 85.58   | 220    | 11756 | 11756         | 0       
```

### 75. `05_optimization` / `05CA_trend_proxy_persistence_riskoff_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05CA_trend_proxy_persistence_riskoff_0001\experiment_bundle.json`
- experiment_id: `exp_05ca_trend_proxy_persistence_riskoff_v1`
- bundle_status: `completed`
- latest_attempt: `att_0003`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-30T13:07:02.801226+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: max_probability_margin(min_margin=0.07) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=3)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `84.15199999999999` |
| `profit_factor` | `1.376037821847658` |
| `trade_count` | `488` |
| `win_rate` | `0.5430327868852459` |
| `expectancy_per_trade` | `0.8622131147540983` |
| `max_dd_pct` | `12.053703863194865` |
| `recovery_factor` | `3.3404255319148928` |
| `net_profit` | `420.76` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `12.053703863194865` |
| `equity_dd_amount` | `125.96000000000004` |
| `max_dd_pct` | `11.640003454861274` |
| `max_dd_amount` | `121.28999999999996` |
| `ulcer_index` | `7.274127603224929` |
| `worst_day` | `-30.5` |
| `worst_week` | `-37.67999999999999` |
| `min_free_margin` | `472.48` |
| `consecutive_losses` | `7` |
| `time_under_water` | `22846800.0` |
| `longest_recovery_duration` | `13839900.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `3.0` |
| `payoff_ratio` | `1.1579488085736895` |
| `avg_win` | `5.810150943396227` |
| `avg_loss` | `-5.017623318385651` |
| `long_count` | `205` |
| `short_count` | `283` |
| `long_expectancy` | `2.146048780487805` |
| `short_expectancy` | `-0.067773851590106` |
| `mfe_mean` | `5.9151639344262295` |
| `mfe_median` | `4.285` |
| `mfe_p90` | `13.169` |
| `mae_mean` | `5.057766393442623` |
| `mae_median` | `3.41` |
| `mae_p90` | `10.136000000000001` |
| `no_trade_rate` | `0.8985199047294998` |
| `hold_distribution` | `{'p50': 3.0, 'p90': 3.0}` |
| `loss_trade_mfe` | `2.864977578475336` |
| `realized_over_mfe` | `-3.190816570311263` |
| `rule_pass_rates` | `{'long_signal_rate': 0.044062606328683224, 'short_signal_rate': 0.057417488941816947}` |
| `win_trade_mae` | `2.7678867924528303` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0003 | completed | 2026-03-30 13:07:02 UTC | 38.46   | 330    | 6755  | 6720          | 35      
att_0002 | completed | 2026-03-30 13:05:59 UTC | 84.15   | 488    | 11756 | 11756         | 0       
att_0001 | completed | 2026-03-30 12:59:11 UTC | 84.15   | 488    | 11756 | 11756         | 0       
```

### 76. `05_optimization` / `05AO_05w_combo_loose_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05AO_05w_combo_loose_0001\experiment_bundle.json`
- experiment_id: `exp_05ao_05w_combo_loose_v1`
- bundle_status: `completed`
- latest_attempt: `att_0001`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-29T17:57:07.585361+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: combo_probability_gate(min_margin=0.05, min_probability_diff=0.07) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=3)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `82.792` |
| `profit_factor` | `1.3593839529109442` |
| `trade_count` | `500` |
| `win_rate` | `0.538` |
| `expectancy_per_trade` | `0.82792` |
| `max_dd_pct` | `12.88449601298764` |
| `recovery_factor` | `3.0681885561814393` |
| `net_profit` | `413.96` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `12.88449601298764` |
| `equity_dd_amount` | `134.92000000000007` |
| `max_dd_pct` | `12.470191635461662` |
| `max_dd_amount` | `130.21000000000004` |
| `ulcer_index` | `7.352021457537294` |
| `worst_day` | `-30.5` |
| `worst_week` | `-37.67999999999999` |
| `min_free_margin` | `472.48` |
| `consecutive_losses` | `8` |
| `time_under_water` | `22611900.0` |
| `longest_recovery_duration` | `13839900.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `3.0` |
| `payoff_ratio` | `1.1673520190424838` |
| `avg_win` | `5.82089219330855` |
| `avg_loss` | `-4.986406926406926` |
| `long_count` | `210` |
| `short_count` | `290` |
| `long_expectancy` | `2.090666666666667` |
| `short_expectancy` | `-0.08648275862068965` |
| `mfe_mean` | `5.84272` |
| `mfe_median` | `4.195` |
| `mfe_p90` | `13.088000000000001` |
| `mae_mean` | `5.0317799999999995` |
| `mae_median` | `3.46` |
| `mae_p90` | `9.938` |
| `no_trade_rate` | `0.8969887716910514` |
| `hold_distribution` | `{'p50': 3.0, 'p90': 3.0}` |
| `loss_trade_mfe` | `2.8156277056277057` |
| `realized_over_mfe` | `-2.961020476624279` |
| `rule_pass_rates` | `{'long_signal_rate': 0.04474310990132698, 'short_signal_rate': 0.05826811840762164}` |
| `win_trade_mae` | `2.7560594795539033` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0001 | completed | 2026-03-29 17:57:07 UTC | 82.79   | 500    | 11756 | 11756         | 0       
```

### 77. `05_optimization` / `05EN_05dp_short_bias_diff_hold5_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05EN_05dp_short_bias_diff_hold5_0001\experiment_bundle.json`
- experiment_id: `exp_05en_05dp_short_bias_diff_hold5_v1`
- bundle_status: `completed`
- latest_attempt: `att_0001`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-30T15:04:11.105599+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3, long_threshold=0.45) | filters: probability_difference(min_probability_diff=0.0775) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=5)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `82.05` |
| `profit_factor` | `1.4089169308055738` |
| `trade_count` | `332` |
| `win_rate` | `0.5090361445783133` |
| `expectancy_per_trade` | `1.2356927710843373` |
| `max_dd_pct` | `13.97179899687708` |
| `recovery_factor` | `2.7787185044703313` |
| `net_profit` | `410.25` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `13.97179899687708` |
| `equity_dd_amount` | `147.6400000000001` |
| `max_dd_pct` | `13.388711273502324` |
| `max_dd_amount` | `140.71000000000004` |
| `ulcer_index` | `6.987143419519953` |
| `worst_day` | `-38.74` |
| `worst_week` | `-51.34` |
| `min_free_margin` | `446.92` |
| `consecutive_losses` | `12` |
| `time_under_water` | `22887300.0` |
| `longest_recovery_duration` | `13839900.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `5.0` |
| `payoff_ratio` | `1.3588962113686898` |
| `avg_win` | `8.36396449704142` |
| `avg_loss` | `-6.154969325153374` |
| `long_count` | `121` |
| `short_count` | `211` |
| `long_expectancy` | `2.5522314049586776` |
| `short_expectancy` | `0.4807109004739336` |
| `mfe_mean` | `7.664668674698795` |
| `mfe_median` | `5.645` |
| `mfe_p90` | `15.90800000000001` |
| `mae_mean` | `6.694548192771085` |
| `mae_median` | `5.17` |
| `mae_p90` | `12.840000000000003` |
| `no_trade_rate` | `0.9174038788703641` |
| `hold_distribution` | `{'p50': 5.0, 'p90': 5.0}` |
| `loss_trade_mfe` | `3.5107361963190185` |
| `realized_over_mfe` | `-4.829103898529887` |
| `rule_pass_rates` | `{'long_signal_rate': 0.030792786662129975, 'short_signal_rate': 0.05180333446750596}` |
| `win_trade_mae` | `3.6028994082840238` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0001 | completed | 2026-03-30 15:04:11 UTC | 82.05   | 332    | 11756 | 11756         | 0       
```

### 78. `05_optimization` / `05T_no_ma_trend_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05T_no_ma_trend_0001\experiment_bundle.json`
- experiment_id: `exp_05t_moving_average_trend_sector_ablation_v1`
- bundle_status: `completed`
- latest_attempt: `att_0001`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-29T16:47:03.718358+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: max_probability_margin(min_margin=0.07) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=3)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `81.24600000000001` |
| `profit_factor` | `1.5315059531597541` |
| `trade_count` | `325` |
| `win_rate` | `0.5753846153846154` |
| `expectancy_per_trade` | `1.2499384615384617` |
| `max_dd_pct` | `12.389278564330052` |
| `recovery_factor` | `4.722506393861893` |
| `net_profit` | `406.23` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `12.389278564330052` |
| `equity_dd_amount` | `86.01999999999998` |
| `max_dd_pct` | `11.903832530973967` |
| `max_dd_amount` | `82.34000000000003` |
| `ulcer_index` | `2.366587565705905` |
| `worst_day` | `-29.390000000000004` |
| `worst_week` | `-25.15` |
| `min_free_margin` | `462.36` |
| `consecutive_losses` | `9` |
| `time_under_water` | `22153500.0` |
| `longest_recovery_duration` | `5186100.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `3.0` |
| `payoff_ratio` | `1.1302022542034549` |
| `avg_win` | `6.25951871657754` |
| `avg_loss` | `-5.538405797101449` |
| `long_count` | `152` |
| `short_count` | `173` |
| `long_expectancy` | `2.0530921052631577` |
| `short_expectancy` | `0.5442774566473989` |
| `mfe_mean` | `6.81163076923077` |
| `mfe_median` | `4.78` |
| `mfe_p90` | `15.330000000000005` |
| `mae_mean` | `5.144738461538461` |
| `mae_median` | `3.55` |
| `mae_p90` | `10.816` |
| `no_trade_rate` | `0.9495576726777816` |
| `hold_distribution` | `{'p50': 3.0, 'p90': 3.0}` |
| `loss_trade_mfe` | `3.4447101449275364` |
| `realized_over_mfe` | `-2.5398298479291297` |
| `rule_pass_rates` | `{'long_signal_rate': 0.024923443348077577, 'short_signal_rate': 0.025518883974140864}` |
| `win_trade_mae` | `2.917005347593583` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0001 | completed | 2026-03-29 16:47:03 UTC | 81.25   | 325    | 11756 | 11756         | 0       
```

### 79. `05_optimization` / `05AV_05ai_combo_loose_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05AV_05ai_combo_loose_0001\experiment_bundle.json`
- experiment_id: `exp_05av_05ai_combo_loose_v1`
- bundle_status: `completed`
- latest_attempt: `att_0001`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-30T10:40:58.380371+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: combo_probability_gate(min_margin=0.05, min_probability_diff=0.07) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=3)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `80.51` |
| `profit_factor` | `1.3499278499278498` |
| `trade_count` | `492` |
| `win_rate` | `0.5345528455284553` |
| `expectancy_per_trade` | `0.8181910569105691` |
| `max_dd_pct` | `12.898609580166692` |
| `recovery_factor` | `3.0176161919040485` |
| `net_profit` | `402.55` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `12.898609580166692` |
| `equity_dd_amount` | `133.39999999999998` |
| `max_dd_pct` | `12.479151312982435` |
| `max_dd_amount` | `128.69000000000005` |
| `ulcer_index` | `7.302510554592419` |
| `worst_day` | `-23.57` |
| `worst_week` | `-37.67999999999999` |
| `min_free_margin` | `472.48` |
| `consecutive_losses` | `10` |
| `time_under_water` | `22614900.0` |
| `longest_recovery_duration` | `13839900.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `3.0` |
| `payoff_ratio` | `1.1754124624847058` |
| `avg_win` | `5.904676806083651` |
| `avg_loss` | `-5.02349344978166` |
| `long_count` | `205` |
| `short_count` | `287` |
| `long_expectancy` | `2.1150243902439025` |
| `short_expectancy` | `-0.10811846689895471` |
| `mfe_mean` | `5.90760162601626` |
| `mfe_median` | `4.3` |
| `mfe_p90` | `13.187000000000001` |
| `mae_mean` | `5.067418699186992` |
| `mae_median` | `3.46` |
| `mae_p90` | `10.118000000000004` |
| `no_trade_rate` | `0.8979244641034365` |
| `hold_distribution` | `{'p50': 3.0, 'p90': 3.0}` |
| `loss_trade_mfe` | `2.82353711790393` |
| `realized_over_mfe` | `-3.2527422317843873` |
| `rule_pass_rates` | `{'long_signal_rate': 0.044062606328683224, 'short_signal_rate': 0.058012929567880234}` |
| `win_trade_mae` | `2.7584410646387836` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0001 | completed | 2026-03-30 10:40:58 UTC | 80.51   | 492    | 11756 | 11756         | 0       
```

### 80. `05_optimization` / `05CC_trend_proxy_persistence_downside_riskoff_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05CC_trend_proxy_persistence_downside_riskoff_0001\experiment_bundle.json`
- experiment_id: `exp_05cc_trend_proxy_persistence_downside_riskoff_v1`
- bundle_status: `completed`
- latest_attempt: `att_0003`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-30T13:09:47.516499+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: max_probability_margin(min_margin=0.07) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=3)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `78.506` |
| `profit_factor` | `1.3414313797122628` |
| `trade_count` | `495` |
| `win_rate` | `0.5414141414141415` |
| `expectancy_per_trade` | `0.7929898989898989` |
| `max_dd_pct` | `12.006369111785821` |
| `recovery_factor` | `3.2333607907743` |
| `net_profit` | `392.53` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `12.006369111785821` |
| `equity_dd_amount` | `121.39999999999998` |
| `max_dd_pct` | `11.613377434766626` |
| `max_dd_amount` | `116.91999999999996` |
| `ulcer_index` | `7.248835496808677` |
| `worst_day` | `-30.5` |
| `worst_week` | `-37.67999999999999` |
| `min_free_margin` | `472.48` |
| `consecutive_losses` | `9` |
| `time_under_water` | `22983600.0` |
| `longest_recovery_duration` | `13839900.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `3.0` |
| `payoff_ratio` | `1.1362123999801628` |
| `avg_win` | `5.754440298507463` |
| `avg_loss` | `-5.064581497797358` |
| `long_count` | `206` |
| `short_count` | `289` |
| `long_expectancy` | `1.5776699029126213` |
| `short_expectancy` | `0.23366782006920417` |
| `mfe_mean` | `5.9941414141414135` |
| `mfe_median` | `4.29` |
| `mfe_p90` | `13.412000000000008` |
| `mae_mean` | `4.914141414141414` |
| `mae_median` | `3.41` |
| `mae_p90` | `9.866000000000003` |
| `no_trade_rate` | `0.8973290234773733` |
| `hold_distribution` | `{'p50': 3.0, 'p90': 3.0}` |
| `loss_trade_mfe` | `3.127488986784141` |
| `realized_over_mfe` | `-2.7792638850734943` |
| `rule_pass_rates` | `{'long_signal_rate': 0.044147669275263694, 'short_signal_rate': 0.05852330724736305}` |
| `win_trade_mae` | `2.7494402985074626` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0003 | completed | 2026-03-30 13:09:47 UTC | 47.40   | 333    | 6755  | 6720          | 35      
att_0002 | completed | 2026-03-30 13:08:43 UTC | 78.51   | 495    | 11756 | 11756         | 0       
att_0001 | completed | 2026-03-30 13:02:35 UTC | 78.51   | 495    | 11756 | 11756         | 0       
```

### 81. `05_optimization` / `05BZ_trend_proxy_persistence_downside_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05BZ_trend_proxy_persistence_downside_0001\experiment_bundle.json`
- experiment_id: `exp_05bz_trend_proxy_persistence_downside_v1`
- bundle_status: `completed`
- latest_attempt: `att_0001`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-30T12:57:28.405498+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: max_probability_margin(min_margin=0.07) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=3)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `78.354` |
| `profit_factor` | `1.3388339690200046` |
| `trade_count` | `494` |
| `win_rate` | `0.5445344129554656` |
| `expectancy_per_trade` | `0.7930566801619433` |
| `max_dd_pct` | `12.272825936815517` |
| `recovery_factor` | `3.149529704960206` |
| `net_profit` | `391.77` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `12.272825936815517` |
| `equity_dd_amount` | `124.38999999999999` |
| `max_dd_pct` | `12.002256174794171` |
| `max_dd_amount` | `121.28999999999996` |
| `ulcer_index` | `7.3678982691913975` |
| `worst_day` | `-30.5` |
| `worst_week` | `-37.67999999999999` |
| `min_free_margin` | `472.48` |
| `consecutive_losses` | `7` |
| `time_under_water` | `22846800.0` |
| `longest_recovery_duration` | `13839900.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `3.0` |
| `payoff_ratio` | `1.1198425391431266` |
| `avg_win` | `5.754646840148699` |
| `avg_loss` | `-5.1388` |
| `long_count` | `207` |
| `short_count` | `287` |
| `long_expectancy` | `1.6199033816425121` |
| `short_expectancy` | `0.1966898954703833` |
| `mfe_mean` | `6.013744939271255` |
| `mfe_median` | `4.33` |
| `mfe_p90` | `13.448999999999996` |
| `mae_mean` | `4.89831983805668` |
| `mae_median` | `3.43` |
| `mae_p90` | `9.881999999999998` |
| `no_trade_rate` | `0.8984348417829193` |
| `hold_distribution` | `{'p50': 3.0, 'p90': 3.0}` |
| `loss_trade_mfe` | `3.147777777777778` |
| `realized_over_mfe` | `-2.8260788585954524` |
| `rule_pass_rates` | `{'long_signal_rate': 0.04397754338210275, 'short_signal_rate': 0.05758761483497788}` |
| `win_trade_mae` | `2.70271375464684` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0001 | completed | 2026-03-30 12:57:28 UTC | 78.35   | 494    | 11756 | 11756         | 0       
```

### 82. `05_optimization` / `05Z_no_leader_rel_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05Z_no_leader_rel_0001\experiment_bundle.json`
- experiment_id: `exp_05z_leader_relative_sector_ablation_v1`
- bundle_status: `completed`
- latest_attempt: `att_0001`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-29T16:55:28.322666+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: max_probability_margin(min_margin=0.07) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=3)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `77.97` |
| `profit_factor` | `1.3350637295768837` |
| `trade_count` | `523` |
| `win_rate` | `0.5372848948374761` |
| `expectancy_per_trade` | `0.7454110898661568` |
| `max_dd_pct` | `11.797752808988765` |
| `recovery_factor` | `5.4018290148261` |
| `net_profit` | `389.85` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `11.797752808988765` |
| `equity_dd_amount` | `72.17000000000007` |
| `max_dd_pct` | `9.91656353547048` |
| `max_dd_amount` | `52.879999999999995` |
| `ulcer_index` | `3.5705661306043974` |
| `worst_day` | `-34.56` |
| `worst_week` | `-23.740000000000002` |
| `min_free_margin` | `438.67` |
| `consecutive_losses` | `6` |
| `time_under_water` | `22858500.0` |
| `longest_recovery_duration` | `8833500.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `3.0` |
| `payoff_ratio` | `1.1497701870377433` |
| `avg_win` | `5.52797153024911` |
| `avg_loss` | `-4.807892561983471` |
| `long_count` | `253` |
| `short_count` | `270` |
| `long_expectancy` | `0.858300395256917` |
| `short_expectancy` | `0.6396296296296295` |
| `mfe_mean` | `5.553097514340344` |
| `mfe_median` | `4.03` |
| `mfe_p90` | `12.268` |
| `mae_mean` | `4.924933078393881` |
| `mae_median` | `3.33` |
| `mae_p90` | `10.666` |
| `no_trade_rate` | `0.8914596801633209` |
| `hold_distribution` | `{'p50': 3.0, 'p90': 3.0}` |
| `loss_trade_mfe` | `2.5833471074380165` |
| `realized_over_mfe` | `-3.6812509043736696` |
| `rule_pass_rates` | `{'long_signal_rate': 0.05248383804014971, 'short_signal_rate': 0.05605648179652943}` |
| `win_trade_mae` | `2.6182562277580073` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0001 | completed | 2026-03-29 16:55:28 UTC | 77.97   | 523    | 11756 | 11756         | 0       
```

### 83. `05_optimization` / `05BM_05w_balanced_tight_margin_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05BM_05w_balanced_tight_margin_0001\experiment_bundle.json`
- experiment_id: `exp_05bm_05w_balanced_tight_margin_v1`
- bundle_status: `completed`
- latest_attempt: `att_0002`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-30T11:38:10.500575+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.45, long_threshold=0.45) | filters: max_probability_margin(min_margin=0.07) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=3)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `77.296` |
| `profit_factor` | `1.420023039972178` |
| `trade_count` | `355` |
| `win_rate` | `0.532394366197183` |
| `expectancy_per_trade` | `1.0886760563380282` |
| `max_dd_pct` | `11.064699159527876` |
| `recovery_factor` | `3.532723948811701` |
| `net_profit` | `386.48` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `11.064699159527876` |
| `equity_dd_amount` | `109.39999999999998` |
| `max_dd_pct` | `10.556826849733024` |
| `max_dd_amount` | `103.79999999999995` |
| `ulcer_index` | `6.6881368735102` |
| `worst_day` | `-32.36` |
| `worst_week` | `-43.27` |
| `min_free_margin` | `470.23` |
| `consecutive_losses` | `8` |
| `time_under_water` | `22776000.0` |
| `longest_recovery_duration` | `13839900.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `3.0` |
| `payoff_ratio` | `1.2472160033618074` |
| `avg_win` | `6.913333333333333` |
| `avg_loss` | `-5.543012048192771` |
| `long_count` | `160` |
| `short_count` | `195` |
| `long_expectancy` | `2.1174375000000003` |
| `short_expectancy` | `0.24456410256410258` |
| `mfe_mean` | `6.744647887323944` |
| `mfe_median` | `4.94` |
| `mfe_p90` | `14.576` |
| `mae_mean` | `5.7901690140845075` |
| `mae_median` | `4.21` |
| `mae_p90` | `11.592` |
| `no_trade_rate` | `0.9282068730860837` |
| `hold_distribution` | `{'p50': 3.0, 'p90': 3.0}` |
| `loss_trade_mfe` | `3.0836746987951806` |
| `realized_over_mfe` | `-3.4681048014133737` |
| `rule_pass_rates` | `{'long_signal_rate': 0.03402517863218782, 'short_signal_rate': 0.037767948281728476}` |
| `win_trade_mae` | `3.1652910052910053` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0002 | completed | 2026-03-30 11:38:10 UTC | 28.58   | 227    | 6755  | 6720          | 35      
att_0001 | completed | 2026-03-30 11:34:58 UTC | 77.30   | 355    | 11756 | 11756         | 0       
```

### 84. `05_optimization` / `05AD_drop_di_spread14_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05AD_drop_di_spread14_0001\experiment_bundle.json`
- experiment_id: `exp_05ad_di_spread_14_feature_ablation_v1`
- bundle_status: `completed`
- latest_attempt: `att_0002`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-29T17:22:46.800063+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: max_probability_margin(min_margin=0.07) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=3)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `76.554` |
| `profit_factor` | `1.3094366163024762` |
| `trade_count` | `524` |
| `win_rate` | `0.5209923664122137` |
| `expectancy_per_trade` | `0.7304770992366412` |
| `max_dd_pct` | `11.151322923443937` |
| `recovery_factor` | `4.652607268749241` |
| `net_profit` | `382.77` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `11.151322923443937` |
| `equity_dd_amount` | `82.26999999999998` |
| `max_dd_pct` | `8.789022386526996` |
| `max_dd_amount` | `78.76999999999998` |
| `ulcer_index` | `4.33480346999596` |
| `worst_day` | `-27.139999999999997` |
| `worst_week` | `-29.479999999999997` |
| `min_free_margin` | `470.33` |
| `consecutive_losses` | `7` |
| `time_under_water` | `22345800.0` |
| `longest_recovery_duration` | `13157100.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `3.0` |
| `payoff_ratio` | `1.2039142516187602` |
| `avg_win` | `5.933186813186813` |
| `avg_loss` | `-4.928247011952191` |
| `long_count` | `216` |
| `short_count` | `308` |
| `long_expectancy` | `1.088888888888889` |
| `short_expectancy` | `0.4791233766233766` |
| `mfe_mean` | `5.791087786259542` |
| `mfe_median` | `4.1` |
| `mfe_p90` | `13.520999999999999` |
| `mae_mean` | `4.913053435114504` |
| `mae_median` | `3.475` |
| `mae_p90` | `10.629` |
| `no_trade_rate` | `0.8944368832936372` |
| `hold_distribution` | `{'p50': 3.0, 'p90': 3.0}` |
| `loss_trade_mfe` | `2.764741035856574` |
| `realized_over_mfe` | `-3.4142922651551033` |
| `rule_pass_rates` | `{'long_signal_rate': 0.04499829874106839, 'short_signal_rate': 0.06056481796529432}` |
| `win_trade_mae` | `2.586153846153846` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0002 | completed | 2026-03-29 17:22:46 UTC | 23.92   | 346    | 6755  | 6720          | 35      
att_0001 | completed | 2026-03-29 17:21:54 UTC | 76.55   | 524    | 11756 | 11756         | 0       
```

### 85. `05_optimization` / `05BB_trend_proxy_persistence_only_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05BB_trend_proxy_persistence_only_0001\experiment_bundle.json`
- experiment_id: `exp_05bb_trend_proxy_persistence_only_v1`
- bundle_status: `completed`
- latest_attempt: `att_0002`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-30T11:27:45.867308+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: max_probability_margin(min_margin=0.07) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=3)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `75.676` |
| `profit_factor` | `1.3308037978003533` |
| `trade_count` | `490` |
| `win_rate` | `0.5387755102040817` |
| `expectancy_per_trade` | `0.7722040816326531` |
| `max_dd_pct` | `12.34551853777547` |
| `recovery_factor` | `3.064550093140033` |
| `net_profit` | `378.38` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `12.34551853777547` |
| `equity_dd_amount` | `123.47000000000003` |
| `max_dd_pct` | `11.787981039607939` |
| `max_dd_amount` | `117.38` |
| `ulcer_index` | `7.260856883657908` |
| `worst_day` | `-24.010000000000005` |
| `worst_week` | `-37.67999999999999` |
| `min_free_margin` | `472.48` |
| `consecutive_losses` | `10` |
| `time_under_water` | `22989900.0` |
| `longest_recovery_duration` | `13839900.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `3.0` |
| `payoff_ratio` | `1.1392487056927265` |
| `avg_win` | `5.765909090909091` |
| `avg_loss` | `-5.061150442477876` |
| `long_count` | `202` |
| `short_count` | `288` |
| `long_expectancy` | `1.5388118811881186` |
| `short_expectancy` | `0.2345138888888889` |
| `mfe_mean` | `6.01561224489796` |
| `mfe_median` | `4.3149999999999995` |
| `mfe_p90` | `13.570000000000002` |
| `mae_mean` | `4.921673469387755` |
| `mae_median` | `3.46` |
| `mae_p90` | `9.786000000000003` |
| `no_trade_rate` | `0.8987750935692412` |
| `hold_distribution` | `{'p50': 3.0, 'p90': 3.0}` |
| `loss_trade_mfe` | `3.158716814159292` |
| `realized_over_mfe` | `-2.826675245247619` |
| `rule_pass_rates` | `{'long_signal_rate': 0.043382102756039466, 'short_signal_rate': 0.05784280367471929}` |
| `win_trade_mae` | `2.7706439393939397` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0002 | completed | 2026-03-30 11:27:45 UTC | 44.79   | 328    | 6755  | 6720          | 35      
att_0001 | completed | 2026-03-30 11:26:41 UTC | 75.68   | 490    | 11756 | 11756         | 0       
```

### 86. `05_optimization` / `05X_no_session_ctx_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05X_no_session_ctx_0001\experiment_bundle.json`
- experiment_id: `exp_05x_session_context_sector_ablation_v1`
- bundle_status: `completed`
- latest_attempt: `att_0001`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-29T16:52:40.356808+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: max_probability_margin(min_margin=0.07) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=3)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `75.382` |
| `profit_factor` | `1.3200988551822537` |
| `trade_count` | `499` |
| `win_rate` | `0.5410821643286573` |
| `expectancy_per_trade` | `0.7553306613226454` |
| `max_dd_pct` | `11.600394811054722` |
| `recovery_factor` | `4.581378388233859` |
| `net_profit` | `376.91` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `11.600394811054722` |
| `equity_dd_amount` | `82.2700000000001` |
| `max_dd_pct` | `8.815691290907148` |
| `max_dd_amount` | `66.15999999999997` |
| `ulcer_index` | `2.3678233395679746` |
| `worst_day` | `-25.270000000000003` |
| `worst_week` | `-23.099999999999998` |
| `min_free_margin` | `460.72` |
| `consecutive_losses` | `6` |
| `time_under_water` | `21678300.0` |
| `longest_recovery_duration` | `4311600.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `3.0` |
| `payoff_ratio` | `1.1196393993953189` |
| `avg_win` | `5.757000000000001` |
| `avg_loss` | `-5.141834061135372` |
| `long_count` | `217` |
| `short_count` | `282` |
| `long_expectancy` | `0.5986175115207374` |
| `short_expectancy` | `0.8759219858156028` |
| `mfe_mean` | `5.766613226452906` |
| `mfe_median` | `4.17` |
| `mfe_p90` | `12.919999999999998` |
| `mae_mean` | `5.003967935871744` |
| `mae_median` | `3.51` |
| `mae_p90` | `10.834` |
| `no_trade_rate` | `0.9014971078598163` |
| `hold_distribution` | `{'p50': 3.0, 'p90': 3.0}` |
| `loss_trade_mfe` | `2.7937991266375546` |
| `realized_over_mfe` | `-2.8761501611224403` |
| `rule_pass_rates` | `{'long_signal_rate': 0.04125552909152773, 'short_signal_rate': 0.057247363048656005}` |
| `win_trade_mae` | `2.6382962962962964` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0001 | completed | 2026-03-29 16:52:40 UTC | 75.38   | 499    | 11756 | 11756         | 0       
```

### 87. `05_optimization` / `05AJ_trend_proxy_light_vb_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05AJ_trend_proxy_light_vb_0001\experiment_bundle.json`
- experiment_id: `exp_05aj_trend_proxy_light_vb_v1`
- bundle_status: `completed`
- latest_attempt: `att_0002`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-29T17:54:12.391744+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: max_probability_margin(min_margin=0.07) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=3)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `75.362` |
| `profit_factor` | `1.3242296737998742` |
| `trade_count` | `492` |
| `win_rate` | `0.5447154471544715` |
| `expectancy_per_trade` | `0.7658739837398374` |
| `max_dd_pct` | `12.061998673180145` |
| `recovery_factor` | `3.1400833333333336` |
| `net_profit` | `376.81` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `12.061998673180145` |
| `equity_dd_amount` | `120.0` |
| `max_dd_pct` | `11.601201758277217` |
| `max_dd_amount` | `115.07000000000005` |
| `ulcer_index` | `7.169615998911733` |
| `worst_day` | `-23.57` |
| `worst_week` | `-37.67999999999999` |
| `min_free_margin` | `472.48` |
| `consecutive_losses` | `10` |
| `time_under_water` | `22857900.0` |
| `longest_recovery_duration` | `13839900.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `3.0` |
| `payoff_ratio` | `1.1068188318327308` |
| `avg_win` | `5.742462686567165` |
| `avg_loss` | `-5.188258928571429` |
| `long_count` | `202` |
| `short_count` | `290` |
| `long_expectancy` | `1.6293069306930694` |
| `short_expectancy` | `0.16444827586206895` |
| `mfe_mean` | `6.045752032520325` |
| `mfe_median` | `4.4350000000000005` |
| `mfe_p90` | `13.650000000000004` |
| `mae_mean` | `4.929857723577236` |
| `mae_median` | `3.43` |
| `mae_p90` | `10.002000000000002` |
| `no_trade_rate` | `0.8984348417829193` |
| `hold_distribution` | `{'p50': 3.0, 'p90': 3.0}` |
| `loss_trade_mfe` | `3.1683035714285714` |
| `realized_over_mfe` | `-3.0771064052311394` |
| `rule_pass_rates` | `{'long_signal_rate': 0.04355222864920041, 'short_signal_rate': 0.058012929567880234}` |
| `win_trade_mae` | `2.7199253731343287` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0002 | completed | 2026-03-29 17:54:12 UTC | 34.76   | 334    | 6755  | 6720          | 35      
att_0001 | completed | 2026-03-29 17:53:10 UTC | 75.36   | 492    | 11756 | 11756         | 0       
```

### 88. `05_optimization` / `05R_semantic_interact_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05R_semantic_interact_0001\experiment_bundle.json`
- experiment_id: `exp_05R_semantic_interact_v1`
- bundle_status: `completed`
- latest_attempt: `att_0002`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-29T16:35:41.661156+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: max_probability_margin(min_margin=0.07) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=3)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `75.154` |
| `profit_factor` | `1.191124561314277` |
| `trade_count` | `847` |
| `win_rate` | `0.5053128689492326` |
| `expectancy_per_trade` | `0.44364817001180634` |
| `max_dd_pct` | `21.80504885694906` |
| `recovery_factor` | `3.159324028922144` |
| `net_profit` | `375.77` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `21.80504885694906` |
| `equity_dd_amount` | `118.94000000000005` |
| `max_dd_pct` | `21.486057895026313` |
| `max_dd_amount` | `117.20000000000005` |
| `ulcer_index` | `8.030834928266234` |
| `worst_day` | `-41.67` |
| `worst_week` | `-40.73000000000001` |
| `min_free_margin` | `416.44` |
| `consecutive_losses` | `11` |
| `time_under_water` | `23113200.0` |
| `longest_recovery_duration` | `13839900.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `3.0` |
| `payoff_ratio` | `1.1660775495109394` |
| `avg_win` | `5.471658878504672` |
| `avg_loss` | `-4.6923627684964195` |
| `long_count` | `370` |
| `short_count` | `477` |
| `long_expectancy` | `1.0824054054054055` |
| `short_expectancy` | `-0.05182389937106921` |
| `mfe_mean` | `5.0658441558441565` |
| `mfe_median` | `3.53` |
| `mfe_p90` | `10.021999999999998` |
| `mae_mean` | `4.972998819362456` |
| `mae_median` | `3.78` |
| `mae_p90` | `10.52` |
| `no_trade_rate` | `0.8206022456617897` |
| `hold_distribution` | `{'p50': 3.0, 'p90': 3.0}` |
| `loss_trade_mfe` | `2.2453221957040572` |
| `realized_over_mfe` | `-3.1758183995815097` |
| `rule_pass_rates` | `{'long_signal_rate': 0.07417488941816945, 'short_signal_rate': 0.10522286492004083}` |
| `win_trade_mae` | `2.8408177570093454` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0002 | completed | 2026-03-29 16:35:41 UTC | -1.02   | 527    | 6755  | 6720          | 35      
att_0001 | completed | 2026-03-29 16:34:03 UTC | 75.15   | 847    | 11756 | 11756         | 0       
```

### 89. `05_optimization` / `05BC_trend_proxy_breakout_only_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05BC_trend_proxy_breakout_only_0001\experiment_bundle.json`
- experiment_id: `exp_05bc_trend_proxy_breakout_only_v1`
- bundle_status: `completed`
- latest_attempt: `att_0001`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-30T11:15:30.250419+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: max_probability_margin(min_margin=0.07) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=3)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `74.408` |
| `profit_factor` | `1.3218812455118831` |
| `trade_count` | `493` |
| `win_rate` | `0.5354969574036511` |
| `expectancy_per_trade` | `0.7546450304259635` |
| `max_dd_pct` | `11.87891186777127` |
| `recovery_factor` | `3.1719669196009903` |
| `net_profit` | `372.04` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `11.87891186777127` |
| `equity_dd_amount` | `117.28999999999996` |
| `max_dd_pct` | `11.485168630637947` |
| `max_dd_amount` | `113.05999999999995` |
| `ulcer_index` | `7.0988967873767725` |
| `worst_day` | `-23.57` |
| `worst_week` | `-37.67999999999999` |
| `min_free_margin` | `472.48` |
| `consecutive_losses` | `7` |
| `time_under_water` | `22756200.0` |
| `longest_recovery_duration` | `13839900.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `3.0` |
| `payoff_ratio` | `1.1466318379629594` |
| `avg_win` | `5.787386363636363` |
| `avg_loss` | `-5.047292576419213` |
| `long_count` | `206` |
| `short_count` | `287` |
| `long_expectancy` | `1.6235436893203883` |
| `short_expectancy` | `0.13097560975609757` |
| `mfe_mean` | `5.997099391480731` |
| `mfe_median` | `4.28` |
| `mfe_p90` | `13.486000000000004` |
| `mae_mean` | `4.902596348884382` |
| `mae_median` | `3.47` |
| `mae_p90` | `9.898000000000001` |
| `no_trade_rate` | `0.8979244641034365` |
| `hold_distribution` | `{'p50': 3.0, 'p90': 3.0}` |
| `loss_trade_mfe` | `3.1558515283842796` |
| `realized_over_mfe` | `-2.803970922348266` |
| `rule_pass_rates` | `{'long_signal_rate': 0.04397754338210275, 'short_signal_rate': 0.058097992514460704}` |
| `win_trade_mae` | `2.7266666666666666` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0001 | completed | 2026-03-30 11:15:30 UTC | 74.41   | 493    | 11756 | 11756         | 0       
```

### 90. `05_optimization` / `05BD_trend_proxy_volatility_only_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05BD_trend_proxy_volatility_only_0001\experiment_bundle.json`
- experiment_id: `exp_05bd_trend_proxy_volatility_only_v1`
- bundle_status: `completed`
- latest_attempt: `att_0001`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-30T11:17:11.296277+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: max_probability_margin(min_margin=0.07) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=3)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `74.302` |
| `profit_factor` | `1.3161141554065552` |
| `trade_count` | `491` |
| `win_rate` | `0.5437881873727087` |
| `expectancy_per_trade` | `0.7566395112016293` |
| `max_dd_pct` | `12.812750601443469` |
| `recovery_factor` | `2.906509153497104` |
| `net_profit` | `371.51` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `12.812750601443469` |
| `equity_dd_amount` | `127.82000000000005` |
| `max_dd_pct` | `12.377591441957735` |
| `max_dd_amount` | `123.11000000000001` |
| `ulcer_index` | `7.29812701514261` |
| `worst_day` | `-23.369999999999997` |
| `worst_week` | `-37.67999999999999` |
| `min_free_margin` | `472.48` |
| `consecutive_losses` | `9` |
| `time_under_water` | `22848000.0` |
| `longest_recovery_duration` | `13839900.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `3.0` |
| `payoff_ratio` | `1.1041556959216043` |
| `avg_win` | `5.793071161048689` |
| `avg_loss` | `-5.246607142857143` |
| `long_count` | `204` |
| `short_count` | `287` |
| `long_expectancy` | `1.5040196078431372` |
| `short_expectancy` | `0.2254006968641115` |
| `mfe_mean` | `6.046558044806518` |
| `mfe_median` | `4.32` |
| `mfe_p90` | `13.71` |
| `mae_mean` | `4.991588594704684` |
| `mae_median` | `3.41` |
| `mae_p90` | `10.13` |
| `no_trade_rate` | `0.8985199047294998` |
| `hold_distribution` | `{'p50': 3.0, 'p90': 3.0}` |
| `loss_trade_mfe` | `3.1051339285714286` |
| `realized_over_mfe` | `-2.882274178028967` |
| `rule_pass_rates` | `{'long_signal_rate': 0.04380741748894182, 'short_signal_rate': 0.05767267778155835}` |
| `win_trade_mae` | `2.7582771535580526` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0001 | completed | 2026-03-30 11:17:11 UTC | 74.30   | 491    | 11756 | 11756         | 0       
```

### 91. `05_optimization` / `05AF_drop_vortex_indicator_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05AF_drop_vortex_indicator_0001\experiment_bundle.json`
- experiment_id: `exp_05af_vortex_indicator_feature_ablation_v1`
- bundle_status: `completed`
- latest_attempt: `att_0001`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-29T17:20:29.788948+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: max_probability_margin(min_margin=0.07) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=3)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `73.57400000000001` |
| `profit_factor` | `1.2926547919268743` |
| `trade_count` | `533` |
| `win_rate` | `0.525328330206379` |
| `expectancy_per_trade` | `0.690187617260788` |
| `max_dd_pct` | `11.858567804428041` |
| `recovery_factor` | `4.471496292694787` |
| `net_profit` | `367.87` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `11.858567804428041` |
| `equity_dd_amount` | `82.26999999999998` |
| `max_dd_pct` | `8.777753591641268` |
| `max_dd_amount` | `64.51999999999998` |
| `ulcer_index` | `3.0411310621427456` |
| `worst_day` | `-22.61` |
| `worst_week` | `-31.279999999999994` |
| `min_free_margin` | `463.45` |
| `consecutive_losses` | `7` |
| `time_under_water` | `22353300.0` |
| `longest_recovery_duration` | `8833500.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `3.0` |
| `payoff_ratio` | `1.1680059369910685` |
| `avg_win` | `5.803142857142857` |
| `avg_loss` | `-4.968418972332016` |
| `long_count` | `245` |
| `short_count` | `288` |
| `long_expectancy` | `0.4310612244897959` |
| `short_expectancy` | `0.910625` |
| `mfe_mean` | `5.7778611632270165` |
| `mfe_median` | `4.03` |
| `mfe_p90` | `12.919999999999998` |
| `mae_mean` | `4.869155722326455` |
| `mae_median` | `3.47` |
| `mae_p90` | `10.362000000000002` |
| `no_trade_rate` | `0.8935011908812521` |
| `hold_distribution` | `{'p50': 3.0, 'p90': 3.0}` |
| `loss_trade_mfe` | `2.7877075098814226` |
| `realized_over_mfe` | `-3.3388489320996264` |
| `rule_pass_rates` | `{'long_signal_rate': 0.04959169785641375, 'short_signal_rate': 0.05690711126233413}` |
| `win_trade_mae` | `2.59175` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0001 | completed | 2026-03-29 17:20:29 UTC | 73.57   | 533    | 11756 | 11756         | 0       
```

### 92. `05_optimization` / `05CD_trend_proxy_persistence_session_riskoff_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05CD_trend_proxy_persistence_session_riskoff_0001\experiment_bundle.json`
- experiment_id: `exp_05cd_trend_proxy_persistence_session_riskoff_v1`
- bundle_status: `completed`
- latest_attempt: `att_0001`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-30T13:04:18.304485+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: max_probability_margin(min_margin=0.07) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=3)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `73.066` |
| `profit_factor` | `1.315371932217436` |
| `trade_count` | `489` |
| `win_rate` | `0.5439672801635992` |
| `expectancy_per_trade` | `0.7470961145194274` |
| `max_dd_pct` | `12.05166600454319` |
| `recovery_factor` | `3.0879046572563587` |
| `net_profit` | `365.33` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `12.05166600454319` |
| `equity_dd_amount` | `118.31000000000006` |
| `max_dd_pct` | `11.584636920027382` |
| `max_dd_amount` | `113.38` |
| `ulcer_index` | `7.1455883131025395` |
| `worst_day` | `-30.5` |
| `worst_week` | `-37.67999999999999` |
| `min_free_margin` | `472.48` |
| `consecutive_losses` | `7` |
| `time_under_water` | `22849800.0` |
| `longest_recovery_duration` | `13839900.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `3.0` |
| `payoff_ratio` | `1.102736619866497` |
| `avg_win` | `5.728345864661654` |
| `avg_loss` | `-5.194663677130046` |
| `long_count` | `205` |
| `short_count` | `284` |
| `long_expectancy` | `1.603170731707317` |
| `short_expectancy` | `0.1291549295774648` |
| `mfe_mean` | `6.000081799591002` |
| `mfe_median` | `4.32` |
| `mfe_p90` | `13.58` |
| `mae_mean` | `4.941308793456033` |
| `mae_median` | `3.45` |
| `mae_p90` | `10.033999999999997` |
| `no_trade_rate` | `0.8992004083021435` |
| `hold_distribution` | `{'p50': 3.0, 'p90': 3.0}` |
| `loss_trade_mfe` | `3.1383856502242153` |
| `realized_over_mfe` | `-3.1024466758053295` |
| `rule_pass_rates` | `{'long_signal_rate': 0.043467165702619937, 'short_signal_rate': 0.057332425995236476}` |
| `win_trade_mae` | `2.7363157894736845` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0001 | completed | 2026-03-30 13:04:18 UTC | 73.07   | 489    | 11756 | 11756         | 0       
```

### 93. `05_optimization` / `05BP_frontier_vote_w_bb_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05BP_frontier_vote_w_bb_0001\experiment_bundle.json`
- experiment_id: `exp_05bp_frontier_vote_w_bb_v1`
- bundle_status: `completed`
- latest_attempt: `att_0001`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-30T11:46:48.345992+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: max_probability_margin(min_margin=0.07) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=3)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `72.70599999999999` |
| `profit_factor` | `1.3149109053266226` |
| `trade_count` | `488` |
| `win_rate` | `0.5430327868852459` |
| `expectancy_per_trade` | `0.7449385245901639` |
| `max_dd_pct` | `13.085573092632746` |
| `recovery_factor` | `2.8017726396917144` |
| `net_profit` | `363.53` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `13.085573092632746` |
| `equity_dd_amount` | `129.75` |
| `max_dd_pct` | `12.648573191579764` |
| `max_dd_amount` | `125.04000000000008` |
| `ulcer_index` | `7.820985071696121` |
| `worst_day` | `-30.5` |
| `worst_week` | `-37.67999999999999` |
| `min_free_margin` | `472.48` |
| `consecutive_losses` | `10` |
| `time_under_water` | `22848900.0` |
| `longest_recovery_duration` | `13839900.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `3.0` |
| `payoff_ratio` | `1.1065099316522147` |
| `avg_win` | `5.728000000000001` |
| `avg_loss` | `-5.176636771300449` |
| `long_count` | `203` |
| `short_count` | `285` |
| `long_expectancy` | `1.577192118226601` |
| `short_expectancy` | `0.152140350877193` |
| `mfe_mean` | `6.003299180327869` |
| `mfe_median` | `4.3149999999999995` |
| `mfe_p90` | `13.590000000000002` |
| `mae_mean` | `4.950266393442623` |
| `mae_median` | `3.46` |
| `mae_p90` | `9.954` |
| `no_trade_rate` | `0.8989452194624021` |
| `hold_distribution` | `{'p50': 3.0, 'p90': 3.0}` |
| `loss_trade_mfe` | `3.1310313901345292` |
| `realized_over_mfe` | `-2.8766777918553124` |
| `rule_pass_rates` | `{'long_signal_rate': 0.04363729159578088, 'short_signal_rate': 0.057417488941816947}` |
| `win_trade_mae` | `2.753433962264151` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0001 | completed | 2026-03-30 11:46:48 UTC | 72.71   | 488    | 11756 | 11756         | 0       
```

### 94. `05_optimization` / `05BS_frontier_vote_w_bb_ah_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05BS_frontier_vote_w_bb_ah_0001\experiment_bundle.json`
- experiment_id: `exp_05bs_frontier_vote_w_bb_ah_v1`
- bundle_status: `completed`
- latest_attempt: `att_0001`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-30T11:52:15.676133+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: max_probability_margin(min_margin=0.07) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=3)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `70.768` |
| `profit_factor` | `1.306485002295346` |
| `trade_count` | `488` |
| `win_rate` | `0.5368852459016393` |
| `expectancy_per_trade` | `0.7250819672131147` |
| `max_dd_pct` | `13.02870090634441` |
| `recovery_factor` | `2.7719545632589115` |
| `net_profit` | `353.84` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `13.02870090634441` |
| `equity_dd_amount` | `127.64999999999998` |
| `max_dd_pct` | `12.590347877720676` |
| `max_dd_amount` | `122.98000000000002` |
| `ulcer_index` | `7.878868355175794` |
| `worst_day` | `-30.5` |
| `worst_week` | `-37.67999999999999` |
| `min_free_margin` | `472.48` |
| `consecutive_losses` | `10` |
| `time_under_water` | `22913100.0` |
| `longest_recovery_duration` | `13839900.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `3.0` |
| `payoff_ratio` | `1.1269679790791916` |
| `avg_win` | `5.757061068702289` |
| `avg_loss` | `-5.108451327433628` |
| `long_count` | `202` |
| `short_count` | `286` |
| `long_expectancy` | `1.5724257425742574` |
| `short_expectancy` | `0.1266083916083916` |
| `mfe_mean` | `5.993872950819672` |
| `mfe_median` | `4.285` |
| `mfe_p90` | `13.590000000000002` |
| `mae_mean` | `4.9495696721311475` |
| `mae_median` | `3.46` |
| `mae_p90` | `9.954` |
| `no_trade_rate` | `0.8987750935692412` |
| `hold_distribution` | `{'p50': 3.0, 'p90': 3.0}` |
| `loss_trade_mfe` | `3.134336283185841` |
| `realized_over_mfe` | `-2.879962182384818` |
| `rule_pass_rates` | `{'long_signal_rate': 0.04363729159578088, 'short_signal_rate': 0.05758761483497788}` |
| `win_trade_mae` | `2.759618320610687` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0001 | completed | 2026-03-30 11:52:15 UTC | 70.77   | 488    | 11756 | 11756         | 0       
```

### 95. `05_optimization` / `05CB_trend_proxy_persistence_leader_drag_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05CB_trend_proxy_persistence_leader_drag_0001\experiment_bundle.json`
- experiment_id: `exp_05cb_trend_proxy_persistence_leader_drag_v1`
- bundle_status: `completed`
- latest_attempt: `att_0001`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-30T13:00:54.007588+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: max_probability_margin(min_margin=0.07) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=3)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `69.21199999999999` |
| `profit_factor` | `1.2933880443905623` |
| `trade_count` | `489` |
| `win_rate` | `0.5419222903885481` |
| `expectancy_per_trade` | `0.7076891615541923` |
| `max_dd_pct` | `12.110849302500153` |
| `recovery_factor` | `2.9791666666666674` |
| `net_profit` | `346.06` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `12.110849302500153` |
| `equity_dd_amount` | `116.15999999999997` |
| `max_dd_pct` | `11.824380856760369` |
| `max_dd_amount` | `113.05999999999995` |
| `ulcer_index` | `7.274473275040702` |
| `worst_day` | `-30.5` |
| `worst_week` | `-37.67999999999999` |
| `min_free_margin` | `472.48` |
| `consecutive_losses` | `7` |
| `time_under_water` | `22851300.0` |
| `longest_recovery_duration` | `13839900.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `3.0` |
| `payoff_ratio` | `1.0932789507301357` |
| `avg_win` | `5.756943396226415` |
| `avg_loss` | `-5.265758928571429` |
| `long_count` | `203` |
| `short_count` | `286` |
| `long_expectancy` | `1.4993103448275862` |
| `short_expectancy` | `0.14580419580419582` |
| `mfe_mean` | `5.961145194274029` |
| `mfe_median` | `4.28` |
| `mfe_p90` | `13.263999999999996` |
| `mae_mean` | `5.021779141104295` |
| `mae_median` | `3.41` |
| `mae_p90` | `10.229999999999997` |
| `no_trade_rate` | `0.8987750935692412` |
| `hold_distribution` | `{'p50': 3.0, 'p90': 3.0}` |
| `loss_trade_mfe` | `3.0605803571428574` |
| `realized_over_mfe` | `-3.139121275557018` |
| `rule_pass_rates` | `{'long_signal_rate': 0.043297039809459, 'short_signal_rate': 0.05792786662129976}` |
| `win_trade_mae` | `2.7620377358490567` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0001 | completed | 2026-03-30 13:00:54 UTC | 69.21   | 489    | 11756 | 11756         | 0       
```

### 96. `05_optimization` / `05AZ_05aj_combo_loose_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05AZ_05aj_combo_loose_0001\experiment_bundle.json`
- experiment_id: `exp_05az_05aj_combo_loose_v1`
- bundle_status: `completed`
- latest_attempt: `att_0001`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-30T10:47:22.170272+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: combo_probability_gate(min_margin=0.05, min_probability_diff=0.07) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=3)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `69.174` |
| `profit_factor` | `1.2905152283837587` |
| `trade_count` | `498` |
| `win_rate` | `0.5381526104417671` |
| `expectancy_per_trade` | `0.6945180722891566` |
| `max_dd_pct` | `13.31429627955708` |
| `recovery_factor` | `2.6683382194105847` |
| `net_profit` | `345.87` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `13.31429627955708` |
| `equity_dd_amount` | `129.62` |
| `max_dd_pct` | `12.847222222222218` |
| `max_dd_amount` | `124.68999999999994` |
| `ulcer_index` | `7.629815728587887` |
| `worst_day` | `-23.57` |
| `worst_week` | `-37.67999999999999` |
| `min_free_margin` | `472.48` |
| `consecutive_losses` | `10` |
| `time_under_water` | `22860900.0` |
| `longest_recovery_duration` | `13839900.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `3.0` |
| `payoff_ratio` | `1.1075317258517332` |
| `avg_win` | `5.732873134328359` |
| `avg_loss` | `-5.176260869565217` |
| `long_count` | `205` |
| `short_count` | `293` |
| `long_expectancy` | `1.5395121951219513` |
| `short_expectancy` | `0.10331058020477815` |
| `mfe_mean` | `5.978895582329317` |
| `mfe_median` | `4.33` |
| `mfe_p90` | `13.590000000000002` |
| `mae_mean` | `4.939939759036145` |
| `mae_median` | `3.45` |
| `mae_p90` | `9.954` |
| `no_trade_rate` | `0.8971588975842123` |
| `hold_distribution` | `{'p50': 3.0, 'p90': 3.0}` |
| `loss_trade_mfe` | `3.107` |
| `realized_over_mfe` | `-3.0971937230743665` |
| `rule_pass_rates` | `{'long_signal_rate': 0.044147669275263694, 'short_signal_rate': 0.058693433140523985}` |
| `win_trade_mae` | `2.7225373134328357` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0001 | completed | 2026-03-30 10:47:22 UTC | 69.17   | 498    | 11756 | 11756         | 0       
```

### 97. `05_optimization` / `05EU_05dp_near_short_only_hold5_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05EU_05dp_near_short_only_hold5_0001\experiment_bundle.json`
- experiment_id: `exp_05eu_05dp_near_short_only_hold5_v1`
- bundle_status: `completed`
- latest_attempt: `att_0001`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-30T15:49:25.472793+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3, long_threshold=0.6) | filters: max_probability_margin(min_margin=0.0675) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=5)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `68.948` |
| `profit_factor` | `1.459898612593383` |
| `trade_count` | `255` |
| `win_rate` | `0.5019607843137255` |
| `expectancy_per_trade` | `1.351921568627451` |
| `max_dd_pct` | `13.678924948037787` |
| `recovery_factor` | `2.593199939822475` |
| `net_profit` | `344.74` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `13.678924948037787` |
| `equity_dd_amount` | `132.94000000000005` |
| `max_dd_pct` | `12.435530085959888` |
| `max_dd_amount` | `119.35000000000002` |
| `ulcer_index` | `7.948148728671653` |
| `worst_day` | `-28.209999999999997` |
| `worst_week` | `-40.989999999999995` |
| `min_free_margin` | `455.62` |
| `consecutive_losses` | `7` |
| `time_under_water` | `22817100.0` |
| `longest_recovery_duration` | `14962800.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `5.0` |
| `payoff_ratio` | `1.448493154682497` |
| `avg_win` | `8.54953125` |
| `avg_loss` | `-5.90236220472441` |
| `long_count` | `19` |
| `short_count` | `236` |
| `long_expectancy` | `8.90421052631579` |
| `short_expectancy` | `0.7438983050847457` |
| `mfe_mean` | `8.130745098039217` |
| `mfe_median` | `5.69` |
| `mfe_p90` | `17.253999999999998` |
| `mae_mean` | `6.603607843137255` |
| `mae_median` | `4.96` |
| `mae_p90` | `12.709999999999997` |
| `no_trade_rate` | `0.9339911534535557` |
| `hold_distribution` | `{'p50': 5.0, 'p90': 5.0}` |
| `loss_trade_mfe` | `3.7530708661417322` |
| `realized_over_mfe` | `-4.804337425367065` |
| `rule_pass_rates` | `{'long_signal_rate': 0.005273902687989112, 'short_signal_rate': 0.06073494385845526}` |
| `win_trade_mae` | `3.656328125` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0001 | completed | 2026-03-30 15:49:25 UTC | 68.95   | 255    | 11756 | 11756         | 0       
```

### 98. `05_optimization` / `05D_mt5_validation_diff_tightgap_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05D_mt5_validation_diff_tightgap_0001\experiment_bundle.json`
- experiment_id: `exp_stage05_diff_tightgap_validation_0001`
- bundle_status: `completed`
- latest_attempt: `att_0002`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-29T10:54:38.650791+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: probability_difference(min_probability_diff=0.0775) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=3)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `68.662` |
| `profit_factor` | `1.30112534975309` |
| `trade_count` | `487` |
| `win_rate` | `0.5318275154004107` |
| `expectancy_per_trade` | `0.7049486652977413` |
| `max_dd_pct` | `12.774646356423034` |
| `recovery_factor` | `4.172967059681537` |
| `net_profit` | `343.31` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `12.774646356423034` |
| `equity_dd_amount` | `82.26999999999998` |
| `max_dd_pct` | `10.618862087583357` |
| `max_dd_amount` | `72.76999999999998` |
| `ulcer_index` | `2.469317461372238` |
| `worst_day` | `-20.78` |
| `worst_week` | `-30.83` |
| `min_free_margin` | `466.37` |
| `consecutive_losses` | `12` |
| `time_under_water` | `22164900.0` |
| `longest_recovery_duration` | `3977400.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `3.0` |
| `payoff_ratio` | `1.1453921997826428` |
| `avg_win` | `5.7274131274131275` |
| `avg_loss` | `-5.000394736842105` |
| `long_count` | `224` |
| `short_count` | `263` |
| `long_expectancy` | `0.7312946428571429` |
| `short_expectancy` | `0.6825095057034221` |
| `mfe_mean` | `5.787720739219712` |
| `mfe_median` | `4.16` |
| `mfe_p90` | `12.984000000000005` |
| `mae_mean` | `4.749466119096509` |
| `mae_median` | `3.22` |
| `mae_p90` | `10.562000000000001` |
| `no_trade_rate` | `0.905239877509357` |
| `hold_distribution` | `{'p50': 3.0, 'p90': 3.0}` |
| `loss_trade_mfe` | `2.8174122807017543` |
| `realized_over_mfe` | `-3.5094407209301215` |
| `rule_pass_rates` | `{'long_signal_rate': 0.04457298400816604, 'short_signal_rate': 0.05018713848247703}` |
| `win_trade_mae` | `2.465791505791506` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0002 | completed | 2026-03-29 10:54:38 UTC | 1.81    | 351    | 6755  | 6720          | 35      
att_0001 | completed | 2026-03-29 10:51:39 UTC | 68.66   | 487    | 11756 | 11756         | 0       
```

### 99. `05_optimization` / `05BI_05w_short_bias_margin_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05BI_05w_short_bias_margin_0001\experiment_bundle.json`
- experiment_id: `exp_05bi_05w_short_bias_margin_v1`
- bundle_status: `completed`
- latest_attempt: `att_0001`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-30T11:29:29.548684+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3, long_threshold=0.45) | filters: max_probability_margin(min_margin=0.07) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=3)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `68.414` |
| `profit_factor` | `1.3139437770170432` |
| `trade_count` | `446` |
| `win_rate` | `0.515695067264574` |
| `expectancy_per_trade` | `0.7669730941704036` |
| `max_dd_pct` | `14.344542183534307` |
| `recovery_factor` | `2.4306828679030765` |
| `net_profit` | `342.07` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `14.344542183534307` |
| `equity_dd_amount` | `140.73000000000002` |
| `max_dd_pct` | `13.686077143062144` |
| `max_dd_amount` | `133.51999999999998` |
| `ulcer_index` | `8.77461640113589` |
| `worst_day` | `-32.36` |
| `worst_week` | `-39.38999999999999` |
| `min_free_margin` | `470.23` |
| `consecutive_losses` | `10` |
| `time_under_water` | `22776600.0` |
| `longest_recovery_duration` | `13839900.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `3.0` |
| `payoff_ratio` | `1.2339645905899188` |
| `avg_win` | `6.224608695652174` |
| `avg_loss` | `-5.044398148148148` |
| `long_count` | `160` |
| `short_count` | `286` |
| `long_expectancy` | `2.1174375000000003` |
| `short_expectancy` | `0.011468531468531473` |
| `mfe_mean` | `6.08` |
| `mfe_median` | `4.415` |
| `mfe_p90` | `13.425` |
| `mae_mean` | `5.343295964125561` |
| `mae_median` | `3.9050000000000002` |
| `mae_p90` | `10.615` |
| `no_trade_rate` | `0.9085573324259952` |
| `hold_distribution` | `{'p50': 3.0, 'p90': 3.0}` |
| `loss_trade_mfe` | `2.943611111111111` |
| `realized_over_mfe` | `-3.3126103261407085` |
| `rule_pass_rates` | `{'long_signal_rate': 0.03402517863218782, 'short_signal_rate': 0.057417488941816947}` |
| `win_trade_mae` | `2.97` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0001 | completed | 2026-03-30 11:29:29 UTC | 68.41   | 446    | 11756 | 11756         | 0       
```

### 100. `05_optimization` / `05AC_drop_adx14_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05AC_drop_adx14_0001\experiment_bundle.json`
- experiment_id: `exp_05ac_adx_14_feature_ablation_v1`
- bundle_status: `completed`
- latest_attempt: `att_0001`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-29T17:16:18.974367+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: max_probability_margin(min_margin=0.07) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=3)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `68.006` |
| `profit_factor` | `1.2725145261470647` |
| `trade_count` | `532` |
| `win_rate` | `0.5263157894736842` |
| `expectancy_per_trade` | `0.6391541353383459` |
| `max_dd_pct` | `11.945694787280397` |
| `recovery_factor` | `4.021643997634532` |
| `net_profit` | `340.03` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `11.945694787280397` |
| `equity_dd_amount` | `84.55000000000007` |
| `max_dd_pct` | `11.566070303295989` |
| `max_dd_amount` | `84.43000000000006` |
| `ulcer_index` | `3.6810145820433036` |
| `worst_day` | `-23.520000000000003` |
| `worst_week` | `-32.9` |
| `min_free_margin` | `470.69` |
| `consecutive_losses` | `7` |
| `time_under_water` | `22198500.0` |
| `longest_recovery_duration` | `13236300.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `3.0` |
| `payoff_ratio` | `1.1452630735323581` |
| `avg_win` | `5.670642857142857` |
| `avg_loss` | `-4.951388888888889` |
| `long_count` | `249` |
| `short_count` | `283` |
| `long_expectancy` | `0.4683132530120482` |
| `short_expectancy` | `0.789469964664311` |
| `mfe_mean` | `5.697218045112782` |
| `mfe_median` | `3.9050000000000002` |
| `mfe_p90` | `12.911000000000003` |
| `mae_mean` | `4.945394736842105` |
| `mae_median` | `3.475` |
| `mae_p90` | `10.809000000000001` |
| `no_trade_rate` | `0.892565498468867` |
| `hold_distribution` | `{'p50': 3.0, 'p90': 3.0}` |
| `loss_trade_mfe` | `2.745952380952381` |
| `realized_over_mfe` | `-3.7565276471938103` |
| `rule_pass_rates` | `{'long_signal_rate': 0.05052739026879891, 'short_signal_rate': 0.05690711126233413}` |
| `win_trade_mae` | `2.633035714285714` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0001 | completed | 2026-03-29 17:16:18 UTC | 68.01   | 532    | 11756 | 11756         | 0       
```

### 101. `03_max_probability_margin` / `03E_mt5_validation_baseline_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\03_max_probability_margin\02_runs\active\03E_mt5_validation_baseline_0001\experiment_bundle.json`
- experiment_id: `exp_stage03_margin_validation_0001`
- bundle_status: `completed`
- latest_attempt: `att_0005`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-29T10:56:34.784273+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: max_probability_margin(min_margin=0.07) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=3)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `67.664` |
| `profit_factor` | `1.2655010319633986` |
| `trade_count` | `530` |
| `win_rate` | `0.5264150943396226` |
| `expectancy_per_trade` | `0.6383396226415095` |
| `max_dd_pct` | `12.201705598813493` |
| `recovery_factor` | `4.112313115351891` |
| `net_profit` | `338.32` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `12.201705598813493` |
| `equity_dd_amount` | `82.26999999999998` |
| `max_dd_pct` | `9.01709222534345` |
| `max_dd_amount` | `66.55999999999995` |
| `ulcer_index` | `3.556990606308009` |
| `worst_day` | `-22.61` |
| `worst_week` | `-28.810000000000002` |
| `min_free_margin` | `461.19` |
| `consecutive_losses` | `6` |
| `time_under_water` | `22404900.0` |
| `longest_recovery_duration` | `13237500.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `3.0` |
| `payoff_ratio` | `1.1384973441677886` |
| `avg_win` | `5.779892473118279` |
| `avg_loss` | `-5.076772908366534` |
| `long_count` | `242` |
| `short_count` | `288` |
| `long_expectancy` | `0.40342975206611575` |
| `short_expectancy` | `0.8357291666666666` |
| `mfe_mean` | `5.767566037735849` |
| `mfe_median` | `4.08` |
| `mfe_p90` | `12.936000000000003` |
| `mae_mean` | `4.935283018867924` |
| `mae_median` | `3.46` |
| `mae_p90` | `10.665000000000003` |
| `no_trade_rate` | `0.8934161279346716` |
| `hold_distribution` | `{'p50': 3.0, 'p90': 3.0}` |
| `loss_trade_mfe` | `2.8058964143426293` |
| `realized_over_mfe` | `-3.669763322988739` |
| `rule_pass_rates` | `{'long_signal_rate': 0.04925144607009187, 'short_signal_rate': 0.057332425995236476}` |
| `win_trade_mae` | `2.5720071684587813` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0005 | completed | 2026-03-29 10:56:34 UTC | 7.07    | 357    | 6755  | 6720          | 35      
att_0004 | failed    | 2026-03-29 10:53:38 UTC | -       | -      | -     | -             | -       
att_0003 | completed | 2026-03-29 06:12:48 UTC | 67.66   | 530    | 11756 | 11756         | 0       
att_0002 | completed | 2026-03-29 06:04:01 UTC | 67.66   | 530    | 11756 | 11756         | 0       
att_0001 | completed | 2026-03-28 19:04:09 UTC | 68.06   | 529    | 11696 | -             | -       
```

### 102. `05_optimization` / `05H_mt5_validation_diff_07000_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05H_mt5_validation_diff_07000_0001\experiment_bundle.json`
- experiment_id: `exp_stage05_diff_frontier_07000_validation_0001`
- bundle_status: `completed`
- latest_attempt: `att_0001`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-29T14:18:56.268790+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: probability_difference(min_probability_diff=0.07) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=3)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `67.616` |
| `profit_factor` | `1.2507472428038477` |
| `trade_count` | `588` |
| `win_rate` | `0.5170068027210885` |
| `expectancy_per_trade` | `0.5749659863945578` |
| `max_dd_pct` | `12.535807886877551` |
| `recovery_factor` | `4.109395891576517` |
| `net_profit` | `338.08` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `12.535807886877551` |
| `equity_dd_amount` | `82.26999999999998` |
| `max_dd_pct` | `9.249383565571419` |
| `max_dd_amount` | `71.80999999999995` |
| `ulcer_index` | `3.6162909573374873` |
| `worst_day` | `-24.259999999999998` |
| `worst_week` | `-33.519999999999996` |
| `min_free_margin` | `460.66` |
| `consecutive_losses` | `8` |
| `time_under_water` | `22405200.0` |
| `longest_recovery_duration` | `7077000.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `3.0` |
| `payoff_ratio` | `1.1684612399878052` |
| `avg_win` | `5.547269736842105` |
| `avg_loss` | `-4.7475` |
| `long_count` | `273` |
| `short_count` | `315` |
| `long_expectancy` | `0.37223443223443226` |
| `short_expectancy` | `0.7506666666666666` |
| `mfe_mean` | `5.433367346938776` |
| `mfe_median` | `3.715` |
| `mfe_p90` | `12.263000000000002` |
| `mae_mean` | `4.685952380952381` |
| `mae_median` | `3.175` |
| `mae_p90` | `10.040000000000006` |
| `no_trade_rate` | `0.8829533855052739` |
| `hold_distribution` | `{'p50': 3.0, 'p90': 3.0}` |
| `loss_trade_mfe` | `2.6053169014084507` |
| `realized_over_mfe` | `-3.859945309661509` |
| `rule_pass_rates` | `{'long_signal_rate': 0.05520585233072474, 'short_signal_rate': 0.06184076216400136}` |
| `win_trade_mae` | `2.441447368421053` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0001 | completed | 2026-03-29 14:18:56 UTC | 67.62   | 588    | 11756 | 11756         | 0       
```

### 103. `05_optimization` / `05P_margin_diff_mix_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05P_margin_diff_mix_0001\experiment_bundle.json`
- experiment_id: `exp_05P_margin_diff_mix_v1`
- bundle_status: `completed`
- latest_attempt: `att_0002`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-29T16:07:03.229119+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: combo_probability_gate(min_margin=0.07, min_probability_diff=0.0775) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=3)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `67.402` |
| `profit_factor` | `1.308174145230758` |
| `trade_count` | `451` |
| `win_rate` | `0.541019955654102` |
| `expectancy_per_trade` | `0.747250554323725` |
| `max_dd_pct` | `12.550724637681157` |
| `recovery_factor` | `4.096389935577975` |
| `net_profit` | `337.01` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `12.550724637681157` |
| `equity_dd_amount` | `82.26999999999998` |
| `max_dd_pct` | `10.443755561296246` |
| `max_dd_amount` | `72.76999999999998` |
| `ulcer_index` | `2.3919393195387273` |
| `worst_day` | `-19.46` |
| `worst_week` | `-26.119999999999994` |
| `min_free_margin` | `470.13` |
| `consecutive_losses` | `9` |
| `time_under_water` | `21651000.0` |
| `longest_recovery_duration` | `5007000.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `3.0` |
| `payoff_ratio` | `1.1098034756670774` |
| `avg_win` | `5.863032786885245` |
| `avg_loss` | `-5.282946859903381` |
| `long_count` | `204` |
| `short_count` | `247` |
| `long_expectancy` | `0.7218627450980392` |
| `short_expectancy` | `0.7682186234817814` |
| `mfe_mean` | `6.046186252771618` |
| `mfe_median` | `4.32` |
| `mfe_p90` | `13.43` |
| `mae_mean` | `4.934279379157428` |
| `mae_median` | `3.47` |
| `mae_p90` | `10.8` |
| `no_trade_rate` | `0.9115345355563117` |
| `hold_distribution` | `{'p50': 3.0, 'p90': 3.0}` |
| `loss_trade_mfe` | `2.9818357487922706` |
| `realized_over_mfe` | `-3.187359200891721` |
| `rule_pass_rates` | `{'long_signal_rate': 0.040915277305205854, 'short_signal_rate': 0.047550187138482476}` |
| `win_trade_mae` | `2.568934426229508` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0002 | completed | 2026-03-29 16:07:03 UTC | 1.69    | 309    | 6755  | 6720          | 35      
att_0001 | completed | 2026-03-29 16:04:12 UTC | 67.40   | 451    | 11756 | 11756         | 0       
```

### 104. `05_optimization` / `05AY_05aj_diff_only_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05AY_05aj_diff_only_0001\experiment_bundle.json`
- experiment_id: `exp_05ay_05aj_diff_only_v1`
- bundle_status: `completed`
- latest_attempt: `att_0001`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-30T10:45:44.874911+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: probability_difference(min_probability_diff=0.0775) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=3)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `67.05399999999999` |
| `profit_factor` | `1.3160837182992364` |
| `trade_count` | `462` |
| `win_rate` | `0.5324675324675324` |
| `expectancy_per_trade` | `0.7256926406926406` |
| `max_dd_pct` | `12.468938097078802` |
| `recovery_factor` | `3.327741935483871` |
| `net_profit` | `335.27` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `12.468938097078802` |
| `equity_dd_amount` | `100.75` |
| `max_dd_pct` | `12.058460802179393` |
| `max_dd_amount` | `99.01999999999998` |
| `ulcer_index` | `6.508746059822758` |
| `worst_day` | `-24.010000000000005` |
| `worst_week` | `-46.709999999999994` |
| `min_free_margin` | `464.73` |
| `consecutive_losses` | `7` |
| `time_under_water` | `22678500.0` |
| `longest_recovery_duration` | `13155600.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `3.0` |
| `payoff_ratio` | `1.1555857038725001` |
| `avg_win` | `5.674674796747968` |
| `avg_loss` | `-4.910648148148148` |
| `long_count` | `200` |
| `short_count` | `262` |
| `long_expectancy` | `1.6748500000000002` |
| `short_expectancy` | `0.0011450381679389218` |
| `mfe_mean` | `5.794632034632034` |
| `mfe_median` | `4.195` |
| `mfe_p90` | `12.853000000000009` |
| `mae_mean` | `5.068160173160173` |
| `mae_median` | `3.37` |
| `mae_p90` | `10.510000000000014` |
| `no_trade_rate` | `0.9082170806396733` |
| `hold_distribution` | `{'p50': 3.0, 'p90': 3.0}` |
| `loss_trade_mfe` | `2.9003703703703705` |
| `realized_over_mfe` | `-3.2514047859530986` |
| `rule_pass_rates` | `{'long_signal_rate': 0.03989452194624022, 'short_signal_rate': 0.05188839741408642}` |
| `win_trade_mae` | `2.793943089430894` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0001 | completed | 2026-03-30 10:45:44 UTC | 67.05   | 462    | 11756 | 11756         | 0       
```

### 105. `05_optimization` / `05AE_drop_supertrend103_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05AE_drop_supertrend103_0001\experiment_bundle.json`
- experiment_id: `exp_05ae_supertrend_10_3_feature_ablation_v1`
- bundle_status: `completed`
- latest_attempt: `att_0001`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-29T17:19:05.918604+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: max_probability_margin(min_margin=0.07) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=3)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `65.958` |
| `profit_factor` | `1.282593979486037` |
| `trade_count` | `523` |
| `win_rate` | `0.5468451242829828` |
| `expectancy_per_trade` | `0.6305736137667305` |
| `max_dd_pct` | `12.584513721051179` |
| `recovery_factor` | `4.008630120335482` |
| `net_profit` | `329.79` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `12.584513721051179` |
| `equity_dd_amount` | `82.26999999999998` |
| `max_dd_pct` | `9.248883226133277` |
| `max_dd_amount` | `66.82000000000005` |
| `ulcer_index` | `4.248439809593877` |
| `worst_day` | `-26.35` |
| `worst_week` | `-39.22` |
| `min_free_margin` | `470.63` |
| `consecutive_losses` | `6` |
| `time_under_water` | `22691100.0` |
| `longest_recovery_duration` | `13237500.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `3.0` |
| `payoff_ratio` | `1.0628488571265409` |
| `avg_win` | `5.233566433566433` |
| `avg_loss` | `-4.92409282700422` |
| `long_count` | `244` |
| `short_count` | `279` |
| `long_expectancy` | `0.7280327868852459` |
| `short_expectancy` | `0.5453405017921147` |
| `mfe_mean` | `5.707667304015296` |
| `mfe_median` | `4.07` |
| `mfe_p90` | `12.542000000000003` |
| `mae_mean` | `4.737495219885277` |
| `mae_median` | `3.3` |
| `mae_p90` | `9.926` |
| `no_trade_rate` | `0.8955427015991834` |
| `hold_distribution` | `{'p50': 3.0, 'p90': 3.0}` |
| `loss_trade_mfe` | `3.1484388185654004` |
| `realized_over_mfe` | `-3.0361767472223096` |
| `rule_pass_rates` | `{'long_signal_rate': 0.04967676080299421, 'short_signal_rate': 0.054780537597822386}` |
| `win_trade_mae` | `2.6254895104895106` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0001 | completed | 2026-03-29 17:19:05 UTC | 65.96   | 523    | 11756 | 11756         | 0       
```

### 106. `05_optimization` / `05BE_trend_proxy_breadth_only_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05BE_trend_proxy_breadth_only_0001\experiment_bundle.json`
- experiment_id: `exp_05be_trend_proxy_breadth_only_v1`
- bundle_status: `completed`
- latest_attempt: `att_0001`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-30T11:18:52.113437+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: max_probability_margin(min_margin=0.07) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=3)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `65.23400000000001` |
| `profit_factor` | `1.2759195343958314` |
| `trade_count` | `490` |
| `win_rate` | `0.5346938775510204` |
| `expectancy_per_trade` | `0.6656530612244899` |
| `max_dd_pct` | `13.530382154227652` |
| `recovery_factor` | `2.532965752892755` |
| `net_profit` | `326.17` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `13.530382154227652` |
| `equity_dd_amount` | `128.76999999999998` |
| `max_dd_pct` | `13.44774644036428` |
| `max_dd_amount` | `127.88000000000011` |
| `ulcer_index` | `8.146940951629167` |
| `worst_day` | `-30.5` |
| `worst_week` | `-37.67999999999999` |
| `min_free_margin` | `472.48` |
| `consecutive_losses` | `7` |
| `time_under_water` | `22914300.0` |
| `longest_recovery_duration` | `13840800.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `3.0` |
| `payoff_ratio` | `1.1103421902375936` |
| `avg_win` | `5.756832061068702` |
| `avg_loss` | `-5.184736842105263` |
| `long_count` | `203` |
| `short_count` | `287` |
| `long_expectancy` | `1.424334975369458` |
| `short_expectancy` | `0.12902439024390244` |
| `mfe_mean` | `5.935877551020408` |
| `mfe_median` | `4.215` |
| `mfe_p90` | `13.091000000000001` |
| `mae_mean` | `5.02634693877551` |
| `mae_median` | `3.43` |
| `mae_p90` | `10.190000000000008` |
| `no_trade_rate` | `0.8991153453555631` |
| `hold_distribution` | `{'p50': 3.0, 'p90': 3.0}` |
| `loss_trade_mfe` | `3.0439473684210525` |
| `realized_over_mfe` | `-2.8736472686089445` |
| `rule_pass_rates` | `{'long_signal_rate': 0.04287172507655665, 'short_signal_rate': 0.058012929567880234}` |
| `win_trade_mae` | `2.750916030534351` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0001 | completed | 2026-03-30 11:18:52 UTC | 65.23   | 490    | 11756 | 11756         | 0       
```

### 107. `05_optimization` / `05FE_05ca_cls_scale_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05FE_05ca_cls_scale_0001\experiment_bundle.json`
- experiment_id: `exp_05fe_05ca_cls_scale_v1`
- bundle_status: `completed`
- latest_attempt: `att_0001`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-30T16:23:24.448362+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: max_probability_margin(min_margin=0.0675) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=5)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `65.192` |
| `profit_factor` | `1.2421531992660224` |
| `trade_count` | `440` |
| `win_rate` | `0.5204545454545455` |
| `expectancy_per_trade` | `0.7408181818181818` |
| `max_dd_pct` | `16.642925286530144` |
| `recovery_factor` | `2.559560266980761` |
| `net_profit` | `325.96` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `16.642925286530144` |
| `equity_dd_amount` | `127.35000000000002` |
| `max_dd_pct` | `13.022966839716519` |
| `max_dd_amount` | `123.66999999999996` |
| `ulcer_index` | `7.314183308224225` |
| `worst_day` | `-72.86000000000001` |
| `worst_week` | `-36.650000000000006` |
| `min_free_margin` | `436.59` |
| `consecutive_losses` | `7` |
| `time_under_water` | `22741500.0` |
| `longest_recovery_duration` | `13243800.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `5.0` |
| `payoff_ratio` | `1.144516703253846` |
| `avg_win` | `7.301528384279476` |
| `avg_loss` | `-6.3795734597156395` |
| `long_count` | `92` |
| `short_count` | `348` |
| `long_expectancy` | `1.3131521739130434` |
| `short_expectancy` | `0.5895114942528735` |
| `mfe_mean` | `7.336681818181818` |
| `mfe_median` | `5.68` |
| `mfe_p90` | `15.260000000000009` |
| `mae_mean` | `6.3025` |
| `mae_median` | `4.484999999999999` |
| `mae_p90` | `12.482000000000001` |
| `no_trade_rate` | `0.8739367131677441` |
| `hold_distribution` | `{'p50': 5.0, 'p90': 5.0}` |
| `loss_trade_mfe` | `3.8366350710900474` |
| `realized_over_mfe` | `-2.69402347557713` |
| `rule_pass_rates` | `{'long_signal_rate': 0.01939435182034706, 'short_signal_rate': 0.10666893501190881}` |
| `win_trade_mae` | `3.1412663755458516` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0001 | completed | 2026-03-30 16:23:24 UTC | 65.19   | 440    | 11756 | 11756         | 0       
```

### 108. `05_optimization` / `05F_mt5_validation_margin_07250_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05F_mt5_validation_margin_07250_0001\experiment_bundle.json`
- experiment_id: `exp_stage05_margin_frontier_07250_validation_0001`
- bundle_status: `completed`
- latest_attempt: `att_0001`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-29T14:16:12.589464+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: max_probability_margin(min_margin=0.0725) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=3)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `64.838` |
| `profit_factor` | `1.2651926018634405` |
| `trade_count` | `502` |
| `win_rate` | `0.5258964143426295` |
| `expectancy_per_trade` | `0.645796812749004` |
| `max_dd_pct` | `12.542496912780326` |
| `recovery_factor` | `3.9405615655767603` |
| `net_profit` | `324.19` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `12.542496912780326` |
| `equity_dd_amount` | `82.26999999999998` |
| `max_dd_pct` | `9.979776537915411` |
| `max_dd_amount` | `69.58000000000004` |
| `ulcer_index` | `2.976618468968846` |
| `worst_day` | `-22.61` |
| `worst_week` | `-32.9` |
| `min_free_margin` | `466.93` |
| `consecutive_losses` | `6` |
| `time_under_water` | `22620300.0` |
| `longest_recovery_duration` | `9679200.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `3.0` |
| `payoff_ratio` | `1.1405903001647684` |
| `avg_win` | `5.858560606060607` |
| `avg_loss` | `-5.136428571428572` |
| `long_count` | `231` |
| `short_count` | `271` |
| `long_expectancy` | `0.4332900432900433` |
| `short_expectancy` | `0.8269372693726937` |
| `mfe_mean` | `5.82496015936255` |
| `mfe_median` | `4.145` |
| `mfe_p90` | `12.88900000000001` |
| `mae_mean` | `4.9473107569721115` |
| `mae_median` | `3.33` |
| `mae_p90` | `10.809000000000001` |
| `no_trade_rate` | `0.8998809118747874` |
| `hold_distribution` | `{'p50': 3.0, 'p90': 3.0}` |
| `loss_trade_mfe` | `2.8382773109243695` |
| `realized_over_mfe` | `-3.4050539099890873` |
| `rule_pass_rates` | `{'long_signal_rate': 0.04627424293977543, 'short_signal_rate': 0.05384484518543722}` |
| `win_trade_mae` | `2.549015151515152` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0001 | completed | 2026-03-29 14:16:12 UTC | 64.84   | 502    | 11756 | 11756         | 0       
```

### 109. `05_optimization` / `05FD_05ca_flatup_longdown_margin0675_hold5_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05FD_05ca_flatup_longdown_margin0675_hold5_0001\experiment_bundle.json`
- experiment_id: `exp_05fd_05ca_flatup_longdown_margin0675_hold5_v1`
- bundle_status: `completed`
- latest_attempt: `att_0002`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-30T16:21:45.109921+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: max_probability_margin(min_margin=0.0675) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=5)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `64.77000000000001` |
| `profit_factor` | `1.221579829632924` |
| `trade_count` | `511` |
| `win_rate` | `0.5146771037181996` |
| `expectancy_per_trade` | `0.6337573385518591` |
| `max_dd_pct` | `22.942765905183006` |
| `recovery_factor` | `1.3335941360566628` |
| `net_profit` | `323.85` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `22.942765905183006` |
| `equity_dd_amount` | `242.84000000000003` |
| `max_dd_pct` | `22.72452430890162` |
| `max_dd_amount` | `240.5300000000001` |
| `ulcer_index` | `12.980152738505323` |
| `worst_day` | `-31.13` |
| `worst_week` | `-45.190000000000005` |
| `min_free_margin` | `464.16` |
| `consecutive_losses` | `7` |
| `time_under_water` | `23130600.0` |
| `longest_recovery_duration` | `13243800.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `5.0` |
| `payoff_ratio` | `1.1519079762318067` |
| `avg_win` | `6.788593155893537` |
| `avg_loss` | `-5.893346774193549` |
| `long_count` | `63` |
| `short_count` | `448` |
| `long_expectancy` | `3.41031746031746` |
| `short_expectancy` | `0.24330357142857142` |
| `mfe_mean` | `6.892622309197652` |
| `mfe_median` | `5.12` |
| `mfe_p90` | `14.54` |
| `mae_mean` | `6.221702544031311` |
| `mae_median` | `4.65` |
| `mae_p90` | `12.5` |
| `no_trade_rate` | `0.8515651582170807` |
| `hold_distribution` | `{'p50': 5.0, 'p90': 5.0}` |
| `loss_trade_mfe` | `3.380040322580645` |
| `realized_over_mfe` | `-3.7541010039329437` |
| `rule_pass_rates` | `{'long_signal_rate': 0.01522626743790405, 'short_signal_rate': 0.13320857434501532}` |
| `win_trade_mae` | `3.5120912547528516` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0002 | completed | 2026-03-30 16:21:45 UTC | 64.77   | 511    | 11756 | 11756         | 0       
att_0001 | completed | 2026-03-30 16:11:19 UTC | 64.77   | 511    | 11756 | 11756         | 0       
```

### 110. `05_optimization` / `05G_mt5_validation_diff_07250_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05G_mt5_validation_diff_07250_0001\experiment_bundle.json`
- experiment_id: `exp_stage05_diff_frontier_07250_validation_0001`
- bundle_status: `completed`
- latest_attempt: `att_0001`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-29T14:17:34.048388+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: probability_difference(min_probability_diff=0.0725) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=3)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `63.624` |
| `profit_factor` | `1.2451735219994915` |
| `trade_count` | `557` |
| `win_rate` | `0.5098743267504489` |
| `expectancy_per_trade` | `0.5711310592459605` |
| `max_dd_pct` | `12.993966579271564` |
| `recovery_factor` | `3.8667801142579323` |
| `net_profit` | `318.12` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `12.993966579271564` |
| `equity_dd_amount` | `82.26999999999998` |
| `max_dd_pct` | `10.317013137214188` |
| `max_dd_amount` | `69.57999999999993` |
| `ulcer_index` | `3.12408170570803` |
| `worst_day` | `-24.259999999999998` |
| `worst_week` | `-37.60999999999999` |
| `min_free_margin` | `461.55` |
| `consecutive_losses` | `7` |
| `time_under_water` | `22203000.0` |
| `longest_recovery_duration` | `6044400.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `3.0` |
| `payoff_ratio` | `1.1969449700910604` |
| `avg_win` | `5.688908450704226` |
| `avg_loss` | `-4.752857142857143` |
| `long_count` | `262` |
| `short_count` | `295` |
| `long_expectancy` | `0.4113740458015267` |
| `short_expectancy` | `0.7130169491525424` |
| `mfe_mean` | `5.474811490125673` |
| `mfe_median` | `3.79` |
| `mfe_p90` | `12.112000000000002` |
| `mae_mean` | `4.706876122082585` |
| `mae_median` | `3.18` |
| `mae_p90` | `10.118000000000002` |
| `no_trade_rate` | `0.8903538618577748` |
| `hold_distribution` | `{'p50': 3.0, 'p90': 3.0}` |
| `loss_trade_mfe` | `2.603772893772894` |
| `realized_over_mfe` | `-3.662325486360206` |
| `rule_pass_rates` | `{'long_signal_rate': 0.05188839741408642, 'short_signal_rate': 0.05775774072813882}` |
| `win_trade_mae` | `2.434014084507042` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0001 | completed | 2026-03-29 14:17:34 UTC | 63.62   | 557    | 11756 | 11756         | 0       
```

### 111. `05_optimization` / `05AU_05ai_diff_only_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05AU_05ai_diff_only_0001\experiment_bundle.json`
- experiment_id: `exp_05au_05ai_diff_only_v1`
- bundle_status: `completed`
- latest_attempt: `att_0001`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-30T10:39:21.321171+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: probability_difference(min_probability_diff=0.0775) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=3)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `63.461999999999996` |
| `profit_factor` | `1.3004260556712743` |
| `trade_count` | `457` |
| `win_rate` | `0.5317286652078774` |
| `expectancy_per_trade` | `0.6943326039387309` |
| `max_dd_pct` | `12.16722667355905` |
| `recovery_factor` | `2.8085501858736084` |
| `net_profit` | `317.31` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `12.16722667355905` |
| `equity_dd_amount` | `112.9799999999999` |
| `max_dd_pct` | `11.980916688205394` |
| `max_dd_amount` | `111.25` |
| `ulcer_index` | `6.4044720632525545` |
| `worst_day` | `-24.010000000000005` |
| `worst_week` | `-46.709999999999994` |
| `min_free_margin` | `469.82` |
| `consecutive_losses` | `7` |
| `time_under_water` | `22692000.0` |
| `longest_recovery_duration` | `13155600.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `3.0` |
| `payoff_ratio` | `1.1452311765993939` |
| `avg_win` | `5.6523045267489715` |
| `avg_loss` | `-4.935514018691589` |
| `long_count` | `197` |
| `short_count` | `260` |
| `long_expectancy` | `1.713756345177665` |
| `short_expectancy` | `-0.07807692307692309` |
| `mfe_mean` | `5.777286652078774` |
| `mfe_median` | `4.02` |
| `mfe_p90` | `12.896` |
| `mae_mean` | `5.142100656455142` |
| `mae_median` | `3.46` |
| `mae_p90` | `10.55` |
| `no_trade_rate` | `0.9100034025178633` |
| `hold_distribution` | `{'p50': 3.0, 'p90': 3.0}` |
| `loss_trade_mfe` | `2.898878504672897` |
| `realized_over_mfe` | `-3.5563107881207188` |
| `rule_pass_rates` | `{'long_signal_rate': 0.038703640694113646, 'short_signal_rate': 0.05129295678802314}` |
| `win_trade_mae` | `2.874238683127572` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0001 | completed | 2026-03-30 10:39:21 UTC | 63.46   | 457    | 11756 | 11756         | 0       
```

### 112. `05_optimization` / `05BG_trend_proxy_breakout_breadth_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05BG_trend_proxy_breakout_breadth_0001\experiment_bundle.json`
- experiment_id: `exp_05bg_trend_proxy_breakout_breadth_v1`
- bundle_status: `completed`
- latest_attempt: `att_0001`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-30T11:22:14.535963+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: max_probability_margin(min_margin=0.07) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=3)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `63.412` |
| `profit_factor` | `1.2709057819322096` |
| `trade_count` | `490` |
| `win_rate` | `0.5306122448979592` |
| `expectancy_per_trade` | `0.647061224489796` |
| `max_dd_pct` | `13.144494630986875` |
| `recovery_factor` | `2.569576140692115` |
| `net_profit` | `317.06` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `13.144494630986875` |
| `equity_dd_amount` | `123.38999999999999` |
| `max_dd_pct` | `12.683010237886599` |
| `max_dd_amount` | `118.68000000000006` |
| `ulcer_index` | `7.61947491017927` |
| `worst_day` | `-30.5` |
| `worst_week` | `-37.67999999999999` |
| `min_free_margin` | `472.48` |
| `consecutive_losses` | `7` |
| `time_under_water` | `22922400.0` |
| `longest_recovery_duration` | `13839900.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `3.0` |
| `payoff_ratio` | `1.1242628070938778` |
| `avg_win` | `5.720884615384616` |
| `avg_loss` | `-5.088565217391304` |
| `long_count` | `203` |
| `short_count` | `287` |
| `long_expectancy` | `1.3906896551724137` |
| `short_expectancy` | `0.1210801393728223` |
| `mfe_mean` | `5.918061224489795` |
| `mfe_median` | `4.215` |
| `mfe_p90` | `13.22700000000001` |
| `mae_mean` | `4.992857142857143` |
| `mae_median` | `3.475` |
| `mae_p90` | `10.019000000000002` |
| `no_trade_rate` | `0.8980945899965975` |
| `hold_distribution` | `{'p50': 3.0, 'p90': 3.0}` |
| `loss_trade_mfe` | `3.0810434782608693` |
| `realized_over_mfe` | `-2.963956791624729` |
| `rule_pass_rates` | `{'long_signal_rate': 0.04355222864920041, 'short_signal_rate': 0.05835318135420211}` |
| `win_trade_mae` | `2.745807692307692` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0001 | completed | 2026-03-30 11:22:14 UTC | 63.41   | 490    | 11756 | 11756         | 0       
```

### 113. `05_optimization` / `05BN_05w_balanced_tight_diff_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05BN_05w_balanced_tight_diff_0001\experiment_bundle.json`
- experiment_id: `exp_05bn_05w_balanced_tight_diff_v1`
- bundle_status: `completed`
- latest_attempt: `att_0001`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-30T11:36:20.268217+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.45, long_threshold=0.45) | filters: probability_difference(min_probability_diff=0.0775) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=3)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `63.282000000000004` |
| `profit_factor` | `1.3593608031982556` |
| `trade_count` | `334` |
| `win_rate` | `0.5299401197604791` |
| `expectancy_per_trade` | `0.9473353293413175` |
| `max_dd_pct` | `11.145773810443076` |
| `recovery_factor` | `3.224396209110364` |
| `net_profit` | `316.41` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `11.145773810443076` |
| `equity_dd_amount` | `98.13` |
| `max_dd_pct` | `10.314030538749645` |
| `max_dd_amount` | `93.08000000000004` |
| `ulcer_index` | `6.64826021162193` |
| `worst_day` | `-27.14` |
| `worst_week` | `-44.06` |
| `min_free_margin` | `478.95` |
| `consecutive_losses` | `8` |
| `time_under_water` | `22870500.0` |
| `longest_recovery_duration` | `13839900.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `3.0` |
| `payoff_ratio` | `1.2057607124413905` |
| `avg_win` | `6.762090395480227` |
| `avg_loss` | `-5.608152866242039` |
| `long_count` | `152` |
| `short_count` | `182` |
| `long_expectancy` | `1.8925` |
| `short_expectancy` | `0.15796703296703296` |
| `mfe_mean` | `6.733293413173653` |
| `mfe_median` | `5.1` |
| `mfe_p90` | `14.149999999999997` |
| `mae_mean` | `5.908562874251497` |
| `mae_median` | `4.3149999999999995` |
| `mae_p90` | `11.959999999999997` |
| `no_trade_rate` | `0.9347567199727799` |
| `hold_distribution` | `{'p50': 3.0, 'p90': 3.0}` |
| `loss_trade_mfe` | `3.2463694267515923` |
| `realized_over_mfe` | `-3.7878767189248412` |
| `rule_pass_rates` | `{'long_signal_rate': 0.030877849608710446, 'short_signal_rate': 0.034365430418509695}` |
| `win_trade_mae` | `3.266271186440678` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0001 | completed | 2026-03-30 11:36:20 UTC | 63.28   | 334    | 11756 | 11756         | 0       
```

### 114. `05_optimization` / `05AN_05w_diff_only_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05AN_05w_diff_only_0001\experiment_bundle.json`
- experiment_id: `exp_05an_05w_diff_only_v1`
- bundle_status: `completed`
- latest_attempt: `att_0001`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-29T17:55:46.596946+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: probability_difference(min_probability_diff=0.0775) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=3)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `63.129999999999995` |
| `profit_factor` | `1.2957573599685177` |
| `trade_count` | `463` |
| `win_rate` | `0.5248380129589633` |
| `expectancy_per_trade` | `0.6817494600431965` |
| `max_dd_pct` | `12.40297542043984` |
| `recovery_factor` | `2.8477986286539143` |
| `net_profit` | `315.65` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `12.40297542043984` |
| `equity_dd_amount` | `110.84000000000003` |
| `max_dd_pct` | `12.002299841885863` |
| `max_dd_amount` | `108.70000000000005` |
| `ulcer_index` | `7.033252983209113` |
| `worst_day` | `-24.010000000000005` |
| `worst_week` | `-46.709999999999994` |
| `min_free_margin` | `476.73` |
| `consecutive_losses` | `7` |
| `time_under_water` | `22936200.0` |
| `longest_recovery_duration` | `13238100.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `3.0` |
| `payoff_ratio` | `1.1731136592307567` |
| `avg_win` | `5.690987654320988` |
| `avg_loss` | `-4.851181818181818` |
| `long_count` | `201` |
| `short_count` | `262` |
| `long_expectancy` | `1.6162189054726368` |
| `short_expectancy` | `-0.0351526717557252` |
| `mfe_mean` | `5.774816414686825` |
| `mfe_median` | `4.18` |
| `mfe_p90` | `12.826000000000004` |
| `mae_mean` | `5.085442764578834` |
| `mae_median` | `3.38` |
| `mae_p90` | `10.466000000000005` |
| `no_trade_rate` | `0.9079618917999319` |
| `hold_distribution` | `{'p50': 3.0, 'p90': 3.0}` |
| `loss_trade_mfe` | `2.934772727272727` |
| `realized_over_mfe` | `-3.230361946305615` |
| `rule_pass_rates` | `{'long_signal_rate': 0.040149710785981625, 'short_signal_rate': 0.05188839741408642}` |
| `win_trade_mae` | `2.8499999999999996` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0001 | completed | 2026-03-29 17:55:46 UTC | 63.13   | 463    | 11756 | 11756         | 0       
```

### 115. `05_optimization` / `05U_no_momentum_osc_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05U_no_momentum_osc_0001\experiment_bundle.json`
- experiment_id: `exp_05u_momentum_oscillator_sector_ablation_v1`
- bundle_status: `completed`
- latest_attempt: `att_0001`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-29T16:48:27.086607+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: max_probability_margin(min_margin=0.07) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=3)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `62.954` |
| `profit_factor` | `1.2822062238320229` |
| `trade_count` | `461` |
| `win_rate` | `0.5336225596529284` |
| `expectancy_per_trade` | `0.6827982646420824` |
| `max_dd_pct` | `12.471208276400533` |
| `recovery_factor` | `4.926749100015657` |
| `net_profit` | `314.77` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `12.471208276400533` |
| `equity_dd_amount` | `63.88999999999993` |
| `max_dd_pct` | `11.805773454659551` |
| `max_dd_amount` | `60.25` |
| `ulcer_index` | `4.381972300784344` |
| `worst_day` | `-30.03` |
| `worst_week` | `-22.48` |
| `min_free_margin` | `437.7` |
| `consecutive_losses` | `11` |
| `time_under_water` | `22610700.0` |
| `longest_recovery_duration` | `13839900.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `3.0` |
| `payoff_ratio` | `1.1206273907474997` |
| `avg_win` | `5.813658536585367` |
| `avg_loss` | `-5.187860465116279` |
| `long_count` | `218` |
| `short_count` | `243` |
| `long_expectancy` | `1.2393577981651376` |
| `short_expectancy` | `0.18349794238683126` |
| `mfe_mean` | `5.913297180043385` |
| `mfe_median` | `4.24` |
| `mfe_p90` | `12.92` |
| `mae_mean` | `5.095379609544468` |
| `mae_median` | `3.75` |
| `mae_p90` | `10.81` |
| `no_trade_rate` | `0.9057502551888398` |
| `hold_distribution` | `{'p50': 3.0, 'p90': 3.0}` |
| `loss_trade_mfe` | `2.9957209302325585` |
| `realized_over_mfe` | `-3.6064184389032854` |
| `rule_pass_rates` | `{'long_signal_rate': 0.04491323579448792, 'short_signal_rate': 0.04933650901667234}` |
| `win_trade_mae` | `2.8087398373983743` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0001 | completed | 2026-03-29 16:48:27 UTC | 62.95   | 461    | 11756 | 11756         | 0       
```

### 116. `05_optimization` / `05C_mt5_validation_margin_tightgap_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05C_mt5_validation_margin_tightgap_0001\experiment_bundle.json`
- experiment_id: `exp_stage05_margin_tightgap_validation_0001`
- bundle_status: `completed`
- latest_attempt: `att_0002`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-29T10:59:14.051096+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: max_probability_margin(min_margin=0.085) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=3)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `62.822` |
| `profit_factor` | `1.337150891956293` |
| `trade_count` | `378` |
| `win_rate` | `0.5476190476190477` |
| `expectancy_per_trade` | `0.830978835978836` |
| `max_dd_pct` | `12.474980287499239` |
| `recovery_factor` | `3.8180381670110624` |
| `net_profit` | `314.11` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `12.474980287499239` |
| `equity_dd_amount` | `82.26999999999998` |
| `max_dd_pct` | `11.307723043552716` |
| `max_dd_amount` | `79.24000000000001` |
| `ulcer_index` | `2.709922503123142` |
| `worst_day` | `-25.39` |
| `worst_week` | `-21.33` |
| `min_free_margin` | `469.94` |
| `consecutive_losses` | `7` |
| `time_under_water` | `21809100.0` |
| `longest_recovery_duration` | `9678300.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `3.0` |
| `payoff_ratio` | `1.104602910746503` |
| `avg_win` | `6.018212560386473` |
| `avg_loss` | `-5.448304093567251` |
| `long_count` | `175` |
| `short_count` | `203` |
| `long_expectancy` | `0.9544` |
| `short_expectancy` | `0.7245812807881774` |
| `mfe_mean` | `6.308809523809524` |
| `mfe_median` | `4.385` |
| `mfe_p90` | `14.233` |
| `mae_mean` | `5.144338624338624` |
| `mae_median` | `3.5599999999999996` |
| `mae_p90` | `11.586` |
| `no_trade_rate` | `0.9276114324600204` |
| `hold_distribution` | `{'p50': 3.0, 'p90': 3.0}` |
| `loss_trade_mfe` | `3.1205263157894736` |
| `realized_over_mfe` | `-2.191758854219529` |
| `rule_pass_rates` | `{'long_signal_rate': 0.03496087104457298, 'short_signal_rate': 0.0374276964954066}` |
| `win_trade_mae` | `2.7478260869565214` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0002 | completed | 2026-03-29 10:59:14 UTC | 0.74    | 255    | 6755  | 6720          | 35      
att_0001 | completed | 2026-03-29 10:49:48 UTC | 62.82   | 378    | 11756 | 11756         | 0       
```

### 117. `05_optimization` / `05AL_trend_proxy_light_pc_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05AL_trend_proxy_light_pc_0001\experiment_bundle.json`
- experiment_id: `exp_05al_trend_proxy_light_pc_v1`
- bundle_status: `completed`
- latest_attempt: `att_0001`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-29T17:48:52.930376+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: max_probability_margin(min_margin=0.07) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=3)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `62.736000000000004` |
| `profit_factor` | `1.268233241835766` |
| `trade_count` | `490` |
| `win_rate` | `0.5306122448979592` |
| `expectancy_per_trade` | `0.6401632653061224` |
| `max_dd_pct` | `14.067138858257694` |
| `recovery_factor` | `2.364362704454663` |
| `net_profit` | `313.68` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `14.067138858257694` |
| `equity_dd_amount` | `132.66999999999996` |
| `max_dd_pct` | `13.781989916395423` |
| `max_dd_amount` | `129.56999999999994` |
| `ulcer_index` | `8.463035713065029` |
| `worst_day` | `-30.5` |
| `worst_week` | `-37.67999999999999` |
| `min_free_margin` | `472.48` |
| `consecutive_losses` | `10` |
| `time_under_water` | `22999500.0` |
| `longest_recovery_duration` | `13839900.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `3.0` |
| `payoff_ratio` | `1.1218986370085622` |
| `avg_win` | `5.70426923076923` |
| `avg_loss` | `-5.084478260869566` |
| `long_count` | `202` |
| `short_count` | `288` |
| `long_expectancy` | `1.4453960396039602` |
| `short_expectancy` | `0.07538194444444445` |
| `mfe_mean` | `5.90965306122449` |
| `mfe_median` | `4.21` |
| `mfe_p90` | `13.22700000000001` |
| `mae_mean` | `4.997612244897959` |
| `mae_median` | `3.5949999999999998` |
| `mae_p90` | `9.938` |
| `no_trade_rate` | `0.8990302824089826` |
| `hold_distribution` | `{'p50': 3.0, 'p90': 3.0}` |
| `loss_trade_mfe` | `3.088391304347826` |
| `realized_over_mfe` | `-2.906283082784497` |
| `rule_pass_rates` | `{'long_signal_rate': 0.043297039809459, 'short_signal_rate': 0.05767267778155835}` |
| `win_trade_mae` | `2.775346153846154` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0001 | completed | 2026-03-29 17:48:52 UTC | 62.74   | 490    | 11756 | 11756         | 0       
```

### 118. `05_optimization` / `05FF_05ca_temp_shortbias_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05FF_05ca_temp_shortbias_0001\experiment_bundle.json`
- experiment_id: `exp_05ff_05ca_temp_shortbias_v1`
- bundle_status: `completed`
- latest_attempt: `att_0001`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-30T16:25:18.010079+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: max_probability_margin(min_margin=0.0675) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=5)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `62.43200000000001` |
| `profit_factor` | `1.1538582863451756` |
| `trade_count` | `722` |
| `win_rate` | `0.48753462603878117` |
| `expectancy_per_trade` | `0.43235457063711913` |
| `max_dd_pct` | `29.935208582895424` |
| `recovery_factor` | `0.9117887603692018` |
| `net_profit` | `312.16` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `29.935208582895424` |
| `equity_dd_amount` | `342.3600000000001` |
| `max_dd_pct` | `29.355845754737725` |
| `max_dd_amount` | `333.82000000000005` |
| `ulcer_index` | `16.940784811837858` |
| `worst_day` | `-34.4` |
| `worst_week` | `-64.45` |
| `min_free_margin` | `448.28` |
| `consecutive_losses` | `9` |
| `time_under_water` | `23248500.0` |
| `longest_recovery_duration` | `13839900.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `5.0` |
| `payoff_ratio` | `1.212862403260554` |
| `avg_win` | `6.650681818181818` |
| `avg_loss` | `-5.48345945945946` |
| `long_count` | `30` |
| `short_count` | `692` |
| `long_expectancy` | `8.604000000000001` |
| `short_expectancy` | `0.07809248554913295` |
| `mfe_mean` | `6.241385041551246` |
| `mfe_median` | `4.33` |
| `mfe_p90` | `13.529999999999996` |
| `mae_mean` | `5.708240997229917` |
| `mae_median` | `4.25` |
| `mae_p90` | `11.37` |
| `no_trade_rate` | `0.7697346036066689` |
| `hold_distribution` | `{'p50': 5.0, 'p90': 5.0}` |
| `loss_trade_mfe` | `2.9695675675675677` |
| `realized_over_mfe` | `-5.585149816624534` |
| `rule_pass_rates` | `{'long_signal_rate': 0.008506294658046955, 'short_signal_rate': 0.2217591017352841}` |
| `win_trade_mae` | `3.0768465909090907` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0001 | completed | 2026-03-30 16:25:18 UTC | 62.43   | 722    | 11756 | 11756         | 0       
```

### 119. `05_optimization` / `05BL_05w_long_bias_diff_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05BL_05w_long_bias_diff_0001\experiment_bundle.json`
- experiment_id: `exp_05bl_05w_long_bias_diff_v1`
- bundle_status: `completed`
- latest_attempt: `att_0001`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-30T11:33:36.307660+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.575, long_threshold=0.375) | filters: probability_difference(min_probability_diff=0.0775) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=3)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `62.227999999999994` |
| `profit_factor` | `1.6282229894804854` |
| `trade_count` | `204` |
| `win_rate` | `0.6029411764705882` |
| `expectancy_per_trade` | `1.5251960784313725` |
| `max_dd_pct` | `13.996656383033734` |
| `recovery_factor` | `3.831301563846815` |
| `net_profit` | `311.14` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `13.996656383033734` |
| `equity_dd_amount` | `81.21000000000004` |
| `max_dd_pct` | `10.406591128920823` |
| `max_dd_amount` | `60.25` |
| `ulcer_index` | `1.3846274547895259` |
| `worst_day` | `-25.309999999999995` |
| `worst_week` | `-14.350000000000001` |
| `min_free_margin` | `484.99` |
| `consecutive_losses` | `4` |
| `time_under_water` | `22649400.0` |
| `longest_recovery_duration` | `9679200.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `3.0` |
| `payoff_ratio` | `1.072244407706661` |
| `avg_win` | `6.556178861788617` |
| `avg_loss` | `-6.114444444444445` |
| `long_count` | `193` |
| `short_count` | `11` |
| `long_expectancy` | `1.2158031088082901` |
| `short_expectancy` | `6.953636363636364` |
| `mfe_mean` | `7.176421568627451` |
| `mfe_median` | `4.795` |
| `mfe_p90` | `16.60700000000003` |
| `mae_mean` | `5.584705882352941` |
| `mae_median` | `3.57` |
| `mae_p90` | `12.216000000000005` |
| `no_trade_rate` | `0.9596801633208575` |
| `hold_distribution` | `{'p50': 3.0, 'p90': 3.0}` |
| `loss_trade_mfe` | `3.795432098765432` |
| `realized_over_mfe` | `-2.3823104142894733` |
| `rule_pass_rates` | `{'long_signal_rate': 0.038533514800952705, 'short_signal_rate': 0.0017863218781898605}` |
| `win_trade_mae` | `3.3159349593495935` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0001 | completed | 2026-03-30 11:33:36 UTC | 62.23   | 204    | 11756 | 11756         | 0       
```

### 120. `05_optimization` / `05AH_trend_proxy_sector_replacement_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05AH_trend_proxy_sector_replacement_0001\experiment_bundle.json`
- experiment_id: `exp_05ah_trend_proxy_sector_replacement_v1`
- bundle_status: `completed`
- latest_attempt: `att_0002`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-29T17:32:24.190264+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: max_probability_margin(min_margin=0.07) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=3)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `62.2` |
| `profit_factor` | `1.2631734829444967` |
| `trade_count` | `489` |
| `win_rate` | `0.5337423312883436` |
| `expectancy_per_trade` | `0.6359918200408998` |
| `max_dd_pct` | `13.454463789194513` |
| `recovery_factor` | `2.4719815594944747` |
| `net_profit` | `311.0` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `13.454463789194513` |
| `equity_dd_amount` | `125.81000000000006` |
| `max_dd_pct` | `12.99216822229375` |
| `max_dd_amount` | `121.10000000000002` |
| `ulcer_index` | `7.922504691164585` |
| `worst_day` | `-30.5` |
| `worst_week` | `-37.67999999999999` |
| `min_free_margin` | `472.48` |
| `consecutive_losses` | `7` |
| `time_under_water` | `22915500.0` |
| `longest_recovery_duration` | `13839900.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `3.0` |
| `payoff_ratio` | `1.1034618931469167` |
| `avg_win` | `5.719272030651341` |
| `avg_loss` | `-5.183026315789474` |
| `long_count` | `202` |
| `short_count` | `287` |
| `long_expectancy` | `1.378910891089109` |
| `short_expectancy` | `0.11310104529616725` |
| `mfe_mean` | `5.9153374233128835` |
| `mfe_median` | `4.21` |
| `mfe_p90` | `13.263999999999996` |
| `mae_mean` | `5.0556646216768915` |
| `mae_median` | `3.48` |
| `mae_p90` | `10.134` |
| `no_trade_rate` | `0.899285471248724` |
| `hold_distribution` | `{'p50': 3.0, 'p90': 3.0}` |
| `loss_trade_mfe` | `3.0598684210526317` |
| `realized_over_mfe` | `-2.9041963173500807` |
| `rule_pass_rates` | `{'long_signal_rate': 0.04287172507655665, 'short_signal_rate': 0.05784280367471929}` |
| `win_trade_mae` | `2.809616858237548` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0002 | completed | 2026-03-29 17:32:24 UTC | 44.56   | 331    | 6755  | 6720          | 35      
att_0001 | completed | 2026-03-29 17:31:19 UTC | 62.20   | 489    | 11756 | 11756         | 0       
```

### 121. `05_optimization` / `05AK_trend_proxy_light_core3_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05AK_trend_proxy_light_core3_0001\experiment_bundle.json`
- experiment_id: `exp_05ak_trend_proxy_light_core3_v1`
- bundle_status: `completed`
- latest_attempt: `att_0001`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-29T17:47:14.398400+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: max_probability_margin(min_margin=0.07) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=3)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `61.826` |
| `profit_factor` | `1.2556525910120908` |
| `trade_count` | `493` |
| `win_rate` | `0.5354969574036511` |
| `expectancy_per_trade` | `0.6270385395537525` |
| `max_dd_pct` | `13.911288157795845` |
| `recovery_factor` | `2.3859987650509407` |
| `net_profit` | `309.13` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `13.911288157795845` |
| `equity_dd_amount` | `129.56000000000006` |
| `max_dd_pct` | `13.82715784044016` |
| `max_dd_amount` | `128.66999999999996` |
| `ulcer_index` | `8.393798077447377` |
| `worst_day` | `-30.5` |
| `worst_week` | `-38.46999999999999` |
| `min_free_margin` | `470.23` |
| `consecutive_losses` | `7` |
| `time_under_water` | `22924200.0` |
| `longest_recovery_duration` | `13840800.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `3.0` |
| `payoff_ratio` | `1.0891834975066998` |
| `avg_win` | `5.751174242424242` |
| `avg_loss` | `-5.280262008733625` |
| `long_count` | `205` |
| `short_count` | `288` |
| `long_expectancy` | `1.4061951219512194` |
| `short_expectancy` | `0.07243055555555557` |
| `mfe_mean` | `5.8977079107505075` |
| `mfe_median` | `4.21` |
| `mfe_p90` | `13.060000000000002` |
| `mae_mean` | `5.055476673427992` |
| `mae_median` | `3.48` |
| `mae_p90` | `10.55` |
| `no_trade_rate` | `0.8991153453555631` |
| `hold_distribution` | `{'p50': 3.0, 'p90': 3.0}` |
| `loss_trade_mfe` | `3.026506550218341` |
| `realized_over_mfe` | `-3.1208748068668797` |
| `rule_pass_rates` | `{'long_signal_rate': 0.043382102756039466, 'short_signal_rate': 0.05750255188839742}` |
| `win_trade_mae` | `2.753598484848485` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0001 | completed | 2026-03-29 17:47:14 UTC | 61.83   | 493    | 11756 | 11756         | 0       
```

### 122. `04_probability_difference_filter` / `04C_mt5_validation_baseline_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\04_probability_difference_filter\02_runs\active\04C_mt5_validation_baseline_0001\experiment_bundle.json`
- experiment_id: `exp_stage04_diff_validation_0001`
- bundle_status: `completed`
- latest_attempt: `att_0002`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-29T06:10:06.719044+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: probability_difference(min_probability_diff=0.0825) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=3)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `60.648` |
| `profit_factor` | `1.2829972095974915` |
| `trade_count` | `435` |
| `win_rate` | `0.5402298850574713` |
| `expectancy_per_trade` | `0.6971034482758621` |
| `max_dd_pct` | `12.670958600295709` |
| `recovery_factor` | `3.6859122401847584` |
| `net_profit` | `303.24` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `12.670958600295709` |
| `equity_dd_amount` | `82.26999999999998` |
| `max_dd_pct` | `11.474745134383674` |
| `max_dd_amount` | `79.2399999999999` |
| `ulcer_index` | `2.201610130938037` |
| `worst_day` | `-33.330000000000005` |
| `worst_week` | `-32.690000000000005` |
| `min_free_margin` | `474.57` |
| `consecutive_losses` | `9` |
| `time_under_water` | `20788500.0` |
| `longest_recovery_duration` | `2579700.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `3.0` |
| `payoff_ratio` | `1.0919125188063759` |
| `avg_win` | `5.850085106382979` |
| `avg_loss` | `-5.35765` |
| `long_count` | `201` |
| `short_count` | `234` |
| `long_expectancy` | `0.8196517412935324` |
| `short_expectancy` | `0.5918376068376068` |
| `mfe_mean` | `5.990252873563219` |
| `mfe_median` | `4.28` |
| `mfe_p90` | `13.334000000000005` |
| `mae_mean` | `4.943494252873563` |
| `mae_median` | `3.32` |
| `mae_p90` | `11.014000000000003` |
| `no_trade_rate` | `0.9163831235113984` |
| `hold_distribution` | `{'p50': 3.0, 'p90': 3.0}` |
| `loss_trade_mfe` | `2.9386` |
| `realized_over_mfe` | `-3.1282664055045486` |
| `rule_pass_rates` | `{'long_signal_rate': 0.040149710785981625, 'short_signal_rate': 0.043467165702619937}` |
| `win_trade_mae` | `2.5257446808510635` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0002 | completed | 2026-03-29 06:10:06 UTC | 60.65   | 435    | 11756 | 11756         | 0       
att_0001 | completed | 2026-03-28 19:17:37 UTC | 61.04   | 434    | 11696 | -             | -       
```

### 123. `05_optimization` / `05E_mt5_validation_margin_08250_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05E_mt5_validation_margin_08250_0001\experiment_bundle.json`
- experiment_id: `exp_stage05_margin_frontier_08250_validation_0001`
- bundle_status: `completed`
- latest_attempt: `att_0001`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-29T14:14:51.332769+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: max_probability_margin(min_margin=0.0825) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=3)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `56.752` |
| `profit_factor` | `1.272809429499875` |
| `trade_count` | `408` |
| `win_rate` | `0.5392156862745098` |
| `expectancy_per_trade` | `0.6954901960784313` |
| `max_dd_pct` | `12.613068408303436` |
| `recovery_factor` | `3.4491309104169208` |
| `net_profit` | `283.76` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `12.613068408303436` |
| `equity_dd_amount` | `82.26999999999998` |
| `max_dd_pct` | `11.425440493698996` |
| `max_dd_amount` | `79.24000000000001` |
| `ulcer_index` | `2.2329105166810725` |
| `worst_day` | `-19.46` |
| `worst_week` | `-21.509999999999998` |
| `min_free_margin` | `474.57` |
| `consecutive_losses` | `7` |
| `time_under_water` | `22051800.0` |
| `longest_recovery_duration` | `5001600.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `3.0` |
| `payoff_ratio` | `1.0876735124817114` |
| `avg_win` | `6.0177272727272735` |
| `avg_loss` | `-5.532659574468085` |
| `long_count` | `184` |
| `short_count` | `224` |
| `long_expectancy` | `0.8529891304347827` |
| `short_expectancy` | `0.5661160714285713` |
| `mfe_mean` | `6.195294117647059` |
| `mfe_median` | `4.385` |
| `mfe_p90` | `13.696000000000002` |
| `mae_mean` | `5.114877450980392` |
| `mae_median` | `3.54` |
| `mae_p90` | `11.153` |
| `no_trade_rate` | `0.9208914596801633` |
| `hold_distribution` | `{'p50': 3.0, 'p90': 3.0}` |
| `loss_trade_mfe` | `3.0631382978723405` |
| `realized_over_mfe` | `-2.8134234473363837` |
| `rule_pass_rates` | `{'long_signal_rate': 0.03717250765566519, 'short_signal_rate': 0.04193603266417149}` |
| `win_trade_mae` | `2.640727272727273` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0001 | completed | 2026-03-29 14:14:51 UTC | 56.75   | 408    | 11756 | 11756         | 0       
```

### 124. `05_optimization` / `05V_no_vol_band_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05V_no_vol_band_0001\experiment_bundle.json`
- experiment_id: `exp_05v_volatility_band_sector_ablation_v1`
- bundle_status: `completed`
- latest_attempt: `att_0001`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-29T16:49:50.748502+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: max_probability_margin(min_margin=0.07) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=3)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `55.98` |
| `profit_factor` | `1.2701450618177608` |
| `trade_count` | `429` |
| `win_rate` | `0.5407925407925408` |
| `expectancy_per_trade` | `0.6524475524475524` |
| `max_dd_pct` | `14.465563624215363` |
| `recovery_factor` | `3.4022122280296565` |
| `net_profit` | `279.9` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `14.465563624215363` |
| `equity_dd_amount` | `82.27000000000004` |
| `max_dd_pct` | `13.775996610289182` |
| `max_dd_amount` | `78.02999999999997` |
| `ulcer_index` | `4.396914416936819` |
| `worst_day` | `-18.73` |
| `worst_week` | `-18.69` |
| `min_free_margin` | `436.37` |
| `consecutive_losses` | `5` |
| `time_under_water` | `22495500.0` |
| `longest_recovery_duration` | `5810100.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `3.0` |
| `payoff_ratio` | `1.0785283499055986` |
| `avg_win` | `5.672456896551724` |
| `avg_loss` | `-5.259441624365482` |
| `long_count` | `222` |
| `short_count` | `207` |
| `long_expectancy` | `0.6277027027027027` |
| `short_expectancy` | `0.6789855072463769` |
| `mfe_mean` | `5.768554778554779` |
| `mfe_median` | `4.16` |
| `mfe_p90` | `13.58` |
| `mae_mean` | `5.276526806526807` |
| `mae_median` | `3.6` |
| `mae_p90` | `11.838000000000001` |
| `no_trade_rate` | `0.9210615855733243` |
| `hold_distribution` | `{'p50': 3.0, 'p90': 3.0}` |
| `loss_trade_mfe` | `2.7339086294416246` |
| `realized_over_mfe` | `-3.7556823165968938` |
| `rule_pass_rates` | `{'long_signal_rate': 0.04040489962572304, 'short_signal_rate': 0.038533514800952705}` |
| `win_trade_mae` | `2.825301724137931` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0001 | completed | 2026-03-29 16:49:50 UTC | 55.98   | 429    | 11756 | 11756         | 0       
```

### 125. `05_optimization` / `05DA_mt5_validation_margin_regularized_vote_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05DA_mt5_validation_margin_regularized_vote_0001\experiment_bundle.json`
- experiment_id: `exp_05da_margin_regularized_vote_v1`
- bundle_status: `completed`
- latest_attempt: `att_0003`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-30T12:52:42.457337+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: max_probability_margin(min_margin=0.07) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=3)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `53.238` |
| `profit_factor` | `1.222041490453192` |
| `trade_count` | `489` |
| `win_rate` | `0.5296523517382413` |
| `expectancy_per_trade` | `0.5443558282208589` |
| `max_dd_pct` | `14.149025773485317` |
| `recovery_factor` | `2.1127867291054843` |
| `net_profit` | `266.19` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `14.149025773485317` |
| `equity_dd_amount` | `125.99000000000001` |
| `max_dd_pct` | `13.665814055686386` |
| `max_dd_amount` | `121.27999999999997` |
| `ulcer_index` | `8.286855690874646` |
| `worst_day` | `-30.5` |
| `worst_week` | `-37.67999999999999` |
| `min_free_margin` | `472.48` |
| `consecutive_losses` | `7` |
| `time_under_water` | `22925400.0` |
| `longest_recovery_duration` | `13839900.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `3.0` |
| `payoff_ratio` | `1.085210589977738` |
| `avg_win` | `5.656447876447876` |
| `avg_loss` | `-5.212304347826087` |
| `long_count` | `203` |
| `short_count` | `286` |
| `long_expectancy` | `1.3754679802955663` |
| `short_expectancy` | `-0.045559440559440556` |
| `mfe_mean` | `5.8635787321063395` |
| `mfe_median` | `4.18` |
| `mfe_p90` | `13.0` |
| `mae_mean` | `5.0736605316973415` |
| `mae_median` | `3.56` |
| `mae_p90` | `10.229999999999997` |
| `no_trade_rate` | `0.8999659748213679` |
| `hold_distribution` | `{'p50': 3.0, 'p90': 3.0}` |
| `loss_trade_mfe` | `3.0637391304347825` |
| `realized_over_mfe` | `-3.186132461023815` |
| `rule_pass_rates` | `{'long_signal_rate': 0.04287172507655665, 'short_signal_rate': 0.057162300102075535}` |
| `win_trade_mae` | `2.7927027027027025` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0003 | completed | 2026-03-30 12:52:42 UTC | 46.22   | 329    | 6755  | 6720          | 35      
att_0002 | completed | 2026-03-30 12:51:32 UTC | 53.24   | 489    | 11756 | 11756         | 0       
att_0001 | completed | 2026-03-30 12:49:06 UTC | 53.24   | 489    | 11756 | 11756         | 0       
```

### 126. `05_optimization` / `05BJ_05w_short_bias_diff_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05BJ_05w_short_bias_diff_0001\experiment_bundle.json`
- experiment_id: `exp_05bj_05w_short_bias_diff_v1`
- bundle_status: `completed`
- latest_attempt: `att_0001`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-30T11:30:53.418796+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3, long_threshold=0.45) | filters: probability_difference(min_probability_diff=0.0775) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=3)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `53.004` |
| `profit_factor` | `1.2587656346114415` |
| `trade_count` | `416` |
| `win_rate` | `0.5024038461538461` |
| `expectancy_per_trade` | `0.6370673076923077` |
| `max_dd_pct` | `13.425810403103238` |
| `recovery_factor` | `2.238911886457717` |
| `net_profit` | `265.02` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `13.425810403103238` |
| `equity_dd_amount` | `118.37` |
| `max_dd_pct` | `12.741665050813825` |
| `max_dd_amount` | `111.71000000000004` |
| `ulcer_index` | `8.181993103698952` |
| `worst_day` | `-25.870000000000005` |
| `worst_week` | `-42.519999999999996` |
| `min_free_margin` | `472.09` |
| `consecutive_losses` | `7` |
| `time_under_water` | `22935900.0` |
| `longest_recovery_duration` | `13839900.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `3.0` |
| `payoff_ratio` | `1.2467200304524801` |
| `avg_win` | `6.168373205741627` |
| `avg_loss` | `-4.9476811594202905` |
| `long_count` | `152` |
| `short_count` | `264` |
| `long_expectancy` | `1.8925` |
| `short_expectancy` | `-0.08575757575757577` |
| `mfe_mean` | `6.05625` |
| `mfe_median` | `4.494999999999999` |
| `mfe_p90` | `13.030000000000001` |
| `mae_mean` | `5.389471153846154` |
| `mae_median` | `3.835` |
| `mae_p90` | `10.940000000000001` |
| `no_trade_rate` | `0.9171486900306227` |
| `hold_distribution` | `{'p50': 3.0, 'p90': 3.0}` |
| `loss_trade_mfe` | `3.059420289855072` |
| `realized_over_mfe` | `-3.296609421981442` |
| `rule_pass_rates` | `{'long_signal_rate': 0.030877849608710446, 'short_signal_rate': 0.05197346036066689}` |
| `win_trade_mae` | `3.0663636363636364` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0001 | completed | 2026-03-30 11:30:53 UTC | 53.00   | 416    | 11756 | 11756         | 0       
```

### 127. `05_optimization` / `05AA_no_breadth_disp_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05AA_no_breadth_disp_0001\experiment_bundle.json`
- experiment_id: `exp_05aa_breadth_dispersion_sector_ablation_v1`
- bundle_status: `completed`
- latest_attempt: `att_0001`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-29T16:56:51.758248+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: max_probability_margin(min_margin=0.07) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=3)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `49.11000000000001` |
| `profit_factor` | `1.1919634132040808` |
| `trade_count` | `501` |
| `win_rate` | `0.5349301397205589` |
| `expectancy_per_trade` | `0.49011976047904193` |
| `max_dd_pct` | `13.631016485792394` |
| `recovery_factor` | `2.9846845751792883` |
| `net_profit` | `245.55` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `13.631016485792394` |
| `equity_dd_amount` | `82.26999999999998` |
| `max_dd_pct` | `10.813999999999998` |
| `max_dd_amount` | `70.82999999999993` |
| `ulcer_index` | `5.160475407608112` |
| `worst_day` | `-34.99` |
| `worst_week` | `-40.82` |
| `min_free_margin` | `434.97` |
| `consecutive_losses` | `10` |
| `time_under_water` | `23083500.0` |
| `longest_recovery_duration` | `13236300.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `3.0` |
| `payoff_ratio` | `1.0362965495393688` |
| `avg_win` | `5.6891791044776125` |
| `avg_loss` | `-5.48991416309013` |
| `long_count` | `225` |
| `short_count` | `276` |
| `long_expectancy` | `0.49124444444444443` |
| `short_expectancy` | `0.4892028985507246` |
| `mfe_mean` | `5.648702594810379` |
| `mfe_median` | `4.02` |
| `mfe_p90` | `12.92` |
| `mae_mean` | `5.085528942115769` |
| `mae_median` | `3.48` |
| `mae_p90` | `11.12` |
| `no_trade_rate` | `0.8971588975842123` |
| `hold_distribution` | `{'p50': 3.0, 'p90': 3.0}` |
| `loss_trade_mfe` | `2.7051502145922743` |
| `realized_over_mfe` | `-4.034334123868616` |
| `rule_pass_rates` | `{'long_signal_rate': 0.04618917999319497, 'short_signal_rate': 0.05665192242259272}` |
| `win_trade_mae` | `2.760335820895522` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0001 | completed | 2026-03-29 16:56:51 UTC | 49.11   | 501    | 11756 | 11756         | 0       
```

### 128. `05_optimization` / `05FC_05ca_shortup_longdown_margin0675_hold5_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05FC_05ca_shortup_longdown_margin0675_hold5_0001\experiment_bundle.json`
- experiment_id: `exp_05fc_05ca_shortup_longdown_margin0675_hold5_v1`
- bundle_status: `completed`
- latest_attempt: `att_0002`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-30T16:20:05.102200+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: max_probability_margin(min_margin=0.0675) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=5)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `49.11` |
| `profit_factor` | `1.1025256679512818` |
| `trade_count` | `840` |
| `win_rate` | `0.48333333333333334` |
| `expectancy_per_trade` | `0.29232142857142857` |
| `max_dd_pct` | `31.036379350986092` |
| `recovery_factor` | `0.8692650807136787` |
| `net_profit` | `245.54999999999998` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `31.036379350986092` |
| `equity_dd_amount` | `282.48` |
| `max_dd_pct` | `29.348000000000003` |
| `max_dd_amount` | `276.35` |
| `ulcer_index` | `18.317315817939` |
| `worst_day` | `-37.63` |
| `worst_week` | `-55.34000000000001` |
| `min_free_margin` | `340.04` |
| `consecutive_losses` | `11` |
| `time_under_water` | `23097000.0` |
| `longest_recovery_duration` | `13839900.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `5.0` |
| `payoff_ratio` | `1.1785619209134393` |
| `avg_win` | `6.503842364532019` |
| `avg_loss` | `-5.518456221198157` |
| `long_count` | `26` |
| `short_count` | `814` |
| `long_expectancy` | `6.398846153846154` |
| `short_expectancy` | `0.09727272727272726` |
| `mfe_mean` | `6.016809523809524` |
| `mfe_median` | `4.29` |
| `mfe_p90` | `13.431` |
| `mae_mean` | `5.543083333333333` |
| `mae_median` | `4.21` |
| `mae_p90` | `11.124000000000002` |
| `no_trade_rate` | `0.7068730860837019` |
| `hold_distribution` | `{'p50': 5.0, 'p90': 5.0}` |
| `loss_trade_mfe` | `2.760852534562212` |
| `realized_over_mfe` | `-4.278122292900879` |
| `rule_pass_rates` | `{'long_signal_rate': 0.007910854031983668, 'short_signal_rate': 0.28521605988431437}` |
| `win_trade_mae` | `2.81384236453202` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0002 | completed | 2026-03-30 16:20:05 UTC | 49.11   | 840    | 11756 | 11756         | 0       
att_0001 | completed | 2026-03-30 16:09:40 UTC | 49.11   | 840    | 11756 | 11756         | 0       
```

### 129. `05_optimization` / `05CY_mt5_validation_margin_elasticnet_logreg_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05CY_mt5_validation_margin_elasticnet_logreg_0001\experiment_bundle.json`
- experiment_id: `exp_05cy_margin_elasticnet_logreg_v1`
- bundle_status: `completed`
- latest_attempt: `att_0003`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-30T12:55:34.797551+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: max_probability_margin(min_margin=0.07) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=3)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `42.51` |
| `profit_factor` | `1.1782165765312538` |
| `trade_count` | `477` |
| `win_rate` | `0.5283018867924528` |
| `expectancy_per_trade` | `0.4455974842767295` |
| `max_dd_pct` | `14.825953571514844` |
| `recovery_factor` | `1.7315682281059062` |
| `net_profit` | `212.54999999999998` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `14.825953571514844` |
| `equity_dd_amount` | `122.75` |
| `max_dd_pct` | `14.503733514352222` |
| `max_dd_amount` | `119.65000000000009` |
| `ulcer_index` | `8.767805873527077` |
| `worst_day` | `-32.59` |
| `worst_week` | `-37.67999999999999` |
| `min_free_margin` | `464.66` |
| `consecutive_losses` | `7` |
| `time_under_water` | `22773300.0` |
| `longest_recovery_duration` | `13839900.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `3.0` |
| `payoff_ratio` | `1.0519790861886196` |
| `avg_win` | `5.576190476190477` |
| `avg_loss` | `-5.300666666666667` |
| `long_count` | `199` |
| `short_count` | `278` |
| `long_expectancy` | `1.093819095477387` |
| `short_expectancy` | `-0.01841726618705036` |
| `mfe_mean` | `5.821299790356394` |
| `mfe_median` | `4.16` |
| `mfe_p90` | `12.944000000000003` |
| `mae_mean` | `5.183165618448637` |
| `mae_median` | `3.48` |
| `mae_p90` | `10.804000000000002` |
| `no_trade_rate` | `0.90217761143246` |
| `hold_distribution` | `{'p50': 3.0, 'p90': 3.0}` |
| `loss_trade_mfe` | `3.1178666666666666` |
| `realized_over_mfe` | `-3.2653918044399575` |
| `rule_pass_rates` | `{'long_signal_rate': 0.041680843824430075, 'short_signal_rate': 0.0561415447431099}` |
| `win_trade_mae` | `2.8279365079365077` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0003 | completed | 2026-03-30 12:55:34 UTC | 29.23   | 325    | 6755  | 6720          | 35      
att_0002 | completed | 2026-03-30 12:54:40 UTC | 42.51   | 477    | 11756 | 11756         | 0       
att_0001 | completed | 2026-03-30 12:45:03 UTC | 42.51   | 477    | 11756 | 11756         | 0       
```

### 130. `05_optimization` / `05Y_no_risk_proxy_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05Y_no_risk_proxy_0001\experiment_bundle.json`
- experiment_id: `exp_05y_risk_proxy_sector_ablation_v1`
- bundle_status: `completed`
- latest_attempt: `att_0001`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-29T16:54:04.949205+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: max_probability_margin(min_margin=0.07) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=3)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `42.081999999999994` |
| `profit_factor` | `1.1792722098680228` |
| `trade_count` | `494` |
| `win_rate` | `0.520242914979757` |
| `expectancy_per_trade` | `0.42593117408906883` |
| `max_dd_pct` | `16.55884328490119` |
| `recovery_factor` | `1.4973669228579563` |
| `net_profit` | `210.41` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `16.55884328490119` |
| `equity_dd_amount` | `140.51999999999998` |
| `max_dd_pct` | `15.839823606813896` |
| `max_dd_amount` | `133.62` |
| `ulcer_index` | `9.364573167184522` |
| `worst_day` | `-34.02` |
| `worst_week` | `-36.89999999999999` |
| `min_free_margin` | `448.86` |
| `consecutive_losses` | `13` |
| `time_under_water` | `22791900.0` |
| `longest_recovery_duration` | `13839900.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `3.0` |
| `payoff_ratio` | `1.08750005345806` |
| `avg_win` | `5.3856031128404664` |
| `avg_loss` | `-4.952278481012659` |
| `long_count` | `220` |
| `short_count` | `274` |
| `long_expectancy` | `0.5077727272727273` |
| `short_expectancy` | `0.3602189781021897` |
| `mfe_mean` | `5.837773279352227` |
| `mfe_median` | `4.145` |
| `mfe_p90` | `13.043` |
| `mae_mean` | `4.94172064777328` |
| `mae_median` | `3.495` |
| `mae_p90` | `10.571` |
| `no_trade_rate` | `0.9004763525008507` |
| `hold_distribution` | `{'p50': 3.0, 'p90': 3.0}` |
| `loss_trade_mfe` | `3.2931645569620254` |
| `realized_over_mfe` | `-3.410007675796444` |
| `rule_pass_rates` | `{'long_signal_rate': 0.044317795168424635, 'short_signal_rate': 0.05520585233072474}` |
| `win_trade_mae` | `2.7273929961089496` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0001 | completed | 2026-03-29 16:54:04 UTC | 42.08   | 494    | 11756 | 11756         | 0       
```

### 131. `05_optimization` / `05O_thr_diff_mix_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05O_thr_diff_mix_0001\experiment_bundle.json`
- experiment_id: `exp_05O_thr_diff_mix_v1`
- bundle_status: `completed`
- latest_attempt: `att_0001`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-29T16:02:52.648160+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.535, long_threshold=0.4) | filters: probability_difference(min_probability_diff=0.0775) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=3)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `41.006` |
| `profit_factor` | `1.2793019834350479` |
| `trade_count` | `247` |
| `win_rate` | `0.5587044534412956` |
| `expectancy_per_trade` | `0.830080971659919` |
| `max_dd_pct` | `16.28071263654847` |
| `recovery_factor` | `2.1698592443644826` |
| `net_profit` | `205.03` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `16.28071263654847` |
| `equity_dd_amount` | `94.49000000000001` |
| `max_dd_pct` | `16.26003652779214` |
| `max_dd_amount` | `94.37` |
| `ulcer_index` | `2.4835112752310415` |
| `worst_day` | `-28.53` |
| `worst_week` | `-22.840000000000003` |
| `min_free_margin` | `448.22` |
| `consecutive_losses` | `6` |
| `time_under_water` | `22260000.0` |
| `longest_recovery_duration` | `7407000.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `3.0` |
| `payoff_ratio` | `1.0104631608291321` |
| `avg_win` | `6.805144927536232` |
| `avg_loss` | `-6.734678899082569` |
| `long_count` | `192` |
| `short_count` | `55` |
| `long_expectancy` | `0.703125` |
| `short_expectancy` | `1.2732727272727273` |
| `mfe_mean` | `7.156437246963563` |
| `mfe_median` | `4.71` |
| `mfe_p90` | `16.662` |
| `mae_mean` | `5.978947368421053` |
| `mae_median` | `4.08` |
| `mae_p90` | `12.946000000000002` |
| `no_trade_rate` | `0.9501531133038449` |
| `hold_distribution` | `{'p50': 3.0, 'p90': 3.0}` |
| `loss_trade_mfe` | `3.508623853211009` |
| `realized_over_mfe` | `-2.3810219611015504` |
| `rule_pass_rates` | `{'long_signal_rate': 0.03895882953385505, 'short_signal_rate': 0.010888057162300102}` |
| `win_trade_mae` | `3.082536231884058` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0001 | completed | 2026-03-29 16:02:52 UTC | 41.01   | 247    | 11756 | 11756         | 0       
```

### 132. `05_optimization` / `05Q_thr_margin_diff_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05Q_thr_margin_diff_0001\experiment_bundle.json`
- experiment_id: `exp_05Q_thr_margin_diff_v1`
- bundle_status: `completed`
- latest_attempt: `att_0001`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-29T16:05:30.318531+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.535, long_threshold=0.4) | filters: combo_probability_gate(min_margin=0.07, min_probability_diff=0.0775) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=3)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `41.006` |
| `profit_factor` | `1.2793019834350479` |
| `trade_count` | `247` |
| `win_rate` | `0.5587044534412956` |
| `expectancy_per_trade` | `0.830080971659919` |
| `max_dd_pct` | `16.28071263654847` |
| `recovery_factor` | `2.1698592443644826` |
| `net_profit` | `205.03` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `16.28071263654847` |
| `equity_dd_amount` | `94.49000000000001` |
| `max_dd_pct` | `16.26003652779214` |
| `max_dd_amount` | `94.37` |
| `ulcer_index` | `2.4835112752310415` |
| `worst_day` | `-28.53` |
| `worst_week` | `-22.840000000000003` |
| `min_free_margin` | `448.22` |
| `consecutive_losses` | `6` |
| `time_under_water` | `22260000.0` |
| `longest_recovery_duration` | `7407000.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `3.0` |
| `payoff_ratio` | `1.0104631608291321` |
| `avg_win` | `6.805144927536232` |
| `avg_loss` | `-6.734678899082569` |
| `long_count` | `192` |
| `short_count` | `55` |
| `long_expectancy` | `0.703125` |
| `short_expectancy` | `1.2732727272727273` |
| `mfe_mean` | `7.156437246963563` |
| `mfe_median` | `4.71` |
| `mfe_p90` | `16.662` |
| `mae_mean` | `5.978947368421053` |
| `mae_median` | `4.08` |
| `mae_p90` | `12.946000000000002` |
| `no_trade_rate` | `0.9501531133038449` |
| `hold_distribution` | `{'p50': 3.0, 'p90': 3.0}` |
| `loss_trade_mfe` | `3.508623853211009` |
| `realized_over_mfe` | `-2.3810219611015504` |
| `rule_pass_rates` | `{'long_signal_rate': 0.03895882953385505, 'short_signal_rate': 0.010888057162300102}` |
| `win_trade_mae` | `3.082536231884058` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0001 | completed | 2026-03-29 16:05:30 UTC | 41.01   | 247    | 11756 | 11756         | 0       
```

### 133. `05_optimization` / `05CZ_mt5_validation_margin_pca_logreg_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05CZ_mt5_validation_margin_pca_logreg_0001\experiment_bundle.json`
- experiment_id: `exp_05cz_margin_pca_logreg_v1`
- bundle_status: `completed`
- latest_attempt: `att_0001`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-30T12:46:40.584353+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: max_probability_margin(min_margin=0.07) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=3)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `37.5` |
| `profit_factor` | `1.4009751716173735` |
| `trade_count` | `168` |
| `win_rate` | `0.5654761904761905` |
| `expectancy_per_trade` | `1.1160714285714286` |
| `max_dd_pct` | `21.304935332346698` |
| `recovery_factor` | `1.4157354273633345` |
| `net_profit` | `187.5` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `21.304935332346698` |
| `equity_dd_amount` | `132.44` |
| `max_dd_pct` | `19.319950706965887` |
| `max_dd_amount` | `119.15000000000003` |
| `ulcer_index` | `2.8959090066058604` |
| `worst_day` | `-74.81000000000002` |
| `worst_week` | `-17.28` |
| `min_free_margin` | `468.92` |
| `consecutive_losses` | `8` |
| `time_under_water` | `22927200.0` |
| `longest_recovery_duration` | `13243800.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `3.0` |
| `payoff_ratio` | `1.076538816084929` |
| `avg_win` | `6.895894736842106` |
| `avg_loss` | `-6.405616438356165` |
| `long_count` | `81` |
| `short_count` | `87` |
| `long_expectancy` | `0.9255555555555556` |
| `short_expectancy` | `1.293448275862069` |
| `mfe_mean` | `7.991428571428571` |
| `mfe_median` | `5.23` |
| `mfe_p90` | `17.352000000000004` |
| `mae_mean` | `6.500654761904761` |
| `mae_median` | `4.605` |
| `mae_p90` | `14.120000000000005` |
| `no_trade_rate` | `0.9695474651241919` |
| `hold_distribution` | `{'p50': 3.0, 'p90': 3.0}` |
| `loss_trade_mfe` | `4.768767123287671` |
| `realized_over_mfe` | `-2.5598990012560408` |
| `rule_pass_rates` | `{'long_signal_rate': 0.015821708063967335, 'short_signal_rate': 0.014630826811840763}` |
| `win_trade_mae` | `4.082631578947368` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0001 | completed | 2026-03-30 12:46:40 UTC | 37.50   | 168    | 11756 | 11756         | 0       
```

### 134. `05_optimization` / `05N_thr_margin_mix_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05N_thr_margin_mix_0001\experiment_bundle.json`
- experiment_id: `exp_05N_thr_margin_mix_v1`
- bundle_status: `completed`
- latest_attempt: `att_0001`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-29T16:01:33.608989+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.535, long_threshold=0.4) | filters: max_probability_margin(min_margin=0.07) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=3)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `35.614000000000004` |
| `profit_factor` | `1.2197065972436427` |
| `trade_count` | `278` |
| `win_rate` | `0.5431654676258992` |
| `expectancy_per_trade` | `0.6405395683453237` |
| `max_dd_pct` | `17.162` |
| `recovery_factor` | `1.9911662752991177` |
| `net_profit` | `178.07` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `17.162` |
| `equity_dd_amount` | `89.42999999999995` |
| `max_dd_pct` | `16.817999999999994` |
| `max_dd_amount` | `89.30999999999995` |
| `ulcer_index` | `6.025811095417065` |
| `worst_day` | `-25.980000000000004` |
| `worst_week` | `-22.840000000000003` |
| `min_free_margin` | `404.53` |
| `consecutive_losses` | `7` |
| `time_under_water` | `22387800.0` |
| `longest_recovery_duration` | `9150600.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `3.0` |
| `payoff_ratio` | `1.02584594602611` |
| `avg_win` | `6.546754966887417` |
| `avg_loss` | `-6.381811023622047` |
| `long_count` | `223` |
| `short_count` | `55` |
| `long_expectancy` | `0.47668161434977585` |
| `short_expectancy` | `1.3049090909090908` |
| `mfe_mean` | `6.793129496402877` |
| `mfe_median` | `4.4350000000000005` |
| `mfe_p90` | `14.802000000000008` |
| `mae_mean` | `5.939604316546763` |
| `mae_median` | `4.095000000000001` |
| `mae_p90` | `12.917000000000003` |
| `no_trade_rate` | `0.942752636951344` |
| `hold_distribution` | `{'p50': 3.0, 'p90': 3.0}` |
| `loss_trade_mfe` | `3.262204724409449` |
| `realized_over_mfe` | `-3.169495040356704` |
| `rule_pass_rates` | `{'long_signal_rate': 0.046019054100034026, 'short_signal_rate': 0.01122830894862198}` |
| `win_trade_mae` | `3.055099337748344` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0001 | completed | 2026-03-29 16:01:33 UTC | 35.61   | 278    | 11756 | 11756         | 0       
```

### 135. `02_individual_thresholds` / `02H_mt5_validation_baseline_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\02_individual_thresholds\02_runs\active\02H_mt5_validation_baseline_0001\experiment_bundle.json`
- experiment_id: `exp_stage02_threshold_validation_0001`
- bundle_status: `completed`
- latest_attempt: `att_0002`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-29T06:07:43.273554+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.535, long_threshold=0.4) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=3)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `32.397999999999996` |
| `profit_factor` | `1.0754477073193451` |
| `trade_count` | `878` |
| `win_rate` | `0.5136674259681093` |
| `expectancy_per_trade` | `0.18449886104783597` |
| `max_dd_pct` | `41.099931916181255` |
| `recovery_factor` | `0.7453984907049511` |
| `net_profit` | `161.98999999999998` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `41.099931916181255` |
| `equity_dd_amount` | `217.32` |
| `max_dd_pct` | `39.924359047456136` |
| `max_dd_amount` | `210.06999999999994` |
| `ulcer_index` | `9.391441650379699` |
| `worst_day` | `-83.82999999999998` |
| `worst_week` | `-44.58999999999996` |
| `min_free_margin` | `303.01` |
| `consecutive_losses` | `12` |
| `time_under_water` | `22321500.0` |
| `longest_recovery_duration` | `7950000.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `3.0` |
| `payoff_ratio` | `1.018217674113881` |
| `avg_win` | `5.1198226164079825` |
| `avg_loss` | `-5.028220140515223` |
| `long_count` | `838` |
| `short_count` | `40` |
| `long_expectancy` | `0.043281622911694496` |
| `short_expectancy` | `3.143` |
| `mfe_mean` | `5.106970387243736` |
| `mfe_median` | `3.76` |
| `mfe_p90` | `11.070000000000007` |
| `mae_mean` | `5.097061503416857` |
| `mae_median` | `3.7350000000000003` |
| `mae_p90` | `11.195000000000004` |
| `no_trade_rate` | `0.7676930928887377` |
| `hold_distribution` | `{'p50': 3.0, 'p90': 3.0}` |
| `loss_trade_mfe` | `2.520093676814988` |
| `realized_over_mfe` | `-7.055146965975255` |
| `rule_pass_rates` | `{'long_signal_rate': 0.22107859816264036, 'short_signal_rate': 0.01122830894862198}` |
| `win_trade_mae` | `2.6903769401330373` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0002 | completed | 2026-03-29 06:07:43 UTC | 32.40   | 878    | 11756 | 11756         | 0       
att_0001 | completed | 2026-03-28 18:59:05 UTC | 31.98   | 877    | 11696 | -             | -       
```

### 136. `05_optimization` / `05GA_05dp_riskpct050_atr14x15_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05GA_05dp_riskpct050_atr14x15_0001\experiment_bundle.json`
- experiment_id: `exp_05ga_05dp_riskpct050_atr14x15_v1`
- bundle_status: `completed`
- latest_attempt: `att_0002`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-31T15:06:09.183682+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: max_probability_margin(min_margin=0.0675) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=5)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `25.078` |
| `profit_factor` | `1.3111568812348007` |
| `trade_count` | `426` |
| `win_rate` | `0.49061032863849763` |
| `expectancy_per_trade` | `0.29434272300469483` |
| `max_dd_pct` | `6.559368812623734` |
| `recovery_factor` | `2.8673679396295513` |
| `net_profit` | `125.39` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `6.559368812623734` |
| `equity_dd_amount` | `43.729999999999905` |
| `max_dd_pct` | `6.5208258312327505` |
| `max_dd_amount` | `43.460000000000036` |
| `ulcer_index` | `3.5422659243200445` |
| `worst_day` | `-8.7` |
| `worst_week` | `-17.37` |
| `min_free_margin` | `479.15` |
| `consecutive_losses` | `8` |
| `time_under_water` | `22262700.0` |
| `longest_recovery_duration` | `13237500.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `4.269953051643192` |
| `payoff_ratio` | `1.3613447044399605` |
| `avg_win` | `2.5280861244019137` |
| `avg_loss` | `-1.8570506912442397` |
| `long_count` | `183` |
| `short_count` | `243` |
| `long_expectancy` | `0.5867213114754098` |
| `short_expectancy` | `0.07415637860082305` |
| `mfe_mean` | `2.3807981220657277` |
| `mfe_median` | `1.745` |
| `mfe_p90` | `5.5` |
| `mae_mean` | `1.543661971830986` |
| `mae_median` | `1.47` |
| `mae_p90` | `2.925` |
| `no_trade_rate` | `0.8937563797209935` |
| `hold_distribution` | `{'p50': 5.0, 'p90': 5.0}` |
| `loss_trade_mfe` | `1.1023041474654378` |
| `realized_over_mfe` | `-3.0489014221309225` |
| `rule_pass_rates` | `{'long_signal_rate': 0.04550867642055121, 'short_signal_rate': 0.06073494385845526}` |
| `win_trade_mae` | `0.8953588516746411` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `None` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `None` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': None, 'p90_points': None}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0002 | completed | 2026-03-31 15:06:09 UTC | 25.08   | 426    | 11756 | 11756         | 0       
att_0001 | failed    | 2026-03-31 15:00:37 UTC | -       | -      | -     | -             | -       
```

### 137. `05_optimization` / `05FN_ovr_proxy_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05FN_ovr_proxy_0001\experiment_bundle.json`
- experiment_id: `exp_05fn_ovr_proxy_v1`
- bundle_status: `completed`
- latest_attempt: `att_0004`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-31T13:51:41.920414+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: max_probability_margin(min_margin=0.0675) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=5)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `8.863999999999999` |
| `profit_factor` | `1.2002530272908005` |
| `trade_count` | `70` |
| `win_rate` | `0.5285714285714286` |
| `expectancy_per_trade` | `0.6331428571428571` |
| `max_dd_pct` | `9.720795592492308` |
| `recovery_factor` | `0.851488952929874` |
| `net_profit` | `44.32` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `9.720795592492308` |
| `equity_dd_amount` | `52.05000000000007` |
| `max_dd_pct` | `7.748000000000002` |
| `max_dd_amount` | `38.74000000000001` |
| `ulcer_index` | `3.4894793979792356` |
| `worst_day` | `-16.86` |
| `worst_week` | `-29.94` |
| `min_free_margin` | `449.36` |
| `consecutive_losses` | `4` |
| `time_under_water` | `21612300.0` |
| `longest_recovery_duration` | `5340000.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `5.0` |
| `payoff_ratio` | `1.0704959432593628` |
| `avg_win` | `7.179459459459459` |
| `avg_loss` | `-6.706666666666666` |
| `long_count` | `24` |
| `short_count` | `46` |
| `long_expectancy` | `0.7633333333333333` |
| `short_expectancy` | `0.5652173913043478` |
| `mfe_mean` | `7.494428571428571` |
| `mfe_median` | `6.17` |
| `mfe_p90` | `14.644` |
| `mae_mean` | `5.91` |
| `mae_median` | `4.14` |
| `mae_p90` | `16.514` |
| `no_trade_rate` | `0.9908982647158897` |
| `hold_distribution` | `{'p50': 5.0, 'p90': 5.0}` |
| `loss_trade_mfe` | `4.368181818181818` |
| `realized_over_mfe` | `-5.329864394791711` |
| `rule_pass_rates` | `{'long_signal_rate': 0.0024668254508336167, 'short_signal_rate': 0.006634909833276624}` |
| `win_trade_mae` | `2.684324324324324` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0004 | completed | 2026-03-31 13:51:41 UTC | 24.55   | 61     | 6755  | 6720          | 35      
att_0003 | completed | 2026-03-31 13:50:33 UTC | 8.86    | 70     | 11756 | 11756         | 0       
att_0002 | completed | 2026-03-31 13:48:38 UTC | 8.86    | 70     | 11756 | 11756         | 0       
att_0001 | completed | 2026-03-31 13:31:58 UTC | 8.86    | 70     | 11756 | 11756         | 0       
```

### 138. `05_optimization` / `05BV_frontier_stack_w_bb_bf_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05BV_frontier_stack_w_bb_bf_0001\experiment_bundle.json`
- experiment_id: `exp_05bv_frontier_stack_w_bb_bf_v1`
- bundle_status: `completed`
- latest_attempt: `att_0002`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-30T12:16:12.650475+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: max_probability_margin(min_margin=0.07) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=3)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `-11.846` |
| `profit_factor` | `0.9291625804291147` |
| `trade_count` | `270` |
| `win_rate` | `0.48518518518518516` |
| `expectancy_per_trade` | `-0.21937037037037035` |
| `max_dd_pct` | `27.60133240988093` |
| `recovery_factor` | `-0.35386545584896656` |
| `net_profit` | `-59.23` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `27.60133240988093` |
| `equity_dd_amount` | `167.37999999999994` |
| `max_dd_pct` | `27.31605158141222` |
| `max_dd_amount` | `165.64999999999998` |
| `ulcer_index` | `13.98716592895996` |
| `worst_day` | `-57.80999999999999` |
| `worst_week` | `-41.41` |
| `min_free_margin` | `426.76` |
| `consecutive_losses` | `7` |
| `time_under_water` | `23346000.0` |
| `longest_recovery_duration` | `15037200.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `3.0` |
| `payoff_ratio` | `0.9859053334324195` |
| `avg_win` | `5.9306106870229005` |
| `avg_loss` | `-6.015395683453237` |
| `long_count` | `120` |
| `short_count` | `150` |
| `long_expectancy` | `0.2704166666666667` |
| `short_expectancy` | `-0.6112000000000001` |
| `mfe_mean` | `5.87162962962963` |
| `mfe_median` | `4.15` |
| `mfe_p90` | `13.126999999999997` |
| `mae_mean` | `6.043777777777778` |
| `mae_median` | `4.195` |
| `mae_p90` | `12.437` |
| `no_trade_rate` | `0.9452194624021776` |
| `hold_distribution` | `{'p50': 3.0, 'p90': 3.0}` |
| `loss_trade_mfe` | `3.1345323741007194` |
| `realized_over_mfe` | `-6.847035765800915` |
| `rule_pass_rates` | `{'long_signal_rate': 0.026199387546784622, 'short_signal_rate': 0.028581150051037767}` |
| `win_trade_mae` | `3.077786259541985` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0002 | completed | 2026-03-30 12:16:12 UTC | 12.02   | 153    | 6755  | 6720          | 35      
att_0001 | completed | 2026-03-30 12:15:06 UTC | -11.85  | 270    | 11756 | 11756         | 0       
```

### 139. `05_optimization` / `05BW_frontier_stack_w_bb_ah_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05BW_frontier_stack_w_bb_ah_0001\experiment_bundle.json`
- experiment_id: `exp_05bw_frontier_stack_w_bb_ah_v1`
- bundle_status: `completed`
- latest_attempt: `att_0002`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-30T12:19:30.894800+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: max_probability_margin(min_margin=0.07) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=3)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `-16.9` |
| `profit_factor` | `0.9302471479751035` |
| `trade_count` | `416` |
| `win_rate` | `0.49038461538461536` |
| `expectancy_per_trade` | `-0.20312499999999997` |
| `max_dd_pct` | `30.366747344359286` |
| `recovery_factor` | `-0.46770354790502006` |
| `net_profit` | `-84.49999999999999` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `30.366747344359286` |
| `equity_dd_amount` | `180.67000000000002` |
| `max_dd_pct` | `29.895898361706802` |
| `max_dd_amount` | `177.19000000000005` |
| `ulcer_index` | `17.503502274186793` |
| `worst_day` | `-44.64999999999999` |
| `worst_week` | `-65.39` |
| `min_free_margin` | `402.0` |
| `consecutive_losses` | `9` |
| `time_under_water` | `23001600.0` |
| `longest_recovery_duration` | `14875200.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `3.0` |
| `payoff_ratio` | `0.9667274282878529` |
| `avg_win` | `5.524117647058824` |
| `avg_loss` | `-5.714245283018868` |
| `long_count` | `197` |
| `short_count` | `219` |
| `long_expectancy` | `0.1041116751269036` |
| `short_expectancy` | `-0.47949771689497717` |
| `mfe_mean` | `5.5520432692307695` |
| `mfe_median` | `3.875` |
| `mfe_p90` | `11.75` |
| `mae_mean` | `5.545649038461538` |
| `mae_median` | `3.66` |
| `mae_p90` | `12.370000000000001` |
| `no_trade_rate` | `0.9134909833276624` |
| `hold_distribution` | `{'p50': 3.0, 'p90': 3.0}` |
| `loss_trade_mfe` | `3.002924528301887` |
| `realized_over_mfe` | `-5.294410070396671` |
| `rule_pass_rates` | `{'long_signal_rate': 0.03929908132017693, 'short_signal_rate': 0.0472099353521606}` |
| `win_trade_mae` | `2.626666666666667` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0002 | completed | 2026-03-30 12:19:30 UTC | 33.58   | 247    | 6755  | 6720          | 35      
att_0001 | completed | 2026-03-30 12:18:25 UTC | -16.90  | 416    | 11756 | 11756         | 0       
```

### 140. `05_optimization` / `05BU_frontier_stack_w_bf_0001`

- run_bucket: `active`
- bundle_path: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05BU_frontier_stack_w_bf_0001\experiment_bundle.json`
- experiment_id: `exp_05bu_frontier_stack_w_bf_v1`
- bundle_status: `completed`
- latest_attempt: `att_0001`
- latest_attempt_status: `completed`
- latest_attempt_ended_at_utc: `2026-03-30T12:08:32.659525+00:00`
- rule_summary: `entry: threshold_entry(short_threshold=0.3333333333333333, long_threshold=0.3333333333333333) | filters: max_probability_margin(min_margin=0.07) | position: single_position_only(max_concurrent_positions=1) | exit: time_exit(max_hold_bars=3)`
- ready_rows: `11756` / `52809`
- expected_ready_rows: `11756`
- ready_row_gap: `0`
- contract_skip_count: `41052`
- startup_skip_count: `1`
- unexpected_skip_count: `0`

#### Headline

| Metric | Value |
|---|---|
| `return_pct` | `-20.889999999999997` |
| `profit_factor` | `0.8872955241918081` |
| `trade_count` | `301` |
| `win_rate` | `0.4850498338870432` |
| `expectancy_per_trade` | `-0.3470099667774086` |
| `max_dd_pct` | `30.07376786287018` |
| `recovery_factor` | `-0.6188529446616896` |
| `net_profit` | `-104.44999999999999` |

#### Risk

| Metric | Value |
|---|---|
| `equity_dd_pct` | `30.07376786287018` |
| `equity_dd_amount` | `168.78000000000003` |
| `max_dd_pct` | `29.049327354260086` |
| `max_dd_amount` | `161.95` |
| `ulcer_index` | `19.21976302925898` |
| `worst_day` | `-113.29999999999997` |
| `worst_week` | `-100.05999999999999` |
| `min_free_margin` | `381.54` |
| `consecutive_losses` | `7` |
| `time_under_water` | `22860000.0` |
| `longest_recovery_duration` | `15487200.0` |

#### Diagnostics

| Metric | Value |
|---|---|
| `avg_hold` | `3.0` |
| `payoff_ratio` | `0.9419918236282894` |
| `avg_win` | `5.632260273972603` |
| `avg_loss` | `-5.979096774193549` |
| `long_count` | `140` |
| `short_count` | `161` |
| `long_expectancy` | `-0.002285714285714245` |
| `short_expectancy` | `-0.6467701863354037` |
| `mfe_mean` | `5.718504983388704` |
| `mfe_median` | `3.91` |
| `mfe_p90` | `12.27` |
| `mae_mean` | `6.022491694352159` |
| `mae_median` | `4.15` |
| `mae_p90` | `13.33` |
| `no_trade_rate` | `0.9347567199727799` |
| `hold_distribution` | `{'p50': 3.0, 'p90': 3.0}` |
| `loss_trade_mfe` | `3.1835483870967742` |
| `realized_over_mfe` | `-6.266037983652475` |
| `rule_pass_rates` | `{'long_signal_rate': 0.029516842463422933, 'short_signal_rate': 0.03572643756379721}` |
| `win_trade_mae` | `2.978150684931507` |

#### Execution

| Metric | Value |
|---|---|
| `skip_rate` | `0.7773864303433127` |
| `external_mismatch_count` | `17350` |
| `fill_rate` | `1.0` |
| `avg_spread` | `135.09070423602037` |
| `avg_slippage` | `0.0` |
| `reject_count` | `0` |
| `data_readiness_failures` | `1` |
| `broker_constraint_events` | `0` |
| `next_tick_fill_distance` | `{'mean_points': 0.0, 'p90_points': 0.0}` |
| `runtime_warning_counts` | `{'HANDLE_NOT_READY_EMA9_-1': 1}` |
| `skip_reason_breakdown` | `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 8673, 'SESSION_CASH_OPEN_NOT_FOUND': 23702, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 5926, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 1204, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 1547}` |

#### Attempts

```text
Attempt  | Status    | EndedUTC                | Return% | Trades | Ready | ExpectedReady | ReadyGap
---------+-----------+-------------------------+---------+--------+-------+---------------+---------
att_0001 | completed | 2026-03-30 12:08:32 UTC | -20.89  | 301    | 11756 | 11756         | 0       
```
