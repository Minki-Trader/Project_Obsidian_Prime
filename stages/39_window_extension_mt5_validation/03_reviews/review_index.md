# Stage 39 Review Index

- latest extended validation review: `stage39_extended_validation_20260413.md`
- companion json: `stage39_extended_validation_20260413.json`
- latest-window feature-path correction review: `stage39_latest_window_feature_path_ab_correction_20260414.md`
- generator: `analyze_stage39_extended_validation.py`
- attempt chain:
  - `39A att_0001`: failed fast because the already-open GUI `terminal64.exe` ignored the scripted `/config:` launch and no shadow csv was written
  - `39A att_0002`: successful extended `34D` bridge run after rerunning with an exclusive terminal launch
  - `39B att_0001`: successful extended `34B` bridge run
  - `39A att_0003`: successful latest-window `34D` shadow audit run
  - `39A att_0007` / `att_0008`: genuine latest-window `34D` built-in versus contract-aligned feature-path replay
  - `39B att_0002`: mislabeled artifact; summary saved `false` for the feature-path flag but the actual tester ini used `true`
  - `39B att_0003`: valid latest-window `34B` contract-aligned replay
  - `39B att_0004`: corrective latest-window `34B` built-in replay
- read order:
  - `../00_spec/stage_brief.md`
  - `stage39_extended_validation_20260413.md`
  - `stage39_latest_window_feature_path_ab_correction_20260414.md`
  - `../04_selected/selection_status.md`
