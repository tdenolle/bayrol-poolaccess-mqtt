# Bayrol Poolaccess - MQTT Topics Reference

> **Note:** This document is generated from reverse engineering of the Bayrol Poolaccess MQTT protocol.
> Topics are addressed using the pattern: `d02/{serial}/{mode}/{topic_full}`
> where `mode` is `g` (get), `s` (set), or `v` (value).

---

## Table of Contents

- [Topic Types Overview](#topic-types-overview)
- [Type 1 – Device Status](#type-1--device-status)
- [Type 4 – Numeric Topics](#type-4--numeric-topics)
  - [pH Control](#ph-control)
  - [Redox / Chlorine (mV) Control](#redox--chlorine-mv-control)
  - [Salt Electrolysis](#salt-electrolysis)
  - [Temperature](#temperature)
  - [Pool Settings](#pool-settings)
  - [Calibration & Hardware](#calibration--hardware)
  - [Dosing Runtime Variables](#dosing-runtime-variables)
  - [System Readings & Variables](#system-readings--variables)
  - [Pump & Filtration Timers](#pump--filtration-timers)
  - [Output Timers (OUT1–OUT4)](#output-timers-out1out4)
  - [Light Programs](#light-programs)
  - [Heating Timers](#heating-timers)
  - [Smart Pump](#smart-pump)
  - [System Info & Internal](#system-info--internal)
- [Type 5 – Enum Topics](#type-5--enum-topics)
  - [General Settings](#general-settings)
  - [pH Dosing Enums](#ph-dosing-enums)
  - [Salt Electrolysis Enums](#salt-electrolysis-enums)
  - [Redox / Chlorine Dosing Enums](#redox--chlorine-dosing-enums)
  - [Operation Mode & Status](#operation-mode--status)
  - [Status Info & Alerts](#status-info--alerts)
  - [Pump & Filtration Enums](#pump--filtration-enums)
  - [Output Functions (OUT1–OUT4)](#output-functions-out1out4)
  - [Heating Enums](#heating-enums)
  - [Network & Connectivity](#network--connectivity)
  - [Device & System Enums](#device--system-enums)
  - [Internal / GUI Variables](#internal--gui-variables)
- [Type 6 – String Topics](#type-6--string-topics)

---

## Topic Types Overview

| Type | Description | Value Format |
|------|-------------|--------------|
| 1    | Device status | Coded value (e.g. `17.0`, `17.4`) |
| 4    | Numeric parameters & readings | Numeric value |
| 5    | Enumerated parameters & states | Coded value (e.g. `19.xx`) |
| 6    | String parameters | String value |

---

## Type 1 – Device Status

| Topic | Name | Description (EN) | Description (FR) |
|-------|------|-------------------|-------------------|
| `1.0` | `e_topic_device_status` | Device status | Statut appareil |

**Values:**

| Code | EN | FR |
|------|----|----|
| `17.0` | Device OFFLINE | Appareil HORS LIGNE |
| `17.4` | Device ONLINE | Appareil EN LIGNE |

---

## Type 4 – Numeric Topics

All numeric topics carry a numeric value.

### pH Control

| Topic | Name | Description (EN) | Description (FR) |
|-------|------|-------------------|-------------------|
| `4.2` | `e_num_ph_setpoint` | Desired pH level in the pool | Valeur de pH désirée dans la piscine |
| `4.3` | `e_num_ph_upper_limit` | Warning message if pH reading above | Message d'alerte si pH supérieur à |
| `4.4` | `e_num_ph_lower_limit` | Warning message if pH reading below | Message d'alerte si pH inférieur à |
| `4.5` | `e_num_ph_dos_time` | Time interval for automatic pH monitoring | Intervalle de temps de contrôle du dosage |
| `4.6` | `e_num_ph_in_pool` | pH measurement in the pool | — |
| `4.7` | `e_num_cal_ph_buffer_1` | pH value of the buffer solution | Valeur du pH de la solution tampon |
| `4.34` | `e_num_ph_dos_delta` | Approximation for automatic pH monitoring | Approche minimale pour contrôle du dosage |
| `4.38` | `e_num_ph_dos_cycle` | Dosing cycle (pump ON/OFF time) | Cycle de dosage de la pompe doseuse |
| `4.40` | `e_num_ph_base_p_range` | Base p-range pH (40m³ \| 2.2l/h \| normal) | Base bande prop. pH (40m³ \| 2.2l/h \| normal) |
| `4.42` | `e_num_ph_base_min_dos_rate` | Base min. dos. pH (40m³ \| 2.2l/h \| normal) | Base dos. min. pH (40m³ \| 2.2l/h \| normal) |
| `4.45` | `e_num_ph_man_dos_base_time` | Base man. dos. pH (10m³ \| 2,2l/h \| 0,1pH) | Base dos. man. pH (10m³ \| 2,2l/h \| 0,1pH) |
| `4.47` | `e_num_ph_dos_normal_per_cent` | Adjust 'normal' dosing amount (pH) | Vitesse de dosage de base (pH) |
| `4.78` | `e_num_var_ph` | pH | — |
| `4.79` | `e_num_var_ph_display` | Current pH reading | Valeur de pH actuelle |
| `4.80` | `e_num_var_ph_pool` | Pool measurement | Valeur piscine |
| `4.81` | `e_num_var_ph_buffer` | Buffer | — |
| `4.89` | `e_num_var_ph_dos_rate` | Dosing | Dosage |
| `4.96` | `e_num_var_ph_dos_monitoring_cycle` | Dos. time pH | Temps pH |
| `4.116` | `e_num_ph_manual_runtime_in_min` | Stop time-limited dosing after | Durée maximale du dosage manuel |
| `4.117` | `e_num_ph_manual_limit` | Stop time-limited dosing at a pH value of | Arrêter le dosage manuel à pH |
| `4.139` | `e_num_var_ph_pump_progress_in_s` | pH pump runtime progress | Temps de fonctionnement de la pompe pH |
| `4.140` | `e_num_var_ph_cal_progress_in_s` | Measurement in progress… | Mesure en cours… |
| `4.152` | `e_num_var_ph_manual_progress_in_min` | pH time-limited dosing progress | Dosage manuel pH |
| `4.153` | `e_num_var_ph_pause_progress_in_min` | pH pause elapsed time | Dosage pH en pause |
| `4.182` | `e_num_var_ph_minus` | pH-Minus | — |
| `4.183` | `e_num_var_ph_plus` | pH-Plus | — |
| `4.192` | `e_num_var_ph_0_01` | pH [0,01] | — |

### Redox / Chlorine (mV) Control

| Topic | Name | Description (EN) | Description (FR) |
|-------|------|-------------------|-------------------|
| `4.8` | `e_num_cl_setpoint` | Desired level of chlorine in the pool (DPD1) | Taux de chlore désiré dans la piscine |
| `4.9` | `e_num_cl_dpd` | Current level of chlorine in the pool (DPD1) | Taux de chlore mesuré dans la piscine (DPD1) |
| `4.12` | `e_num_add_cl_dos_time` | Start chlorine dosing for | Démarrer l'injection de chlore pendant |
| `4.13` | `e_num_man_dos_mv_time` | Duration of the manual dosing | Durée du dosage manuel |
| `4.14` | `e_num_man_dos_mv_delta` | Increase chlorine level by | — |
| `4.15` | `e_num_man_dos_ph_minus_time` | Duration of the manual dosing | Durée du dosage manuel |
| `4.16` | `e_num_man_dos_ph_minus_delta` | Reduce pH level by | — |
| `4.17` | `e_num_man_dos_ph_plus_time` | Duration of the manual dosing | Durée du dosage manuel |
| `4.18` | `e_num_man_dos_ph_plus_delta` | Increase pH level by | — |
| `4.26` | `e_num_mv_upper_limit` | Warning message if redox reading above | Message d'alerte si redox supérieur à |
| `4.27` | `e_num_mv_lower_limit` | Warning message if redox reading below | Message d'alerte si redox inférieur à |
| `4.28` | `e_num_mv_setpoint` | Setpoint for redox control | Valeur redox désirée dans la piscine |
| `4.29` | `e_num_mv_dos_time` | Time interval for redox monitoring | Intervalle de temps contrôle du redox |
| `4.30` | `e_num_mv_dos_delta` | Approximation for redox monitoring | Approche minimale pour contrôle du redox |
| `4.39` | `e_num_mv_dos_cycle` | Dosing cycle (pump ON/OFF time) | Cycle de dosage de la pompe doseuse |
| `4.44` | `e_num_mv_filtered` | Accept redox reading as setpoint | Utiliser la valeur redox comme consigne |
| `4.46` | `e_num_mv_man_dos_base_time_se` | Base man. dos. Cl (10m³ \| 13g/h \| 0,1mg/l) | Base dos. man. Cl (10m³ \| 13g/h \| 0,1mg/l) |
| `4.48` | `e_num_mv_dos_normal_per_cent_se` | Adjust 'normal' production level | Production de base |
| `4.82` | `e_num_var_mv_se` | Electrolysis | Electrolyse |
| `4.83` | `e_num_var_mv_display` | Current redox reading | Valeur redox actuelle |
| `4.84` | `e_num_var_mv_filtered` | Redox | — |
| `4.90` | `e_num_var_mv_dos_rate` | Dosing | Dosage |
| `4.97` | `e_num_var_mv_dos_monitoring_cycle` | Dos. time mV | Temps mV |
| `4.118` | `e_num_mv_switch_on_level` | Desired redox range \| minimum | Valeur redox désirée \| Minimum |
| `4.158` | `e_num_mv_deadzone` | Accepted drop of the redox reading (dead zone) | Zone morte redox (écart de mesure toléré) |
| `4.159` | `e_num_mv_stop_plus_limit` | Stop plus+ cycles if redox exceeds setpoint by | Arrêt des cycles plus+ (écart max mesure consigne) |
| `4.199` | `e_num_var_mv_manual_progress_in_min` | Time-limited dosing progress | Dosage manuel chlore |
| `4.200` | `e_num_var_mv_pause_progress_in_min` | Pause elapsed time | Dosage chlore en pause |
| `4.201` | `e_num_mv_manual_runtime_in_min` | Stop time-limited dosing after | Durée maximale du dosage manuel |
| `4.202` | `e_num_mv_manual_limit` | Stop time-limited dosing at a redox value of | Arrêter le dosage manuel à redox |
| `4.203` | `e_num_var_mv_pump_progress_in_s` | Chlorine pump runtime progress | Temps de fonctionnement de la pompe chlore |
| `4.204` | `e_num_var_mv` | Redox | — |
| `4.207` | `e_num_mv_base_p_range_cl` | Base p-range mV (40m³ \| 2.2l/h \| normal) | Base bande prop. mV (40m³ \| 2.2l/h \| normal) |
| `4.208` | `e_num_mv_base_min_dos_rate_cl` | Base min. dos. mV (40m³ \| 2.2l/h \| normal) | Base dos. min. mV (40m³ \| 2.2l/h \| normal) |
| `4.209` | `e_num_mv_dos_normal_per_cent_cl` | Adjust 'normal' dosing amount (redox) | Vitesse de dosage de base (redox) |
| `4.210` | `e_num_mv_man_dos_base_time_cl` | Base man. dos. Cl (10m³ \| 2,2l/h \| 0,1mg/l) | Base dos. man. Cl (10m³ \| 2,2l/h \| 0,1mg/l) |
| `4.189` | `e_num_ram_mv_mon_set_time_in_s` | Redox monitoring timer (setpoint) | — |
| `4.193` | `e_num_ram_mv_mon_rise_time_in_s` | Redox monitoring timer (rise) | — |
| `4.194` | `e_num_ram_mv_mon_set_active_time_in_s` | Redox monitoring active timer (setpoint) | — |
| `4.195` | `e_num_ram_mv_mon_rise_active_time_in_s` | Redox monitoring active timer | — |

### Salt Electrolysis

| Topic | Name | Description (EN) | Description (FR) |
|-------|------|-------------------|-------------------|
| `4.41` | `e_num_mv_base_p_range_se` | Base p-range mV (40m³ \| 13g/h \| normal) | Base bande prop. mV (40m³ \| 13g/h \| normal) |
| `4.43` | `e_num_mv_base_min_dos_rate_se_not_used` | Base min. dos. mV (40m³ \| 13g/h \| normal) | Base dos. min. mV (40m³ \| 13g/h \| normal) |
| `4.51` | `e_num_se_polarity_cycle` | Polarity change after | Temps d'inversion de polarité |
| `4.52` | `e_num_var_se_salt_warning_limit` | Salt level warning | Pré-alarme taux de sel bas |
| `4.53` | `e_num_var_se_salt_low_limit` | Cell protection mode, if salt level below | Protection cellule si sel inférieur à |
| `4.54` | `e_num_var_se_t_low_limit` | Cell protection mode, if temperature below | Protection cellule si température inférieure à |
| `4.64` | `e_num_se_test_power` | Production rate salt electrolysis | Production électrolyse de sel |
| `4.66` | `e_num_se_min_power` | Minimum production rate when ON | Production minimale |
| `4.75` | `e_num_se_constant_power` | Production rate in Constant mode | Production en mode constant |
| `4.77` | `e_num_se_manual_runtime_in_min` | Stop time-limited production after | Arrêt de la production après |
| `4.91` | `e_num_var_se_production_rate` | Production | — |
| `4.104` | `e_num_var_se_voltage` | Cell voltage | Tension cellule |
| `4.105` | `e_num_var_se_current` | Cell current | Courant cellule |
| `4.106` | `e_num_var_se_power` | Cell power | Puissance cellule |
| `4.108` | `e_num_var_se_test_cycle_rest_time` | Polarity reversal in | Inversion de polarité dans |
| `4.111` | `e_num_var_se_rest_time` | Stop production in | Arrêt production dans |
| `4.112` | `e_num_var_se_cycle_rest_time` | Next automatic polarity reversal in | Inversion de polarité dans |
| `4.114` | `e_num_max_current_5_plates` | Max. current 5-plates cell | Courant max. cellule 5 plaques |
| `4.115` | `e_num_max_current_7_plates` | Max. current 7-plates cell | Courant max. cellule 7 plaques |
| `4.119` | `e_num_ram_se_time_since_last_reversal_in_s` | Time since last polarity reversal | Temps depuis la dernière inversion de pol. |
| `4.120` | `e_num_ram_se_op_time_in_min` | Cell operating hours | Temps de production cellule |
| `4.121` | `e_num_ram_se_op_time_a_in_min` | Cell operating hours (polarity A) | Temps de production cellule (Pol. A) |
| `4.122` | `e_num_ram_se_op_time_b_in_min` | Cell operating hours (polarity B) | Temps de production cellule (Pol. B) |
| `4.125` | `e_num_se_plus_cl_delta_daily` | Chlorine increase by daily plus+ cycle | Production de chlore par cycle plus+ quotidien |
| `4.136` | `e_num_se_test_cycle_time_in_s` | Production time salt electrolysis | Temps de production électrolyse |
| `4.141` | `e_num_se_cover_factor` | Production rate factor when pool cover is closed | Coefficient de production avec volet fermé |
| `4.146` | `e_num_var_se_proposed_production_rate` | Recommended production rate | Production recommandée |
| `4.147` | `e_num_var_se_daily_production` | Estimated daily chlorine production | Production de chlore quotidienne estimée |
| `4.148` | `e_num_se_safe_mode_daily_production` | Desired daily chlorine production in safe mode | Production quotidienne en mode Safe |
| `4.149` | `e_num_se_manual_power` | Production rate | Production |
| `4.150` | `e_num_se_manual_limit` | Stop time-limited production at a redox value of | Arrêt de la production à la valeur redox de |
| `4.155` | `e_num_ram_se_boost_progress_in_min` | BOOST mode elapsed time | Temps écoulé mode BOOST |
| `4.156` | `e_num_var_se_manual_progress_in_min` | Time-limited production progress | Temps écoulé production manuelle |
| `4.157` | `e_num_var_se_pause_progress_in_min` | Salt electrolysis pause elapsed time | Electrolyse en pause |
| `4.162` | `e_num_se_plus_cl_delta_weekly` | Chlorine increase by weekly plus+ cycle | Production de chlore par cycle plus+ hebdomadaire |
| `4.165` | `e_num_var_se_t_off_limit` | Salt electrolysis switched off, if temperature below | Production arrêtée si température inférieure à |
| `4.166` | `e_num_var_se_salt_off_limit` | Salt electrolysis switched off, if salt level below | Production arrêtée si sel inférieur à |
| `4.173` | `e_num_average_production_rate` | Cell average production rate | — |
| `4.174` | `e_num_average_production_rate_5_plates` | Production rate 5-plates cell | — |
| `4.175` | `e_num_average_production_rate_7_plates` | Production rate 7-plates cell | — |
| `4.177` | `e_num_ram_se_op_time_x_power_a_in_min` | Cell weighted operating hours (pol. A) | Temps de production pondéré (Pol. A) |
| `4.178` | `e_num_ram_se_op_time_x_power_b_in_min` | Cell weighted operating hours (pol. B) | Temps de production pondéré (Pol. B) |
| `4.179` | `e_num_ram_se_plus_time_in_s` | Plus+ cycle timer | Timer cycle plus+ |
| `4.180` | `e_num_ram_se_polarity` | Current Polarity 0/1 | Polarité actuelle 0/1 |
| `4.188` | `e_num_var_se_op_time_x_power_in_min` | Cell weighted operating hours (time × %) | Temps de production pondéré (temps × %) |
| `4.196` | `e_num_var_se_desired_production_rate` | Production | — |
| `4.213` | `e_num_se_t_off_limit` | Salt electrolysis switched off, if temperature below | Production arrêtée si température inférieure à |

### Temperature

| Topic | Name | Description (EN) | Description (FR) |
|-------|------|-------------------|-------------------|
| `4.11` | `e_num_pool_temp` | Pool temperature | Température de la piscine |
| `4.49` | `e_num_cal_t_pool` | Pool temperature (thermometer) | Mesure de la température de l'eau |
| `4.98` | `e_num_var_t` | Temp. | — |
| `4.99` | `e_num_var_t_display` | Current temperature reading | Température actuelle |
| `4.123` | `e_num_t_set` | Desired temp. | T. désirée |
| `4.124` | `e_num_t_upper_limit` | — | — |
| `4.220` | `e_num_var_t_act` | Current temp. | Temp. actuelle |

### Pool Settings

| Topic | Name | Description (EN) | Description (FR) |
|-------|------|-------------------|-------------------|
| `4.10` | `e_num_pool_volume` | Pool volume | Volume de la piscine |
| `4.35` | `e_num_suction_runtime_in_min` | Desired pH pump runtime | Temps d'amorçage désiré |
| `4.36` | `e_num_rinse_time` | Rinse time | Temps de rinçage |
| `4.37` | `e_num_start_delay` | Start delay | Délai d'activation |
| `4.55` | `e_num_cal_salt_pool` | Real salt level in the pool | Taux de sel mesuré dans la piscine |
| `4.100` | `e_num_var_salt` | Salt | Sel |
| `4.101` | `e_num_var_salt_display` | Current salt level reading | Niveau de sel actuel |
| `4.102` | `e_num_var_cond` | Conductivity | Conductivité |
| `4.103` | `e_num_var_cond_display` | Current conductivity reading | Conductivité actuelle |
| `4.107` | `e_num_var_u_bat` | Internal battery voltage | Tension batterie interne |
| `4.113` | `e_num_logging_cycle` | Store logging data every | Enregistrer les données toutes les |
| `4.137` | `e_num_var_salt_level_in_pool` | Measured salt level in the pool | Taux de sel mesuré dans la piscine |
| `4.138` | `e_num_var_salt_to_add` | Amount of salt to add | Quantité de sel à ajouter |
| `4.143` | `e_num_daily_filter_time` | Daily filtration time | Temps de filtration quotidien |
| `4.144` | `e_num_salt_preferred_level` | Preferred salt level in the pool | Niveau de sel désiré dans la piscine |
| `4.145` | `e_num_var_min_daily_filter_time` | Recommended min. daily filtration time | Temps de filtration quotidien minimum recommandé |
| `4.160` | `e_num_display_on_level` | Display on level | — |
| `4.161` | `e_num_display_dim_level` | Display dimming level | — |
| `4.163` | `e_num_pool_volume_init` | Pool volume | Volume de la piscine |
| `4.164` | `e_num_salt_preferred_level_init` | Preferred salt level in the pool | Niveau de sel désiré dans la piscine |
| `4.167` | `e_num_var_din_flow` | Flow BNC | — |
| `4.168` | `e_num_var_din_level_ph` | Level pH | — |
| `4.169` | `e_num_var_din_cover` | Cover | — |
| `4.172` | `e_num_var_u_bat_overview` | Battery | — |
| `4.181` | `e_num_gas_detection_level` | Gas detection sensitivity | Sensibilité détection de gaz |
| `4.184` | `e_num_var_salt_block_ph` | Salt | Sel |
| `4.185` | `e_num_var_cond_block_ph` | Conductivity | Conductivité |
| `4.205` | `e_num_var_din_level_cl` | Level Cl | — |
| `4.206` | `e_num_var_din_flow_230` | Flow 230V~ | — |
| `4.212` | `e_num_var_no_of_messages` | No. of active messages | — |
| `4.304` | `e_num_var_fm_signal_strength` | Signal strength (must be at least 50%) | Puissance du signal (doit être d'au moins 50%) |

### Calibration & Hardware

| Topic | Name | Description (EN) | Description (FR) |
|-------|------|-------------------|-------------------|
| `4.19` | `e_num_hw_cal_offset_ph` | HW calibration pH offset | — |
| `4.20` | `e_num_hw_cal_factor_ph` | HW calibration pH factor | — |
| `4.21` | `e_num_cal_ph_offset` | pH calibration offset | Décalage du point zéro pH |
| `4.22` | `e_num_cal_ph_slope` | pH electrode slope | Pente de la sonde pH |
| `4.23` | `e_num_hw_cal_offset_mv` | HW calibration mV offset | — |
| `4.24` | `e_num_hw_cal_factor_mv` | HW calibration mV factor | — |
| `4.25` | `e_num_cal_mv_offset` | Redox calibration offset | Décalage du point zéro redox |
| `4.31` | `e_num_cal_mv_buffer` | Redox value of the buffer solution | Valeur redox de la solution tampon |
| `4.32` | `e_num_pump_capacity_ph` | Dosing capacity of the pH pump | Capacité de dosage de la pompe pH |
| `4.33` | `e_num_pump_capacity_mv` | Dosing capacity of the chlorine pump | Capacité de dosage de la pompe chlore |
| `4.56` | `e_num_cal_salt_offset` | Salt measurement calibration offset | — |
| `4.57` | `e_num_cal_cond_pool` | Conductivity in the pool (manual measurement) | Conductivité de l'eau (mesure manuelle) |
| `4.58` | `e_num_cal_cond_offset` | Conductivity calibration offset | Décalage du point zéro conductivité |
| `4.59` | `e_num_cal_t_offset` | Temperature calibration offset | Décalage du point zéro température |
| `4.60` | `e_num_hw_cal_offset_t` | HW calibration offset temperature | — |
| `4.61` | `e_num_hw_cal_factor_t` | HW calibration factor temperature | — |
| `4.62` | `e_num_hw_cal_offset_cond` | HW calibration offset conductivity | — |
| `4.63` | `e_num_hw_cal_factor_cond` | HW calibration factor conductivity | — |
| `4.142` | `e_num_var_mv_cal_progress_in_s` | Measurement in progress… | Mesure en cours… |
| `4.170` | `e_num_var_max_current_a` | Max. current A | — |
| `4.171` | `e_num_var_max_current_b` | Max. current B | — |
| `4.197` | `e_num_adc1_delta_old_new` | ADC1 correction from old to new config. | — |
| `4.198` | `e_num_adc1_cal_offset` | ADC1 calibration offset | — |
| `4.214` | `e_num_var_cond_u_adc` | Conductivity ADC voltage | — |
| `4.215` | `e_num_var_gas_alarm_set_limit` | Gas alarm if < | — |
| `4.216` | `e_num_var_gas_alarm_reset_limit` | Reset Gas alarm if > | — |
| `4.217` | `e_num_pump_capacity_ph_6l` | Dosing capacity of the pH pump | Capacité de dosage de la pompe pH |
| `4.218` | `e_num_pump_capacity_mv_6l` | Dosing capacity of the chlorine pump | Capacité de dosage de la pompe chlore |
| `4.219` | `e_num_hw_cal_offset_cond_correction_v1_60` | HW calibration offset conductivity v1.60 | — |

### Dosing Runtime Variables

| Topic | Name | Description (EN) | Description (FR) |
|-------|------|-------------------|-------------------|
| `4.85` | `e_num_var_add_cl_dos_rest_time` | Rem. time | Fin dos. |
| `4.86` | `e_num_var_man_dos_mv_rest_time` | Rem. time | Fin dos. |
| `4.87` | `e_num_var_man_dos_ph_minus_rest_time` | Rem. time | Fin dos. |
| `4.88` | `e_num_var_man_dos_ph_plus_rest_time` | Rem. time | Fin dos. |
| `4.92` | `e_num_var_delay_rest_time` | Start delay remaining time | Prêt en |
| `4.93` | `e_num_var_suction_rest_time` | Ready in | Prêt en |
| `4.94` | `e_num_var_rinse_rest_time` | Ready in | Prêt en |
| `4.95` | `e_num_var_add_cl_wait_rest_time` | Ready in | Prêt en |

### System Readings & Variables

| Topic | Name | Description (EN) | Description (FR) |
|-------|------|-------------------|-------------------|
| `4.67` | `e_num_sw_version` | — | — |
| `4.68` | `e_num_sw_date` | — | — |
| `4.109` | `e_num_var_sw_version` | Current software version | Version logiciel actuelle |
| `4.110` | `e_num_var_sw_date` | Current software date code | Code date logiciel actuel |
| `4.126` | `e_num_var_progress_percent` | Progress bar 0–100% | — |
| `4.127` | `e_num_var_progress_s` | Progress bar time in [s] | — |
| `4.128` | `e_num_var_progress_min` | Progress bar time in [min] | — |
| `4.176` | `e_num_ram_power_on_time_in_min` | Device total operating hours | Temps de fonctionnement total appareil |
| `4.186` | `e_num_var_last_power_off_duration_in_s` | Last power off duration | — |
| `4.187` | `e_num_ram_function_status` | — | — |
| `4.190` | `e_num_ram_timestamp_32_bit_lower` | Timestamp lower 16 bits | — |
| `4.191` | `e_num_ram_timestamp_32_bit_upper` | Timestamp upper 16 bits | — |
| `4.211` | `e_num_var_no_of_eventlog_events` | — | — |
| `4.239` | `e_num_var_rssi_from_client` | RSSI signal strength (from Control Module) | RSSI du Control Module |
| `4.240` | `e_num_rtc_utc_offset_in_s` | Local time = UTC + this offset | — |

### Date & Time

| Topic | Name | Description (EN) |
|-------|------|-------------------|
| `4.69` | `e_num_time_h` | time.hours |
| `4.70` | `e_num_time_min` | time.minutes |
| `4.71` | `e_num_time_s` | time.seconds |
| `4.72` | `e_num_date_d` | date.day |
| `4.73` | `e_num_date_m` | date.month |
| `4.74` | `e_num_date_y` | date.year |

### Access Level

| Topic | Name | Description (EN) |
|-------|------|-------------------|
| `4.129` | `e_num_guest_guest` | View = guest \| edit = guest |
| `4.130` | `e_num_guest_user` | View = guest \| edit = user |
| `4.131` | `e_num_user_user` | View = user \| edit = user |
| `4.132` | `e_num_user_service` | View = user \| edit = service |
| `4.133` | `e_num_customer_iel` | View, edit = customer_iel |
| `4.134` | `e_num_var_guest` | var: view = guest |
| `4.135` | `e_num_var_user` | var: view = user |
| `4.151` | `e_num_invisible` | This item should be invisible |

### Pump & Filtration Timers

| Topic | Name | Description (EN) | Description (FR) |
|-------|------|-------------------|-------------------|
| `4.221` | `e_num_pump_clock_timer1_start_time` | Start time | Heure de démarrage |
| `4.222` | `e_num_pump_clock_timer1_stop_time` | Stop time | Temps d'arrêt |
| `4.223` | `e_num_pump_clock_timer1_weekdays` | Days of week | Jours |
| `4.224` | `e_num_pump_clock_timer2_start_time` | Start time | Heure de démarrage |
| `4.225` | `e_num_pump_clock_timer2_stop_time` | Stop time | Temps d'arrêt |
| `4.226` | `e_num_pump_clock_timer2_weekdays` | Days of week | Jours |
| `4.227` | `e_num_pump_clock_timer3_start_time` | Start time | Heure de démarrage |
| `4.228` | `e_num_pump_clock_timer3_stop_time` | Stop time | Temps d'arrêt |
| `4.229` | `e_num_pump_clock_timer3_weekdays` | Days of week | Jours |

### Output Timers (OUT1–OUT4)

<details>
<summary>OUT1 Timers</summary>

| Topic | Name | Description (EN) | Description (FR) |
|-------|------|-------------------|-------------------|
| `4.230` | `e_num_out1_clock_timer1_start_time` | Start time | Heure de démarrage |
| `4.231` | `e_num_out1_clock_timer1_stop_time` | Stop time | Temps d'arrêt |
| `4.232` | `e_num_out1_clock_timer1_weekdays` | Days of week | Jours |
| `4.233` | `e_num_out1_clock_timer2_start_time` | Start time | Heure de démarrage |
| `4.234` | `e_num_out1_clock_timer2_stop_time` | Stop time | Temps d'arrêt |
| `4.235` | `e_num_out1_clock_timer2_weekdays` | Days of week | Jours |
| `4.236` | `e_num_out1_clock_timer3_start_time` | Start time | Heure de démarrage |
| `4.237` | `e_num_out1_clock_timer3_stop_time` | Stop time | Temps d'arrêt |
| `4.238` | `e_num_out1_clock_timer3_weekdays` | Days of week | Jours |

</details>

<details>
<summary>OUT2 Timers</summary>

| Topic | Name | Description (EN) | Description (FR) |
|-------|------|-------------------|-------------------|
| `4.241` | `e_num_out2_clock_timer1_start_time` | Start time | Heure de démarrage |
| `4.242` | `e_num_out2_clock_timer1_stop_time` | Stop time | — |
| `4.243` | `e_num_out2_clock_timer1_weekdays` | Days of week | Jours |
| `4.244` | `e_num_out2_clock_timer2_start_time` | Start time | Heure de démarrage |
| `4.245` | `e_num_out2_clock_timer2_stop_time` | Stop time | Temps d'arrêt |
| `4.246` | `e_num_out2_clock_timer2_weekdays` | Days of week | Jours |
| `4.247` | `e_num_out2_clock_timer3_start_time` | Start time | Heure de démarrage |
| `4.248` | `e_num_out2_clock_timer3_stop_time` | Stop time | Temps d'arrêt |
| `4.249` | `e_num_out2_clock_timer3_weekdays` | Days of week | Jours |

</details>

<details>
<summary>OUT3 Timers</summary>

| Topic | Name | Description (EN) | Description (FR) |
|-------|------|-------------------|-------------------|
| `4.250` | `e_num_out3_clock_timer1_start_time` | Start time | Heure de démarrage |
| `4.251` | `e_num_out3_clock_timer1_stop_time` | Stop time | Temps d'arrêt |
| `4.252` | `e_num_out3_clock_timer1_weekdays` | Days of week | Jours |
| `4.253` | `e_num_out3_clock_timer2_start_time` | Start time | Heure de démarrage |
| `4.254` | `e_num_out3_clock_timer2_stop_time` | Stop time | Temps d'arrêt |
| `4.255` | `e_num_out3_clock_timer2_weekdays` | Days of week | Jours |
| `4.256` | `e_num_out3_clock_timer3_start_time` | Start time | Heure de démarrage |
| `4.257` | `e_num_out3_clock_timer3_stop_time` | Stop time | Temps d'arrêt |
| `4.258` | `e_num_out3_clock_timer3_weekdays` | Days of week | Jours |

</details>

<details>
<summary>OUT4 Timers</summary>

| Topic | Name | Description (EN) | Description (FR) |
|-------|------|-------------------|-------------------|
| `4.259` | `e_num_out4_clock_timer1_start_time` | Start time | Heure de démarrage |
| `4.260` | `e_num_out4_clock_timer1_stop_time` | Stop time | Temps d'arrêt |
| `4.261` | `e_num_out4_clock_timer1_weekdays` | Days of week | Jours |
| `4.262` | `e_num_out4_clock_timer2_start_time` | Start time | Heure de démarrage |
| `4.263` | `e_num_out4_clock_timer2_stop_time` | Stop time | Temps d'arrêt |
| `4.264` | `e_num_out4_clock_timer2_weekdays` | Days of week | Jours |
| `4.265` | `e_num_out4_clock_timer3_start_time` | Start time | Heure de démarrage |
| `4.266` | `e_num_out4_clock_timer3_stop_time` | Stop time | Temps d'arrêt |
| `4.267` | `e_num_out4_clock_timer3_weekdays` | Days of week | Jours |

</details>

### Light Programs

| Topic | Name | Description (EN) | Description (FR) |
|-------|------|-------------------|-------------------|
| `4.268` | `e_num_out1_clock_timer1_light_program` | Light program | Programme éclairage |
| `4.269` | `e_num_out1_clock_timer2_light_program` | Light program | Programme éclairage |
| `4.270` | `e_num_out1_clock_timer3_light_program` | Light program | Programme éclairage |
| `4.271` | `e_num_out2_clock_timer1_light_program` | Light program | Programme éclairage |
| `4.272` | `e_num_out2_clock_timer2_light_program` | Light program | Programme éclairage |
| `4.273` | `e_num_out2_clock_timer3_light_program` | Light program | Programme éclairage |
| `4.274` | `e_num_out3_clock_timer1_light_program` | Light program | Programme éclairage |
| `4.275` | `e_num_out3_clock_timer2_light_program` | Light program | Programme éclairage |
| `4.276` | `e_num_out3_clock_timer3_light_program` | Light program | Programme éclairage |
| `4.277` | `e_num_out4_clock_timer1_light_program` | Light program | Programme éclairage |
| `4.278` | `e_num_out4_clock_timer2_light_program` | Light program | Programme éclairage |
| `4.279` | `e_num_out4_clock_timer3_light_program` | Light program | Programme éclairage |
| `4.280` | `e_num_out1_light_reset_on_time` | Program RESET ON time | Temps ON réinitialisation programme |
| `4.281` | `e_num_out1_light_reset_off_time` | Program RESET OFF time | Temps OFF réinitialisation programme |
| `4.282` | `e_num_out1_light_next_program_on_time` | NEXT program ON time | Temps ON programme suivant |
| `4.283` | `e_num_out1_light_next_program_off_time` | NEXT program OFF time | Temps OFF programme suivant |
| `4.284` – `4.295` | `e_num_out{2-4}_light_*` | Same pattern for OUT2, OUT3, OUT4 | — |
| `4.305` | `e_num_out1_manual_light_program` | Test light program | Tester programme éclairage |
| `4.306` | `e_num_out2_manual_light_program` | Test light program | Tester programme éclairage |
| `4.307` | `e_num_out3_manual_light_program` | Test light program | Tester programme éclairage |
| `4.308` | `e_num_out4_manual_light_program` | Test light program | Tester programme éclairage |

### Heating Timers

| Topic | Name | Description (EN) | Description (FR) |
|-------|------|-------------------|-------------------|
| `4.296` | `e_num_heating_hysteresis` | Accepted deviation (hysteresis) | Écart accepté (hystérésis) |
| `4.297` | `e_num_frost_protection_temp` | Activate frost protection if water temp. below | Activer le mode Hors Gel si la temp. est inférieure à |
| `4.298` | `e_num_frost_protection_hysteresis` | Accepted deviation (hysteresis) | Écart accepté (hystérésis) |
| `4.299` | `e_num_frost_protection_min_runtime` | Min. pump runtime in frost protection | Temps de filtration min. en mode Hors Gel |
| `4.309` | `e_num_heating_clock_timer1_start_time` | Blocking start time | Début du blocage |
| `4.310` | `e_num_heating_clock_timer1_stop_time` | Blocking stop time | Fin du blocage |
| `4.311` | `e_num_heating_clock_timer1_weekdays` | Days of week | Jours |
| `4.312` | `e_num_heating_clock_timer2_start_time` | Blocking start time | Début du blocage |
| `4.313` | `e_num_heating_clock_timer2_stop_time` | Blocking stop time | Fin du blocage |
| `4.314` | `e_num_heating_clock_timer2_weekdays` | Days of week | Jours |
| `4.315` | `e_num_heating_clock_timer3_start_time` | Blocking start time | Début du blocage |
| `4.316` | `e_num_heating_clock_timer3_stop_time` | Blocking stop time | Fin du blocage |
| `4.317` | `e_num_heating_clock_timer3_weekdays` | Days of week | Jours |

### Smart Pump

| Topic | Name | Description (EN) | Description (FR) |
|-------|------|-------------------|-------------------|
| `4.300` | `e_num_pump_smart_start_time` | Pump start time in Smart mode | Heure de démarrage filtration en mode Smart |
| `4.301` | `e_num_pump_smart_runtime_T_30` | Daily pump runtime at 30°C [hh:mm] | Temps de filtration quotidien à 30°C [hh:mm] |
| `4.302` | `e_num_pump_smart_runtime_T_12` | Daily pump runtime at 12°C [hh:mm] | Temps de filtration quotidien à 12°C [hh:mm] |
| `4.303` | `e_num_pump_winter_runtime` | Daily pump runtime in winter mode (< 12°C) [hh:mm] | Temps de filtration quotidien en mode Hiver (<12°C) |
| `4.318` | `e_num_ram_pump_smart_runtime_in_s` | — | — |
| `4.319` | `e_num_pump_smart_date_code` | — | — |
| `4.320` | `e_num_var_pump_smart_planned_runtime` | Planned runtime today (Smart mode) | Temps de fonc. prévue aujourd'hui (mode Smart) |
| `4.321` | `e_num_var_pump_smart_expired_runtime` | Actual runtime today | Temps de fonctionnement passé aujourd'hui |
| `4.322` | `e_num_var_pump_smart_t_average` | Average temperature | Température moyenne |

---

## Type 5 – Enum Topics

Enum topics use coded values (format `19.xx`). Below are the topics grouped by category, with their possible values.

### General Settings

#### `5.2` – `e_enum_language` — Menu language

| Code | EN | FR |
|------|----|----|
| `19.19` | Deutsch | — |
| `19.20` | English | — |
| `19.21` | Français | — |
| `19.22` | Español | — |

#### `5.7` – `e_enum_default_set` — Regional standard settings

| Code | EN | FR |
|------|----|----|
| `19.33` | Deutschland | Allemagne |
| `19.36` | Italia | Italie |
| `19.37` | Europe | — |

#### `5.9` – `e_enum_alarm_sound` — Acoustic alarm signal in case of messages

| Code | EN | FR |
|------|----|----|
| `19.17` | Yes | Oui |
| `19.18` | No | Non |

#### `5.14` – `e_enum_welcome_y_n` — Run commissioning wizard at next system start

Yes (`19.17`) / No (`19.18`)

#### `5.16` – `e_enum_demo_mode` — Simulate measurement readings

Yes (`19.17`) / No (`19.208`)

#### `5.52` – `e_enum_show_circulation` — Show filtration on/off

Yes (`19.17`) / No (`19.18`)

#### `5.53` – `e_enum_show_alarms` — Show alarms

Yes (`19.17`) / No (`19.18`)

#### `5.54` – `e_enum_show_calibrations` — Show calibrations

Yes (`19.17`) / No (`19.18`)

#### `5.55` – `e_enum_show_settings` — Show user input (parameter settings)

Yes (`19.17`) / No (`19.18`)

#### `5.56` – `e_enum_show_others` — Show other events

Yes (`19.17`) / No (`19.18`)

#### `5.57` – `e_enum_simulate_message` — Simulate Safe Mode / Stopped messages

Yes (`19.17`) / No (`19.18`)

#### `5.90` – `e_enum_context_menu_login` — Login for context menus

Yes (`19.17`) / No (`19.18`)

#### `5.91` – `e_enum_auto_login` — Activate auto login

Yes (`19.17`) / No (`19.18`)

#### `5.107` – `e_enum_auto_login_level` — Auto login user level

| Code | EN | FR |
|------|----|----|
| `19.200` | Guest (viewing only) | Invité (visualisation uniquement) |
| `19.201` | User (limited access) | Utilisateur (accès limité) |
| `19.202` | Service (full access) | Service (accès complet) |

#### `5.115` – `e_enum_auto_summer_winter_time` — Automatic summer/winter time changeover

Yes (`19.17`) / No (`19.18`)

#### `5.148` – `e_enum_activate_logging` — Activate data logging on USB stick

Yes (`19.17`) / No (`19.18`)

#### `5.240` – `e_enum_touch_beep_on_off` — Touch beep

ON (`19.54`) / OFF (`19.55`)

#### `5.241` – `e_enum_ntp_sync_on_off` — Synchronize time with Web

ON (`19.54`) / OFF (`19.55`)

### pH Dosing Enums

#### `5.3` – `e_enum_ph_dos_amount` — Adjust pH dosing amount

| Code | EN | FR |
|------|----|----|
| `19.3` | quarter | Multipl. 0,25 |
| `19.4` | half | Multipl. 0,5 |
| `19.5` | 0,75-fold | Multipl. 0,75 |
| `19.6` | normal | — |
| `19.7` | 1,25-fold | Multipl. 1,25 |
| `19.8` | 1,5-fold | Multipl. 1,5 |
| `19.9` | double | Multipl. 2 |
| `19.10` | triple | Multipl. 3 |
| `19.81` | 5-fold | Multipl. 5 |
| `19.82` | 10-fold | Multipl. 10 |

> Same value set applies to: `5.4` (`e_enum_ph_increase_dosing`)

#### `5.8` – `e_enum_ph_dos_dir` — Product used for pH dosing

| Code | EN | FR |
|------|----|----|
| `19.38` | pH-Minus (acid) | pH-Minus (acide) |
| `19.39` | pH-Plus (dye) | pH-Plus (base) |

#### `5.42` – `e_enum_ph_on_off` — Automatic pH dosing ON/OFF

Yes (`19.17`) / No (`19.18`)

#### `5.58` – `e_enum_run_ph_pump` — Switch on pH pump for 1 minute

Yes (`19.17`) / No (`19.18`)

#### `5.59` – `e_enum_ph_pause_runtime` — Pause pH dosing for

| Code | EN | FR |
|------|----|----|
| `19.123` | 1 hour | 1 heure |
| `19.124` | 2 hours | 2 heures |
| `19.125` | 4 hours | 4 heures |
| `19.126` | 8 hours | 8 heures |
| `19.127` | 12 hours | 12 heures |
| `19.128` | 24 hours | 24 heures |
| `19.129` | 48 hours | 48 heures |

#### `5.95` – `e_enum_ph_safety` — If a pH problem is detected

| Code | EN | FR |
|------|----|----|
| `19.187` | stop dosing | Arrêter le dosage |
| `19.188` | continue dosing | Continuer le dosage |

#### `5.102` – `e_enum_ph_run_suction` — Run pH pump for the selected time

Yes (`19.17`) / No (`19.18`)

#### `5.103` – `e_enum_ph_cal_method` — Pool measurement or buffer solution?

| Code | EN | FR |
|------|----|----|
| `19.193` | Pool measurement | Mesure dans la piscine |
| `19.194` | pH 7 buffer | Solution tampon pH7 |

#### `5.108` – `e_enum_ph_activate_manual_gui` — Activate time-limited pH dosing

Yes (`19.17`)

#### `5.109` – `e_enum_ph_activate_pause_gui` — Pause pH dosing

Yes (`19.17`) / No (`19.18`)

#### `5.110` – `e_enum_ph_manual_stop_at_setpoint` — Stop dosing when setpoint is reached

Yes (`19.17`)

### Salt Electrolysis Enums

#### `5.5` – `e_enum_se_production_level` — Adjust salt electrolysis production level

Same value set as `e_enum_ph_dos_amount` (quarter → 10-fold).

> Same value set applies to: `5.6` (`e_enum_se_increase_production`)

#### `5.40` – `e_enum_se_on_off` — Salt electrolysis ON/OFF

Yes (`19.17`) / No (`19.18`)

#### `5.41` – `e_enum_se_opmode` — Salt electrolysis operating mode

| Code | EN | FR |
|------|----|----|
| `19.195` | Auto (redox control) | Auto (contrôle redox) |
| `19.115` | Auto plus+ | — |
| `19.106` | Constant mode | Production constante |

#### `5.43` – `e_enum_se_cell_type` — Connected cell type

| Code | EN | FR |
|------|----|----|
| `19.109` | Automatic identification | Identification automatique |
| `19.97` | no cell | Pas de cellule |
| `19.98` | 5 plates cell | Cellule 5 plaques |
| `19.99` | 7 plates cell | Cellule 7 plaques |
| `19.178` | Final production test | Test appareil |

#### `5.49` – `e_enum_se_auto_plus_days` — Day of week for the weekly plus+ cycle

| Code | EN | FR |
|------|----|----|
| `19.116` | Monday | Lundi |
| `19.117` | Tuesday | Mardi |
| `19.118` | Wednesday | Mercredi |
| `19.119` | Thursday | Jeudi |
| `19.120` | Friday | Vendredi |
| `19.121` | Saturday | Samedi |
| `19.122` | Sunday | Dimanche |

#### `5.50` – `e_enum_se_stop_if_temp_low` — Stop salt electrolysis if temperature low

Yes (`19.17`) / No (`19.18`)

#### `5.51` – `e_enum_se_stop_if_salt_low` — Stop electrolysis if salt level low

Yes (`19.17`) / No (`19.18`)

#### `5.60` – `e_enum_se_pause_runtime` — Pause salt electrolysis for

Same value set as `e_enum_ph_pause_runtime` (1h → 48h).

#### `5.61` – `e_enum_also_pause_ph` — Pause pH dosing also

Yes (`19.17`) / No (`19.18`)

#### `5.62` – `e_enum_also_pause_se` — Pause salt electrolysis also

Yes (`19.17`) / No (`19.18`)

#### `5.63` – `e_enum_se_boost_runtime` — Duration of BOOST mode

| Code | EN | FR |
|------|----|----|
| `19.123` | 1 hour | 1 heure |
| `19.125` | 4 hours | 4 heures |
| `19.127` | 12 hours | 12 heures |
| `19.128` | 24 hours | 24 heures |
| `19.129` | 48 hours | 48 heures |
| `19.130` | 72 hours | 72 heures |

#### `5.89` – `e_enum_run_se` — Switch on salt electrolysis

Yes (`19.17`) / No (`19.18`)

#### `5.94` – `e_enum_se_safety` — If a redox problem is detected

| Code | EN | FR |
|------|----|----|
| `19.184` | activate Safe Mode | Activer le mode Safe |
| `19.185` | stop production | Arrêter la production |
| `19.186` | continue production | Continuer production |

> Same value set applies to: `5.113` (`e_enum_se_safety_without_continue`)

#### `5.96` – `e_enum_mv_setpoint_max_time` — Redox setpoint monitoring

| Code | EN | FR |
|------|----|----|
| `19.189` | 1 day | 1 jour |
| `19.190` | 2 days | 2 jours |
| `19.191` | 3 days | 3 jours |

> Same value set applies to: `5.97` (`e_enum_mv_reaction_max_time`)

#### `5.99` – `e_enum_salt_use_add_salt_wizard` — Activate 'Add salt' wizard

Yes (`19.17`) / No (`19.18`)

#### `5.100` – `e_enum_se_plus_cycles_per_week` — Daily or weekly plus+ cycles

| Code | EN | FR |
|------|----|----|
| `19.203` | weekly plus+ cycles | 1 cycle plus+ par semaine |
| `19.205` | daily plus+ cycles | Cycles plus+ quotidiens |

#### `5.101` – `e_enum_se_plus_x7` — Additional plus+ cycles every day

Yes (`19.17`) / No (`19.18`)

#### `5.104` – `e_enum_se_activate_boost_gui` — Activate BOOST mode

Yes (`19.17`)

#### `5.105` – `e_enum_se_activate_manual_gui` — Activate time-limited constant production

Yes (`19.17`) / No (`19.18`)

#### `5.106` – `e_enum_se_activate_pause_gui` — Pause salt electrolysis

Yes (`19.17`) / No (`19.18`)

#### `5.111` – `e_enum_se_manual_stop_at_setpoint` — Stop production when setpoint is reached

Yes (`19.17`)

#### `5.112` – `e_enum_se_never_stop_plus` — Never stop plus+ cycles (not recommended)

Yes (`19.17`) / No (`19.18`)

#### `5.116` – `e_enum_salt_pre_warning` — Show info message when salt level drops

Yes (`19.17`) / No (`19.208`)

### Redox / Chlorine Dosing Enums

#### `5.154` – `e_enum_mv_on_off` — Automatic chlorine dosing ON/OFF

Yes (`19.17`) / No (`19.18`)

#### `5.155` – `e_enum_mv_activate_manual_gui` — Activate time-limited chlorine dosing

Yes (`19.17`) / No (`19.18`)

#### `5.157` – `e_enum_mv_activate_pause_gui` — Pause chlorine dosing

Yes (`19.17`) / No (`19.18`)

#### `5.159` – `e_enum_mv_run_suction` — Run chlorine pump for the selected time

Yes (`19.17`) / No (`19.18`)

#### `5.160` – `e_enum_mv_pause_runtime` — Pause chlorine dosing for

Same value set as `e_enum_ph_pause_runtime` (1h → 48h).

#### `5.161` – `e_enum_also_pause_mv` — Pause chlorine dosing also

Yes (`19.17`) / No (`19.18`)

#### `5.164` – `e_enum_run_mv_pump` — Switch on chlorine pump for 1 minute

Yes (`19.17`) / No (`19.18`)

#### `5.175` – `e_enum_mv_dos_amount` — Adjust chlorine dosing amount

Same value set as `e_enum_ph_dos_amount` (quarter → 10-fold).

### Operation Mode & Status

#### `5.20` – `e_enum_opmode` — Automatic operation

| Code | EN | FR |
|------|----|----|
| `19.100` | OFF | — |
| `19.101` | Auto | — |
| `19.102` | pH AUTO SE (redox) OFF | pH Auto Electrolyse (mV) Off |
| `19.103` | pH OFF SE (redox) AUTO | pH Off Electrolyse (mV) Auto |

#### `5.21` – `e_enum_se_manual_continuous` — Continuous operation

Yes (`19.17`) / No (`19.18`)

#### `5.17` – `e_enum_se_polarity` — Polarity

| Code | Value |
|------|-------|
| `19.89` | A |
| `19.90` | B |
| `19.55` | OFF |

#### `5.34` – `e_enum_var_se_mode` — Polarity (variable)

| Code | EN | FR |
|------|----|----|
| `19.55` | OFF | — |
| `19.110` | A (Automatic) | A (Automatique) |
| `19.111` | B (Automatic) | B (Automatique) |
| `19.112` | A (Manual) | A (Manuel) |
| `19.113` | B (Manual) | B (Manuel) |

#### `5.35` – `e_enum_var_se_cell_type` — Identified connected cell type

| Code | EN | FR |
|------|----|----|
| `19.97` | no cell | Pas de cellule |
| `19.98` | 5 plates cell | Cellule 5 plaques |
| `19.99` | 7 plates cell | Cellule 7 plaques |
| `19.178` | Final production test | Test appareil |

### Status Info & Alerts

#### `5.45` – `e_enum_var_ph_status_info` — pH status info

| Code | EN | FR |
|------|----|----|
| `19.157` | Stopped (pH error) | Arrêt (erreur mesure pH) |
| `19.159` | pH-Minus canister empty | Bidon pH-Minus vide |
| `19.160` | pH-Plus Canister empty | Bidon pH-Plus vide |
| `19.161` | pH too high | pH trop haut |
| `19.162` | pH too low | pH trop bas |
| `19.171` | Start delay | Délai de démarrage |

#### `5.46` – `e_enum_var_se_status_info` — Salt electrolysis status info

| Code | EN | FR |
|------|----|----|
| `19.147` | Stopped (gas detected) | Arrêt (gaz détecté) |
| `19.149` | Stopped (redox error) | Arrêt (erreur redox) |
| `19.151` | Stopped (low salt) | Arrêt (sel bas) |
| `19.153` | Stopped (low temp.) | Arrêt (temp. basse) |
| `19.155` | Safe mode (redox error) | Mode Safe (erreur redox) |
| `19.163` | Redox too high | Redox (mV) trop haut |
| `19.164` | Redox too low | Redox (mV) trop bas |
| `19.165` | Salt low \| cell protection | Sel bas \| protection |
| `19.166` | Temp. low \| cell protection | Temp. basse \| protection |
| `19.167` | Production low | Production trop basse |
| `19.168` | Redox warning | Avertissement redox |
| `19.171` | Start delay | Délai de démarrage |
| `19.215` | Salt below preferred level | Sel en dessous du niv. préf. |
| `19.260` | No cell current | Pas de courant de cellule |

#### `5.48` – `e_enum_var_sys_status_info` — System status info

| Code | EN | FR |
|------|----|----|
| `19.148` | Salt electrolysis stopped (gas detected) | Electrolyse arrêtée (gaz détecté) |
| `19.150` | Salt electrolysis stopped (redox monitoring error) | Electrolyse arrêtée (erreur redox) |
| `19.152` | Salt electrolysis stopped (low salt) | Electrolyse arrêtée (sel bas) |
| `19.156` | Salt electrolysis in safe mode (redox monitoring error) | Electrolyse en mode safe (erreur redox) |
| `19.158` | pH stopped (pH monitoring error) | Dosage pH arrêté (erreur mesure pH) |
| `19.159` | pH-Minus canister empty | Bidon pH-Minus vide |
| `19.160` | pH-Plus Canister empty | Bidon pH-Plus vide |
| `19.161` | pH too high | pH trop haut |
| `19.162` | pH too low | pH trop bas |
| `19.163` | Redox too high | Redox (mV) trop haut |
| `19.164` | Redox too low | Redox (mV) trop bas |
| `19.165` | Salt low \| cell protection | Sel bas \| protection |
| `19.166` | Temp. low \| cell protection | Temp. basse \| protection |
| `19.167` | Production low | Production trop basse |
| `19.168` | Redox warning | Avertissement redox |
| `19.170` | Filtration off (no flow) | Filtration off (pas de débit) |
| `19.174` | Everything is OK. Enjoy your pool! | Tout va bien. Profitez de votre piscine ! |
| `19.215` | Salt below preferred level | Sel en dessous du niv. préf. |
| `19.260` | No cell current | Pas de courant de cellule |
| `19.272` | Chlorine canister empty | Bidon chlore vide |
| `19.302` | Chlorine stopped (redox monitoring error) | Dosage chlore arrêté (erreur mesure redox) |
| `19.356` | Dosing paused at current pump speed | Dosage en pause à la vitesse actuelle de la pompe |

#### `5.171` – `e_enum_var_mv_status_info` — Chlorine/redox status info

| Code | EN | FR |
|------|----|----|
| `19.271` | Stopped (redox error) | Arrêt (erreur redox) |
| `19.272` | Chlorine canister empty | Bidon chlore vide |
| `19.163` | Redox too high | Redox (mV) trop haut |
| `19.164` | Redox too low | Redox (mV) trop bas |
| `19.171` | Start delay | Délai de démarrage |

#### `5.80` – `e_enum_var_ph_minus_canister_status` — pH-Minus canister

| Code | EN | FR |
|------|----|----|
| `19.257` | no level sensor | Pas de capteur de niveau |
| `19.258` | filled | Plein |
| `19.259` | empty | Vide |

> Same value set applies to: `5.143` (`e_enum_var_ph_plus_canister_status`), `5.169` (`e_enum_var_mv_canister_status`)

#### `5.37` – `e_enum_var_gas_sensor` — Gas sensor

| Code | EN | FR |
|------|----|----|
| `19.104` | Gas detected | Gaz détecté |
| `19.105` | Water detected | Eau détectée |

#### `5.36` – `e_enum_var_pool_cover_contact` — Pool cover contact (BNC)

| Code | EN | FR |
|------|----|----|
| `19.176` | open | Ouvert |
| `19.177` | closed | Fermé |

#### `5.83` – `e_enum_var_cover_status` — Cover status

| Code | EN | FR |
|------|----|----|
| `19.55` | OFF | — |
| `19.142` | open | ouvert |
| `19.143` | closed | fermé |

### Input Sensors & Flow

#### `5.11` – `e_enum_use_flow_in_bnc` — Paddle switch on FLOW input (BNC)

Yes (`19.17`) / No (`19.18`)

#### `5.12` – `e_enum_level_ph_in` — Level switch in the pH canister

| Code | EN | FR |
|------|----|----|
| `19.179` | Not used | Désactivé |
| `19.199` | BAYROL suction lance | Crépine d'aspiration BAYROL |
| `19.181` | Empty => contact closed | Vide => contact fermé |

#### `5.13` – `e_enum_level_mv_in` — Level switch in the Cl canister

| Code | EN | FR |
|------|----|----|
| `19.179` | Not used | Désactivé |
| `19.199` | BAYROL suction lance | Crépine d'aspiration BAYROL |
| `19.181` | Empty => contact closed | Vide => contact fermé |

#### `5.93` – `e_enum_cover_switch` — Pool cover switch

| Code | EN | FR |
|------|----|----|
| `19.179` | Not used | Désactivé |
| `19.182` | Cover closed => contact closed | Volet fermé => contact fermé |

#### `5.182` – `e_enum_use_flow_in_230V` — Use 230V~ signal from filter pump

Yes (`19.17`) / No (`19.18`)

#### `5.176` – `e_enum_temp_sensor` — Temperature sensor

| Code | EN | FR |
|------|----|----|
| `19.179` | Not used | Désactivé |
| `19.287` | BAYROL sensor (type PT1000) | Sonde BAYROL (PT1000) |

### Pump & Filtration Enums

#### `5.184` – `e_enum_vsp_opmode` — Filtration mode (variable speed pump)

| Code | EN | FR |
|------|----|----|
| `19.312` | OFF | — |
| `19.315` | Low | — |
| `19.316` | Med | — |
| `19.317` | High | — |
| `19.346` | Auto | — |
| `19.330` | Smart | — |
| `19.338` | Anti-freeze | Hors Gel |

> Same basic values apply to: `5.271` (`e_enum_vsp_opmode_no_temp`, without Smart/Anti-freeze)

#### `5.256` – `e_enum_on_off_filter_pump_opmode` — Filtration mode (on/off pump)

| Code | EN | FR |
|------|----|----|
| `19.313` | ON | — |
| `19.346` | Auto | — |
| `19.330` | Smart | — |
| `19.338` | Anti-freeze | Hors Gel |

#### `5.215` – `e_enum_use_vsp` — Use variable speed pump

Yes (`19.17`) / No (`19.18`)

#### `5.216` – `e_enum_vsp_extend_runtime_to_t_div_2` — Extend pump runtime at high temp.

ON (`19.54`) / OFF (`19.55`)

#### `5.207` – `e_enum_pump_clock_timer1_speed` — Pump speed (timers 1–3)

| Code | Value |
|------|-------|
| `19.315` | Low |
| `19.316` | Med |
| `19.317` | High |

> Same value set applies to: `5.209`, `5.211` (timers 2 & 3)

#### `5.206` – `e_enum_pump_clock_timer1_active` — Activate timer

ON (`19.54`) / OFF (`19.55`)

> Same applies to: `5.208`, `5.210` (timers 2 & 3)

#### `5.249` – `e_enum_pump_speed_smart_mode` — Pump speed in Smart mode

Med (`19.316`) / High (`19.317`)

#### `5.250` – `e_enum_pump_speed_winter_mode` — Pump speed in Winter mode

Med (`19.316`) / High (`19.317`)

#### `5.251` – `e_enum_pump_speed_frost_protection` — Pump speed in frost protection mode

Med (`19.316`) / High (`19.317`)

#### `5.252` – `e_enum_pump_use_frost_protection` — Activate frost protection

ON (`19.54`) / OFF (`19.55`)

#### `5.254` – `e_enum_pump_force_on_in_boost_mode` — Force filter pump ON during BOOST mode

ON (`19.54`) / OFF (`19.55`)

#### `5.270` – `e_enum_pump_speed_boost` — Pump speed in BOOST mode

Low (`19.315`) / Med (`19.316`) / High (`19.317`)

#### `5.246` – `e_enum_dosing_at_vsp_low` — Dosing when pump speed low

ON (`19.54`) / OFF (`19.55`)

#### `5.247` – `e_enum_dosing_at_vsp_med` — Dosing when pump speed med

ON (`19.54`) / OFF (`19.55`)

#### `5.248` – `e_enum_dosing_at_vsp_high` — Dosing when pump speed high

ON (`19.54`) / OFF (`19.55`)

#### `5.274` – `e_enum_dosing_at_pump_off_flow_on` — Dosing when pump OFF & flow signal ON

ON (`19.54`) / OFF (`19.55`)

### Output Functions (OUT1–OUT4)

#### `5.186` – `e_enum_out1_opmode` — Operating mode

| Code | EN | FR |
|------|----|----|
| `19.100` | OFF | — |
| `19.311` | ON | — |
| `19.345` | Auto | — |

> Same values for: `5.187` (OUT2), `5.188` (OUT3), `5.189` (OUT4)

#### `5.217` – `e_enum_out1_function` — OUT 1 function

| Code | EN | FR |
|------|----|----|
| `19.324` | Not used | Non utilisé |
| `19.329` | Filter pump (on/off) | Filtration (on/off) |
| `19.326` | Pool heating | Chauffage piscine |
| `19.328` | Multicoloured pool lighting | Eclairage piscine multicolore |

> Same values for: `5.218` (OUT2), `5.219` (OUT3), `5.220` (OUT4)
> Variants without heating: `5.261`–`5.264` (`e_enum_out{1-4}_function_no_heating`)

#### `5.212`–`5.214` – OUT1 clock timers active

ON (`19.54`) / OFF (`19.55`)

> Same pattern for OUT2 (`5.222`–`5.224`), OUT3 (`5.225`–`5.227`), OUT4 (`5.228`–`5.230`)

#### `5.231`–`5.234` – `e_enum_out{1-4}_block_if_no_flow` — Block output if no flow

ON (`19.54`) / OFF (`19.55`)

#### `5.235`–`5.238` – `e_enum_out{1-4}_next_light_program` — Click for colour change

ON (`19.54`) / OFF (`19.55`)

#### `5.258` – `e_enum_pool_light_with_programs_used` — Pool light controlled by power breaks

ON (`19.54`) / OFF (`19.55`)

### Heating Enums

#### `5.185` – `e_enum_heating_opmode` — Heating mode

| Code | EN | FR |
|------|----|----|
| `19.100` | OFF | — |
| `19.101` | Auto | — |

#### `5.243` – `e_enum_heating_at_vsp_low` — Heat when pump speed low

ON (`19.54`) / OFF (`19.55`)

#### `5.244` – `e_enum_heating_at_vsp_med` — Heat when pump speed med

ON (`19.54`) / OFF (`19.55`)

#### `5.245` – `e_enum_heating_at_vsp_high` — Heat when pump speed high

ON (`19.54`) / OFF (`19.55`)

#### `5.273` – `e_enum_heating_at_pump_off_flow_on` — Heat when pump OFF & flow signal ON

ON (`19.54`) / OFF (`19.55`)

#### `5.267`–`5.269` – Heating blocking clock timers active

ON (`19.54`) / OFF (`19.55`)

### Network & Connectivity

#### `5.150` – `e_enum_wifi` — Activate WiFi

ON (`19.54`)

#### `5.151` – `e_enum_dhcp` — DHCP (automatic configuration)

ON (`19.54`) / OFF (`19.55`)

#### `5.152` – `e_enum_var_wifi_state` — WiFi status

| Code | EN | FR |
|------|----|----|
| `19.263` | WiFi switched off | WiFi désactivé |
| `19.264` | No WiFi network selected | Aucun réseau WiFi sélectionné |
| `19.265` | Initializing WiFi… | Initialisation du Wifi... |
| `19.267` | Connecting WiFi… | Connexion WiFi… |
| `19.290` | WiFi or password error | Erreur WiFi ou mot de passe |
| `19.291` | Connecting internet… | Connexion à internet… |
| `19.292` | WiFi connected / no internet connection | WiFi connecté / Pas d'internet |
| `19.293` | Initializing DNS… | Initialisation DNS… |
| `19.294` | DNS error | Erreur DNS |
| `19.309` | Connected | Connecté |

#### `5.153` – `e_enum_var_wifi_signal` — WiFi signal strength

| Code | EN |
|------|------|
| `19.268` | WiFi signal full |
| `19.269` | WiFi signal medium |
| `19.270` | WiFi signal weak |

#### `5.174` – `e_enum_var_webportal_state` — Web portal status

| Code | EN | FR |
|------|----|----|
| `19.281` | Not connected | Pas connecté |
| `19.282` | Waiting for WiFi connection | Attente de connexion WiFi |
| `19.283` | Please enter Web portal PIN | Entrez code PIN du portail Web |
| `19.285` | No reply from Web portal | Pas de réponse du portail Web |
| `19.286` | Device registration… | Enregistrement de l'appareil… |
| `19.295` | No connection \| PIN? \| Registration? | Erreur connex. \| PIN? \| enregistrement? |
| `19.296` | Registration successful | Enregistrement réussi |
| `19.297` | Initializing MQTT… | Initialisation MQTT… |
| `19.298` | MQTT configuration failed | Echec configuration MQTT |
| `19.299` | Connecting MQTT… | Connexion MQTT… |
| `19.300` | MQTT connection failed | Echec connexion MQTT |
| `19.301` | MQTT connected | MQTT connecté |
| `19.307` | Sending data… | Envoie données… |
| `19.310` | Connected | Connecté |

#### `5.203` – `e_enum_var_fm_connection_status` — Connection status (Control Module)

| Code | EN | FR |
|------|----|----|
| `19.318` | Not connected | Pas connecté |
| `19.319` | Connected | Connecté |
| `19.320` | Connection lost | Perte de connexion |

#### `5.242` – `e_enum_var_fm_connection_quality` — Connection quality

| Code | EN | FR |
|------|----|----|
| `19.331` | No connection | Pas de connexion |
| `19.332` | Unstable | Instable |
| `19.333` | Good | Bonne |
| `19.334` | Optimal | Optimale |

#### `5.205` – `e_enum_fm_connect_mode` — Connect Smart&Easy Control Module

ON (`19.54`) / OFF (`19.55`)

#### `5.181` – `e_enum_resend_all_topics` — Resend all MQTT topics

ON (`19.54`) / OFF (`19.55`)

### Device & System Enums

#### `5.10` – `e_enum_controller_type` — Controller type

| Code | EN |
|------|------|
| `19.52` | Automatic pH |
| `19.53` | Automatic Cl/pH |

#### `5.172` – `e_enum_device_type` — Device type

| Code | EN |
|------|------|
| `19.288` | Auto detect |
| `19.274` | Automatic SALT |
| `19.276` | Automatic Cl-pH |
| `19.277` | Automatic pH |

> Same base values for: `5.173` (`e_enum_var_device_type`), `5.178` (`e_enum_var_detected_device_type`), `5.180` (`e_enum_last_detected_device_type`)

#### `5.147` – `e_enum_var_hw_version` — Hardware version

| Code | EN |
|------|------|
| `19.261` | 1.0.0.0 |
| `19.262` | 1.1.0.0 |

#### `5.239` – `e_enum_var_sw_update_required` — Software update required

Yes (`19.336`) / No (`19.337`)

#### `5.183` – `e_enum_device_6_l_per_h` — Device has 6l/h pumps

ON (`19.54`) / OFF (`19.55`)

#### `5.253` – `e_enum_box_configuration` — Select configuration

| Code | EN |
|------|------|
| `19.335` | Smart&Easy Box |

#### `5.255` – `e_enum_keep_fm_config` — Keep existing configuration of switching functions

ON (`19.54`) / OFF (`19.55`)

#### `5.257` – `e_enum_control_box_used` — I am using a Smart&Easy Box

ON (`19.54`) / OFF (`19.55`)

### Internal / GUI Variables

The following are internal/GUI state variables, typically read-only:

| Topic | Name | Description |
|-------|------|-------------|
| `5.22` | `e_enum_var_ph_status` | pH status |
| `5.25` | `e_enum_var_se_status` | mV status (SE) |
| `5.27` | `e_enum_var_system_status` | System state |
| `5.29` | `e_enum_var_flow_pump_status` | Filtration status |
| `5.32` | `e_enum_var_salt_status` | Salt status |
| `5.33` | `e_enum_var_t_status` | Temp. status |
| `5.38` | `e_enum_var_se_on_off` | SE status (ON/OFF) |
| `5.44` | `e_enum_var_se_polarity` | Current polarity (OFF/A/B) |
| `5.47` | `e_enum_var_sys_status` | System status |
| `5.73` | `e_enum_var_ph_value_status` | pH value status |
| `5.74` | `e_enum_var_se_value_status` | SE value status |
| `5.75` | `e_enum_var_t_value_status` | Temp. value status |
| `5.76` | `e_enum_var_salt_value_status` | Salt value status |
| `5.77` | `e_enum_var_standby_info` | Standby info messages |
| `5.78` | `e_enum_var_ph_opmode_icon` | pH operating mode icon |
| `5.79` | `e_enum_var_ph_pump_status` | pH pump status (standby/ON/OFF) |
| `5.81` | `e_enum_var_se_opmode` | SE operating mode |
| `5.82` | `e_enum_var_se_polarity_status` | SE polarity status |
| `5.84` | `e_enum_var_t_low_status` | Temperature low status |
| `5.92` | `e_enum_sys_overview` | System overview |
| `5.117` | `e_enum_run_se_in_overview` | SE cycle in overview |
| `5.118` | `e_enum_var_ph_pump_on_off` | pH pump ON/OFF |
| `5.120` | `e_enum_var_se_test_running` | SE test running |
| `5.122` | `e_enum_var_se_blocked` | SE blocked |
| `5.123` | `e_enum_var_plus_cycle_active` | Plus+ cycle active |
| `5.124` | `e_enum_var_safe_mode_cycle_active` | Safe mode production cycle active |
| `5.125` | `e_enum_var_se_opmode_icon` | SE operating mode icon |
| `5.126` | `e_enum_var_se_safe_mode` | SE safe mode (Yes/No) |
| `5.128` | `e_enum_var_ph_opmode` | pH operating mode |
| `5.130` | `e_enum_var_se_activate_boost` | SE BOOST activated |
| `5.131` | `e_enum_var_se_activate_manual` | SE manual activated |
| `5.132` | `e_enum_var_se_activate_pause` | SE pause activated |
| `5.133` | `e_enum_var_ph_activate_manual` | pH manual activated |
| `5.134` | `e_enum_var_ph_activate_pause` | pH pause activated |
| `5.141` | `e_enum_var_ph_blocked_by_salt` | pH blocked by salt |
| `5.142` | `e_enum_var_ph_blocked` | pH blocked |
| `5.162` | `e_enum_var_mv_activate_manual` | mV manual activated |
| `5.163` | `e_enum_var_mv_activate_pause` | mV pause activated |
| `5.165` | `e_enum_var_mv_pump_on_off` | Cl pump ON/OFF |
| `5.166` | `e_enum_var_mv_opmode` | mV operating mode |
| `5.167` | `e_enum_var_mv_status` | mV status |
| `5.168` | `e_enum_var_mv_pump_status` | mV pump status (standby/ON/OFF) |
| `5.170` | `e_enum_var_mv_value_status` | mV value status |
| `5.177` | `e_enum_var_mv_opmode_icon` | mV operating mode icon |
| `5.179` | `e_enum_var_mv_blocked` | mV blocked |
| `5.190` | `e_enum_var_vsp_used` | Variable speed pump used |
| `5.191` | `e_enum_var_heating_used` | Heating used |
| `5.192`–`5.195` | `e_enum_var_out{1-4}_used` | OUT 1–4 used |
| `5.196` | `e_enum_var_vsp_speed` | Pump speed (OFF/Low/Med/High) |
| `5.197` | `e_enum_var_vsp_on_off` | Pump ON/OFF |
| `5.198` | `e_enum_var_heating_on_off` | Heating ON/OFF |
| `5.199`–`5.202` | `e_enum_var_out{1-4}_on_off` | OUT 1–4 ON/OFF |
| `5.204` | `e_enum_var_water_treatment_status` | Water treatment status |
| `5.265` | `e_enum_fm_supported` | Control Module supported |
| `5.266` | `e_enum_fm_used` | Control Module used |

---

## Type 6 – String Topics

All string topics carry a text string value.

| Topic | Name | Description (EN) | Description (FR) |
|-------|------|-------------------|-------------------|
| `6.2` | `e_string_mac` | Device MAC address | Adresse MAC |
| `6.3` | `e_string_ip` | Device IP address | Adresse IP |
| `6.4` | `e_string_gateway` | Gateway IP address | Adresse passerelle |
| `6.5` | `e_string_netmask` | Netmask | Masque |
| `6.6` | `e_string_password` | Password | Mot de passe |
| `6.7` | `e_string_email` | E-Mail address | Adresse E-mail |
| `6.8` | `e_string_username` | Username | Nom utilisateur |
| `6.9` | `e_string_dns` | DNS IP address | Adresse IP DNS |
| `6.10` | `e_string_webportal_pin` | Web portal PIN | PIN portail web |
| `6.11` | `e_string_serial_no_gui` | Enter new Serial No. | Numéro de série (menu) |
| `6.12` | `e_string_url` | Web portal URL | URL portail Web |
| `6.13` | `e_string_url_gui` | Enter new Web portal URL | URL portail Web (menu) |
| `6.14` | `e_string_device_name` | Device name | Nom de l'appareil |
| `6.15` | `e_string_sw_version` | Software version | Version logiciel |
| `6.16` | `e_string_serial_no` | Serial No. | Numéro de série |
| `6.17` | `e_string_hw_version` | Hardware version | — |
| `6.18` | `e_string_hw_version_gui` | Enter new Hardware version | — |
| `6.19` | `e_string_vsp_name` | Filtration | — |
| `6.20` | `e_string_heating_name` | Heating | Chauffage |
| `6.21` | `e_string_out1_name_universal` | Function name (OUT1) | Nom de la fonction |
| `6.22` | `e_string_out2_name_universal` | Function name (OUT2) | Nom de la fonction |
| `6.23` | `e_string_out3_name_universal` | Function name (OUT3) | Nom de la fonction |
| `6.24` | `e_string_out4_name_universal` | Function name (OUT4) | Nom de la fonction |
| `6.25` | `e_string_out1_name_pool_light` | Pool light name (OUT1) | Nom de l'éclairage de piscine |
| `6.26` | `e_string_out2_name_pool_light` | Pool light name (OUT2) | Nom de l'éclairage de piscine |
| `6.27` | `e_string_out3_name_pool_light` | Pool light name (OUT3) | Nom de l'éclairage de piscine |
| `6.28` | `e_string_out4_name_pool_light` | Pool light name (OUT4) | Nom de l'éclairage de piscine |
| `6.29` | `e_string_diag_settings` | Diag settings | — |
| `6.30` | `e_string_fm_sw_version` | Software version (Control Module) | Version logiciel (Control Module) |
| `6.31` | `e_string_fm_serial_no` | Serial No. (Control Module) | Numéro de série (Control Module) |
| `6.32` | `e_string_sw_commit` | Software commit | — |
| `6.33` | `e_string_fm_sw_commit` | Software commit (Control Module) | — |
| `6.34` | `e_string_fm_matching_sw_version` | Matching software version (Control Module) | Version logiciel corresp. (Control Module) |
