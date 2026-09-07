# MapSpatial-EvalKit Results

- Direct source: `/mnt/nas-tbt/caoziqi/code/SpatialIntelligence/MapSpatial-EvalKit/results` (JSONL, **read-only**)
- Generated: 2026-08-29 05:18
- Direct models: 21 (skipped `*.broken` / `*.old*` / `logs` / `docs`)
- Direct records: 1362470
- Draw source: `/mnt/nas-tbt/caoziqi/code/SpatialIntelligence/MapSpatial-EvalKit/results_draw` (JSONL, **read-only**)
- Draw models: 5
- Draw records: 4285

Accuracy is **correct / answered × 100**, using each JSONL record's `exact_match`.
Empty files (`total=0`) are shown as —. Models were not all run on the same slice; overall scores are **not** directly comparable.

## Direct (`results`)

## 1. Overall

| Model | Strategy | Backend | Acc (%) | Direct | Oracle | Δ (pp) | N | Correct | Cells |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GLM-4.6V-Flash | direct | vllm | 57.4 | 54.2 | 60.6 | +6.5 | 65200 | 37422 | 192 |
| MiMo-Embodied-7B | direct | vllm | 54.9 | 53.5 | 56.2 | +2.6 | 65200 | 35767 | 192 |
| SenseNova-SI-1.5-InternVL3-8B | direct | sensenova_si | 54.1 | 53.0 | 55.3 | +2.3 | 65200 | 35296 | 192 |
| Qwen2.5-VL-7B-Instruct | direct | vllm | 53.2 | 51.2 | 55.3 | +4.0 | 65200 | 34713 | 192 |
| ThinkMorph-7B | direct | veomni_thinkmorph | 51.4 | 48.8 | 54.1 | +5.3 | 65200 | 33545 | 192 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | sensenova_si | 51.4 | 49.6 | 53.3 | +3.7 | 65200 | 33539 | 192 |
| Bagel-7B-MoT | direct | veomni_bagel | 51.1 | 48.8 | 53.3 | +4.5 | 65200 | 33287 | 192 |
| JoyAI-Image | direct | veomni_joyai | 50.7 | 47.8 | 53.5 | +5.7 | 65200 | 33032 | 192 |
| Step3-VL-10B | direct | vllm | 50.6 | 47.6 | 53.5 | +5.9 | 65200 | 32979 | 192 |
| Qwen3-VL-8B-Instruct | direct | vllm | 50.1 | 46.8 | 53.5 | +6.7 | 65200 | 32679 | 192 |
| ViLaSR | direct | vilasr | 48.3 | 47.2 | 49.4 | +2.2 | 58470 | 28265 | 162 |
| InternVL3-8B-Instruct | direct | vllm | 47.1 | 45.0 | 49.3 | +4.3 | 65200 | 30734 | 192 |
| Qwen2-VL-7B-Instruct | direct | vllm | 42.4 | 41.9 | 42.9 | +1.1 | 65200 | 27641 | 192 |
| Spatial-MLLM | direct | spatial_mllm | 41.1 | 41.2 | 41.0 | -0.1 | 65200 | 26800 | 192 |
| InternVL3_5-8B | direct | vllm | 40.6 | 38.8 | 42.5 | +3.7 | 65200 | 26487 | 192 |
| SenseNova-U1-8B-MoT | direct | veomni_u1 | 40.4 | 40.5 | 40.3 | -0.2 | 65200 | 26351 | 192 |
| LatentUM-Base | direct | veomni_latentum | 40.1 | 38.8 | 41.4 | +2.6 | 65200 | 26156 | 192 |
| Show-o2-7B | direct | veomni_showo2 | 39.5 | 37.9 | 41.1 | +3.2 | 65200 | 25744 | 192 |
| BLIP3o-8B | direct | veomni_blip3o | 36.2 | 36.1 | 36.2 | +0.1 | 65200 | 23580 | 192 |
| Cambrian-S-7B-LFP | direct | cambrian | 35.4 | 35.5 | 35.3 | -0.2 | 65200 | 23086 | 192 |
| Janus-Pro-7B | direct | veomni_janus | 33.1 | 32.2 | 33.9 | +1.7 | 65200 | 21549 | 192 |

## 2. Completeness

| Model | Tasks | Views | Families | N | Cells | Files |
| --- | --- | --- | --- | --- | --- | --- |
| GLM-4.6V-Flash | t1,t2,t3,t4 | blank,sat,webrd04,wprd01 | base,transform,world | 65200 | 192 | 192 |
| MiMo-Embodied-7B | t1,t2,t3,t4 | blank,sat,webrd04,wprd01 | base,transform,world | 65200 | 192 | 192 |
| SenseNova-SI-1.5-InternVL3-8B | t1,t2,t3,t4 | blank,sat,webrd04,wprd01 | base,transform,world | 65200 | 192 | 192 |
| Qwen2.5-VL-7B-Instruct | t1,t2,t3,t4 | blank,sat,webrd04,wprd01 | base,transform,world | 65200 | 192 | 192 |
| ThinkMorph-7B | t1,t2,t3,t4 | blank,sat,webrd04,wprd01 | base,transform,world | 65200 | 192 | 192 |
| SenseNova-SI-1.3-Qwen3-VL-8B | t1,t2,t3,t4 | blank,sat,webrd04,wprd01 | base,transform,world | 65200 | 192 | 192 |
| Bagel-7B-MoT | t1,t2,t3,t4 | blank,sat,webrd04,wprd01 | base,transform,world | 65200 | 192 | 192 |
| JoyAI-Image | t1,t2,t3,t4 | blank,sat,webrd04,wprd01 | base,transform,world | 65200 | 192 | 192 |
| Step3-VL-10B | t1,t2,t3,t4 | blank,sat,webrd04,wprd01 | base,transform,world | 65200 | 192 | 192 |
| Qwen3-VL-8B-Instruct | t1,t2,t3,t4 | blank,sat,webrd04,wprd01 | base,transform,world | 65200 | 192 | 192 |
| ViLaSR | t1,t2,t3,t4 | blank,sat,webrd04,wprd01 | base,transform,world | 58470 | 162 | 162 |
| InternVL3-8B-Instruct | t1,t2,t3,t4 | blank,sat,webrd04,wprd01 | base,transform,world | 65200 | 192 | 192 |
| Qwen2-VL-7B-Instruct | t1,t2,t3,t4 | blank,sat,webrd04,wprd01 | base,transform,world | 65200 | 192 | 192 |
| Spatial-MLLM | t1,t2,t3,t4 | blank,sat,webrd04,wprd01 | base,transform,world | 65200 | 192 | 192 |
| InternVL3_5-8B | t1,t2,t3,t4 | blank,sat,webrd04,wprd01 | base,transform,world | 65200 | 192 | 192 |
| SenseNova-U1-8B-MoT | t1,t2,t3,t4 | blank,sat,webrd04,wprd01 | base,transform,world | 65200 | 192 | 192 |
| LatentUM-Base | t1,t2,t3,t4 | blank,sat,webrd04,wprd01 | base,transform,world | 65200 | 192 | 192 |
| Show-o2-7B | t1,t2,t3,t4 | blank,sat,webrd04,wprd01 | base,transform,world | 65200 | 192 | 192 |
| BLIP3o-8B | t1,t2,t3,t4 | blank,sat,webrd04,wprd01 | base,transform,world | 65200 | 192 | 192 |
| Cambrian-S-7B-LFP | t1,t2,t3,t4 | blank,sat,webrd04,wprd01 | base,transform,world | 65200 | 192 | 192 |
| Janus-Pro-7B | t1,t2,t3,t4 | blank,sat,webrd04,wprd01 | base,transform,world | 65200 | 192 | 192 |

## 3. By evidence condition

| Model | Direct (%) | N_direct | Oracle (%) | N_oracle | Δ (pp) |
| --- | --- | --- | --- | --- | --- |
| GLM-4.6V-Flash | 54.2 | 32600 | 60.6 | 32600 | +6.5 |
| MiMo-Embodied-7B | 53.5 | 32600 | 56.2 | 32600 | +2.6 |
| SenseNova-SI-1.5-InternVL3-8B | 53.0 | 32600 | 55.3 | 32600 | +2.3 |
| Qwen2.5-VL-7B-Instruct | 51.2 | 32600 | 55.3 | 32600 | +4.0 |
| ThinkMorph-7B | 48.8 | 32600 | 54.1 | 32600 | +5.3 |
| SenseNova-SI-1.3-Qwen3-VL-8B | 49.6 | 32600 | 53.3 | 32600 | +3.7 |
| Bagel-7B-MoT | 48.8 | 32600 | 53.3 | 32600 | +4.5 |
| JoyAI-Image | 47.8 | 32600 | 53.5 | 32600 | +5.7 |
| Step3-VL-10B | 47.6 | 32600 | 53.5 | 32600 | +5.9 |
| Qwen3-VL-8B-Instruct | 46.8 | 32600 | 53.5 | 32600 | +6.7 |
| ViLaSR | 47.2 | 29070 | 49.4 | 29400 | +2.2 |
| InternVL3-8B-Instruct | 45.0 | 32600 | 49.3 | 32600 | +4.3 |
| Qwen2-VL-7B-Instruct | 41.9 | 32600 | 42.9 | 32600 | +1.1 |
| Spatial-MLLM | 41.2 | 32600 | 41.0 | 32600 | -0.1 |
| InternVL3_5-8B | 38.8 | 32600 | 42.5 | 32600 | +3.7 |
| SenseNova-U1-8B-MoT | 40.5 | 32600 | 40.3 | 32600 | -0.2 |
| LatentUM-Base | 38.8 | 32600 | 41.4 | 32600 | +2.6 |
| Show-o2-7B | 37.9 | 32600 | 41.1 | 32600 | +3.2 |
| BLIP3o-8B | 36.1 | 32600 | 36.2 | 32600 | +0.1 |
| Cambrian-S-7B-LFP | 35.5 | 32600 | 35.3 | 32600 | -0.2 |
| Janus-Pro-7B | 32.2 | 32600 | 33.9 | 32600 | +1.7 |

## 4. By view

| Model | blank | sat | webrd04 | wprd01 | Overall |
| --- | --- | --- | --- | --- | --- |
| GLM-4.6V-Flash | 66.3 | 55.8 | 49.6 | 55.7 | 57.4 |
| MiMo-Embodied-7B | 66.7 | 51.4 | 45.7 | 53.7 | 54.9 |
| SenseNova-SI-1.5-InternVL3-8B | 65.4 | 51.0 | 43.2 | 53.3 | 54.1 |
| Qwen2.5-VL-7B-Instruct | 57.9 | 53.4 | 46.5 | 51.8 | 53.2 |
| ThinkMorph-7B | 63.1 | 48.4 | 42.5 | 50.0 | 51.4 |
| SenseNova-SI-1.3-Qwen3-VL-8B | 58.6 | 49.9 | 43.1 | 50.8 | 51.4 |
| Bagel-7B-MoT | 65.0 | 48.2 | 46.6 | 47.3 | 51.1 |
| JoyAI-Image | 58.0 | 50.1 | 44.9 | 48.3 | 50.7 |
| Step3-VL-10B | 57.5 | 50.8 | 38.3 | 49.0 | 50.6 |
| Qwen3-VL-8B-Instruct | 55.5 | 49.2 | 45.2 | 49.1 | 50.1 |
| ViLaSR | 59.5 | 45.4 | 33.5 | 46.2 | 48.3 |
| InternVL3-8B-Instruct | 54.5 | 45.2 | 42.5 | 46.0 | 47.1 |
| Qwen2-VL-7B-Instruct | 48.8 | 40.9 | 39.9 | 40.9 | 42.4 |
| Spatial-MLLM | 52.3 | 39.4 | 33.4 | 38.2 | 41.1 |
| InternVL3_5-8B | 50.1 | 40.8 | 39.9 | 35.6 | 40.6 |
| SenseNova-U1-8B-MoT | 51.6 | 37.3 | 33.3 | 38.9 | 40.4 |
| LatentUM-Base | 46.4 | 37.5 | 38.7 | 39.6 | 40.1 |
| Show-o2-7B | 44.1 | 37.4 | 38.1 | 39.4 | 39.5 |
| BLIP3o-8B | 37.4 | 35.9 | 37.8 | 35.5 | 36.2 |
| Cambrian-S-7B-LFP | 39.8 | 35.9 | 31.5 | 33.3 | 35.4 |
| Janus-Pro-7B | 42.8 | 30.9 | 28.9 | 30.7 | 33.1 |

## 5. By task

| Model | t1 | t2 | t3 | t4 | Overall |
| --- | --- | --- | --- | --- | --- |
| GLM-4.6V-Flash | 69.3 | 57.0 | 31.7 | 57.8 | 57.4 |
| MiMo-Embodied-7B | 71.1 | 57.1 | 32.6 | 44.5 | 54.9 |
| SenseNova-SI-1.5-InternVL3-8B | 68.0 | 63.5 | 40.3 | 33.0 | 54.1 |
| Qwen2.5-VL-7B-Instruct | 60.0 | 52.7 | 53.6 | 45.4 | 53.2 |
| ThinkMorph-7B | 62.0 | 60.5 | 33.6 | 37.3 | 51.4 |
| SenseNova-SI-1.3-Qwen3-VL-8B | 62.5 | 50.8 | 27.3 | 52.3 | 51.4 |
| Bagel-7B-MoT | 62.1 | 62.0 | 25.4 | 38.4 | 51.1 |
| JoyAI-Image | 60.7 | 49.6 | 34.2 | 48.9 | 50.7 |
| Step3-VL-10B | 65.9 | 44.4 | 47.5 | 40.9 | 50.6 |
| Qwen3-VL-8B-Instruct | 58.0 | 48.5 | 27.7 | 55.3 | 50.1 |
| ViLaSR | 56.1 | 56.7 | 37.1 | 31.2 | 48.3 |
| InternVL3-8B-Instruct | 51.5 | 57.6 | 37.5 | 34.2 | 47.1 |
| Qwen2-VL-7B-Instruct | 48.6 | 44.4 | 39.3 | 33.9 | 42.4 |
| Spatial-MLLM | 46.7 | 54.4 | 24.3 | 27.2 | 41.1 |
| InternVL3_5-8B | 51.1 | 44.2 | 28.2 | 30.2 | 40.6 |
| SenseNova-U1-8B-MoT | 48.1 | 45.5 | 21.7 | 35.2 | 40.4 |
| LatentUM-Base | 45.7 | 44.7 | 31.2 | 32.5 | 40.1 |
| Show-o2-7B | 36.1 | 48.1 | 51.4 | 26.0 | 39.5 |
| BLIP3o-8B | 30.7 | 44.5 | 37.0 | 32.1 | 36.2 |
| Cambrian-S-7B-LFP | 34.9 | 46.0 | 34.2 | 23.5 | 35.4 |
| Janus-Pro-7B | 41.4 | 41.1 | 41.9 | 7.5 | 33.1 |

## 6. By variant family

| Model | base | transform | world | Overall |
| --- | --- | --- | --- | --- |
| GLM-4.6V-Flash | 53.1 | 59.8 | 41.5 | 57.4 |
| MiMo-Embodied-7B | 56.3 | 56.6 | 33.2 | 54.9 |
| SenseNova-SI-1.5-InternVL3-8B | 54.9 | 56.0 | 32.9 | 54.1 |
| Qwen2.5-VL-7B-Instruct | 52.9 | 54.8 | 37.2 | 53.2 |
| ThinkMorph-7B | 51.8 | 53.3 | 31.9 | 51.4 |
| SenseNova-SI-1.3-Qwen3-VL-8B | 51.8 | 52.8 | 36.2 | 51.4 |
| Bagel-7B-MoT | 52.4 | 52.4 | 34.6 | 51.1 |
| JoyAI-Image | 51.4 | 51.7 | 38.5 | 50.7 |
| Step3-VL-10B | 51.2 | 51.9 | 35.3 | 50.6 |
| Qwen3-VL-8B-Instruct | 52.1 | 51.1 | 36.1 | 50.1 |
| ViLaSR | 50.1 | 49.2 | 28.5 | 48.3 |
| InternVL3-8B-Instruct | 49.0 | 48.5 | 28.7 | 47.1 |
| Qwen2-VL-7B-Instruct | 43.5 | 43.1 | 32.8 | 42.4 |
| Spatial-MLLM | 42.2 | 42.6 | 23.5 | 41.1 |
| InternVL3_5-8B | 46.9 | 40.9 | 25.1 | 40.6 |
| SenseNova-U1-8B-MoT | 42.0 | 41.2 | 28.5 | 40.4 |
| LatentUM-Base | 45.0 | 40.4 | 27.1 | 40.1 |
| Show-o2-7B | 41.5 | 39.4 | 35.7 | 39.5 |
| BLIP3o-8B | 38.7 | 36.2 | 30.2 | 36.2 |
| Cambrian-S-7B-LFP | 38.3 | 35.9 | 24.0 | 35.4 |
| Janus-Pro-7B | 37.8 | 33.9 | 14.6 | 33.1 |

## 7. T4 · base + transform (comparable subset)

Aggregated across views with `total>0`.

### Direct

| Model | base | rot90 | rot180 | rot270 | mirror_h | m_r90 | m_r180 | m_r270 | All |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GLM-4.6V-Flash | 49.6 | 57.0 | 58.0 | 59.0 | 56.7 | 57.3 | 56.6 | 56.6 | 56.1 |
| MiMo-Embodied-7B | 55.3 | 56.2 | 57.1 | 56.3 | 53.6 | 55.1 | 54.1 | 55.4 | 55.4 |
| SenseNova-SI-1.5-InternVL3-8B | 54.3 | 56.1 | 56.9 | 58.4 | 53.3 | 55.0 | 52.0 | 51.9 | 54.7 |
| Qwen2.5-VL-7B-Instruct | 50.5 | 54.3 | 52.6 | 55.8 | 53.2 | 49.4 | 53.0 | 52.7 | 52.6 |
| ThinkMorph-7B | 48.3 | 51.3 | 49.0 | 51.2 | 51.5 | 51.9 | 51.3 | 50.0 | 50.5 |
| SenseNova-SI-1.3-Qwen3-VL-8B | 49.8 | 51.6 | 52.2 | 53.3 | 51.9 | 50.9 | 49.1 | 49.5 | 51.0 |
| Bagel-7B-MoT | 50.1 | 49.5 | 50.0 | 50.0 | 51.8 | 50.8 | 51.8 | 49.3 | 50.4 |
| JoyAI-Image | 49.3 | 50.8 | 49.5 | 51.7 | 48.7 | 45.6 | 47.6 | 47.7 | 48.9 |
| Step3-VL-10B | 48.4 | 50.8 | 51.0 | 50.8 | 47.1 | 48.3 | 47.1 | 49.2 | 49.0 |
| Qwen3-VL-8B-Instruct | 48.9 | 48.6 | 49.1 | 50.3 | 48.5 | 45.5 | 45.8 | 46.8 | 48.0 |
| ViLaSR | 49.2 | 52.0 | 48.9 | 51.6 | 46.9 | 45.6 | 46.2 | 45.6 | 48.3 |
| InternVL3-8B-Instruct | 47.1 | 47.6 | 46.5 | 47.6 | 46.7 | 45.1 | 45.6 | 45.0 | 46.4 |
| Qwen2-VL-7B-Instruct | 42.2 | 40.9 | 40.2 | 43.7 | 43.0 | 45.8 | 43.0 | 43.2 | 42.7 |
| Spatial-MLLM | 42.5 | 44.3 | 44.6 | 43.2 | 41.2 | 42.9 | 41.1 | 41.1 | 42.6 |
| InternVL3_5-8B | 44.4 | 43.8 | 43.3 | 42.0 | 35.8 | 36.6 | 35.4 | 36.7 | 40.0 |
| SenseNova-U1-8B-MoT | 42.2 | 44.6 | 43.2 | 45.9 | 39.2 | 40.3 | 38.0 | 38.4 | 41.5 |
| LatentUM-Base | 43.7 | 40.1 | 43.9 | 40.1 | 36.0 | 39.6 | 35.6 | 38.0 | 39.8 |
| Show-o2-7B | 40.8 | 42.1 | 40.2 | 42.8 | 36.0 | 33.8 | 36.5 | 33.5 | 38.3 |
| BLIP3o-8B | 38.8 | 41.3 | 39.6 | 40.7 | 33.7 | 31.6 | 34.2 | 31.9 | 36.6 |
| Cambrian-S-7B-LFP | 38.7 | 40.7 | 40.4 | 40.8 | 33.3 | 32.5 | 33.1 | 30.8 | 36.4 |
| Janus-Pro-7B | 37.0 | 37.4 | 36.9 | 37.2 | 30.9 | 29.4 | 29.2 | 29.8 | 33.6 |

### Oracle

| Model | base | rot90 | rot180 | rot270 | mirror_h | m_r90 | m_r180 | m_r270 | All |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GLM-4.6V-Flash | 56.7 | 62.4 | 62.8 | 63.7 | 61.7 | 62.6 | 59.9 | 62.1 | 61.3 |
| MiMo-Embodied-7B | 57.3 | 58.8 | 59.1 | 58.9 | 57.1 | 57.6 | 56.5 | 57.3 | 57.8 |
| SenseNova-SI-1.5-InternVL3-8B | 55.6 | 58.1 | 60.0 | 60.8 | 55.6 | 56.7 | 54.8 | 54.4 | 56.9 |
| Qwen2.5-VL-7B-Instruct | 55.4 | 57.3 | 56.5 | 59.1 | 57.4 | 54.4 | 56.7 | 55.4 | 56.5 |
| ThinkMorph-7B | 55.2 | 56.0 | 53.2 | 55.7 | 55.4 | 56.8 | 57.1 | 55.3 | 55.6 |
| SenseNova-SI-1.3-Qwen3-VL-8B | 53.7 | 56.1 | 56.8 | 56.6 | 54.2 | 52.8 | 51.8 | 52.9 | 54.3 |
| Bagel-7B-MoT | 54.7 | 54.0 | 53.9 | 54.6 | 55.2 | 55.0 | 54.5 | 52.6 | 54.3 |
| JoyAI-Image | 53.4 | 56.6 | 56.7 | 58.6 | 55.1 | 51.9 | 52.1 | 51.1 | 54.4 |
| Step3-VL-10B | 54.0 | 57.4 | 56.9 | 56.0 | 52.6 | 54.4 | 51.8 | 53.5 | 54.5 |
| Qwen3-VL-8B-Instruct | 55.2 | 55.8 | 57.4 | 57.3 | 55.2 | 52.5 | 49.8 | 52.4 | 54.5 |
| ViLaSR | 50.9 | 52.4 | 53.0 | 52.3 | 49.7 | 48.3 | 48.9 | 48.0 | 50.5 |
| InternVL3-8B-Instruct | 51.0 | 51.0 | 49.4 | 52.6 | 52.0 | 50.6 | 49.6 | 50.0 | 50.8 |
| Qwen2-VL-7B-Instruct | 44.7 | 41.2 | 42.6 | 43.8 | 43.0 | 46.7 | 42.9 | 43.3 | 43.6 |
| Spatial-MLLM | 41.9 | 43.8 | 44.2 | 43.2 | 41.6 | 42.6 | 41.4 | 40.8 | 42.4 |
| InternVL3_5-8B | 49.4 | 47.1 | 47.2 | 45.0 | 38.9 | 41.4 | 38.9 | 39.9 | 43.8 |
| SenseNova-U1-8B-MoT | 41.9 | 45.9 | 44.6 | 46.3 | 37.5 | 38.8 | 37.3 | 37.1 | 41.2 |
| LatentUM-Base | 46.4 | 42.5 | 45.5 | 42.5 | 40.0 | 42.5 | 37.8 | 41.2 | 42.5 |
| Show-o2-7B | 42.3 | 44.9 | 43.6 | 44.4 | 39.6 | 37.4 | 41.0 | 36.4 | 41.2 |
| BLIP3o-8B | 38.6 | 40.9 | 39.3 | 41.5 | 34.2 | 31.7 | 34.1 | 32.5 | 36.7 |
| Cambrian-S-7B-LFP | 37.9 | 41.1 | 40.1 | 40.9 | 33.3 | 32.0 | 33.0 | 30.9 | 36.2 |
| Janus-Pro-7B | 38.5 | 38.8 | 38.5 | 39.2 | 31.8 | 32.0 | 32.3 | 30.7 | 35.4 |

## 8. T1 / T2 · base + transform

### Direct

| Model | base | rot90 | rot180 | rot270 | mirror_h | m_r90 | m_r180 | m_r270 | All |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GLM-4.6V-Flash | 53.7 | 64.6 | 66.0 | 66.8 | 63.3 | 64.4 | 62.5 | 63.7 | 62.7 |
| MiMo-Embodied-7B | 65.0 | 65.2 | 66.3 | 64.7 | 61.0 | 63.9 | 61.3 | 62.9 | 63.8 |
| SenseNova-SI-1.5-InternVL3-8B | 65.5 | 66.5 | 67.3 | 69.1 | 62.4 | 64.5 | 60.5 | 60.1 | 64.5 |
| Qwen2.5-VL-7B-Instruct | 52.9 | 57.6 | 54.1 | 59.1 | 55.5 | 50.5 | 55.4 | 53.1 | 54.7 |
| ThinkMorph-7B | 57.2 | 59.8 | 57.1 | 60.5 | 61.0 | 60.9 | 60.9 | 58.3 | 59.4 |
| SenseNova-SI-1.3-Qwen3-VL-8B | 54.8 | 55.9 | 55.9 | 57.8 | 56.4 | 54.3 | 53.4 | 52.5 | 55.1 |
| Bagel-7B-MoT | 60.7 | 59.9 | 59.8 | 60.7 | 63.0 | 61.6 | 63.0 | 59.2 | 61.0 |
| JoyAI-Image | 53.7 | 55.2 | 52.2 | 56.2 | 51.7 | 48.7 | 50.1 | 49.7 | 52.2 |
| Step3-VL-10B | 54.5 | 56.5 | 56.9 | 56.7 | 50.2 | 52.8 | 51.4 | 52.7 | 54.0 |
| Qwen3-VL-8B-Instruct | 52.4 | 51.2 | 50.9 | 52.2 | 50.7 | 46.7 | 46.6 | 47.2 | 49.9 |
| ViLaSR | 58.9 | 59.7 | 56.8 | 59.8 | 52.9 | 52.0 | 51.3 | 50.6 | 55.2 |
| InternVL3-8B-Instruct | 53.2 | 54.5 | 52.5 | 54.3 | 54.0 | 51.4 | 51.5 | 50.5 | 52.8 |
| Qwen2-VL-7B-Instruct | 46.5 | 44.0 | 42.9 | 47.3 | 47.3 | 51.0 | 46.8 | 46.3 | 46.5 |
| Spatial-MLLM | 52.2 | 52.5 | 53.9 | 51.4 | 48.3 | 50.8 | 48.8 | 47.4 | 50.7 |
| InternVL3_5-8B | 52.5 | 51.1 | 51.1 | 47.8 | 39.2 | 40.5 | 39.1 | 41.1 | 45.6 |
| SenseNova-U1-8B-MoT | 49.4 | 51.5 | 49.8 | 53.5 | 43.8 | 44.6 | 42.2 | 42.4 | 47.2 |
| LatentUM-Base | 50.1 | 44.6 | 49.5 | 44.8 | 37.8 | 44.1 | 37.6 | 40.5 | 43.9 |
| Show-o2-7B | 44.8 | 46.6 | 44.1 | 48.0 | 37.0 | 34.4 | 38.5 | 33.5 | 41.0 |
| BLIP3o-8B | 40.2 | 44.6 | 41.9 | 43.9 | 33.0 | 30.7 | 34.2 | 30.9 | 37.5 |
| Cambrian-S-7B-LFP | 44.6 | 47.5 | 46.7 | 47.3 | 35.8 | 34.4 | 35.5 | 32.1 | 40.6 |
| Janus-Pro-7B | 46.1 | 45.1 | 44.4 | 45.1 | 35.3 | 34.5 | 33.4 | 34.6 | 40.1 |

### Oracle

| Model | base | rot90 | rot180 | rot270 | mirror_h | m_r90 | m_r180 | m_r270 | All |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GLM-4.6V-Flash | 57.6 | 65.2 | 65.2 | 67.0 | 63.8 | 65.0 | 62.3 | 64.1 | 63.5 |
| MiMo-Embodied-7B | 64.0 | 65.8 | 66.4 | 66.0 | 63.3 | 63.7 | 62.4 | 63.2 | 64.3 |
| SenseNova-SI-1.5-InternVL3-8B | 67.8 | 68.6 | 70.5 | 71.8 | 64.9 | 66.0 | 63.1 | 63.0 | 67.0 |
| Qwen2.5-VL-7B-Instruct | 57.3 | 59.5 | 56.9 | 61.9 | 59.3 | 54.8 | 58.5 | 55.3 | 57.9 |
| ThinkMorph-7B | 63.6 | 63.7 | 59.5 | 62.6 | 63.2 | 64.8 | 65.3 | 61.6 | 63.1 |
| SenseNova-SI-1.3-Qwen3-VL-8B | 58.7 | 60.8 | 61.1 | 60.8 | 58.1 | 55.3 | 55.0 | 55.5 | 58.2 |
| Bagel-7B-MoT | 64.0 | 62.2 | 62.5 | 63.3 | 64.7 | 64.0 | 63.5 | 60.1 | 63.1 |
| JoyAI-Image | 57.7 | 62.2 | 60.5 | 64.1 | 58.6 | 55.0 | 54.0 | 52.5 | 58.1 |
| Step3-VL-10B | 57.5 | 60.2 | 59.5 | 57.8 | 52.9 | 56.5 | 52.4 | 53.9 | 56.4 |
| Qwen3-VL-8B-Instruct | 59.2 | 58.7 | 60.1 | 59.7 | 57.8 | 54.2 | 49.5 | 52.8 | 56.6 |
| ViLaSR | 59.9 | 60.7 | 59.6 | 60.8 | 56.5 | 54.8 | 54.3 | 53.5 | 57.6 |
| InternVL3-8B-Instruct | 57.0 | 57.1 | 53.9 | 58.2 | 58.1 | 56.6 | 54.9 | 54.7 | 56.3 |
| Qwen2-VL-7B-Instruct | 49.3 | 42.9 | 45.1 | 46.1 | 45.8 | 50.8 | 45.5 | 45.3 | 46.5 |
| Spatial-MLLM | 50.8 | 52.1 | 52.5 | 51.5 | 48.5 | 50.3 | 48.8 | 47.8 | 50.3 |
| InternVL3_5-8B | 58.1 | 54.9 | 54.7 | 52.0 | 42.9 | 46.6 | 42.4 | 43.8 | 49.8 |
| SenseNova-U1-8B-MoT | 48.5 | 52.9 | 51.1 | 53.1 | 41.5 | 42.5 | 41.0 | 39.8 | 46.4 |
| LatentUM-Base | 52.9 | 46.9 | 50.8 | 46.5 | 42.5 | 46.9 | 39.8 | 43.9 | 46.5 |
| Show-o2-7B | 45.0 | 48.4 | 46.7 | 48.4 | 40.2 | 37.4 | 42.8 | 36.5 | 43.3 |
| BLIP3o-8B | 40.3 | 44.1 | 41.7 | 44.5 | 33.9 | 30.1 | 34.2 | 31.7 | 37.7 |
| Cambrian-S-7B-LFP | 43.5 | 47.8 | 46.0 | 47.5 | 35.4 | 33.9 | 35.3 | 31.7 | 40.3 |
| Janus-Pro-7B | 47.6 | 47.4 | 46.5 | 48.2 | 36.7 | 37.2 | 38.1 | 35.7 | 42.4 |

## 9. T3 · base + transform

### Direct

| Model | base | rot90 | rot180 | rot270 | mirror_h | m_r90 | m_r180 | m_r270 | All |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GLM-4.6V-Flash | 30.5 | 26.8 | 26.2 | 30.8 | 27.0 | 28.5 | 30.0 | 26.5 | 28.4 |
| MiMo-Embodied-7B | 33.0 | 30.5 | 31.0 | 31.5 | 32.5 | 29.8 | 32.5 | 33.8 | 31.9 |
| SenseNova-SI-1.5-InternVL3-8B | 39.0 | 42.2 | 43.5 | 44.8 | 42.2 | 45.5 | 41.2 | 42.8 | 42.4 |
| Qwen2.5-VL-7B-Instruct | 54.8 | 54.5 | 54.5 | 55.0 | 56.0 | 54.0 | 55.0 | 57.0 | 55.1 |
| ThinkMorph-7B | 31.2 | 33.2 | 32.2 | 32.0 | 30.5 | 35.0 | 30.2 | 33.2 | 32.1 |
| SenseNova-SI-1.3-Qwen3-VL-8B | 24.5 | 26.2 | 25.5 | 27.5 | 23.0 | 26.5 | 21.0 | 25.8 | 25.0 |
| Bagel-7B-MoT | 23.2 | 18.2 | 18.2 | 17.8 | 16.5 | 18.8 | 18.0 | 19.5 | 19.0 |
| JoyAI-Image | 33.7 | 31.8 | 33.8 | 33.5 | 33.0 | 33.8 | 31.5 | 32.2 | 32.9 |
| Step3-VL-10B | 47.2 | 45.8 | 44.0 | 43.8 | 49.5 | 48.2 | 47.2 | 50.0 | 47.0 |
| Qwen3-VL-8B-Instruct | 25.0 | 24.8 | 25.0 | 25.5 | 24.2 | 24.5 | 25.0 | 25.5 | 24.9 |
| ViLaSR | 39.5 | 39.0 | 36.0 | 37.5 | 35.0 | 34.0 | 38.5 | 37.0 | 37.1 |
| InternVL3-8B-Instruct | 40.5 | 34.2 | 33.8 | 33.5 | 31.5 | 32.5 | 34.5 | 33.8 | 34.6 |
| Qwen2-VL-7B-Instruct | 39.2 | 39.8 | 36.5 | 39.5 | 38.2 | 37.5 | 37.8 | 40.5 | 38.6 |
| Spatial-MLLM | 22.0 | 23.2 | 24.0 | 25.2 | 23.0 | 23.0 | 23.2 | 25.8 | 23.6 |
| InternVL3_5-8B | 27.5 | 27.5 | 26.5 | 26.0 | 25.0 | 25.8 | 25.2 | 25.0 | 26.1 |
| SenseNova-U1-8B-MoT | 16.8 | 20.2 | 19.2 | 16.0 | 17.0 | 19.5 | 18.5 | 20.0 | 18.3 |
| LatentUM-Base | 34.5 | 30.2 | 30.0 | 29.5 | 30.5 | 30.5 | 30.0 | 30.5 | 30.9 |
| Show-o2-7B | 53.8 | 53.5 | 52.0 | 51.8 | 53.0 | 51.5 | 53.0 | 53.0 | 52.8 |
| BLIP3o-8B | 41.3 | 34.8 | 36.8 | 36.5 | 36.2 | 34.0 | 34.0 | 34.8 | 36.4 |
| Cambrian-S-7B-LFP | 35.0 | 33.2 | 35.8 | 34.2 | 35.0 | 37.8 | 35.8 | 38.5 | 35.6 |
| Janus-Pro-7B | 45.0 | 49.8 | 46.8 | 46.8 | 48.5 | 40.0 | 46.0 | 42.2 | 45.6 |

### Oracle

| Model | base | rot90 | rot180 | rot270 | mirror_h | m_r90 | m_r180 | m_r270 | All |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GLM-4.6V-Flash | 34.3 | 30.8 | 30.8 | 30.8 | 29.8 | 32.8 | 27.0 | 32.2 | 31.2 |
| MiMo-Embodied-7B | 33.5 | 33.8 | 31.2 | 33.2 | 32.0 | 35.2 | 31.8 | 35.8 | 33.3 |
| SenseNova-SI-1.5-InternVL3-8B | 37.0 | 41.5 | 44.8 | 45.0 | 42.2 | 44.2 | 42.0 | 41.8 | 42.0 |
| Qwen2.5-VL-7B-Instruct | 59.3 | 57.8 | 60.0 | 58.0 | 58.0 | 57.8 | 56.8 | 57.8 | 58.2 |
| ThinkMorph-7B | 33.3 | 36.5 | 36.8 | 36.2 | 32.8 | 37.8 | 34.5 | 37.0 | 35.5 |
| SenseNova-SI-1.3-Qwen3-VL-8B | 26.2 | 27.8 | 26.0 | 27.2 | 25.2 | 29.0 | 23.8 | 28.0 | 26.6 |
| Bagel-7B-MoT | 27.5 | 27.0 | 23.2 | 23.8 | 22.8 | 26.8 | 23.2 | 27.0 | 25.3 |
| JoyAI-Image | 33.3 | 34.2 | 36.2 | 35.0 | 35.0 | 33.5 | 35.0 | 32.8 | 34.3 |
| Step3-VL-10B | 53.7 | 56.5 | 53.2 | 56.5 | 51.5 | 50.0 | 52.8 | 56.5 | 53.8 |
| Qwen3-VL-8B-Instruct | 26.3 | 25.8 | 24.8 | 25.5 | 24.5 | 25.2 | 26.0 | 25.8 | 25.5 |
| ViLaSR | 37.5 | 35.0 | 41.5 | 39.0 | 35.5 | 35.5 | 38.5 | 41.0 | 37.9 |
| InternVL3-8B-Instruct | 45.3 | 42.0 | 41.0 | 43.2 | 41.5 | 43.0 | 38.8 | 42.2 | 42.3 |
| Qwen2-VL-7B-Instruct | 42.3 | 42.8 | 41.2 | 41.8 | 39.8 | 42.5 | 40.5 | 42.8 | 41.7 |
| Spatial-MLLM | 21.7 | 23.5 | 24.2 | 25.5 | 22.8 | 23.5 | 24.5 | 24.8 | 23.7 |
| InternVL3_5-8B | 32.8 | 28.2 | 27.2 | 27.8 | 27.5 | 26.5 | 29.5 | 27.5 | 28.6 |
| SenseNova-U1-8B-MoT | 18.2 | 23.2 | 21.0 | 19.5 | 17.2 | 20.2 | 20.0 | 23.8 | 20.3 |
| LatentUM-Base | 35.0 | 30.0 | 30.8 | 30.2 | 31.8 | 32.0 | 30.8 | 31.2 | 31.7 |
| Show-o2-7B | 59.0 | 60.0 | 60.2 | 57.8 | 62.5 | 57.8 | 59.8 | 57.2 | 59.3 |
| BLIP3o-8B | 41.5 | 36.5 | 36.2 | 38.2 | 36.2 | 38.5 | 34.8 | 36.5 | 37.6 |
| Cambrian-S-7B-LFP | 33.5 | 34.0 | 34.5 | 34.5 | 37.0 | 37.2 | 35.2 | 39.8 | 35.6 |
| Janus-Pro-7B | 48.5 | 47.2 | 49.0 | 49.2 | 46.0 | 46.2 | 46.2 | 44.5 | 47.2 |

## 10. World variants

### Direct

| Model | interv | sham | All |
| --- | --- | --- | --- |
| GLM-4.6V-Flash | 28.6 | 32.0 | 30.3 |
| MiMo-Embodied-7B | 32.8 | 28.0 | 30.4 |
| SenseNova-SI-1.5-InternVL3-8B | 30.6 | 32.2 | 31.4 |
| Qwen2.5-VL-7B-Instruct | 22.7 | 45.9 | 34.3 |
| ThinkMorph-7B | 26.2 | 29.3 | 27.8 |
| SenseNova-SI-1.3-Qwen3-VL-8B | 27.9 | 36.7 | 32.3 |
| Bagel-7B-MoT | 33.8 | 24.2 | 29.0 |
| JoyAI-Image | 30.8 | 38.9 | 34.9 |
| Step3-VL-10B | 29.6 | 30.2 | 29.9 |
| Qwen3-VL-8B-Instruct | 29.3 | 34.0 | 31.7 |
| ViLaSR | 26.2 | 29.4 | 27.7 |
| InternVL3-8B-Instruct | 24.2 | 30.0 | 27.1 |
| Qwen2-VL-7B-Instruct | 26.6 | 35.2 | 30.9 |
| Spatial-MLLM | 28.2 | 17.8 | 23.0 |
| InternVL3_5-8B | 23.5 | 23.8 | 23.6 |
| SenseNova-U1-8B-MoT | 35.2 | 20.5 | 27.9 |
| LatentUM-Base | 24.7 | 27.4 | 26.0 |
| Show-o2-7B | 30.2 | 34.0 | 32.1 |
| BLIP3o-8B | 24.2 | 36.8 | 30.5 |
| Cambrian-S-7B-LFP | 21.2 | 27.0 | 24.1 |
| Janus-Pro-7B | 7.1 | 21.5 | 14.3 |

### Oracle

| Model | interv | sham | All |
| --- | --- | --- | --- |
| GLM-4.6V-Flash | 58.2 | 47.2 | 52.7 |
| MiMo-Embodied-7B | 40.4 | 31.4 | 35.9 |
| SenseNova-SI-1.5-InternVL3-8B | 35.8 | 33.2 | 34.5 |
| Qwen2.5-VL-7B-Instruct | 27.5 | 52.6 | 40.0 |
| ThinkMorph-7B | 37.2 | 34.6 | 35.9 |
| SenseNova-SI-1.3-Qwen3-VL-8B | 36.8 | 43.2 | 40.0 |
| Bagel-7B-MoT | 49.8 | 30.4 | 40.1 |
| JoyAI-Image | 41.0 | 43.3 | 42.2 |
| Step3-VL-10B | 40.9 | 40.7 | 40.8 |
| Qwen3-VL-8B-Instruct | 39.8 | 41.5 | 40.6 |
| ViLaSR | 27.9 | 31.2 | 29.3 |
| InternVL3-8B-Instruct | 26.4 | 34.0 | 30.2 |
| Qwen2-VL-7B-Instruct | 31.0 | 38.5 | 34.8 |
| Spatial-MLLM | 28.2 | 19.8 | 24.0 |
| InternVL3_5-8B | 26.4 | 26.7 | 26.5 |
| SenseNova-U1-8B-MoT | 38.8 | 19.5 | 29.1 |
| LatentUM-Base | 26.2 | 30.2 | 28.2 |
| Show-o2-7B | 38.8 | 39.8 | 39.3 |
| BLIP3o-8B | 24.8 | 35.0 | 29.9 |
| Cambrian-S-7B-LFP | 20.1 | 27.7 | 23.9 |
| Janus-Pro-7B | 6.7 | 23.3 | 15.0 |

## 11. Per-cell detail

Non-empty cells only.

| Model | Strategy | View | Task | Variant | Condition | Acc (%) | Correct | Answered | Total | Errors |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GLM-4.6V-Flash | direct | blank | t1 | base/direct | direct | 71.5 | 286 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | blank | t1 | base/oracle | oracle | 69.8 | 279 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | blank | t1 | transform/mirror_h/direct | direct | 69.8 | 279 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | blank | t1 | transform/mirror_h/oracle | oracle | 71.5 | 286 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | blank | t1 | transform/mirror_h_rot180/direct | direct | 69.2 | 277 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | blank | t1 | transform/mirror_h_rot180/oracle | oracle | 69.0 | 276 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | blank | t1 | transform/mirror_h_rot270/direct | direct | 69.5 | 278 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | blank | t1 | transform/mirror_h_rot270/oracle | oracle | 72.2 | 289 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | blank | t1 | transform/mirror_h_rot90/direct | direct | 71.0 | 284 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | blank | t1 | transform/mirror_h_rot90/oracle | oracle | 70.0 | 280 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | blank | t1 | transform/rot180/direct | direct | 71.0 | 284 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | blank | t1 | transform/rot180/oracle | oracle | 74.0 | 296 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | blank | t1 | transform/rot270/direct | direct | 73.2 | 293 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | blank | t1 | transform/rot270/oracle | oracle | 76.0 | 304 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | blank | t1 | transform/rot90/direct | direct | 69.5 | 278 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | blank | t1 | transform/rot90/oracle | oracle | 71.2 | 285 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | blank | t2 | base/direct | direct | 60.8 | 243 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | blank | t2 | base/oracle | oracle | 56.2 | 225 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | blank | t2 | transform/mirror_h/direct | direct | 65.2 | 261 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | blank | t2 | transform/mirror_h/oracle | oracle | 62.0 | 248 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | blank | t2 | transform/mirror_h_rot180/direct | direct | 63.0 | 252 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | blank | t2 | transform/mirror_h_rot180/oracle | oracle | 61.5 | 246 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | blank | t2 | transform/mirror_h_rot270/direct | direct | 62.0 | 248 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | blank | t2 | transform/mirror_h_rot270/oracle | oracle | 60.0 | 240 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | blank | t2 | transform/mirror_h_rot90/direct | direct | 61.5 | 246 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | blank | t2 | transform/mirror_h_rot90/oracle | oracle | 59.2 | 237 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | blank | t2 | transform/rot180/direct | direct | 64.0 | 256 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | blank | t2 | transform/rot180/oracle | oracle | 59.8 | 239 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | blank | t2 | transform/rot270/direct | direct | 60.8 | 243 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | blank | t2 | transform/rot270/oracle | oracle | 63.0 | 252 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | blank | t2 | transform/rot90/direct | direct | 64.2 | 257 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | blank | t2 | transform/rot90/oracle | oracle | 59.5 | 238 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | sat | t1 | base/direct | direct | 54.8 | 219 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | sat | t1 | base/oracle | oracle | 56.5 | 226 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | sat | t1 | transform/mirror_h/direct | direct | 65.8 | 263 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | sat | t1 | transform/mirror_h/oracle | oracle | 67.5 | 270 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | sat | t1 | transform/mirror_h_rot180/direct | direct | 67.8 | 271 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | sat | t1 | transform/mirror_h_rot180/oracle | oracle | 65.5 | 262 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | sat | t1 | transform/mirror_h_rot270/direct | direct | 68.5 | 274 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | sat | t1 | transform/mirror_h_rot270/oracle | oracle | 69.2 | 277 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | sat | t1 | transform/mirror_h_rot90/direct | direct | 69.2 | 277 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | sat | t1 | transform/mirror_h_rot90/oracle | oracle | 69.5 | 278 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | sat | t1 | transform/rot180/direct | direct | 70.8 | 283 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | sat | t1 | transform/rot180/oracle | oracle | 75.2 | 301 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | sat | t1 | transform/rot270/direct | direct | 73.0 | 292 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | sat | t1 | transform/rot270/oracle | oracle | 72.2 | 289 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | sat | t1 | transform/rot90/direct | direct | 67.0 | 268 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | sat | t1 | transform/rot90/oracle | oracle | 72.0 | 288 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | sat | t2 | base/direct | direct | 29.8 | 119 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | sat | t2 | base/oracle | oracle | 50.0 | 200 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | sat | t2 | transform/mirror_h/direct | direct | 55.2 | 221 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | sat | t2 | transform/mirror_h/oracle | oracle | 58.2 | 233 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | sat | t2 | transform/mirror_h_rot180/direct | direct | 51.5 | 206 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | sat | t2 | transform/mirror_h_rot180/oracle | oracle | 53.0 | 212 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | sat | t2 | transform/mirror_h_rot270/direct | direct | 57.2 | 229 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | sat | t2 | transform/mirror_h_rot270/oracle | oracle | 56.8 | 227 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | sat | t2 | transform/mirror_h_rot90/direct | direct | 58.0 | 232 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | sat | t2 | transform/mirror_h_rot90/oracle | oracle | 59.5 | 238 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | sat | t2 | transform/rot180/direct | direct | 58.8 | 235 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | sat | t2 | transform/rot180/oracle | oracle | 53.2 | 213 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | sat | t2 | transform/rot270/direct | direct | 61.2 | 245 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | sat | t2 | transform/rot270/oracle | oracle | 58.2 | 233 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | sat | t2 | transform/rot90/direct | direct | 57.2 | 229 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | sat | t2 | transform/rot90/oracle | oracle | 57.8 | 231 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | sat | t3 | base/direct | direct | 31.5 | 63 | 200 | 200 | 0 |
| GLM-4.6V-Flash | direct | sat | t3 | base/oracle | oracle | 32.5 | 65 | 200 | 200 | 0 |
| GLM-4.6V-Flash | direct | sat | t3 | transform/mirror_h/direct | direct | 28.5 | 57 | 200 | 200 | 0 |
| GLM-4.6V-Flash | direct | sat | t3 | transform/mirror_h/oracle | oracle | 36.0 | 72 | 200 | 200 | 0 |
| GLM-4.6V-Flash | direct | sat | t3 | transform/mirror_h_rot180/direct | direct | 33.0 | 66 | 200 | 200 | 0 |
| GLM-4.6V-Flash | direct | sat | t3 | transform/mirror_h_rot180/oracle | oracle | 32.0 | 64 | 200 | 200 | 0 |
| GLM-4.6V-Flash | direct | sat | t3 | transform/mirror_h_rot270/direct | direct | 35.0 | 70 | 200 | 200 | 0 |
| GLM-4.6V-Flash | direct | sat | t3 | transform/mirror_h_rot270/oracle | oracle | 38.5 | 77 | 200 | 200 | 0 |
| GLM-4.6V-Flash | direct | sat | t3 | transform/mirror_h_rot90/direct | direct | 30.5 | 61 | 200 | 200 | 0 |
| GLM-4.6V-Flash | direct | sat | t3 | transform/mirror_h_rot90/oracle | oracle | 37.0 | 74 | 200 | 200 | 0 |
| GLM-4.6V-Flash | direct | sat | t3 | transform/rot180/direct | direct | 29.5 | 59 | 200 | 200 | 0 |
| GLM-4.6V-Flash | direct | sat | t3 | transform/rot180/oracle | oracle | 34.5 | 69 | 200 | 200 | 0 |
| GLM-4.6V-Flash | direct | sat | t3 | transform/rot270/direct | direct | 32.0 | 64 | 200 | 200 | 0 |
| GLM-4.6V-Flash | direct | sat | t3 | transform/rot270/oracle | oracle | 36.5 | 73 | 200 | 200 | 0 |
| GLM-4.6V-Flash | direct | sat | t3 | transform/rot90/direct | direct | 32.0 | 64 | 200 | 200 | 0 |
| GLM-4.6V-Flash | direct | sat | t3 | transform/rot90/oracle | oracle | 38.0 | 76 | 200 | 200 | 0 |
| GLM-4.6V-Flash | direct | sat | t3 | world/intervention_001/direct | direct | 44.0 | 88 | 200 | 200 | 0 |
| GLM-4.6V-Flash | direct | sat | t3 | world/intervention_001/oracle | oracle | 45.0 | 90 | 200 | 200 | 0 |
| GLM-4.6V-Flash | direct | sat | t3 | world/sham_001/direct | direct | 31.0 | 62 | 200 | 200 | 0 |
| GLM-4.6V-Flash | direct | sat | t3 | world/sham_001/oracle | oracle | 31.0 | 62 | 200 | 200 | 0 |
| GLM-4.6V-Flash | direct | sat | t4 | base/direct | direct | 48.5 | 194 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | sat | t4 | base/oracle | oracle | 69.5 | 278 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | sat | t4 | transform/mirror_h/direct | direct | 49.5 | 198 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | sat | t4 | transform/mirror_h/oracle | oracle | 69.0 | 276 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | sat | t4 | transform/mirror_h_rot180/direct | direct | 48.0 | 192 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | sat | t4 | transform/mirror_h_rot180/oracle | oracle | 67.8 | 271 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | sat | t4 | transform/mirror_h_rot270/direct | direct | 49.0 | 196 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | sat | t4 | transform/mirror_h_rot270/oracle | oracle | 71.0 | 284 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | sat | t4 | transform/mirror_h_rot90/direct | direct | 49.5 | 198 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | sat | t4 | transform/mirror_h_rot90/oracle | oracle | 69.0 | 276 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | sat | t4 | transform/rot180/direct | direct | 47.8 | 191 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | sat | t4 | transform/rot180/oracle | oracle | 69.2 | 277 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | sat | t4 | transform/rot270/direct | direct | 48.5 | 194 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | sat | t4 | transform/rot270/oracle | oracle | 68.8 | 275 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | sat | t4 | transform/rot90/direct | direct | 47.5 | 190 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | sat | t4 | transform/rot90/oracle | oracle | 67.5 | 270 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | sat | t4 | world/intervention_001/direct | direct | 15.0 | 30 | 200 | 200 | 0 |
| GLM-4.6V-Flash | direct | sat | t4 | world/intervention_001/oracle | oracle | 82.0 | 164 | 200 | 200 | 0 |
| GLM-4.6V-Flash | direct | sat | t4 | world/sham_001/direct | direct | 42.0 | 84 | 200 | 200 | 0 |
| GLM-4.6V-Flash | direct | sat | t4 | world/sham_001/oracle | oracle | 68.5 | 137 | 200 | 200 | 0 |
| GLM-4.6V-Flash | direct | webrd04 | t1 | base/direct | direct | 71.5 | 286 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | webrd04 | t1 | base/oracle | oracle | 73.0 | 292 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | webrd04 | t2 | base/direct | direct | 56.2 | 225 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | webrd04 | t2 | base/oracle | oracle | 51.2 | 205 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | webrd04 | t3 | base/direct | direct | 31.5 | 63 | 200 | 200 | 0 |
| GLM-4.6V-Flash | direct | webrd04 | t3 | base/oracle | oracle | 41.5 | 83 | 200 | 200 | 0 |
| GLM-4.6V-Flash | direct | webrd04 | t3 | world/intervention_001/direct | direct | 44.0 | 88 | 200 | 200 | 0 |
| GLM-4.6V-Flash | direct | webrd04 | t3 | world/intervention_001/oracle | oracle | 44.0 | 88 | 200 | 200 | 0 |
| GLM-4.6V-Flash | direct | webrd04 | t3 | world/sham_001/direct | direct | 28.5 | 57 | 200 | 200 | 0 |
| GLM-4.6V-Flash | direct | webrd04 | t3 | world/sham_001/oracle | oracle | 36.0 | 72 | 200 | 200 | 0 |
| GLM-4.6V-Flash | direct | webrd04 | t4 | base/direct | direct | 43.8 | 175 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | webrd04 | t4 | base/oracle | oracle | 57.8 | 231 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | webrd04 | t4 | world/intervention_001/direct | direct | 16.5 | 33 | 200 | 200 | 0 |
| GLM-4.6V-Flash | direct | webrd04 | t4 | world/intervention_001/oracle | oracle | 56.5 | 113 | 200 | 200 | 0 |
| GLM-4.6V-Flash | direct | webrd04 | t4 | world/sham_001/direct | direct | 32.0 | 64 | 200 | 200 | 0 |
| GLM-4.6V-Flash | direct | webrd04 | t4 | world/sham_001/oracle | oracle | 53.5 | 107 | 200 | 200 | 0 |
| GLM-4.6V-Flash | direct | wprd01 | t1 | base/direct | direct | 56.2 | 225 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | wprd01 | t1 | base/oracle | oracle | 54.5 | 218 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | wprd01 | t1 | transform/mirror_h/direct | direct | 68.8 | 275 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | wprd01 | t1 | transform/mirror_h/oracle | oracle | 69.2 | 277 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | wprd01 | t1 | transform/mirror_h_rot180/direct | direct | 66.5 | 266 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | wprd01 | t1 | transform/mirror_h_rot180/oracle | oracle | 68.8 | 275 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | wprd01 | t1 | transform/mirror_h_rot270/direct | direct | 69.2 | 277 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | wprd01 | t1 | transform/mirror_h_rot270/oracle | oracle | 66.5 | 266 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | wprd01 | t1 | transform/mirror_h_rot90/direct | direct | 70.0 | 280 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | wprd01 | t1 | transform/mirror_h_rot90/oracle | oracle | 72.0 | 288 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | wprd01 | t1 | transform/rot180/direct | direct | 72.8 | 291 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | wprd01 | t1 | transform/rot180/oracle | oracle | 73.8 | 295 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | wprd01 | t1 | transform/rot270/direct | direct | 73.2 | 293 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | wprd01 | t1 | transform/rot270/oracle | oracle | 73.5 | 294 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | wprd01 | t1 | transform/rot90/direct | direct | 69.0 | 276 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | wprd01 | t1 | transform/rot90/oracle | oracle | 72.5 | 290 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | wprd01 | t2 | base/direct | direct | 28.8 | 115 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | wprd01 | t2 | base/oracle | oracle | 49.8 | 199 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | wprd01 | t2 | transform/mirror_h/direct | direct | 55.0 | 220 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | wprd01 | t2 | transform/mirror_h/oracle | oracle | 54.5 | 218 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | wprd01 | t2 | transform/mirror_h_rot180/direct | direct | 57.0 | 228 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | wprd01 | t2 | transform/mirror_h_rot180/oracle | oracle | 56.2 | 225 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | wprd01 | t2 | transform/mirror_h_rot270/direct | direct | 55.8 | 223 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | wprd01 | t2 | transform/mirror_h_rot270/oracle | oracle | 59.8 | 239 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | wprd01 | t2 | transform/mirror_h_rot90/direct | direct | 56.5 | 226 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | wprd01 | t2 | transform/mirror_h_rot90/oracle | oracle | 59.5 | 238 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | wprd01 | t2 | transform/rot180/direct | direct | 58.8 | 235 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | wprd01 | t2 | transform/rot180/oracle | oracle | 55.0 | 220 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | wprd01 | t2 | transform/rot270/direct | direct | 59.2 | 237 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | wprd01 | t2 | transform/rot270/oracle | oracle | 59.2 | 237 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | wprd01 | t2 | transform/rot90/direct | direct | 60.8 | 243 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | wprd01 | t2 | transform/rot90/oracle | oracle | 58.0 | 232 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | wprd01 | t3 | base/direct | direct | 28.5 | 57 | 200 | 200 | 0 |
| GLM-4.6V-Flash | direct | wprd01 | t3 | base/oracle | oracle | 29.0 | 58 | 200 | 200 | 0 |
| GLM-4.6V-Flash | direct | wprd01 | t3 | transform/mirror_h/direct | direct | 25.5 | 51 | 200 | 200 | 0 |
| GLM-4.6V-Flash | direct | wprd01 | t3 | transform/mirror_h/oracle | oracle | 23.5 | 47 | 200 | 200 | 0 |
| GLM-4.6V-Flash | direct | wprd01 | t3 | transform/mirror_h_rot180/direct | direct | 27.0 | 54 | 200 | 200 | 0 |
| GLM-4.6V-Flash | direct | wprd01 | t3 | transform/mirror_h_rot180/oracle | oracle | 22.0 | 44 | 200 | 200 | 0 |
| GLM-4.6V-Flash | direct | wprd01 | t3 | transform/mirror_h_rot270/direct | direct | 18.0 | 36 | 200 | 200 | 0 |
| GLM-4.6V-Flash | direct | wprd01 | t3 | transform/mirror_h_rot270/oracle | oracle | 26.0 | 52 | 200 | 200 | 0 |
| GLM-4.6V-Flash | direct | wprd01 | t3 | transform/mirror_h_rot90/direct | direct | 26.5 | 53 | 200 | 200 | 0 |
| GLM-4.6V-Flash | direct | wprd01 | t3 | transform/mirror_h_rot90/oracle | oracle | 28.5 | 57 | 200 | 200 | 0 |
| GLM-4.6V-Flash | direct | wprd01 | t3 | transform/rot180/direct | direct | 23.0 | 46 | 200 | 200 | 0 |
| GLM-4.6V-Flash | direct | wprd01 | t3 | transform/rot180/oracle | oracle | 27.0 | 54 | 200 | 200 | 0 |
| GLM-4.6V-Flash | direct | wprd01 | t3 | transform/rot270/direct | direct | 29.5 | 59 | 200 | 200 | 0 |
| GLM-4.6V-Flash | direct | wprd01 | t3 | transform/rot270/oracle | oracle | 25.0 | 50 | 200 | 200 | 0 |
| GLM-4.6V-Flash | direct | wprd01 | t3 | transform/rot90/direct | direct | 21.5 | 43 | 200 | 200 | 0 |
| GLM-4.6V-Flash | direct | wprd01 | t3 | transform/rot90/oracle | oracle | 23.5 | 47 | 200 | 200 | 0 |
| GLM-4.6V-Flash | direct | wprd01 | t3 | world/intervention_001/direct | direct | 46.0 | 92 | 200 | 200 | 0 |
| GLM-4.6V-Flash | direct | wprd01 | t3 | world/intervention_001/oracle | oracle | 49.0 | 98 | 200 | 200 | 0 |
| GLM-4.6V-Flash | direct | wprd01 | t3 | world/sham_001/direct | direct | 19.5 | 39 | 200 | 200 | 0 |
| GLM-4.6V-Flash | direct | wprd01 | t3 | world/sham_001/oracle | oracle | 24.5 | 49 | 200 | 200 | 0 |
| GLM-4.6V-Flash | direct | wprd01 | t4 | base/direct | direct | 52.2 | 209 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | wprd01 | t4 | base/oracle | oracle | 69.2 | 277 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | wprd01 | t4 | transform/mirror_h/direct | direct | 54.2 | 217 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | wprd01 | t4 | transform/mirror_h/oracle | oracle | 73.2 | 293 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | wprd01 | t4 | transform/mirror_h_rot180/direct | direct | 56.5 | 226 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | wprd01 | t4 | transform/mirror_h_rot180/oracle | oracle | 70.2 | 281 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | wprd01 | t4 | transform/mirror_h_rot270/direct | direct | 51.8 | 207 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | wprd01 | t4 | transform/mirror_h_rot270/oracle | oracle | 71.2 | 285 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | wprd01 | t4 | transform/mirror_h_rot90/direct | direct | 51.8 | 207 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | wprd01 | t4 | transform/mirror_h_rot90/oracle | oracle | 71.5 | 286 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | wprd01 | t4 | transform/rot180/direct | direct | 52.2 | 209 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | wprd01 | t4 | transform/rot180/oracle | oracle | 74.0 | 296 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | wprd01 | t4 | transform/rot270/direct | direct | 51.2 | 205 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | wprd01 | t4 | transform/rot270/oracle | oracle | 71.8 | 287 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | wprd01 | t4 | transform/rot90/direct | direct | 51.2 | 205 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | wprd01 | t4 | transform/rot90/oracle | oracle | 72.8 | 291 | 400 | 400 | 0 |
| GLM-4.6V-Flash | direct | wprd01 | t4 | world/intervention_001/direct | direct | 6.0 | 12 | 200 | 200 | 0 |
| GLM-4.6V-Flash | direct | wprd01 | t4 | world/intervention_001/oracle | oracle | 72.5 | 145 | 200 | 200 | 0 |
| GLM-4.6V-Flash | direct | wprd01 | t4 | world/sham_001/direct | direct | 39.0 | 78 | 200 | 200 | 0 |
| GLM-4.6V-Flash | direct | wprd01 | t4 | world/sham_001/oracle | oracle | 70.0 | 140 | 200 | 200 | 0 |
| MiMo-Embodied-7B | direct | blank | t1 | base/direct | direct | 76.2 | 305 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | blank | t1 | base/oracle | oracle | 73.2 | 293 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | blank | t1 | transform/mirror_h/direct | direct | 71.8 | 287 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | blank | t1 | transform/mirror_h/oracle | oracle | 74.5 | 298 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | blank | t1 | transform/mirror_h_rot180/direct | direct | 72.2 | 289 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | blank | t1 | transform/mirror_h_rot180/oracle | oracle | 72.8 | 291 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | blank | t1 | transform/mirror_h_rot270/direct | direct | 71.8 | 287 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | blank | t1 | transform/mirror_h_rot270/oracle | oracle | 70.2 | 281 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | blank | t1 | transform/mirror_h_rot90/direct | direct | 74.8 | 299 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | blank | t1 | transform/mirror_h_rot90/oracle | oracle | 73.5 | 294 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | blank | t1 | transform/rot180/direct | direct | 74.0 | 296 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | blank | t1 | transform/rot180/oracle | oracle | 76.2 | 305 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | blank | t1 | transform/rot270/direct | direct | 78.2 | 313 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | blank | t1 | transform/rot270/oracle | oracle | 77.0 | 308 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | blank | t1 | transform/rot90/direct | direct | 74.0 | 296 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | blank | t1 | transform/rot90/oracle | oracle | 74.2 | 297 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | blank | t2 | base/direct | direct | 61.8 | 247 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | blank | t2 | base/oracle | oracle | 53.2 | 213 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | blank | t2 | transform/mirror_h/direct | direct | 61.0 | 244 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | blank | t2 | transform/mirror_h/oracle | oracle | 61.2 | 245 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | blank | t2 | transform/mirror_h_rot180/direct | direct | 59.8 | 239 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | blank | t2 | transform/mirror_h_rot180/oracle | oracle | 56.8 | 227 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | blank | t2 | transform/mirror_h_rot270/direct | direct | 62.8 | 251 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | blank | t2 | transform/mirror_h_rot270/oracle | oracle | 57.2 | 229 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | blank | t2 | transform/mirror_h_rot90/direct | direct | 58.5 | 234 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | blank | t2 | transform/mirror_h_rot90/oracle | oracle | 54.8 | 219 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | blank | t2 | transform/rot180/direct | direct | 63.5 | 254 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | blank | t2 | transform/rot180/oracle | oracle | 60.5 | 242 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | blank | t2 | transform/rot270/direct | direct | 57.8 | 231 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | blank | t2 | transform/rot270/oracle | oracle | 58.8 | 235 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | blank | t2 | transform/rot90/direct | direct | 63.0 | 252 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | blank | t2 | transform/rot90/oracle | oracle | 57.8 | 231 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | sat | t1 | base/direct | direct | 72.2 | 289 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | sat | t1 | base/oracle | oracle | 71.0 | 284 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | sat | t1 | transform/mirror_h/direct | direct | 57.2 | 229 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | sat | t1 | transform/mirror_h/oracle | oracle | 65.0 | 260 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | sat | t1 | transform/mirror_h_rot180/direct | direct | 60.0 | 240 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | sat | t1 | transform/mirror_h_rot180/oracle | oracle | 63.0 | 252 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | sat | t1 | transform/mirror_h_rot270/direct | direct | 61.5 | 246 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | sat | t1 | transform/mirror_h_rot270/oracle | oracle | 63.0 | 252 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | sat | t1 | transform/mirror_h_rot90/direct | direct | 62.8 | 251 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | sat | t1 | transform/mirror_h_rot90/oracle | oracle | 66.8 | 267 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | sat | t1 | transform/rot180/direct | direct | 70.2 | 281 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | sat | t1 | transform/rot180/oracle | oracle | 73.8 | 295 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | sat | t1 | transform/rot270/direct | direct | 70.2 | 281 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | sat | t1 | transform/rot270/oracle | oracle | 75.0 | 300 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | sat | t1 | transform/rot90/direct | direct | 68.0 | 272 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | sat | t1 | transform/rot90/oracle | oracle | 71.0 | 284 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | sat | t2 | base/direct | direct | 54.8 | 219 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | sat | t2 | base/oracle | oracle | 54.0 | 216 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | sat | t2 | transform/mirror_h/direct | direct | 54.2 | 217 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | sat | t2 | transform/mirror_h/oracle | oracle | 53.8 | 215 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | sat | t2 | transform/mirror_h_rot180/direct | direct | 57.8 | 231 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | sat | t2 | transform/mirror_h_rot180/oracle | oracle | 58.8 | 235 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | sat | t2 | transform/mirror_h_rot270/direct | direct | 58.5 | 234 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | sat | t2 | transform/mirror_h_rot270/oracle | oracle | 59.2 | 237 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | sat | t2 | transform/mirror_h_rot90/direct | direct | 58.8 | 235 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | sat | t2 | transform/mirror_h_rot90/oracle | oracle | 56.5 | 226 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | sat | t2 | transform/rot180/direct | direct | 58.5 | 234 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | sat | t2 | transform/rot180/oracle | oracle | 55.2 | 221 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | sat | t2 | transform/rot270/direct | direct | 56.0 | 224 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | sat | t2 | transform/rot270/oracle | oracle | 53.2 | 213 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | sat | t2 | transform/rot90/direct | direct | 59.0 | 236 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | sat | t2 | transform/rot90/oracle | oracle | 59.0 | 236 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | sat | t3 | base/direct | direct | 34.0 | 68 | 200 | 200 | 0 |
| MiMo-Embodied-7B | direct | sat | t3 | base/oracle | oracle | 32.0 | 64 | 200 | 200 | 0 |
| MiMo-Embodied-7B | direct | sat | t3 | transform/mirror_h/direct | direct | 34.5 | 69 | 200 | 200 | 0 |
| MiMo-Embodied-7B | direct | sat | t3 | transform/mirror_h/oracle | oracle | 31.5 | 63 | 200 | 200 | 0 |
| MiMo-Embodied-7B | direct | sat | t3 | transform/mirror_h_rot180/direct | direct | 32.5 | 65 | 200 | 200 | 0 |
| MiMo-Embodied-7B | direct | sat | t3 | transform/mirror_h_rot180/oracle | oracle | 33.0 | 66 | 200 | 200 | 0 |
| MiMo-Embodied-7B | direct | sat | t3 | transform/mirror_h_rot270/direct | direct | 33.0 | 66 | 200 | 200 | 0 |
| MiMo-Embodied-7B | direct | sat | t3 | transform/mirror_h_rot270/oracle | oracle | 40.0 | 80 | 200 | 200 | 0 |
| MiMo-Embodied-7B | direct | sat | t3 | transform/mirror_h_rot90/direct | direct | 29.5 | 59 | 200 | 200 | 0 |
| MiMo-Embodied-7B | direct | sat | t3 | transform/mirror_h_rot90/oracle | oracle | 33.0 | 66 | 200 | 200 | 0 |
| MiMo-Embodied-7B | direct | sat | t3 | transform/rot180/direct | direct | 29.0 | 58 | 200 | 200 | 0 |
| MiMo-Embodied-7B | direct | sat | t3 | transform/rot180/oracle | oracle | 33.5 | 67 | 200 | 200 | 0 |
| MiMo-Embodied-7B | direct | sat | t3 | transform/rot270/direct | direct | 33.5 | 67 | 200 | 200 | 0 |
| MiMo-Embodied-7B | direct | sat | t3 | transform/rot270/oracle | oracle | 33.0 | 66 | 200 | 200 | 0 |
| MiMo-Embodied-7B | direct | sat | t3 | transform/rot90/direct | direct | 32.0 | 64 | 200 | 200 | 0 |
| MiMo-Embodied-7B | direct | sat | t3 | transform/rot90/oracle | oracle | 30.0 | 60 | 200 | 200 | 0 |
| MiMo-Embodied-7B | direct | sat | t3 | world/intervention_001/direct | direct | 43.5 | 87 | 200 | 200 | 0 |
| MiMo-Embodied-7B | direct | sat | t3 | world/intervention_001/oracle | oracle | 42.5 | 85 | 200 | 200 | 0 |
| MiMo-Embodied-7B | direct | sat | t3 | world/sham_001/direct | direct | 31.0 | 62 | 200 | 200 | 0 |
| MiMo-Embodied-7B | direct | sat | t3 | world/sham_001/oracle | oracle | 29.5 | 59 | 200 | 200 | 0 |
| MiMo-Embodied-7B | direct | sat | t4 | base/direct | direct | 40.0 | 160 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | sat | t4 | base/oracle | oracle | 47.8 | 191 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | sat | t4 | transform/mirror_h/direct | direct | 40.5 | 162 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | sat | t4 | transform/mirror_h/oracle | oracle | 48.0 | 192 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | sat | t4 | transform/mirror_h_rot180/direct | direct | 40.2 | 161 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | sat | t4 | transform/mirror_h_rot180/oracle | oracle | 48.0 | 192 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | sat | t4 | transform/mirror_h_rot270/direct | direct | 41.0 | 164 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | sat | t4 | transform/mirror_h_rot270/oracle | oracle | 44.2 | 177 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | sat | t4 | transform/mirror_h_rot90/direct | direct | 40.8 | 163 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | sat | t4 | transform/mirror_h_rot90/oracle | oracle | 45.0 | 180 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | sat | t4 | transform/rot180/direct | direct | 40.5 | 162 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | sat | t4 | transform/rot180/oracle | oracle | 49.2 | 197 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | sat | t4 | transform/rot270/direct | direct | 41.2 | 165 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | sat | t4 | transform/rot270/oracle | oracle | 47.0 | 188 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | sat | t4 | transform/rot90/direct | direct | 40.2 | 161 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | sat | t4 | transform/rot90/oracle | oracle | 46.8 | 187 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | sat | t4 | world/intervention_001/direct | direct | 23.5 | 47 | 200 | 200 | 0 |
| MiMo-Embodied-7B | direct | sat | t4 | world/intervention_001/oracle | oracle | 42.0 | 84 | 200 | 200 | 0 |
| MiMo-Embodied-7B | direct | sat | t4 | world/sham_001/direct | direct | 30.5 | 61 | 200 | 200 | 0 |
| MiMo-Embodied-7B | direct | sat | t4 | world/sham_001/oracle | oracle | 38.5 | 77 | 200 | 200 | 0 |
| MiMo-Embodied-7B | direct | webrd04 | t1 | base/direct | direct | 75.2 | 301 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | webrd04 | t1 | base/oracle | oracle | 74.5 | 298 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | webrd04 | t2 | base/direct | direct | 50.2 | 201 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | webrd04 | t2 | base/oracle | oracle | 54.2 | 217 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | webrd04 | t3 | base/direct | direct | 31.0 | 62 | 200 | 200 | 0 |
| MiMo-Embodied-7B | direct | webrd04 | t3 | base/oracle | oracle | 32.0 | 64 | 200 | 200 | 0 |
| MiMo-Embodied-7B | direct | webrd04 | t3 | world/intervention_001/direct | direct | 39.0 | 78 | 200 | 200 | 0 |
| MiMo-Embodied-7B | direct | webrd04 | t3 | world/intervention_001/oracle | oracle | 40.0 | 80 | 200 | 200 | 0 |
| MiMo-Embodied-7B | direct | webrd04 | t3 | world/sham_001/direct | direct | 23.0 | 46 | 200 | 200 | 0 |
| MiMo-Embodied-7B | direct | webrd04 | t3 | world/sham_001/oracle | oracle | 23.0 | 46 | 200 | 200 | 0 |
| MiMo-Embodied-7B | direct | webrd04 | t4 | base/direct | direct | 36.8 | 147 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | webrd04 | t4 | base/oracle | oracle | 50.2 | 201 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | webrd04 | t4 | world/intervention_001/direct | direct | 31.0 | 62 | 200 | 200 | 0 |
| MiMo-Embodied-7B | direct | webrd04 | t4 | world/intervention_001/oracle | oracle | 36.0 | 72 | 200 | 200 | 0 |
| MiMo-Embodied-7B | direct | webrd04 | t4 | world/sham_001/direct | direct | 31.0 | 62 | 200 | 200 | 0 |
| MiMo-Embodied-7B | direct | webrd04 | t4 | world/sham_001/oracle | oracle | 37.5 | 75 | 200 | 200 | 0 |
| MiMo-Embodied-7B | direct | wprd01 | t1 | base/direct | direct | 76.2 | 305 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | wprd01 | t1 | base/oracle | oracle | 75.5 | 302 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | wprd01 | t1 | transform/mirror_h/direct | direct | 67.5 | 270 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | wprd01 | t1 | transform/mirror_h/oracle | oracle | 70.8 | 283 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | wprd01 | t1 | transform/mirror_h_rot180/direct | direct | 65.8 | 263 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | wprd01 | t1 | transform/mirror_h_rot180/oracle | oracle | 68.8 | 275 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | wprd01 | t1 | transform/mirror_h_rot270/direct | direct | 67.0 | 268 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | wprd01 | t1 | transform/mirror_h_rot270/oracle | oracle | 70.5 | 282 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | wprd01 | t1 | transform/mirror_h_rot90/direct | direct | 71.5 | 286 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | wprd01 | t1 | transform/mirror_h_rot90/oracle | oracle | 72.2 | 289 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | wprd01 | t1 | transform/rot180/direct | direct | 74.8 | 299 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | wprd01 | t1 | transform/rot180/oracle | oracle | 72.8 | 291 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | wprd01 | t1 | transform/rot270/direct | direct | 73.8 | 295 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | wprd01 | t1 | transform/rot270/oracle | oracle | 73.2 | 293 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | wprd01 | t1 | transform/rot90/direct | direct | 73.2 | 293 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | wprd01 | t1 | transform/rot90/oracle | oracle | 74.8 | 299 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | wprd01 | t2 | base/direct | direct | 53.5 | 214 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | wprd01 | t2 | base/oracle | oracle | 56.5 | 226 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | wprd01 | t2 | transform/mirror_h/direct | direct | 54.2 | 217 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | wprd01 | t2 | transform/mirror_h/oracle | oracle | 54.8 | 219 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | wprd01 | t2 | transform/mirror_h_rot180/direct | direct | 52.2 | 209 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | wprd01 | t2 | transform/mirror_h_rot180/oracle | oracle | 54.2 | 217 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | wprd01 | t2 | transform/mirror_h_rot270/direct | direct | 55.8 | 223 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | wprd01 | t2 | transform/mirror_h_rot270/oracle | oracle | 59.2 | 237 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | wprd01 | t2 | transform/mirror_h_rot90/direct | direct | 57.2 | 229 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | wprd01 | t2 | transform/mirror_h_rot90/oracle | oracle | 58.2 | 233 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | wprd01 | t2 | transform/rot180/direct | direct | 57.0 | 228 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | wprd01 | t2 | transform/rot180/oracle | oracle | 60.0 | 240 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | wprd01 | t2 | transform/rot270/direct | direct | 52.0 | 208 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | wprd01 | t2 | transform/rot270/oracle | oracle | 58.5 | 234 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | wprd01 | t2 | transform/rot90/direct | direct | 54.2 | 217 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | wprd01 | t2 | transform/rot90/oracle | oracle | 58.2 | 233 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | wprd01 | t3 | base/direct | direct | 34.0 | 68 | 200 | 200 | 0 |
| MiMo-Embodied-7B | direct | wprd01 | t3 | base/oracle | oracle | 36.5 | 73 | 200 | 200 | 0 |
| MiMo-Embodied-7B | direct | wprd01 | t3 | transform/mirror_h/direct | direct | 30.5 | 61 | 200 | 200 | 0 |
| MiMo-Embodied-7B | direct | wprd01 | t3 | transform/mirror_h/oracle | oracle | 32.5 | 65 | 200 | 200 | 0 |
| MiMo-Embodied-7B | direct | wprd01 | t3 | transform/mirror_h_rot180/direct | direct | 32.5 | 65 | 200 | 200 | 0 |
| MiMo-Embodied-7B | direct | wprd01 | t3 | transform/mirror_h_rot180/oracle | oracle | 30.5 | 61 | 200 | 200 | 0 |
| MiMo-Embodied-7B | direct | wprd01 | t3 | transform/mirror_h_rot270/direct | direct | 34.5 | 69 | 200 | 200 | 0 |
| MiMo-Embodied-7B | direct | wprd01 | t3 | transform/mirror_h_rot270/oracle | oracle | 31.5 | 63 | 200 | 200 | 0 |
| MiMo-Embodied-7B | direct | wprd01 | t3 | transform/mirror_h_rot90/direct | direct | 30.0 | 60 | 200 | 200 | 0 |
| MiMo-Embodied-7B | direct | wprd01 | t3 | transform/mirror_h_rot90/oracle | oracle | 37.5 | 75 | 200 | 200 | 0 |
| MiMo-Embodied-7B | direct | wprd01 | t3 | transform/rot180/direct | direct | 33.0 | 66 | 200 | 200 | 0 |
| MiMo-Embodied-7B | direct | wprd01 | t3 | transform/rot180/oracle | oracle | 29.0 | 58 | 200 | 200 | 0 |
| MiMo-Embodied-7B | direct | wprd01 | t3 | transform/rot270/direct | direct | 29.5 | 59 | 200 | 200 | 0 |
| MiMo-Embodied-7B | direct | wprd01 | t3 | transform/rot270/oracle | oracle | 33.5 | 67 | 200 | 200 | 0 |
| MiMo-Embodied-7B | direct | wprd01 | t3 | transform/rot90/direct | direct | 29.0 | 58 | 200 | 200 | 0 |
| MiMo-Embodied-7B | direct | wprd01 | t3 | transform/rot90/oracle | oracle | 37.5 | 75 | 200 | 200 | 0 |
| MiMo-Embodied-7B | direct | wprd01 | t3 | world/intervention_001/direct | direct | 36.5 | 73 | 200 | 200 | 0 |
| MiMo-Embodied-7B | direct | wprd01 | t3 | world/intervention_001/oracle | oracle | 39.0 | 78 | 200 | 200 | 0 |
| MiMo-Embodied-7B | direct | wprd01 | t3 | world/sham_001/direct | direct | 23.5 | 47 | 200 | 200 | 0 |
| MiMo-Embodied-7B | direct | wprd01 | t3 | world/sham_001/oracle | oracle | 22.5 | 45 | 200 | 200 | 0 |
| MiMo-Embodied-7B | direct | wprd01 | t4 | base/direct | direct | 45.2 | 181 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | wprd01 | t4 | base/oracle | oracle | 55.2 | 221 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | wprd01 | t4 | transform/mirror_h/direct | direct | 43.8 | 175 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | wprd01 | t4 | transform/mirror_h/oracle | oracle | 53.8 | 215 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | wprd01 | t4 | transform/mirror_h_rot180/direct | direct | 46.2 | 185 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | wprd01 | t4 | transform/mirror_h_rot180/oracle | oracle | 54.8 | 219 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | wprd01 | t4 | transform/mirror_h_rot270/direct | direct | 46.2 | 185 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | wprd01 | t4 | transform/mirror_h_rot270/oracle | oracle | 56.5 | 226 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | wprd01 | t4 | transform/mirror_h_rot90/direct | direct | 42.0 | 168 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | wprd01 | t4 | transform/mirror_h_rot90/oracle | oracle | 56.0 | 224 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | wprd01 | t4 | transform/rot180/direct | direct | 44.2 | 177 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | wprd01 | t4 | transform/rot180/oracle | oracle | 52.5 | 210 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | wprd01 | t4 | transform/rot270/direct | direct | 45.8 | 183 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | wprd01 | t4 | transform/rot270/oracle | oracle | 53.8 | 215 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | wprd01 | t4 | transform/rot90/direct | direct | 43.2 | 173 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | wprd01 | t4 | transform/rot90/oracle | oracle | 53.2 | 213 | 400 | 400 | 0 |
| MiMo-Embodied-7B | direct | wprd01 | t4 | world/intervention_001/direct | direct | 23.5 | 47 | 200 | 200 | 0 |
| MiMo-Embodied-7B | direct | wprd01 | t4 | world/intervention_001/oracle | oracle | 43.0 | 86 | 200 | 200 | 0 |
| MiMo-Embodied-7B | direct | wprd01 | t4 | world/sham_001/direct | direct | 29.0 | 58 | 200 | 200 | 0 |
| MiMo-Embodied-7B | direct | wprd01 | t4 | world/sham_001/oracle | oracle | 37.5 | 75 | 200 | 200 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | blank | t1 | base/direct | direct | 74.0 | 296 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | blank | t1 | base/oracle | oracle | 77.8 | 311 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | blank | t1 | transform/mirror_h/direct | direct | 57.8 | 231 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | blank | t1 | transform/mirror_h/oracle | oracle | 61.0 | 244 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | blank | t1 | transform/mirror_h_rot180/direct | direct | 51.0 | 204 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | blank | t1 | transform/mirror_h_rot180/oracle | oracle | 53.8 | 215 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | blank | t1 | transform/mirror_h_rot270/direct | direct | 53.5 | 214 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | blank | t1 | transform/mirror_h_rot270/oracle | oracle | 57.8 | 231 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | blank | t1 | transform/mirror_h_rot90/direct | direct | 60.2 | 241 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | blank | t1 | transform/mirror_h_rot90/oracle | oracle | 61.2 | 245 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | blank | t1 | transform/rot180/direct | direct | 74.8 | 299 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | blank | t1 | transform/rot180/oracle | oracle | 77.2 | 309 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | blank | t1 | transform/rot270/direct | direct | 75.2 | 301 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | blank | t1 | transform/rot270/oracle | oracle | 77.8 | 311 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | blank | t1 | transform/rot90/direct | direct | 69.2 | 277 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | blank | t1 | transform/rot90/oracle | oracle | 69.8 | 279 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | blank | t2 | base/direct | direct | 60.5 | 242 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | blank | t2 | base/oracle | oracle | 66.5 | 266 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | blank | t2 | transform/mirror_h/direct | direct | 62.0 | 248 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | blank | t2 | transform/mirror_h/oracle | oracle | 67.5 | 270 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | blank | t2 | transform/mirror_h_rot180/direct | direct | 63.0 | 252 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | blank | t2 | transform/mirror_h_rot180/oracle | oracle | 69.5 | 278 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | blank | t2 | transform/mirror_h_rot270/direct | direct | 63.8 | 255 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | blank | t2 | transform/mirror_h_rot270/oracle | oracle | 68.5 | 274 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | blank | t2 | transform/mirror_h_rot90/direct | direct | 65.5 | 262 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | blank | t2 | transform/mirror_h_rot90/oracle | oracle | 68.2 | 273 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | blank | t2 | transform/rot180/direct | direct | 61.8 | 247 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | blank | t2 | transform/rot180/oracle | oracle | 64.5 | 258 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | blank | t2 | transform/rot270/direct | direct | 64.5 | 258 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | blank | t2 | transform/rot270/oracle | oracle | 64.0 | 256 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | blank | t2 | transform/rot90/direct | direct | 64.8 | 259 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | blank | t2 | transform/rot90/oracle | oracle | 65.8 | 263 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | sat | t1 | base/direct | direct | 68.0 | 272 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | sat | t1 | base/oracle | oracle | 75.2 | 301 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | sat | t1 | transform/mirror_h/direct | direct | 59.2 | 237 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | sat | t1 | transform/mirror_h/oracle | oracle | 63.2 | 253 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | sat | t1 | transform/mirror_h_rot180/direct | direct | 56.0 | 224 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | sat | t1 | transform/mirror_h_rot180/oracle | oracle | 59.5 | 238 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | sat | t1 | transform/mirror_h_rot270/direct | direct | 52.8 | 211 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | sat | t1 | transform/mirror_h_rot270/oracle | oracle | 55.8 | 223 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | sat | t1 | transform/mirror_h_rot90/direct | direct | 64.2 | 257 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | sat | t1 | transform/mirror_h_rot90/oracle | oracle | 68.0 | 272 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | sat | t1 | transform/rot180/direct | direct | 70.5 | 282 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | sat | t1 | transform/rot180/oracle | oracle | 77.5 | 310 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | sat | t1 | transform/rot270/direct | direct | 70.2 | 281 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | sat | t1 | transform/rot270/oracle | oracle | 80.2 | 321 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | sat | t1 | transform/rot90/direct | direct | 65.8 | 263 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | sat | t1 | transform/rot90/oracle | oracle | 71.0 | 284 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | sat | t2 | base/direct | direct | 60.8 | 243 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | sat | t2 | base/oracle | oracle | 59.0 | 236 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | sat | t2 | transform/mirror_h/direct | direct | 61.5 | 246 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | sat | t2 | transform/mirror_h/oracle | oracle | 61.8 | 247 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | sat | t2 | transform/mirror_h_rot180/direct | direct | 62.8 | 251 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | sat | t2 | transform/mirror_h_rot180/oracle | oracle | 66.5 | 266 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | sat | t2 | transform/mirror_h_rot270/direct | direct | 61.0 | 244 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | sat | t2 | transform/mirror_h_rot270/oracle | oracle | 65.0 | 260 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | sat | t2 | transform/mirror_h_rot90/direct | direct | 63.2 | 253 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | sat | t2 | transform/mirror_h_rot90/oracle | oracle | 64.5 | 258 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | sat | t2 | transform/rot180/direct | direct | 57.5 | 230 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | sat | t2 | transform/rot180/oracle | oracle | 62.0 | 248 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | sat | t2 | transform/rot270/direct | direct | 60.5 | 242 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | sat | t2 | transform/rot270/oracle | oracle | 61.8 | 247 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | sat | t2 | transform/rot90/direct | direct | 59.5 | 238 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | sat | t2 | transform/rot90/oracle | oracle | 62.5 | 250 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | sat | t3 | base/direct | direct | 42.5 | 85 | 200 | 200 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | sat | t3 | base/oracle | oracle | 42.5 | 85 | 200 | 200 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | sat | t3 | transform/mirror_h/direct | direct | 43.5 | 87 | 200 | 200 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | sat | t3 | transform/mirror_h/oracle | oracle | 42.5 | 85 | 200 | 200 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | sat | t3 | transform/mirror_h_rot180/direct | direct | 44.5 | 89 | 200 | 200 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | sat | t3 | transform/mirror_h_rot180/oracle | oracle | 43.5 | 87 | 200 | 200 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | sat | t3 | transform/mirror_h_rot270/direct | direct | 43.0 | 86 | 200 | 200 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | sat | t3 | transform/mirror_h_rot270/oracle | oracle | 39.0 | 78 | 200 | 200 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | sat | t3 | transform/mirror_h_rot90/direct | direct | 44.5 | 89 | 200 | 200 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | sat | t3 | transform/mirror_h_rot90/oracle | oracle | 43.5 | 87 | 200 | 200 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | sat | t3 | transform/rot180/direct | direct | 43.5 | 87 | 200 | 200 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | sat | t3 | transform/rot180/oracle | oracle | 44.5 | 89 | 200 | 200 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | sat | t3 | transform/rot270/direct | direct | 43.0 | 86 | 200 | 200 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | sat | t3 | transform/rot270/oracle | oracle | 42.5 | 85 | 200 | 200 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | sat | t3 | transform/rot90/direct | direct | 43.0 | 86 | 200 | 200 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | sat | t3 | transform/rot90/oracle | oracle | 38.5 | 77 | 200 | 200 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | sat | t3 | world/intervention_001/direct | direct | 20.5 | 41 | 200 | 200 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | sat | t3 | world/intervention_001/oracle | oracle | 23.0 | 46 | 200 | 200 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | sat | t3 | world/sham_001/direct | direct | 44.5 | 89 | 200 | 200 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | sat | t3 | world/sham_001/oracle | oracle | 42.5 | 85 | 200 | 200 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | sat | t4 | base/direct | direct | 30.2 | 121 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | sat | t4 | base/oracle | oracle | 32.8 | 131 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | sat | t4 | transform/mirror_h/direct | direct | 32.8 | 131 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | sat | t4 | transform/mirror_h/oracle | oracle | 34.2 | 137 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | sat | t4 | transform/mirror_h_rot180/direct | direct | 30.2 | 121 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | sat | t4 | transform/mirror_h_rot180/oracle | oracle | 36.8 | 147 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | sat | t4 | transform/mirror_h_rot270/direct | direct | 31.2 | 125 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | sat | t4 | transform/mirror_h_rot270/oracle | oracle | 37.5 | 150 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | sat | t4 | transform/mirror_h_rot90/direct | direct | 31.2 | 125 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | sat | t4 | transform/mirror_h_rot90/oracle | oracle | 37.5 | 150 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | sat | t4 | transform/rot180/direct | direct | 33.0 | 132 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | sat | t4 | transform/rot180/oracle | oracle | 36.5 | 146 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | sat | t4 | transform/rot270/direct | direct | 35.5 | 142 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | sat | t4 | transform/rot270/oracle | oracle | 38.0 | 152 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | sat | t4 | transform/rot90/direct | direct | 30.8 | 123 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | sat | t4 | transform/rot90/oracle | oracle | 34.8 | 139 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | sat | t4 | world/intervention_001/direct | direct | 32.0 | 64 | 200 | 200 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | sat | t4 | world/intervention_001/oracle | oracle | 43.5 | 87 | 200 | 200 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | sat | t4 | world/sham_001/direct | direct | 24.0 | 48 | 200 | 200 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | sat | t4 | world/sham_001/oracle | oracle | 28.0 | 56 | 200 | 200 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | webrd04 | t1 | base/direct | direct | 71.0 | 284 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | webrd04 | t1 | base/oracle | oracle | 71.0 | 284 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | webrd04 | t2 | base/direct | direct | 54.5 | 218 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | webrd04 | t2 | base/oracle | oracle | 58.5 | 234 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | webrd04 | t3 | base/direct | direct | 33.0 | 66 | 200 | 200 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | webrd04 | t3 | base/oracle | oracle | 29.0 | 58 | 200 | 200 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | webrd04 | t3 | world/intervention_001/direct | direct | 27.5 | 55 | 200 | 200 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | webrd04 | t3 | world/intervention_001/oracle | oracle | 30.0 | 60 | 200 | 200 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | webrd04 | t3 | world/sham_001/direct | direct | 40.5 | 81 | 200 | 200 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | webrd04 | t3 | world/sham_001/oracle | oracle | 37.5 | 75 | 200 | 200 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | webrd04 | t4 | base/direct | direct | 32.2 | 129 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | webrd04 | t4 | base/oracle | oracle | 30.8 | 123 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | webrd04 | t4 | world/intervention_001/direct | direct | 34.0 | 68 | 200 | 200 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | webrd04 | t4 | world/intervention_001/oracle | oracle | 37.5 | 75 | 200 | 200 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | webrd04 | t4 | world/sham_001/direct | direct | 21.0 | 42 | 200 | 200 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | webrd04 | t4 | world/sham_001/oracle | oracle | 24.5 | 49 | 200 | 200 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | wprd01 | t1 | base/direct | direct | 77.5 | 310 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | wprd01 | t1 | base/oracle | oracle | 76.0 | 304 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | wprd01 | t1 | transform/mirror_h/direct | direct | 69.0 | 276 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | wprd01 | t1 | transform/mirror_h/oracle | oracle | 67.2 | 269 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | wprd01 | t1 | transform/mirror_h_rot180/direct | direct | 63.8 | 255 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | wprd01 | t1 | transform/mirror_h_rot180/oracle | oracle | 61.8 | 247 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | wprd01 | t1 | transform/mirror_h_rot270/direct | direct | 63.0 | 252 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | wprd01 | t1 | transform/mirror_h_rot270/oracle | oracle | 61.8 | 247 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | wprd01 | t1 | transform/mirror_h_rot90/direct | direct | 68.5 | 274 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | wprd01 | t1 | transform/mirror_h_rot90/oracle | oracle | 69.0 | 276 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | wprd01 | t1 | transform/rot180/direct | direct | 76.5 | 306 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | wprd01 | t1 | transform/rot180/oracle | oracle | 77.2 | 309 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | wprd01 | t1 | transform/rot270/direct | direct | 82.0 | 328 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | wprd01 | t1 | transform/rot270/oracle | oracle | 82.5 | 330 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | wprd01 | t1 | transform/rot90/direct | direct | 76.2 | 305 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | wprd01 | t1 | transform/rot90/oracle | oracle | 76.2 | 305 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | wprd01 | t2 | base/direct | direct | 58.0 | 232 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | wprd01 | t2 | base/oracle | oracle | 58.8 | 235 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | wprd01 | t2 | transform/mirror_h/direct | direct | 64.8 | 259 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | wprd01 | t2 | transform/mirror_h/oracle | oracle | 68.8 | 275 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | wprd01 | t2 | transform/mirror_h_rot180/direct | direct | 66.5 | 266 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | wprd01 | t2 | transform/mirror_h_rot180/oracle | oracle | 67.8 | 271 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | wprd01 | t2 | transform/mirror_h_rot270/direct | direct | 66.8 | 267 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | wprd01 | t2 | transform/mirror_h_rot270/oracle | oracle | 69.0 | 276 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | wprd01 | t2 | transform/mirror_h_rot90/direct | direct | 65.0 | 260 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | wprd01 | t2 | transform/mirror_h_rot90/oracle | oracle | 64.8 | 259 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | wprd01 | t2 | transform/rot180/direct | direct | 62.8 | 251 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | wprd01 | t2 | transform/rot180/oracle | oracle | 64.5 | 258 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | wprd01 | t2 | transform/rot270/direct | direct | 62.2 | 249 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | wprd01 | t2 | transform/rot270/oracle | oracle | 64.2 | 257 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | wprd01 | t2 | transform/rot90/direct | direct | 63.5 | 254 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | wprd01 | t2 | transform/rot90/oracle | oracle | 66.2 | 265 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | wprd01 | t3 | base/direct | direct | 41.5 | 83 | 200 | 200 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | wprd01 | t3 | base/oracle | oracle | 39.5 | 79 | 200 | 200 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | wprd01 | t3 | transform/mirror_h/direct | direct | 41.0 | 82 | 200 | 200 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | wprd01 | t3 | transform/mirror_h/oracle | oracle | 42.0 | 84 | 200 | 200 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | wprd01 | t3 | transform/mirror_h_rot180/direct | direct | 38.0 | 76 | 200 | 200 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | wprd01 | t3 | transform/mirror_h_rot180/oracle | oracle | 40.5 | 81 | 200 | 200 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | wprd01 | t3 | transform/mirror_h_rot270/direct | direct | 42.5 | 85 | 200 | 200 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | wprd01 | t3 | transform/mirror_h_rot270/oracle | oracle | 44.5 | 89 | 200 | 200 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | wprd01 | t3 | transform/mirror_h_rot90/direct | direct | 46.5 | 93 | 200 | 200 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | wprd01 | t3 | transform/mirror_h_rot90/oracle | oracle | 45.0 | 90 | 200 | 200 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | wprd01 | t3 | transform/rot180/direct | direct | 43.5 | 87 | 200 | 200 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | wprd01 | t3 | transform/rot180/oracle | oracle | 45.0 | 90 | 200 | 200 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | wprd01 | t3 | transform/rot270/direct | direct | 46.5 | 93 | 200 | 200 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | wprd01 | t3 | transform/rot270/oracle | oracle | 47.5 | 95 | 200 | 200 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | wprd01 | t3 | transform/rot90/direct | direct | 41.5 | 83 | 200 | 200 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | wprd01 | t3 | transform/rot90/oracle | oracle | 44.5 | 89 | 200 | 200 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | wprd01 | t3 | world/intervention_001/direct | direct | 35.0 | 70 | 200 | 200 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | wprd01 | t3 | world/intervention_001/oracle | oracle | 36.5 | 73 | 200 | 200 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | wprd01 | t3 | world/sham_001/direct | direct | 37.0 | 74 | 200 | 200 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | wprd01 | t3 | world/sham_001/oracle | oracle | 42.5 | 85 | 200 | 200 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | wprd01 | t4 | base/direct | direct | 33.2 | 133 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | wprd01 | t4 | base/oracle | oracle | 33.0 | 132 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | wprd01 | t4 | transform/mirror_h/direct | direct | 30.8 | 123 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | wprd01 | t4 | transform/mirror_h/oracle | oracle | 34.2 | 137 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | wprd01 | t4 | transform/mirror_h_rot180/direct | direct | 33.8 | 135 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | wprd01 | t4 | transform/mirror_h_rot180/oracle | oracle | 35.2 | 141 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | wprd01 | t4 | transform/mirror_h_rot270/direct | direct | 32.2 | 129 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | wprd01 | t4 | transform/mirror_h_rot270/oracle | oracle | 32.8 | 131 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | wprd01 | t4 | transform/mirror_h_rot90/direct | direct | 31.2 | 125 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | wprd01 | t4 | transform/mirror_h_rot90/oracle | oracle | 32.8 | 131 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | wprd01 | t4 | transform/rot180/direct | direct | 32.0 | 128 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | wprd01 | t4 | transform/rot180/oracle | oracle | 35.5 | 142 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | wprd01 | t4 | transform/rot270/direct | direct | 30.8 | 123 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | wprd01 | t4 | transform/rot270/oracle | oracle | 33.2 | 133 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | wprd01 | t4 | transform/rot90/direct | direct | 32.8 | 131 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | wprd01 | t4 | transform/rot90/oracle | oracle | 35.5 | 142 | 400 | 400 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | wprd01 | t4 | world/intervention_001/direct | direct | 34.5 | 69 | 200 | 200 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | wprd01 | t4 | world/intervention_001/oracle | oracle | 44.5 | 89 | 200 | 200 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | wprd01 | t4 | world/sham_001/direct | direct | 26.0 | 52 | 200 | 200 | 0 |
| SenseNova-SI-1.5-InternVL3-8B | direct | wprd01 | t4 | world/sham_001/oracle | oracle | 24.0 | 48 | 200 | 200 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | blank | t1 | base/direct | direct | 54.0 | 216 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | blank | t1 | base/oracle | oracle | 62.2 | 249 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | blank | t1 | transform/mirror_h/direct | direct | 60.2 | 241 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | blank | t1 | transform/mirror_h/oracle | oracle | 69.0 | 276 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | blank | t1 | transform/mirror_h_rot180/direct | direct | 59.8 | 239 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | blank | t1 | transform/mirror_h_rot180/oracle | oracle | 64.5 | 258 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | blank | t1 | transform/mirror_h_rot270/direct | direct | 57.5 | 230 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | blank | t1 | transform/mirror_h_rot270/oracle | oracle | 58.2 | 233 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | blank | t1 | transform/mirror_h_rot90/direct | direct | 47.8 | 191 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | blank | t1 | transform/mirror_h_rot90/oracle | oracle | 60.0 | 240 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | blank | t1 | transform/rot180/direct | direct | 55.8 | 223 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | blank | t1 | transform/rot180/oracle | oracle | 61.8 | 247 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | blank | t1 | transform/rot270/direct | direct | 64.2 | 257 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | blank | t1 | transform/rot270/oracle | oracle | 67.8 | 271 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | blank | t1 | transform/rot90/direct | direct | 60.8 | 243 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | blank | t1 | transform/rot90/oracle | oracle | 66.0 | 264 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | blank | t2 | base/direct | direct | 57.0 | 228 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | blank | t2 | base/oracle | oracle | 56.0 | 224 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | blank | t2 | transform/mirror_h/direct | direct | 59.2 | 237 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | blank | t2 | transform/mirror_h/oracle | oracle | 52.2 | 209 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | blank | t2 | transform/mirror_h_rot180/direct | direct | 59.8 | 239 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | blank | t2 | transform/mirror_h_rot180/oracle | oracle | 55.0 | 220 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | blank | t2 | transform/mirror_h_rot270/direct | direct | 57.5 | 230 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | blank | t2 | transform/mirror_h_rot270/oracle | oracle | 52.8 | 211 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | blank | t2 | transform/mirror_h_rot90/direct | direct | 57.8 | 231 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | blank | t2 | transform/mirror_h_rot90/oracle | oracle | 51.0 | 204 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | blank | t2 | transform/rot180/direct | direct | 59.2 | 237 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | blank | t2 | transform/rot180/oracle | oracle | 49.5 | 198 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | blank | t2 | transform/rot270/direct | direct | 59.2 | 237 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | blank | t2 | transform/rot270/oracle | oracle | 52.2 | 209 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | blank | t2 | transform/rot90/direct | direct | 55.2 | 221 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | blank | t2 | transform/rot90/oracle | oracle | 51.0 | 204 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | sat | t1 | base/direct | direct | 69.0 | 276 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | sat | t1 | base/oracle | oracle | 70.5 | 282 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | sat | t1 | transform/mirror_h/direct | direct | 55.8 | 223 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | sat | t1 | transform/mirror_h/oracle | oracle | 64.8 | 259 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | sat | t1 | transform/mirror_h_rot180/direct | direct | 56.2 | 225 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | sat | t1 | transform/mirror_h_rot180/oracle | oracle | 60.2 | 241 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | sat | t1 | transform/mirror_h_rot270/direct | direct | 53.0 | 212 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | sat | t1 | transform/mirror_h_rot270/oracle | oracle | 58.5 | 234 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | sat | t1 | transform/mirror_h_rot90/direct | direct | 46.5 | 186 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | sat | t1 | transform/mirror_h_rot90/oracle | oracle | 55.5 | 222 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | sat | t1 | transform/rot180/direct | direct | 55.0 | 220 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | sat | t1 | transform/rot180/oracle | oracle | 62.8 | 251 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | sat | t1 | transform/rot270/direct | direct | 63.8 | 255 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | sat | t1 | transform/rot270/oracle | oracle | 71.0 | 284 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | sat | t1 | transform/rot90/direct | direct | 64.0 | 256 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | sat | t1 | transform/rot90/oracle | oracle | 70.0 | 280 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | sat | t2 | base/direct | direct | 35.2 | 141 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | sat | t2 | base/oracle | oracle | 44.5 | 178 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | sat | t2 | transform/mirror_h/direct | direct | 54.0 | 216 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | sat | t2 | transform/mirror_h/oracle | oracle | 53.0 | 212 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | sat | t2 | transform/mirror_h_rot180/direct | direct | 55.8 | 223 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | sat | t2 | transform/mirror_h_rot180/oracle | oracle | 56.5 | 226 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | sat | t2 | transform/mirror_h_rot270/direct | direct | 53.8 | 215 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | sat | t2 | transform/mirror_h_rot270/oracle | oracle | 56.0 | 224 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | sat | t2 | transform/mirror_h_rot90/direct | direct | 55.2 | 221 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | sat | t2 | transform/mirror_h_rot90/oracle | oracle | 53.0 | 212 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | sat | t2 | transform/rot180/direct | direct | 54.8 | 219 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | sat | t2 | transform/rot180/oracle | oracle | 54.5 | 218 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | sat | t2 | transform/rot270/direct | direct | 55.0 | 220 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | sat | t2 | transform/rot270/oracle | oracle | 56.8 | 227 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | sat | t2 | transform/rot90/direct | direct | 54.0 | 216 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | sat | t2 | transform/rot90/oracle | oracle | 51.0 | 204 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | sat | t3 | base/direct | direct | 57.0 | 114 | 200 | 200 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | sat | t3 | base/oracle | oracle | 58.5 | 117 | 200 | 200 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | sat | t3 | transform/mirror_h/direct | direct | 59.0 | 118 | 200 | 200 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | sat | t3 | transform/mirror_h/oracle | oracle | 60.0 | 120 | 200 | 200 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | sat | t3 | transform/mirror_h_rot180/direct | direct | 58.0 | 116 | 200 | 200 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | sat | t3 | transform/mirror_h_rot180/oracle | oracle | 59.5 | 119 | 200 | 200 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | sat | t3 | transform/mirror_h_rot270/direct | direct | 61.0 | 122 | 200 | 200 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | sat | t3 | transform/mirror_h_rot270/oracle | oracle | 61.0 | 122 | 200 | 200 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | sat | t3 | transform/mirror_h_rot90/direct | direct | 56.5 | 113 | 200 | 200 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | sat | t3 | transform/mirror_h_rot90/oracle | oracle | 60.5 | 121 | 200 | 200 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | sat | t3 | transform/rot180/direct | direct | 56.0 | 112 | 200 | 200 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | sat | t3 | transform/rot180/oracle | oracle | 62.0 | 124 | 200 | 200 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | sat | t3 | transform/rot270/direct | direct | 57.5 | 115 | 200 | 200 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | sat | t3 | transform/rot270/oracle | oracle | 60.0 | 120 | 200 | 200 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | sat | t3 | transform/rot90/direct | direct | 56.5 | 113 | 200 | 200 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | sat | t3 | transform/rot90/oracle | oracle | 60.0 | 120 | 200 | 200 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | sat | t3 | world/intervention_001/direct | direct | 33.5 | 67 | 200 | 200 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | sat | t3 | world/intervention_001/oracle | oracle | 33.0 | 66 | 200 | 200 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | sat | t3 | world/sham_001/direct | direct | 56.5 | 113 | 200 | 200 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | sat | t3 | world/sham_001/oracle | oracle | 62.0 | 124 | 200 | 200 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | sat | t4 | base/direct | direct | 41.5 | 166 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | sat | t4 | base/oracle | oracle | 49.2 | 197 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | sat | t4 | transform/mirror_h/direct | direct | 44.0 | 176 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | sat | t4 | transform/mirror_h/oracle | oracle | 52.2 | 209 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | sat | t4 | transform/mirror_h_rot180/direct | direct | 42.8 | 171 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | sat | t4 | transform/mirror_h_rot180/oracle | oracle | 51.2 | 205 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | sat | t4 | transform/mirror_h_rot270/direct | direct | 46.8 | 187 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | sat | t4 | transform/mirror_h_rot270/oracle | oracle | 54.8 | 219 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | sat | t4 | transform/mirror_h_rot90/direct | direct | 42.2 | 169 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | sat | t4 | transform/mirror_h_rot90/oracle | oracle | 52.0 | 208 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | sat | t4 | transform/rot180/direct | direct | 45.5 | 182 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | sat | t4 | transform/rot180/oracle | oracle | 52.8 | 211 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | sat | t4 | transform/rot270/direct | direct | 44.8 | 179 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | sat | t4 | transform/rot270/oracle | oracle | 51.8 | 207 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | sat | t4 | transform/rot90/direct | direct | 42.5 | 170 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | sat | t4 | transform/rot90/oracle | oracle | 49.8 | 199 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | sat | t4 | world/intervention_001/direct | direct | 9.5 | 19 | 200 | 200 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | sat | t4 | world/intervention_001/oracle | oracle | 21.0 | 42 | 200 | 200 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | sat | t4 | world/sham_001/direct | direct | 38.5 | 77 | 200 | 200 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | sat | t4 | world/sham_001/oracle | oracle | 46.0 | 92 | 200 | 200 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | webrd04 | t1 | base/direct | direct | 54.0 | 216 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | webrd04 | t1 | base/oracle | oracle | 63.8 | 255 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | webrd04 | t2 | base/direct | direct | 52.0 | 208 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | webrd04 | t2 | base/oracle | oracle | 49.2 | 197 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | webrd04 | t3 | base/direct | direct | 57.5 | 115 | 200 | 200 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | webrd04 | t3 | base/oracle | oracle | 64.5 | 129 | 200 | 200 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | webrd04 | t3 | world/intervention_001/direct | direct | 24.5 | 49 | 200 | 200 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | webrd04 | t3 | world/intervention_001/oracle | oracle | 23.5 | 47 | 200 | 200 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | webrd04 | t3 | world/sham_001/direct | direct | 61.0 | 122 | 200 | 200 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | webrd04 | t3 | world/sham_001/oracle | oracle | 60.5 | 121 | 200 | 200 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | webrd04 | t4 | base/direct | direct | 40.5 | 162 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | webrd04 | t4 | base/oracle | oracle | 47.0 | 188 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | webrd04 | t4 | world/intervention_001/direct | direct | 14.0 | 28 | 200 | 200 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | webrd04 | t4 | world/intervention_001/oracle | oracle | 20.0 | 40 | 200 | 200 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | webrd04 | t4 | world/sham_001/direct | direct | 35.0 | 70 | 200 | 200 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | webrd04 | t4 | world/sham_001/oracle | oracle | 49.5 | 99 | 200 | 200 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | wprd01 | t1 | base/direct | direct | 69.0 | 276 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | wprd01 | t1 | base/oracle | oracle | 74.0 | 296 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | wprd01 | t1 | transform/mirror_h/direct | direct | 52.0 | 208 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | wprd01 | t1 | transform/mirror_h/oracle | oracle | 66.0 | 264 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | wprd01 | t1 | transform/mirror_h_rot180/direct | direct | 49.5 | 198 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | wprd01 | t1 | transform/mirror_h_rot180/oracle | oracle | 61.8 | 247 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | wprd01 | t1 | transform/mirror_h_rot270/direct | direct | 46.2 | 185 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | wprd01 | t1 | transform/mirror_h_rot270/oracle | oracle | 55.5 | 222 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | wprd01 | t1 | transform/mirror_h_rot90/direct | direct | 41.8 | 167 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | wprd01 | t1 | transform/mirror_h_rot90/oracle | oracle | 56.0 | 224 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | wprd01 | t1 | transform/rot180/direct | direct | 50.0 | 200 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | wprd01 | t1 | transform/rot180/oracle | oracle | 61.0 | 244 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | wprd01 | t1 | transform/rot270/direct | direct | 57.8 | 231 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | wprd01 | t1 | transform/rot270/oracle | oracle | 67.0 | 268 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | wprd01 | t1 | transform/rot90/direct | direct | 59.2 | 237 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | wprd01 | t1 | transform/rot90/oracle | oracle | 67.2 | 269 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | wprd01 | t2 | base/direct | direct | 32.8 | 131 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | wprd01 | t2 | base/oracle | oracle | 38.5 | 154 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | wprd01 | t2 | transform/mirror_h/direct | direct | 51.8 | 207 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | wprd01 | t2 | transform/mirror_h/oracle | oracle | 50.8 | 203 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | wprd01 | t2 | transform/mirror_h_rot180/direct | direct | 51.2 | 205 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | wprd01 | t2 | transform/mirror_h_rot180/oracle | oracle | 53.0 | 212 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | wprd01 | t2 | transform/mirror_h_rot270/direct | direct | 50.8 | 203 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | wprd01 | t2 | transform/mirror_h_rot270/oracle | oracle | 50.8 | 203 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | wprd01 | t2 | transform/mirror_h_rot90/direct | direct | 54.0 | 216 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | wprd01 | t2 | transform/mirror_h_rot90/oracle | oracle | 53.0 | 212 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | wprd01 | t2 | transform/rot180/direct | direct | 50.0 | 200 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | wprd01 | t2 | transform/rot180/oracle | oracle | 52.0 | 208 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | wprd01 | t2 | transform/rot270/direct | direct | 54.5 | 218 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | wprd01 | t2 | transform/rot270/oracle | oracle | 56.8 | 227 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | wprd01 | t2 | transform/rot90/direct | direct | 52.2 | 209 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | wprd01 | t2 | transform/rot90/oracle | oracle | 52.0 | 208 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | wprd01 | t3 | base/direct | direct | 50.0 | 100 | 200 | 200 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | wprd01 | t3 | base/oracle | oracle | 55.0 | 110 | 200 | 200 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | wprd01 | t3 | transform/mirror_h/direct | direct | 53.0 | 106 | 200 | 200 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | wprd01 | t3 | transform/mirror_h/oracle | oracle | 56.0 | 112 | 200 | 200 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | wprd01 | t3 | transform/mirror_h_rot180/direct | direct | 52.0 | 104 | 200 | 200 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | wprd01 | t3 | transform/mirror_h_rot180/oracle | oracle | 54.0 | 108 | 200 | 200 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | wprd01 | t3 | transform/mirror_h_rot270/direct | direct | 53.0 | 106 | 200 | 200 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | wprd01 | t3 | transform/mirror_h_rot270/oracle | oracle | 54.5 | 109 | 200 | 200 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | wprd01 | t3 | transform/mirror_h_rot90/direct | direct | 51.5 | 103 | 200 | 200 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | wprd01 | t3 | transform/mirror_h_rot90/oracle | oracle | 55.0 | 110 | 200 | 200 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | wprd01 | t3 | transform/rot180/direct | direct | 53.0 | 106 | 200 | 200 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | wprd01 | t3 | transform/rot180/oracle | oracle | 58.0 | 116 | 200 | 200 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | wprd01 | t3 | transform/rot270/direct | direct | 52.5 | 105 | 200 | 200 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | wprd01 | t3 | transform/rot270/oracle | oracle | 56.0 | 112 | 200 | 200 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | wprd01 | t3 | transform/rot90/direct | direct | 52.5 | 105 | 200 | 200 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | wprd01 | t3 | transform/rot90/oracle | oracle | 55.5 | 111 | 200 | 200 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | wprd01 | t3 | world/intervention_001/direct | direct | 43.0 | 86 | 200 | 200 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | wprd01 | t3 | world/intervention_001/oracle | oracle | 45.0 | 90 | 200 | 200 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | wprd01 | t3 | world/sham_001/direct | direct | 43.5 | 87 | 200 | 200 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | wprd01 | t3 | world/sham_001/oracle | oracle | 52.0 | 104 | 200 | 200 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | wprd01 | t4 | base/direct | direct | 43.5 | 174 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | wprd01 | t4 | base/oracle | oracle | 48.2 | 193 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | wprd01 | t4 | transform/mirror_h/direct | direct | 45.5 | 182 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | wprd01 | t4 | transform/mirror_h/oracle | oracle | 50.8 | 203 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | wprd01 | t4 | transform/mirror_h_rot180/direct | direct | 46.8 | 187 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | wprd01 | t4 | transform/mirror_h_rot180/oracle | oracle | 51.0 | 204 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | wprd01 | t4 | transform/mirror_h_rot270/direct | direct | 51.8 | 207 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | wprd01 | t4 | transform/mirror_h_rot270/oracle | oracle | 54.0 | 216 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | wprd01 | t4 | transform/mirror_h_rot90/direct | direct | 45.8 | 183 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | wprd01 | t4 | transform/mirror_h_rot90/oracle | oracle | 51.0 | 204 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | wprd01 | t4 | transform/rot180/direct | direct | 49.0 | 196 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | wprd01 | t4 | transform/rot180/oracle | oracle | 54.5 | 218 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | wprd01 | t4 | transform/rot270/direct | direct | 47.5 | 190 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | wprd01 | t4 | transform/rot270/oracle | oracle | 50.5 | 202 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | wprd01 | t4 | transform/rot90/direct | direct | 46.0 | 184 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | wprd01 | t4 | transform/rot90/oracle | oracle | 51.2 | 205 | 400 | 400 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | wprd01 | t4 | world/intervention_001/direct | direct | 11.5 | 23 | 200 | 200 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | wprd01 | t4 | world/intervention_001/oracle | oracle | 22.5 | 45 | 200 | 200 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | wprd01 | t4 | world/sham_001/direct | direct | 41.0 | 82 | 200 | 200 | 0 |
| Qwen2.5-VL-7B-Instruct | direct | wprd01 | t4 | world/sham_001/oracle | oracle | 45.5 | 91 | 200 | 200 | 0 |
| ThinkMorph-7B | direct | blank | t1 | base/direct | direct | 59.8 | 239 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | blank | t1 | base/oracle | oracle | 61.8 | 247 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | blank | t1 | transform/mirror_h/direct | direct | 66.2 | 265 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | blank | t1 | transform/mirror_h/oracle | oracle | 68.0 | 272 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | blank | t1 | transform/mirror_h_rot180/direct | direct | 67.5 | 270 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | blank | t1 | transform/mirror_h_rot180/oracle | oracle | 71.2 | 285 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | blank | t1 | transform/mirror_h_rot270/direct | direct | 60.5 | 242 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | blank | t1 | transform/mirror_h_rot270/oracle | oracle | 63.5 | 254 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | blank | t1 | transform/mirror_h_rot90/direct | direct | 66.8 | 267 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | blank | t1 | transform/mirror_h_rot90/oracle | oracle | 70.2 | 281 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | blank | t1 | transform/rot180/direct | direct | 52.0 | 208 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | blank | t1 | transform/rot180/oracle | oracle | 53.8 | 215 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | blank | t1 | transform/rot270/direct | direct | 55.8 | 223 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | blank | t1 | transform/rot270/oracle | oracle | 56.8 | 227 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | blank | t1 | transform/rot90/direct | direct | 59.5 | 238 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | blank | t1 | transform/rot90/oracle | oracle | 63.2 | 253 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | blank | t2 | base/direct | direct | 60.5 | 242 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | blank | t2 | base/oracle | oracle | 67.5 | 270 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | blank | t2 | transform/mirror_h/direct | direct | 65.0 | 260 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | blank | t2 | transform/mirror_h/oracle | oracle | 65.5 | 262 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | blank | t2 | transform/mirror_h_rot180/direct | direct | 63.0 | 252 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | blank | t2 | transform/mirror_h_rot180/oracle | oracle | 67.5 | 270 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | blank | t2 | transform/mirror_h_rot270/direct | direct | 61.5 | 246 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | blank | t2 | transform/mirror_h_rot270/oracle | oracle | 66.8 | 267 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | blank | t2 | transform/mirror_h_rot90/direct | direct | 61.5 | 246 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | blank | t2 | transform/mirror_h_rot90/oracle | oracle | 65.8 | 263 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | blank | t2 | transform/rot180/direct | direct | 60.2 | 241 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | blank | t2 | transform/rot180/oracle | oracle | 66.2 | 265 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | blank | t2 | transform/rot270/direct | direct | 58.8 | 235 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | blank | t2 | transform/rot270/oracle | oracle | 69.0 | 276 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | blank | t2 | transform/rot90/direct | direct | 57.5 | 230 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | blank | t2 | transform/rot90/oracle | oracle | 67.2 | 269 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | sat | t1 | base/direct | direct | 57.5 | 230 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | sat | t1 | base/oracle | oracle | 64.5 | 258 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | sat | t1 | transform/mirror_h/direct | direct | 60.0 | 240 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | sat | t1 | transform/mirror_h/oracle | oracle | 63.8 | 255 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | sat | t1 | transform/mirror_h_rot180/direct | direct | 57.8 | 231 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | sat | t1 | transform/mirror_h_rot180/oracle | oracle | 64.8 | 259 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | sat | t1 | transform/mirror_h_rot270/direct | direct | 56.5 | 226 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | sat | t1 | transform/mirror_h_rot270/oracle | oracle | 60.5 | 242 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | sat | t1 | transform/mirror_h_rot90/direct | direct | 61.8 | 247 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | sat | t1 | transform/mirror_h_rot90/oracle | oracle | 65.5 | 262 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | sat | t1 | transform/rot180/direct | direct | 51.8 | 207 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | sat | t1 | transform/rot180/oracle | oracle | 57.2 | 229 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | sat | t1 | transform/rot270/direct | direct | 58.2 | 233 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | sat | t1 | transform/rot270/oracle | oracle | 61.5 | 246 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | sat | t1 | transform/rot90/direct | direct | 56.5 | 226 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | sat | t1 | transform/rot90/oracle | oracle | 60.5 | 242 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | sat | t2 | base/direct | direct | 56.2 | 225 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | sat | t2 | base/oracle | oracle | 59.0 | 236 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | sat | t2 | transform/mirror_h/direct | direct | 57.2 | 229 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | sat | t2 | transform/mirror_h/oracle | oracle | 58.2 | 233 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | sat | t2 | transform/mirror_h_rot180/direct | direct | 57.8 | 231 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | sat | t2 | transform/mirror_h_rot180/oracle | oracle | 59.5 | 238 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | sat | t2 | transform/mirror_h_rot270/direct | direct | 57.2 | 229 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | sat | t2 | transform/mirror_h_rot270/oracle | oracle | 61.0 | 244 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | sat | t2 | transform/mirror_h_rot90/direct | direct | 57.2 | 229 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | sat | t2 | transform/mirror_h_rot90/oracle | oracle | 58.5 | 234 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | sat | t2 | transform/rot180/direct | direct | 58.0 | 232 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | sat | t2 | transform/rot180/oracle | oracle | 56.5 | 226 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | sat | t2 | transform/rot270/direct | direct | 59.8 | 239 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | sat | t2 | transform/rot270/oracle | oracle | 62.0 | 248 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | sat | t2 | transform/rot90/direct | direct | 59.8 | 239 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | sat | t2 | transform/rot90/oracle | oracle | 62.0 | 248 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | sat | t3 | base/direct | direct | 30.0 | 60 | 200 | 200 | 0 |
| ThinkMorph-7B | direct | sat | t3 | base/oracle | oracle | 32.0 | 64 | 200 | 200 | 0 |
| ThinkMorph-7B | direct | sat | t3 | transform/mirror_h/direct | direct | 29.0 | 58 | 200 | 200 | 0 |
| ThinkMorph-7B | direct | sat | t3 | transform/mirror_h/oracle | oracle | 32.0 | 64 | 200 | 200 | 0 |
| ThinkMorph-7B | direct | sat | t3 | transform/mirror_h_rot180/direct | direct | 27.0 | 54 | 200 | 200 | 0 |
| ThinkMorph-7B | direct | sat | t3 | transform/mirror_h_rot180/oracle | oracle | 36.0 | 72 | 200 | 200 | 0 |
| ThinkMorph-7B | direct | sat | t3 | transform/mirror_h_rot270/direct | direct | 32.5 | 65 | 200 | 200 | 0 |
| ThinkMorph-7B | direct | sat | t3 | transform/mirror_h_rot270/oracle | oracle | 39.5 | 79 | 200 | 200 | 0 |
| ThinkMorph-7B | direct | sat | t3 | transform/mirror_h_rot90/direct | direct | 35.0 | 70 | 200 | 200 | 0 |
| ThinkMorph-7B | direct | sat | t3 | transform/mirror_h_rot90/oracle | oracle | 38.0 | 76 | 200 | 200 | 0 |
| ThinkMorph-7B | direct | sat | t3 | transform/rot180/direct | direct | 32.5 | 65 | 200 | 200 | 0 |
| ThinkMorph-7B | direct | sat | t3 | transform/rot180/oracle | oracle | 40.0 | 80 | 200 | 200 | 0 |
| ThinkMorph-7B | direct | sat | t3 | transform/rot270/direct | direct | 31.5 | 63 | 200 | 200 | 0 |
| ThinkMorph-7B | direct | sat | t3 | transform/rot270/oracle | oracle | 38.0 | 76 | 200 | 200 | 0 |
| ThinkMorph-7B | direct | sat | t3 | transform/rot90/direct | direct | 33.0 | 66 | 200 | 200 | 0 |
| ThinkMorph-7B | direct | sat | t3 | transform/rot90/oracle | oracle | 37.5 | 75 | 200 | 200 | 0 |
| ThinkMorph-7B | direct | sat | t3 | world/intervention_001/direct | direct | 33.5 | 67 | 200 | 200 | 0 |
| ThinkMorph-7B | direct | sat | t3 | world/intervention_001/oracle | oracle | 34.5 | 69 | 200 | 200 | 0 |
| ThinkMorph-7B | direct | sat | t3 | world/sham_001/direct | direct | 37.0 | 74 | 200 | 200 | 0 |
| ThinkMorph-7B | direct | sat | t3 | world/sham_001/oracle | oracle | 34.5 | 69 | 200 | 200 | 0 |
| ThinkMorph-7B | direct | sat | t4 | base/direct | direct | 32.5 | 130 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | sat | t4 | base/oracle | oracle | 43.2 | 173 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | sat | t4 | transform/mirror_h/direct | direct | 32.8 | 131 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | sat | t4 | transform/mirror_h/oracle | oracle | 41.5 | 166 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | sat | t4 | transform/mirror_h_rot180/direct | direct | 30.8 | 123 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | sat | t4 | transform/mirror_h_rot180/oracle | oracle | 42.8 | 171 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | sat | t4 | transform/mirror_h_rot270/direct | direct | 32.2 | 129 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | sat | t4 | transform/mirror_h_rot270/oracle | oracle | 44.5 | 178 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | sat | t4 | transform/mirror_h_rot90/direct | direct | 32.0 | 128 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | sat | t4 | transform/mirror_h_rot90/oracle | oracle | 42.0 | 168 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | sat | t4 | transform/rot180/direct | direct | 31.5 | 126 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | sat | t4 | transform/rot180/oracle | oracle | 42.8 | 171 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | sat | t4 | transform/rot270/direct | direct | 31.5 | 126 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | sat | t4 | transform/rot270/oracle | oracle | 43.5 | 174 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | sat | t4 | transform/rot90/direct | direct | 35.2 | 141 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | sat | t4 | transform/rot90/oracle | oracle | 41.2 | 165 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | sat | t4 | world/intervention_001/direct | direct | 17.5 | 35 | 200 | 200 | 0 |
| ThinkMorph-7B | direct | sat | t4 | world/intervention_001/oracle | oracle | 41.0 | 82 | 200 | 200 | 0 |
| ThinkMorph-7B | direct | sat | t4 | world/sham_001/direct | direct | 27.0 | 54 | 200 | 200 | 0 |
| ThinkMorph-7B | direct | sat | t4 | world/sham_001/oracle | oracle | 39.5 | 79 | 200 | 200 | 0 |
| ThinkMorph-7B | direct | webrd04 | t1 | base/direct | direct | 58.5 | 234 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | webrd04 | t1 | base/oracle | oracle | 65.5 | 262 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | webrd04 | t2 | base/direct | direct | 54.0 | 216 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | webrd04 | t2 | base/oracle | oracle | 58.2 | 233 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | webrd04 | t3 | base/direct | direct | 32.0 | 64 | 200 | 200 | 0 |
| ThinkMorph-7B | direct | webrd04 | t3 | base/oracle | oracle | 35.0 | 70 | 200 | 200 | 0 |
| ThinkMorph-7B | direct | webrd04 | t3 | world/intervention_001/direct | direct | 36.0 | 72 | 200 | 200 | 0 |
| ThinkMorph-7B | direct | webrd04 | t3 | world/intervention_001/oracle | oracle | 37.0 | 74 | 200 | 200 | 0 |
| ThinkMorph-7B | direct | webrd04 | t3 | world/sham_001/direct | direct | 23.0 | 46 | 200 | 200 | 0 |
| ThinkMorph-7B | direct | webrd04 | t3 | world/sham_001/oracle | oracle | 29.0 | 58 | 200 | 200 | 0 |
| ThinkMorph-7B | direct | webrd04 | t4 | base/direct | direct | 32.5 | 130 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | webrd04 | t4 | base/oracle | oracle | 42.0 | 168 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | webrd04 | t4 | world/intervention_001/direct | direct | 19.5 | 39 | 200 | 200 | 0 |
| ThinkMorph-7B | direct | webrd04 | t4 | world/intervention_001/oracle | oracle | 41.0 | 82 | 200 | 200 | 0 |
| ThinkMorph-7B | direct | webrd04 | t4 | world/sham_001/direct | direct | 27.5 | 55 | 200 | 200 | 0 |
| ThinkMorph-7B | direct | webrd04 | t4 | world/sham_001/oracle | oracle | 32.5 | 65 | 200 | 200 | 0 |
| ThinkMorph-7B | direct | wprd01 | t1 | base/direct | direct | 70.8 | 283 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | wprd01 | t1 | base/oracle | oracle | 70.5 | 282 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | wprd01 | t1 | transform/mirror_h/direct | direct | 60.8 | 243 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | wprd01 | t1 | transform/mirror_h/oracle | oracle | 62.0 | 248 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | wprd01 | t1 | transform/mirror_h_rot180/direct | direct | 59.8 | 239 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | wprd01 | t1 | transform/mirror_h_rot180/oracle | oracle | 67.2 | 269 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | wprd01 | t1 | transform/mirror_h_rot270/direct | direct | 58.8 | 235 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | wprd01 | t1 | transform/mirror_h_rot270/oracle | oracle | 58.8 | 235 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | wprd01 | t1 | transform/mirror_h_rot90/direct | direct | 60.2 | 241 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | wprd01 | t1 | transform/mirror_h_rot90/oracle | oracle | 67.2 | 269 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | wprd01 | t1 | transform/rot180/direct | direct | 61.2 | 245 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | wprd01 | t1 | transform/rot180/oracle | oracle | 60.0 | 240 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | wprd01 | t1 | transform/rot270/direct | direct | 68.2 | 273 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | wprd01 | t1 | transform/rot270/oracle | oracle | 62.0 | 248 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | wprd01 | t1 | transform/rot90/direct | direct | 66.2 | 265 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | wprd01 | t1 | transform/rot90/oracle | oracle | 66.2 | 265 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | wprd01 | t2 | base/direct | direct | 40.0 | 160 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | wprd01 | t2 | base/oracle | oracle | 62.0 | 248 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | wprd01 | t2 | transform/mirror_h/direct | direct | 56.5 | 226 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | wprd01 | t2 | transform/mirror_h/oracle | oracle | 61.8 | 247 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | wprd01 | t2 | transform/mirror_h_rot180/direct | direct | 59.5 | 238 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | wprd01 | t2 | transform/mirror_h_rot180/oracle | oracle | 61.5 | 246 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | wprd01 | t2 | transform/mirror_h_rot270/direct | direct | 55.5 | 222 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | wprd01 | t2 | transform/mirror_h_rot270/oracle | oracle | 59.2 | 237 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | wprd01 | t2 | transform/mirror_h_rot90/direct | direct | 57.8 | 231 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | wprd01 | t2 | transform/mirror_h_rot90/oracle | oracle | 61.2 | 245 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | wprd01 | t2 | transform/rot180/direct | direct | 59.2 | 237 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | wprd01 | t2 | transform/rot180/oracle | oracle | 63.5 | 254 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | wprd01 | t2 | transform/rot270/direct | direct | 62.0 | 248 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | wprd01 | t2 | transform/rot270/oracle | oracle | 64.5 | 258 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | wprd01 | t2 | transform/rot90/direct | direct | 59.5 | 238 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | wprd01 | t2 | transform/rot90/oracle | oracle | 63.0 | 252 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | wprd01 | t3 | base/direct | direct | 31.5 | 63 | 200 | 200 | 0 |
| ThinkMorph-7B | direct | wprd01 | t3 | base/oracle | oracle | 33.0 | 66 | 200 | 200 | 0 |
| ThinkMorph-7B | direct | wprd01 | t3 | transform/mirror_h/direct | direct | 32.0 | 64 | 200 | 200 | 0 |
| ThinkMorph-7B | direct | wprd01 | t3 | transform/mirror_h/oracle | oracle | 33.5 | 67 | 200 | 200 | 0 |
| ThinkMorph-7B | direct | wprd01 | t3 | transform/mirror_h_rot180/direct | direct | 33.5 | 67 | 200 | 200 | 0 |
| ThinkMorph-7B | direct | wprd01 | t3 | transform/mirror_h_rot180/oracle | oracle | 33.0 | 66 | 200 | 200 | 0 |
| ThinkMorph-7B | direct | wprd01 | t3 | transform/mirror_h_rot270/direct | direct | 34.0 | 68 | 200 | 200 | 0 |
| ThinkMorph-7B | direct | wprd01 | t3 | transform/mirror_h_rot270/oracle | oracle | 34.5 | 69 | 200 | 200 | 0 |
| ThinkMorph-7B | direct | wprd01 | t3 | transform/mirror_h_rot90/direct | direct | 35.0 | 70 | 200 | 200 | 0 |
| ThinkMorph-7B | direct | wprd01 | t3 | transform/mirror_h_rot90/oracle | oracle | 37.5 | 75 | 200 | 200 | 0 |
| ThinkMorph-7B | direct | wprd01 | t3 | transform/rot180/direct | direct | 32.0 | 64 | 200 | 200 | 0 |
| ThinkMorph-7B | direct | wprd01 | t3 | transform/rot180/oracle | oracle | 33.5 | 67 | 200 | 200 | 0 |
| ThinkMorph-7B | direct | wprd01 | t3 | transform/rot270/direct | direct | 32.5 | 65 | 200 | 200 | 0 |
| ThinkMorph-7B | direct | wprd01 | t3 | transform/rot270/oracle | oracle | 34.5 | 69 | 200 | 200 | 0 |
| ThinkMorph-7B | direct | wprd01 | t3 | transform/rot90/direct | direct | 33.5 | 67 | 200 | 200 | 0 |
| ThinkMorph-7B | direct | wprd01 | t3 | transform/rot90/oracle | oracle | 35.5 | 71 | 200 | 200 | 0 |
| ThinkMorph-7B | direct | wprd01 | t3 | world/intervention_001/direct | direct | 33.0 | 66 | 200 | 200 | 0 |
| ThinkMorph-7B | direct | wprd01 | t3 | world/intervention_001/oracle | oracle | 33.5 | 67 | 200 | 200 | 0 |
| ThinkMorph-7B | direct | wprd01 | t3 | world/sham_001/direct | direct | 32.0 | 64 | 200 | 200 | 0 |
| ThinkMorph-7B | direct | wprd01 | t3 | world/sham_001/oracle | oracle | 33.0 | 66 | 200 | 200 | 0 |
| ThinkMorph-7B | direct | wprd01 | t4 | base/direct | direct | 35.2 | 141 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | wprd01 | t4 | base/oracle | oracle | 45.5 | 182 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | wprd01 | t4 | transform/mirror_h/direct | direct | 34.2 | 137 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | wprd01 | t4 | transform/mirror_h/oracle | oracle | 45.0 | 180 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | wprd01 | t4 | transform/mirror_h_rot180/direct | direct | 35.5 | 142 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | wprd01 | t4 | transform/mirror_h_rot180/oracle | oracle | 45.2 | 181 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | wprd01 | t4 | transform/mirror_h_rot270/direct | direct | 34.2 | 137 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | wprd01 | t4 | transform/mirror_h_rot270/oracle | oracle | 46.5 | 186 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | wprd01 | t4 | transform/mirror_h_rot90/direct | direct | 34.8 | 139 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | wprd01 | t4 | transform/mirror_h_rot90/oracle | oracle | 42.5 | 170 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | wprd01 | t4 | transform/rot180/direct | direct | 34.8 | 139 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | wprd01 | t4 | transform/rot180/oracle | oracle | 42.2 | 169 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | wprd01 | t4 | transform/rot270/direct | direct | 34.5 | 138 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | wprd01 | t4 | transform/rot270/oracle | oracle | 45.5 | 182 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | wprd01 | t4 | transform/rot90/direct | direct | 34.0 | 136 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | wprd01 | t4 | transform/rot90/oracle | oracle | 43.8 | 175 | 400 | 400 | 0 |
| ThinkMorph-7B | direct | wprd01 | t4 | world/intervention_001/direct | direct | 18.0 | 36 | 200 | 200 | 0 |
| ThinkMorph-7B | direct | wprd01 | t4 | world/intervention_001/oracle | oracle | 36.5 | 73 | 200 | 200 | 0 |
| ThinkMorph-7B | direct | wprd01 | t4 | world/sham_001/direct | direct | 29.5 | 59 | 200 | 200 | 0 |
| ThinkMorph-7B | direct | wprd01 | t4 | world/sham_001/oracle | oracle | 39.0 | 78 | 200 | 200 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | blank | t1 | base/direct | direct | 67.2 | 269 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | blank | t1 | base/oracle | oracle | 72.8 | 291 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | blank | t1 | transform/mirror_h/direct | direct | 63.5 | 254 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | blank | t1 | transform/mirror_h/oracle | oracle | 62.2 | 249 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | blank | t1 | transform/mirror_h_rot180/direct | direct | 58.8 | 235 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | blank | t1 | transform/mirror_h_rot180/oracle | oracle | 58.2 | 233 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | blank | t1 | transform/mirror_h_rot270/direct | direct | 52.8 | 211 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | blank | t1 | transform/mirror_h_rot270/oracle | oracle | 53.5 | 214 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | blank | t1 | transform/mirror_h_rot90/direct | direct | 57.8 | 231 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | blank | t1 | transform/mirror_h_rot90/oracle | oracle | 55.2 | 221 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | blank | t1 | transform/rot180/direct | direct | 64.5 | 258 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | blank | t1 | transform/rot180/oracle | oracle | 69.8 | 279 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | blank | t1 | transform/rot270/direct | direct | 66.8 | 267 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | blank | t1 | transform/rot270/oracle | oracle | 71.0 | 284 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | blank | t1 | transform/rot90/direct | direct | 68.0 | 272 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | blank | t1 | transform/rot90/oracle | oracle | 72.0 | 288 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | blank | t2 | base/direct | direct | 48.5 | 194 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | blank | t2 | base/oracle | oracle | 54.8 | 219 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | blank | t2 | transform/mirror_h/direct | direct | 49.8 | 199 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | blank | t2 | transform/mirror_h/oracle | oracle | 60.0 | 240 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | blank | t2 | transform/mirror_h_rot180/direct | direct | 50.5 | 202 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | blank | t2 | transform/mirror_h_rot180/oracle | oracle | 56.8 | 227 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | blank | t2 | transform/mirror_h_rot270/direct | direct | 46.5 | 186 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | blank | t2 | transform/mirror_h_rot270/oracle | oracle | 62.2 | 249 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | blank | t2 | transform/mirror_h_rot90/direct | direct | 48.0 | 192 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | blank | t2 | transform/mirror_h_rot90/oracle | oracle | 54.5 | 218 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | blank | t2 | transform/rot180/direct | direct | 52.2 | 209 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | blank | t2 | transform/rot180/oracle | oracle | 62.2 | 249 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | blank | t2 | transform/rot270/direct | direct | 49.8 | 199 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | blank | t2 | transform/rot270/oracle | oracle | 56.0 | 224 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | blank | t2 | transform/rot90/direct | direct | 50.5 | 202 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | blank | t2 | transform/rot90/oracle | oracle | 58.2 | 233 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | sat | t1 | base/direct | direct | 58.0 | 232 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | sat | t1 | base/oracle | oracle | 67.8 | 271 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | sat | t1 | transform/mirror_h/direct | direct | 60.5 | 242 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | sat | t1 | transform/mirror_h/oracle | oracle | 62.8 | 251 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | sat | t1 | transform/mirror_h_rot180/direct | direct | 54.8 | 219 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | sat | t1 | transform/mirror_h_rot180/oracle | oracle | 58.5 | 234 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | sat | t1 | transform/mirror_h_rot270/direct | direct | 51.8 | 207 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | sat | t1 | transform/mirror_h_rot270/oracle | oracle | 55.8 | 223 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | sat | t1 | transform/mirror_h_rot90/direct | direct | 57.2 | 229 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | sat | t1 | transform/mirror_h_rot90/oracle | oracle | 60.2 | 241 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | sat | t1 | transform/rot180/direct | direct | 51.8 | 207 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | sat | t1 | transform/rot180/oracle | oracle | 65.0 | 260 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | sat | t1 | transform/rot270/direct | direct | 64.5 | 258 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | sat | t1 | transform/rot270/oracle | oracle | 67.2 | 269 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | sat | t1 | transform/rot90/direct | direct | 56.2 | 225 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | sat | t1 | transform/rot90/oracle | oracle | 68.2 | 273 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | sat | t2 | base/direct | direct | 46.5 | 186 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | sat | t2 | base/oracle | oracle | 43.5 | 174 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | sat | t2 | transform/mirror_h/direct | direct | 50.2 | 201 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | sat | t2 | transform/mirror_h/oracle | oracle | 49.8 | 199 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | sat | t2 | transform/mirror_h_rot180/direct | direct | 50.2 | 201 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | sat | t2 | transform/mirror_h_rot180/oracle | oracle | 48.2 | 193 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | sat | t2 | transform/mirror_h_rot270/direct | direct | 52.8 | 211 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | sat | t2 | transform/mirror_h_rot270/oracle | oracle | 53.8 | 215 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | sat | t2 | transform/mirror_h_rot90/direct | direct | 47.5 | 190 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | sat | t2 | transform/mirror_h_rot90/oracle | oracle | 48.2 | 193 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | sat | t2 | transform/rot180/direct | direct | 54.5 | 218 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | sat | t2 | transform/rot180/oracle | oracle | 48.2 | 193 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | sat | t2 | transform/rot270/direct | direct | 53.5 | 214 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | sat | t2 | transform/rot270/oracle | oracle | 52.2 | 209 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | sat | t2 | transform/rot90/direct | direct | 49.2 | 197 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | sat | t2 | transform/rot90/oracle | oracle | 49.0 | 196 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | sat | t3 | base/direct | direct | 26.0 | 52 | 200 | 200 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | sat | t3 | base/oracle | oracle | 28.0 | 56 | 200 | 200 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | sat | t3 | transform/mirror_h/direct | direct | 25.0 | 50 | 200 | 200 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | sat | t3 | transform/mirror_h/oracle | oracle | 28.0 | 56 | 200 | 200 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | sat | t3 | transform/mirror_h_rot180/direct | direct | 23.5 | 47 | 200 | 200 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | sat | t3 | transform/mirror_h_rot180/oracle | oracle | 25.5 | 51 | 200 | 200 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | sat | t3 | transform/mirror_h_rot270/direct | direct | 27.0 | 54 | 200 | 200 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | sat | t3 | transform/mirror_h_rot270/oracle | oracle | 31.5 | 63 | 200 | 200 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | sat | t3 | transform/mirror_h_rot90/direct | direct | 29.0 | 58 | 200 | 200 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | sat | t3 | transform/mirror_h_rot90/oracle | oracle | 32.5 | 65 | 200 | 200 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | sat | t3 | transform/rot180/direct | direct | 27.5 | 55 | 200 | 200 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | sat | t3 | transform/rot180/oracle | oracle | 28.0 | 56 | 200 | 200 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | sat | t3 | transform/rot270/direct | direct | 29.0 | 58 | 200 | 200 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | sat | t3 | transform/rot270/oracle | oracle | 29.0 | 58 | 200 | 200 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | sat | t3 | transform/rot90/direct | direct | 29.0 | 58 | 200 | 200 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | sat | t3 | transform/rot90/oracle | oracle | 29.5 | 59 | 200 | 200 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | sat | t3 | world/intervention_001/direct | direct | 40.0 | 80 | 200 | 200 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | sat | t3 | world/intervention_001/oracle | oracle | 39.0 | 78 | 200 | 200 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | sat | t3 | world/sham_001/direct | direct | 22.0 | 44 | 200 | 200 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | sat | t3 | world/sham_001/oracle | oracle | 25.5 | 51 | 200 | 200 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | sat | t4 | base/direct | direct | 52.5 | 210 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | sat | t4 | base/oracle | oracle | 57.0 | 228 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | sat | t4 | transform/mirror_h/direct | direct | 49.8 | 199 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | sat | t4 | transform/mirror_h/oracle | oracle | 56.0 | 224 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | sat | t4 | transform/mirror_h_rot180/direct | direct | 48.5 | 194 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | sat | t4 | transform/mirror_h_rot180/oracle | oracle | 55.5 | 222 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | sat | t4 | transform/mirror_h_rot270/direct | direct | 50.8 | 203 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | sat | t4 | transform/mirror_h_rot270/oracle | oracle | 57.0 | 228 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | sat | t4 | transform/mirror_h_rot90/direct | direct | 52.0 | 208 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | sat | t4 | transform/mirror_h_rot90/oracle | oracle | 56.8 | 227 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | sat | t4 | transform/rot180/direct | direct | 51.8 | 207 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | sat | t4 | transform/rot180/oracle | oracle | 58.0 | 232 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | sat | t4 | transform/rot270/direct | direct | 50.2 | 201 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | sat | t4 | transform/rot270/oracle | oracle | 59.5 | 238 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | sat | t4 | transform/rot90/direct | direct | 49.8 | 199 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | sat | t4 | transform/rot90/oracle | oracle | 55.2 | 221 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | sat | t4 | world/intervention_001/direct | direct | 10.5 | 21 | 200 | 200 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | sat | t4 | world/intervention_001/oracle | oracle | 32.0 | 64 | 200 | 200 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | sat | t4 | world/sham_001/direct | direct | 57.5 | 115 | 200 | 200 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | sat | t4 | world/sham_001/oracle | oracle | 72.0 | 144 | 200 | 200 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | webrd04 | t1 | base/direct | direct | 62.0 | 248 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | webrd04 | t1 | base/oracle | oracle | 67.8 | 271 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | webrd04 | t2 | base/direct | direct | 43.8 | 175 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | webrd04 | t2 | base/oracle | oracle | 43.8 | 175 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | webrd04 | t3 | base/direct | direct | 25.0 | 50 | 200 | 200 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | webrd04 | t3 | base/oracle | oracle | 26.5 | 53 | 200 | 200 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | webrd04 | t3 | world/intervention_001/direct | direct | 43.5 | 87 | 200 | 200 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | webrd04 | t3 | world/intervention_001/oracle | oracle | 44.0 | 88 | 200 | 200 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | webrd04 | t3 | world/sham_001/direct | direct | 21.0 | 42 | 200 | 200 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | webrd04 | t3 | world/sham_001/oracle | oracle | 23.0 | 46 | 200 | 200 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | webrd04 | t4 | base/direct | direct | 43.0 | 172 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | webrd04 | t4 | base/oracle | oracle | 50.0 | 200 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | webrd04 | t4 | world/intervention_001/direct | direct | 11.0 | 22 | 200 | 200 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | webrd04 | t4 | world/intervention_001/oracle | oracle | 27.5 | 55 | 200 | 200 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | webrd04 | t4 | world/sham_001/direct | direct | 47.5 | 95 | 200 | 200 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | webrd04 | t4 | world/sham_001/oracle | oracle | 58.5 | 117 | 200 | 200 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | wprd01 | t1 | base/direct | direct | 68.2 | 273 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | wprd01 | t1 | base/oracle | oracle | 70.8 | 283 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | wprd01 | t1 | transform/mirror_h/direct | direct | 64.5 | 258 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | wprd01 | t1 | transform/mirror_h/oracle | oracle | 64.0 | 256 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | wprd01 | t1 | transform/mirror_h_rot180/direct | direct | 58.5 | 234 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | wprd01 | t1 | transform/mirror_h_rot180/oracle | oracle | 57.2 | 229 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | wprd01 | t1 | transform/mirror_h_rot270/direct | direct | 60.5 | 242 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | wprd01 | t1 | transform/mirror_h_rot270/oracle | oracle | 56.2 | 225 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | wprd01 | t1 | transform/mirror_h_rot90/direct | direct | 64.0 | 256 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | wprd01 | t1 | transform/mirror_h_rot90/oracle | oracle | 62.5 | 250 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | wprd01 | t1 | transform/rot180/direct | direct | 59.8 | 239 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | wprd01 | t1 | transform/rot180/oracle | oracle | 68.5 | 274 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | wprd01 | t1 | transform/rot270/direct | direct | 64.2 | 257 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | wprd01 | t1 | transform/rot270/oracle | oracle | 67.5 | 270 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | wprd01 | t1 | transform/rot90/direct | direct | 63.8 | 255 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | wprd01 | t1 | transform/rot90/oracle | oracle | 69.2 | 277 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | wprd01 | t2 | base/direct | direct | 44.0 | 176 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | wprd01 | t2 | base/oracle | oracle | 48.5 | 194 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | wprd01 | t2 | transform/mirror_h/direct | direct | 50.0 | 200 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | wprd01 | t2 | transform/mirror_h/oracle | oracle | 50.0 | 200 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | wprd01 | t2 | transform/mirror_h_rot180/direct | direct | 47.5 | 190 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | wprd01 | t2 | transform/mirror_h_rot180/oracle | oracle | 51.2 | 205 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | wprd01 | t2 | transform/mirror_h_rot270/direct | direct | 50.5 | 202 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | wprd01 | t2 | transform/mirror_h_rot270/oracle | oracle | 51.8 | 207 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | wprd01 | t2 | transform/mirror_h_rot90/direct | direct | 51.5 | 206 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | wprd01 | t2 | transform/mirror_h_rot90/oracle | oracle | 51.2 | 205 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | wprd01 | t2 | transform/rot180/direct | direct | 52.8 | 211 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | wprd01 | t2 | transform/rot180/oracle | oracle | 52.8 | 211 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | wprd01 | t2 | transform/rot270/direct | direct | 48.2 | 193 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | wprd01 | t2 | transform/rot270/oracle | oracle | 50.5 | 202 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | wprd01 | t2 | transform/rot90/direct | direct | 47.8 | 191 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | wprd01 | t2 | transform/rot90/oracle | oracle | 48.2 | 193 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | wprd01 | t3 | base/direct | direct | 22.5 | 45 | 200 | 200 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | wprd01 | t3 | base/oracle | oracle | 24.0 | 48 | 200 | 200 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | wprd01 | t3 | transform/mirror_h/direct | direct | 21.0 | 42 | 200 | 200 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | wprd01 | t3 | transform/mirror_h/oracle | oracle | 22.5 | 45 | 200 | 200 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | wprd01 | t3 | transform/mirror_h_rot180/direct | direct | 18.5 | 37 | 200 | 200 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | wprd01 | t3 | transform/mirror_h_rot180/oracle | oracle | 22.0 | 44 | 200 | 200 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | wprd01 | t3 | transform/mirror_h_rot270/direct | direct | 24.5 | 49 | 200 | 200 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | wprd01 | t3 | transform/mirror_h_rot270/oracle | oracle | 24.5 | 49 | 200 | 200 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | wprd01 | t3 | transform/mirror_h_rot90/direct | direct | 24.0 | 48 | 200 | 200 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | wprd01 | t3 | transform/mirror_h_rot90/oracle | oracle | 25.5 | 51 | 200 | 200 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | wprd01 | t3 | transform/rot180/direct | direct | 23.5 | 47 | 200 | 200 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | wprd01 | t3 | transform/rot180/oracle | oracle | 24.0 | 48 | 200 | 200 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | wprd01 | t3 | transform/rot270/direct | direct | 26.0 | 52 | 200 | 200 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | wprd01 | t3 | transform/rot270/oracle | oracle | 25.5 | 51 | 200 | 200 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | wprd01 | t3 | transform/rot90/direct | direct | 23.5 | 47 | 200 | 200 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | wprd01 | t3 | transform/rot90/oracle | oracle | 26.0 | 52 | 200 | 200 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | wprd01 | t3 | world/intervention_001/direct | direct | 49.5 | 99 | 200 | 200 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | wprd01 | t3 | world/intervention_001/oracle | oracle | 49.0 | 98 | 200 | 200 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | wprd01 | t3 | world/sham_001/direct | direct | 10.5 | 21 | 200 | 200 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | wprd01 | t3 | world/sham_001/oracle | oracle | 13.5 | 27 | 200 | 200 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | wprd01 | t4 | base/direct | direct | 52.0 | 208 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | wprd01 | t4 | base/oracle | oracle | 55.8 | 223 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | wprd01 | t4 | transform/mirror_h/direct | direct | 55.5 | 222 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | wprd01 | t4 | transform/mirror_h/oracle | oracle | 57.5 | 230 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | wprd01 | t4 | transform/mirror_h_rot180/direct | direct | 52.0 | 208 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | wprd01 | t4 | transform/mirror_h_rot180/oracle | oracle | 56.5 | 226 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | wprd01 | t4 | transform/mirror_h_rot270/direct | direct | 54.0 | 216 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | wprd01 | t4 | transform/mirror_h_rot270/oracle | oracle | 58.2 | 233 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | wprd01 | t4 | transform/mirror_h_rot90/direct | direct | 54.0 | 216 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | wprd01 | t4 | transform/mirror_h_rot90/oracle | oracle | 57.8 | 231 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | wprd01 | t4 | transform/rot180/direct | direct | 57.0 | 228 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | wprd01 | t4 | transform/rot180/oracle | oracle | 61.0 | 244 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | wprd01 | t4 | transform/rot270/direct | direct | 55.0 | 220 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | wprd01 | t4 | transform/rot270/oracle | oracle | 58.2 | 233 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | wprd01 | t4 | transform/rot90/direct | direct | 52.5 | 210 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | wprd01 | t4 | transform/rot90/oracle | oracle | 56.5 | 226 | 400 | 400 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | wprd01 | t4 | world/intervention_001/direct | direct | 13.0 | 26 | 200 | 200 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | wprd01 | t4 | world/intervention_001/oracle | oracle | 29.5 | 59 | 200 | 200 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | wprd01 | t4 | world/sham_001/direct | direct | 61.5 | 123 | 200 | 200 | 0 |
| SenseNova-SI-1.3-Qwen3-VL-8B | direct | wprd01 | t4 | world/sham_001/oracle | oracle | 67.0 | 134 | 200 | 200 | 0 |
| Bagel-7B-MoT | direct | blank | t1 | base/direct | direct | 59.5 | 238 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | blank | t1 | base/oracle | oracle | 62.2 | 249 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | blank | t1 | transform/mirror_h/direct | direct | 71.0 | 284 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | blank | t1 | transform/mirror_h/oracle | oracle | 68.2 | 273 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | blank | t1 | transform/mirror_h_rot180/direct | direct | 67.5 | 270 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | blank | t1 | transform/mirror_h_rot180/oracle | oracle | 64.0 | 256 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | blank | t1 | transform/mirror_h_rot270/direct | direct | 60.8 | 243 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | blank | t1 | transform/mirror_h_rot270/oracle | oracle | 60.5 | 242 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | blank | t1 | transform/mirror_h_rot90/direct | direct | 64.5 | 258 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | blank | t1 | transform/mirror_h_rot90/oracle | oracle | 66.8 | 267 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | blank | t1 | transform/rot180/direct | direct | 55.8 | 223 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | blank | t1 | transform/rot180/oracle | oracle | 55.8 | 223 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | blank | t1 | transform/rot270/direct | direct | 59.2 | 237 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | blank | t1 | transform/rot270/oracle | oracle | 60.8 | 243 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | blank | t1 | transform/rot90/direct | direct | 61.0 | 244 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | blank | t1 | transform/rot90/oracle | oracle | 60.2 | 241 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | blank | t2 | base/direct | direct | 65.0 | 260 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | blank | t2 | base/oracle | oracle | 68.8 | 275 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | blank | t2 | transform/mirror_h/direct | direct | 65.5 | 262 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | blank | t2 | transform/mirror_h/oracle | oracle | 69.5 | 278 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | blank | t2 | transform/mirror_h_rot180/direct | direct | 68.5 | 274 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | blank | t2 | transform/mirror_h_rot180/oracle | oracle | 72.5 | 290 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | blank | t2 | transform/mirror_h_rot270/direct | direct | 65.5 | 262 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | blank | t2 | transform/mirror_h_rot270/oracle | oracle | 71.2 | 285 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | blank | t2 | transform/mirror_h_rot90/direct | direct | 67.0 | 268 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | blank | t2 | transform/mirror_h_rot90/oracle | oracle | 69.0 | 276 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | blank | t2 | transform/rot180/direct | direct | 65.5 | 262 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | blank | t2 | transform/rot180/oracle | oracle | 69.0 | 276 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | blank | t2 | transform/rot270/direct | direct | 64.8 | 259 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | blank | t2 | transform/rot270/oracle | oracle | 70.2 | 281 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | blank | t2 | transform/rot90/direct | direct | 63.5 | 254 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | blank | t2 | transform/rot90/oracle | oracle | 68.0 | 272 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | sat | t1 | base/direct | direct | 56.2 | 225 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | sat | t1 | base/oracle | oracle | 64.2 | 257 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | sat | t1 | transform/mirror_h/direct | direct | 62.5 | 250 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | sat | t1 | transform/mirror_h/oracle | oracle | 64.8 | 259 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | sat | t1 | transform/mirror_h_rot180/direct | direct | 60.5 | 242 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | sat | t1 | transform/mirror_h_rot180/oracle | oracle | 61.8 | 247 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | sat | t1 | transform/mirror_h_rot270/direct | direct | 54.5 | 218 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | sat | t1 | transform/mirror_h_rot270/oracle | oracle | 53.5 | 214 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | sat | t1 | transform/mirror_h_rot90/direct | direct | 59.8 | 239 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | sat | t1 | transform/mirror_h_rot90/oracle | oracle | 64.0 | 256 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | sat | t1 | transform/rot180/direct | direct | 54.5 | 218 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | sat | t1 | transform/rot180/oracle | oracle | 64.0 | 256 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | sat | t1 | transform/rot270/direct | direct | 59.5 | 238 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | sat | t1 | transform/rot270/oracle | oracle | 64.5 | 258 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | sat | t1 | transform/rot90/direct | direct | 55.0 | 220 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | sat | t1 | transform/rot90/oracle | oracle | 59.0 | 236 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | sat | t2 | base/direct | direct | 57.2 | 229 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | sat | t2 | base/oracle | oracle | 60.0 | 240 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | sat | t2 | transform/mirror_h/direct | direct | 55.8 | 223 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | sat | t2 | transform/mirror_h/oracle | oracle | 57.8 | 231 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | sat | t2 | transform/mirror_h_rot180/direct | direct | 58.5 | 234 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | sat | t2 | transform/mirror_h_rot180/oracle | oracle | 59.5 | 238 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | sat | t2 | transform/mirror_h_rot270/direct | direct | 57.2 | 229 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | sat | t2 | transform/mirror_h_rot270/oracle | oracle | 60.2 | 241 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | sat | t2 | transform/mirror_h_rot90/direct | direct | 58.0 | 232 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | sat | t2 | transform/mirror_h_rot90/oracle | oracle | 60.2 | 241 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | sat | t2 | transform/rot180/direct | direct | 60.5 | 242 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | sat | t2 | transform/rot180/oracle | oracle | 61.0 | 244 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | sat | t2 | transform/rot270/direct | direct | 57.2 | 229 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | sat | t2 | transform/rot270/oracle | oracle | 58.8 | 235 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | sat | t2 | transform/rot90/direct | direct | 58.0 | 232 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | sat | t2 | transform/rot90/oracle | oracle | 59.5 | 238 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | sat | t3 | base/direct | direct | 30.0 | 60 | 200 | 200 | 0 |
| Bagel-7B-MoT | direct | sat | t3 | base/oracle | oracle | 33.5 | 67 | 200 | 200 | 0 |
| Bagel-7B-MoT | direct | sat | t3 | transform/mirror_h/direct | direct | 27.0 | 54 | 200 | 200 | 0 |
| Bagel-7B-MoT | direct | sat | t3 | transform/mirror_h/oracle | oracle | 34.5 | 69 | 200 | 200 | 0 |
| Bagel-7B-MoT | direct | sat | t3 | transform/mirror_h_rot180/direct | direct | 29.0 | 58 | 200 | 200 | 0 |
| Bagel-7B-MoT | direct | sat | t3 | transform/mirror_h_rot180/oracle | oracle | 34.5 | 69 | 200 | 200 | 0 |
| Bagel-7B-MoT | direct | sat | t3 | transform/mirror_h_rot270/direct | direct | 30.5 | 61 | 200 | 200 | 0 |
| Bagel-7B-MoT | direct | sat | t3 | transform/mirror_h_rot270/oracle | oracle | 35.5 | 71 | 200 | 200 | 0 |
| Bagel-7B-MoT | direct | sat | t3 | transform/mirror_h_rot90/direct | direct | 30.0 | 60 | 200 | 200 | 0 |
| Bagel-7B-MoT | direct | sat | t3 | transform/mirror_h_rot90/oracle | oracle | 34.5 | 69 | 200 | 200 | 0 |
| Bagel-7B-MoT | direct | sat | t3 | transform/rot180/direct | direct | 29.0 | 58 | 200 | 200 | 0 |
| Bagel-7B-MoT | direct | sat | t3 | transform/rot180/oracle | oracle | 34.0 | 68 | 200 | 200 | 0 |
| Bagel-7B-MoT | direct | sat | t3 | transform/rot270/direct | direct | 28.0 | 56 | 200 | 200 | 0 |
| Bagel-7B-MoT | direct | sat | t3 | transform/rot270/oracle | oracle | 34.5 | 69 | 200 | 200 | 0 |
| Bagel-7B-MoT | direct | sat | t3 | transform/rot90/direct | direct | 28.5 | 57 | 200 | 200 | 0 |
| Bagel-7B-MoT | direct | sat | t3 | transform/rot90/oracle | oracle | 36.5 | 73 | 200 | 200 | 0 |
| Bagel-7B-MoT | direct | sat | t3 | world/intervention_001/direct | direct | 42.0 | 84 | 200 | 200 | 0 |
| Bagel-7B-MoT | direct | sat | t3 | world/intervention_001/oracle | oracle | 47.0 | 94 | 200 | 200 | 0 |
| Bagel-7B-MoT | direct | sat | t3 | world/sham_001/direct | direct | 24.5 | 49 | 200 | 200 | 0 |
| Bagel-7B-MoT | direct | sat | t3 | world/sham_001/oracle | oracle | 33.5 | 67 | 200 | 200 | 0 |
| Bagel-7B-MoT | direct | sat | t4 | base/direct | direct | 32.8 | 131 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | sat | t4 | base/oracle | oracle | 41.5 | 166 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | sat | t4 | transform/mirror_h/direct | direct | 33.5 | 134 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | sat | t4 | transform/mirror_h/oracle | oracle | 41.0 | 164 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | sat | t4 | transform/mirror_h_rot180/direct | direct | 33.0 | 132 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | sat | t4 | transform/mirror_h_rot180/oracle | oracle | 41.5 | 166 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | sat | t4 | transform/mirror_h_rot270/direct | direct | 33.5 | 134 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | sat | t4 | transform/mirror_h_rot270/oracle | oracle | 42.0 | 168 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | sat | t4 | transform/mirror_h_rot90/direct | direct | 33.0 | 132 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | sat | t4 | transform/mirror_h_rot90/oracle | oracle | 40.8 | 163 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | sat | t4 | transform/rot180/direct | direct | 35.5 | 142 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | sat | t4 | transform/rot180/oracle | oracle | 41.2 | 165 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | sat | t4 | transform/rot270/direct | direct | 33.2 | 133 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | sat | t4 | transform/rot270/oracle | oracle | 42.2 | 169 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | sat | t4 | transform/rot90/direct | direct | 32.2 | 129 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | sat | t4 | transform/rot90/oracle | oracle | 41.5 | 166 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | sat | t4 | world/intervention_001/direct | direct | 24.5 | 49 | 200 | 200 | 0 |
| Bagel-7B-MoT | direct | sat | t4 | world/intervention_001/oracle | oracle | 48.5 | 97 | 200 | 200 | 0 |
| Bagel-7B-MoT | direct | sat | t4 | world/sham_001/direct | direct | 26.5 | 53 | 200 | 200 | 0 |
| Bagel-7B-MoT | direct | sat | t4 | world/sham_001/oracle | oracle | 35.0 | 70 | 200 | 200 | 0 |
| Bagel-7B-MoT | direct | webrd04 | t1 | base/direct | direct | 62.2 | 249 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | webrd04 | t1 | base/oracle | oracle | 66.5 | 266 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | webrd04 | t2 | base/direct | direct | 59.5 | 238 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | webrd04 | t2 | base/oracle | oracle | 62.0 | 248 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | webrd04 | t3 | base/direct | direct | 32.0 | 64 | 200 | 200 | 0 |
| Bagel-7B-MoT | direct | webrd04 | t3 | base/oracle | oracle | 38.5 | 77 | 200 | 200 | 0 |
| Bagel-7B-MoT | direct | webrd04 | t3 | world/intervention_001/direct | direct | 48.0 | 96 | 200 | 200 | 0 |
| Bagel-7B-MoT | direct | webrd04 | t3 | world/intervention_001/oracle | oracle | 53.0 | 106 | 200 | 200 | 0 |
| Bagel-7B-MoT | direct | webrd04 | t3 | world/sham_001/direct | direct | 25.5 | 51 | 200 | 200 | 0 |
| Bagel-7B-MoT | direct | webrd04 | t3 | world/sham_001/oracle | oracle | 28.5 | 57 | 200 | 200 | 0 |
| Bagel-7B-MoT | direct | webrd04 | t4 | base/direct | direct | 34.8 | 139 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | webrd04 | t4 | base/oracle | oracle | 43.8 | 175 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | webrd04 | t4 | world/intervention_001/direct | direct | 19.0 | 38 | 200 | 200 | 0 |
| Bagel-7B-MoT | direct | webrd04 | t4 | world/intervention_001/oracle | oracle | 55.5 | 111 | 200 | 200 | 0 |
| Bagel-7B-MoT | direct | webrd04 | t4 | world/sham_001/direct | direct | 30.5 | 61 | 200 | 200 | 0 |
| Bagel-7B-MoT | direct | webrd04 | t4 | world/sham_001/oracle | oracle | 37.5 | 75 | 200 | 200 | 0 |
| Bagel-7B-MoT | direct | wprd01 | t1 | base/direct | direct | 78.5 | 314 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | wprd01 | t1 | base/oracle | oracle | 67.0 | 268 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | wprd01 | t1 | transform/mirror_h/direct | direct | 64.5 | 258 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | wprd01 | t1 | transform/mirror_h/oracle | oracle | 64.5 | 258 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | wprd01 | t1 | transform/mirror_h_rot180/direct | direct | 63.0 | 252 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | wprd01 | t1 | transform/mirror_h_rot180/oracle | oracle | 62.0 | 248 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | wprd01 | t1 | transform/mirror_h_rot270/direct | direct | 58.2 | 233 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | wprd01 | t1 | transform/mirror_h_rot270/oracle | oracle | 54.5 | 218 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | wprd01 | t1 | transform/mirror_h_rot90/direct | direct | 63.5 | 254 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | wprd01 | t1 | transform/mirror_h_rot90/oracle | oracle | 65.2 | 261 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | wprd01 | t1 | transform/rot180/direct | direct | 60.2 | 241 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | wprd01 | t1 | transform/rot180/oracle | oracle | 62.8 | 251 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | wprd01 | t1 | transform/rot270/direct | direct | 62.8 | 251 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | wprd01 | t1 | transform/rot270/oracle | oracle | 63.8 | 255 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | wprd01 | t1 | transform/rot90/direct | direct | 64.0 | 256 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | wprd01 | t1 | transform/rot90/oracle | oracle | 65.5 | 262 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | wprd01 | t2 | base/direct | direct | 47.2 | 189 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | wprd01 | t2 | base/oracle | oracle | 61.2 | 245 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | wprd01 | t2 | transform/mirror_h/direct | direct | 59.0 | 236 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | wprd01 | t2 | transform/mirror_h/oracle | oracle | 63.2 | 253 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | wprd01 | t2 | transform/mirror_h_rot180/direct | direct | 59.8 | 239 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | wprd01 | t2 | transform/mirror_h_rot180/oracle | oracle | 61.5 | 246 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | wprd01 | t2 | transform/mirror_h_rot270/direct | direct | 59.0 | 236 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | wprd01 | t2 | transform/mirror_h_rot270/oracle | oracle | 60.5 | 242 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | wprd01 | t2 | transform/mirror_h_rot90/direct | direct | 57.0 | 228 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | wprd01 | t2 | transform/mirror_h_rot90/oracle | oracle | 58.8 | 235 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | wprd01 | t2 | transform/rot180/direct | direct | 62.0 | 248 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | wprd01 | t2 | transform/rot180/oracle | oracle | 62.8 | 251 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | wprd01 | t2 | transform/rot270/direct | direct | 60.5 | 242 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | wprd01 | t2 | transform/rot270/oracle | oracle | 61.8 | 247 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | wprd01 | t2 | transform/rot90/direct | direct | 58.0 | 232 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | wprd01 | t2 | transform/rot90/oracle | oracle | 61.0 | 244 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | wprd01 | t3 | base/direct | direct | 7.5 | 15 | 200 | 200 | 0 |
| Bagel-7B-MoT | direct | wprd01 | t3 | base/oracle | oracle | 10.5 | 21 | 200 | 200 | 0 |
| Bagel-7B-MoT | direct | wprd01 | t3 | transform/mirror_h/direct | direct | 6.0 | 12 | 200 | 200 | 0 |
| Bagel-7B-MoT | direct | wprd01 | t3 | transform/mirror_h/oracle | oracle | 11.0 | 22 | 200 | 200 | 0 |
| Bagel-7B-MoT | direct | wprd01 | t3 | transform/mirror_h_rot180/direct | direct | 7.0 | 14 | 200 | 200 | 0 |
| Bagel-7B-MoT | direct | wprd01 | t3 | transform/mirror_h_rot180/oracle | oracle | 12.0 | 24 | 200 | 200 | 0 |
| Bagel-7B-MoT | direct | wprd01 | t3 | transform/mirror_h_rot270/direct | direct | 8.5 | 17 | 200 | 200 | 0 |
| Bagel-7B-MoT | direct | wprd01 | t3 | transform/mirror_h_rot270/oracle | oracle | 18.5 | 37 | 200 | 200 | 0 |
| Bagel-7B-MoT | direct | wprd01 | t3 | transform/mirror_h_rot90/direct | direct | 7.5 | 15 | 200 | 200 | 0 |
| Bagel-7B-MoT | direct | wprd01 | t3 | transform/mirror_h_rot90/oracle | oracle | 19.0 | 38 | 200 | 200 | 0 |
| Bagel-7B-MoT | direct | wprd01 | t3 | transform/rot180/direct | direct | 7.5 | 15 | 200 | 200 | 0 |
| Bagel-7B-MoT | direct | wprd01 | t3 | transform/rot180/oracle | oracle | 12.5 | 25 | 200 | 200 | 0 |
| Bagel-7B-MoT | direct | wprd01 | t3 | transform/rot270/direct | direct | 7.5 | 15 | 200 | 200 | 0 |
| Bagel-7B-MoT | direct | wprd01 | t3 | transform/rot270/oracle | oracle | 13.0 | 26 | 200 | 200 | 0 |
| Bagel-7B-MoT | direct | wprd01 | t3 | transform/rot90/direct | direct | 8.0 | 16 | 200 | 200 | 0 |
| Bagel-7B-MoT | direct | wprd01 | t3 | transform/rot90/oracle | oracle | 17.5 | 35 | 200 | 200 | 0 |
| Bagel-7B-MoT | direct | wprd01 | t3 | world/intervention_001/direct | direct | 46.5 | 93 | 200 | 200 | 0 |
| Bagel-7B-MoT | direct | wprd01 | t3 | world/intervention_001/oracle | oracle | 47.5 | 95 | 200 | 200 | 0 |
| Bagel-7B-MoT | direct | wprd01 | t3 | world/sham_001/direct | direct | 7.0 | 14 | 200 | 200 | 0 |
| Bagel-7B-MoT | direct | wprd01 | t3 | world/sham_001/oracle | oracle | 10.0 | 20 | 200 | 200 | 0 |
| Bagel-7B-MoT | direct | wprd01 | t4 | base/direct | direct | 38.0 | 152 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | wprd01 | t4 | base/oracle | oracle | 45.8 | 183 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | wprd01 | t4 | transform/mirror_h/direct | direct | 37.5 | 150 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | wprd01 | t4 | transform/mirror_h/oracle | oracle | 45.2 | 181 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | wprd01 | t4 | transform/mirror_h_rot180/direct | direct | 37.8 | 151 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | wprd01 | t4 | transform/mirror_h_rot180/oracle | oracle | 44.5 | 178 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | wprd01 | t4 | transform/mirror_h_rot270/direct | direct | 35.5 | 142 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | wprd01 | t4 | transform/mirror_h_rot270/oracle | oracle | 44.0 | 176 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | wprd01 | t4 | transform/mirror_h_rot90/direct | direct | 35.5 | 142 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | wprd01 | t4 | transform/mirror_h_rot90/oracle | oracle | 43.2 | 173 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | wprd01 | t4 | transform/rot180/direct | direct | 38.0 | 152 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | wprd01 | t4 | transform/rot180/oracle | oracle | 45.2 | 181 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | wprd01 | t4 | transform/rot270/direct | direct | 35.2 | 141 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | wprd01 | t4 | transform/rot270/oracle | oracle | 45.5 | 182 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | wprd01 | t4 | transform/rot90/direct | direct | 35.5 | 142 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | wprd01 | t4 | transform/rot90/oracle | oracle | 44.2 | 177 | 400 | 400 | 0 |
| Bagel-7B-MoT | direct | wprd01 | t4 | world/intervention_001/direct | direct | 23.0 | 46 | 200 | 200 | 0 |
| Bagel-7B-MoT | direct | wprd01 | t4 | world/intervention_001/oracle | oracle | 47.5 | 95 | 200 | 200 | 0 |
| Bagel-7B-MoT | direct | wprd01 | t4 | world/sham_001/direct | direct | 31.0 | 62 | 200 | 200 | 0 |
| Bagel-7B-MoT | direct | wprd01 | t4 | world/sham_001/oracle | oracle | 38.0 | 76 | 200 | 200 | 0 |
| JoyAI-Image | direct | blank | t1 | base/direct | direct | 61.0 | 244 | 400 | 400 | 0 |
| JoyAI-Image | direct | blank | t1 | base/oracle | oracle | 68.5 | 274 | 400 | 400 | 0 |
| JoyAI-Image | direct | blank | t1 | transform/mirror_h/direct | direct | 60.0 | 240 | 400 | 400 | 0 |
| JoyAI-Image | direct | blank | t1 | transform/mirror_h/oracle | oracle | 61.2 | 245 | 400 | 400 | 0 |
| JoyAI-Image | direct | blank | t1 | transform/mirror_h_rot180/direct | direct | 54.8 | 219 | 400 | 400 | 0 |
| JoyAI-Image | direct | blank | t1 | transform/mirror_h_rot180/oracle | oracle | 56.8 | 227 | 400 | 400 | 0 |
| JoyAI-Image | direct | blank | t1 | transform/mirror_h_rot270/direct | direct | 49.8 | 199 | 400 | 400 | 0 |
| JoyAI-Image | direct | blank | t1 | transform/mirror_h_rot270/oracle | oracle | 50.2 | 201 | 400 | 400 | 0 |
| JoyAI-Image | direct | blank | t1 | transform/mirror_h_rot90/direct | direct | 54.0 | 216 | 400 | 400 | 0 |
| JoyAI-Image | direct | blank | t1 | transform/mirror_h_rot90/oracle | oracle | 52.8 | 211 | 400 | 400 | 0 |
| JoyAI-Image | direct | blank | t1 | transform/rot180/direct | direct | 59.8 | 239 | 400 | 400 | 0 |
| JoyAI-Image | direct | blank | t1 | transform/rot180/oracle | oracle | 66.8 | 267 | 400 | 400 | 0 |
| JoyAI-Image | direct | blank | t1 | transform/rot270/direct | direct | 66.5 | 266 | 400 | 400 | 0 |
| JoyAI-Image | direct | blank | t1 | transform/rot270/oracle | oracle | 74.2 | 297 | 400 | 400 | 0 |
| JoyAI-Image | direct | blank | t1 | transform/rot90/direct | direct | 64.0 | 256 | 400 | 400 | 0 |
| JoyAI-Image | direct | blank | t1 | transform/rot90/oracle | oracle | 70.5 | 282 | 400 | 400 | 0 |
| JoyAI-Image | direct | blank | t2 | base/direct | direct | 49.0 | 196 | 400 | 400 | 0 |
| JoyAI-Image | direct | blank | t2 | base/oracle | oracle | 55.8 | 223 | 400 | 400 | 0 |
| JoyAI-Image | direct | blank | t2 | transform/mirror_h/direct | direct | 52.0 | 208 | 400 | 400 | 0 |
| JoyAI-Image | direct | blank | t2 | transform/mirror_h/oracle | oracle | 62.5 | 250 | 400 | 400 | 0 |
| JoyAI-Image | direct | blank | t2 | transform/mirror_h_rot180/direct | direct | 51.2 | 205 | 400 | 400 | 0 |
| JoyAI-Image | direct | blank | t2 | transform/mirror_h_rot180/oracle | oracle | 56.0 | 224 | 400 | 400 | 0 |
| JoyAI-Image | direct | blank | t2 | transform/mirror_h_rot270/direct | direct | 55.5 | 222 | 400 | 400 | 0 |
| JoyAI-Image | direct | blank | t2 | transform/mirror_h_rot270/oracle | oracle | 61.0 | 244 | 400 | 400 | 0 |
| JoyAI-Image | direct | blank | t2 | transform/mirror_h_rot90/direct | direct | 52.5 | 210 | 400 | 400 | 0 |
| JoyAI-Image | direct | blank | t2 | transform/mirror_h_rot90/oracle | oracle | 62.5 | 250 | 400 | 400 | 0 |
| JoyAI-Image | direct | blank | t2 | transform/rot180/direct | direct | 51.2 | 205 | 400 | 400 | 0 |
| JoyAI-Image | direct | blank | t2 | transform/rot180/oracle | oracle | 60.0 | 240 | 400 | 400 | 0 |
| JoyAI-Image | direct | blank | t2 | transform/rot270/direct | direct | 52.5 | 210 | 400 | 400 | 0 |
| JoyAI-Image | direct | blank | t2 | transform/rot270/oracle | oracle | 57.8 | 231 | 400 | 400 | 0 |
| JoyAI-Image | direct | blank | t2 | transform/rot90/direct | direct | 49.8 | 199 | 400 | 400 | 0 |
| JoyAI-Image | direct | blank | t2 | transform/rot90/oracle | oracle | 57.2 | 229 | 400 | 400 | 0 |
| JoyAI-Image | direct | sat | t1 | base/direct | direct | 61.2 | 245 | 400 | 400 | 0 |
| JoyAI-Image | direct | sat | t1 | base/oracle | oracle | 64.5 | 258 | 400 | 400 | 0 |
| JoyAI-Image | direct | sat | t1 | transform/mirror_h/direct | direct | 55.5 | 222 | 400 | 400 | 0 |
| JoyAI-Image | direct | sat | t1 | transform/mirror_h/oracle | oracle | 65.0 | 260 | 400 | 400 | 0 |
| JoyAI-Image | direct | sat | t1 | transform/mirror_h_rot180/direct | direct | 48.2 | 193 | 400 | 400 | 0 |
| JoyAI-Image | direct | sat | t1 | transform/mirror_h_rot180/oracle | oracle | 53.2 | 213 | 400 | 400 | 0 |
| JoyAI-Image | direct | sat | t1 | transform/mirror_h_rot270/direct | direct | 49.0 | 196 | 400 | 400 | 0 |
| JoyAI-Image | direct | sat | t1 | transform/mirror_h_rot270/oracle | oracle | 49.0 | 196 | 400 | 400 | 0 |
| JoyAI-Image | direct | sat | t1 | transform/mirror_h_rot90/direct | direct | 47.5 | 190 | 400 | 400 | 0 |
| JoyAI-Image | direct | sat | t1 | transform/mirror_h_rot90/oracle | oracle | 56.0 | 224 | 400 | 400 | 0 |
| JoyAI-Image | direct | sat | t1 | transform/rot180/direct | direct | 57.2 | 229 | 400 | 400 | 0 |
| JoyAI-Image | direct | sat | t1 | transform/rot180/oracle | oracle | 67.2 | 269 | 400 | 400 | 0 |
| JoyAI-Image | direct | sat | t1 | transform/rot270/direct | direct | 65.2 | 261 | 400 | 400 | 0 |
| JoyAI-Image | direct | sat | t1 | transform/rot270/oracle | oracle | 71.0 | 284 | 400 | 400 | 0 |
| JoyAI-Image | direct | sat | t1 | transform/rot90/direct | direct | 62.0 | 248 | 400 | 400 | 0 |
| JoyAI-Image | direct | sat | t1 | transform/rot90/oracle | oracle | 67.8 | 271 | 400 | 400 | 0 |
| JoyAI-Image | direct | sat | t2 | base/direct | direct | 41.2 | 165 | 400 | 400 | 0 |
| JoyAI-Image | direct | sat | t2 | base/oracle | oracle | 46.8 | 187 | 400 | 400 | 0 |
| JoyAI-Image | direct | sat | t2 | transform/mirror_h/direct | direct | 45.8 | 183 | 400 | 400 | 0 |
| JoyAI-Image | direct | sat | t2 | transform/mirror_h/oracle | oracle | 56.0 | 224 | 400 | 400 | 0 |
| JoyAI-Image | direct | sat | t2 | transform/mirror_h_rot180/direct | direct | 47.0 | 188 | 400 | 400 | 0 |
| JoyAI-Image | direct | sat | t2 | transform/mirror_h_rot180/oracle | oracle | 51.0 | 204 | 400 | 400 | 0 |
| JoyAI-Image | direct | sat | t2 | transform/mirror_h_rot270/direct | direct | 47.5 | 190 | 400 | 400 | 0 |
| JoyAI-Image | direct | sat | t2 | transform/mirror_h_rot270/oracle | oracle | 55.5 | 222 | 400 | 400 | 0 |
| JoyAI-Image | direct | sat | t2 | transform/mirror_h_rot90/direct | direct | 48.2 | 193 | 400 | 400 | 0 |
| JoyAI-Image | direct | sat | t2 | transform/mirror_h_rot90/oracle | oracle | 53.2 | 213 | 400 | 400 | 0 |
| JoyAI-Image | direct | sat | t2 | transform/rot180/direct | direct | 44.2 | 177 | 400 | 400 | 0 |
| JoyAI-Image | direct | sat | t2 | transform/rot180/oracle | oracle | 52.2 | 209 | 400 | 400 | 0 |
| JoyAI-Image | direct | sat | t2 | transform/rot270/direct | direct | 49.0 | 196 | 400 | 400 | 0 |
| JoyAI-Image | direct | sat | t2 | transform/rot270/oracle | oracle | 56.5 | 226 | 400 | 400 | 0 |
| JoyAI-Image | direct | sat | t2 | transform/rot90/direct | direct | 48.8 | 195 | 400 | 400 | 0 |
| JoyAI-Image | direct | sat | t2 | transform/rot90/oracle | oracle | 54.2 | 217 | 400 | 400 | 0 |
| JoyAI-Image | direct | sat | t3 | base/direct | direct | 34.0 | 68 | 200 | 200 | 0 |
| JoyAI-Image | direct | sat | t3 | base/oracle | oracle | 35.5 | 71 | 200 | 200 | 0 |
| JoyAI-Image | direct | sat | t3 | transform/mirror_h/direct | direct | 33.5 | 67 | 200 | 200 | 0 |
| JoyAI-Image | direct | sat | t3 | transform/mirror_h/oracle | oracle | 37.0 | 74 | 200 | 200 | 0 |
| JoyAI-Image | direct | sat | t3 | transform/mirror_h_rot180/direct | direct | 31.0 | 62 | 200 | 200 | 0 |
| JoyAI-Image | direct | sat | t3 | transform/mirror_h_rot180/oracle | oracle | 37.5 | 75 | 200 | 200 | 0 |
| JoyAI-Image | direct | sat | t3 | transform/mirror_h_rot270/direct | direct | 31.0 | 62 | 200 | 200 | 0 |
| JoyAI-Image | direct | sat | t3 | transform/mirror_h_rot270/oracle | oracle | 32.0 | 64 | 200 | 200 | 0 |
| JoyAI-Image | direct | sat | t3 | transform/mirror_h_rot90/direct | direct | 34.5 | 69 | 200 | 200 | 0 |
| JoyAI-Image | direct | sat | t3 | transform/mirror_h_rot90/oracle | oracle | 36.0 | 72 | 200 | 200 | 0 |
| JoyAI-Image | direct | sat | t3 | transform/rot180/direct | direct | 34.0 | 68 | 200 | 200 | 0 |
| JoyAI-Image | direct | sat | t3 | transform/rot180/oracle | oracle | 39.0 | 78 | 200 | 200 | 0 |
| JoyAI-Image | direct | sat | t3 | transform/rot270/direct | direct | 33.0 | 66 | 200 | 200 | 0 |
| JoyAI-Image | direct | sat | t3 | transform/rot270/oracle | oracle | 36.5 | 73 | 200 | 200 | 0 |
| JoyAI-Image | direct | sat | t3 | transform/rot90/direct | direct | 31.5 | 63 | 200 | 200 | 0 |
| JoyAI-Image | direct | sat | t3 | transform/rot90/oracle | oracle | 35.0 | 70 | 200 | 200 | 0 |
| JoyAI-Image | direct | sat | t3 | world/intervention_001/direct | direct | 36.5 | 73 | 200 | 200 | 0 |
| JoyAI-Image | direct | sat | t3 | world/intervention_001/oracle | oracle | 35.5 | 71 | 200 | 200 | 0 |
| JoyAI-Image | direct | sat | t3 | world/sham_001/direct | direct | 31.0 | 62 | 200 | 200 | 0 |
| JoyAI-Image | direct | sat | t3 | world/sham_001/oracle | oracle | 35.0 | 70 | 200 | 200 | 0 |
| JoyAI-Image | direct | sat | t4 | base/direct | direct | 46.5 | 186 | 400 | 400 | 0 |
| JoyAI-Image | direct | sat | t4 | base/oracle | oracle | 56.2 | 225 | 400 | 400 | 0 |
| JoyAI-Image | direct | sat | t4 | transform/mirror_h/direct | direct | 48.8 | 195 | 400 | 400 | 0 |
| JoyAI-Image | direct | sat | t4 | transform/mirror_h/oracle | oracle | 58.8 | 235 | 400 | 400 | 0 |
| JoyAI-Image | direct | sat | t4 | transform/mirror_h_rot180/direct | direct | 50.0 | 200 | 400 | 400 | 0 |
| JoyAI-Image | direct | sat | t4 | transform/mirror_h_rot180/oracle | oracle | 55.5 | 222 | 400 | 400 | 0 |
| JoyAI-Image | direct | sat | t4 | transform/mirror_h_rot270/direct | direct | 51.5 | 206 | 400 | 400 | 0 |
| JoyAI-Image | direct | sat | t4 | transform/mirror_h_rot270/oracle | oracle | 59.2 | 237 | 400 | 400 | 0 |
| JoyAI-Image | direct | sat | t4 | transform/mirror_h_rot90/direct | direct | 43.2 | 173 | 400 | 400 | 0 |
| JoyAI-Image | direct | sat | t4 | transform/mirror_h_rot90/oracle | oracle | 54.5 | 218 | 400 | 400 | 0 |
| JoyAI-Image | direct | sat | t4 | transform/rot180/direct | direct | 50.8 | 203 | 400 | 400 | 0 |
| JoyAI-Image | direct | sat | t4 | transform/rot180/oracle | oracle | 58.2 | 233 | 400 | 400 | 0 |
| JoyAI-Image | direct | sat | t4 | transform/rot270/direct | direct | 48.8 | 195 | 400 | 400 | 0 |
| JoyAI-Image | direct | sat | t4 | transform/rot270/oracle | oracle | 55.0 | 220 | 400 | 400 | 0 |
| JoyAI-Image | direct | sat | t4 | transform/rot90/direct | direct | 48.8 | 195 | 400 | 400 | 0 |
| JoyAI-Image | direct | sat | t4 | transform/rot90/oracle | oracle | 54.0 | 216 | 400 | 400 | 0 |
| JoyAI-Image | direct | sat | t4 | world/intervention_001/direct | direct | 22.5 | 45 | 200 | 200 | 0 |
| JoyAI-Image | direct | sat | t4 | world/intervention_001/oracle | oracle | 49.5 | 99 | 200 | 200 | 0 |
| JoyAI-Image | direct | sat | t4 | world/sham_001/direct | direct | 48.5 | 97 | 200 | 200 | 0 |
| JoyAI-Image | direct | sat | t4 | world/sham_001/oracle | oracle | 54.5 | 109 | 200 | 200 | 0 |
| JoyAI-Image | direct | webrd04 | t1 | base/direct | direct | 62.2 | 249 | 400 | 400 | 0 |
| JoyAI-Image | direct | webrd04 | t1 | base/oracle | oracle | 68.5 | 274 | 400 | 400 | 0 |
| JoyAI-Image | direct | webrd04 | t2 | base/direct | direct | 42.2 | 169 | 400 | 400 | 0 |
| JoyAI-Image | direct | webrd04 | t2 | base/oracle | oracle | 45.5 | 182 | 400 | 400 | 0 |
| JoyAI-Image | direct | webrd04 | t3 | base/direct | direct | 35.0 | 70 | 200 | 200 | 0 |
| JoyAI-Image | direct | webrd04 | t3 | base/oracle | oracle | 32.5 | 65 | 200 | 200 | 0 |
| JoyAI-Image | direct | webrd04 | t3 | world/intervention_001/direct | direct | 39.5 | 79 | 200 | 200 | 0 |
| JoyAI-Image | direct | webrd04 | t3 | world/intervention_001/oracle | oracle | 38.5 | 77 | 200 | 200 | 0 |
| JoyAI-Image | direct | webrd04 | t3 | world/sham_001/direct | direct | 35.5 | 71 | 200 | 200 | 0 |
| JoyAI-Image | direct | webrd04 | t3 | world/sham_001/oracle | oracle | 35.0 | 70 | 200 | 200 | 0 |
| JoyAI-Image | direct | webrd04 | t4 | base/direct | direct | 43.8 | 175 | 400 | 400 | 0 |
| JoyAI-Image | direct | webrd04 | t4 | base/oracle | oracle | 48.2 | 193 | 400 | 400 | 0 |
| JoyAI-Image | direct | webrd04 | t4 | world/intervention_001/direct | direct | 24.0 | 48 | 200 | 200 | 0 |
| JoyAI-Image | direct | webrd04 | t4 | world/intervention_001/oracle | oracle | 37.5 | 75 | 200 | 200 | 0 |
| JoyAI-Image | direct | webrd04 | t4 | world/sham_001/direct | direct | 41.0 | 82 | 200 | 200 | 0 |
| JoyAI-Image | direct | webrd04 | t4 | world/sham_001/oracle | oracle | 48.5 | 97 | 200 | 200 | 0 |
| JoyAI-Image | direct | wprd01 | t1 | base/direct | direct | 60.8 | 243 | 400 | 400 | 0 |
| JoyAI-Image | direct | wprd01 | t1 | base/oracle | oracle | 66.8 | 267 | 400 | 400 | 0 |
| JoyAI-Image | direct | wprd01 | t1 | transform/mirror_h/direct | direct | 57.2 | 229 | 400 | 400 | 0 |
| JoyAI-Image | direct | wprd01 | t1 | transform/mirror_h/oracle | oracle | 62.8 | 251 | 400 | 400 | 0 |
| JoyAI-Image | direct | wprd01 | t1 | transform/mirror_h_rot180/direct | direct | 56.5 | 226 | 400 | 400 | 0 |
| JoyAI-Image | direct | wprd01 | t1 | transform/mirror_h_rot180/oracle | oracle | 61.8 | 247 | 400 | 400 | 0 |
| JoyAI-Image | direct | wprd01 | t1 | transform/mirror_h_rot270/direct | direct | 52.5 | 210 | 400 | 400 | 0 |
| JoyAI-Image | direct | wprd01 | t1 | transform/mirror_h_rot270/oracle | oracle | 55.5 | 222 | 400 | 400 | 0 |
| JoyAI-Image | direct | wprd01 | t1 | transform/mirror_h_rot90/direct | direct | 46.8 | 187 | 400 | 400 | 0 |
| JoyAI-Image | direct | wprd01 | t1 | transform/mirror_h_rot90/oracle | oracle | 56.8 | 227 | 400 | 400 | 0 |
| JoyAI-Image | direct | wprd01 | t1 | transform/rot180/direct | direct | 60.5 | 242 | 400 | 400 | 0 |
| JoyAI-Image | direct | wprd01 | t1 | transform/rot180/oracle | oracle | 72.2 | 289 | 400 | 400 | 0 |
| JoyAI-Image | direct | wprd01 | t1 | transform/rot270/direct | direct | 62.8 | 251 | 400 | 400 | 0 |
| JoyAI-Image | direct | wprd01 | t1 | transform/rot270/oracle | oracle | 76.5 | 306 | 400 | 400 | 0 |
| JoyAI-Image | direct | wprd01 | t1 | transform/rot90/direct | direct | 67.0 | 268 | 400 | 400 | 0 |
| JoyAI-Image | direct | wprd01 | t1 | transform/rot90/oracle | oracle | 75.2 | 301 | 400 | 400 | 0 |
| JoyAI-Image | direct | wprd01 | t2 | base/direct | direct | 51.5 | 206 | 400 | 400 | 0 |
| JoyAI-Image | direct | wprd01 | t2 | base/oracle | oracle | 45.2 | 181 | 400 | 400 | 0 |
| JoyAI-Image | direct | wprd01 | t2 | transform/mirror_h/direct | direct | 39.8 | 159 | 400 | 400 | 0 |
| JoyAI-Image | direct | wprd01 | t2 | transform/mirror_h/oracle | oracle | 44.2 | 177 | 400 | 400 | 0 |
| JoyAI-Image | direct | wprd01 | t2 | transform/mirror_h_rot180/direct | direct | 42.8 | 171 | 400 | 400 | 0 |
| JoyAI-Image | direct | wprd01 | t2 | transform/mirror_h_rot180/oracle | oracle | 45.2 | 181 | 400 | 400 | 0 |
| JoyAI-Image | direct | wprd01 | t2 | transform/mirror_h_rot270/direct | direct | 43.8 | 175 | 400 | 400 | 0 |
| JoyAI-Image | direct | wprd01 | t2 | transform/mirror_h_rot270/oracle | oracle | 44.0 | 176 | 400 | 400 | 0 |
| JoyAI-Image | direct | wprd01 | t2 | transform/mirror_h_rot90/direct | direct | 43.2 | 173 | 400 | 400 | 0 |
| JoyAI-Image | direct | wprd01 | t2 | transform/mirror_h_rot90/oracle | oracle | 48.5 | 194 | 400 | 400 | 0 |
| JoyAI-Image | direct | wprd01 | t2 | transform/rot180/direct | direct | 40.0 | 160 | 400 | 400 | 0 |
| JoyAI-Image | direct | wprd01 | t2 | transform/rot180/oracle | oracle | 44.5 | 178 | 400 | 400 | 0 |
| JoyAI-Image | direct | wprd01 | t2 | transform/rot270/direct | direct | 41.5 | 166 | 400 | 400 | 0 |
| JoyAI-Image | direct | wprd01 | t2 | transform/rot270/oracle | oracle | 48.5 | 194 | 400 | 400 | 0 |
| JoyAI-Image | direct | wprd01 | t2 | transform/rot90/direct | direct | 39.8 | 159 | 400 | 400 | 0 |
| JoyAI-Image | direct | wprd01 | t2 | transform/rot90/oracle | oracle | 48.2 | 193 | 400 | 400 | 0 |
| JoyAI-Image | direct | wprd01 | t3 | base/direct | direct | 32.0 | 64 | 200 | 200 | 0 |
| JoyAI-Image | direct | wprd01 | t3 | base/oracle | oracle | 32.0 | 64 | 200 | 200 | 0 |
| JoyAI-Image | direct | wprd01 | t3 | transform/mirror_h/direct | direct | 32.5 | 65 | 200 | 200 | 0 |
| JoyAI-Image | direct | wprd01 | t3 | transform/mirror_h/oracle | oracle | 33.0 | 66 | 200 | 200 | 0 |
| JoyAI-Image | direct | wprd01 | t3 | transform/mirror_h_rot180/direct | direct | 32.0 | 64 | 200 | 200 | 0 |
| JoyAI-Image | direct | wprd01 | t3 | transform/mirror_h_rot180/oracle | oracle | 32.5 | 65 | 200 | 200 | 0 |
| JoyAI-Image | direct | wprd01 | t3 | transform/mirror_h_rot270/direct | direct | 33.5 | 67 | 200 | 200 | 0 |
| JoyAI-Image | direct | wprd01 | t3 | transform/mirror_h_rot270/oracle | oracle | 33.5 | 67 | 200 | 200 | 0 |
| JoyAI-Image | direct | wprd01 | t3 | transform/mirror_h_rot90/direct | direct | 33.0 | 66 | 200 | 200 | 0 |
| JoyAI-Image | direct | wprd01 | t3 | transform/mirror_h_rot90/oracle | oracle | 31.0 | 62 | 200 | 200 | 0 |
| JoyAI-Image | direct | wprd01 | t3 | transform/rot180/direct | direct | 33.5 | 67 | 200 | 200 | 0 |
| JoyAI-Image | direct | wprd01 | t3 | transform/rot180/oracle | oracle | 33.5 | 67 | 200 | 200 | 0 |
| JoyAI-Image | direct | wprd01 | t3 | transform/rot270/direct | direct | 34.0 | 68 | 200 | 200 | 0 |
| JoyAI-Image | direct | wprd01 | t3 | transform/rot270/oracle | oracle | 33.5 | 67 | 200 | 200 | 0 |
| JoyAI-Image | direct | wprd01 | t3 | transform/rot90/direct | direct | 32.0 | 64 | 200 | 200 | 0 |
| JoyAI-Image | direct | wprd01 | t3 | transform/rot90/oracle | oracle | 33.5 | 67 | 200 | 200 | 0 |
| JoyAI-Image | direct | wprd01 | t3 | world/intervention_001/direct | direct | 40.0 | 80 | 200 | 200 | 0 |
| JoyAI-Image | direct | wprd01 | t3 | world/intervention_001/oracle | oracle | 39.5 | 79 | 200 | 200 | 0 |
| JoyAI-Image | direct | wprd01 | t3 | world/sham_001/direct | direct | 30.0 | 60 | 200 | 200 | 0 |
| JoyAI-Image | direct | wprd01 | t3 | world/sham_001/oracle | oracle | 33.0 | 66 | 200 | 200 | 0 |
| JoyAI-Image | direct | wprd01 | t4 | base/direct | direct | 46.0 | 184 | 400 | 400 | 0 |
| JoyAI-Image | direct | wprd01 | t4 | base/oracle | oracle | 52.0 | 208 | 400 | 400 | 0 |
| JoyAI-Image | direct | wprd01 | t4 | transform/mirror_h/direct | direct | 46.0 | 184 | 400 | 400 | 0 |
| JoyAI-Image | direct | wprd01 | t4 | transform/mirror_h/oracle | oracle | 50.5 | 202 | 400 | 400 | 0 |
| JoyAI-Image | direct | wprd01 | t4 | transform/mirror_h_rot180/direct | direct | 46.0 | 184 | 400 | 400 | 0 |
| JoyAI-Image | direct | wprd01 | t4 | transform/mirror_h_rot180/oracle | oracle | 54.2 | 217 | 400 | 400 | 0 |
| JoyAI-Image | direct | wprd01 | t4 | transform/mirror_h_rot270/direct | direct | 47.2 | 189 | 400 | 400 | 0 |
| JoyAI-Image | direct | wprd01 | t4 | transform/mirror_h_rot270/oracle | oracle | 52.8 | 211 | 400 | 400 | 0 |
| JoyAI-Image | direct | wprd01 | t4 | transform/mirror_h_rot90/direct | direct | 40.8 | 163 | 400 | 400 | 0 |
| JoyAI-Image | direct | wprd01 | t4 | transform/mirror_h_rot90/oracle | oracle | 49.8 | 199 | 400 | 400 | 0 |
| JoyAI-Image | direct | wprd01 | t4 | transform/rot180/direct | direct | 48.0 | 192 | 400 | 400 | 0 |
| JoyAI-Image | direct | wprd01 | t4 | transform/rot180/oracle | oracle | 52.5 | 210 | 400 | 400 | 0 |
| JoyAI-Image | direct | wprd01 | t4 | transform/rot270/direct | direct | 45.5 | 182 | 400 | 400 | 0 |
| JoyAI-Image | direct | wprd01 | t4 | transform/rot270/oracle | oracle | 52.5 | 210 | 400 | 400 | 0 |
| JoyAI-Image | direct | wprd01 | t4 | transform/rot90/direct | direct | 45.8 | 183 | 400 | 400 | 0 |
| JoyAI-Image | direct | wprd01 | t4 | transform/rot90/oracle | oracle | 47.8 | 191 | 400 | 400 | 0 |
| JoyAI-Image | direct | wprd01 | t4 | world/intervention_001/direct | direct | 22.5 | 45 | 200 | 200 | 0 |
| JoyAI-Image | direct | wprd01 | t4 | world/intervention_001/oracle | oracle | 45.5 | 91 | 200 | 200 | 0 |
| JoyAI-Image | direct | wprd01 | t4 | world/sham_001/direct | direct | 47.5 | 95 | 200 | 200 | 0 |
| JoyAI-Image | direct | wprd01 | t4 | world/sham_001/oracle | oracle | 54.0 | 108 | 200 | 200 | 0 |
| Step3-VL-10B | direct | blank | t1 | base/direct | direct | 76.5 | 306 | 400 | 400 | 0 |
| Step3-VL-10B | direct | blank | t1 | base/oracle | oracle | 74.8 | 299 | 400 | 400 | 0 |
| Step3-VL-10B | direct | blank | t1 | transform/mirror_h/direct | direct | 61.0 | 244 | 400 | 400 | 0 |
| Step3-VL-10B | direct | blank | t1 | transform/mirror_h/oracle | oracle | 65.8 | 263 | 400 | 400 | 0 |
| Step3-VL-10B | direct | blank | t1 | transform/mirror_h_rot180/direct | direct | 61.2 | 245 | 400 | 400 | 0 |
| Step3-VL-10B | direct | blank | t1 | transform/mirror_h_rot180/oracle | oracle | 60.5 | 242 | 400 | 400 | 0 |
| Step3-VL-10B | direct | blank | t1 | transform/mirror_h_rot270/direct | direct | 63.8 | 255 | 400 | 400 | 0 |
| Step3-VL-10B | direct | blank | t1 | transform/mirror_h_rot270/oracle | oracle | 67.8 | 271 | 400 | 400 | 0 |
| Step3-VL-10B | direct | blank | t1 | transform/mirror_h_rot90/direct | direct | 64.5 | 258 | 400 | 400 | 0 |
| Step3-VL-10B | direct | blank | t1 | transform/mirror_h_rot90/oracle | oracle | 64.2 | 257 | 400 | 400 | 0 |
| Step3-VL-10B | direct | blank | t1 | transform/rot180/direct | direct | 72.8 | 291 | 400 | 400 | 0 |
| Step3-VL-10B | direct | blank | t1 | transform/rot180/oracle | oracle | 72.5 | 290 | 400 | 400 | 0 |
| Step3-VL-10B | direct | blank | t1 | transform/rot270/direct | direct | 72.2 | 289 | 400 | 400 | 0 |
| Step3-VL-10B | direct | blank | t1 | transform/rot270/oracle | oracle | 70.2 | 281 | 400 | 400 | 0 |
| Step3-VL-10B | direct | blank | t1 | transform/rot90/direct | direct | 72.2 | 289 | 400 | 400 | 0 |
| Step3-VL-10B | direct | blank | t1 | transform/rot90/oracle | oracle | 70.8 | 283 | 400 | 400 | 0 |
| Step3-VL-10B | direct | blank | t2 | base/direct | direct | 42.8 | 171 | 400 | 400 | 0 |
| Step3-VL-10B | direct | blank | t2 | base/oracle | oracle | 43.0 | 172 | 400 | 400 | 0 |
| Step3-VL-10B | direct | blank | t2 | transform/mirror_h/direct | direct | 47.5 | 190 | 400 | 400 | 0 |
| Step3-VL-10B | direct | blank | t2 | transform/mirror_h/oracle | oracle | 46.5 | 186 | 400 | 400 | 0 |
| Step3-VL-10B | direct | blank | t2 | transform/mirror_h_rot180/direct | direct | 49.2 | 197 | 400 | 400 | 0 |
| Step3-VL-10B | direct | blank | t2 | transform/mirror_h_rot180/oracle | oracle | 47.2 | 189 | 400 | 400 | 0 |
| Step3-VL-10B | direct | blank | t2 | transform/mirror_h_rot270/direct | direct | 48.8 | 195 | 400 | 400 | 0 |
| Step3-VL-10B | direct | blank | t2 | transform/mirror_h_rot270/oracle | oracle | 45.0 | 180 | 400 | 400 | 0 |
| Step3-VL-10B | direct | blank | t2 | transform/mirror_h_rot90/direct | direct | 46.8 | 187 | 400 | 400 | 0 |
| Step3-VL-10B | direct | blank | t2 | transform/mirror_h_rot90/oracle | oracle | 48.5 | 194 | 400 | 400 | 0 |
| Step3-VL-10B | direct | blank | t2 | transform/rot180/direct | direct | 46.0 | 184 | 400 | 400 | 0 |
| Step3-VL-10B | direct | blank | t2 | transform/rot180/oracle | oracle | 49.5 | 198 | 400 | 400 | 0 |
| Step3-VL-10B | direct | blank | t2 | transform/rot270/direct | direct | 47.2 | 189 | 400 | 400 | 0 |
| Step3-VL-10B | direct | blank | t2 | transform/rot270/oracle | oracle | 44.8 | 179 | 400 | 400 | 0 |
| Step3-VL-10B | direct | blank | t2 | transform/rot90/direct | direct | 45.8 | 183 | 400 | 400 | 0 |
| Step3-VL-10B | direct | blank | t2 | transform/rot90/oracle | oracle | 50.0 | 200 | 400 | 400 | 0 |
| Step3-VL-10B | direct | sat | t1 | base/direct | direct | 71.8 | 287 | 400 | 400 | 0 |
| Step3-VL-10B | direct | sat | t1 | base/oracle | oracle | 75.5 | 302 | 400 | 400 | 0 |
| Step3-VL-10B | direct | sat | t1 | transform/mirror_h/direct | direct | 59.8 | 239 | 400 | 400 | 0 |
| Step3-VL-10B | direct | sat | t1 | transform/mirror_h/oracle | oracle | 55.2 | 221 | 400 | 400 | 0 |
| Step3-VL-10B | direct | sat | t1 | transform/mirror_h_rot180/direct | direct | 56.0 | 224 | 400 | 400 | 0 |
| Step3-VL-10B | direct | sat | t1 | transform/mirror_h_rot180/oracle | oracle | 57.2 | 229 | 400 | 400 | 0 |
| Step3-VL-10B | direct | sat | t1 | transform/mirror_h_rot270/direct | direct | 57.8 | 231 | 400 | 400 | 0 |
| Step3-VL-10B | direct | sat | t1 | transform/mirror_h_rot270/oracle | oracle | 57.5 | 230 | 400 | 400 | 0 |
| Step3-VL-10B | direct | sat | t1 | transform/mirror_h_rot90/direct | direct | 59.0 | 236 | 400 | 400 | 0 |
| Step3-VL-10B | direct | sat | t1 | transform/mirror_h_rot90/oracle | oracle | 65.0 | 260 | 400 | 400 | 0 |
| Step3-VL-10B | direct | sat | t1 | transform/rot180/direct | direct | 70.5 | 282 | 400 | 400 | 0 |
| Step3-VL-10B | direct | sat | t1 | transform/rot180/oracle | oracle | 68.8 | 275 | 400 | 400 | 0 |
| Step3-VL-10B | direct | sat | t1 | transform/rot270/direct | direct | 70.0 | 280 | 400 | 400 | 0 |
| Step3-VL-10B | direct | sat | t1 | transform/rot270/oracle | oracle | 69.2 | 277 | 400 | 400 | 0 |
| Step3-VL-10B | direct | sat | t1 | transform/rot90/direct | direct | 68.5 | 274 | 400 | 400 | 0 |
| Step3-VL-10B | direct | sat | t1 | transform/rot90/oracle | oracle | 71.2 | 285 | 400 | 400 | 0 |
| Step3-VL-10B | direct | sat | t2 | base/direct | direct | 42.2 | 169 | 400 | 400 | 0 |
| Step3-VL-10B | direct | sat | t2 | base/oracle | oracle | 46.5 | 186 | 400 | 400 | 0 |
| Step3-VL-10B | direct | sat | t2 | transform/mirror_h/direct | direct | 41.0 | 164 | 400 | 400 | 0 |
| Step3-VL-10B | direct | sat | t2 | transform/mirror_h/oracle | oracle | 46.8 | 187 | 400 | 400 | 0 |
| Step3-VL-10B | direct | sat | t2 | transform/mirror_h_rot180/direct | direct | 42.0 | 168 | 400 | 400 | 0 |
| Step3-VL-10B | direct | sat | t2 | transform/mirror_h_rot180/oracle | oracle | 46.5 | 186 | 400 | 400 | 0 |
| Step3-VL-10B | direct | sat | t2 | transform/mirror_h_rot270/direct | direct | 43.5 | 174 | 400 | 400 | 0 |
| Step3-VL-10B | direct | sat | t2 | transform/mirror_h_rot270/oracle | oracle | 48.0 | 192 | 400 | 400 | 0 |
| Step3-VL-10B | direct | sat | t2 | transform/mirror_h_rot90/direct | direct | 40.0 | 160 | 400 | 400 | 0 |
| Step3-VL-10B | direct | sat | t2 | transform/mirror_h_rot90/oracle | oracle | 49.0 | 196 | 400 | 400 | 0 |
| Step3-VL-10B | direct | sat | t2 | transform/rot180/direct | direct | 41.8 | 167 | 400 | 400 | 0 |
| Step3-VL-10B | direct | sat | t2 | transform/rot180/oracle | oracle | 49.5 | 198 | 400 | 400 | 0 |
| Step3-VL-10B | direct | sat | t2 | transform/rot270/direct | direct | 42.8 | 171 | 400 | 400 | 0 |
| Step3-VL-10B | direct | sat | t2 | transform/rot270/oracle | oracle | 46.8 | 187 | 400 | 400 | 0 |
| Step3-VL-10B | direct | sat | t2 | transform/rot90/direct | direct | 46.2 | 185 | 400 | 400 | 0 |
| Step3-VL-10B | direct | sat | t2 | transform/rot90/oracle | oracle | 47.2 | 189 | 400 | 400 | 0 |
| Step3-VL-10B | direct | sat | t3 | base/direct | direct | 49.5 | 99 | 200 | 200 | 0 |
| Step3-VL-10B | direct | sat | t3 | base/oracle | oracle | 65.5 | 131 | 200 | 200 | 0 |
| Step3-VL-10B | direct | sat | t3 | transform/mirror_h/direct | direct | 48.5 | 97 | 200 | 200 | 0 |
| Step3-VL-10B | direct | sat | t3 | transform/mirror_h/oracle | oracle | 58.0 | 116 | 200 | 200 | 0 |
| Step3-VL-10B | direct | sat | t3 | transform/mirror_h_rot180/direct | direct | 49.0 | 98 | 200 | 200 | 0 |
| Step3-VL-10B | direct | sat | t3 | transform/mirror_h_rot180/oracle | oracle | 52.5 | 105 | 200 | 200 | 0 |
| Step3-VL-10B | direct | sat | t3 | transform/mirror_h_rot270/direct | direct | 49.0 | 98 | 200 | 200 | 0 |
| Step3-VL-10B | direct | sat | t3 | transform/mirror_h_rot270/oracle | oracle | 58.0 | 116 | 200 | 200 | 0 |
| Step3-VL-10B | direct | sat | t3 | transform/mirror_h_rot90/direct | direct | 52.0 | 104 | 200 | 200 | 0 |
| Step3-VL-10B | direct | sat | t3 | transform/mirror_h_rot90/oracle | oracle | 52.0 | 104 | 200 | 200 | 0 |
| Step3-VL-10B | direct | sat | t3 | transform/rot180/direct | direct | 49.0 | 98 | 200 | 200 | 0 |
| Step3-VL-10B | direct | sat | t3 | transform/rot180/oracle | oracle | 55.5 | 111 | 200 | 200 | 0 |
| Step3-VL-10B | direct | sat | t3 | transform/rot270/direct | direct | 48.0 | 96 | 200 | 200 | 0 |
| Step3-VL-10B | direct | sat | t3 | transform/rot270/oracle | oracle | 59.5 | 119 | 200 | 200 | 0 |
| Step3-VL-10B | direct | sat | t3 | transform/rot90/direct | direct | 47.0 | 94 | 200 | 200 | 0 |
| Step3-VL-10B | direct | sat | t3 | transform/rot90/oracle | oracle | 60.5 | 121 | 200 | 200 | 0 |
| Step3-VL-10B | direct | sat | t3 | world/intervention_001/direct | direct | 32.0 | 64 | 200 | 200 | 0 |
| Step3-VL-10B | direct | sat | t3 | world/intervention_001/oracle | oracle | 37.0 | 74 | 200 | 200 | 0 |
| Step3-VL-10B | direct | sat | t3 | world/sham_001/direct | direct | 41.5 | 83 | 200 | 200 | 0 |
| Step3-VL-10B | direct | sat | t3 | world/sham_001/oracle | oracle | 49.5 | 99 | 200 | 200 | 0 |
| Step3-VL-10B | direct | sat | t4 | base/direct | direct | 37.0 | 148 | 400 | 400 | 0 |
| Step3-VL-10B | direct | sat | t4 | base/oracle | oracle | 51.0 | 204 | 400 | 400 | 0 |
| Step3-VL-10B | direct | sat | t4 | transform/mirror_h/direct | direct | 39.2 | 157 | 400 | 400 | 0 |
| Step3-VL-10B | direct | sat | t4 | transform/mirror_h/oracle | oracle | 54.0 | 216 | 400 | 400 | 0 |
| Step3-VL-10B | direct | sat | t4 | transform/mirror_h_rot180/direct | direct | 36.5 | 146 | 400 | 400 | 0 |
| Step3-VL-10B | direct | sat | t4 | transform/mirror_h_rot180/oracle | oracle | 50.8 | 203 | 400 | 400 | 0 |
| Step3-VL-10B | direct | sat | t4 | transform/mirror_h_rot270/direct | direct | 39.0 | 156 | 400 | 400 | 0 |
| Step3-VL-10B | direct | sat | t4 | transform/mirror_h_rot270/oracle | oracle | 51.5 | 206 | 400 | 400 | 0 |
| Step3-VL-10B | direct | sat | t4 | transform/mirror_h_rot90/direct | direct | 35.5 | 142 | 400 | 400 | 0 |
| Step3-VL-10B | direct | sat | t4 | transform/mirror_h_rot90/oracle | oracle | 51.0 | 204 | 400 | 400 | 0 |
| Step3-VL-10B | direct | sat | t4 | transform/rot180/direct | direct | 37.2 | 149 | 400 | 400 | 0 |
| Step3-VL-10B | direct | sat | t4 | transform/rot180/oracle | oracle | 52.2 | 209 | 400 | 400 | 0 |
| Step3-VL-10B | direct | sat | t4 | transform/rot270/direct | direct | 39.8 | 159 | 400 | 400 | 0 |
| Step3-VL-10B | direct | sat | t4 | transform/rot270/oracle | oracle | 51.5 | 206 | 400 | 400 | 0 |
| Step3-VL-10B | direct | sat | t4 | transform/rot90/direct | direct | 34.5 | 138 | 400 | 400 | 0 |
| Step3-VL-10B | direct | sat | t4 | transform/rot90/oracle | oracle | 51.0 | 204 | 400 | 400 | 0 |
| Step3-VL-10B | direct | sat | t4 | world/intervention_001/direct | direct | 29.0 | 58 | 200 | 200 | 0 |
| Step3-VL-10B | direct | sat | t4 | world/intervention_001/oracle | oracle | 60.5 | 121 | 200 | 200 | 0 |
| Step3-VL-10B | direct | sat | t4 | world/sham_001/direct | direct | 19.5 | 39 | 200 | 200 | 0 |
| Step3-VL-10B | direct | sat | t4 | world/sham_001/oracle | oracle | 40.5 | 81 | 200 | 200 | 0 |
| Step3-VL-10B | direct | webrd04 | t1 | base/direct | direct | 56.8 | 227 | 400 | 400 | 0 |
| Step3-VL-10B | direct | webrd04 | t1 | base/oracle | oracle | 66.0 | 264 | 400 | 400 | 0 |
| Step3-VL-10B | direct | webrd04 | t2 | base/direct | direct | 31.8 | 127 | 400 | 400 | 0 |
| Step3-VL-10B | direct | webrd04 | t2 | base/oracle | oracle | 35.8 | 143 | 400 | 400 | 0 |
| Step3-VL-10B | direct | webrd04 | t3 | base/direct | direct | 46.5 | 93 | 200 | 200 | 0 |
| Step3-VL-10B | direct | webrd04 | t3 | base/oracle | oracle | 45.0 | 90 | 200 | 200 | 0 |
| Step3-VL-10B | direct | webrd04 | t3 | world/intervention_001/direct | direct | 25.5 | 51 | 200 | 200 | 0 |
| Step3-VL-10B | direct | webrd04 | t3 | world/intervention_001/oracle | oracle | 29.5 | 59 | 200 | 200 | 0 |
| Step3-VL-10B | direct | webrd04 | t3 | world/sham_001/direct | direct | 43.5 | 87 | 200 | 200 | 0 |
| Step3-VL-10B | direct | webrd04 | t3 | world/sham_001/oracle | oracle | 43.0 | 86 | 200 | 200 | 0 |
| Step3-VL-10B | direct | webrd04 | t4 | base/direct | direct | 27.0 | 108 | 400 | 400 | 0 |
| Step3-VL-10B | direct | webrd04 | t4 | base/oracle | oracle | 35.2 | 141 | 400 | 400 | 0 |
| Step3-VL-10B | direct | webrd04 | t4 | world/intervention_001/direct | direct | 26.5 | 53 | 200 | 200 | 0 |
| Step3-VL-10B | direct | webrd04 | t4 | world/intervention_001/oracle | oracle | 39.0 | 78 | 200 | 200 | 0 |
| Step3-VL-10B | direct | webrd04 | t4 | world/sham_001/direct | direct | 13.5 | 27 | 200 | 200 | 0 |
| Step3-VL-10B | direct | webrd04 | t4 | world/sham_001/oracle | oracle | 25.5 | 51 | 200 | 200 | 0 |
| Step3-VL-10B | direct | wprd01 | t1 | base/direct | direct | 74.5 | 298 | 400 | 400 | 0 |
| Step3-VL-10B | direct | wprd01 | t1 | base/oracle | oracle | 75.5 | 302 | 400 | 400 | 0 |
| Step3-VL-10B | direct | wprd01 | t1 | transform/mirror_h/direct | direct | 54.2 | 217 | 400 | 400 | 0 |
| Step3-VL-10B | direct | wprd01 | t1 | transform/mirror_h/oracle | oracle | 57.2 | 229 | 400 | 400 | 0 |
| Step3-VL-10B | direct | wprd01 | t1 | transform/mirror_h_rot180/direct | direct | 57.8 | 231 | 400 | 400 | 0 |
| Step3-VL-10B | direct | wprd01 | t1 | transform/mirror_h_rot180/oracle | oracle | 58.0 | 232 | 400 | 400 | 0 |
| Step3-VL-10B | direct | wprd01 | t1 | transform/mirror_h_rot270/direct | direct | 60.5 | 242 | 400 | 400 | 0 |
| Step3-VL-10B | direct | wprd01 | t1 | transform/mirror_h_rot270/oracle | oracle | 59.8 | 239 | 400 | 400 | 0 |
| Step3-VL-10B | direct | wprd01 | t1 | transform/mirror_h_rot90/direct | direct | 65.0 | 260 | 400 | 400 | 0 |
| Step3-VL-10B | direct | wprd01 | t1 | transform/mirror_h_rot90/oracle | oracle | 64.2 | 257 | 400 | 400 | 0 |
| Step3-VL-10B | direct | wprd01 | t1 | transform/rot180/direct | direct | 70.8 | 283 | 400 | 400 | 0 |
| Step3-VL-10B | direct | wprd01 | t1 | transform/rot180/oracle | oracle | 71.5 | 286 | 400 | 400 | 0 |
| Step3-VL-10B | direct | wprd01 | t1 | transform/rot270/direct | direct | 70.8 | 283 | 400 | 400 | 0 |
| Step3-VL-10B | direct | wprd01 | t1 | transform/rot270/oracle | oracle | 69.0 | 276 | 400 | 400 | 0 |
| Step3-VL-10B | direct | wprd01 | t1 | transform/rot90/direct | direct | 68.8 | 275 | 400 | 400 | 0 |
| Step3-VL-10B | direct | wprd01 | t1 | transform/rot90/oracle | oracle | 73.0 | 292 | 400 | 400 | 0 |
| Step3-VL-10B | direct | wprd01 | t2 | base/direct | direct | 40.0 | 160 | 400 | 400 | 0 |
| Step3-VL-10B | direct | wprd01 | t2 | base/oracle | oracle | 42.8 | 171 | 400 | 400 | 0 |
| Step3-VL-10B | direct | wprd01 | t2 | transform/mirror_h/direct | direct | 37.5 | 150 | 400 | 400 | 0 |
| Step3-VL-10B | direct | wprd01 | t2 | transform/mirror_h/oracle | oracle | 45.8 | 183 | 400 | 400 | 0 |
| Step3-VL-10B | direct | wprd01 | t2 | transform/mirror_h_rot180/direct | direct | 42.2 | 169 | 400 | 400 | 0 |
| Step3-VL-10B | direct | wprd01 | t2 | transform/mirror_h_rot180/oracle | oracle | 44.8 | 179 | 400 | 400 | 0 |
| Step3-VL-10B | direct | wprd01 | t2 | transform/mirror_h_rot270/direct | direct | 42.0 | 168 | 400 | 400 | 0 |
| Step3-VL-10B | direct | wprd01 | t2 | transform/mirror_h_rot270/oracle | oracle | 45.5 | 182 | 400 | 400 | 0 |
| Step3-VL-10B | direct | wprd01 | t2 | transform/mirror_h_rot90/direct | direct | 41.2 | 165 | 400 | 400 | 0 |
| Step3-VL-10B | direct | wprd01 | t2 | transform/mirror_h_rot90/oracle | oracle | 48.0 | 192 | 400 | 400 | 0 |
| Step3-VL-10B | direct | wprd01 | t2 | transform/rot180/direct | direct | 39.5 | 158 | 400 | 400 | 0 |
| Step3-VL-10B | direct | wprd01 | t2 | transform/rot180/oracle | oracle | 45.2 | 181 | 400 | 400 | 0 |
| Step3-VL-10B | direct | wprd01 | t2 | transform/rot270/direct | direct | 37.2 | 149 | 400 | 400 | 0 |
| Step3-VL-10B | direct | wprd01 | t2 | transform/rot270/oracle | oracle | 46.8 | 187 | 400 | 400 | 0 |
| Step3-VL-10B | direct | wprd01 | t2 | transform/rot90/direct | direct | 37.5 | 150 | 400 | 400 | 0 |
| Step3-VL-10B | direct | wprd01 | t2 | transform/rot90/oracle | oracle | 49.0 | 196 | 400 | 400 | 0 |
| Step3-VL-10B | direct | wprd01 | t3 | base/direct | direct | 45.5 | 91 | 200 | 200 | 0 |
| Step3-VL-10B | direct | wprd01 | t3 | base/oracle | oracle | 50.5 | 101 | 200 | 200 | 0 |
| Step3-VL-10B | direct | wprd01 | t3 | transform/mirror_h/direct | direct | 50.5 | 101 | 200 | 200 | 0 |
| Step3-VL-10B | direct | wprd01 | t3 | transform/mirror_h/oracle | oracle | 45.0 | 90 | 200 | 200 | 0 |
| Step3-VL-10B | direct | wprd01 | t3 | transform/mirror_h_rot180/direct | direct | 45.5 | 91 | 200 | 200 | 0 |
| Step3-VL-10B | direct | wprd01 | t3 | transform/mirror_h_rot180/oracle | oracle | 53.0 | 106 | 200 | 200 | 0 |
| Step3-VL-10B | direct | wprd01 | t3 | transform/mirror_h_rot270/direct | direct | 51.0 | 102 | 200 | 200 | 0 |
| Step3-VL-10B | direct | wprd01 | t3 | transform/mirror_h_rot270/oracle | oracle | 55.0 | 110 | 200 | 200 | 0 |
| Step3-VL-10B | direct | wprd01 | t3 | transform/mirror_h_rot90/direct | direct | 44.5 | 89 | 200 | 200 | 0 |
| Step3-VL-10B | direct | wprd01 | t3 | transform/mirror_h_rot90/oracle | oracle | 48.0 | 96 | 200 | 200 | 0 |
| Step3-VL-10B | direct | wprd01 | t3 | transform/rot180/direct | direct | 39.0 | 78 | 200 | 200 | 0 |
| Step3-VL-10B | direct | wprd01 | t3 | transform/rot180/oracle | oracle | 51.0 | 102 | 200 | 200 | 0 |
| Step3-VL-10B | direct | wprd01 | t3 | transform/rot270/direct | direct | 39.5 | 79 | 200 | 200 | 0 |
| Step3-VL-10B | direct | wprd01 | t3 | transform/rot270/oracle | oracle | 53.5 | 107 | 200 | 200 | 0 |
| Step3-VL-10B | direct | wprd01 | t3 | transform/rot90/direct | direct | 44.5 | 89 | 200 | 200 | 0 |
| Step3-VL-10B | direct | wprd01 | t3 | transform/rot90/oracle | oracle | 52.5 | 105 | 200 | 200 | 0 |
| Step3-VL-10B | direct | wprd01 | t3 | world/intervention_001/direct | direct | 36.0 | 72 | 200 | 200 | 0 |
| Step3-VL-10B | direct | wprd01 | t3 | world/intervention_001/oracle | oracle | 36.0 | 72 | 200 | 200 | 0 |
| Step3-VL-10B | direct | wprd01 | t3 | world/sham_001/direct | direct | 48.0 | 96 | 200 | 200 | 0 |
| Step3-VL-10B | direct | wprd01 | t3 | world/sham_001/oracle | oracle | 49.5 | 99 | 200 | 200 | 0 |
| Step3-VL-10B | direct | wprd01 | t4 | base/direct | direct | 33.8 | 135 | 400 | 400 | 0 |
| Step3-VL-10B | direct | wprd01 | t4 | base/oracle | oracle | 49.0 | 196 | 400 | 400 | 0 |
| Step3-VL-10B | direct | wprd01 | t4 | transform/mirror_h/direct | direct | 34.2 | 137 | 400 | 400 | 0 |
| Step3-VL-10B | direct | wprd01 | t4 | transform/mirror_h/oracle | oracle | 51.0 | 204 | 400 | 400 | 0 |
| Step3-VL-10B | direct | wprd01 | t4 | transform/mirror_h_rot180/direct | direct | 31.8 | 127 | 400 | 400 | 0 |
| Step3-VL-10B | direct | wprd01 | t4 | transform/mirror_h_rot180/oracle | oracle | 48.5 | 194 | 400 | 400 | 0 |
| Step3-VL-10B | direct | wprd01 | t4 | transform/mirror_h_rot270/direct | direct | 37.2 | 149 | 400 | 400 | 0 |
| Step3-VL-10B | direct | wprd01 | t4 | transform/mirror_h_rot270/oracle | oracle | 49.8 | 199 | 400 | 400 | 0 |
| Step3-VL-10B | direct | wprd01 | t4 | transform/mirror_h_rot90/direct | direct | 34.8 | 139 | 400 | 400 | 0 |
| Step3-VL-10B | direct | wprd01 | t4 | transform/mirror_h_rot90/oracle | oracle | 49.2 | 197 | 400 | 400 | 0 |
| Step3-VL-10B | direct | wprd01 | t4 | transform/rot180/direct | direct | 36.2 | 145 | 400 | 400 | 0 |
| Step3-VL-10B | direct | wprd01 | t4 | transform/rot180/oracle | oracle | 49.2 | 197 | 400 | 400 | 0 |
| Step3-VL-10B | direct | wprd01 | t4 | transform/rot270/direct | direct | 33.0 | 132 | 400 | 400 | 0 |
| Step3-VL-10B | direct | wprd01 | t4 | transform/rot270/oracle | oracle | 49.0 | 196 | 400 | 400 | 0 |
| Step3-VL-10B | direct | wprd01 | t4 | transform/rot90/direct | direct | 37.8 | 151 | 400 | 400 | 0 |
| Step3-VL-10B | direct | wprd01 | t4 | transform/rot90/oracle | oracle | 47.8 | 191 | 400 | 400 | 0 |
| Step3-VL-10B | direct | wprd01 | t4 | world/intervention_001/direct | direct | 28.5 | 57 | 200 | 200 | 0 |
| Step3-VL-10B | direct | wprd01 | t4 | world/intervention_001/oracle | oracle | 43.5 | 87 | 200 | 200 | 0 |
| Step3-VL-10B | direct | wprd01 | t4 | world/sham_001/direct | direct | 15.0 | 30 | 200 | 200 | 0 |
| Step3-VL-10B | direct | wprd01 | t4 | world/sham_001/oracle | oracle | 36.0 | 72 | 200 | 200 | 0 |
| Qwen3-VL-8B-Instruct | direct | blank | t1 | base/direct | direct | 61.0 | 244 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | blank | t1 | base/oracle | oracle | 66.2 | 265 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | blank | t1 | transform/mirror_h/direct | direct | 60.5 | 242 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | blank | t1 | transform/mirror_h/oracle | oracle | 62.5 | 250 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | blank | t1 | transform/mirror_h_rot180/direct | direct | 54.5 | 218 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | blank | t1 | transform/mirror_h_rot180/oracle | oracle | 50.8 | 203 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | blank | t1 | transform/mirror_h_rot270/direct | direct | 51.5 | 206 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | blank | t1 | transform/mirror_h_rot270/oracle | oracle | 52.5 | 210 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | blank | t1 | transform/mirror_h_rot90/direct | direct | 50.2 | 201 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | blank | t1 | transform/mirror_h_rot90/oracle | oracle | 56.8 | 227 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | blank | t1 | transform/rot180/direct | direct | 56.8 | 227 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | blank | t1 | transform/rot180/oracle | oracle | 63.8 | 255 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | blank | t1 | transform/rot270/direct | direct | 61.5 | 246 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | blank | t1 | transform/rot270/oracle | oracle | 65.8 | 263 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | blank | t1 | transform/rot90/direct | direct | 58.2 | 233 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | blank | t1 | transform/rot90/oracle | oracle | 62.2 | 249 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | blank | t2 | base/direct | direct | 46.2 | 185 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | blank | t2 | base/oracle | oracle | 54.8 | 219 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | blank | t2 | transform/mirror_h/direct | direct | 47.0 | 188 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | blank | t2 | transform/mirror_h/oracle | oracle | 59.8 | 239 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | blank | t2 | transform/mirror_h_rot180/direct | direct | 44.5 | 178 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | blank | t2 | transform/mirror_h_rot180/oracle | oracle | 52.2 | 209 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | blank | t2 | transform/mirror_h_rot270/direct | direct | 51.5 | 206 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | blank | t2 | transform/mirror_h_rot270/oracle | oracle | 58.2 | 233 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | blank | t2 | transform/mirror_h_rot90/direct | direct | 49.0 | 196 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | blank | t2 | transform/mirror_h_rot90/oracle | oracle | 57.2 | 229 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | blank | t2 | transform/rot180/direct | direct | 47.8 | 191 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | blank | t2 | transform/rot180/oracle | oracle | 62.8 | 251 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | blank | t2 | transform/rot270/direct | direct | 50.2 | 201 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | blank | t2 | transform/rot270/oracle | oracle | 55.0 | 220 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | blank | t2 | transform/rot90/direct | direct | 45.8 | 183 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | blank | t2 | transform/rot90/oracle | oracle | 57.8 | 231 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | sat | t1 | base/direct | direct | 63.0 | 252 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | sat | t1 | base/oracle | oracle | 69.2 | 277 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | sat | t1 | transform/mirror_h/direct | direct | 56.5 | 226 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | sat | t1 | transform/mirror_h/oracle | oracle | 62.8 | 251 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | sat | t1 | transform/mirror_h_rot180/direct | direct | 48.8 | 195 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | sat | t1 | transform/mirror_h_rot180/oracle | oracle | 49.2 | 197 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | sat | t1 | transform/mirror_h_rot270/direct | direct | 49.0 | 196 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | sat | t1 | transform/mirror_h_rot270/oracle | oracle | 51.2 | 205 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | sat | t1 | transform/mirror_h_rot90/direct | direct | 47.0 | 188 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | sat | t1 | transform/mirror_h_rot90/oracle | oracle | 56.5 | 226 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | sat | t1 | transform/rot180/direct | direct | 56.8 | 227 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | sat | t1 | transform/rot180/oracle | oracle | 65.5 | 262 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | sat | t1 | transform/rot270/direct | direct | 59.2 | 237 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | sat | t1 | transform/rot270/oracle | oracle | 68.5 | 274 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | sat | t1 | transform/rot90/direct | direct | 56.2 | 225 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | sat | t1 | transform/rot90/oracle | oracle | 61.5 | 246 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | sat | t2 | base/direct | direct | 43.0 | 172 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | sat | t2 | base/oracle | oracle | 48.5 | 194 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | sat | t2 | transform/mirror_h/direct | direct | 44.5 | 178 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | sat | t2 | transform/mirror_h/oracle | oracle | 53.2 | 213 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | sat | t2 | transform/mirror_h_rot180/direct | direct | 43.8 | 175 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | sat | t2 | transform/mirror_h_rot180/oracle | oracle | 51.0 | 204 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | sat | t2 | transform/mirror_h_rot270/direct | direct | 45.0 | 180 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | sat | t2 | transform/mirror_h_rot270/oracle | oracle | 53.0 | 212 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | sat | t2 | transform/mirror_h_rot90/direct | direct | 44.5 | 178 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | sat | t2 | transform/mirror_h_rot90/oracle | oracle | 49.5 | 198 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | sat | t2 | transform/rot180/direct | direct | 47.2 | 189 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | sat | t2 | transform/rot180/oracle | oracle | 53.5 | 214 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | sat | t2 | transform/rot270/direct | direct | 46.2 | 185 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | sat | t2 | transform/rot270/oracle | oracle | 54.2 | 217 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | sat | t2 | transform/rot90/direct | direct | 45.8 | 183 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | sat | t2 | transform/rot90/oracle | oracle | 53.5 | 214 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | sat | t3 | base/direct | direct | 24.0 | 48 | 200 | 200 | 0 |
| Qwen3-VL-8B-Instruct | direct | sat | t3 | base/oracle | oracle | 26.0 | 52 | 200 | 200 | 0 |
| Qwen3-VL-8B-Instruct | direct | sat | t3 | transform/mirror_h/direct | direct | 24.0 | 48 | 200 | 200 | 0 |
| Qwen3-VL-8B-Instruct | direct | sat | t3 | transform/mirror_h/oracle | oracle | 24.0 | 48 | 200 | 200 | 0 |
| Qwen3-VL-8B-Instruct | direct | sat | t3 | transform/mirror_h_rot180/direct | direct | 24.5 | 49 | 200 | 200 | 0 |
| Qwen3-VL-8B-Instruct | direct | sat | t3 | transform/mirror_h_rot180/oracle | oracle | 26.0 | 52 | 200 | 200 | 0 |
| Qwen3-VL-8B-Instruct | direct | sat | t3 | transform/mirror_h_rot270/direct | direct | 25.0 | 50 | 200 | 200 | 0 |
| Qwen3-VL-8B-Instruct | direct | sat | t3 | transform/mirror_h_rot270/oracle | oracle | 26.0 | 52 | 200 | 200 | 0 |
| Qwen3-VL-8B-Instruct | direct | sat | t3 | transform/mirror_h_rot90/direct | direct | 24.5 | 49 | 200 | 200 | 0 |
| Qwen3-VL-8B-Instruct | direct | sat | t3 | transform/mirror_h_rot90/oracle | oracle | 24.0 | 48 | 200 | 200 | 0 |
| Qwen3-VL-8B-Instruct | direct | sat | t3 | transform/rot180/direct | direct | 25.0 | 50 | 200 | 200 | 0 |
| Qwen3-VL-8B-Instruct | direct | sat | t3 | transform/rot180/oracle | oracle | 24.5 | 49 | 200 | 200 | 0 |
| Qwen3-VL-8B-Instruct | direct | sat | t3 | transform/rot270/direct | direct | 25.0 | 50 | 200 | 200 | 0 |
| Qwen3-VL-8B-Instruct | direct | sat | t3 | transform/rot270/oracle | oracle | 25.5 | 51 | 200 | 200 | 0 |
| Qwen3-VL-8B-Instruct | direct | sat | t3 | transform/rot90/direct | direct | 24.5 | 49 | 200 | 200 | 0 |
| Qwen3-VL-8B-Instruct | direct | sat | t3 | transform/rot90/oracle | oracle | 26.5 | 53 | 200 | 200 | 0 |
| Qwen3-VL-8B-Instruct | direct | sat | t3 | world/intervention_001/direct | direct | 40.5 | 81 | 200 | 200 | 0 |
| Qwen3-VL-8B-Instruct | direct | sat | t3 | world/intervention_001/oracle | oracle | 39.5 | 79 | 200 | 200 | 0 |
| Qwen3-VL-8B-Instruct | direct | sat | t3 | world/sham_001/direct | direct | 25.0 | 50 | 200 | 200 | 0 |
| Qwen3-VL-8B-Instruct | direct | sat | t3 | world/sham_001/oracle | oracle | 27.0 | 54 | 200 | 200 | 0 |
| Qwen3-VL-8B-Instruct | direct | sat | t4 | base/direct | direct | 53.0 | 212 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | sat | t4 | base/oracle | oracle | 60.0 | 240 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | sat | t4 | transform/mirror_h/direct | direct | 51.5 | 206 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | sat | t4 | transform/mirror_h/oracle | oracle | 62.0 | 248 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | sat | t4 | transform/mirror_h_rot180/direct | direct | 51.2 | 205 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | sat | t4 | transform/mirror_h_rot180/oracle | oracle | 61.2 | 245 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | sat | t4 | transform/mirror_h_rot270/direct | direct | 54.2 | 217 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | sat | t4 | transform/mirror_h_rot270/oracle | oracle | 65.2 | 261 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | sat | t4 | transform/mirror_h_rot90/direct | direct | 49.5 | 198 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | sat | t4 | transform/mirror_h_rot90/oracle | oracle | 59.0 | 236 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | sat | t4 | transform/rot180/direct | direct | 51.2 | 205 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | sat | t4 | transform/rot180/oracle | oracle | 64.5 | 258 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | sat | t4 | transform/rot270/direct | direct | 54.2 | 217 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | sat | t4 | transform/rot270/oracle | oracle | 64.5 | 258 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | sat | t4 | transform/rot90/direct | direct | 50.8 | 203 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | sat | t4 | transform/rot90/oracle | oracle | 61.5 | 246 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | sat | t4 | world/intervention_001/direct | direct | 14.5 | 29 | 200 | 200 | 0 |
| Qwen3-VL-8B-Instruct | direct | sat | t4 | world/intervention_001/oracle | oracle | 43.0 | 86 | 200 | 200 | 0 |
| Qwen3-VL-8B-Instruct | direct | sat | t4 | world/sham_001/direct | direct | 41.0 | 82 | 200 | 200 | 0 |
| Qwen3-VL-8B-Instruct | direct | sat | t4 | world/sham_001/oracle | oracle | 56.0 | 112 | 200 | 200 | 0 |
| Qwen3-VL-8B-Instruct | direct | webrd04 | t1 | base/direct | direct | 59.2 | 237 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | webrd04 | t1 | base/oracle | oracle | 67.2 | 269 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | webrd04 | t2 | base/direct | direct | 48.0 | 192 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | webrd04 | t2 | base/oracle | oracle | 50.5 | 202 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | webrd04 | t3 | base/direct | direct | 26.0 | 52 | 200 | 200 | 0 |
| Qwen3-VL-8B-Instruct | direct | webrd04 | t3 | base/oracle | oracle | 27.0 | 54 | 200 | 200 | 0 |
| Qwen3-VL-8B-Instruct | direct | webrd04 | t3 | world/intervention_001/direct | direct | 45.5 | 91 | 200 | 200 | 0 |
| Qwen3-VL-8B-Instruct | direct | webrd04 | t3 | world/intervention_001/oracle | oracle | 42.5 | 85 | 200 | 200 | 0 |
| Qwen3-VL-8B-Instruct | direct | webrd04 | t3 | world/sham_001/direct | direct | 26.0 | 52 | 200 | 200 | 0 |
| Qwen3-VL-8B-Instruct | direct | webrd04 | t3 | world/sham_001/oracle | oracle | 27.0 | 54 | 200 | 200 | 0 |
| Qwen3-VL-8B-Instruct | direct | webrd04 | t4 | base/direct | direct | 46.5 | 186 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | webrd04 | t4 | base/oracle | oracle | 55.5 | 222 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | webrd04 | t4 | world/intervention_001/direct | direct | 16.0 | 32 | 200 | 200 | 0 |
| Qwen3-VL-8B-Instruct | direct | webrd04 | t4 | world/intervention_001/oracle | oracle | 32.5 | 65 | 200 | 200 | 0 |
| Qwen3-VL-8B-Instruct | direct | webrd04 | t4 | world/sham_001/direct | direct | 42.5 | 85 | 200 | 200 | 0 |
| Qwen3-VL-8B-Instruct | direct | webrd04 | t4 | world/sham_001/oracle | oracle | 54.5 | 109 | 200 | 200 | 0 |
| Qwen3-VL-8B-Instruct | direct | wprd01 | t1 | base/direct | direct | 59.0 | 236 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | wprd01 | t1 | base/oracle | oracle | 69.8 | 279 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | wprd01 | t1 | transform/mirror_h/direct | direct | 56.0 | 224 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | wprd01 | t1 | transform/mirror_h/oracle | oracle | 60.2 | 241 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | wprd01 | t1 | transform/mirror_h_rot180/direct | direct | 47.0 | 188 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | wprd01 | t1 | transform/mirror_h_rot180/oracle | oracle | 49.8 | 199 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | wprd01 | t1 | transform/mirror_h_rot270/direct | direct | 46.2 | 185 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | wprd01 | t1 | transform/mirror_h_rot270/oracle | oracle | 51.8 | 207 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | wprd01 | t1 | transform/mirror_h_rot90/direct | direct | 48.8 | 195 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | wprd01 | t1 | transform/mirror_h_rot90/oracle | oracle | 54.8 | 219 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | wprd01 | t1 | transform/rot180/direct | direct | 57.0 | 228 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | wprd01 | t1 | transform/rot180/oracle | oracle | 64.2 | 257 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | wprd01 | t1 | transform/rot270/direct | direct | 58.2 | 233 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | wprd01 | t1 | transform/rot270/oracle | oracle | 66.0 | 264 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | wprd01 | t1 | transform/rot90/direct | direct | 59.8 | 239 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | wprd01 | t1 | transform/rot90/oracle | oracle | 68.2 | 273 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | wprd01 | t2 | base/direct | direct | 40.0 | 160 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | wprd01 | t2 | base/oracle | oracle | 47.2 | 189 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | wprd01 | t2 | transform/mirror_h/direct | direct | 39.8 | 159 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | wprd01 | t2 | transform/mirror_h/oracle | oracle | 48.2 | 193 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | wprd01 | t2 | transform/mirror_h_rot180/direct | direct | 41.0 | 164 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | wprd01 | t2 | transform/mirror_h_rot180/oracle | oracle | 44.2 | 177 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | wprd01 | t2 | transform/mirror_h_rot270/direct | direct | 40.2 | 161 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | wprd01 | t2 | transform/mirror_h_rot270/oracle | oracle | 49.8 | 199 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | wprd01 | t2 | transform/mirror_h_rot90/direct | direct | 40.5 | 162 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | wprd01 | t2 | transform/mirror_h_rot90/oracle | oracle | 50.8 | 203 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | wprd01 | t2 | transform/rot180/direct | direct | 40.0 | 160 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | wprd01 | t2 | transform/rot180/oracle | oracle | 50.8 | 203 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | wprd01 | t2 | transform/rot270/direct | direct | 37.8 | 151 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | wprd01 | t2 | transform/rot270/oracle | oracle | 48.5 | 194 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | wprd01 | t2 | transform/rot90/direct | direct | 41.5 | 166 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | wprd01 | t2 | transform/rot90/oracle | oracle | 48.8 | 195 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | wprd01 | t3 | base/direct | direct | 25.0 | 50 | 200 | 200 | 0 |
| Qwen3-VL-8B-Instruct | direct | wprd01 | t3 | base/oracle | oracle | 26.0 | 52 | 200 | 200 | 0 |
| Qwen3-VL-8B-Instruct | direct | wprd01 | t3 | transform/mirror_h/direct | direct | 24.5 | 49 | 200 | 200 | 0 |
| Qwen3-VL-8B-Instruct | direct | wprd01 | t3 | transform/mirror_h/oracle | oracle | 25.0 | 50 | 200 | 200 | 0 |
| Qwen3-VL-8B-Instruct | direct | wprd01 | t3 | transform/mirror_h_rot180/direct | direct | 25.5 | 51 | 200 | 200 | 0 |
| Qwen3-VL-8B-Instruct | direct | wprd01 | t3 | transform/mirror_h_rot180/oracle | oracle | 26.0 | 52 | 200 | 200 | 0 |
| Qwen3-VL-8B-Instruct | direct | wprd01 | t3 | transform/mirror_h_rot270/direct | direct | 26.0 | 52 | 200 | 200 | 0 |
| Qwen3-VL-8B-Instruct | direct | wprd01 | t3 | transform/mirror_h_rot270/oracle | oracle | 25.5 | 51 | 200 | 200 | 0 |
| Qwen3-VL-8B-Instruct | direct | wprd01 | t3 | transform/mirror_h_rot90/direct | direct | 24.5 | 49 | 200 | 200 | 0 |
| Qwen3-VL-8B-Instruct | direct | wprd01 | t3 | transform/mirror_h_rot90/oracle | oracle | 26.5 | 53 | 200 | 200 | 0 |
| Qwen3-VL-8B-Instruct | direct | wprd01 | t3 | transform/rot180/direct | direct | 25.0 | 50 | 200 | 200 | 0 |
| Qwen3-VL-8B-Instruct | direct | wprd01 | t3 | transform/rot180/oracle | oracle | 25.0 | 50 | 200 | 200 | 0 |
| Qwen3-VL-8B-Instruct | direct | wprd01 | t3 | transform/rot270/direct | direct | 26.0 | 52 | 200 | 200 | 0 |
| Qwen3-VL-8B-Instruct | direct | wprd01 | t3 | transform/rot270/oracle | oracle | 25.5 | 51 | 200 | 200 | 0 |
| Qwen3-VL-8B-Instruct | direct | wprd01 | t3 | transform/rot90/direct | direct | 25.0 | 50 | 200 | 200 | 0 |
| Qwen3-VL-8B-Instruct | direct | wprd01 | t3 | transform/rot90/oracle | oracle | 25.0 | 50 | 200 | 200 | 0 |
| Qwen3-VL-8B-Instruct | direct | wprd01 | t3 | world/intervention_001/direct | direct | 45.0 | 90 | 200 | 200 | 0 |
| Qwen3-VL-8B-Instruct | direct | wprd01 | t3 | world/intervention_001/oracle | oracle | 45.5 | 91 | 200 | 200 | 0 |
| Qwen3-VL-8B-Instruct | direct | wprd01 | t3 | world/sham_001/direct | direct | 26.0 | 52 | 200 | 200 | 0 |
| Qwen3-VL-8B-Instruct | direct | wprd01 | t3 | world/sham_001/oracle | oracle | 26.0 | 52 | 200 | 200 | 0 |
| Qwen3-VL-8B-Instruct | direct | wprd01 | t4 | base/direct | direct | 54.5 | 218 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | wprd01 | t4 | base/oracle | oracle | 62.0 | 248 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | wprd01 | t4 | transform/mirror_h/direct | direct | 56.8 | 227 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | wprd01 | t4 | transform/mirror_h/oracle | oracle | 63.8 | 255 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | wprd01 | t4 | transform/mirror_h_rot180/direct | direct | 56.0 | 224 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | wprd01 | t4 | transform/mirror_h_rot180/oracle | oracle | 63.2 | 253 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | wprd01 | t4 | transform/mirror_h_rot270/direct | direct | 58.2 | 233 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | wprd01 | t4 | transform/mirror_h_rot270/oracle | oracle | 64.5 | 258 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | wprd01 | t4 | transform/mirror_h_rot90/direct | direct | 55.2 | 221 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | wprd01 | t4 | transform/mirror_h_rot90/oracle | oracle | 63.0 | 252 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | wprd01 | t4 | transform/rot180/direct | direct | 60.0 | 240 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | wprd01 | t4 | transform/rot180/oracle | oracle | 66.5 | 266 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | wprd01 | t4 | transform/rot270/direct | direct | 59.8 | 239 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | wprd01 | t4 | transform/rot270/oracle | oracle | 67.8 | 271 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | wprd01 | t4 | transform/rot90/direct | direct | 54.2 | 217 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | wprd01 | t4 | transform/rot90/oracle | oracle | 63.0 | 252 | 400 | 400 | 0 |
| Qwen3-VL-8B-Instruct | direct | wprd01 | t4 | world/intervention_001/direct | direct | 14.5 | 29 | 200 | 200 | 0 |
| Qwen3-VL-8B-Instruct | direct | wprd01 | t4 | world/intervention_001/oracle | oracle | 35.5 | 71 | 200 | 200 | 0 |
| Qwen3-VL-8B-Instruct | direct | wprd01 | t4 | world/sham_001/direct | direct | 43.5 | 87 | 200 | 200 | 0 |
| Qwen3-VL-8B-Instruct | direct | wprd01 | t4 | world/sham_001/oracle | oracle | 58.5 | 117 | 200 | 200 | 0 |
| ViLaSR | direct | blank | t1 | base/direct | direct | 64.0 | 256 | 400 | 400 | 0 |
| ViLaSR | direct | blank | t1 | base/oracle | oracle | 65.8 | 263 | 400 | 400 | 0 |
| ViLaSR | direct | blank | t1 | transform/mirror_h/direct | direct | 56.8 | 227 | 400 | 400 | 0 |
| ViLaSR | direct | blank | t1 | transform/mirror_h/oracle | oracle | 62.0 | 248 | 400 | 400 | 0 |
| ViLaSR | direct | blank | t1 | transform/mirror_h_rot180/direct | direct | 53.0 | 212 | 400 | 400 | 0 |
| ViLaSR | direct | blank | t1 | transform/mirror_h_rot180/oracle | oracle | 60.8 | 243 | 400 | 400 | 0 |
| ViLaSR | direct | blank | t1 | transform/mirror_h_rot270/direct | direct | 53.2 | 213 | 400 | 400 | 0 |
| ViLaSR | direct | blank | t1 | transform/mirror_h_rot270/oracle | oracle | 54.2 | 217 | 400 | 400 | 0 |
| ViLaSR | direct | blank | t1 | transform/mirror_h_rot90/direct | direct | 50.0 | 200 | 400 | 400 | 0 |
| ViLaSR | direct | blank | t1 | transform/mirror_h_rot90/oracle | oracle | 57.5 | 230 | 400 | 400 | 0 |
| ViLaSR | direct | blank | t1 | transform/rot180/direct | direct | 60.8 | 243 | 400 | 400 | 0 |
| ViLaSR | direct | blank | t1 | transform/rot180/oracle | oracle | 64.8 | 259 | 400 | 400 | 0 |
| ViLaSR | direct | blank | t1 | transform/rot270/direct | direct | 70.2 | 281 | 400 | 400 | 0 |
| ViLaSR | direct | blank | t1 | transform/rot270/oracle | oracle | 69.2 | 277 | 400 | 400 | 0 |
| ViLaSR | direct | blank | t1 | transform/rot90/direct | direct | 63.5 | 254 | 400 | 400 | 0 |
| ViLaSR | direct | blank | t1 | transform/rot90/oracle | oracle | 66.5 | 266 | 400 | 400 | 0 |
| ViLaSR | direct | blank | t2 | base/direct | direct | 61.0 | 244 | 400 | 400 | 0 |
| ViLaSR | direct | blank | t2 | base/oracle | oracle | 57.8 | 231 | 400 | 400 | 0 |
| ViLaSR | direct | blank | t2 | transform/mirror_h/direct | direct | 59.2 | 237 | 400 | 400 | 0 |
| ViLaSR | direct | blank | t2 | transform/mirror_h/oracle | oracle | 55.0 | 220 | 400 | 400 | 0 |
| ViLaSR | direct | blank | t2 | transform/mirror_h_rot180/direct | direct | 60.5 | 242 | 400 | 400 | 0 |
| ViLaSR | direct | blank | t2 | transform/mirror_h_rot180/oracle | oracle | 55.8 | 223 | 400 | 400 | 0 |
| ViLaSR | direct | blank | t2 | transform/mirror_h_rot270/direct | direct | 58.8 | 235 | 400 | 400 | 0 |
| ViLaSR | direct | blank | t2 | transform/mirror_h_rot270/oracle | oracle | 57.5 | 230 | 400 | 400 | 0 |
| ViLaSR | direct | blank | t2 | transform/mirror_h_rot90/direct | direct | 61.8 | 247 | 400 | 400 | 0 |
| ViLaSR | direct | blank | t2 | transform/mirror_h_rot90/oracle | oracle | 53.5 | 214 | 400 | 400 | 0 |
| ViLaSR | direct | blank | t2 | transform/rot180/direct | direct | 62.5 | 250 | 400 | 400 | 0 |
| ViLaSR | direct | blank | t2 | transform/rot180/oracle | oracle | 58.2 | 233 | 400 | 400 | 0 |
| ViLaSR | direct | blank | t2 | transform/rot270/direct | direct | 58.0 | 232 | 400 | 400 | 0 |
| ViLaSR | direct | blank | t2 | transform/rot270/oracle | oracle | 53.0 | 212 | 400 | 400 | 0 |
| ViLaSR | direct | blank | t2 | transform/rot90/direct | direct | 61.8 | 247 | 400 | 400 | 0 |
| ViLaSR | direct | blank | t2 | transform/rot90/oracle | oracle | 58.0 | 232 | 400 | 400 | 0 |
| ViLaSR | direct | sat | t1 | base/direct | direct | 56.5 | 226 | 400 | 400 | 0 |
| ViLaSR | direct | sat | t1 | base/oracle | oracle | 64.8 | 259 | 400 | 400 | 0 |
| ViLaSR | direct | sat | t1 | transform/mirror_h/direct | direct | 46.5 | 186 | 400 | 400 | 0 |
| ViLaSR | direct | sat | t1 | transform/mirror_h/oracle | oracle | 57.5 | 230 | 400 | 400 | 0 |
| ViLaSR | direct | sat | t1 | transform/mirror_h_rot180/direct | direct | 43.5 | 174 | 400 | 400 | 0 |
| ViLaSR | direct | sat | t1 | transform/mirror_h_rot180/oracle | oracle | 48.5 | 194 | 400 | 400 | 0 |
| ViLaSR | direct | sat | t1 | transform/mirror_h_rot270/direct | direct | 38.2 | 153 | 400 | 400 | 0 |
| ViLaSR | direct | sat | t1 | transform/mirror_h_rot270/oracle | oracle | 47.8 | 191 | 400 | 400 | 0 |
| ViLaSR | direct | sat | t1 | transform/mirror_h_rot90/direct | direct | 45.8 | 183 | 400 | 400 | 0 |
| ViLaSR | direct | sat | t1 | transform/mirror_h_rot90/oracle | oracle | 52.8 | 211 | 400 | 400 | 0 |
| ViLaSR | direct | sat | t1 | transform/rot180/direct | direct | 53.5 | 214 | 400 | 400 | 0 |
| ViLaSR | direct | sat | t1 | transform/rot180/oracle | oracle | 60.5 | 242 | 400 | 400 | 0 |
| ViLaSR | direct | sat | t1 | transform/rot270/direct | direct | 63.2 | 253 | 400 | 400 | 0 |
| ViLaSR | direct | sat | t1 | transform/rot270/oracle | oracle | 66.5 | 266 | 400 | 400 | 0 |
| ViLaSR | direct | sat | t1 | transform/rot90/direct | direct | 55.5 | 222 | 400 | 400 | 0 |
| ViLaSR | direct | sat | t1 | transform/rot90/oracle | oracle | 59.2 | 237 | 400 | 400 | 0 |
| ViLaSR | direct | sat | t2 | base/direct | direct | 57.8 | 231 | 400 | 400 | 0 |
| ViLaSR | direct | sat | t2 | base/oracle | oracle | 55.8 | 223 | 400 | 400 | 0 |
| ViLaSR | direct | sat | t2 | transform/mirror_h/direct | direct | 56.5 | 226 | 400 | 400 | 0 |
| ViLaSR | direct | sat | t2 | transform/mirror_h/oracle | oracle | 54.0 | 216 | 400 | 400 | 0 |
| ViLaSR | direct | sat | t2 | transform/mirror_h_rot180/direct | direct | 57.0 | 228 | 400 | 400 | 0 |
| ViLaSR | direct | sat | t2 | transform/mirror_h_rot180/oracle | oracle | 56.0 | 224 | 400 | 400 | 0 |
| ViLaSR | direct | sat | t2 | transform/mirror_h_rot270/direct | direct | 57.2 | 229 | 400 | 400 | 0 |
| ViLaSR | direct | sat | t2 | transform/mirror_h_rot270/oracle | oracle | 58.0 | 232 | 400 | 400 | 0 |
| ViLaSR | direct | sat | t2 | transform/mirror_h_rot90/direct | direct | 57.5 | 230 | 400 | 400 | 0 |
| ViLaSR | direct | sat | t2 | transform/mirror_h_rot90/oracle | oracle | 56.8 | 227 | 400 | 400 | 0 |
| ViLaSR | direct | sat | t2 | transform/rot180/direct | direct | 56.5 | 226 | 400 | 400 | 0 |
| ViLaSR | direct | sat | t2 | transform/rot180/oracle | oracle | 59.0 | 236 | 400 | 400 | 0 |
| ViLaSR | direct | sat | t2 | transform/rot270/direct | direct | 55.8 | 223 | 400 | 400 | 0 |
| ViLaSR | direct | sat | t2 | transform/rot270/oracle | oracle | 56.0 | 224 | 400 | 400 | 0 |
| ViLaSR | direct | sat | t2 | transform/rot90/direct | direct | 59.8 | 239 | 400 | 400 | 0 |
| ViLaSR | direct | sat | t2 | transform/rot90/oracle | oracle | 59.8 | 239 | 400 | 400 | 0 |
| ViLaSR | direct | sat | t3 | base/direct | direct | 39.5 | 79 | 200 | 200 | 0 |
| ViLaSR | direct | sat | t3 | base/oracle | oracle | 37.5 | 75 | 200 | 200 | 0 |
| ViLaSR | direct | sat | t3 | transform/mirror_h/direct | direct | 35.0 | 70 | 200 | 200 | 0 |
| ViLaSR | direct | sat | t3 | transform/mirror_h/oracle | oracle | 35.5 | 71 | 200 | 200 | 0 |
| ViLaSR | direct | sat | t3 | transform/mirror_h_rot180/direct | direct | 38.5 | 77 | 200 | 200 | 0 |
| ViLaSR | direct | sat | t3 | transform/mirror_h_rot180/oracle | oracle | 38.5 | 77 | 200 | 200 | 0 |
| ViLaSR | direct | sat | t3 | transform/mirror_h_rot270/direct | direct | 37.0 | 74 | 200 | 200 | 0 |
| ViLaSR | direct | sat | t3 | transform/mirror_h_rot270/oracle | oracle | 41.0 | 82 | 200 | 200 | 0 |
| ViLaSR | direct | sat | t3 | transform/mirror_h_rot90/direct | direct | 34.0 | 68 | 200 | 200 | 0 |
| ViLaSR | direct | sat | t3 | transform/mirror_h_rot90/oracle | oracle | 35.5 | 71 | 200 | 200 | 0 |
| ViLaSR | direct | sat | t3 | transform/rot180/direct | direct | 36.0 | 72 | 200 | 200 | 0 |
| ViLaSR | direct | sat | t3 | transform/rot180/oracle | oracle | 41.5 | 83 | 200 | 200 | 0 |
| ViLaSR | direct | sat | t3 | transform/rot270/direct | direct | 37.5 | 75 | 200 | 200 | 0 |
| ViLaSR | direct | sat | t3 | transform/rot270/oracle | oracle | 39.0 | 78 | 200 | 200 | 0 |
| ViLaSR | direct | sat | t3 | transform/rot90/direct | direct | 39.0 | 78 | 200 | 200 | 0 |
| ViLaSR | direct | sat | t3 | transform/rot90/oracle | oracle | 35.0 | 70 | 200 | 200 | 0 |
| ViLaSR | direct | sat | t3 | world/intervention_001/direct | direct | 33.5 | 67 | 200 | 200 | 0 |
| ViLaSR | direct | sat | t3 | world/intervention_001/oracle | oracle | 31.0 | 62 | 200 | 200 | 0 |
| ViLaSR | direct | sat | t3 | world/sham_001/direct | direct | 39.0 | 78 | 200 | 200 | 0 |
| ViLaSR | direct | sat | t3 | world/sham_001/oracle | oracle | 39.5 | 79 | 200 | 200 | 0 |
| ViLaSR | direct | sat | t4 | base/direct | direct | 33.0 | 132 | 400 | 400 | 0 |
| ViLaSR | direct | sat | t4 | base/oracle | oracle | 36.0 | 144 | 400 | 400 | 0 |
| ViLaSR | direct | sat | t4 | transform/mirror_h/direct | direct | 31.2 | 125 | 400 | 400 | 0 |
| ViLaSR | direct | sat | t4 | transform/mirror_h/oracle | oracle | 34.0 | 136 | 400 | 400 | 0 |
| ViLaSR | direct | sat | t4 | transform/mirror_h_rot180/direct | direct | 33.2 | 133 | 400 | 400 | 0 |
| ViLaSR | direct | sat | t4 | transform/mirror_h_rot180/oracle | oracle | 35.8 | 143 | 400 | 400 | 0 |
| ViLaSR | direct | sat | t4 | transform/mirror_h_rot270/direct | direct | 31.8 | 127 | 400 | 400 | 0 |
| ViLaSR | direct | sat | t4 | transform/mirror_h_rot270/oracle | oracle | 33.2 | 133 | 400 | 400 | 0 |
| ViLaSR | direct | sat | t4 | transform/mirror_h_rot90/direct | direct | 31.0 | 124 | 400 | 400 | 0 |
| ViLaSR | direct | sat | t4 | transform/mirror_h_rot90/oracle | oracle | 34.2 | 137 | 400 | 400 | 0 |
| ViLaSR | direct | sat | t4 | transform/rot180/direct | direct | 26.5 | 106 | 400 | 400 | 0 |
| ViLaSR | direct | sat | t4 | transform/rot180/oracle | oracle | 37.2 | 149 | 400 | 400 | 0 |
| ViLaSR | direct | sat | t4 | transform/rot270/direct | direct | 31.8 | 127 | 400 | 400 | 0 |
| ViLaSR | direct | sat | t4 | transform/rot270/oracle | oracle | 30.5 | 122 | 400 | 400 | 0 |
| ViLaSR | direct | sat | t4 | transform/rot90/direct | direct | 33.0 | 132 | 400 | 400 | 0 |
| ViLaSR | direct | sat | t4 | transform/rot90/oracle | oracle | 32.0 | 128 | 400 | 400 | 0 |
| ViLaSR | direct | sat | t4 | world/intervention_001/direct | direct | 21.5 | 43 | 200 | 200 | 0 |
| ViLaSR | direct | sat | t4 | world/intervention_001/oracle | oracle | 26.5 | 53 | 200 | 200 | 0 |
| ViLaSR | direct | sat | t4 | world/sham_001/direct | direct | 27.5 | 55 | 200 | 200 | 0 |
| ViLaSR | direct | sat | t4 | world/sham_001/oracle | oracle | 28.0 | 56 | 200 | 200 | 0 |
| ViLaSR | direct | webrd04 | t2 | base/oracle | oracle | 53.5 | 214 | 400 | 400 | 0 |
| ViLaSR | direct | webrd04 | t4 | base/direct | direct | 31.0 | 124 | 400 | 400 | 0 |
| ViLaSR | direct | webrd04 | t4 | base/oracle | oracle | 31.0 | 124 | 400 | 400 | 0 |
| ViLaSR | direct | webrd04 | t4 | world/intervention_001/direct | direct | 28.5 | 57 | 200 | 200 | 0 |
| ViLaSR | direct | webrd04 | t4 | world/intervention_001/oracle | oracle | 24.0 | 48 | 200 | 200 | 0 |
| ViLaSR | direct | webrd04 | t4 | world/sham_001/direct | direct | 25.0 | 50 | 200 | 200 | 0 |
| ViLaSR | direct | webrd04 | t4 | world/sham_001/oracle | oracle | 26.0 | 52 | 200 | 200 | 0 |
| ViLaSR | direct | wprd01 | t1 | base/direct | direct | 60.0 | 240 | 400 | 400 | 0 |
| ViLaSR | direct | wprd01 | t1 | base/oracle | oracle | 66.8 | 267 | 400 | 400 | 0 |
| ViLaSR | direct | wprd01 | t1 | transform/mirror_h/direct | direct | 43.2 | 173 | 400 | 400 | 0 |
| ViLaSR | direct | wprd01 | t1 | transform/mirror_h/oracle | oracle | 54.2 | 217 | 400 | 400 | 0 |
| ViLaSR | direct | wprd01 | t1 | transform/mirror_h_rot180/direct | direct | 40.0 | 160 | 400 | 400 | 0 |
| ViLaSR | direct | wprd01 | t1 | transform/mirror_h_rot180/oracle | oracle | 51.0 | 204 | 400 | 400 | 0 |
| ViLaSR | direct | wprd01 | t1 | transform/mirror_h_rot270/direct | direct | 41.2 | 165 | 400 | 400 | 0 |
| ViLaSR | direct | wprd01 | t1 | transform/mirror_h_rot270/oracle | oracle | 47.8 | 191 | 400 | 400 | 0 |
| ViLaSR | direct | wprd01 | t1 | transform/mirror_h_rot90/direct | direct | 43.2 | 173 | 400 | 400 | 0 |
| ViLaSR | direct | wprd01 | t1 | transform/mirror_h_rot90/oracle | oracle | 54.2 | 217 | 400 | 400 | 0 |
| ViLaSR | direct | wprd01 | t1 | transform/rot180/direct | direct | 52.0 | 208 | 400 | 400 | 0 |
| ViLaSR | direct | wprd01 | t1 | transform/rot180/oracle | oracle | 58.8 | 235 | 400 | 400 | 0 |
| ViLaSR | direct | wprd01 | t1 | transform/rot270/direct | direct | 59.5 | 238 | 400 | 400 | 0 |
| ViLaSR | direct | wprd01 | t1 | transform/rot270/oracle | oracle | 65.2 | 261 | 400 | 400 | 0 |
| ViLaSR | direct | wprd01 | t1 | transform/rot90/direct | direct | 60.0 | 240 | 400 | 400 | 0 |
| ViLaSR | direct | wprd01 | t1 | transform/rot90/oracle | oracle | 63.8 | 255 | 400 | 400 | 0 |
| ViLaSR | direct | wprd01 | t2 | base/direct | direct | 54.0 | 216 | 400 | 400 | 0 |
| ViLaSR | direct | wprd01 | t2 | base/oracle | oracle | 55.0 | 220 | 400 | 400 | 0 |
| ViLaSR | direct | wprd01 | t2 | transform/mirror_h/direct | direct | 55.2 | 221 | 400 | 400 | 0 |
| ViLaSR | direct | wprd01 | t2 | transform/mirror_h/oracle | oracle | 56.2 | 225 | 400 | 400 | 0 |
| ViLaSR | direct | wprd01 | t2 | transform/mirror_h_rot180/direct | direct | 54.0 | 216 | 400 | 400 | 0 |
| ViLaSR | direct | wprd01 | t2 | transform/mirror_h_rot180/oracle | oracle | 54.0 | 216 | 400 | 400 | 0 |
| ViLaSR | direct | wprd01 | t2 | transform/mirror_h_rot270/direct | direct | 54.8 | 219 | 400 | 400 | 0 |
| ViLaSR | direct | wprd01 | t2 | transform/mirror_h_rot270/oracle | oracle | 55.5 | 222 | 400 | 400 | 0 |
| ViLaSR | direct | wprd01 | t2 | transform/mirror_h_rot90/direct | direct | 54.0 | 216 | 400 | 400 | 0 |
| ViLaSR | direct | wprd01 | t2 | transform/mirror_h_rot90/oracle | oracle | 53.8 | 215 | 400 | 400 | 0 |
| ViLaSR | direct | wprd01 | t2 | transform/rot180/direct | direct | 55.2 | 221 | 400 | 400 | 0 |
| ViLaSR | direct | wprd01 | t2 | transform/rot180/oracle | oracle | 56.2 | 225 | 400 | 400 | 0 |
| ViLaSR | direct | wprd01 | t2 | transform/rot270/direct | direct | 52.0 | 208 | 400 | 400 | 0 |
| ViLaSR | direct | wprd01 | t2 | transform/rot270/oracle | oracle | 54.8 | 219 | 400 | 400 | 0 |
| ViLaSR | direct | wprd01 | t2 | transform/rot90/direct | direct | 57.5 | 230 | 400 | 400 | 0 |
| ViLaSR | direct | wprd01 | t2 | transform/rot90/oracle | oracle | 57.0 | 228 | 400 | 400 | 0 |
| ViLaSR | direct | wprd01 | t4 | base/direct | direct | 30.5 | 122 | 400 | 400 | 0 |
| ViLaSR | direct | wprd01 | t4 | base/oracle | oracle | 29.0 | 116 | 400 | 400 | 0 |
| ViLaSR | direct | wprd01 | t4 | transform/mirror_h/direct | direct | 32.8 | 131 | 400 | 400 | 0 |
| ViLaSR | direct | wprd01 | t4 | transform/mirror_h/oracle | oracle | 31.8 | 127 | 400 | 400 | 0 |
| ViLaSR | direct | wprd01 | t4 | transform/mirror_h_rot180/direct | direct | 32.0 | 128 | 400 | 400 | 0 |
| ViLaSR | direct | wprd01 | t4 | transform/mirror_h_rot180/oracle | oracle | 35.0 | 140 | 400 | 400 | 0 |
| ViLaSR | direct | wprd01 | t4 | transform/mirror_h_rot270/direct | direct | 33.8 | 135 | 400 | 400 | 0 |
| ViLaSR | direct | wprd01 | t4 | transform/mirror_h_rot270/oracle | oracle | 33.2 | 133 | 400 | 400 | 0 |
| ViLaSR | direct | wprd01 | t4 | transform/mirror_h_rot90/direct | direct | 27.2 | 109 | 400 | 400 | 0 |
| ViLaSR | direct | wprd01 | t4 | transform/mirror_h_rot90/oracle | oracle | 30.0 | 120 | 400 | 400 | 0 |
| ViLaSR | direct | wprd01 | t4 | transform/rot180/direct | direct | 30.5 | 122 | 400 | 400 | 0 |
| ViLaSR | direct | wprd01 | t4 | transform/rot180/oracle | oracle | 35.2 | 141 | 400 | 400 | 0 |
| ViLaSR | direct | wprd01 | t4 | transform/rot270/direct | direct | 29.2 | 117 | 400 | 400 | 0 |
| ViLaSR | direct | wprd01 | t4 | transform/rot270/oracle | oracle | 30.0 | 120 | 400 | 400 | 0 |
| ViLaSR | direct | wprd01 | t4 | transform/rot90/direct | direct | 31.5 | 126 | 400 | 400 | 0 |
| ViLaSR | direct | wprd01 | t4 | transform/rot90/oracle | oracle | 32.0 | 128 | 400 | 400 | 0 |
| ViLaSR | direct | wprd01 | t4 | world/intervention_001/direct | direct | 21.5 | 43 | 200 | 200 | 0 |
| ViLaSR | direct | wprd01 | t4 | world/intervention_001/oracle | oracle | 30.0 | 60 | 200 | 200 | 0 |
| ViLaSR | direct | wprd01 | t4 | world/sham_001/direct | direct | 20.0 | 14 | 70 | 70 | 0 |
| InternVL3-8B-Instruct | direct | blank | t1 | base/direct | direct | 50.2 | 201 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | blank | t1 | base/oracle | oracle | 59.5 | 238 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | blank | t1 | transform/mirror_h/direct | direct | 46.5 | 186 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | blank | t1 | transform/mirror_h/oracle | oracle | 56.5 | 226 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | blank | t1 | transform/mirror_h_rot180/direct | direct | 42.0 | 168 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | blank | t1 | transform/mirror_h_rot180/oracle | oracle | 50.8 | 203 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | blank | t1 | transform/mirror_h_rot270/direct | direct | 38.8 | 155 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | blank | t1 | transform/mirror_h_rot270/oracle | oracle | 46.5 | 186 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | blank | t1 | transform/mirror_h_rot90/direct | direct | 38.8 | 155 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | blank | t1 | transform/mirror_h_rot90/oracle | oracle | 54.2 | 217 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | blank | t1 | transform/rot180/direct | direct | 45.5 | 182 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | blank | t1 | transform/rot180/oracle | oracle | 49.5 | 198 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | blank | t1 | transform/rot270/direct | direct | 51.0 | 204 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | blank | t1 | transform/rot270/oracle | oracle | 59.8 | 239 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | blank | t1 | transform/rot90/direct | direct | 50.0 | 200 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | blank | t1 | transform/rot90/oracle | oracle | 51.8 | 207 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | blank | t2 | base/direct | direct | 59.0 | 236 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | blank | t2 | base/oracle | oracle | 60.0 | 240 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | blank | t2 | transform/mirror_h/direct | direct | 60.2 | 241 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | blank | t2 | transform/mirror_h/oracle | oracle | 62.5 | 250 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | blank | t2 | transform/mirror_h_rot180/direct | direct | 63.2 | 253 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | blank | t2 | transform/mirror_h_rot180/oracle | oracle | 62.2 | 249 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | blank | t2 | transform/mirror_h_rot270/direct | direct | 54.8 | 219 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | blank | t2 | transform/mirror_h_rot270/oracle | oracle | 63.2 | 253 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | blank | t2 | transform/mirror_h_rot90/direct | direct | 58.8 | 235 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | blank | t2 | transform/mirror_h_rot90/oracle | oracle | 56.8 | 227 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | blank | t2 | transform/rot180/direct | direct | 62.0 | 248 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | blank | t2 | transform/rot180/oracle | oracle | 59.8 | 239 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | blank | t2 | transform/rot270/direct | direct | 56.0 | 224 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | blank | t2 | transform/rot270/oracle | oracle | 58.5 | 234 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | blank | t2 | transform/rot90/direct | direct | 56.0 | 224 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | blank | t2 | transform/rot90/oracle | oracle | 61.0 | 244 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | sat | t1 | base/direct | direct | 60.8 | 243 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | sat | t1 | base/oracle | oracle | 66.2 | 265 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | sat | t1 | transform/mirror_h/direct | direct | 44.5 | 178 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | sat | t1 | transform/mirror_h/oracle | oracle | 54.0 | 216 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | sat | t1 | transform/mirror_h_rot180/direct | direct | 40.8 | 163 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | sat | t1 | transform/mirror_h_rot180/oracle | oracle | 47.8 | 191 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | sat | t1 | transform/mirror_h_rot270/direct | direct | 40.8 | 163 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | sat | t1 | transform/mirror_h_rot270/oracle | oracle | 46.2 | 185 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | sat | t1 | transform/mirror_h_rot90/direct | direct | 42.5 | 170 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | sat | t1 | transform/mirror_h_rot90/oracle | oracle | 53.0 | 212 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | sat | t1 | transform/rot180/direct | direct | 42.8 | 171 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | sat | t1 | transform/rot180/oracle | oracle | 49.0 | 196 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | sat | t1 | transform/rot270/direct | direct | 51.0 | 204 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | sat | t1 | transform/rot270/oracle | oracle | 60.5 | 242 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | sat | t1 | transform/rot90/direct | direct | 48.8 | 195 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | sat | t1 | transform/rot90/oracle | oracle | 55.8 | 223 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | sat | t2 | base/direct | direct | 44.5 | 178 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | sat | t2 | base/oracle | oracle | 45.5 | 182 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | sat | t2 | transform/mirror_h/direct | direct | 55.0 | 220 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | sat | t2 | transform/mirror_h/oracle | oracle | 57.5 | 230 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | sat | t2 | transform/mirror_h_rot180/direct | direct | 55.5 | 222 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | sat | t2 | transform/mirror_h_rot180/oracle | oracle | 59.5 | 238 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | sat | t2 | transform/mirror_h_rot270/direct | direct | 57.0 | 228 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | sat | t2 | transform/mirror_h_rot270/oracle | oracle | 60.2 | 241 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | sat | t2 | transform/mirror_h_rot90/direct | direct | 59.0 | 236 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | sat | t2 | transform/mirror_h_rot90/oracle | oracle | 58.2 | 233 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | sat | t2 | transform/rot180/direct | direct | 56.8 | 227 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | sat | t2 | transform/rot180/oracle | oracle | 56.2 | 225 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | sat | t2 | transform/rot270/direct | direct | 54.8 | 219 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | sat | t2 | transform/rot270/oracle | oracle | 56.8 | 227 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | sat | t2 | transform/rot90/direct | direct | 56.2 | 225 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | sat | t2 | transform/rot90/oracle | oracle | 57.8 | 231 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | sat | t3 | base/direct | direct | 40.5 | 81 | 200 | 200 | 0 |
| InternVL3-8B-Instruct | direct | sat | t3 | base/oracle | oracle | 51.5 | 103 | 200 | 200 | 0 |
| InternVL3-8B-Instruct | direct | sat | t3 | transform/mirror_h/direct | direct | 33.0 | 66 | 200 | 200 | 0 |
| InternVL3-8B-Instruct | direct | sat | t3 | transform/mirror_h/oracle | oracle | 48.5 | 97 | 200 | 200 | 0 |
| InternVL3-8B-Instruct | direct | sat | t3 | transform/mirror_h_rot180/direct | direct | 38.5 | 77 | 200 | 200 | 0 |
| InternVL3-8B-Instruct | direct | sat | t3 | transform/mirror_h_rot180/oracle | oracle | 45.0 | 90 | 200 | 200 | 0 |
| InternVL3-8B-Instruct | direct | sat | t3 | transform/mirror_h_rot270/direct | direct | 37.5 | 75 | 200 | 200 | 0 |
| InternVL3-8B-Instruct | direct | sat | t3 | transform/mirror_h_rot270/oracle | oracle | 50.0 | 100 | 200 | 200 | 0 |
| InternVL3-8B-Instruct | direct | sat | t3 | transform/mirror_h_rot90/direct | direct | 36.0 | 72 | 200 | 200 | 0 |
| InternVL3-8B-Instruct | direct | sat | t3 | transform/mirror_h_rot90/oracle | oracle | 49.0 | 98 | 200 | 200 | 0 |
| InternVL3-8B-Instruct | direct | sat | t3 | transform/rot180/direct | direct | 36.0 | 72 | 200 | 200 | 0 |
| InternVL3-8B-Instruct | direct | sat | t3 | transform/rot180/oracle | oracle | 46.0 | 92 | 200 | 200 | 0 |
| InternVL3-8B-Instruct | direct | sat | t3 | transform/rot270/direct | direct | 37.0 | 74 | 200 | 200 | 0 |
| InternVL3-8B-Instruct | direct | sat | t3 | transform/rot270/oracle | oracle | 49.5 | 99 | 200 | 200 | 0 |
| InternVL3-8B-Instruct | direct | sat | t3 | transform/rot90/direct | direct | 39.0 | 78 | 200 | 200 | 0 |
| InternVL3-8B-Instruct | direct | sat | t3 | transform/rot90/oracle | oracle | 48.0 | 96 | 200 | 200 | 0 |
| InternVL3-8B-Instruct | direct | sat | t3 | world/intervention_001/direct | direct | 44.0 | 88 | 200 | 200 | 0 |
| InternVL3-8B-Instruct | direct | sat | t3 | world/intervention_001/oracle | oracle | 44.0 | 88 | 200 | 200 | 0 |
| InternVL3-8B-Instruct | direct | sat | t3 | world/sham_001/direct | direct | 24.5 | 49 | 200 | 200 | 0 |
| InternVL3-8B-Instruct | direct | sat | t3 | world/sham_001/oracle | oracle | 36.0 | 72 | 200 | 200 | 0 |
| InternVL3-8B-Instruct | direct | sat | t4 | base/direct | direct | 31.2 | 125 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | sat | t4 | base/oracle | oracle | 36.2 | 145 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | sat | t4 | transform/mirror_h/direct | direct | 31.2 | 125 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | sat | t4 | transform/mirror_h/oracle | oracle | 38.8 | 155 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | sat | t4 | transform/mirror_h_rot180/direct | direct | 31.0 | 124 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | sat | t4 | transform/mirror_h_rot180/oracle | oracle | 36.8 | 147 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | sat | t4 | transform/mirror_h_rot270/direct | direct | 30.5 | 122 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | sat | t4 | transform/mirror_h_rot270/oracle | oracle | 39.0 | 156 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | sat | t4 | transform/mirror_h_rot90/direct | direct | 31.2 | 125 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | sat | t4 | transform/mirror_h_rot90/oracle | oracle | 36.5 | 146 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | sat | t4 | transform/rot180/direct | direct | 34.0 | 136 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | sat | t4 | transform/rot180/oracle | oracle | 39.2 | 157 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | sat | t4 | transform/rot270/direct | direct | 33.5 | 134 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | sat | t4 | transform/rot270/oracle | oracle | 39.8 | 159 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | sat | t4 | transform/rot90/direct | direct | 31.8 | 127 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | sat | t4 | transform/rot90/oracle | oracle | 37.2 | 149 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | sat | t4 | world/intervention_001/direct | direct | 9.0 | 18 | 200 | 200 | 0 |
| InternVL3-8B-Instruct | direct | sat | t4 | world/intervention_001/oracle | oracle | 12.0 | 24 | 200 | 200 | 0 |
| InternVL3-8B-Instruct | direct | sat | t4 | world/sham_001/direct | direct | 30.5 | 61 | 200 | 200 | 0 |
| InternVL3-8B-Instruct | direct | sat | t4 | world/sham_001/oracle | oracle | 35.0 | 70 | 200 | 200 | 0 |
| InternVL3-8B-Instruct | direct | webrd04 | t1 | base/direct | direct | 51.0 | 204 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | webrd04 | t1 | base/oracle | oracle | 58.2 | 233 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | webrd04 | t2 | base/direct | direct | 57.8 | 231 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | webrd04 | t2 | base/oracle | oracle | 57.8 | 231 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | webrd04 | t3 | base/direct | direct | 50.0 | 100 | 200 | 200 | 0 |
| InternVL3-8B-Instruct | direct | webrd04 | t3 | base/oracle | oracle | 48.5 | 97 | 200 | 200 | 0 |
| InternVL3-8B-Instruct | direct | webrd04 | t3 | world/intervention_001/direct | direct | 27.0 | 54 | 200 | 200 | 0 |
| InternVL3-8B-Instruct | direct | webrd04 | t3 | world/intervention_001/oracle | oracle | 27.5 | 55 | 200 | 200 | 0 |
| InternVL3-8B-Instruct | direct | webrd04 | t3 | world/sham_001/direct | direct | 41.0 | 82 | 200 | 200 | 0 |
| InternVL3-8B-Instruct | direct | webrd04 | t3 | world/sham_001/oracle | oracle | 41.0 | 82 | 200 | 200 | 0 |
| InternVL3-8B-Instruct | direct | webrd04 | t4 | base/direct | direct | 35.5 | 142 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | webrd04 | t4 | base/oracle | oracle | 40.2 | 161 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | webrd04 | t4 | world/intervention_001/direct | direct | 11.5 | 23 | 200 | 200 | 0 |
| InternVL3-8B-Instruct | direct | webrd04 | t4 | world/intervention_001/oracle | oracle | 15.0 | 30 | 200 | 200 | 0 |
| InternVL3-8B-Instruct | direct | webrd04 | t4 | world/sham_001/direct | direct | 35.5 | 71 | 200 | 200 | 0 |
| InternVL3-8B-Instruct | direct | webrd04 | t4 | world/sham_001/oracle | oracle | 36.0 | 72 | 200 | 200 | 0 |
| InternVL3-8B-Instruct | direct | wprd01 | t1 | base/direct | direct | 62.2 | 249 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | wprd01 | t1 | base/oracle | oracle | 65.5 | 262 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | wprd01 | t1 | transform/mirror_h/direct | direct | 57.8 | 231 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | wprd01 | t1 | transform/mirror_h/oracle | oracle | 60.2 | 241 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | wprd01 | t1 | transform/mirror_h_rot180/direct | direct | 47.2 | 189 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | wprd01 | t1 | transform/mirror_h_rot180/oracle | oracle | 52.0 | 208 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | wprd01 | t1 | transform/mirror_h_rot270/direct | direct | 48.8 | 195 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | wprd01 | t1 | transform/mirror_h_rot270/oracle | oracle | 51.2 | 205 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | wprd01 | t1 | transform/mirror_h_rot90/direct | direct | 48.5 | 194 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | wprd01 | t1 | transform/mirror_h_rot90/oracle | oracle | 57.2 | 229 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | wprd01 | t1 | transform/rot180/direct | direct | 48.2 | 193 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | wprd01 | t1 | transform/rot180/oracle | oracle | 50.2 | 201 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | wprd01 | t1 | transform/rot270/direct | direct | 53.5 | 214 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | wprd01 | t1 | transform/rot270/oracle | oracle | 56.2 | 225 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | wprd01 | t1 | transform/rot90/direct | direct | 56.0 | 224 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | wprd01 | t1 | transform/rot90/oracle | oracle | 57.2 | 229 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | wprd01 | t2 | base/direct | direct | 39.8 | 159 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | wprd01 | t2 | base/oracle | oracle | 43.5 | 174 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | wprd01 | t2 | transform/mirror_h/direct | direct | 60.2 | 241 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | wprd01 | t2 | transform/mirror_h/oracle | oracle | 58.0 | 232 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | wprd01 | t2 | transform/mirror_h_rot180/direct | direct | 60.5 | 242 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | wprd01 | t2 | transform/mirror_h_rot180/oracle | oracle | 57.0 | 228 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | wprd01 | t2 | transform/mirror_h_rot270/direct | direct | 63.0 | 252 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | wprd01 | t2 | transform/mirror_h_rot270/oracle | oracle | 60.8 | 243 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | wprd01 | t2 | transform/mirror_h_rot90/direct | direct | 61.0 | 244 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | wprd01 | t2 | transform/mirror_h_rot90/oracle | oracle | 60.0 | 240 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | wprd01 | t2 | transform/rot180/direct | direct | 59.5 | 238 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | wprd01 | t2 | transform/rot180/oracle | oracle | 58.5 | 234 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | wprd01 | t2 | transform/rot270/direct | direct | 59.5 | 238 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | wprd01 | t2 | transform/rot270/oracle | oracle | 57.5 | 230 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | wprd01 | t2 | transform/rot90/direct | direct | 60.0 | 240 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | wprd01 | t2 | transform/rot90/oracle | oracle | 59.0 | 236 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | wprd01 | t3 | base/direct | direct | 31.0 | 62 | 200 | 200 | 0 |
| InternVL3-8B-Instruct | direct | wprd01 | t3 | base/oracle | oracle | 36.0 | 72 | 200 | 200 | 0 |
| InternVL3-8B-Instruct | direct | wprd01 | t3 | transform/mirror_h/direct | direct | 30.0 | 60 | 200 | 200 | 0 |
| InternVL3-8B-Instruct | direct | wprd01 | t3 | transform/mirror_h/oracle | oracle | 34.5 | 69 | 200 | 200 | 0 |
| InternVL3-8B-Instruct | direct | wprd01 | t3 | transform/mirror_h_rot180/direct | direct | 30.5 | 61 | 200 | 200 | 0 |
| InternVL3-8B-Instruct | direct | wprd01 | t3 | transform/mirror_h_rot180/oracle | oracle | 32.5 | 65 | 200 | 200 | 0 |
| InternVL3-8B-Instruct | direct | wprd01 | t3 | transform/mirror_h_rot270/direct | direct | 30.0 | 60 | 200 | 200 | 0 |
| InternVL3-8B-Instruct | direct | wprd01 | t3 | transform/mirror_h_rot270/oracle | oracle | 34.5 | 69 | 200 | 200 | 0 |
| InternVL3-8B-Instruct | direct | wprd01 | t3 | transform/mirror_h_rot90/direct | direct | 29.0 | 58 | 200 | 200 | 0 |
| InternVL3-8B-Instruct | direct | wprd01 | t3 | transform/mirror_h_rot90/oracle | oracle | 37.0 | 74 | 200 | 200 | 0 |
| InternVL3-8B-Instruct | direct | wprd01 | t3 | transform/rot180/direct | direct | 31.5 | 63 | 200 | 200 | 0 |
| InternVL3-8B-Instruct | direct | wprd01 | t3 | transform/rot180/oracle | oracle | 36.0 | 72 | 200 | 200 | 0 |
| InternVL3-8B-Instruct | direct | wprd01 | t3 | transform/rot270/direct | direct | 30.0 | 60 | 200 | 200 | 0 |
| InternVL3-8B-Instruct | direct | wprd01 | t3 | transform/rot270/oracle | oracle | 37.0 | 74 | 200 | 200 | 0 |
| InternVL3-8B-Instruct | direct | wprd01 | t3 | transform/rot90/direct | direct | 29.5 | 59 | 200 | 200 | 0 |
| InternVL3-8B-Instruct | direct | wprd01 | t3 | transform/rot90/oracle | oracle | 36.0 | 72 | 200 | 200 | 0 |
| InternVL3-8B-Instruct | direct | wprd01 | t3 | world/intervention_001/direct | direct | 46.0 | 92 | 200 | 200 | 0 |
| InternVL3-8B-Instruct | direct | wprd01 | t3 | world/intervention_001/oracle | oracle | 46.5 | 93 | 200 | 200 | 0 |
| InternVL3-8B-Instruct | direct | wprd01 | t3 | world/sham_001/direct | direct | 17.5 | 35 | 200 | 200 | 0 |
| InternVL3-8B-Instruct | direct | wprd01 | t3 | world/sham_001/oracle | oracle | 20.5 | 41 | 200 | 200 | 0 |
| InternVL3-8B-Instruct | direct | wprd01 | t4 | base/direct | direct | 35.5 | 142 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | wprd01 | t4 | base/oracle | oracle | 37.0 | 148 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | wprd01 | t4 | transform/mirror_h/direct | direct | 33.2 | 133 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | wprd01 | t4 | transform/mirror_h/oracle | oracle | 38.8 | 155 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | wprd01 | t4 | transform/mirror_h_rot180/direct | direct | 35.2 | 141 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | wprd01 | t4 | transform/mirror_h_rot180/oracle | oracle | 42.0 | 168 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | wprd01 | t4 | transform/mirror_h_rot270/direct | direct | 38.0 | 152 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | wprd01 | t4 | transform/mirror_h_rot270/oracle | oracle | 40.8 | 163 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | wprd01 | t4 | transform/mirror_h_rot90/direct | direct | 33.8 | 135 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | wprd01 | t4 | transform/mirror_h_rot90/oracle | oracle | 36.8 | 147 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | wprd01 | t4 | transform/rot180/direct | direct | 36.2 | 145 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | wprd01 | t4 | transform/rot180/oracle | oracle | 40.8 | 163 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | wprd01 | t4 | transform/rot270/direct | direct | 35.2 | 141 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | wprd01 | t4 | transform/rot270/oracle | oracle | 41.5 | 166 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | wprd01 | t4 | transform/rot90/direct | direct | 35.0 | 140 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | wprd01 | t4 | transform/rot90/oracle | oracle | 37.0 | 148 | 400 | 400 | 0 |
| InternVL3-8B-Instruct | direct | wprd01 | t4 | world/intervention_001/direct | direct | 8.0 | 16 | 200 | 200 | 0 |
| InternVL3-8B-Instruct | direct | wprd01 | t4 | world/intervention_001/oracle | oracle | 13.5 | 27 | 200 | 200 | 0 |
| InternVL3-8B-Instruct | direct | wprd01 | t4 | world/sham_001/direct | direct | 31.0 | 62 | 200 | 200 | 0 |
| InternVL3-8B-Instruct | direct | wprd01 | t4 | world/sham_001/oracle | oracle | 35.5 | 71 | 200 | 200 | 0 |
| Qwen2-VL-7B-Instruct | direct | blank | t1 | base/direct | direct | 55.8 | 223 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | blank | t1 | base/oracle | oracle | 60.8 | 243 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | blank | t1 | transform/mirror_h/direct | direct | 53.0 | 212 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | blank | t1 | transform/mirror_h/oracle | oracle | 54.5 | 218 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | blank | t1 | transform/mirror_h_rot180/direct | direct | 48.0 | 192 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | blank | t1 | transform/mirror_h_rot180/oracle | oracle | 54.2 | 217 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | blank | t1 | transform/mirror_h_rot270/direct | direct | 48.0 | 192 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | blank | t1 | transform/mirror_h_rot270/oracle | oracle | 49.0 | 196 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | blank | t1 | transform/mirror_h_rot90/direct | direct | 52.8 | 211 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | blank | t1 | transform/mirror_h_rot90/oracle | oracle | 59.2 | 237 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | blank | t1 | transform/rot180/direct | direct | 42.8 | 171 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | blank | t1 | transform/rot180/oracle | oracle | 48.0 | 192 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | blank | t1 | transform/rot270/direct | direct | 51.2 | 205 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | blank | t1 | transform/rot270/oracle | oracle | 54.5 | 218 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | blank | t1 | transform/rot90/direct | direct | 47.0 | 188 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | blank | t1 | transform/rot90/oracle | oracle | 50.0 | 200 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | blank | t2 | base/direct | direct | 52.0 | 208 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | blank | t2 | base/oracle | oracle | 43.0 | 172 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | blank | t2 | transform/mirror_h/direct | direct | 46.8 | 187 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | blank | t2 | transform/mirror_h/oracle | oracle | 43.0 | 172 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | blank | t2 | transform/mirror_h_rot180/direct | direct | 56.5 | 226 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | blank | t2 | transform/mirror_h_rot180/oracle | oracle | 45.0 | 180 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | blank | t2 | transform/mirror_h_rot270/direct | direct | 46.8 | 187 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | blank | t2 | transform/mirror_h_rot270/oracle | oracle | 40.0 | 160 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | blank | t2 | transform/mirror_h_rot90/direct | direct | 51.5 | 206 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | blank | t2 | transform/mirror_h_rot90/oracle | oracle | 40.5 | 162 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | blank | t2 | transform/rot180/direct | direct | 48.5 | 194 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | blank | t2 | transform/rot180/oracle | oracle | 42.5 | 170 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | blank | t2 | transform/rot270/direct | direct | 47.5 | 190 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | blank | t2 | transform/rot270/oracle | oracle | 40.2 | 161 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | blank | t2 | transform/rot90/direct | direct | 50.8 | 203 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | blank | t2 | transform/rot90/oracle | oracle | 39.8 | 159 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | sat | t1 | base/direct | direct | 46.5 | 186 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | sat | t1 | base/oracle | oracle | 52.2 | 209 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | sat | t1 | transform/mirror_h/direct | direct | 45.8 | 183 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | sat | t1 | transform/mirror_h/oracle | oracle | 44.0 | 176 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | sat | t1 | transform/mirror_h_rot180/direct | direct | 35.8 | 143 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | sat | t1 | transform/mirror_h_rot180/oracle | oracle | 39.8 | 159 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | sat | t1 | transform/mirror_h_rot270/direct | direct | 41.2 | 165 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | sat | t1 | transform/mirror_h_rot270/oracle | oracle | 42.5 | 170 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | sat | t1 | transform/mirror_h_rot90/direct | direct | 50.2 | 201 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | sat | t1 | transform/mirror_h_rot90/oracle | oracle | 56.0 | 224 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | sat | t1 | transform/rot180/direct | direct | 35.0 | 140 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | sat | t1 | transform/rot180/oracle | oracle | 44.0 | 176 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | sat | t1 | transform/rot270/direct | direct | 45.5 | 182 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | sat | t1 | transform/rot270/oracle | oracle | 46.8 | 187 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | sat | t1 | transform/rot90/direct | direct | 35.2 | 141 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | sat | t1 | transform/rot90/oracle | oracle | 41.8 | 167 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | sat | t2 | base/direct | direct | 34.2 | 137 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | sat | t2 | base/oracle | oracle | 43.8 | 175 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | sat | t2 | transform/mirror_h/direct | direct | 44.5 | 178 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | sat | t2 | transform/mirror_h/oracle | oracle | 41.8 | 167 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | sat | t2 | transform/mirror_h_rot180/direct | direct | 50.0 | 200 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | sat | t2 | transform/mirror_h_rot180/oracle | oracle | 44.8 | 179 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | sat | t2 | transform/mirror_h_rot270/direct | direct | 50.5 | 202 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | sat | t2 | transform/mirror_h_rot270/oracle | oracle | 45.8 | 183 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | sat | t2 | transform/mirror_h_rot90/direct | direct | 51.5 | 206 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | sat | t2 | transform/mirror_h_rot90/oracle | oracle | 43.2 | 173 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | sat | t2 | transform/rot180/direct | direct | 48.0 | 192 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | sat | t2 | transform/rot180/oracle | oracle | 43.8 | 175 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | sat | t2 | transform/rot270/direct | direct | 45.2 | 181 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | sat | t2 | transform/rot270/oracle | oracle | 41.0 | 164 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | sat | t2 | transform/rot90/direct | direct | 50.2 | 201 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | sat | t2 | transform/rot90/oracle | oracle | 42.2 | 169 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | sat | t3 | base/direct | direct | 41.0 | 82 | 200 | 200 | 0 |
| Qwen2-VL-7B-Instruct | direct | sat | t3 | base/oracle | oracle | 46.5 | 93 | 200 | 200 | 0 |
| Qwen2-VL-7B-Instruct | direct | sat | t3 | transform/mirror_h/direct | direct | 42.0 | 84 | 200 | 200 | 0 |
| Qwen2-VL-7B-Instruct | direct | sat | t3 | transform/mirror_h/oracle | oracle | 43.5 | 87 | 200 | 200 | 0 |
| Qwen2-VL-7B-Instruct | direct | sat | t3 | transform/mirror_h_rot180/direct | direct | 43.5 | 87 | 200 | 200 | 0 |
| Qwen2-VL-7B-Instruct | direct | sat | t3 | transform/mirror_h_rot180/oracle | oracle | 47.0 | 94 | 200 | 200 | 0 |
| Qwen2-VL-7B-Instruct | direct | sat | t3 | transform/mirror_h_rot270/direct | direct | 44.0 | 88 | 200 | 200 | 0 |
| Qwen2-VL-7B-Instruct | direct | sat | t3 | transform/mirror_h_rot270/oracle | oracle | 46.0 | 92 | 200 | 200 | 0 |
| Qwen2-VL-7B-Instruct | direct | sat | t3 | transform/mirror_h_rot90/direct | direct | 43.0 | 86 | 200 | 200 | 0 |
| Qwen2-VL-7B-Instruct | direct | sat | t3 | transform/mirror_h_rot90/oracle | oracle | 46.0 | 92 | 200 | 200 | 0 |
| Qwen2-VL-7B-Instruct | direct | sat | t3 | transform/rot180/direct | direct | 43.0 | 86 | 200 | 200 | 0 |
| Qwen2-VL-7B-Instruct | direct | sat | t3 | transform/rot180/oracle | oracle | 47.5 | 95 | 200 | 200 | 0 |
| Qwen2-VL-7B-Instruct | direct | sat | t3 | transform/rot270/direct | direct | 43.0 | 86 | 200 | 200 | 0 |
| Qwen2-VL-7B-Instruct | direct | sat | t3 | transform/rot270/oracle | oracle | 48.0 | 96 | 200 | 200 | 0 |
| Qwen2-VL-7B-Instruct | direct | sat | t3 | transform/rot90/direct | direct | 41.5 | 83 | 200 | 200 | 0 |
| Qwen2-VL-7B-Instruct | direct | sat | t3 | transform/rot90/oracle | oracle | 48.5 | 97 | 200 | 200 | 0 |
| Qwen2-VL-7B-Instruct | direct | sat | t3 | world/intervention_001/direct | direct | 28.5 | 57 | 200 | 200 | 0 |
| Qwen2-VL-7B-Instruct | direct | sat | t3 | world/intervention_001/oracle | oracle | 30.0 | 60 | 200 | 200 | 0 |
| Qwen2-VL-7B-Instruct | direct | sat | t3 | world/sham_001/direct | direct | 48.0 | 96 | 200 | 200 | 0 |
| Qwen2-VL-7B-Instruct | direct | sat | t3 | world/sham_001/oracle | oracle | 47.5 | 95 | 200 | 200 | 0 |
| Qwen2-VL-7B-Instruct | direct | sat | t4 | base/direct | direct | 30.0 | 120 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | sat | t4 | base/oracle | oracle | 34.0 | 136 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | sat | t4 | transform/mirror_h/direct | direct | 30.5 | 122 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | sat | t4 | transform/mirror_h/oracle | oracle | 35.0 | 140 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | sat | t4 | transform/mirror_h_rot180/direct | direct | 34.0 | 136 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | sat | t4 | transform/mirror_h_rot180/oracle | oracle | 34.5 | 138 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | sat | t4 | transform/mirror_h_rot270/direct | direct | 35.8 | 143 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | sat | t4 | transform/mirror_h_rot270/oracle | oracle | 36.5 | 146 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | sat | t4 | transform/mirror_h_rot90/direct | direct | 32.0 | 128 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | sat | t4 | transform/mirror_h_rot90/oracle | oracle | 34.0 | 136 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | sat | t4 | transform/rot180/direct | direct | 31.8 | 127 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | sat | t4 | transform/rot180/oracle | oracle | 34.0 | 136 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | sat | t4 | transform/rot270/direct | direct | 34.0 | 136 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | sat | t4 | transform/rot270/oracle | oracle | 38.2 | 153 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | sat | t4 | transform/rot90/direct | direct | 30.2 | 121 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | sat | t4 | transform/rot90/oracle | oracle | 34.0 | 136 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | sat | t4 | world/intervention_001/direct | direct | 24.5 | 49 | 200 | 200 | 0 |
| Qwen2-VL-7B-Instruct | direct | sat | t4 | world/intervention_001/oracle | oracle | 30.0 | 60 | 200 | 200 | 0 |
| Qwen2-VL-7B-Instruct | direct | sat | t4 | world/sham_001/direct | direct | 27.0 | 54 | 200 | 200 | 0 |
| Qwen2-VL-7B-Instruct | direct | sat | t4 | world/sham_001/oracle | oracle | 32.0 | 64 | 200 | 200 | 0 |
| Qwen2-VL-7B-Instruct | direct | webrd04 | t1 | base/direct | direct | 55.5 | 222 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | webrd04 | t1 | base/oracle | oracle | 64.0 | 256 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | webrd04 | t2 | base/direct | direct | 45.2 | 181 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | webrd04 | t2 | base/oracle | oracle | 40.5 | 162 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | webrd04 | t3 | base/direct | direct | 44.0 | 88 | 200 | 200 | 0 |
| Qwen2-VL-7B-Instruct | direct | webrd04 | t3 | base/oracle | oracle | 42.5 | 85 | 200 | 200 | 0 |
| Qwen2-VL-7B-Instruct | direct | webrd04 | t3 | world/intervention_001/direct | direct | 24.5 | 49 | 200 | 200 | 0 |
| Qwen2-VL-7B-Instruct | direct | webrd04 | t3 | world/intervention_001/oracle | oracle | 26.0 | 52 | 200 | 200 | 0 |
| Qwen2-VL-7B-Instruct | direct | webrd04 | t3 | world/sham_001/direct | direct | 45.5 | 91 | 200 | 200 | 0 |
| Qwen2-VL-7B-Instruct | direct | webrd04 | t3 | world/sham_001/oracle | oracle | 44.0 | 88 | 200 | 200 | 0 |
| Qwen2-VL-7B-Instruct | direct | webrd04 | t4 | base/direct | direct | 31.5 | 126 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | webrd04 | t4 | base/oracle | oracle | 32.5 | 130 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | webrd04 | t4 | world/intervention_001/direct | direct | 25.5 | 51 | 200 | 200 | 0 |
| Qwen2-VL-7B-Instruct | direct | webrd04 | t4 | world/intervention_001/oracle | oracle | 35.0 | 70 | 200 | 200 | 0 |
| Qwen2-VL-7B-Instruct | direct | webrd04 | t4 | world/sham_001/direct | direct | 21.0 | 42 | 200 | 200 | 0 |
| Qwen2-VL-7B-Instruct | direct | webrd04 | t4 | world/sham_001/oracle | oracle | 31.0 | 62 | 200 | 200 | 0 |
| Qwen2-VL-7B-Instruct | direct | wprd01 | t1 | base/direct | direct | 51.0 | 204 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | wprd01 | t1 | base/oracle | oracle | 47.5 | 190 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | wprd01 | t1 | transform/mirror_h/direct | direct | 48.8 | 195 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | wprd01 | t1 | transform/mirror_h/oracle | oracle | 50.5 | 202 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | wprd01 | t1 | transform/mirror_h_rot180/direct | direct | 43.2 | 173 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | wprd01 | t1 | transform/mirror_h_rot180/oracle | oracle | 47.8 | 191 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | wprd01 | t1 | transform/mirror_h_rot270/direct | direct | 46.8 | 187 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | wprd01 | t1 | transform/mirror_h_rot270/oracle | oracle | 49.2 | 197 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | wprd01 | t1 | transform/mirror_h_rot90/direct | direct | 55.5 | 222 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | wprd01 | t1 | transform/mirror_h_rot90/oracle | oracle | 63.0 | 252 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | wprd01 | t1 | transform/rot180/direct | direct | 41.5 | 166 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | wprd01 | t1 | transform/rot180/oracle | oracle | 51.5 | 206 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | wprd01 | t1 | transform/rot270/direct | direct | 46.2 | 185 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | wprd01 | t1 | transform/rot270/oracle | oracle | 52.0 | 208 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | wprd01 | t1 | transform/rot90/direct | direct | 40.0 | 160 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | wprd01 | t1 | transform/rot90/oracle | oracle | 45.2 | 181 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | wprd01 | t2 | base/direct | direct | 31.5 | 126 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | wprd01 | t2 | base/oracle | oracle | 42.5 | 170 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | wprd01 | t2 | transform/mirror_h/direct | direct | 45.2 | 181 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | wprd01 | t2 | transform/mirror_h/oracle | oracle | 41.0 | 164 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | wprd01 | t2 | transform/mirror_h_rot180/direct | direct | 47.2 | 189 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | wprd01 | t2 | transform/mirror_h_rot180/oracle | oracle | 41.8 | 167 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | wprd01 | t2 | transform/mirror_h_rot270/direct | direct | 44.8 | 179 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | wprd01 | t2 | transform/mirror_h_rot270/oracle | oracle | 45.5 | 182 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | wprd01 | t2 | transform/mirror_h_rot90/direct | direct | 44.8 | 179 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | wprd01 | t2 | transform/mirror_h_rot90/oracle | oracle | 43.0 | 172 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | wprd01 | t2 | transform/rot180/direct | direct | 41.5 | 166 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | wprd01 | t2 | transform/rot180/oracle | oracle | 40.8 | 163 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | wprd01 | t2 | transform/rot270/direct | direct | 48.0 | 192 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | wprd01 | t2 | transform/rot270/oracle | oracle | 42.0 | 168 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | wprd01 | t2 | transform/rot90/direct | direct | 41.0 | 164 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | wprd01 | t2 | transform/rot90/oracle | oracle | 38.5 | 154 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | wprd01 | t3 | base/direct | direct | 32.5 | 65 | 200 | 200 | 0 |
| Qwen2-VL-7B-Instruct | direct | wprd01 | t3 | base/oracle | oracle | 38.0 | 76 | 200 | 200 | 0 |
| Qwen2-VL-7B-Instruct | direct | wprd01 | t3 | transform/mirror_h/direct | direct | 34.5 | 69 | 200 | 200 | 0 |
| Qwen2-VL-7B-Instruct | direct | wprd01 | t3 | transform/mirror_h/oracle | oracle | 36.0 | 72 | 200 | 200 | 0 |
| Qwen2-VL-7B-Instruct | direct | wprd01 | t3 | transform/mirror_h_rot180/direct | direct | 32.0 | 64 | 200 | 200 | 0 |
| Qwen2-VL-7B-Instruct | direct | wprd01 | t3 | transform/mirror_h_rot180/oracle | oracle | 34.0 | 68 | 200 | 200 | 0 |
| Qwen2-VL-7B-Instruct | direct | wprd01 | t3 | transform/mirror_h_rot270/direct | direct | 37.0 | 74 | 200 | 200 | 0 |
| Qwen2-VL-7B-Instruct | direct | wprd01 | t3 | transform/mirror_h_rot270/oracle | oracle | 39.5 | 79 | 200 | 200 | 0 |
| Qwen2-VL-7B-Instruct | direct | wprd01 | t3 | transform/mirror_h_rot90/direct | direct | 32.0 | 64 | 200 | 200 | 0 |
| Qwen2-VL-7B-Instruct | direct | wprd01 | t3 | transform/mirror_h_rot90/oracle | oracle | 39.0 | 78 | 200 | 200 | 0 |
| Qwen2-VL-7B-Instruct | direct | wprd01 | t3 | transform/rot180/direct | direct | 30.0 | 60 | 200 | 200 | 0 |
| Qwen2-VL-7B-Instruct | direct | wprd01 | t3 | transform/rot180/oracle | oracle | 35.0 | 70 | 200 | 200 | 0 |
| Qwen2-VL-7B-Instruct | direct | wprd01 | t3 | transform/rot270/direct | direct | 36.0 | 72 | 200 | 200 | 0 |
| Qwen2-VL-7B-Instruct | direct | wprd01 | t3 | transform/rot270/oracle | oracle | 35.5 | 71 | 200 | 200 | 0 |
| Qwen2-VL-7B-Instruct | direct | wprd01 | t3 | transform/rot90/direct | direct | 38.0 | 76 | 200 | 200 | 0 |
| Qwen2-VL-7B-Instruct | direct | wprd01 | t3 | transform/rot90/oracle | oracle | 37.0 | 74 | 200 | 200 | 0 |
| Qwen2-VL-7B-Instruct | direct | wprd01 | t3 | world/intervention_001/direct | direct | 31.5 | 63 | 200 | 200 | 0 |
| Qwen2-VL-7B-Instruct | direct | wprd01 | t3 | world/intervention_001/oracle | oracle | 32.0 | 64 | 200 | 200 | 0 |
| Qwen2-VL-7B-Instruct | direct | wprd01 | t3 | world/sham_001/direct | direct | 44.0 | 88 | 200 | 200 | 0 |
| Qwen2-VL-7B-Instruct | direct | wprd01 | t3 | world/sham_001/oracle | oracle | 41.5 | 83 | 200 | 200 | 0 |
| Qwen2-VL-7B-Instruct | direct | wprd01 | t4 | base/direct | direct | 35.8 | 143 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | wprd01 | t4 | base/oracle | oracle | 34.5 | 138 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | wprd01 | t4 | transform/mirror_h/direct | direct | 34.2 | 137 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | wprd01 | t4 | transform/mirror_h/oracle | oracle | 37.5 | 150 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | wprd01 | t4 | transform/mirror_h_rot180/direct | direct | 34.5 | 138 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | wprd01 | t4 | transform/mirror_h_rot180/oracle | oracle | 38.0 | 152 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | wprd01 | t4 | transform/mirror_h_rot270/direct | direct | 34.8 | 139 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | wprd01 | t4 | transform/mirror_h_rot270/oracle | oracle | 38.2 | 153 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | wprd01 | t4 | transform/mirror_h_rot90/direct | direct | 36.5 | 146 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | wprd01 | t4 | transform/mirror_h_rot90/oracle | oracle | 38.5 | 154 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | wprd01 | t4 | transform/rot180/direct | direct | 36.5 | 146 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | wprd01 | t4 | transform/rot180/oracle | oracle | 38.0 | 152 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | wprd01 | t4 | transform/rot270/direct | direct | 35.8 | 143 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | wprd01 | t4 | transform/rot270/oracle | oracle | 38.0 | 152 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | wprd01 | t4 | transform/rot90/direct | direct | 33.5 | 134 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | wprd01 | t4 | transform/rot90/oracle | oracle | 36.8 | 147 | 400 | 400 | 0 |
| Qwen2-VL-7B-Instruct | direct | wprd01 | t4 | world/intervention_001/direct | direct | 25.0 | 50 | 200 | 200 | 0 |
| Qwen2-VL-7B-Instruct | direct | wprd01 | t4 | world/intervention_001/oracle | oracle | 33.0 | 66 | 200 | 200 | 0 |
| Qwen2-VL-7B-Instruct | direct | wprd01 | t4 | world/sham_001/direct | direct | 25.5 | 51 | 200 | 200 | 0 |
| Qwen2-VL-7B-Instruct | direct | wprd01 | t4 | world/sham_001/oracle | oracle | 35.0 | 70 | 200 | 200 | 0 |
| Spatial-MLLM | direct | blank | t1 | base/direct | direct | 59.8 | 239 | 400 | 400 | 0 |
| Spatial-MLLM | direct | blank | t1 | base/oracle | oracle | 52.5 | 210 | 400 | 400 | 0 |
| Spatial-MLLM | direct | blank | t1 | transform/mirror_h/direct | direct | 42.0 | 168 | 400 | 400 | 0 |
| Spatial-MLLM | direct | blank | t1 | transform/mirror_h/oracle | oracle | 44.5 | 178 | 400 | 400 | 0 |
| Spatial-MLLM | direct | blank | t1 | transform/mirror_h_rot180/direct | direct | 41.2 | 165 | 400 | 400 | 0 |
| Spatial-MLLM | direct | blank | t1 | transform/mirror_h_rot180/oracle | oracle | 41.0 | 164 | 400 | 400 | 0 |
| Spatial-MLLM | direct | blank | t1 | transform/mirror_h_rot270/direct | direct | 41.0 | 164 | 400 | 400 | 0 |
| Spatial-MLLM | direct | blank | t1 | transform/mirror_h_rot270/oracle | oracle | 41.5 | 166 | 400 | 400 | 0 |
| Spatial-MLLM | direct | blank | t1 | transform/mirror_h_rot90/direct | direct | 46.5 | 186 | 400 | 400 | 0 |
| Spatial-MLLM | direct | blank | t1 | transform/mirror_h_rot90/oracle | oracle | 47.0 | 188 | 400 | 400 | 0 |
| Spatial-MLLM | direct | blank | t1 | transform/rot180/direct | direct | 53.0 | 212 | 400 | 400 | 0 |
| Spatial-MLLM | direct | blank | t1 | transform/rot180/oracle | oracle | 49.2 | 197 | 400 | 400 | 0 |
| Spatial-MLLM | direct | blank | t1 | transform/rot270/direct | direct | 53.0 | 212 | 400 | 400 | 0 |
| Spatial-MLLM | direct | blank | t1 | transform/rot270/oracle | oracle | 52.2 | 209 | 400 | 400 | 0 |
| Spatial-MLLM | direct | blank | t1 | transform/rot90/direct | direct | 50.0 | 200 | 400 | 400 | 0 |
| Spatial-MLLM | direct | blank | t1 | transform/rot90/oracle | oracle | 49.0 | 196 | 400 | 400 | 0 |
| Spatial-MLLM | direct | blank | t2 | base/direct | direct | 56.2 | 225 | 400 | 400 | 0 |
| Spatial-MLLM | direct | blank | t2 | base/oracle | oracle | 50.5 | 202 | 400 | 400 | 0 |
| Spatial-MLLM | direct | blank | t2 | transform/mirror_h/direct | direct | 57.5 | 230 | 400 | 400 | 0 |
| Spatial-MLLM | direct | blank | t2 | transform/mirror_h/oracle | oracle | 53.0 | 212 | 400 | 400 | 0 |
| Spatial-MLLM | direct | blank | t2 | transform/mirror_h_rot180/direct | direct | 60.5 | 242 | 400 | 400 | 0 |
| Spatial-MLLM | direct | blank | t2 | transform/mirror_h_rot180/oracle | oracle | 57.8 | 231 | 400 | 400 | 0 |
| Spatial-MLLM | direct | blank | t2 | transform/mirror_h_rot270/direct | direct | 59.5 | 238 | 400 | 400 | 0 |
| Spatial-MLLM | direct | blank | t2 | transform/mirror_h_rot270/oracle | oracle | 56.2 | 225 | 400 | 400 | 0 |
| Spatial-MLLM | direct | blank | t2 | transform/mirror_h_rot90/direct | direct | 58.0 | 232 | 400 | 400 | 0 |
| Spatial-MLLM | direct | blank | t2 | transform/mirror_h_rot90/oracle | oracle | 52.8 | 211 | 400 | 400 | 0 |
| Spatial-MLLM | direct | blank | t2 | transform/rot180/direct | direct | 60.2 | 241 | 400 | 400 | 0 |
| Spatial-MLLM | direct | blank | t2 | transform/rot180/oracle | oracle | 57.5 | 230 | 400 | 400 | 0 |
| Spatial-MLLM | direct | blank | t2 | transform/rot270/direct | direct | 57.5 | 230 | 400 | 400 | 0 |
| Spatial-MLLM | direct | blank | t2 | transform/rot270/oracle | oracle | 55.5 | 222 | 400 | 400 | 0 |
| Spatial-MLLM | direct | blank | t2 | transform/rot90/direct | direct | 59.0 | 236 | 400 | 400 | 0 |
| Spatial-MLLM | direct | blank | t2 | transform/rot90/oracle | oracle | 59.0 | 236 | 400 | 400 | 0 |
| Spatial-MLLM | direct | sat | t1 | base/direct | direct | 48.8 | 195 | 400 | 400 | 0 |
| Spatial-MLLM | direct | sat | t1 | base/oracle | oracle | 48.0 | 192 | 400 | 400 | 0 |
| Spatial-MLLM | direct | sat | t1 | transform/mirror_h/direct | direct | 41.8 | 167 | 400 | 400 | 0 |
| Spatial-MLLM | direct | sat | t1 | transform/mirror_h/oracle | oracle | 43.8 | 175 | 400 | 400 | 0 |
| Spatial-MLLM | direct | sat | t1 | transform/mirror_h_rot180/direct | direct | 44.0 | 176 | 400 | 400 | 0 |
| Spatial-MLLM | direct | sat | t1 | transform/mirror_h_rot180/oracle | oracle | 46.0 | 184 | 400 | 400 | 0 |
| Spatial-MLLM | direct | sat | t1 | transform/mirror_h_rot270/direct | direct | 43.0 | 172 | 400 | 400 | 0 |
| Spatial-MLLM | direct | sat | t1 | transform/mirror_h_rot270/oracle | oracle | 44.0 | 176 | 400 | 400 | 0 |
| Spatial-MLLM | direct | sat | t1 | transform/mirror_h_rot90/direct | direct | 45.5 | 182 | 400 | 400 | 0 |
| Spatial-MLLM | direct | sat | t1 | transform/mirror_h_rot90/oracle | oracle | 46.2 | 185 | 400 | 400 | 0 |
| Spatial-MLLM | direct | sat | t1 | transform/rot180/direct | direct | 52.8 | 211 | 400 | 400 | 0 |
| Spatial-MLLM | direct | sat | t1 | transform/rot180/oracle | oracle | 50.2 | 201 | 400 | 400 | 0 |
| Spatial-MLLM | direct | sat | t1 | transform/rot270/direct | direct | 52.0 | 208 | 400 | 400 | 0 |
| Spatial-MLLM | direct | sat | t1 | transform/rot270/oracle | oracle | 49.2 | 197 | 400 | 400 | 0 |
| Spatial-MLLM | direct | sat | t1 | transform/rot90/direct | direct | 49.0 | 196 | 400 | 400 | 0 |
| Spatial-MLLM | direct | sat | t1 | transform/rot90/oracle | oracle | 49.5 | 198 | 400 | 400 | 0 |
| Spatial-MLLM | direct | sat | t2 | base/direct | direct | 54.2 | 217 | 400 | 400 | 0 |
| Spatial-MLLM | direct | sat | t2 | base/oracle | oracle | 55.0 | 220 | 400 | 400 | 0 |
| Spatial-MLLM | direct | sat | t2 | transform/mirror_h/direct | direct | 54.8 | 219 | 400 | 400 | 0 |
| Spatial-MLLM | direct | sat | t2 | transform/mirror_h/oracle | oracle | 54.2 | 217 | 400 | 400 | 0 |
| Spatial-MLLM | direct | sat | t2 | transform/mirror_h_rot180/direct | direct | 55.0 | 220 | 400 | 400 | 0 |
| Spatial-MLLM | direct | sat | t2 | transform/mirror_h_rot180/oracle | oracle | 57.5 | 230 | 400 | 400 | 0 |
| Spatial-MLLM | direct | sat | t2 | transform/mirror_h_rot270/direct | direct | 51.0 | 204 | 400 | 400 | 0 |
| Spatial-MLLM | direct | sat | t2 | transform/mirror_h_rot270/oracle | oracle | 54.5 | 218 | 400 | 400 | 0 |
| Spatial-MLLM | direct | sat | t2 | transform/mirror_h_rot90/direct | direct | 56.5 | 226 | 400 | 400 | 0 |
| Spatial-MLLM | direct | sat | t2 | transform/mirror_h_rot90/oracle | oracle | 56.2 | 225 | 400 | 400 | 0 |
| Spatial-MLLM | direct | sat | t2 | transform/rot180/direct | direct | 58.2 | 233 | 400 | 400 | 0 |
| Spatial-MLLM | direct | sat | t2 | transform/rot180/oracle | oracle | 60.0 | 240 | 400 | 400 | 0 |
| Spatial-MLLM | direct | sat | t2 | transform/rot270/direct | direct | 50.5 | 202 | 400 | 400 | 0 |
| Spatial-MLLM | direct | sat | t2 | transform/rot270/oracle | oracle | 54.5 | 218 | 400 | 400 | 0 |
| Spatial-MLLM | direct | sat | t2 | transform/rot90/direct | direct | 57.0 | 228 | 400 | 400 | 0 |
| Spatial-MLLM | direct | sat | t2 | transform/rot90/oracle | oracle | 57.0 | 228 | 400 | 400 | 0 |
| Spatial-MLLM | direct | sat | t3 | base/direct | direct | 22.5 | 45 | 200 | 200 | 0 |
| Spatial-MLLM | direct | sat | t3 | base/oracle | oracle | 23.0 | 46 | 200 | 200 | 0 |
| Spatial-MLLM | direct | sat | t3 | transform/mirror_h/direct | direct | 22.0 | 44 | 200 | 200 | 0 |
| Spatial-MLLM | direct | sat | t3 | transform/mirror_h/oracle | oracle | 20.0 | 40 | 200 | 200 | 0 |
| Spatial-MLLM | direct | sat | t3 | transform/mirror_h_rot180/direct | direct | 22.0 | 44 | 200 | 200 | 0 |
| Spatial-MLLM | direct | sat | t3 | transform/mirror_h_rot180/oracle | oracle | 20.0 | 40 | 200 | 200 | 0 |
| Spatial-MLLM | direct | sat | t3 | transform/mirror_h_rot270/direct | direct | 25.5 | 51 | 200 | 200 | 0 |
| Spatial-MLLM | direct | sat | t3 | transform/mirror_h_rot270/oracle | oracle | 23.5 | 47 | 200 | 200 | 0 |
| Spatial-MLLM | direct | sat | t3 | transform/mirror_h_rot90/direct | direct | 21.5 | 43 | 200 | 200 | 0 |
| Spatial-MLLM | direct | sat | t3 | transform/mirror_h_rot90/oracle | oracle | 22.5 | 45 | 200 | 200 | 0 |
| Spatial-MLLM | direct | sat | t3 | transform/rot180/direct | direct | 25.0 | 50 | 200 | 200 | 0 |
| Spatial-MLLM | direct | sat | t3 | transform/rot180/oracle | oracle | 24.5 | 49 | 200 | 200 | 0 |
| Spatial-MLLM | direct | sat | t3 | transform/rot270/direct | direct | 25.0 | 50 | 200 | 200 | 0 |
| Spatial-MLLM | direct | sat | t3 | transform/rot270/oracle | oracle | 23.0 | 46 | 200 | 200 | 0 |
| Spatial-MLLM | direct | sat | t3 | transform/rot90/direct | direct | 22.5 | 45 | 200 | 200 | 0 |
| Spatial-MLLM | direct | sat | t3 | transform/rot90/oracle | oracle | 22.5 | 45 | 200 | 200 | 0 |
| Spatial-MLLM | direct | sat | t3 | world/intervention_001/direct | direct | 27.5 | 55 | 200 | 200 | 0 |
| Spatial-MLLM | direct | sat | t3 | world/intervention_001/oracle | oracle | 27.5 | 55 | 200 | 200 | 0 |
| Spatial-MLLM | direct | sat | t3 | world/sham_001/direct | direct | 16.0 | 32 | 200 | 200 | 0 |
| Spatial-MLLM | direct | sat | t3 | world/sham_001/oracle | oracle | 17.0 | 34 | 200 | 200 | 0 |
| Spatial-MLLM | direct | sat | t4 | base/direct | direct | 28.2 | 113 | 400 | 400 | 0 |
| Spatial-MLLM | direct | sat | t4 | base/oracle | oracle | 28.2 | 113 | 400 | 400 | 0 |
| Spatial-MLLM | direct | sat | t4 | transform/mirror_h/direct | direct | 29.8 | 119 | 400 | 400 | 0 |
| Spatial-MLLM | direct | sat | t4 | transform/mirror_h/oracle | oracle | 28.8 | 115 | 400 | 400 | 0 |
| Spatial-MLLM | direct | sat | t4 | transform/mirror_h_rot180/direct | direct | 27.8 | 111 | 400 | 400 | 0 |
| Spatial-MLLM | direct | sat | t4 | transform/mirror_h_rot180/oracle | oracle | 29.8 | 119 | 400 | 400 | 0 |
| Spatial-MLLM | direct | sat | t4 | transform/mirror_h_rot270/direct | direct | 30.0 | 120 | 400 | 400 | 0 |
| Spatial-MLLM | direct | sat | t4 | transform/mirror_h_rot270/oracle | oracle | 27.8 | 111 | 400 | 400 | 0 |
| Spatial-MLLM | direct | sat | t4 | transform/mirror_h_rot90/direct | direct | 29.5 | 118 | 400 | 400 | 0 |
| Spatial-MLLM | direct | sat | t4 | transform/mirror_h_rot90/oracle | oracle | 29.2 | 117 | 400 | 400 | 0 |
| Spatial-MLLM | direct | sat | t4 | transform/rot180/direct | direct | 24.8 | 99 | 400 | 400 | 0 |
| Spatial-MLLM | direct | sat | t4 | transform/rot180/oracle | oracle | 28.2 | 113 | 400 | 400 | 0 |
| Spatial-MLLM | direct | sat | t4 | transform/rot270/direct | direct | 27.8 | 111 | 400 | 400 | 0 |
| Spatial-MLLM | direct | sat | t4 | transform/rot270/oracle | oracle | 28.2 | 113 | 400 | 400 | 0 |
| Spatial-MLLM | direct | sat | t4 | transform/rot90/direct | direct | 29.2 | 117 | 400 | 400 | 0 |
| Spatial-MLLM | direct | sat | t4 | transform/rot90/oracle | oracle | 29.2 | 117 | 400 | 400 | 0 |
| Spatial-MLLM | direct | sat | t4 | world/intervention_001/direct | direct | 22.5 | 45 | 200 | 200 | 0 |
| Spatial-MLLM | direct | sat | t4 | world/intervention_001/oracle | oracle | 19.0 | 38 | 200 | 200 | 0 |
| Spatial-MLLM | direct | sat | t4 | world/sham_001/direct | direct | 21.0 | 42 | 200 | 200 | 0 |
| Spatial-MLLM | direct | sat | t4 | world/sham_001/oracle | oracle | 22.5 | 45 | 200 | 200 | 0 |
| Spatial-MLLM | direct | webrd04 | t1 | base/direct | direct | 48.2 | 193 | 400 | 400 | 0 |
| Spatial-MLLM | direct | webrd04 | t1 | base/oracle | oracle | 47.2 | 189 | 400 | 400 | 0 |
| Spatial-MLLM | direct | webrd04 | t2 | base/direct | direct | 51.0 | 204 | 400 | 400 | 0 |
| Spatial-MLLM | direct | webrd04 | t2 | base/oracle | oracle | 50.2 | 201 | 400 | 400 | 0 |
| Spatial-MLLM | direct | webrd04 | t3 | base/direct | direct | 19.5 | 39 | 200 | 200 | 0 |
| Spatial-MLLM | direct | webrd04 | t3 | base/oracle | oracle | 20.5 | 41 | 200 | 200 | 0 |
| Spatial-MLLM | direct | webrd04 | t3 | world/intervention_001/direct | direct | 44.0 | 88 | 200 | 200 | 0 |
| Spatial-MLLM | direct | webrd04 | t3 | world/intervention_001/oracle | oracle | 46.0 | 92 | 200 | 200 | 0 |
| Spatial-MLLM | direct | webrd04 | t3 | world/sham_001/direct | direct | 12.0 | 24 | 200 | 200 | 0 |
| Spatial-MLLM | direct | webrd04 | t3 | world/sham_001/oracle | oracle | 14.0 | 28 | 200 | 200 | 0 |
| Spatial-MLLM | direct | webrd04 | t4 | base/direct | direct | 25.8 | 103 | 400 | 400 | 0 |
| Spatial-MLLM | direct | webrd04 | t4 | base/oracle | oracle | 25.5 | 102 | 400 | 400 | 0 |
| Spatial-MLLM | direct | webrd04 | t4 | world/intervention_001/direct | direct | 21.0 | 42 | 200 | 200 | 0 |
| Spatial-MLLM | direct | webrd04 | t4 | world/intervention_001/oracle | oracle | 22.0 | 44 | 200 | 200 | 0 |
| Spatial-MLLM | direct | webrd04 | t4 | world/sham_001/direct | direct | 18.5 | 37 | 200 | 200 | 0 |
| Spatial-MLLM | direct | webrd04 | t4 | world/sham_001/oracle | oracle | 21.5 | 43 | 200 | 200 | 0 |
| Spatial-MLLM | direct | wprd01 | t1 | base/direct | direct | 48.5 | 194 | 400 | 400 | 0 |
| Spatial-MLLM | direct | wprd01 | t1 | base/oracle | oracle | 48.8 | 195 | 400 | 400 | 0 |
| Spatial-MLLM | direct | wprd01 | t1 | transform/mirror_h/direct | direct | 42.0 | 168 | 400 | 400 | 0 |
| Spatial-MLLM | direct | wprd01 | t1 | transform/mirror_h/oracle | oracle | 42.8 | 171 | 400 | 400 | 0 |
| Spatial-MLLM | direct | wprd01 | t1 | transform/mirror_h_rot180/direct | direct | 42.5 | 170 | 400 | 400 | 0 |
| Spatial-MLLM | direct | wprd01 | t1 | transform/mirror_h_rot180/oracle | oracle | 42.8 | 171 | 400 | 400 | 0 |
| Spatial-MLLM | direct | wprd01 | t1 | transform/mirror_h_rot270/direct | direct | 38.8 | 155 | 400 | 400 | 0 |
| Spatial-MLLM | direct | wprd01 | t1 | transform/mirror_h_rot270/oracle | oracle | 42.0 | 168 | 400 | 400 | 0 |
| Spatial-MLLM | direct | wprd01 | t1 | transform/mirror_h_rot90/direct | direct | 47.8 | 191 | 400 | 400 | 0 |
| Spatial-MLLM | direct | wprd01 | t1 | transform/mirror_h_rot90/oracle | oracle | 46.2 | 185 | 400 | 400 | 0 |
| Spatial-MLLM | direct | wprd01 | t1 | transform/rot180/direct | direct | 46.5 | 186 | 400 | 400 | 0 |
| Spatial-MLLM | direct | wprd01 | t1 | transform/rot180/oracle | oracle | 46.0 | 184 | 400 | 400 | 0 |
| Spatial-MLLM | direct | wprd01 | t1 | transform/rot270/direct | direct | 45.8 | 183 | 400 | 400 | 0 |
| Spatial-MLLM | direct | wprd01 | t1 | transform/rot270/oracle | oracle | 46.0 | 184 | 400 | 400 | 0 |
| Spatial-MLLM | direct | wprd01 | t1 | transform/rot90/direct | direct | 47.5 | 190 | 400 | 400 | 0 |
| Spatial-MLLM | direct | wprd01 | t1 | transform/rot90/oracle | oracle | 47.2 | 189 | 400 | 400 | 0 |
| Spatial-MLLM | direct | wprd01 | t2 | base/direct | direct | 50.8 | 203 | 400 | 400 | 0 |
| Spatial-MLLM | direct | wprd01 | t2 | base/oracle | oracle | 54.0 | 216 | 400 | 400 | 0 |
| Spatial-MLLM | direct | wprd01 | t2 | transform/mirror_h/direct | direct | 51.8 | 207 | 400 | 400 | 0 |
| Spatial-MLLM | direct | wprd01 | t2 | transform/mirror_h/oracle | oracle | 52.8 | 211 | 400 | 400 | 0 |
| Spatial-MLLM | direct | wprd01 | t2 | transform/mirror_h_rot180/direct | direct | 49.5 | 198 | 400 | 400 | 0 |
| Spatial-MLLM | direct | wprd01 | t2 | transform/mirror_h_rot180/oracle | oracle | 47.8 | 191 | 400 | 400 | 0 |
| Spatial-MLLM | direct | wprd01 | t2 | transform/mirror_h_rot270/direct | direct | 51.2 | 205 | 400 | 400 | 0 |
| Spatial-MLLM | direct | wprd01 | t2 | transform/mirror_h_rot270/oracle | oracle | 48.8 | 195 | 400 | 400 | 0 |
| Spatial-MLLM | direct | wprd01 | t2 | transform/mirror_h_rot90/direct | direct | 50.5 | 202 | 400 | 400 | 0 |
| Spatial-MLLM | direct | wprd01 | t2 | transform/mirror_h_rot90/oracle | oracle | 53.5 | 214 | 400 | 400 | 0 |
| Spatial-MLLM | direct | wprd01 | t2 | transform/rot180/direct | direct | 52.8 | 211 | 400 | 400 | 0 |
| Spatial-MLLM | direct | wprd01 | t2 | transform/rot180/oracle | oracle | 51.8 | 207 | 400 | 400 | 0 |
| Spatial-MLLM | direct | wprd01 | t2 | transform/rot270/direct | direct | 49.8 | 199 | 400 | 400 | 0 |
| Spatial-MLLM | direct | wprd01 | t2 | transform/rot270/oracle | oracle | 51.2 | 205 | 400 | 400 | 0 |
| Spatial-MLLM | direct | wprd01 | t2 | transform/rot90/direct | direct | 52.8 | 211 | 400 | 400 | 0 |
| Spatial-MLLM | direct | wprd01 | t2 | transform/rot90/oracle | oracle | 50.8 | 203 | 400 | 400 | 0 |
| Spatial-MLLM | direct | wprd01 | t3 | base/direct | direct | 24.0 | 48 | 200 | 200 | 0 |
| Spatial-MLLM | direct | wprd01 | t3 | base/oracle | oracle | 21.5 | 43 | 200 | 200 | 0 |
| Spatial-MLLM | direct | wprd01 | t3 | transform/mirror_h/direct | direct | 24.0 | 48 | 200 | 200 | 0 |
| Spatial-MLLM | direct | wprd01 | t3 | transform/mirror_h/oracle | oracle | 25.5 | 51 | 200 | 200 | 0 |
| Spatial-MLLM | direct | wprd01 | t3 | transform/mirror_h_rot180/direct | direct | 24.5 | 49 | 200 | 200 | 0 |
| Spatial-MLLM | direct | wprd01 | t3 | transform/mirror_h_rot180/oracle | oracle | 29.0 | 58 | 200 | 200 | 0 |
| Spatial-MLLM | direct | wprd01 | t3 | transform/mirror_h_rot270/direct | direct | 26.0 | 52 | 200 | 200 | 0 |
| Spatial-MLLM | direct | wprd01 | t3 | transform/mirror_h_rot270/oracle | oracle | 26.0 | 52 | 200 | 200 | 0 |
| Spatial-MLLM | direct | wprd01 | t3 | transform/mirror_h_rot90/direct | direct | 24.5 | 49 | 200 | 200 | 0 |
| Spatial-MLLM | direct | wprd01 | t3 | transform/mirror_h_rot90/oracle | oracle | 24.5 | 49 | 200 | 200 | 0 |
| Spatial-MLLM | direct | wprd01 | t3 | transform/rot180/direct | direct | 23.0 | 46 | 200 | 200 | 0 |
| Spatial-MLLM | direct | wprd01 | t3 | transform/rot180/oracle | oracle | 24.0 | 48 | 200 | 200 | 0 |
| Spatial-MLLM | direct | wprd01 | t3 | transform/rot270/direct | direct | 25.5 | 51 | 200 | 200 | 0 |
| Spatial-MLLM | direct | wprd01 | t3 | transform/rot270/oracle | oracle | 28.0 | 56 | 200 | 200 | 0 |
| Spatial-MLLM | direct | wprd01 | t3 | transform/rot90/direct | direct | 24.0 | 48 | 200 | 200 | 0 |
| Spatial-MLLM | direct | wprd01 | t3 | transform/rot90/oracle | oracle | 24.5 | 49 | 200 | 200 | 0 |
| Spatial-MLLM | direct | wprd01 | t3 | world/intervention_001/direct | direct | 33.0 | 66 | 200 | 200 | 0 |
| Spatial-MLLM | direct | wprd01 | t3 | world/intervention_001/oracle | oracle | 34.5 | 69 | 200 | 200 | 0 |
| Spatial-MLLM | direct | wprd01 | t3 | world/sham_001/direct | direct | 19.0 | 38 | 200 | 200 | 0 |
| Spatial-MLLM | direct | wprd01 | t3 | world/sham_001/oracle | oracle | 24.5 | 49 | 200 | 200 | 0 |
| Spatial-MLLM | direct | wprd01 | t4 | base/direct | direct | 26.5 | 106 | 400 | 400 | 0 |
| Spatial-MLLM | direct | wprd01 | t4 | base/oracle | oracle | 30.8 | 123 | 400 | 400 | 0 |
| Spatial-MLLM | direct | wprd01 | t4 | transform/mirror_h/direct | direct | 28.8 | 115 | 400 | 400 | 0 |
| Spatial-MLLM | direct | wprd01 | t4 | transform/mirror_h/oracle | oracle | 31.5 | 126 | 400 | 400 | 0 |
| Spatial-MLLM | direct | wprd01 | t4 | transform/mirror_h_rot180/direct | direct | 26.0 | 104 | 400 | 400 | 0 |
| Spatial-MLLM | direct | wprd01 | t4 | transform/mirror_h_rot180/oracle | oracle | 26.0 | 104 | 400 | 400 | 0 |
| Spatial-MLLM | direct | wprd01 | t4 | transform/mirror_h_rot270/direct | direct | 29.2 | 117 | 400 | 400 | 0 |
| Spatial-MLLM | direct | wprd01 | t4 | transform/mirror_h_rot270/oracle | oracle | 27.8 | 111 | 400 | 400 | 0 |
| Spatial-MLLM | direct | wprd01 | t4 | transform/mirror_h_rot90/direct | direct | 28.8 | 115 | 400 | 400 | 0 |
| Spatial-MLLM | direct | wprd01 | t4 | transform/mirror_h_rot90/oracle | oracle | 28.2 | 113 | 400 | 400 | 0 |
| Spatial-MLLM | direct | wprd01 | t4 | transform/rot180/direct | direct | 29.5 | 118 | 400 | 400 | 0 |
| Spatial-MLLM | direct | wprd01 | t4 | transform/rot180/oracle | oracle | 30.2 | 121 | 400 | 400 | 0 |
| Spatial-MLLM | direct | wprd01 | t4 | transform/rot270/direct | direct | 27.5 | 110 | 400 | 400 | 0 |
| Spatial-MLLM | direct | wprd01 | t4 | transform/rot270/oracle | oracle | 26.8 | 107 | 400 | 400 | 0 |
| Spatial-MLLM | direct | wprd01 | t4 | transform/rot90/direct | direct | 31.0 | 124 | 400 | 400 | 0 |
| Spatial-MLLM | direct | wprd01 | t4 | transform/rot90/oracle | oracle | 28.8 | 115 | 400 | 400 | 0 |
| Spatial-MLLM | direct | wprd01 | t4 | world/intervention_001/direct | direct | 21.5 | 43 | 200 | 200 | 0 |
| Spatial-MLLM | direct | wprd01 | t4 | world/intervention_001/oracle | oracle | 20.0 | 40 | 200 | 200 | 0 |
| Spatial-MLLM | direct | wprd01 | t4 | world/sham_001/direct | direct | 20.0 | 40 | 200 | 200 | 0 |
| Spatial-MLLM | direct | wprd01 | t4 | world/sham_001/oracle | oracle | 19.0 | 38 | 200 | 200 | 0 |
| InternVL3_5-8B | direct | blank | t1 | base/direct | direct | 78.0 | 312 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | blank | t1 | base/oracle | oracle | 79.8 | 319 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | blank | t1 | transform/mirror_h/direct | direct | 29.0 | 116 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | blank | t1 | transform/mirror_h/oracle | oracle | 33.0 | 132 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | blank | t1 | transform/mirror_h_rot180/direct | direct | 30.2 | 121 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | blank | t1 | transform/mirror_h_rot180/oracle | oracle | 34.0 | 136 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | blank | t1 | transform/mirror_h_rot270/direct | direct | 39.2 | 157 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | blank | t1 | transform/mirror_h_rot270/oracle | oracle | 41.2 | 165 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | blank | t1 | transform/mirror_h_rot90/direct | direct | 43.8 | 175 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | blank | t1 | transform/mirror_h_rot90/oracle | oracle | 53.8 | 215 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | blank | t1 | transform/rot180/direct | direct | 56.5 | 226 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | blank | t1 | transform/rot180/oracle | oracle | 61.8 | 247 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | blank | t1 | transform/rot270/direct | direct | 53.8 | 215 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | blank | t1 | transform/rot270/oracle | oracle | 58.5 | 234 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | blank | t1 | transform/rot90/direct | direct | 55.5 | 222 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | blank | t1 | transform/rot90/oracle | oracle | 57.8 | 231 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | blank | t2 | base/direct | direct | 45.2 | 181 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | blank | t2 | base/oracle | oracle | 50.2 | 201 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | blank | t2 | transform/mirror_h/direct | direct | 46.8 | 187 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | blank | t2 | transform/mirror_h/oracle | oracle | 50.8 | 203 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | blank | t2 | transform/mirror_h_rot180/direct | direct | 49.5 | 198 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | blank | t2 | transform/mirror_h_rot180/oracle | oracle | 52.0 | 208 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | blank | t2 | transform/mirror_h_rot270/direct | direct | 51.0 | 204 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | blank | t2 | transform/mirror_h_rot270/oracle | oracle | 52.5 | 210 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | blank | t2 | transform/mirror_h_rot90/direct | direct | 51.2 | 205 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | blank | t2 | transform/mirror_h_rot90/oracle | oracle | 50.2 | 201 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | blank | t2 | transform/rot180/direct | direct | 49.8 | 199 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | blank | t2 | transform/rot180/oracle | oracle | 52.8 | 211 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | blank | t2 | transform/rot270/direct | direct | 46.0 | 184 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | blank | t2 | transform/rot270/oracle | oracle | 51.0 | 204 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | blank | t2 | transform/rot90/direct | direct | 46.0 | 184 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | blank | t2 | transform/rot90/oracle | oracle | 52.2 | 209 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | sat | t1 | base/direct | direct | 63.2 | 253 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | sat | t1 | base/oracle | oracle | 64.5 | 258 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | sat | t1 | transform/mirror_h/direct | direct | 34.8 | 139 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | sat | t1 | transform/mirror_h/oracle | oracle | 44.2 | 177 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | sat | t1 | transform/mirror_h_rot180/direct | direct | 38.0 | 152 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | sat | t1 | transform/mirror_h_rot180/oracle | oracle | 45.5 | 182 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | sat | t1 | transform/mirror_h_rot270/direct | direct | 34.0 | 136 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | sat | t1 | transform/mirror_h_rot270/oracle | oracle | 42.8 | 171 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | sat | t1 | transform/mirror_h_rot90/direct | direct | 34.5 | 138 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | sat | t1 | transform/mirror_h_rot90/oracle | oracle | 48.5 | 194 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | sat | t1 | transform/rot180/direct | direct | 58.5 | 234 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | sat | t1 | transform/rot180/oracle | oracle | 66.5 | 266 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | sat | t1 | transform/rot270/direct | direct | 54.8 | 219 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | sat | t1 | transform/rot270/oracle | oracle | 65.8 | 263 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | sat | t1 | transform/rot90/direct | direct | 61.5 | 246 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | sat | t1 | transform/rot90/oracle | oracle | 69.5 | 278 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | sat | t2 | base/direct | direct | 38.0 | 152 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | sat | t2 | base/oracle | oracle | 49.0 | 196 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | sat | t2 | transform/mirror_h/direct | direct | 45.5 | 182 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | sat | t2 | transform/mirror_h/oracle | oracle | 43.2 | 173 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | sat | t2 | transform/mirror_h_rot180/direct | direct | 44.8 | 179 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | sat | t2 | transform/mirror_h_rot180/oracle | oracle | 41.2 | 165 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | sat | t2 | transform/mirror_h_rot270/direct | direct | 48.5 | 194 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | sat | t2 | transform/mirror_h_rot270/oracle | oracle | 45.8 | 183 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | sat | t2 | transform/mirror_h_rot90/direct | direct | 44.8 | 179 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | sat | t2 | transform/mirror_h_rot90/oracle | oracle | 43.5 | 174 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | sat | t2 | transform/rot180/direct | direct | 46.8 | 187 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | sat | t2 | transform/rot180/oracle | oracle | 44.0 | 176 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | sat | t2 | transform/rot270/direct | direct | 43.8 | 175 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | sat | t2 | transform/rot270/oracle | oracle | 42.8 | 171 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | sat | t2 | transform/rot90/direct | direct | 43.2 | 173 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | sat | t2 | transform/rot90/oracle | oracle | 45.8 | 183 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | sat | t3 | base/direct | direct | 26.5 | 53 | 200 | 200 | 0 |
| InternVL3_5-8B | direct | sat | t3 | base/oracle | oracle | 33.0 | 66 | 200 | 200 | 0 |
| InternVL3_5-8B | direct | sat | t3 | transform/mirror_h/direct | direct | 27.0 | 54 | 200 | 200 | 0 |
| InternVL3_5-8B | direct | sat | t3 | transform/mirror_h/oracle | oracle | 32.0 | 64 | 200 | 200 | 0 |
| InternVL3_5-8B | direct | sat | t3 | transform/mirror_h_rot180/direct | direct | 26.0 | 52 | 200 | 200 | 0 |
| InternVL3_5-8B | direct | sat | t3 | transform/mirror_h_rot180/oracle | oracle | 33.5 | 67 | 200 | 200 | 0 |
| InternVL3_5-8B | direct | sat | t3 | transform/mirror_h_rot270/direct | direct | 27.5 | 55 | 200 | 200 | 0 |
| InternVL3_5-8B | direct | sat | t3 | transform/mirror_h_rot270/oracle | oracle | 31.0 | 62 | 200 | 200 | 0 |
| InternVL3_5-8B | direct | sat | t3 | transform/mirror_h_rot90/direct | direct | 26.5 | 53 | 200 | 200 | 0 |
| InternVL3_5-8B | direct | sat | t3 | transform/mirror_h_rot90/oracle | oracle | 28.0 | 56 | 200 | 200 | 0 |
| InternVL3_5-8B | direct | sat | t3 | transform/rot180/direct | direct | 30.0 | 60 | 200 | 200 | 0 |
| InternVL3_5-8B | direct | sat | t3 | transform/rot180/oracle | oracle | 30.0 | 60 | 200 | 200 | 0 |
| InternVL3_5-8B | direct | sat | t3 | transform/rot270/direct | direct | 26.0 | 52 | 200 | 200 | 0 |
| InternVL3_5-8B | direct | sat | t3 | transform/rot270/oracle | oracle | 33.0 | 66 | 200 | 200 | 0 |
| InternVL3_5-8B | direct | sat | t3 | transform/rot90/direct | direct | 30.0 | 60 | 200 | 200 | 0 |
| InternVL3_5-8B | direct | sat | t3 | transform/rot90/oracle | oracle | 32.5 | 65 | 200 | 200 | 0 |
| InternVL3_5-8B | direct | sat | t3 | world/intervention_001/direct | direct | 38.5 | 77 | 200 | 200 | 0 |
| InternVL3_5-8B | direct | sat | t3 | world/intervention_001/oracle | oracle | 36.0 | 72 | 200 | 200 | 0 |
| InternVL3_5-8B | direct | sat | t3 | world/sham_001/direct | direct | 25.0 | 50 | 200 | 200 | 0 |
| InternVL3_5-8B | direct | sat | t3 | world/sham_001/oracle | oracle | 29.5 | 59 | 200 | 200 | 0 |
| InternVL3_5-8B | direct | sat | t4 | base/direct | direct | 32.5 | 130 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | sat | t4 | base/oracle | oracle | 37.2 | 149 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | sat | t4 | transform/mirror_h/direct | direct | 36.2 | 145 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | sat | t4 | transform/mirror_h/oracle | oracle | 37.8 | 151 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | sat | t4 | transform/mirror_h_rot180/direct | direct | 31.2 | 125 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | sat | t4 | transform/mirror_h_rot180/oracle | oracle | 35.8 | 143 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | sat | t4 | transform/mirror_h_rot270/direct | direct | 31.2 | 125 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | sat | t4 | transform/mirror_h_rot270/oracle | oracle | 38.8 | 155 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | sat | t4 | transform/mirror_h_rot90/direct | direct | 32.2 | 129 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | sat | t4 | transform/mirror_h_rot90/oracle | oracle | 36.8 | 147 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | sat | t4 | transform/rot180/direct | direct | 32.8 | 131 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | sat | t4 | transform/rot180/oracle | oracle | 38.8 | 155 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | sat | t4 | transform/rot270/direct | direct | 35.5 | 142 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | sat | t4 | transform/rot270/oracle | oracle | 34.5 | 138 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | sat | t4 | transform/rot90/direct | direct | 32.5 | 130 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | sat | t4 | transform/rot90/oracle | oracle | 37.2 | 149 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | sat | t4 | world/intervention_001/direct | direct | 12.5 | 25 | 200 | 200 | 0 |
| InternVL3_5-8B | direct | sat | t4 | world/intervention_001/oracle | oracle | 23.5 | 47 | 200 | 200 | 0 |
| InternVL3_5-8B | direct | sat | t4 | world/sham_001/direct | direct | 27.0 | 54 | 200 | 200 | 0 |
| InternVL3_5-8B | direct | sat | t4 | world/sham_001/oracle | oracle | 32.0 | 64 | 200 | 200 | 0 |
| InternVL3_5-8B | direct | webrd04 | t1 | base/direct | direct | 51.5 | 206 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | webrd04 | t1 | base/oracle | oracle | 70.5 | 282 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | webrd04 | t2 | base/direct | direct | 41.8 | 167 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | webrd04 | t2 | base/oracle | oracle | 42.5 | 170 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | webrd04 | t3 | base/direct | direct | 34.5 | 69 | 200 | 200 | 0 |
| InternVL3_5-8B | direct | webrd04 | t3 | base/oracle | oracle | 39.0 | 78 | 200 | 200 | 0 |
| InternVL3_5-8B | direct | webrd04 | t3 | world/intervention_001/direct | direct | 40.0 | 80 | 200 | 200 | 0 |
| InternVL3_5-8B | direct | webrd04 | t3 | world/intervention_001/oracle | oracle | 38.0 | 76 | 200 | 200 | 0 |
| InternVL3_5-8B | direct | webrd04 | t3 | world/sham_001/direct | direct | 34.5 | 69 | 200 | 200 | 0 |
| InternVL3_5-8B | direct | webrd04 | t3 | world/sham_001/oracle | oracle | 34.0 | 68 | 200 | 200 | 0 |
| InternVL3_5-8B | direct | webrd04 | t4 | base/direct | direct | 33.2 | 133 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | webrd04 | t4 | base/oracle | oracle | 37.2 | 149 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | webrd04 | t4 | world/intervention_001/direct | direct | 22.0 | 44 | 200 | 200 | 0 |
| InternVL3_5-8B | direct | webrd04 | t4 | world/intervention_001/oracle | oracle | 27.5 | 55 | 200 | 200 | 0 |
| InternVL3_5-8B | direct | webrd04 | t4 | world/sham_001/direct | direct | 24.5 | 49 | 200 | 200 | 0 |
| InternVL3_5-8B | direct | webrd04 | t4 | world/sham_001/oracle | oracle | 30.5 | 61 | 200 | 200 | 0 |
| InternVL3_5-8B | direct | wprd01 | t1 | base/direct | direct | 58.0 | 232 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | wprd01 | t1 | base/oracle | oracle | 64.0 | 256 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | wprd01 | t1 | transform/mirror_h/direct | direct | 37.2 | 149 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | wprd01 | t1 | transform/mirror_h/oracle | oracle | 47.5 | 190 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | wprd01 | t1 | transform/mirror_h_rot180/direct | direct | 32.8 | 131 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | wprd01 | t1 | transform/mirror_h_rot180/oracle | oracle | 43.8 | 175 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | wprd01 | t1 | transform/mirror_h_rot270/direct | direct | 36.2 | 145 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | wprd01 | t1 | transform/mirror_h_rot270/oracle | oracle | 46.8 | 187 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | wprd01 | t1 | transform/mirror_h_rot90/direct | direct | 33.5 | 134 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | wprd01 | t1 | transform/mirror_h_rot90/oracle | oracle | 47.2 | 189 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | wprd01 | t1 | transform/rot180/direct | direct | 51.8 | 207 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | wprd01 | t1 | transform/rot180/oracle | oracle | 63.8 | 255 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | wprd01 | t1 | transform/rot270/direct | direct | 52.5 | 210 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | wprd01 | t1 | transform/rot270/oracle | oracle | 61.8 | 247 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | wprd01 | t1 | transform/rot90/direct | direct | 58.8 | 235 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | wprd01 | t1 | transform/rot90/oracle | oracle | 67.0 | 268 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | wprd01 | t2 | base/direct | direct | 44.2 | 177 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | wprd01 | t2 | base/oracle | oracle | 44.0 | 176 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | wprd01 | t2 | transform/mirror_h/direct | direct | 41.8 | 167 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | wprd01 | t2 | transform/mirror_h/oracle | oracle | 38.5 | 154 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | wprd01 | t2 | transform/mirror_h_rot180/direct | direct | 39.5 | 158 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | wprd01 | t2 | transform/mirror_h_rot180/oracle | oracle | 37.8 | 151 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | wprd01 | t2 | transform/mirror_h_rot270/direct | direct | 37.5 | 150 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | wprd01 | t2 | transform/mirror_h_rot270/oracle | oracle | 33.5 | 134 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | wprd01 | t2 | transform/mirror_h_rot90/direct | direct | 35.5 | 142 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | wprd01 | t2 | transform/mirror_h_rot90/oracle | oracle | 36.2 | 145 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | wprd01 | t2 | transform/rot180/direct | direct | 43.2 | 173 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | wprd01 | t2 | transform/rot180/oracle | oracle | 39.5 | 158 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | wprd01 | t2 | transform/rot270/direct | direct | 36.0 | 144 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | wprd01 | t2 | transform/rot270/oracle | oracle | 32.2 | 129 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | wprd01 | t2 | transform/rot90/direct | direct | 41.5 | 166 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | wprd01 | t2 | transform/rot90/oracle | oracle | 37.0 | 148 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | wprd01 | t3 | base/direct | direct | 21.5 | 43 | 200 | 200 | 0 |
| InternVL3_5-8B | direct | wprd01 | t3 | base/oracle | oracle | 26.5 | 53 | 200 | 200 | 0 |
| InternVL3_5-8B | direct | wprd01 | t3 | transform/mirror_h/direct | direct | 23.0 | 46 | 200 | 200 | 0 |
| InternVL3_5-8B | direct | wprd01 | t3 | transform/mirror_h/oracle | oracle | 23.0 | 46 | 200 | 200 | 0 |
| InternVL3_5-8B | direct | wprd01 | t3 | transform/mirror_h_rot180/direct | direct | 24.5 | 49 | 200 | 200 | 0 |
| InternVL3_5-8B | direct | wprd01 | t3 | transform/mirror_h_rot180/oracle | oracle | 25.5 | 51 | 200 | 200 | 0 |
| InternVL3_5-8B | direct | wprd01 | t3 | transform/mirror_h_rot270/direct | direct | 22.5 | 45 | 200 | 200 | 0 |
| InternVL3_5-8B | direct | wprd01 | t3 | transform/mirror_h_rot270/oracle | oracle | 24.0 | 48 | 200 | 200 | 0 |
| InternVL3_5-8B | direct | wprd01 | t3 | transform/mirror_h_rot90/direct | direct | 25.0 | 50 | 200 | 200 | 0 |
| InternVL3_5-8B | direct | wprd01 | t3 | transform/mirror_h_rot90/oracle | oracle | 25.0 | 50 | 200 | 200 | 0 |
| InternVL3_5-8B | direct | wprd01 | t3 | transform/rot180/direct | direct | 23.0 | 46 | 200 | 200 | 0 |
| InternVL3_5-8B | direct | wprd01 | t3 | transform/rot180/oracle | oracle | 24.5 | 49 | 200 | 200 | 0 |
| InternVL3_5-8B | direct | wprd01 | t3 | transform/rot270/direct | direct | 26.0 | 52 | 200 | 200 | 0 |
| InternVL3_5-8B | direct | wprd01 | t3 | transform/rot270/oracle | oracle | 22.5 | 45 | 200 | 200 | 0 |
| InternVL3_5-8B | direct | wprd01 | t3 | transform/rot90/direct | direct | 25.0 | 50 | 200 | 200 | 0 |
| InternVL3_5-8B | direct | wprd01 | t3 | transform/rot90/oracle | oracle | 24.0 | 48 | 200 | 200 | 0 |
| InternVL3_5-8B | direct | wprd01 | t3 | world/intervention_001/direct | direct | 22.5 | 45 | 200 | 200 | 0 |
| InternVL3_5-8B | direct | wprd01 | t3 | world/intervention_001/oracle | oracle | 22.0 | 44 | 200 | 200 | 0 |
| InternVL3_5-8B | direct | wprd01 | t3 | world/sham_001/direct | direct | 22.5 | 45 | 200 | 200 | 0 |
| InternVL3_5-8B | direct | wprd01 | t3 | world/sham_001/oracle | oracle | 23.5 | 47 | 200 | 200 | 0 |
| InternVL3_5-8B | direct | wprd01 | t4 | base/direct | direct | 27.5 | 110 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | wprd01 | t4 | base/oracle | oracle | 29.2 | 117 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | wprd01 | t4 | transform/mirror_h/direct | direct | 26.2 | 105 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | wprd01 | t4 | transform/mirror_h/oracle | oracle | 27.2 | 109 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | wprd01 | t4 | transform/mirror_h_rot180/direct | direct | 27.5 | 110 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | wprd01 | t4 | transform/mirror_h_rot180/oracle | oracle | 31.0 | 124 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | wprd01 | t4 | transform/mirror_h_rot270/direct | direct | 27.5 | 110 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | wprd01 | t4 | transform/mirror_h_rot270/oracle | oracle | 30.8 | 123 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | wprd01 | t4 | transform/mirror_h_rot90/direct | direct | 28.0 | 112 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | wprd01 | t4 | transform/mirror_h_rot90/oracle | oracle | 29.8 | 119 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | wprd01 | t4 | transform/rot180/direct | direct | 23.8 | 95 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | wprd01 | t4 | transform/rot180/oracle | oracle | 30.5 | 122 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | wprd01 | t4 | transform/rot270/direct | direct | 29.8 | 119 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | wprd01 | t4 | transform/rot270/oracle | oracle | 31.0 | 124 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | wprd01 | t4 | transform/rot90/direct | direct | 28.0 | 112 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | wprd01 | t4 | transform/rot90/oracle | oracle | 29.0 | 116 | 400 | 400 | 0 |
| InternVL3_5-8B | direct | wprd01 | t4 | world/intervention_001/direct | direct | 5.5 | 11 | 200 | 200 | 0 |
| InternVL3_5-8B | direct | wprd01 | t4 | world/intervention_001/oracle | oracle | 11.5 | 23 | 200 | 200 | 0 |
| InternVL3_5-8B | direct | wprd01 | t4 | world/sham_001/direct | direct | 9.0 | 18 | 200 | 200 | 0 |
| InternVL3_5-8B | direct | wprd01 | t4 | world/sham_001/oracle | oracle | 10.5 | 21 | 200 | 200 | 0 |
| SenseNova-U1-8B-MoT | direct | blank | t1 | base/direct | direct | 62.0 | 248 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | blank | t1 | base/oracle | oracle | 60.0 | 240 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | blank | t1 | transform/mirror_h/direct | direct | 53.8 | 215 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | blank | t1 | transform/mirror_h/oracle | oracle | 42.8 | 171 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | blank | t1 | transform/mirror_h_rot180/direct | direct | 51.2 | 205 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | blank | t1 | transform/mirror_h_rot180/oracle | oracle | 47.8 | 191 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | blank | t1 | transform/mirror_h_rot270/direct | direct | 46.0 | 184 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | blank | t1 | transform/mirror_h_rot270/oracle | oracle | 40.8 | 163 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | blank | t1 | transform/mirror_h_rot90/direct | direct | 52.8 | 211 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | blank | t1 | transform/mirror_h_rot90/oracle | oracle | 43.2 | 173 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | blank | t1 | transform/rot180/direct | direct | 59.5 | 238 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | blank | t1 | transform/rot180/oracle | oracle | 64.8 | 259 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | blank | t1 | transform/rot270/direct | direct | 65.8 | 263 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | blank | t1 | transform/rot270/oracle | oracle | 68.0 | 272 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | blank | t1 | transform/rot90/direct | direct | 57.8 | 231 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | blank | t1 | transform/rot90/oracle | oracle | 63.5 | 254 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | blank | t2 | base/direct | direct | 47.2 | 189 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | blank | t2 | base/oracle | oracle | 47.8 | 191 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | blank | t2 | transform/mirror_h/direct | direct | 51.5 | 206 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | blank | t2 | transform/mirror_h/oracle | oracle | 48.5 | 194 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | blank | t2 | transform/mirror_h_rot180/direct | direct | 46.8 | 187 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | blank | t2 | transform/mirror_h_rot180/oracle | oracle | 43.5 | 174 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | blank | t2 | transform/mirror_h_rot270/direct | direct | 48.0 | 192 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | blank | t2 | transform/mirror_h_rot270/oracle | oracle | 48.2 | 193 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | blank | t2 | transform/mirror_h_rot90/direct | direct | 52.0 | 208 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | blank | t2 | transform/mirror_h_rot90/oracle | oracle | 48.2 | 193 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | blank | t2 | transform/rot180/direct | direct | 46.2 | 185 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | blank | t2 | transform/rot180/oracle | oracle | 45.2 | 181 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | blank | t2 | transform/rot270/direct | direct | 51.0 | 204 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | blank | t2 | transform/rot270/oracle | oracle | 47.5 | 190 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | blank | t2 | transform/rot90/direct | direct | 49.8 | 199 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | blank | t2 | transform/rot90/oracle | oracle | 49.8 | 199 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | sat | t1 | base/direct | direct | 55.0 | 220 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | sat | t1 | base/oracle | oracle | 56.5 | 226 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | sat | t1 | transform/mirror_h/direct | direct | 35.8 | 143 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | sat | t1 | transform/mirror_h/oracle | oracle | 36.8 | 147 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | sat | t1 | transform/mirror_h_rot180/direct | direct | 36.5 | 146 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | sat | t1 | transform/mirror_h_rot180/oracle | oracle | 37.5 | 150 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | sat | t1 | transform/mirror_h_rot270/direct | direct | 35.2 | 141 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | sat | t1 | transform/mirror_h_rot270/oracle | oracle | 36.2 | 145 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | sat | t1 | transform/mirror_h_rot90/direct | direct | 33.5 | 134 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | sat | t1 | transform/mirror_h_rot90/oracle | oracle | 35.2 | 141 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | sat | t1 | transform/rot180/direct | direct | 52.2 | 209 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | sat | t1 | transform/rot180/oracle | oracle | 58.0 | 232 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | sat | t1 | transform/rot270/direct | direct | 59.5 | 238 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | sat | t1 | transform/rot270/oracle | oracle | 59.2 | 237 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | sat | t1 | transform/rot90/direct | direct | 51.0 | 204 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | sat | t1 | transform/rot90/oracle | oracle | 55.8 | 223 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | sat | t2 | base/direct | direct | 49.2 | 197 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | sat | t2 | base/oracle | oracle | 41.0 | 164 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | sat | t2 | transform/mirror_h/direct | direct | 46.8 | 187 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | sat | t2 | transform/mirror_h/oracle | oracle | 43.2 | 173 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | sat | t2 | transform/mirror_h_rot180/direct | direct | 45.5 | 182 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | sat | t2 | transform/mirror_h_rot180/oracle | oracle | 38.8 | 155 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | sat | t2 | transform/mirror_h_rot270/direct | direct | 47.0 | 188 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | sat | t2 | transform/mirror_h_rot270/oracle | oracle | 39.5 | 158 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | sat | t2 | transform/mirror_h_rot90/direct | direct | 50.0 | 200 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | sat | t2 | transform/mirror_h_rot90/oracle | oracle | 47.5 | 190 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | sat | t2 | transform/rot180/direct | direct | 46.8 | 187 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | sat | t2 | transform/rot180/oracle | oracle | 42.0 | 168 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | sat | t2 | transform/rot270/direct | direct | 46.8 | 187 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | sat | t2 | transform/rot270/oracle | oracle | 44.5 | 178 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | sat | t2 | transform/rot90/direct | direct | 47.0 | 188 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | sat | t2 | transform/rot90/oracle | oracle | 43.5 | 174 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | sat | t3 | base/direct | direct | 13.5 | 27 | 200 | 200 | 0 |
| SenseNova-U1-8B-MoT | direct | sat | t3 | base/oracle | oracle | 18.0 | 36 | 200 | 200 | 0 |
| SenseNova-U1-8B-MoT | direct | sat | t3 | transform/mirror_h/direct | direct | 10.5 | 21 | 200 | 200 | 0 |
| SenseNova-U1-8B-MoT | direct | sat | t3 | transform/mirror_h/oracle | oracle | 12.5 | 25 | 200 | 200 | 0 |
| SenseNova-U1-8B-MoT | direct | sat | t3 | transform/mirror_h_rot180/direct | direct | 14.5 | 29 | 200 | 200 | 0 |
| SenseNova-U1-8B-MoT | direct | sat | t3 | transform/mirror_h_rot180/oracle | oracle | 17.5 | 35 | 200 | 200 | 0 |
| SenseNova-U1-8B-MoT | direct | sat | t3 | transform/mirror_h_rot270/direct | direct | 14.5 | 29 | 200 | 200 | 0 |
| SenseNova-U1-8B-MoT | direct | sat | t3 | transform/mirror_h_rot270/oracle | oracle | 22.0 | 44 | 200 | 200 | 0 |
| SenseNova-U1-8B-MoT | direct | sat | t3 | transform/mirror_h_rot90/direct | direct | 13.0 | 26 | 200 | 200 | 0 |
| SenseNova-U1-8B-MoT | direct | sat | t3 | transform/mirror_h_rot90/oracle | oracle | 16.0 | 32 | 200 | 200 | 0 |
| SenseNova-U1-8B-MoT | direct | sat | t3 | transform/rot180/direct | direct | 16.0 | 32 | 200 | 200 | 0 |
| SenseNova-U1-8B-MoT | direct | sat | t3 | transform/rot180/oracle | oracle | 19.5 | 39 | 200 | 200 | 0 |
| SenseNova-U1-8B-MoT | direct | sat | t3 | transform/rot270/direct | direct | 9.5 | 19 | 200 | 200 | 0 |
| SenseNova-U1-8B-MoT | direct | sat | t3 | transform/rot270/oracle | oracle | 17.0 | 34 | 200 | 200 | 0 |
| SenseNova-U1-8B-MoT | direct | sat | t3 | transform/rot90/direct | direct | 13.0 | 26 | 200 | 200 | 0 |
| SenseNova-U1-8B-MoT | direct | sat | t3 | transform/rot90/oracle | oracle | 19.0 | 38 | 200 | 200 | 0 |
| SenseNova-U1-8B-MoT | direct | sat | t3 | world/intervention_001/direct | direct | 45.5 | 91 | 200 | 200 | 0 |
| SenseNova-U1-8B-MoT | direct | sat | t3 | world/intervention_001/oracle | oracle | 44.5 | 89 | 200 | 200 | 0 |
| SenseNova-U1-8B-MoT | direct | sat | t3 | world/sham_001/direct | direct | 5.0 | 10 | 200 | 200 | 0 |
| SenseNova-U1-8B-MoT | direct | sat | t3 | world/sham_001/oracle | oracle | 5.5 | 11 | 200 | 200 | 0 |
| SenseNova-U1-8B-MoT | direct | sat | t4 | base/direct | direct | 37.2 | 149 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | sat | t4 | base/oracle | oracle | 34.8 | 139 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | sat | t4 | transform/mirror_h/direct | direct | 33.5 | 134 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | sat | t4 | transform/mirror_h/oracle | oracle | 32.8 | 131 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | sat | t4 | transform/mirror_h_rot180/direct | direct | 32.2 | 129 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | sat | t4 | transform/mirror_h_rot180/oracle | oracle | 33.5 | 134 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | sat | t4 | transform/mirror_h_rot270/direct | direct | 34.2 | 137 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | sat | t4 | transform/mirror_h_rot270/oracle | oracle | 34.8 | 139 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | sat | t4 | transform/mirror_h_rot90/direct | direct | 35.5 | 142 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | sat | t4 | transform/mirror_h_rot90/oracle | oracle | 34.8 | 139 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | sat | t4 | transform/rot180/direct | direct | 34.8 | 139 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | sat | t4 | transform/rot180/oracle | oracle | 37.2 | 149 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | sat | t4 | transform/rot270/direct | direct | 37.5 | 150 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | sat | t4 | transform/rot270/oracle | oracle | 38.5 | 154 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | sat | t4 | transform/rot90/direct | direct | 33.2 | 133 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | sat | t4 | transform/rot90/oracle | oracle | 34.2 | 137 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | sat | t4 | world/intervention_001/direct | direct | 22.0 | 44 | 200 | 200 | 0 |
| SenseNova-U1-8B-MoT | direct | sat | t4 | world/intervention_001/oracle | oracle | 27.5 | 55 | 200 | 200 | 0 |
| SenseNova-U1-8B-MoT | direct | sat | t4 | world/sham_001/direct | direct | 29.0 | 58 | 200 | 200 | 0 |
| SenseNova-U1-8B-MoT | direct | sat | t4 | world/sham_001/oracle | oracle | 29.5 | 59 | 200 | 200 | 0 |
| SenseNova-U1-8B-MoT | direct | webrd04 | t1 | base/direct | direct | 49.2 | 197 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | webrd04 | t1 | base/oracle | oracle | 54.0 | 216 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | webrd04 | t2 | base/direct | direct | 33.2 | 133 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | webrd04 | t2 | base/oracle | oracle | 32.0 | 128 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | webrd04 | t3 | base/direct | direct | 19.0 | 38 | 200 | 200 | 0 |
| SenseNova-U1-8B-MoT | direct | webrd04 | t3 | base/oracle | oracle | 18.5 | 37 | 200 | 200 | 0 |
| SenseNova-U1-8B-MoT | direct | webrd04 | t3 | world/intervention_001/direct | direct | 45.5 | 91 | 200 | 200 | 0 |
| SenseNova-U1-8B-MoT | direct | webrd04 | t3 | world/intervention_001/oracle | oracle | 45.5 | 91 | 200 | 200 | 0 |
| SenseNova-U1-8B-MoT | direct | webrd04 | t3 | world/sham_001/direct | direct | 13.5 | 27 | 200 | 200 | 0 |
| SenseNova-U1-8B-MoT | direct | webrd04 | t3 | world/sham_001/oracle | oracle | 13.5 | 27 | 200 | 200 | 0 |
| SenseNova-U1-8B-MoT | direct | webrd04 | t4 | base/direct | direct | 30.0 | 120 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | webrd04 | t4 | base/oracle | oracle | 35.2 | 141 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | webrd04 | t4 | world/intervention_001/direct | direct | 26.0 | 52 | 200 | 200 | 0 |
| SenseNova-U1-8B-MoT | direct | webrd04 | t4 | world/intervention_001/oracle | oracle | 31.5 | 63 | 200 | 200 | 0 |
| SenseNova-U1-8B-MoT | direct | webrd04 | t4 | world/sham_001/direct | direct | 25.5 | 51 | 200 | 200 | 0 |
| SenseNova-U1-8B-MoT | direct | webrd04 | t4 | world/sham_001/oracle | oracle | 26.0 | 52 | 200 | 200 | 0 |
| SenseNova-U1-8B-MoT | direct | wprd01 | t1 | base/direct | direct | 54.2 | 217 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | wprd01 | t1 | base/oracle | oracle | 51.8 | 207 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | wprd01 | t1 | transform/mirror_h/direct | direct | 30.8 | 123 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | wprd01 | t1 | transform/mirror_h/oracle | oracle | 30.0 | 120 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | wprd01 | t1 | transform/mirror_h_rot180/direct | direct | 31.0 | 124 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | wprd01 | t1 | transform/mirror_h_rot180/oracle | oracle | 35.8 | 143 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | wprd01 | t1 | transform/mirror_h_rot270/direct | direct | 29.8 | 119 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | wprd01 | t1 | transform/mirror_h_rot270/oracle | oracle | 30.0 | 120 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | wprd01 | t1 | transform/mirror_h_rot90/direct | direct | 30.8 | 123 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | wprd01 | t1 | transform/mirror_h_rot90/oracle | oracle | 32.5 | 130 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | wprd01 | t1 | transform/rot180/direct | direct | 51.2 | 205 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | wprd01 | t1 | transform/rot180/oracle | oracle | 53.8 | 215 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | wprd01 | t1 | transform/rot270/direct | direct | 57.8 | 231 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | wprd01 | t1 | transform/rot270/oracle | oracle | 57.2 | 229 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | wprd01 | t1 | transform/rot90/direct | direct | 55.0 | 220 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | wprd01 | t1 | transform/rot90/oracle | oracle | 57.5 | 230 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | wprd01 | t2 | base/direct | direct | 45.0 | 180 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | wprd01 | t2 | base/oracle | oracle | 45.0 | 180 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | wprd01 | t2 | transform/mirror_h/direct | direct | 44.2 | 177 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | wprd01 | t2 | transform/mirror_h/oracle | oracle | 47.5 | 190 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | wprd01 | t2 | transform/mirror_h_rot180/direct | direct | 42.2 | 169 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | wprd01 | t2 | transform/mirror_h_rot180/oracle | oracle | 42.8 | 171 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | wprd01 | t2 | transform/mirror_h_rot270/direct | direct | 48.5 | 194 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | wprd01 | t2 | transform/mirror_h_rot270/oracle | oracle | 43.8 | 175 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | wprd01 | t2 | transform/mirror_h_rot90/direct | direct | 48.5 | 194 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | wprd01 | t2 | transform/mirror_h_rot90/oracle | oracle | 48.2 | 193 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | wprd01 | t2 | transform/rot180/direct | direct | 43.0 | 172 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | wprd01 | t2 | transform/rot180/oracle | oracle | 42.8 | 171 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | wprd01 | t2 | transform/rot270/direct | direct | 40.2 | 161 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | wprd01 | t2 | transform/rot270/oracle | oracle | 42.0 | 168 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | wprd01 | t2 | transform/rot90/direct | direct | 48.8 | 195 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | wprd01 | t2 | transform/rot90/oracle | oracle | 47.2 | 189 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | wprd01 | t3 | base/direct | direct | 18.0 | 36 | 200 | 200 | 0 |
| SenseNova-U1-8B-MoT | direct | wprd01 | t3 | base/oracle | oracle | 18.0 | 36 | 200 | 200 | 0 |
| SenseNova-U1-8B-MoT | direct | wprd01 | t3 | transform/mirror_h/direct | direct | 23.5 | 47 | 200 | 200 | 0 |
| SenseNova-U1-8B-MoT | direct | wprd01 | t3 | transform/mirror_h/oracle | oracle | 22.0 | 44 | 200 | 200 | 0 |
| SenseNova-U1-8B-MoT | direct | wprd01 | t3 | transform/mirror_h_rot180/direct | direct | 22.5 | 45 | 200 | 200 | 0 |
| SenseNova-U1-8B-MoT | direct | wprd01 | t3 | transform/mirror_h_rot180/oracle | oracle | 22.5 | 45 | 200 | 200 | 0 |
| SenseNova-U1-8B-MoT | direct | wprd01 | t3 | transform/mirror_h_rot270/direct | direct | 25.5 | 51 | 200 | 200 | 0 |
| SenseNova-U1-8B-MoT | direct | wprd01 | t3 | transform/mirror_h_rot270/oracle | oracle | 25.5 | 51 | 200 | 200 | 0 |
| SenseNova-U1-8B-MoT | direct | wprd01 | t3 | transform/mirror_h_rot90/direct | direct | 26.0 | 52 | 200 | 200 | 0 |
| SenseNova-U1-8B-MoT | direct | wprd01 | t3 | transform/mirror_h_rot90/oracle | oracle | 24.5 | 49 | 200 | 200 | 0 |
| SenseNova-U1-8B-MoT | direct | wprd01 | t3 | transform/rot180/direct | direct | 22.5 | 45 | 200 | 200 | 0 |
| SenseNova-U1-8B-MoT | direct | wprd01 | t3 | transform/rot180/oracle | oracle | 22.5 | 45 | 200 | 200 | 0 |
| SenseNova-U1-8B-MoT | direct | wprd01 | t3 | transform/rot270/direct | direct | 22.5 | 45 | 200 | 200 | 0 |
| SenseNova-U1-8B-MoT | direct | wprd01 | t3 | transform/rot270/oracle | oracle | 22.0 | 44 | 200 | 200 | 0 |
| SenseNova-U1-8B-MoT | direct | wprd01 | t3 | transform/rot90/direct | direct | 27.5 | 55 | 200 | 200 | 0 |
| SenseNova-U1-8B-MoT | direct | wprd01 | t3 | transform/rot90/oracle | oracle | 27.5 | 55 | 200 | 200 | 0 |
| SenseNova-U1-8B-MoT | direct | wprd01 | t3 | world/intervention_001/direct | direct | 52.0 | 104 | 200 | 200 | 0 |
| SenseNova-U1-8B-MoT | direct | wprd01 | t3 | world/intervention_001/oracle | oracle | 53.0 | 106 | 200 | 200 | 0 |
| SenseNova-U1-8B-MoT | direct | wprd01 | t3 | world/sham_001/direct | direct | 8.0 | 16 | 200 | 200 | 0 |
| SenseNova-U1-8B-MoT | direct | wprd01 | t3 | world/sham_001/oracle | oracle | 9.0 | 18 | 200 | 200 | 0 |
| SenseNova-U1-8B-MoT | direct | wprd01 | t4 | base/direct | direct | 39.2 | 157 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | wprd01 | t4 | base/oracle | oracle | 39.0 | 156 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | wprd01 | t4 | transform/mirror_h/direct | direct | 39.5 | 158 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | wprd01 | t4 | transform/mirror_h/oracle | oracle | 38.5 | 154 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | wprd01 | t4 | transform/mirror_h_rot180/direct | direct | 37.8 | 151 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | wprd01 | t4 | transform/mirror_h_rot180/oracle | oracle | 36.5 | 146 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | wprd01 | t4 | transform/mirror_h_rot270/direct | direct | 36.8 | 147 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | wprd01 | t4 | transform/mirror_h_rot270/oracle | oracle | 37.2 | 149 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | wprd01 | t4 | transform/mirror_h_rot90/direct | direct | 40.2 | 161 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | wprd01 | t4 | transform/mirror_h_rot90/oracle | oracle | 39.0 | 156 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | wprd01 | t4 | transform/rot180/direct | direct | 36.2 | 145 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | wprd01 | t4 | transform/rot180/oracle | oracle | 37.0 | 148 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | wprd01 | t4 | transform/rot270/direct | direct | 38.2 | 153 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | wprd01 | t4 | transform/rot270/oracle | oracle | 40.2 | 161 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | wprd01 | t4 | transform/rot90/direct | direct | 38.5 | 154 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | wprd01 | t4 | transform/rot90/oracle | oracle | 38.8 | 155 | 400 | 400 | 0 |
| SenseNova-U1-8B-MoT | direct | wprd01 | t4 | world/intervention_001/direct | direct | 20.5 | 41 | 200 | 200 | 0 |
| SenseNova-U1-8B-MoT | direct | wprd01 | t4 | world/intervention_001/oracle | oracle | 30.5 | 61 | 200 | 200 | 0 |
| SenseNova-U1-8B-MoT | direct | wprd01 | t4 | world/sham_001/direct | direct | 42.0 | 84 | 200 | 200 | 0 |
| SenseNova-U1-8B-MoT | direct | wprd01 | t4 | world/sham_001/oracle | oracle | 33.5 | 67 | 200 | 200 | 0 |
| LatentUM-Base | direct | blank | t1 | base/direct | direct | 59.8 | 239 | 400 | 400 | 0 |
| LatentUM-Base | direct | blank | t1 | base/oracle | oracle | 66.0 | 264 | 400 | 400 | 0 |
| LatentUM-Base | direct | blank | t1 | transform/mirror_h/direct | direct | 30.8 | 123 | 400 | 400 | 0 |
| LatentUM-Base | direct | blank | t1 | transform/mirror_h/oracle | oracle | 35.5 | 142 | 400 | 400 | 0 |
| LatentUM-Base | direct | blank | t1 | transform/mirror_h_rot180/direct | direct | 28.8 | 115 | 400 | 400 | 0 |
| LatentUM-Base | direct | blank | t1 | transform/mirror_h_rot180/oracle | oracle | 37.8 | 151 | 400 | 400 | 0 |
| LatentUM-Base | direct | blank | t1 | transform/mirror_h_rot270/direct | direct | 39.5 | 158 | 400 | 400 | 0 |
| LatentUM-Base | direct | blank | t1 | transform/mirror_h_rot270/oracle | oracle | 43.0 | 172 | 400 | 400 | 0 |
| LatentUM-Base | direct | blank | t1 | transform/mirror_h_rot90/direct | direct | 46.8 | 187 | 400 | 400 | 0 |
| LatentUM-Base | direct | blank | t1 | transform/mirror_h_rot90/oracle | oracle | 52.5 | 210 | 400 | 400 | 0 |
| LatentUM-Base | direct | blank | t1 | transform/rot180/direct | direct | 57.5 | 230 | 400 | 400 | 0 |
| LatentUM-Base | direct | blank | t1 | transform/rot180/oracle | oracle | 56.5 | 226 | 400 | 400 | 0 |
| LatentUM-Base | direct | blank | t1 | transform/rot270/direct | direct | 50.2 | 201 | 400 | 400 | 0 |
| LatentUM-Base | direct | blank | t1 | transform/rot270/oracle | oracle | 51.8 | 207 | 400 | 400 | 0 |
| LatentUM-Base | direct | blank | t1 | transform/rot90/direct | direct | 48.5 | 194 | 400 | 400 | 0 |
| LatentUM-Base | direct | blank | t1 | transform/rot90/oracle | oracle | 52.2 | 209 | 400 | 400 | 0 |
| LatentUM-Base | direct | blank | t2 | base/direct | direct | 39.2 | 157 | 400 | 400 | 0 |
| LatentUM-Base | direct | blank | t2 | base/oracle | oracle | 43.8 | 175 | 400 | 400 | 0 |
| LatentUM-Base | direct | blank | t2 | transform/mirror_h/direct | direct | 45.2 | 181 | 400 | 400 | 0 |
| LatentUM-Base | direct | blank | t2 | transform/mirror_h/oracle | oracle | 47.8 | 191 | 400 | 400 | 0 |
| LatentUM-Base | direct | blank | t2 | transform/mirror_h_rot180/direct | direct | 44.2 | 177 | 400 | 400 | 0 |
| LatentUM-Base | direct | blank | t2 | transform/mirror_h_rot180/oracle | oracle | 46.0 | 184 | 400 | 400 | 0 |
| LatentUM-Base | direct | blank | t2 | transform/mirror_h_rot270/direct | direct | 44.2 | 177 | 400 | 400 | 0 |
| LatentUM-Base | direct | blank | t2 | transform/mirror_h_rot270/oracle | oracle | 47.0 | 188 | 400 | 400 | 0 |
| LatentUM-Base | direct | blank | t2 | transform/mirror_h_rot90/direct | direct | 47.8 | 191 | 400 | 400 | 0 |
| LatentUM-Base | direct | blank | t2 | transform/mirror_h_rot90/oracle | oracle | 46.0 | 184 | 400 | 400 | 0 |
| LatentUM-Base | direct | blank | t2 | transform/rot180/direct | direct | 48.2 | 193 | 400 | 400 | 0 |
| LatentUM-Base | direct | blank | t2 | transform/rot180/oracle | oracle | 49.8 | 199 | 400 | 400 | 0 |
| LatentUM-Base | direct | blank | t2 | transform/rot270/direct | direct | 42.0 | 168 | 400 | 400 | 0 |
| LatentUM-Base | direct | blank | t2 | transform/rot270/oracle | oracle | 43.2 | 173 | 400 | 400 | 0 |
| LatentUM-Base | direct | blank | t2 | transform/rot90/direct | direct | 45.2 | 181 | 400 | 400 | 0 |
| LatentUM-Base | direct | blank | t2 | transform/rot90/oracle | oracle | 47.5 | 190 | 400 | 400 | 0 |
| LatentUM-Base | direct | sat | t1 | base/direct | direct | 59.0 | 236 | 400 | 400 | 0 |
| LatentUM-Base | direct | sat | t1 | base/oracle | oracle | 63.5 | 254 | 400 | 400 | 0 |
| LatentUM-Base | direct | sat | t1 | transform/mirror_h/direct | direct | 26.8 | 107 | 400 | 400 | 0 |
| LatentUM-Base | direct | sat | t1 | transform/mirror_h/oracle | oracle | 30.2 | 121 | 400 | 400 | 0 |
| LatentUM-Base | direct | sat | t1 | transform/mirror_h_rot180/direct | direct | 25.0 | 100 | 400 | 400 | 0 |
| LatentUM-Base | direct | sat | t1 | transform/mirror_h_rot180/oracle | oracle | 28.2 | 113 | 400 | 400 | 0 |
| LatentUM-Base | direct | sat | t1 | transform/mirror_h_rot270/direct | direct | 33.5 | 134 | 400 | 400 | 0 |
| LatentUM-Base | direct | sat | t1 | transform/mirror_h_rot270/oracle | oracle | 38.0 | 152 | 400 | 400 | 0 |
| LatentUM-Base | direct | sat | t1 | transform/mirror_h_rot90/direct | direct | 38.0 | 152 | 400 | 400 | 0 |
| LatentUM-Base | direct | sat | t1 | transform/mirror_h_rot90/oracle | oracle | 44.5 | 178 | 400 | 400 | 0 |
| LatentUM-Base | direct | sat | t1 | transform/rot180/direct | direct | 52.5 | 210 | 400 | 400 | 0 |
| LatentUM-Base | direct | sat | t1 | transform/rot180/oracle | oracle | 54.8 | 219 | 400 | 400 | 0 |
| LatentUM-Base | direct | sat | t1 | transform/rot270/direct | direct | 46.2 | 185 | 400 | 400 | 0 |
| LatentUM-Base | direct | sat | t1 | transform/rot270/oracle | oracle | 47.0 | 188 | 400 | 400 | 0 |
| LatentUM-Base | direct | sat | t1 | transform/rot90/direct | direct | 43.8 | 175 | 400 | 400 | 0 |
| LatentUM-Base | direct | sat | t1 | transform/rot90/oracle | oracle | 46.2 | 185 | 400 | 400 | 0 |
| LatentUM-Base | direct | sat | t2 | base/direct | direct | 43.8 | 175 | 400 | 400 | 0 |
| LatentUM-Base | direct | sat | t2 | base/oracle | oracle | 38.8 | 155 | 400 | 400 | 0 |
| LatentUM-Base | direct | sat | t2 | transform/mirror_h/direct | direct | 44.0 | 176 | 400 | 400 | 0 |
| LatentUM-Base | direct | sat | t2 | transform/mirror_h/oracle | oracle | 45.2 | 181 | 400 | 400 | 0 |
| LatentUM-Base | direct | sat | t2 | transform/mirror_h_rot180/direct | direct | 46.8 | 187 | 400 | 400 | 0 |
| LatentUM-Base | direct | sat | t2 | transform/mirror_h_rot180/oracle | oracle | 41.2 | 165 | 400 | 400 | 0 |
| LatentUM-Base | direct | sat | t2 | transform/mirror_h_rot270/direct | direct | 45.0 | 180 | 400 | 400 | 0 |
| LatentUM-Base | direct | sat | t2 | transform/mirror_h_rot270/oracle | oracle | 41.0 | 164 | 400 | 400 | 0 |
| LatentUM-Base | direct | sat | t2 | transform/mirror_h_rot90/direct | direct | 41.0 | 164 | 400 | 400 | 0 |
| LatentUM-Base | direct | sat | t2 | transform/mirror_h_rot90/oracle | oracle | 39.0 | 156 | 400 | 400 | 0 |
| LatentUM-Base | direct | sat | t2 | transform/rot180/direct | direct | 41.0 | 164 | 400 | 400 | 0 |
| LatentUM-Base | direct | sat | t2 | transform/rot180/oracle | oracle | 42.0 | 168 | 400 | 400 | 0 |
| LatentUM-Base | direct | sat | t2 | transform/rot270/direct | direct | 45.5 | 182 | 400 | 400 | 0 |
| LatentUM-Base | direct | sat | t2 | transform/rot270/oracle | oracle | 43.0 | 172 | 400 | 400 | 0 |
| LatentUM-Base | direct | sat | t2 | transform/rot90/direct | direct | 43.2 | 173 | 400 | 400 | 0 |
| LatentUM-Base | direct | sat | t2 | transform/rot90/oracle | oracle | 39.2 | 157 | 400 | 400 | 0 |
| LatentUM-Base | direct | sat | t3 | base/direct | direct | 35.0 | 70 | 200 | 200 | 0 |
| LatentUM-Base | direct | sat | t3 | base/oracle | oracle | 35.5 | 71 | 200 | 200 | 0 |
| LatentUM-Base | direct | sat | t3 | transform/mirror_h/direct | direct | 35.0 | 70 | 200 | 200 | 0 |
| LatentUM-Base | direct | sat | t3 | transform/mirror_h/oracle | oracle | 36.0 | 72 | 200 | 200 | 0 |
| LatentUM-Base | direct | sat | t3 | transform/mirror_h_rot180/direct | direct | 33.5 | 67 | 200 | 200 | 0 |
| LatentUM-Base | direct | sat | t3 | transform/mirror_h_rot180/oracle | oracle | 36.0 | 72 | 200 | 200 | 0 |
| LatentUM-Base | direct | sat | t3 | transform/mirror_h_rot270/direct | direct | 35.0 | 70 | 200 | 200 | 0 |
| LatentUM-Base | direct | sat | t3 | transform/mirror_h_rot270/oracle | oracle | 36.5 | 73 | 200 | 200 | 0 |
| LatentUM-Base | direct | sat | t3 | transform/mirror_h_rot90/direct | direct | 34.5 | 69 | 200 | 200 | 0 |
| LatentUM-Base | direct | sat | t3 | transform/mirror_h_rot90/oracle | oracle | 37.0 | 74 | 200 | 200 | 0 |
| LatentUM-Base | direct | sat | t3 | transform/rot180/direct | direct | 34.5 | 69 | 200 | 200 | 0 |
| LatentUM-Base | direct | sat | t3 | transform/rot180/oracle | oracle | 35.0 | 70 | 200 | 200 | 0 |
| LatentUM-Base | direct | sat | t3 | transform/rot270/direct | direct | 34.0 | 68 | 200 | 200 | 0 |
| LatentUM-Base | direct | sat | t3 | transform/rot270/oracle | oracle | 35.0 | 70 | 200 | 200 | 0 |
| LatentUM-Base | direct | sat | t3 | transform/rot90/direct | direct | 35.5 | 71 | 200 | 200 | 0 |
| LatentUM-Base | direct | sat | t3 | transform/rot90/oracle | oracle | 35.5 | 71 | 200 | 200 | 0 |
| LatentUM-Base | direct | sat | t3 | world/intervention_001/direct | direct | 36.5 | 73 | 200 | 200 | 0 |
| LatentUM-Base | direct | sat | t3 | world/intervention_001/oracle | oracle | 36.0 | 72 | 200 | 200 | 0 |
| LatentUM-Base | direct | sat | t3 | world/sham_001/direct | direct | 27.5 | 55 | 200 | 200 | 0 |
| LatentUM-Base | direct | sat | t3 | world/sham_001/oracle | oracle | 29.0 | 58 | 200 | 200 | 0 |
| LatentUM-Base | direct | sat | t4 | base/direct | direct | 28.8 | 115 | 400 | 400 | 0 |
| LatentUM-Base | direct | sat | t4 | base/oracle | oracle | 32.8 | 131 | 400 | 400 | 0 |
| LatentUM-Base | direct | sat | t4 | transform/mirror_h/direct | direct | 30.0 | 120 | 400 | 400 | 0 |
| LatentUM-Base | direct | sat | t4 | transform/mirror_h/oracle | oracle | 32.5 | 130 | 400 | 400 | 0 |
| LatentUM-Base | direct | sat | t4 | transform/mirror_h_rot180/direct | direct | 29.8 | 119 | 400 | 400 | 0 |
| LatentUM-Base | direct | sat | t4 | transform/mirror_h_rot180/oracle | oracle | 32.0 | 128 | 400 | 400 | 0 |
| LatentUM-Base | direct | sat | t4 | transform/mirror_h_rot270/direct | direct | 32.2 | 129 | 400 | 400 | 0 |
| LatentUM-Base | direct | sat | t4 | transform/mirror_h_rot270/oracle | oracle | 33.5 | 134 | 400 | 400 | 0 |
| LatentUM-Base | direct | sat | t4 | transform/mirror_h_rot90/direct | direct | 29.2 | 117 | 400 | 400 | 0 |
| LatentUM-Base | direct | sat | t4 | transform/mirror_h_rot90/oracle | oracle | 32.2 | 129 | 400 | 400 | 0 |
| LatentUM-Base | direct | sat | t4 | transform/rot180/direct | direct | 31.8 | 127 | 400 | 400 | 0 |
| LatentUM-Base | direct | sat | t4 | transform/rot180/oracle | oracle | 34.0 | 136 | 400 | 400 | 0 |
| LatentUM-Base | direct | sat | t4 | transform/rot270/direct | direct | 30.8 | 123 | 400 | 400 | 0 |
| LatentUM-Base | direct | sat | t4 | transform/rot270/oracle | oracle | 34.2 | 137 | 400 | 400 | 0 |
| LatentUM-Base | direct | sat | t4 | transform/rot90/direct | direct | 29.5 | 118 | 400 | 400 | 0 |
| LatentUM-Base | direct | sat | t4 | transform/rot90/oracle | oracle | 31.8 | 127 | 400 | 400 | 0 |
| LatentUM-Base | direct | sat | t4 | world/intervention_001/direct | direct | 11.5 | 23 | 200 | 200 | 0 |
| LatentUM-Base | direct | sat | t4 | world/intervention_001/oracle | oracle | 14.5 | 29 | 200 | 200 | 0 |
| LatentUM-Base | direct | sat | t4 | world/sham_001/direct | direct | 24.5 | 49 | 200 | 200 | 0 |
| LatentUM-Base | direct | sat | t4 | world/sham_001/oracle | oracle | 33.5 | 67 | 200 | 200 | 0 |
| LatentUM-Base | direct | webrd04 | t1 | base/direct | direct | 55.2 | 221 | 400 | 400 | 0 |
| LatentUM-Base | direct | webrd04 | t1 | base/oracle | oracle | 64.2 | 257 | 400 | 400 | 0 |
| LatentUM-Base | direct | webrd04 | t2 | base/direct | direct | 44.8 | 179 | 400 | 400 | 0 |
| LatentUM-Base | direct | webrd04 | t2 | base/oracle | oracle | 42.2 | 169 | 400 | 400 | 0 |
| LatentUM-Base | direct | webrd04 | t3 | base/direct | direct | 43.5 | 87 | 200 | 200 | 0 |
| LatentUM-Base | direct | webrd04 | t3 | base/oracle | oracle | 44.0 | 88 | 200 | 200 | 0 |
| LatentUM-Base | direct | webrd04 | t3 | world/intervention_001/direct | direct | 33.0 | 66 | 200 | 200 | 0 |
| LatentUM-Base | direct | webrd04 | t3 | world/intervention_001/oracle | oracle | 33.0 | 66 | 200 | 200 | 0 |
| LatentUM-Base | direct | webrd04 | t3 | world/sham_001/direct | direct | 29.5 | 59 | 200 | 200 | 0 |
| LatentUM-Base | direct | webrd04 | t3 | world/sham_001/oracle | oracle | 29.5 | 59 | 200 | 200 | 0 |
| LatentUM-Base | direct | webrd04 | t4 | base/direct | direct | 32.2 | 129 | 400 | 400 | 0 |
| LatentUM-Base | direct | webrd04 | t4 | base/oracle | oracle | 34.5 | 138 | 400 | 400 | 0 |
| LatentUM-Base | direct | webrd04 | t4 | world/intervention_001/direct | direct | 11.5 | 23 | 200 | 200 | 0 |
| LatentUM-Base | direct | webrd04 | t4 | world/intervention_001/oracle | oracle | 15.5 | 31 | 200 | 200 | 0 |
| LatentUM-Base | direct | webrd04 | t4 | world/sham_001/direct | direct | 31.5 | 63 | 200 | 200 | 0 |
| LatentUM-Base | direct | webrd04 | t4 | world/sham_001/oracle | oracle | 34.0 | 68 | 200 | 200 | 0 |
| LatentUM-Base | direct | wprd01 | t1 | base/direct | direct | 54.5 | 218 | 400 | 400 | 0 |
| LatentUM-Base | direct | wprd01 | t1 | base/oracle | oracle | 59.8 | 239 | 400 | 400 | 0 |
| LatentUM-Base | direct | wprd01 | t1 | transform/mirror_h/direct | direct | 33.5 | 134 | 400 | 400 | 0 |
| LatentUM-Base | direct | wprd01 | t1 | transform/mirror_h/oracle | oracle | 43.8 | 175 | 400 | 400 | 0 |
| LatentUM-Base | direct | wprd01 | t1 | transform/mirror_h_rot180/direct | direct | 35.8 | 143 | 400 | 400 | 0 |
| LatentUM-Base | direct | wprd01 | t1 | transform/mirror_h_rot180/oracle | oracle | 39.8 | 159 | 400 | 400 | 0 |
| LatentUM-Base | direct | wprd01 | t1 | transform/mirror_h_rot270/direct | direct | 36.2 | 145 | 400 | 400 | 0 |
| LatentUM-Base | direct | wprd01 | t1 | transform/mirror_h_rot270/oracle | oracle | 45.0 | 180 | 400 | 400 | 0 |
| LatentUM-Base | direct | wprd01 | t1 | transform/mirror_h_rot90/direct | direct | 45.0 | 180 | 400 | 400 | 0 |
| LatentUM-Base | direct | wprd01 | t1 | transform/mirror_h_rot90/oracle | oracle | 52.8 | 211 | 400 | 400 | 0 |
| LatentUM-Base | direct | wprd01 | t1 | transform/rot180/direct | direct | 52.0 | 208 | 400 | 400 | 0 |
| LatentUM-Base | direct | wprd01 | t1 | transform/rot180/oracle | oracle | 55.2 | 221 | 400 | 400 | 0 |
| LatentUM-Base | direct | wprd01 | t1 | transform/rot270/direct | direct | 42.0 | 168 | 400 | 400 | 0 |
| LatentUM-Base | direct | wprd01 | t1 | transform/rot270/oracle | oracle | 48.5 | 194 | 400 | 400 | 0 |
| LatentUM-Base | direct | wprd01 | t1 | transform/rot90/direct | direct | 42.0 | 168 | 400 | 400 | 0 |
| LatentUM-Base | direct | wprd01 | t1 | transform/rot90/oracle | oracle | 47.8 | 191 | 400 | 400 | 0 |
| LatentUM-Base | direct | wprd01 | t2 | base/direct | direct | 44.8 | 179 | 400 | 400 | 0 |
| LatentUM-Base | direct | wprd01 | t2 | base/oracle | oracle | 44.8 | 179 | 400 | 400 | 0 |
| LatentUM-Base | direct | wprd01 | t2 | transform/mirror_h/direct | direct | 46.8 | 187 | 400 | 400 | 0 |
| LatentUM-Base | direct | wprd01 | t2 | transform/mirror_h/oracle | oracle | 52.8 | 211 | 400 | 400 | 0 |
| LatentUM-Base | direct | wprd01 | t2 | transform/mirror_h_rot180/direct | direct | 45.2 | 181 | 400 | 400 | 0 |
| LatentUM-Base | direct | wprd01 | t2 | transform/mirror_h_rot180/oracle | oracle | 45.5 | 182 | 400 | 400 | 0 |
| LatentUM-Base | direct | wprd01 | t2 | transform/mirror_h_rot270/direct | direct | 44.2 | 177 | 400 | 400 | 0 |
| LatentUM-Base | direct | wprd01 | t2 | transform/mirror_h_rot270/oracle | oracle | 49.5 | 198 | 400 | 400 | 0 |
| LatentUM-Base | direct | wprd01 | t2 | transform/mirror_h_rot90/direct | direct | 46.2 | 185 | 400 | 400 | 0 |
| LatentUM-Base | direct | wprd01 | t2 | transform/mirror_h_rot90/oracle | oracle | 46.5 | 186 | 400 | 400 | 0 |
| LatentUM-Base | direct | wprd01 | t2 | transform/rot180/direct | direct | 45.8 | 183 | 400 | 400 | 0 |
| LatentUM-Base | direct | wprd01 | t2 | transform/rot180/oracle | oracle | 46.8 | 187 | 400 | 400 | 0 |
| LatentUM-Base | direct | wprd01 | t2 | transform/rot270/direct | direct | 42.8 | 171 | 400 | 400 | 0 |
| LatentUM-Base | direct | wprd01 | t2 | transform/rot270/oracle | oracle | 45.8 | 183 | 400 | 400 | 0 |
| LatentUM-Base | direct | wprd01 | t2 | transform/rot90/direct | direct | 44.8 | 179 | 400 | 400 | 0 |
| LatentUM-Base | direct | wprd01 | t2 | transform/rot90/oracle | oracle | 48.5 | 194 | 400 | 400 | 0 |
| LatentUM-Base | direct | wprd01 | t3 | base/direct | direct | 25.0 | 50 | 200 | 200 | 0 |
| LatentUM-Base | direct | wprd01 | t3 | base/oracle | oracle | 25.5 | 51 | 200 | 200 | 0 |
| LatentUM-Base | direct | wprd01 | t3 | transform/mirror_h/direct | direct | 26.0 | 52 | 200 | 200 | 0 |
| LatentUM-Base | direct | wprd01 | t3 | transform/mirror_h/oracle | oracle | 27.5 | 55 | 200 | 200 | 0 |
| LatentUM-Base | direct | wprd01 | t3 | transform/mirror_h_rot180/direct | direct | 26.5 | 53 | 200 | 200 | 0 |
| LatentUM-Base | direct | wprd01 | t3 | transform/mirror_h_rot180/oracle | oracle | 25.5 | 51 | 200 | 200 | 0 |
| LatentUM-Base | direct | wprd01 | t3 | transform/mirror_h_rot270/direct | direct | 26.0 | 52 | 200 | 200 | 0 |
| LatentUM-Base | direct | wprd01 | t3 | transform/mirror_h_rot270/oracle | oracle | 26.0 | 52 | 200 | 200 | 0 |
| LatentUM-Base | direct | wprd01 | t3 | transform/mirror_h_rot90/direct | direct | 26.5 | 53 | 200 | 200 | 0 |
| LatentUM-Base | direct | wprd01 | t3 | transform/mirror_h_rot90/oracle | oracle | 27.0 | 54 | 200 | 200 | 0 |
| LatentUM-Base | direct | wprd01 | t3 | transform/rot180/direct | direct | 25.5 | 51 | 200 | 200 | 0 |
| LatentUM-Base | direct | wprd01 | t3 | transform/rot180/oracle | oracle | 26.5 | 53 | 200 | 200 | 0 |
| LatentUM-Base | direct | wprd01 | t3 | transform/rot270/direct | direct | 25.0 | 50 | 200 | 200 | 0 |
| LatentUM-Base | direct | wprd01 | t3 | transform/rot270/oracle | oracle | 25.5 | 51 | 200 | 200 | 0 |
| LatentUM-Base | direct | wprd01 | t3 | transform/rot90/direct | direct | 25.0 | 50 | 200 | 200 | 0 |
| LatentUM-Base | direct | wprd01 | t3 | transform/rot90/oracle | oracle | 24.5 | 49 | 200 | 200 | 0 |
| LatentUM-Base | direct | wprd01 | t3 | world/intervention_001/direct | direct | 43.0 | 86 | 200 | 200 | 0 |
| LatentUM-Base | direct | wprd01 | t3 | world/intervention_001/oracle | oracle | 43.0 | 86 | 200 | 200 | 0 |
| LatentUM-Base | direct | wprd01 | t3 | world/sham_001/direct | direct | 14.0 | 28 | 200 | 200 | 0 |
| LatentUM-Base | direct | wprd01 | t3 | world/sham_001/oracle | oracle | 15.5 | 31 | 200 | 200 | 0 |
| LatentUM-Base | direct | wprd01 | t4 | base/direct | direct | 32.2 | 129 | 400 | 400 | 0 |
| LatentUM-Base | direct | wprd01 | t4 | base/oracle | oracle | 37.2 | 149 | 400 | 400 | 0 |
| LatentUM-Base | direct | wprd01 | t4 | transform/mirror_h/direct | direct | 36.5 | 146 | 400 | 400 | 0 |
| LatentUM-Base | direct | wprd01 | t4 | transform/mirror_h/oracle | oracle | 40.5 | 162 | 400 | 400 | 0 |
| LatentUM-Base | direct | wprd01 | t4 | transform/mirror_h_rot180/direct | direct | 34.8 | 139 | 400 | 400 | 0 |
| LatentUM-Base | direct | wprd01 | t4 | transform/mirror_h_rot180/oracle | oracle | 39.2 | 157 | 400 | 400 | 0 |
| LatentUM-Base | direct | wprd01 | t4 | transform/mirror_h_rot270/direct | direct | 36.2 | 145 | 400 | 400 | 0 |
| LatentUM-Base | direct | wprd01 | t4 | transform/mirror_h_rot270/oracle | oracle | 42.5 | 170 | 400 | 400 | 0 |
| LatentUM-Base | direct | wprd01 | t4 | transform/mirror_h_rot90/direct | direct | 32.0 | 128 | 400 | 400 | 0 |
| LatentUM-Base | direct | wprd01 | t4 | transform/mirror_h_rot90/oracle | oracle | 37.0 | 148 | 400 | 400 | 0 |
| LatentUM-Base | direct | wprd01 | t4 | transform/rot180/direct | direct | 36.5 | 146 | 400 | 400 | 0 |
| LatentUM-Base | direct | wprd01 | t4 | transform/rot180/oracle | oracle | 40.0 | 160 | 400 | 400 | 0 |
| LatentUM-Base | direct | wprd01 | t4 | transform/rot270/direct | direct | 32.2 | 129 | 400 | 400 | 0 |
| LatentUM-Base | direct | wprd01 | t4 | transform/rot270/oracle | oracle | 38.5 | 154 | 400 | 400 | 0 |
| LatentUM-Base | direct | wprd01 | t4 | transform/rot90/direct | direct | 33.2 | 133 | 400 | 400 | 0 |
| LatentUM-Base | direct | wprd01 | t4 | transform/rot90/oracle | oracle | 39.2 | 157 | 400 | 400 | 0 |
| LatentUM-Base | direct | wprd01 | t4 | world/intervention_001/direct | direct | 12.5 | 25 | 200 | 200 | 0 |
| LatentUM-Base | direct | wprd01 | t4 | world/intervention_001/oracle | oracle | 15.0 | 30 | 200 | 200 | 0 |
| LatentUM-Base | direct | wprd01 | t4 | world/sham_001/direct | direct | 37.5 | 75 | 200 | 200 | 0 |
| LatentUM-Base | direct | wprd01 | t4 | world/sham_001/oracle | oracle | 39.5 | 79 | 200 | 200 | 0 |
| Show-o2-7B | direct | blank | t1 | base/direct | direct | 44.0 | 176 | 400 | 400 | 0 |
| Show-o2-7B | direct | blank | t1 | base/oracle | oracle | 39.5 | 158 | 400 | 400 | 0 |
| Show-o2-7B | direct | blank | t1 | transform/mirror_h/direct | direct | 34.2 | 137 | 400 | 400 | 0 |
| Show-o2-7B | direct | blank | t1 | transform/mirror_h/oracle | oracle | 31.8 | 127 | 400 | 400 | 0 |
| Show-o2-7B | direct | blank | t1 | transform/mirror_h_rot180/direct | direct | 33.2 | 133 | 400 | 400 | 0 |
| Show-o2-7B | direct | blank | t1 | transform/mirror_h_rot180/oracle | oracle | 32.2 | 129 | 400 | 400 | 0 |
| Show-o2-7B | direct | blank | t1 | transform/mirror_h_rot270/direct | direct | 23.2 | 93 | 400 | 400 | 0 |
| Show-o2-7B | direct | blank | t1 | transform/mirror_h_rot270/oracle | oracle | 25.5 | 102 | 400 | 400 | 0 |
| Show-o2-7B | direct | blank | t1 | transform/mirror_h_rot90/direct | direct | 28.0 | 112 | 400 | 400 | 0 |
| Show-o2-7B | direct | blank | t1 | transform/mirror_h_rot90/oracle | oracle | 26.2 | 105 | 400 | 400 | 0 |
| Show-o2-7B | direct | blank | t1 | transform/rot180/direct | direct | 43.2 | 173 | 400 | 400 | 0 |
| Show-o2-7B | direct | blank | t1 | transform/rot180/oracle | oracle | 43.5 | 174 | 400 | 400 | 0 |
| Show-o2-7B | direct | blank | t1 | transform/rot270/direct | direct | 50.5 | 202 | 400 | 400 | 0 |
| Show-o2-7B | direct | blank | t1 | transform/rot270/oracle | oracle | 47.0 | 188 | 400 | 400 | 0 |
| Show-o2-7B | direct | blank | t1 | transform/rot90/direct | direct | 50.2 | 201 | 400 | 400 | 0 |
| Show-o2-7B | direct | blank | t1 | transform/rot90/oracle | oracle | 43.8 | 175 | 400 | 400 | 0 |
| Show-o2-7B | direct | blank | t2 | base/direct | direct | 44.5 | 178 | 400 | 400 | 0 |
| Show-o2-7B | direct | blank | t2 | base/oracle | oracle | 53.8 | 215 | 400 | 400 | 0 |
| Show-o2-7B | direct | blank | t2 | transform/mirror_h/direct | direct | 47.8 | 191 | 400 | 400 | 0 |
| Show-o2-7B | direct | blank | t2 | transform/mirror_h/oracle | oracle | 56.2 | 225 | 400 | 400 | 0 |
| Show-o2-7B | direct | blank | t2 | transform/mirror_h_rot180/direct | direct | 46.0 | 184 | 400 | 400 | 0 |
| Show-o2-7B | direct | blank | t2 | transform/mirror_h_rot180/oracle | oracle | 57.2 | 229 | 400 | 400 | 0 |
| Show-o2-7B | direct | blank | t2 | transform/mirror_h_rot270/direct | direct | 48.2 | 193 | 400 | 400 | 0 |
| Show-o2-7B | direct | blank | t2 | transform/mirror_h_rot270/oracle | oracle | 56.5 | 226 | 400 | 400 | 0 |
| Show-o2-7B | direct | blank | t2 | transform/mirror_h_rot90/direct | direct | 45.0 | 180 | 400 | 400 | 0 |
| Show-o2-7B | direct | blank | t2 | transform/mirror_h_rot90/oracle | oracle | 56.8 | 227 | 400 | 400 | 0 |
| Show-o2-7B | direct | blank | t2 | transform/rot180/direct | direct | 46.5 | 186 | 400 | 400 | 0 |
| Show-o2-7B | direct | blank | t2 | transform/rot180/oracle | oracle | 55.8 | 223 | 400 | 400 | 0 |
| Show-o2-7B | direct | blank | t2 | transform/rot270/direct | direct | 44.8 | 179 | 400 | 400 | 0 |
| Show-o2-7B | direct | blank | t2 | transform/rot270/oracle | oracle | 51.0 | 204 | 400 | 400 | 0 |
| Show-o2-7B | direct | blank | t2 | transform/rot90/direct | direct | 47.0 | 188 | 400 | 400 | 0 |
| Show-o2-7B | direct | blank | t2 | transform/rot90/oracle | oracle | 56.5 | 226 | 400 | 400 | 0 |
| Show-o2-7B | direct | sat | t1 | base/direct | direct | 38.8 | 155 | 400 | 400 | 0 |
| Show-o2-7B | direct | sat | t1 | base/oracle | oracle | 38.5 | 154 | 400 | 400 | 0 |
| Show-o2-7B | direct | sat | t1 | transform/mirror_h/direct | direct | 27.2 | 109 | 400 | 400 | 0 |
| Show-o2-7B | direct | sat | t1 | transform/mirror_h/oracle | oracle | 26.8 | 107 | 400 | 400 | 0 |
| Show-o2-7B | direct | sat | t1 | transform/mirror_h_rot180/direct | direct | 27.0 | 108 | 400 | 400 | 0 |
| Show-o2-7B | direct | sat | t1 | transform/mirror_h_rot180/oracle | oracle | 28.0 | 112 | 400 | 400 | 0 |
| Show-o2-7B | direct | sat | t1 | transform/mirror_h_rot270/direct | direct | 20.0 | 80 | 400 | 400 | 0 |
| Show-o2-7B | direct | sat | t1 | transform/mirror_h_rot270/oracle | oracle | 17.8 | 71 | 400 | 400 | 0 |
| Show-o2-7B | direct | sat | t1 | transform/mirror_h_rot90/direct | direct | 21.8 | 87 | 400 | 400 | 0 |
| Show-o2-7B | direct | sat | t1 | transform/mirror_h_rot90/oracle | oracle | 21.5 | 86 | 400 | 400 | 0 |
| Show-o2-7B | direct | sat | t1 | transform/rot180/direct | direct | 41.2 | 165 | 400 | 400 | 0 |
| Show-o2-7B | direct | sat | t1 | transform/rot180/oracle | oracle | 40.0 | 160 | 400 | 400 | 0 |
| Show-o2-7B | direct | sat | t1 | transform/rot270/direct | direct | 47.8 | 191 | 400 | 400 | 0 |
| Show-o2-7B | direct | sat | t1 | transform/rot270/oracle | oracle | 49.5 | 198 | 400 | 400 | 0 |
| Show-o2-7B | direct | sat | t1 | transform/rot90/direct | direct | 44.2 | 177 | 400 | 400 | 0 |
| Show-o2-7B | direct | sat | t1 | transform/rot90/oracle | oracle | 45.2 | 181 | 400 | 400 | 0 |
| Show-o2-7B | direct | sat | t2 | base/direct | direct | 43.2 | 173 | 400 | 400 | 0 |
| Show-o2-7B | direct | sat | t2 | base/oracle | oracle | 46.0 | 184 | 400 | 400 | 0 |
| Show-o2-7B | direct | sat | t2 | transform/mirror_h/direct | direct | 42.8 | 171 | 400 | 400 | 0 |
| Show-o2-7B | direct | sat | t2 | transform/mirror_h/oracle | oracle | 45.5 | 182 | 400 | 400 | 0 |
| Show-o2-7B | direct | sat | t2 | transform/mirror_h_rot180/direct | direct | 45.5 | 182 | 400 | 400 | 0 |
| Show-o2-7B | direct | sat | t2 | transform/mirror_h_rot180/oracle | oracle | 53.2 | 213 | 400 | 400 | 0 |
| Show-o2-7B | direct | sat | t2 | transform/mirror_h_rot270/direct | direct | 46.5 | 186 | 400 | 400 | 0 |
| Show-o2-7B | direct | sat | t2 | transform/mirror_h_rot270/oracle | oracle | 51.0 | 204 | 400 | 400 | 0 |
| Show-o2-7B | direct | sat | t2 | transform/mirror_h_rot90/direct | direct | 45.8 | 183 | 400 | 400 | 0 |
| Show-o2-7B | direct | sat | t2 | transform/mirror_h_rot90/oracle | oracle | 48.2 | 193 | 400 | 400 | 0 |
| Show-o2-7B | direct | sat | t2 | transform/rot180/direct | direct | 47.0 | 188 | 400 | 400 | 0 |
| Show-o2-7B | direct | sat | t2 | transform/rot180/oracle | oracle | 47.5 | 190 | 400 | 400 | 0 |
| Show-o2-7B | direct | sat | t2 | transform/rot270/direct | direct | 46.2 | 185 | 400 | 400 | 0 |
| Show-o2-7B | direct | sat | t2 | transform/rot270/oracle | oracle | 47.0 | 188 | 400 | 400 | 0 |
| Show-o2-7B | direct | sat | t2 | transform/rot90/direct | direct | 47.0 | 188 | 400 | 400 | 0 |
| Show-o2-7B | direct | sat | t2 | transform/rot90/oracle | oracle | 49.8 | 199 | 400 | 400 | 0 |
| Show-o2-7B | direct | sat | t3 | base/direct | direct | 55.0 | 110 | 200 | 200 | 0 |
| Show-o2-7B | direct | sat | t3 | base/oracle | oracle | 59.5 | 119 | 200 | 200 | 0 |
| Show-o2-7B | direct | sat | t3 | transform/mirror_h/direct | direct | 50.5 | 101 | 200 | 200 | 0 |
| Show-o2-7B | direct | sat | t3 | transform/mirror_h/oracle | oracle | 59.0 | 118 | 200 | 200 | 0 |
| Show-o2-7B | direct | sat | t3 | transform/mirror_h_rot180/direct | direct | 48.0 | 96 | 200 | 200 | 0 |
| Show-o2-7B | direct | sat | t3 | transform/mirror_h_rot180/oracle | oracle | 56.0 | 112 | 200 | 200 | 0 |
| Show-o2-7B | direct | sat | t3 | transform/mirror_h_rot270/direct | direct | 53.0 | 106 | 200 | 200 | 0 |
| Show-o2-7B | direct | sat | t3 | transform/mirror_h_rot270/oracle | oracle | 56.0 | 112 | 200 | 200 | 0 |
| Show-o2-7B | direct | sat | t3 | transform/mirror_h_rot90/direct | direct | 50.5 | 101 | 200 | 200 | 0 |
| Show-o2-7B | direct | sat | t3 | transform/mirror_h_rot90/oracle | oracle | 56.0 | 112 | 200 | 200 | 0 |
| Show-o2-7B | direct | sat | t3 | transform/rot180/direct | direct | 49.5 | 99 | 200 | 200 | 0 |
| Show-o2-7B | direct | sat | t3 | transform/rot180/oracle | oracle | 56.0 | 112 | 200 | 200 | 0 |
| Show-o2-7B | direct | sat | t3 | transform/rot270/direct | direct | 52.0 | 104 | 200 | 200 | 0 |
| Show-o2-7B | direct | sat | t3 | transform/rot270/oracle | oracle | 57.5 | 115 | 200 | 200 | 0 |
| Show-o2-7B | direct | sat | t3 | transform/rot90/direct | direct | 52.0 | 104 | 200 | 200 | 0 |
| Show-o2-7B | direct | sat | t3 | transform/rot90/oracle | oracle | 57.5 | 115 | 200 | 200 | 0 |
| Show-o2-7B | direct | sat | t3 | world/intervention_001/direct | direct | 24.0 | 48 | 200 | 200 | 0 |
| Show-o2-7B | direct | sat | t3 | world/intervention_001/oracle | oracle | 23.0 | 46 | 200 | 200 | 0 |
| Show-o2-7B | direct | sat | t3 | world/sham_001/direct | direct | 46.0 | 92 | 200 | 200 | 0 |
| Show-o2-7B | direct | sat | t3 | world/sham_001/oracle | oracle | 50.0 | 100 | 200 | 200 | 0 |
| Show-o2-7B | direct | sat | t4 | base/direct | direct | 23.0 | 92 | 400 | 400 | 0 |
| Show-o2-7B | direct | sat | t4 | base/oracle | oracle | 26.2 | 105 | 400 | 400 | 0 |
| Show-o2-7B | direct | sat | t4 | transform/mirror_h/direct | direct | 23.8 | 95 | 400 | 400 | 0 |
| Show-o2-7B | direct | sat | t4 | transform/mirror_h/oracle | oracle | 25.5 | 102 | 400 | 400 | 0 |
| Show-o2-7B | direct | sat | t4 | transform/mirror_h_rot180/direct | direct | 22.0 | 88 | 400 | 400 | 0 |
| Show-o2-7B | direct | sat | t4 | transform/mirror_h_rot180/oracle | oracle | 25.8 | 103 | 400 | 400 | 0 |
| Show-o2-7B | direct | sat | t4 | transform/mirror_h_rot270/direct | direct | 23.0 | 92 | 400 | 400 | 0 |
| Show-o2-7B | direct | sat | t4 | transform/mirror_h_rot270/oracle | oracle | 25.2 | 101 | 400 | 400 | 0 |
| Show-o2-7B | direct | sat | t4 | transform/mirror_h_rot90/direct | direct | 24.2 | 97 | 400 | 400 | 0 |
| Show-o2-7B | direct | sat | t4 | transform/mirror_h_rot90/oracle | oracle | 27.2 | 109 | 400 | 400 | 0 |
| Show-o2-7B | direct | sat | t4 | transform/rot180/direct | direct | 21.8 | 87 | 400 | 400 | 0 |
| Show-o2-7B | direct | sat | t4 | transform/rot180/oracle | oracle | 24.5 | 98 | 400 | 400 | 0 |
| Show-o2-7B | direct | sat | t4 | transform/rot270/direct | direct | 22.0 | 88 | 400 | 400 | 0 |
| Show-o2-7B | direct | sat | t4 | transform/rot270/oracle | oracle | 25.0 | 100 | 400 | 400 | 0 |
| Show-o2-7B | direct | sat | t4 | transform/rot90/direct | direct | 22.2 | 89 | 400 | 400 | 0 |
| Show-o2-7B | direct | sat | t4 | transform/rot90/oracle | oracle | 25.5 | 102 | 400 | 400 | 0 |
| Show-o2-7B | direct | sat | t4 | world/intervention_001/direct | direct | 35.5 | 71 | 200 | 200 | 0 |
| Show-o2-7B | direct | sat | t4 | world/intervention_001/oracle | oracle | 51.0 | 102 | 200 | 200 | 0 |
| Show-o2-7B | direct | sat | t4 | world/sham_001/direct | direct | 17.5 | 35 | 200 | 200 | 0 |
| Show-o2-7B | direct | sat | t4 | world/sham_001/oracle | oracle | 24.5 | 49 | 200 | 200 | 0 |
| Show-o2-7B | direct | webrd04 | t1 | base/direct | direct | 43.8 | 175 | 400 | 400 | 0 |
| Show-o2-7B | direct | webrd04 | t1 | base/oracle | oracle | 40.2 | 161 | 400 | 400 | 0 |
| Show-o2-7B | direct | webrd04 | t2 | base/direct | direct | 40.8 | 163 | 400 | 400 | 0 |
| Show-o2-7B | direct | webrd04 | t2 | base/oracle | oracle | 49.5 | 198 | 400 | 400 | 0 |
| Show-o2-7B | direct | webrd04 | t3 | base/direct | direct | 50.5 | 101 | 200 | 200 | 0 |
| Show-o2-7B | direct | webrd04 | t3 | base/oracle | oracle | 57.0 | 114 | 200 | 200 | 0 |
| Show-o2-7B | direct | webrd04 | t3 | world/intervention_001/direct | direct | 21.5 | 43 | 200 | 200 | 0 |
| Show-o2-7B | direct | webrd04 | t3 | world/intervention_001/oracle | oracle | 21.5 | 43 | 200 | 200 | 0 |
| Show-o2-7B | direct | webrd04 | t3 | world/sham_001/direct | direct | 48.0 | 96 | 200 | 200 | 0 |
| Show-o2-7B | direct | webrd04 | t3 | world/sham_001/oracle | oracle | 55.5 | 111 | 200 | 200 | 0 |
| Show-o2-7B | direct | webrd04 | t4 | base/direct | direct | 24.2 | 97 | 400 | 400 | 0 |
| Show-o2-7B | direct | webrd04 | t4 | base/oracle | oracle | 27.2 | 109 | 400 | 400 | 0 |
| Show-o2-7B | direct | webrd04 | t4 | world/intervention_001/direct | direct | 37.0 | 74 | 200 | 200 | 0 |
| Show-o2-7B | direct | webrd04 | t4 | world/intervention_001/oracle | oracle | 52.5 | 105 | 200 | 200 | 0 |
| Show-o2-7B | direct | webrd04 | t4 | world/sham_001/direct | direct | 20.5 | 41 | 200 | 200 | 0 |
| Show-o2-7B | direct | webrd04 | t4 | world/sham_001/oracle | oracle | 23.0 | 46 | 200 | 200 | 0 |
| Show-o2-7B | direct | wprd01 | t1 | base/direct | direct | 60.2 | 241 | 400 | 400 | 0 |
| Show-o2-7B | direct | wprd01 | t1 | base/oracle | oracle | 43.0 | 172 | 400 | 400 | 0 |
| Show-o2-7B | direct | wprd01 | t1 | transform/mirror_h/direct | direct | 29.0 | 116 | 400 | 400 | 0 |
| Show-o2-7B | direct | wprd01 | t1 | transform/mirror_h/oracle | oracle | 30.0 | 120 | 400 | 400 | 0 |
| Show-o2-7B | direct | wprd01 | t1 | transform/mirror_h_rot180/direct | direct | 32.2 | 129 | 400 | 400 | 0 |
| Show-o2-7B | direct | wprd01 | t1 | transform/mirror_h_rot180/oracle | oracle | 33.2 | 133 | 400 | 400 | 0 |
| Show-o2-7B | direct | wprd01 | t1 | transform/mirror_h_rot270/direct | direct | 18.2 | 73 | 400 | 400 | 0 |
| Show-o2-7B | direct | wprd01 | t1 | transform/mirror_h_rot270/oracle | oracle | 19.8 | 79 | 400 | 400 | 0 |
| Show-o2-7B | direct | wprd01 | t1 | transform/mirror_h_rot90/direct | direct | 21.8 | 87 | 400 | 400 | 0 |
| Show-o2-7B | direct | wprd01 | t1 | transform/mirror_h_rot90/oracle | oracle | 22.0 | 88 | 400 | 400 | 0 |
| Show-o2-7B | direct | wprd01 | t1 | transform/rot180/direct | direct | 41.8 | 167 | 400 | 400 | 0 |
| Show-o2-7B | direct | wprd01 | t1 | transform/rot180/oracle | oracle | 42.8 | 171 | 400 | 400 | 0 |
| Show-o2-7B | direct | wprd01 | t1 | transform/rot270/direct | direct | 53.5 | 214 | 400 | 400 | 0 |
| Show-o2-7B | direct | wprd01 | t1 | transform/rot270/oracle | oracle | 49.8 | 199 | 400 | 400 | 0 |
| Show-o2-7B | direct | wprd01 | t1 | transform/rot90/direct | direct | 46.0 | 184 | 400 | 400 | 0 |
| Show-o2-7B | direct | wprd01 | t1 | transform/rot90/oracle | oracle | 48.2 | 193 | 400 | 400 | 0 |
| Show-o2-7B | direct | wprd01 | t2 | base/direct | direct | 43.0 | 172 | 400 | 400 | 0 |
| Show-o2-7B | direct | wprd01 | t2 | base/oracle | oracle | 49.5 | 198 | 400 | 400 | 0 |
| Show-o2-7B | direct | wprd01 | t2 | transform/mirror_h/direct | direct | 41.2 | 165 | 400 | 400 | 0 |
| Show-o2-7B | direct | wprd01 | t2 | transform/mirror_h/oracle | oracle | 51.2 | 205 | 400 | 400 | 0 |
| Show-o2-7B | direct | wprd01 | t2 | transform/mirror_h_rot180/direct | direct | 47.2 | 189 | 400 | 400 | 0 |
| Show-o2-7B | direct | wprd01 | t2 | transform/mirror_h_rot180/oracle | oracle | 52.8 | 211 | 400 | 400 | 0 |
| Show-o2-7B | direct | wprd01 | t2 | transform/mirror_h_rot270/direct | direct | 45.0 | 180 | 400 | 400 | 0 |
| Show-o2-7B | direct | wprd01 | t2 | transform/mirror_h_rot270/oracle | oracle | 48.8 | 195 | 400 | 400 | 0 |
| Show-o2-7B | direct | wprd01 | t2 | transform/mirror_h_rot90/direct | direct | 44.0 | 176 | 400 | 400 | 0 |
| Show-o2-7B | direct | wprd01 | t2 | transform/mirror_h_rot90/oracle | oracle | 49.5 | 198 | 400 | 400 | 0 |
| Show-o2-7B | direct | wprd01 | t2 | transform/rot180/direct | direct | 44.8 | 179 | 400 | 400 | 0 |
| Show-o2-7B | direct | wprd01 | t2 | transform/rot180/oracle | oracle | 50.8 | 203 | 400 | 400 | 0 |
| Show-o2-7B | direct | wprd01 | t2 | transform/rot270/direct | direct | 45.2 | 181 | 400 | 400 | 0 |
| Show-o2-7B | direct | wprd01 | t2 | transform/rot270/oracle | oracle | 46.2 | 185 | 400 | 400 | 0 |
| Show-o2-7B | direct | wprd01 | t2 | transform/rot90/direct | direct | 45.2 | 181 | 400 | 400 | 0 |
| Show-o2-7B | direct | wprd01 | t2 | transform/rot90/oracle | oracle | 47.0 | 188 | 400 | 400 | 0 |
| Show-o2-7B | direct | wprd01 | t3 | base/direct | direct | 56.0 | 112 | 200 | 200 | 0 |
| Show-o2-7B | direct | wprd01 | t3 | base/oracle | oracle | 60.5 | 121 | 200 | 200 | 0 |
| Show-o2-7B | direct | wprd01 | t3 | transform/mirror_h/direct | direct | 55.5 | 111 | 200 | 200 | 0 |
| Show-o2-7B | direct | wprd01 | t3 | transform/mirror_h/oracle | oracle | 66.0 | 132 | 200 | 200 | 0 |
| Show-o2-7B | direct | wprd01 | t3 | transform/mirror_h_rot180/direct | direct | 58.0 | 116 | 200 | 200 | 0 |
| Show-o2-7B | direct | wprd01 | t3 | transform/mirror_h_rot180/oracle | oracle | 63.5 | 127 | 200 | 200 | 0 |
| Show-o2-7B | direct | wprd01 | t3 | transform/mirror_h_rot270/direct | direct | 53.0 | 106 | 200 | 200 | 0 |
| Show-o2-7B | direct | wprd01 | t3 | transform/mirror_h_rot270/oracle | oracle | 58.5 | 117 | 200 | 200 | 0 |
| Show-o2-7B | direct | wprd01 | t3 | transform/mirror_h_rot90/direct | direct | 52.5 | 105 | 200 | 200 | 0 |
| Show-o2-7B | direct | wprd01 | t3 | transform/mirror_h_rot90/oracle | oracle | 59.5 | 119 | 200 | 200 | 0 |
| Show-o2-7B | direct | wprd01 | t3 | transform/rot180/direct | direct | 54.5 | 109 | 200 | 200 | 0 |
| Show-o2-7B | direct | wprd01 | t3 | transform/rot180/oracle | oracle | 64.5 | 129 | 200 | 200 | 0 |
| Show-o2-7B | direct | wprd01 | t3 | transform/rot270/direct | direct | 51.5 | 103 | 200 | 200 | 0 |
| Show-o2-7B | direct | wprd01 | t3 | transform/rot270/oracle | oracle | 58.0 | 116 | 200 | 200 | 0 |
| Show-o2-7B | direct | wprd01 | t3 | transform/rot90/direct | direct | 55.0 | 110 | 200 | 200 | 0 |
| Show-o2-7B | direct | wprd01 | t3 | transform/rot90/oracle | oracle | 62.5 | 125 | 200 | 200 | 0 |
| Show-o2-7B | direct | wprd01 | t3 | world/intervention_001/direct | direct | 27.5 | 55 | 200 | 200 | 0 |
| Show-o2-7B | direct | wprd01 | t3 | world/intervention_001/oracle | oracle | 31.0 | 62 | 200 | 200 | 0 |
| Show-o2-7B | direct | wprd01 | t3 | world/sham_001/direct | direct | 51.0 | 102 | 200 | 200 | 0 |
| Show-o2-7B | direct | wprd01 | t3 | world/sham_001/oracle | oracle | 59.5 | 119 | 200 | 200 | 0 |
| Show-o2-7B | direct | wprd01 | t4 | base/direct | direct | 23.8 | 95 | 400 | 400 | 0 |
| Show-o2-7B | direct | wprd01 | t4 | base/oracle | oracle | 26.2 | 105 | 400 | 400 | 0 |
| Show-o2-7B | direct | wprd01 | t4 | transform/mirror_h/direct | direct | 25.0 | 100 | 400 | 400 | 0 |
| Show-o2-7B | direct | wprd01 | t4 | transform/mirror_h/oracle | oracle | 27.0 | 108 | 400 | 400 | 0 |
| Show-o2-7B | direct | wprd01 | t4 | transform/mirror_h_rot180/direct | direct | 22.0 | 88 | 400 | 400 | 0 |
| Show-o2-7B | direct | wprd01 | t4 | transform/mirror_h_rot180/oracle | oracle | 27.0 | 108 | 400 | 400 | 0 |
| Show-o2-7B | direct | wprd01 | t4 | transform/mirror_h_rot270/direct | direct | 24.0 | 96 | 400 | 400 | 0 |
| Show-o2-7B | direct | wprd01 | t4 | transform/mirror_h_rot270/oracle | oracle | 25.5 | 102 | 400 | 400 | 0 |
| Show-o2-7B | direct | wprd01 | t4 | transform/mirror_h_rot90/direct | direct | 22.0 | 88 | 400 | 400 | 0 |
| Show-o2-7B | direct | wprd01 | t4 | transform/mirror_h_rot90/oracle | oracle | 27.5 | 110 | 400 | 400 | 0 |
| Show-o2-7B | direct | wprd01 | t4 | transform/rot180/direct | direct | 23.5 | 94 | 400 | 400 | 0 |
| Show-o2-7B | direct | wprd01 | t4 | transform/rot180/oracle | oracle | 27.2 | 109 | 400 | 400 | 0 |
| Show-o2-7B | direct | wprd01 | t4 | transform/rot270/direct | direct | 23.8 | 95 | 400 | 400 | 0 |
| Show-o2-7B | direct | wprd01 | t4 | transform/rot270/oracle | oracle | 26.0 | 104 | 400 | 400 | 0 |
| Show-o2-7B | direct | wprd01 | t4 | transform/rot90/direct | direct | 23.8 | 95 | 400 | 400 | 0 |
| Show-o2-7B | direct | wprd01 | t4 | transform/rot90/oracle | oracle | 28.0 | 112 | 400 | 400 | 0 |
| Show-o2-7B | direct | wprd01 | t4 | world/intervention_001/direct | direct | 35.5 | 71 | 200 | 200 | 0 |
| Show-o2-7B | direct | wprd01 | t4 | world/intervention_001/oracle | oracle | 54.0 | 108 | 200 | 200 | 0 |
| Show-o2-7B | direct | wprd01 | t4 | world/sham_001/direct | direct | 21.0 | 42 | 200 | 200 | 0 |
| Show-o2-7B | direct | wprd01 | t4 | world/sham_001/oracle | oracle | 26.5 | 53 | 200 | 200 | 0 |
| BLIP3o-8B | direct | blank | t1 | base/direct | direct | 34.8 | 139 | 400 | 400 | 0 |
| BLIP3o-8B | direct | blank | t1 | base/oracle | oracle | 35.2 | 141 | 400 | 400 | 0 |
| BLIP3o-8B | direct | blank | t1 | transform/mirror_h/direct | direct | 21.0 | 84 | 400 | 400 | 0 |
| BLIP3o-8B | direct | blank | t1 | transform/mirror_h/oracle | oracle | 24.0 | 96 | 400 | 400 | 0 |
| BLIP3o-8B | direct | blank | t1 | transform/mirror_h_rot180/direct | direct | 27.8 | 111 | 400 | 400 | 0 |
| BLIP3o-8B | direct | blank | t1 | transform/mirror_h_rot180/oracle | oracle | 27.0 | 108 | 400 | 400 | 0 |
| BLIP3o-8B | direct | blank | t1 | transform/mirror_h_rot270/direct | direct | 16.5 | 66 | 400 | 400 | 0 |
| BLIP3o-8B | direct | blank | t1 | transform/mirror_h_rot270/oracle | oracle | 17.2 | 69 | 400 | 400 | 0 |
| BLIP3o-8B | direct | blank | t1 | transform/mirror_h_rot90/direct | direct | 14.8 | 59 | 400 | 400 | 0 |
| BLIP3o-8B | direct | blank | t1 | transform/mirror_h_rot90/oracle | oracle | 13.8 | 55 | 400 | 400 | 0 |
| BLIP3o-8B | direct | blank | t1 | transform/rot180/direct | direct | 37.8 | 151 | 400 | 400 | 0 |
| BLIP3o-8B | direct | blank | t1 | transform/rot180/oracle | oracle | 37.5 | 150 | 400 | 400 | 0 |
| BLIP3o-8B | direct | blank | t1 | transform/rot270/direct | direct | 45.2 | 181 | 400 | 400 | 0 |
| BLIP3o-8B | direct | blank | t1 | transform/rot270/oracle | oracle | 46.5 | 186 | 400 | 400 | 0 |
| BLIP3o-8B | direct | blank | t1 | transform/rot90/direct | direct | 44.8 | 179 | 400 | 400 | 0 |
| BLIP3o-8B | direct | blank | t1 | transform/rot90/oracle | oracle | 43.8 | 175 | 400 | 400 | 0 |
| BLIP3o-8B | direct | blank | t2 | base/direct | direct | 42.0 | 168 | 400 | 400 | 0 |
| BLIP3o-8B | direct | blank | t2 | base/oracle | oracle | 42.5 | 170 | 400 | 400 | 0 |
| BLIP3o-8B | direct | blank | t2 | transform/mirror_h/direct | direct | 44.8 | 179 | 400 | 400 | 0 |
| BLIP3o-8B | direct | blank | t2 | transform/mirror_h/oracle | oracle | 46.0 | 184 | 400 | 400 | 0 |
| BLIP3o-8B | direct | blank | t2 | transform/mirror_h_rot180/direct | direct | 43.5 | 174 | 400 | 400 | 0 |
| BLIP3o-8B | direct | blank | t2 | transform/mirror_h_rot180/oracle | oracle | 43.5 | 174 | 400 | 400 | 0 |
| BLIP3o-8B | direct | blank | t2 | transform/mirror_h_rot270/direct | direct | 43.2 | 173 | 400 | 400 | 0 |
| BLIP3o-8B | direct | blank | t2 | transform/mirror_h_rot270/oracle | oracle | 43.0 | 172 | 400 | 400 | 0 |
| BLIP3o-8B | direct | blank | t2 | transform/mirror_h_rot90/direct | direct | 46.0 | 184 | 400 | 400 | 0 |
| BLIP3o-8B | direct | blank | t2 | transform/mirror_h_rot90/oracle | oracle | 45.2 | 181 | 400 | 400 | 0 |
| BLIP3o-8B | direct | blank | t2 | transform/rot180/direct | direct | 45.0 | 180 | 400 | 400 | 0 |
| BLIP3o-8B | direct | blank | t2 | transform/rot180/oracle | oracle | 46.2 | 185 | 400 | 400 | 0 |
| BLIP3o-8B | direct | blank | t2 | transform/rot270/direct | direct | 44.8 | 179 | 400 | 400 | 0 |
| BLIP3o-8B | direct | blank | t2 | transform/rot270/oracle | oracle | 44.2 | 177 | 400 | 400 | 0 |
| BLIP3o-8B | direct | blank | t2 | transform/rot90/direct | direct | 43.8 | 175 | 400 | 400 | 0 |
| BLIP3o-8B | direct | blank | t2 | transform/rot90/oracle | oracle | 44.5 | 178 | 400 | 400 | 0 |
| BLIP3o-8B | direct | sat | t1 | base/direct | direct | 36.2 | 145 | 400 | 400 | 0 |
| BLIP3o-8B | direct | sat | t1 | base/oracle | oracle | 36.2 | 145 | 400 | 400 | 0 |
| BLIP3o-8B | direct | sat | t1 | transform/mirror_h/direct | direct | 22.0 | 88 | 400 | 400 | 0 |
| BLIP3o-8B | direct | sat | t1 | transform/mirror_h/oracle | oracle | 24.8 | 99 | 400 | 400 | 0 |
| BLIP3o-8B | direct | sat | t1 | transform/mirror_h_rot180/direct | direct | 26.2 | 105 | 400 | 400 | 0 |
| BLIP3o-8B | direct | sat | t1 | transform/mirror_h_rot180/oracle | oracle | 26.2 | 105 | 400 | 400 | 0 |
| BLIP3o-8B | direct | sat | t1 | transform/mirror_h_rot270/direct | direct | 16.8 | 67 | 400 | 400 | 0 |
| BLIP3o-8B | direct | sat | t1 | transform/mirror_h_rot270/oracle | oracle | 20.0 | 80 | 400 | 400 | 0 |
| BLIP3o-8B | direct | sat | t1 | transform/mirror_h_rot90/direct | direct | 17.2 | 69 | 400 | 400 | 0 |
| BLIP3o-8B | direct | sat | t1 | transform/mirror_h_rot90/oracle | oracle | 19.2 | 77 | 400 | 400 | 0 |
| BLIP3o-8B | direct | sat | t1 | transform/rot180/direct | direct | 38.0 | 152 | 400 | 400 | 0 |
| BLIP3o-8B | direct | sat | t1 | transform/rot180/oracle | oracle | 38.2 | 153 | 400 | 400 | 0 |
| BLIP3o-8B | direct | sat | t1 | transform/rot270/direct | direct | 42.2 | 169 | 400 | 400 | 0 |
| BLIP3o-8B | direct | sat | t1 | transform/rot270/oracle | oracle | 44.8 | 179 | 400 | 400 | 0 |
| BLIP3o-8B | direct | sat | t1 | transform/rot90/direct | direct | 44.5 | 178 | 400 | 400 | 0 |
| BLIP3o-8B | direct | sat | t1 | transform/rot90/oracle | oracle | 44.8 | 179 | 400 | 400 | 0 |
| BLIP3o-8B | direct | sat | t2 | base/direct | direct | 43.8 | 175 | 400 | 400 | 0 |
| BLIP3o-8B | direct | sat | t2 | base/oracle | oracle | 43.5 | 174 | 400 | 400 | 0 |
| BLIP3o-8B | direct | sat | t2 | transform/mirror_h/direct | direct | 45.5 | 182 | 400 | 400 | 0 |
| BLIP3o-8B | direct | sat | t2 | transform/mirror_h/oracle | oracle | 45.2 | 181 | 400 | 400 | 0 |
| BLIP3o-8B | direct | sat | t2 | transform/mirror_h_rot180/direct | direct | 43.8 | 175 | 400 | 400 | 0 |
| BLIP3o-8B | direct | sat | t2 | transform/mirror_h_rot180/oracle | oracle | 46.0 | 184 | 400 | 400 | 0 |
| BLIP3o-8B | direct | sat | t2 | transform/mirror_h_rot270/direct | direct | 47.0 | 188 | 400 | 400 | 0 |
| BLIP3o-8B | direct | sat | t2 | transform/mirror_h_rot270/oracle | oracle | 47.2 | 189 | 400 | 400 | 0 |
| BLIP3o-8B | direct | sat | t2 | transform/mirror_h_rot90/direct | direct | 45.2 | 181 | 400 | 400 | 0 |
| BLIP3o-8B | direct | sat | t2 | transform/mirror_h_rot90/oracle | oracle | 44.0 | 176 | 400 | 400 | 0 |
| BLIP3o-8B | direct | sat | t2 | transform/rot180/direct | direct | 48.2 | 193 | 400 | 400 | 0 |
| BLIP3o-8B | direct | sat | t2 | transform/rot180/oracle | oracle | 47.8 | 191 | 400 | 400 | 0 |
| BLIP3o-8B | direct | sat | t2 | transform/rot270/direct | direct | 46.8 | 187 | 400 | 400 | 0 |
| BLIP3o-8B | direct | sat | t2 | transform/rot270/oracle | oracle | 46.8 | 187 | 400 | 400 | 0 |
| BLIP3o-8B | direct | sat | t2 | transform/rot90/direct | direct | 47.8 | 191 | 400 | 400 | 0 |
| BLIP3o-8B | direct | sat | t2 | transform/rot90/oracle | oracle | 45.2 | 181 | 400 | 400 | 0 |
| BLIP3o-8B | direct | sat | t3 | base/direct | direct | 33.0 | 66 | 200 | 200 | 0 |
| BLIP3o-8B | direct | sat | t3 | base/oracle | oracle | 32.0 | 64 | 200 | 200 | 0 |
| BLIP3o-8B | direct | sat | t3 | transform/mirror_h/direct | direct | 34.5 | 69 | 200 | 200 | 0 |
| BLIP3o-8B | direct | sat | t3 | transform/mirror_h/oracle | oracle | 33.5 | 67 | 200 | 200 | 0 |
| BLIP3o-8B | direct | sat | t3 | transform/mirror_h_rot180/direct | direct | 34.5 | 69 | 200 | 200 | 0 |
| BLIP3o-8B | direct | sat | t3 | transform/mirror_h_rot180/oracle | oracle | 32.5 | 65 | 200 | 200 | 0 |
| BLIP3o-8B | direct | sat | t3 | transform/mirror_h_rot270/direct | direct | 35.5 | 71 | 200 | 200 | 0 |
| BLIP3o-8B | direct | sat | t3 | transform/mirror_h_rot270/oracle | oracle | 34.5 | 69 | 200 | 200 | 0 |
| BLIP3o-8B | direct | sat | t3 | transform/mirror_h_rot90/direct | direct | 34.5 | 69 | 200 | 200 | 0 |
| BLIP3o-8B | direct | sat | t3 | transform/mirror_h_rot90/oracle | oracle | 37.0 | 74 | 200 | 200 | 0 |
| BLIP3o-8B | direct | sat | t3 | transform/rot180/direct | direct | 36.0 | 72 | 200 | 200 | 0 |
| BLIP3o-8B | direct | sat | t3 | transform/rot180/oracle | oracle | 33.0 | 66 | 200 | 200 | 0 |
| BLIP3o-8B | direct | sat | t3 | transform/rot270/direct | direct | 38.0 | 76 | 200 | 200 | 0 |
| BLIP3o-8B | direct | sat | t3 | transform/rot270/oracle | oracle | 37.0 | 74 | 200 | 200 | 0 |
| BLIP3o-8B | direct | sat | t3 | transform/rot90/direct | direct | 37.5 | 75 | 200 | 200 | 0 |
| BLIP3o-8B | direct | sat | t3 | transform/rot90/oracle | oracle | 37.0 | 74 | 200 | 200 | 0 |
| BLIP3o-8B | direct | sat | t3 | world/intervention_001/direct | direct | 43.5 | 87 | 200 | 200 | 0 |
| BLIP3o-8B | direct | sat | t3 | world/intervention_001/oracle | oracle | 43.5 | 87 | 200 | 200 | 0 |
| BLIP3o-8B | direct | sat | t3 | world/sham_001/direct | direct | 30.0 | 60 | 200 | 200 | 0 |
| BLIP3o-8B | direct | sat | t3 | world/sham_001/oracle | oracle | 28.5 | 57 | 200 | 200 | 0 |
| BLIP3o-8B | direct | sat | t4 | base/direct | direct | 33.8 | 135 | 400 | 400 | 0 |
| BLIP3o-8B | direct | sat | t4 | base/oracle | oracle | 32.2 | 129 | 400 | 400 | 0 |
| BLIP3o-8B | direct | sat | t4 | transform/mirror_h/direct | direct | 33.0 | 132 | 400 | 400 | 0 |
| BLIP3o-8B | direct | sat | t4 | transform/mirror_h/oracle | oracle | 33.8 | 135 | 400 | 400 | 0 |
| BLIP3o-8B | direct | sat | t4 | transform/mirror_h_rot180/direct | direct | 33.5 | 134 | 400 | 400 | 0 |
| BLIP3o-8B | direct | sat | t4 | transform/mirror_h_rot180/oracle | oracle | 32.5 | 130 | 400 | 400 | 0 |
| BLIP3o-8B | direct | sat | t4 | transform/mirror_h_rot270/direct | direct | 32.2 | 129 | 400 | 400 | 0 |
| BLIP3o-8B | direct | sat | t4 | transform/mirror_h_rot270/oracle | oracle | 32.0 | 128 | 400 | 400 | 0 |
| BLIP3o-8B | direct | sat | t4 | transform/mirror_h_rot90/direct | direct | 31.8 | 127 | 400 | 400 | 0 |
| BLIP3o-8B | direct | sat | t4 | transform/mirror_h_rot90/oracle | oracle | 32.5 | 130 | 400 | 400 | 0 |
| BLIP3o-8B | direct | sat | t4 | transform/rot180/direct | direct | 33.5 | 134 | 400 | 400 | 0 |
| BLIP3o-8B | direct | sat | t4 | transform/rot180/oracle | oracle | 32.5 | 130 | 400 | 400 | 0 |
| BLIP3o-8B | direct | sat | t4 | transform/rot270/direct | direct | 32.8 | 131 | 400 | 400 | 0 |
| BLIP3o-8B | direct | sat | t4 | transform/rot270/oracle | oracle | 32.5 | 130 | 400 | 400 | 0 |
| BLIP3o-8B | direct | sat | t4 | transform/rot90/direct | direct | 33.0 | 132 | 400 | 400 | 0 |
| BLIP3o-8B | direct | sat | t4 | transform/rot90/oracle | oracle | 32.2 | 129 | 400 | 400 | 0 |
| BLIP3o-8B | direct | sat | t4 | world/intervention_001/direct | direct | 13.0 | 26 | 200 | 200 | 0 |
| BLIP3o-8B | direct | sat | t4 | world/intervention_001/oracle | oracle | 14.5 | 29 | 200 | 200 | 0 |
| BLIP3o-8B | direct | sat | t4 | world/sham_001/direct | direct | 34.5 | 69 | 200 | 200 | 0 |
| BLIP3o-8B | direct | sat | t4 | world/sham_001/oracle | oracle | 32.5 | 65 | 200 | 200 | 0 |
| BLIP3o-8B | direct | webrd04 | t1 | base/direct | direct | 40.2 | 161 | 400 | 400 | 0 |
| BLIP3o-8B | direct | webrd04 | t1 | base/oracle | oracle | 42.5 | 170 | 400 | 400 | 0 |
| BLIP3o-8B | direct | webrd04 | t2 | base/direct | direct | 43.8 | 175 | 400 | 400 | 0 |
| BLIP3o-8B | direct | webrd04 | t2 | base/oracle | oracle | 42.0 | 168 | 400 | 400 | 0 |
| BLIP3o-8B | direct | webrd04 | t3 | base/direct | direct | 55.0 | 110 | 200 | 200 | 0 |
| BLIP3o-8B | direct | webrd04 | t3 | base/oracle | oracle | 54.0 | 108 | 200 | 200 | 0 |
| BLIP3o-8B | direct | webrd04 | t3 | world/intervention_001/direct | direct | 27.5 | 55 | 200 | 200 | 0 |
| BLIP3o-8B | direct | webrd04 | t3 | world/intervention_001/oracle | oracle | 26.5 | 53 | 200 | 200 | 0 |
| BLIP3o-8B | direct | webrd04 | t3 | world/sham_001/direct | direct | 54.0 | 108 | 200 | 200 | 0 |
| BLIP3o-8B | direct | webrd04 | t3 | world/sham_001/oracle | oracle | 54.5 | 109 | 200 | 200 | 0 |
| BLIP3o-8B | direct | webrd04 | t4 | base/direct | direct | 33.2 | 133 | 400 | 400 | 0 |
| BLIP3o-8B | direct | webrd04 | t4 | base/oracle | oracle | 32.2 | 129 | 400 | 400 | 0 |
| BLIP3o-8B | direct | webrd04 | t4 | world/intervention_001/direct | direct | 13.5 | 27 | 200 | 200 | 0 |
| BLIP3o-8B | direct | webrd04 | t4 | world/intervention_001/oracle | oracle | 13.0 | 26 | 200 | 200 | 0 |
| BLIP3o-8B | direct | webrd04 | t4 | world/sham_001/direct | direct | 34.0 | 68 | 200 | 200 | 0 |
| BLIP3o-8B | direct | webrd04 | t4 | world/sham_001/oracle | oracle | 32.5 | 65 | 200 | 200 | 0 |
| BLIP3o-8B | direct | wprd01 | t1 | base/direct | direct | 49.8 | 199 | 400 | 400 | 0 |
| BLIP3o-8B | direct | wprd01 | t1 | base/oracle | oracle | 38.0 | 152 | 400 | 400 | 0 |
| BLIP3o-8B | direct | wprd01 | t1 | transform/mirror_h/direct | direct | 19.8 | 79 | 400 | 400 | 0 |
| BLIP3o-8B | direct | wprd01 | t1 | transform/mirror_h/oracle | oracle | 19.2 | 77 | 400 | 400 | 0 |
| BLIP3o-8B | direct | wprd01 | t1 | transform/mirror_h_rot180/direct | direct | 20.8 | 83 | 400 | 400 | 0 |
| BLIP3o-8B | direct | wprd01 | t1 | transform/mirror_h_rot180/oracle | oracle | 19.8 | 79 | 400 | 400 | 0 |
| BLIP3o-8B | direct | wprd01 | t1 | transform/mirror_h_rot270/direct | direct | 19.0 | 76 | 400 | 400 | 0 |
| BLIP3o-8B | direct | wprd01 | t1 | transform/mirror_h_rot270/oracle | oracle | 18.0 | 72 | 400 | 400 | 0 |
| BLIP3o-8B | direct | wprd01 | t1 | transform/mirror_h_rot90/direct | direct | 15.8 | 63 | 400 | 400 | 0 |
| BLIP3o-8B | direct | wprd01 | t1 | transform/mirror_h_rot90/oracle | oracle | 13.5 | 54 | 400 | 400 | 0 |
| BLIP3o-8B | direct | wprd01 | t1 | transform/rot180/direct | direct | 36.5 | 146 | 400 | 400 | 0 |
| BLIP3o-8B | direct | wprd01 | t1 | transform/rot180/oracle | oracle | 35.8 | 143 | 400 | 400 | 0 |
| BLIP3o-8B | direct | wprd01 | t1 | transform/rot270/direct | direct | 38.2 | 153 | 400 | 400 | 0 |
| BLIP3o-8B | direct | wprd01 | t1 | transform/rot270/oracle | oracle | 39.8 | 159 | 400 | 400 | 0 |
| BLIP3o-8B | direct | wprd01 | t1 | transform/rot90/direct | direct | 42.0 | 168 | 400 | 400 | 0 |
| BLIP3o-8B | direct | wprd01 | t1 | transform/rot90/oracle | oracle | 40.2 | 161 | 400 | 400 | 0 |
| BLIP3o-8B | direct | wprd01 | t2 | base/direct | direct | 31.5 | 126 | 400 | 400 | 0 |
| BLIP3o-8B | direct | wprd01 | t2 | base/oracle | oracle | 42.2 | 169 | 400 | 400 | 0 |
| BLIP3o-8B | direct | wprd01 | t2 | transform/mirror_h/direct | direct | 45.2 | 181 | 400 | 400 | 0 |
| BLIP3o-8B | direct | wprd01 | t2 | transform/mirror_h/oracle | oracle | 44.0 | 176 | 400 | 400 | 0 |
| BLIP3o-8B | direct | wprd01 | t2 | transform/mirror_h_rot180/direct | direct | 43.0 | 172 | 400 | 400 | 0 |
| BLIP3o-8B | direct | wprd01 | t2 | transform/mirror_h_rot180/oracle | oracle | 42.8 | 171 | 400 | 400 | 0 |
| BLIP3o-8B | direct | wprd01 | t2 | transform/mirror_h_rot270/direct | direct | 43.0 | 172 | 400 | 400 | 0 |
| BLIP3o-8B | direct | wprd01 | t2 | transform/mirror_h_rot270/oracle | oracle | 44.5 | 178 | 400 | 400 | 0 |
| BLIP3o-8B | direct | wprd01 | t2 | transform/mirror_h_rot90/direct | direct | 45.0 | 180 | 400 | 400 | 0 |
| BLIP3o-8B | direct | wprd01 | t2 | transform/mirror_h_rot90/oracle | oracle | 45.0 | 180 | 400 | 400 | 0 |
| BLIP3o-8B | direct | wprd01 | t2 | transform/rot180/direct | direct | 46.0 | 184 | 400 | 400 | 0 |
| BLIP3o-8B | direct | wprd01 | t2 | transform/rot180/oracle | oracle | 44.8 | 179 | 400 | 400 | 0 |
| BLIP3o-8B | direct | wprd01 | t2 | transform/rot270/direct | direct | 46.2 | 185 | 400 | 400 | 0 |
| BLIP3o-8B | direct | wprd01 | t2 | transform/rot270/oracle | oracle | 45.0 | 180 | 400 | 400 | 0 |
| BLIP3o-8B | direct | wprd01 | t2 | transform/rot90/direct | direct | 45.0 | 180 | 400 | 400 | 0 |
| BLIP3o-8B | direct | wprd01 | t2 | transform/rot90/oracle | oracle | 46.2 | 185 | 400 | 400 | 0 |
| BLIP3o-8B | direct | wprd01 | t3 | base/direct | direct | 36.0 | 72 | 200 | 200 | 0 |
| BLIP3o-8B | direct | wprd01 | t3 | base/oracle | oracle | 38.5 | 77 | 200 | 200 | 0 |
| BLIP3o-8B | direct | wprd01 | t3 | transform/mirror_h/direct | direct | 38.0 | 76 | 200 | 200 | 0 |
| BLIP3o-8B | direct | wprd01 | t3 | transform/mirror_h/oracle | oracle | 39.0 | 78 | 200 | 200 | 0 |
| BLIP3o-8B | direct | wprd01 | t3 | transform/mirror_h_rot180/direct | direct | 33.5 | 67 | 200 | 200 | 0 |
| BLIP3o-8B | direct | wprd01 | t3 | transform/mirror_h_rot180/oracle | oracle | 37.0 | 74 | 200 | 200 | 0 |
| BLIP3o-8B | direct | wprd01 | t3 | transform/mirror_h_rot270/direct | direct | 34.0 | 68 | 200 | 200 | 0 |
| BLIP3o-8B | direct | wprd01 | t3 | transform/mirror_h_rot270/oracle | oracle | 38.5 | 77 | 200 | 200 | 0 |
| BLIP3o-8B | direct | wprd01 | t3 | transform/mirror_h_rot90/direct | direct | 33.5 | 67 | 200 | 200 | 0 |
| BLIP3o-8B | direct | wprd01 | t3 | transform/mirror_h_rot90/oracle | oracle | 40.0 | 80 | 200 | 200 | 0 |
| BLIP3o-8B | direct | wprd01 | t3 | transform/rot180/direct | direct | 37.5 | 75 | 200 | 200 | 0 |
| BLIP3o-8B | direct | wprd01 | t3 | transform/rot180/oracle | oracle | 39.5 | 79 | 200 | 200 | 0 |
| BLIP3o-8B | direct | wprd01 | t3 | transform/rot270/direct | direct | 35.0 | 70 | 200 | 200 | 0 |
| BLIP3o-8B | direct | wprd01 | t3 | transform/rot270/oracle | oracle | 39.5 | 79 | 200 | 200 | 0 |
| BLIP3o-8B | direct | wprd01 | t3 | transform/rot90/direct | direct | 32.0 | 64 | 200 | 200 | 0 |
| BLIP3o-8B | direct | wprd01 | t3 | transform/rot90/oracle | oracle | 36.0 | 72 | 200 | 200 | 0 |
| BLIP3o-8B | direct | wprd01 | t3 | world/intervention_001/direct | direct | 36.5 | 73 | 200 | 200 | 0 |
| BLIP3o-8B | direct | wprd01 | t3 | world/intervention_001/oracle | oracle | 37.5 | 75 | 200 | 200 | 0 |
| BLIP3o-8B | direct | wprd01 | t3 | world/sham_001/direct | direct | 32.0 | 64 | 200 | 200 | 0 |
| BLIP3o-8B | direct | wprd01 | t3 | world/sham_001/oracle | oracle | 31.0 | 62 | 200 | 200 | 0 |
| BLIP3o-8B | direct | wprd01 | t4 | base/direct | direct | 34.2 | 137 | 400 | 400 | 0 |
| BLIP3o-8B | direct | wprd01 | t4 | base/oracle | oracle | 34.0 | 136 | 400 | 400 | 0 |
| BLIP3o-8B | direct | wprd01 | t4 | transform/mirror_h/direct | direct | 35.8 | 143 | 400 | 400 | 0 |
| BLIP3o-8B | direct | wprd01 | t4 | transform/mirror_h/oracle | oracle | 34.2 | 137 | 400 | 400 | 0 |
| BLIP3o-8B | direct | wprd01 | t4 | transform/mirror_h_rot180/direct | direct | 35.8 | 143 | 400 | 400 | 0 |
| BLIP3o-8B | direct | wprd01 | t4 | transform/mirror_h_rot180/oracle | oracle | 34.5 | 138 | 400 | 400 | 0 |
| BLIP3o-8B | direct | wprd01 | t4 | transform/mirror_h_rot270/direct | direct | 34.2 | 137 | 400 | 400 | 0 |
| BLIP3o-8B | direct | wprd01 | t4 | transform/mirror_h_rot270/oracle | oracle | 34.0 | 136 | 400 | 400 | 0 |
| BLIP3o-8B | direct | wprd01 | t4 | transform/mirror_h_rot90/direct | direct | 34.2 | 137 | 400 | 400 | 0 |
| BLIP3o-8B | direct | wprd01 | t4 | transform/mirror_h_rot90/oracle | oracle | 33.8 | 135 | 400 | 400 | 0 |
| BLIP3o-8B | direct | wprd01 | t4 | transform/rot180/direct | direct | 35.0 | 140 | 400 | 400 | 0 |
| BLIP3o-8B | direct | wprd01 | t4 | transform/rot180/oracle | oracle | 34.8 | 139 | 400 | 400 | 0 |
| BLIP3o-8B | direct | wprd01 | t4 | transform/rot270/direct | direct | 33.8 | 135 | 400 | 400 | 0 |
| BLIP3o-8B | direct | wprd01 | t4 | transform/rot270/oracle | oracle | 35.5 | 142 | 400 | 400 | 0 |
| BLIP3o-8B | direct | wprd01 | t4 | transform/rot90/direct | direct | 36.0 | 144 | 400 | 400 | 0 |
| BLIP3o-8B | direct | wprd01 | t4 | transform/rot90/oracle | oracle | 34.8 | 139 | 400 | 400 | 0 |
| BLIP3o-8B | direct | wprd01 | t4 | world/intervention_001/direct | direct | 11.0 | 22 | 200 | 200 | 0 |
| BLIP3o-8B | direct | wprd01 | t4 | world/intervention_001/oracle | oracle | 13.5 | 27 | 200 | 200 | 0 |
| BLIP3o-8B | direct | wprd01 | t4 | world/sham_001/direct | direct | 36.0 | 72 | 200 | 200 | 0 |
| BLIP3o-8B | direct | wprd01 | t4 | world/sham_001/oracle | oracle | 31.0 | 62 | 200 | 200 | 0 |
| Cambrian-S-7B-LFP | direct | blank | t1 | base/direct | direct | 42.8 | 171 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | blank | t1 | base/oracle | oracle | 40.8 | 163 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | blank | t1 | transform/mirror_h/direct | direct | 24.0 | 96 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | blank | t1 | transform/mirror_h/oracle | oracle | 25.5 | 102 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | blank | t1 | transform/mirror_h_rot180/direct | direct | 23.2 | 93 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | blank | t1 | transform/mirror_h_rot180/oracle | oracle | 23.8 | 95 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | blank | t1 | transform/mirror_h_rot270/direct | direct | 14.5 | 58 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | blank | t1 | transform/mirror_h_rot270/oracle | oracle | 15.2 | 61 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | blank | t1 | transform/mirror_h_rot90/direct | direct | 20.8 | 83 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | blank | t1 | transform/mirror_h_rot90/oracle | oracle | 20.2 | 81 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | blank | t1 | transform/rot180/direct | direct | 46.0 | 184 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | blank | t1 | transform/rot180/oracle | oracle | 46.5 | 186 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | blank | t1 | transform/rot270/direct | direct | 48.5 | 194 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | blank | t1 | transform/rot270/oracle | oracle | 50.2 | 201 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | blank | t1 | transform/rot90/direct | direct | 47.8 | 191 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | blank | t1 | transform/rot90/oracle | oracle | 49.2 | 197 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | blank | t2 | base/direct | direct | 45.2 | 181 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | blank | t2 | base/oracle | oracle | 45.5 | 182 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | blank | t2 | transform/mirror_h/direct | direct | 46.0 | 184 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | blank | t2 | transform/mirror_h/oracle | oracle | 45.0 | 180 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | blank | t2 | transform/mirror_h_rot180/direct | direct | 46.2 | 185 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | blank | t2 | transform/mirror_h_rot180/oracle | oracle | 45.8 | 183 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | blank | t2 | transform/mirror_h_rot270/direct | direct | 47.5 | 190 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | blank | t2 | transform/mirror_h_rot270/oracle | oracle | 45.8 | 183 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | blank | t2 | transform/mirror_h_rot90/direct | direct | 45.5 | 182 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | blank | t2 | transform/mirror_h_rot90/oracle | oracle | 44.8 | 179 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | blank | t2 | transform/rot180/direct | direct | 46.2 | 185 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | blank | t2 | transform/rot180/oracle | oracle | 45.5 | 182 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | blank | t2 | transform/rot270/direct | direct | 46.8 | 187 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | blank | t2 | transform/rot270/oracle | oracle | 45.5 | 182 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | blank | t2 | transform/rot90/direct | direct | 46.5 | 186 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | blank | t2 | transform/rot90/oracle | oracle | 46.0 | 184 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | sat | t1 | base/direct | direct | 49.8 | 199 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | sat | t1 | base/oracle | oracle | 46.2 | 185 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | sat | t1 | transform/mirror_h/direct | direct | 28.5 | 114 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | sat | t1 | transform/mirror_h/oracle | oracle | 26.2 | 105 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | sat | t1 | transform/mirror_h_rot180/direct | direct | 28.5 | 114 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | sat | t1 | transform/mirror_h_rot180/oracle | oracle | 27.5 | 110 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | sat | t1 | transform/mirror_h_rot270/direct | direct | 20.8 | 83 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | sat | t1 | transform/mirror_h_rot270/oracle | oracle | 20.2 | 81 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | sat | t1 | transform/mirror_h_rot90/direct | direct | 27.8 | 111 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | sat | t1 | transform/mirror_h_rot90/oracle | oracle | 25.8 | 103 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | sat | t1 | transform/rot180/direct | direct | 51.8 | 207 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | sat | t1 | transform/rot180/oracle | oracle | 48.5 | 194 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | sat | t1 | transform/rot270/direct | direct | 53.0 | 212 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | sat | t1 | transform/rot270/oracle | oracle | 52.5 | 210 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | sat | t1 | transform/rot90/direct | direct | 54.2 | 217 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | sat | t1 | transform/rot90/oracle | oracle | 54.5 | 218 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | sat | t2 | base/direct | direct | 47.2 | 189 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | sat | t2 | base/oracle | oracle | 46.0 | 184 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | sat | t2 | transform/mirror_h/direct | direct | 46.8 | 187 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | sat | t2 | transform/mirror_h/oracle | oracle | 47.2 | 189 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | sat | t2 | transform/mirror_h_rot180/direct | direct | 46.5 | 186 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | sat | t2 | transform/mirror_h_rot180/oracle | oracle | 46.2 | 185 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | sat | t2 | transform/mirror_h_rot270/direct | direct | 48.0 | 192 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | sat | t2 | transform/mirror_h_rot270/oracle | oracle | 48.0 | 192 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | sat | t2 | transform/mirror_h_rot90/direct | direct | 45.2 | 181 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | sat | t2 | transform/mirror_h_rot90/oracle | oracle | 46.8 | 187 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | sat | t2 | transform/rot180/direct | direct | 47.0 | 188 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | sat | t2 | transform/rot180/oracle | oracle | 46.5 | 186 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | sat | t2 | transform/rot270/direct | direct | 45.5 | 182 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | sat | t2 | transform/rot270/oracle | oracle | 47.2 | 189 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | sat | t2 | transform/rot90/direct | direct | 45.8 | 183 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | sat | t2 | transform/rot90/oracle | oracle | 47.0 | 188 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | sat | t3 | base/direct | direct | 41.0 | 82 | 200 | 200 | 0 |
| Cambrian-S-7B-LFP | direct | sat | t3 | base/oracle | oracle | 41.0 | 82 | 200 | 200 | 0 |
| Cambrian-S-7B-LFP | direct | sat | t3 | transform/mirror_h/direct | direct | 39.0 | 78 | 200 | 200 | 0 |
| Cambrian-S-7B-LFP | direct | sat | t3 | transform/mirror_h/oracle | oracle | 42.5 | 85 | 200 | 200 | 0 |
| Cambrian-S-7B-LFP | direct | sat | t3 | transform/mirror_h_rot180/direct | direct | 38.5 | 77 | 200 | 200 | 0 |
| Cambrian-S-7B-LFP | direct | sat | t3 | transform/mirror_h_rot180/oracle | oracle | 39.5 | 79 | 200 | 200 | 0 |
| Cambrian-S-7B-LFP | direct | sat | t3 | transform/mirror_h_rot270/direct | direct | 42.0 | 84 | 200 | 200 | 0 |
| Cambrian-S-7B-LFP | direct | sat | t3 | transform/mirror_h_rot270/oracle | oracle | 42.5 | 85 | 200 | 200 | 0 |
| Cambrian-S-7B-LFP | direct | sat | t3 | transform/mirror_h_rot90/direct | direct | 39.0 | 78 | 200 | 200 | 0 |
| Cambrian-S-7B-LFP | direct | sat | t3 | transform/mirror_h_rot90/oracle | oracle | 41.5 | 83 | 200 | 200 | 0 |
| Cambrian-S-7B-LFP | direct | sat | t3 | transform/rot180/direct | direct | 41.0 | 82 | 200 | 200 | 0 |
| Cambrian-S-7B-LFP | direct | sat | t3 | transform/rot180/oracle | oracle | 41.0 | 82 | 200 | 200 | 0 |
| Cambrian-S-7B-LFP | direct | sat | t3 | transform/rot270/direct | direct | 41.5 | 83 | 200 | 200 | 0 |
| Cambrian-S-7B-LFP | direct | sat | t3 | transform/rot270/oracle | oracle | 39.5 | 79 | 200 | 200 | 0 |
| Cambrian-S-7B-LFP | direct | sat | t3 | transform/rot90/direct | direct | 40.0 | 80 | 200 | 200 | 0 |
| Cambrian-S-7B-LFP | direct | sat | t3 | transform/rot90/oracle | oracle | 41.5 | 83 | 200 | 200 | 0 |
| Cambrian-S-7B-LFP | direct | sat | t3 | world/intervention_001/direct | direct | 28.0 | 56 | 200 | 200 | 0 |
| Cambrian-S-7B-LFP | direct | sat | t3 | world/intervention_001/oracle | oracle | 27.0 | 54 | 200 | 200 | 0 |
| Cambrian-S-7B-LFP | direct | sat | t3 | world/sham_001/direct | direct | 40.5 | 81 | 200 | 200 | 0 |
| Cambrian-S-7B-LFP | direct | sat | t3 | world/sham_001/oracle | oracle | 41.5 | 83 | 200 | 200 | 0 |
| Cambrian-S-7B-LFP | direct | sat | t4 | base/direct | direct | 23.8 | 95 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | sat | t4 | base/oracle | oracle | 23.5 | 94 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | sat | t4 | transform/mirror_h/direct | direct | 23.8 | 95 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | sat | t4 | transform/mirror_h/oracle | oracle | 23.0 | 92 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | sat | t4 | transform/mirror_h_rot180/direct | direct | 23.8 | 95 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | sat | t4 | transform/mirror_h_rot180/oracle | oracle | 23.5 | 94 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | sat | t4 | transform/mirror_h_rot270/direct | direct | 21.2 | 85 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | sat | t4 | transform/mirror_h_rot270/oracle | oracle | 21.5 | 86 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | sat | t4 | transform/mirror_h_rot90/direct | direct | 21.8 | 87 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | sat | t4 | transform/mirror_h_rot90/oracle | oracle | 20.5 | 82 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | sat | t4 | transform/rot180/direct | direct | 22.2 | 89 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | sat | t4 | transform/rot180/oracle | oracle | 25.2 | 101 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | sat | t4 | transform/rot270/direct | direct | 22.5 | 90 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | sat | t4 | transform/rot270/oracle | oracle | 21.0 | 84 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | sat | t4 | transform/rot90/direct | direct | 21.0 | 84 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | sat | t4 | transform/rot90/oracle | oracle | 21.2 | 85 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | sat | t4 | world/intervention_001/direct | direct | 21.0 | 42 | 200 | 200 | 0 |
| Cambrian-S-7B-LFP | direct | sat | t4 | world/intervention_001/oracle | oracle | 19.5 | 39 | 200 | 200 | 0 |
| Cambrian-S-7B-LFP | direct | sat | t4 | world/sham_001/direct | direct | 14.5 | 29 | 200 | 200 | 0 |
| Cambrian-S-7B-LFP | direct | sat | t4 | world/sham_001/oracle | oracle | 14.5 | 29 | 200 | 200 | 0 |
| Cambrian-S-7B-LFP | direct | webrd04 | t1 | base/direct | direct | 40.5 | 162 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | webrd04 | t1 | base/oracle | oracle | 39.8 | 159 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | webrd04 | t2 | base/direct | direct | 45.2 | 181 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | webrd04 | t2 | base/oracle | oracle | 45.2 | 181 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | webrd04 | t3 | base/direct | direct | 35.0 | 70 | 200 | 200 | 0 |
| Cambrian-S-7B-LFP | direct | webrd04 | t3 | base/oracle | oracle | 32.0 | 64 | 200 | 200 | 0 |
| Cambrian-S-7B-LFP | direct | webrd04 | t3 | world/intervention_001/direct | direct | 13.5 | 27 | 200 | 200 | 0 |
| Cambrian-S-7B-LFP | direct | webrd04 | t3 | world/intervention_001/oracle | oracle | 13.0 | 26 | 200 | 200 | 0 |
| Cambrian-S-7B-LFP | direct | webrd04 | t3 | world/sham_001/direct | direct | 40.0 | 80 | 200 | 200 | 0 |
| Cambrian-S-7B-LFP | direct | webrd04 | t3 | world/sham_001/oracle | oracle | 39.0 | 78 | 200 | 200 | 0 |
| Cambrian-S-7B-LFP | direct | webrd04 | t4 | base/direct | direct | 26.5 | 106 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | webrd04 | t4 | base/oracle | oracle | 27.5 | 110 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | webrd04 | t4 | world/intervention_001/direct | direct | 14.0 | 28 | 200 | 200 | 0 |
| Cambrian-S-7B-LFP | direct | webrd04 | t4 | world/intervention_001/oracle | oracle | 14.0 | 28 | 200 | 200 | 0 |
| Cambrian-S-7B-LFP | direct | webrd04 | t4 | world/sham_001/direct | direct | 21.5 | 43 | 200 | 200 | 0 |
| Cambrian-S-7B-LFP | direct | webrd04 | t4 | world/sham_001/oracle | oracle | 22.5 | 45 | 200 | 200 | 0 |
| Cambrian-S-7B-LFP | direct | wprd01 | t1 | base/direct | direct | 39.8 | 159 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | wprd01 | t1 | base/oracle | oracle | 38.8 | 155 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | wprd01 | t1 | transform/mirror_h/direct | direct | 24.0 | 96 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | wprd01 | t1 | transform/mirror_h/oracle | oracle | 22.8 | 91 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | wprd01 | t1 | transform/mirror_h_rot180/direct | direct | 22.8 | 91 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | wprd01 | t1 | transform/mirror_h_rot180/oracle | oracle | 23.0 | 92 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | wprd01 | t1 | transform/mirror_h_rot270/direct | direct | 16.2 | 65 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | wprd01 | t1 | transform/mirror_h_rot270/oracle | oracle | 15.2 | 61 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | wprd01 | t1 | transform/mirror_h_rot90/direct | direct | 21.5 | 86 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | wprd01 | t1 | transform/mirror_h_rot90/oracle | oracle | 20.2 | 81 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | wprd01 | t1 | transform/rot180/direct | direct | 43.0 | 172 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | wprd01 | t1 | transform/rot180/oracle | oracle | 43.0 | 172 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | wprd01 | t1 | transform/rot270/direct | direct | 44.5 | 178 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | wprd01 | t1 | transform/rot270/oracle | oracle | 44.2 | 177 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | wprd01 | t1 | transform/rot90/direct | direct | 44.5 | 178 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | wprd01 | t1 | transform/rot90/oracle | oracle | 44.8 | 179 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | wprd01 | t2 | base/direct | direct | 46.0 | 184 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | wprd01 | t2 | base/oracle | oracle | 46.0 | 184 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | wprd01 | t2 | transform/mirror_h/direct | direct | 45.8 | 183 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | wprd01 | t2 | transform/mirror_h/oracle | oracle | 45.8 | 183 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | wprd01 | t2 | transform/mirror_h_rot180/direct | direct | 45.8 | 183 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | wprd01 | t2 | transform/mirror_h_rot180/oracle | oracle | 45.5 | 182 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | wprd01 | t2 | transform/mirror_h_rot270/direct | direct | 45.5 | 182 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | wprd01 | t2 | transform/mirror_h_rot270/oracle | oracle | 45.5 | 182 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | wprd01 | t2 | transform/mirror_h_rot90/direct | direct | 45.5 | 182 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | wprd01 | t2 | transform/mirror_h_rot90/oracle | oracle | 45.5 | 182 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | wprd01 | t2 | transform/rot180/direct | direct | 46.0 | 184 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | wprd01 | t2 | transform/rot180/oracle | oracle | 45.8 | 183 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | wprd01 | t2 | transform/rot270/direct | direct | 45.8 | 183 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | wprd01 | t2 | transform/rot270/oracle | oracle | 45.2 | 181 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | wprd01 | t2 | transform/rot90/direct | direct | 46.0 | 184 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | wprd01 | t2 | transform/rot90/oracle | oracle | 45.5 | 182 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | wprd01 | t3 | base/direct | direct | 29.0 | 58 | 200 | 200 | 0 |
| Cambrian-S-7B-LFP | direct | wprd01 | t3 | base/oracle | oracle | 27.5 | 55 | 200 | 200 | 0 |
| Cambrian-S-7B-LFP | direct | wprd01 | t3 | transform/mirror_h/direct | direct | 31.0 | 62 | 200 | 200 | 0 |
| Cambrian-S-7B-LFP | direct | wprd01 | t3 | transform/mirror_h/oracle | oracle | 31.5 | 63 | 200 | 200 | 0 |
| Cambrian-S-7B-LFP | direct | wprd01 | t3 | transform/mirror_h_rot180/direct | direct | 33.0 | 66 | 200 | 200 | 0 |
| Cambrian-S-7B-LFP | direct | wprd01 | t3 | transform/mirror_h_rot180/oracle | oracle | 31.0 | 62 | 200 | 200 | 0 |
| Cambrian-S-7B-LFP | direct | wprd01 | t3 | transform/mirror_h_rot270/direct | direct | 35.0 | 70 | 200 | 200 | 0 |
| Cambrian-S-7B-LFP | direct | wprd01 | t3 | transform/mirror_h_rot270/oracle | oracle | 37.0 | 74 | 200 | 200 | 0 |
| Cambrian-S-7B-LFP | direct | wprd01 | t3 | transform/mirror_h_rot90/direct | direct | 36.5 | 73 | 200 | 200 | 0 |
| Cambrian-S-7B-LFP | direct | wprd01 | t3 | transform/mirror_h_rot90/oracle | oracle | 33.0 | 66 | 200 | 200 | 0 |
| Cambrian-S-7B-LFP | direct | wprd01 | t3 | transform/rot180/direct | direct | 30.5 | 61 | 200 | 200 | 0 |
| Cambrian-S-7B-LFP | direct | wprd01 | t3 | transform/rot180/oracle | oracle | 28.0 | 56 | 200 | 200 | 0 |
| Cambrian-S-7B-LFP | direct | wprd01 | t3 | transform/rot270/direct | direct | 27.0 | 54 | 200 | 200 | 0 |
| Cambrian-S-7B-LFP | direct | wprd01 | t3 | transform/rot270/oracle | oracle | 29.5 | 59 | 200 | 200 | 0 |
| Cambrian-S-7B-LFP | direct | wprd01 | t3 | transform/rot90/direct | direct | 26.5 | 53 | 200 | 200 | 0 |
| Cambrian-S-7B-LFP | direct | wprd01 | t3 | transform/rot90/oracle | oracle | 26.5 | 53 | 200 | 200 | 0 |
| Cambrian-S-7B-LFP | direct | wprd01 | t3 | world/intervention_001/direct | direct | 35.5 | 71 | 200 | 200 | 0 |
| Cambrian-S-7B-LFP | direct | wprd01 | t3 | world/intervention_001/oracle | oracle | 31.5 | 63 | 200 | 200 | 0 |
| Cambrian-S-7B-LFP | direct | wprd01 | t3 | world/sham_001/direct | direct | 25.5 | 51 | 200 | 200 | 0 |
| Cambrian-S-7B-LFP | direct | wprd01 | t3 | world/sham_001/oracle | oracle | 28.0 | 56 | 200 | 200 | 0 |
| Cambrian-S-7B-LFP | direct | wprd01 | t4 | base/direct | direct | 25.0 | 100 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | wprd01 | t4 | base/oracle | oracle | 24.8 | 99 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | wprd01 | t4 | transform/mirror_h/direct | direct | 26.0 | 104 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | wprd01 | t4 | transform/mirror_h/oracle | oracle | 27.0 | 108 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | wprd01 | t4 | transform/mirror_h_rot180/direct | direct | 25.5 | 102 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | wprd01 | t4 | transform/mirror_h_rot180/oracle | oracle | 26.2 | 105 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | wprd01 | t4 | transform/mirror_h_rot270/direct | direct | 25.0 | 100 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | wprd01 | t4 | transform/mirror_h_rot270/oracle | oracle | 27.0 | 108 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | wprd01 | t4 | transform/mirror_h_rot90/direct | direct | 27.0 | 108 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | wprd01 | t4 | transform/mirror_h_rot90/oracle | oracle | 26.8 | 107 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | wprd01 | t4 | transform/rot180/direct | direct | 25.8 | 103 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | wprd01 | t4 | transform/rot180/oracle | oracle | 25.2 | 101 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | wprd01 | t4 | transform/rot270/direct | direct | 26.0 | 104 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | wprd01 | t4 | transform/rot270/oracle | oracle | 27.2 | 109 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | wprd01 | t4 | transform/rot90/direct | direct | 27.2 | 109 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | wprd01 | t4 | transform/rot90/oracle | oracle | 27.8 | 111 | 400 | 400 | 0 |
| Cambrian-S-7B-LFP | direct | wprd01 | t4 | world/intervention_001/direct | direct | 15.0 | 30 | 200 | 200 | 0 |
| Cambrian-S-7B-LFP | direct | wprd01 | t4 | world/intervention_001/oracle | oracle | 15.5 | 31 | 200 | 200 | 0 |
| Cambrian-S-7B-LFP | direct | wprd01 | t4 | world/sham_001/direct | direct | 20.0 | 40 | 200 | 200 | 0 |
| Cambrian-S-7B-LFP | direct | wprd01 | t4 | world/sham_001/oracle | oracle | 20.5 | 41 | 200 | 200 | 0 |
| Janus-Pro-7B | direct | blank | t1 | base/direct | direct | 50.5 | 202 | 400 | 400 | 0 |
| Janus-Pro-7B | direct | blank | t1 | base/oracle | oracle | 52.0 | 208 | 400 | 400 | 0 |
| Janus-Pro-7B | direct | blank | t1 | transform/mirror_h/direct | direct | 30.8 | 123 | 400 | 400 | 0 |
| Janus-Pro-7B | direct | blank | t1 | transform/mirror_h/oracle | oracle | 33.5 | 134 | 400 | 400 | 0 |
| Janus-Pro-7B | direct | blank | t1 | transform/mirror_h_rot180/direct | direct | 31.8 | 127 | 400 | 400 | 0 |
| Janus-Pro-7B | direct | blank | t1 | transform/mirror_h_rot180/oracle | oracle | 37.8 | 151 | 400 | 400 | 0 |
| Janus-Pro-7B | direct | blank | t1 | transform/mirror_h_rot270/direct | direct | 26.5 | 106 | 400 | 400 | 0 |
| Janus-Pro-7B | direct | blank | t1 | transform/mirror_h_rot270/oracle | oracle | 31.2 | 125 | 400 | 400 | 0 |
| Janus-Pro-7B | direct | blank | t1 | transform/mirror_h_rot90/direct | direct | 32.2 | 129 | 400 | 400 | 0 |
| Janus-Pro-7B | direct | blank | t1 | transform/mirror_h_rot90/oracle | oracle | 38.8 | 155 | 400 | 400 | 0 |
| Janus-Pro-7B | direct | blank | t1 | transform/rot180/direct | direct | 50.0 | 200 | 400 | 400 | 0 |
| Janus-Pro-7B | direct | blank | t1 | transform/rot180/oracle | oracle | 54.0 | 216 | 400 | 400 | 0 |
| Janus-Pro-7B | direct | blank | t1 | transform/rot270/direct | direct | 51.2 | 205 | 400 | 400 | 0 |
| Janus-Pro-7B | direct | blank | t1 | transform/rot270/oracle | oracle | 59.0 | 236 | 400 | 400 | 0 |
| Janus-Pro-7B | direct | blank | t1 | transform/rot90/direct | direct | 51.2 | 205 | 400 | 400 | 0 |
| Janus-Pro-7B | direct | blank | t1 | transform/rot90/oracle | oracle | 56.8 | 227 | 400 | 400 | 0 |
| Janus-Pro-7B | direct | blank | t2 | base/direct | direct | 41.2 | 165 | 400 | 400 | 0 |
| Janus-Pro-7B | direct | blank | t2 | base/oracle | oracle | 40.8 | 163 | 400 | 400 | 0 |
| Janus-Pro-7B | direct | blank | t2 | transform/mirror_h/direct | direct | 44.0 | 176 | 400 | 400 | 0 |
| Janus-Pro-7B | direct | blank | t2 | transform/mirror_h/oracle | oracle | 48.0 | 192 | 400 | 400 | 0 |
| Janus-Pro-7B | direct | blank | t2 | transform/mirror_h_rot180/direct | direct | 41.8 | 167 | 400 | 400 | 0 |
| Janus-Pro-7B | direct | blank | t2 | transform/mirror_h_rot180/oracle | oracle | 46.2 | 185 | 400 | 400 | 0 |
| Janus-Pro-7B | direct | blank | t2 | transform/mirror_h_rot270/direct | direct | 41.2 | 165 | 400 | 400 | 0 |
| Janus-Pro-7B | direct | blank | t2 | transform/mirror_h_rot270/oracle | oracle | 42.8 | 171 | 400 | 400 | 0 |
| Janus-Pro-7B | direct | blank | t2 | transform/mirror_h_rot90/direct | direct | 42.5 | 170 | 400 | 400 | 0 |
| Janus-Pro-7B | direct | blank | t2 | transform/mirror_h_rot90/oracle | oracle | 42.5 | 170 | 400 | 400 | 0 |
| Janus-Pro-7B | direct | blank | t2 | transform/rot180/direct | direct | 41.2 | 165 | 400 | 400 | 0 |
| Janus-Pro-7B | direct | blank | t2 | transform/rot180/oracle | oracle | 43.5 | 174 | 400 | 400 | 0 |
| Janus-Pro-7B | direct | blank | t2 | transform/rot270/direct | direct | 39.2 | 157 | 400 | 400 | 0 |
| Janus-Pro-7B | direct | blank | t2 | transform/rot270/oracle | oracle | 43.2 | 173 | 400 | 400 | 0 |
| Janus-Pro-7B | direct | blank | t2 | transform/rot90/direct | direct | 41.8 | 167 | 400 | 400 | 0 |
| Janus-Pro-7B | direct | blank | t2 | transform/rot90/oracle | oracle | 42.8 | 171 | 400 | 400 | 0 |
| Janus-Pro-7B | direct | sat | t1 | base/direct | direct | 52.8 | 211 | 400 | 400 | 0 |
| Janus-Pro-7B | direct | sat | t1 | base/oracle | oracle | 52.5 | 210 | 400 | 400 | 0 |
| Janus-Pro-7B | direct | sat | t1 | transform/mirror_h/direct | direct | 25.0 | 100 | 400 | 400 | 0 |
| Janus-Pro-7B | direct | sat | t1 | transform/mirror_h/oracle | oracle | 28.2 | 113 | 400 | 400 | 0 |
| Janus-Pro-7B | direct | sat | t1 | transform/mirror_h_rot180/direct | direct | 25.5 | 102 | 400 | 400 | 0 |
| Janus-Pro-7B | direct | sat | t1 | transform/mirror_h_rot180/oracle | oracle | 30.2 | 121 | 400 | 400 | 0 |
| Janus-Pro-7B | direct | sat | t1 | transform/mirror_h_rot270/direct | direct | 28.5 | 114 | 400 | 400 | 0 |
| Janus-Pro-7B | direct | sat | t1 | transform/mirror_h_rot270/oracle | oracle | 29.2 | 117 | 400 | 400 | 0 |
| Janus-Pro-7B | direct | sat | t1 | transform/mirror_h_rot90/direct | direct | 27.5 | 110 | 400 | 400 | 0 |
| Janus-Pro-7B | direct | sat | t1 | transform/mirror_h_rot90/oracle | oracle | 28.8 | 115 | 400 | 400 | 0 |
| Janus-Pro-7B | direct | sat | t1 | transform/rot180/direct | direct | 47.0 | 188 | 400 | 400 | 0 |
| Janus-Pro-7B | direct | sat | t1 | transform/rot180/oracle | oracle | 48.8 | 195 | 400 | 400 | 0 |
| Janus-Pro-7B | direct | sat | t1 | transform/rot270/direct | direct | 49.0 | 196 | 400 | 400 | 0 |
| Janus-Pro-7B | direct | sat | t1 | transform/rot270/oracle | oracle | 53.2 | 213 | 400 | 400 | 0 |
| Janus-Pro-7B | direct | sat | t1 | transform/rot90/direct | direct | 46.8 | 187 | 400 | 400 | 0 |
| Janus-Pro-7B | direct | sat | t1 | transform/rot90/oracle | oracle | 51.5 | 206 | 400 | 400 | 0 |
| Janus-Pro-7B | direct | sat | t2 | base/direct | direct | 40.8 | 163 | 400 | 400 | 0 |
| Janus-Pro-7B | direct | sat | t2 | base/oracle | oracle | 41.5 | 166 | 400 | 400 | 0 |
| Janus-Pro-7B | direct | sat | t2 | transform/mirror_h/direct | direct | 41.2 | 165 | 400 | 400 | 0 |
| Janus-Pro-7B | direct | sat | t2 | transform/mirror_h/oracle | oracle | 42.2 | 169 | 400 | 400 | 0 |
| Janus-Pro-7B | direct | sat | t2 | transform/mirror_h_rot180/direct | direct | 35.0 | 140 | 400 | 400 | 0 |
| Janus-Pro-7B | direct | sat | t2 | transform/mirror_h_rot180/oracle | oracle | 39.0 | 156 | 400 | 400 | 0 |
| Janus-Pro-7B | direct | sat | t2 | transform/mirror_h_rot270/direct | direct | 39.2 | 157 | 400 | 400 | 0 |
| Janus-Pro-7B | direct | sat | t2 | transform/mirror_h_rot270/oracle | oracle | 43.2 | 173 | 400 | 400 | 0 |
| Janus-Pro-7B | direct | sat | t2 | transform/mirror_h_rot90/direct | direct | 40.8 | 163 | 400 | 400 | 0 |
| Janus-Pro-7B | direct | sat | t2 | transform/mirror_h_rot90/oracle | oracle | 42.8 | 171 | 400 | 400 | 0 |
| Janus-Pro-7B | direct | sat | t2 | transform/rot180/direct | direct | 40.0 | 160 | 400 | 400 | 0 |
| Janus-Pro-7B | direct | sat | t2 | transform/rot180/oracle | oracle | 42.0 | 168 | 400 | 400 | 0 |
| Janus-Pro-7B | direct | sat | t2 | transform/rot270/direct | direct | 42.5 | 170 | 400 | 400 | 0 |
| Janus-Pro-7B | direct | sat | t2 | transform/rot270/oracle | oracle | 41.5 | 166 | 400 | 400 | 0 |
| Janus-Pro-7B | direct | sat | t2 | transform/rot90/direct | direct | 41.2 | 165 | 400 | 400 | 0 |
| Janus-Pro-7B | direct | sat | t2 | transform/rot90/oracle | oracle | 41.5 | 166 | 400 | 400 | 0 |
| Janus-Pro-7B | direct | sat | t3 | base/direct | direct | 46.5 | 93 | 200 | 200 | 0 |
| Janus-Pro-7B | direct | sat | t3 | base/oracle | oracle | 48.0 | 96 | 200 | 200 | 0 |
| Janus-Pro-7B | direct | sat | t3 | transform/mirror_h/direct | direct | 50.0 | 100 | 200 | 200 | 0 |
| Janus-Pro-7B | direct | sat | t3 | transform/mirror_h/oracle | oracle | 46.0 | 92 | 200 | 200 | 0 |
| Janus-Pro-7B | direct | sat | t3 | transform/mirror_h_rot180/direct | direct | 48.0 | 96 | 200 | 200 | 0 |
| Janus-Pro-7B | direct | sat | t3 | transform/mirror_h_rot180/oracle | oracle | 51.0 | 102 | 200 | 200 | 0 |
| Janus-Pro-7B | direct | sat | t3 | transform/mirror_h_rot270/direct | direct | 46.5 | 93 | 200 | 200 | 0 |
| Janus-Pro-7B | direct | sat | t3 | transform/mirror_h_rot270/oracle | oracle | 49.5 | 99 | 200 | 200 | 0 |
| Janus-Pro-7B | direct | sat | t3 | transform/mirror_h_rot90/direct | direct | 40.0 | 80 | 200 | 200 | 0 |
| Janus-Pro-7B | direct | sat | t3 | transform/mirror_h_rot90/oracle | oracle | 44.5 | 89 | 200 | 200 | 0 |
| Janus-Pro-7B | direct | sat | t3 | transform/rot180/direct | direct | 46.5 | 93 | 200 | 200 | 0 |
| Janus-Pro-7B | direct | sat | t3 | transform/rot180/oracle | oracle | 49.0 | 98 | 200 | 200 | 0 |
| Janus-Pro-7B | direct | sat | t3 | transform/rot270/direct | direct | 48.5 | 97 | 200 | 200 | 0 |
| Janus-Pro-7B | direct | sat | t3 | transform/rot270/oracle | oracle | 50.5 | 101 | 200 | 200 | 0 |
| Janus-Pro-7B | direct | sat | t3 | transform/rot90/direct | direct | 55.0 | 110 | 200 | 200 | 0 |
| Janus-Pro-7B | direct | sat | t3 | transform/rot90/oracle | oracle | 52.0 | 104 | 200 | 200 | 0 |
| Janus-Pro-7B | direct | sat | t3 | world/intervention_001/direct | direct | 12.5 | 25 | 200 | 200 | 0 |
| Janus-Pro-7B | direct | sat | t3 | world/intervention_001/oracle | oracle | 12.5 | 25 | 200 | 200 | 0 |
| Janus-Pro-7B | direct | sat | t3 | world/sham_001/direct | direct | 41.0 | 82 | 200 | 200 | 0 |
| Janus-Pro-7B | direct | sat | t3 | world/sham_001/oracle | oracle | 39.0 | 78 | 200 | 200 | 0 |
| Janus-Pro-7B | direct | sat | t4 | base/direct | direct | 7.8 | 31 | 400 | 400 | 300 |
| Janus-Pro-7B | direct | sat | t4 | base/oracle | oracle | 9.5 | 38 | 400 | 400 | 300 |
| Janus-Pro-7B | direct | sat | t4 | transform/mirror_h/direct | direct | 8.0 | 32 | 400 | 400 | 300 |
| Janus-Pro-7B | direct | sat | t4 | transform/mirror_h/oracle | oracle | 9.2 | 37 | 400 | 400 | 300 |
| Janus-Pro-7B | direct | sat | t4 | transform/mirror_h_rot180/direct | direct | 8.0 | 32 | 400 | 400 | 300 |
| Janus-Pro-7B | direct | sat | t4 | transform/mirror_h_rot180/oracle | oracle | 9.2 | 37 | 400 | 400 | 300 |
| Janus-Pro-7B | direct | sat | t4 | transform/mirror_h_rot270/direct | direct | 9.5 | 38 | 400 | 400 | 300 |
| Janus-Pro-7B | direct | sat | t4 | transform/mirror_h_rot270/oracle | oracle | 8.5 | 34 | 400 | 400 | 300 |
| Janus-Pro-7B | direct | sat | t4 | transform/mirror_h_rot90/direct | direct | 8.2 | 33 | 400 | 400 | 300 |
| Janus-Pro-7B | direct | sat | t4 | transform/mirror_h_rot90/oracle | oracle | 8.2 | 33 | 400 | 400 | 300 |
| Janus-Pro-7B | direct | sat | t4 | transform/rot180/direct | direct | 9.0 | 36 | 400 | 400 | 300 |
| Janus-Pro-7B | direct | sat | t4 | transform/rot180/oracle | oracle | 9.5 | 38 | 400 | 400 | 300 |
| Janus-Pro-7B | direct | sat | t4 | transform/rot270/direct | direct | 8.2 | 33 | 400 | 400 | 300 |
| Janus-Pro-7B | direct | sat | t4 | transform/rot270/oracle | oracle | 7.8 | 31 | 400 | 400 | 300 |
| Janus-Pro-7B | direct | sat | t4 | transform/rot90/direct | direct | 8.5 | 34 | 400 | 400 | 300 |
| Janus-Pro-7B | direct | sat | t4 | transform/rot90/oracle | oracle | 8.2 | 33 | 400 | 400 | 300 |
| Janus-Pro-7B | direct | sat | t4 | world/intervention_001/direct | direct | 0.0 | 0 | 200 | 200 | 200 |
| Janus-Pro-7B | direct | sat | t4 | world/intervention_001/oracle | oracle | 0.0 | 0 | 200 | 200 | 200 |
| Janus-Pro-7B | direct | sat | t4 | world/sham_001/direct | direct | 0.0 | 0 | 200 | 200 | 200 |
| Janus-Pro-7B | direct | sat | t4 | world/sham_001/oracle | oracle | 0.0 | 0 | 200 | 200 | 200 |
| Janus-Pro-7B | direct | webrd04 | t1 | base/direct | direct | 53.8 | 215 | 400 | 400 | 0 |
| Janus-Pro-7B | direct | webrd04 | t1 | base/oracle | oracle | 55.8 | 223 | 400 | 400 | 0 |
| Janus-Pro-7B | direct | webrd04 | t2 | base/direct | direct | 41.2 | 165 | 400 | 400 | 0 |
| Janus-Pro-7B | direct | webrd04 | t2 | base/oracle | oracle | 43.2 | 173 | 400 | 400 | 0 |
| Janus-Pro-7B | direct | webrd04 | t3 | base/direct | direct | 48.5 | 97 | 200 | 200 | 0 |
| Janus-Pro-7B | direct | webrd04 | t3 | base/oracle | oracle | 49.0 | 98 | 200 | 200 | 0 |
| Janus-Pro-7B | direct | webrd04 | t3 | world/intervention_001/direct | direct | 11.0 | 22 | 200 | 200 | 0 |
| Janus-Pro-7B | direct | webrd04 | t3 | world/intervention_001/oracle | oracle | 11.5 | 23 | 200 | 200 | 0 |
| Janus-Pro-7B | direct | webrd04 | t3 | world/sham_001/direct | direct | 42.5 | 85 | 200 | 200 | 0 |
| Janus-Pro-7B | direct | webrd04 | t3 | world/sham_001/oracle | oracle | 49.5 | 99 | 200 | 200 | 0 |
| Janus-Pro-7B | direct | webrd04 | t4 | base/direct | direct | 10.0 | 40 | 400 | 400 | 300 |
| Janus-Pro-7B | direct | webrd04 | t4 | base/oracle | oracle | 8.2 | 33 | 400 | 400 | 300 |
| Janus-Pro-7B | direct | webrd04 | t4 | world/intervention_001/direct | direct | 0.0 | 0 | 200 | 200 | 200 |
| Janus-Pro-7B | direct | webrd04 | t4 | world/intervention_001/oracle | oracle | 0.0 | 0 | 200 | 200 | 200 |
| Janus-Pro-7B | direct | webrd04 | t4 | world/sham_001/direct | direct | 0.0 | 0 | 200 | 200 | 200 |
| Janus-Pro-7B | direct | webrd04 | t4 | world/sham_001/oracle | oracle | 0.0 | 0 | 200 | 200 | 200 |
| Janus-Pro-7B | direct | wprd01 | t1 | base/direct | direct | 48.0 | 192 | 400 | 400 | 0 |
| Janus-Pro-7B | direct | wprd01 | t1 | base/oracle | oracle | 52.8 | 211 | 400 | 400 | 0 |
| Janus-Pro-7B | direct | wprd01 | t1 | transform/mirror_h/direct | direct | 30.0 | 120 | 400 | 400 | 0 |
| Janus-Pro-7B | direct | wprd01 | t1 | transform/mirror_h/oracle | oracle | 30.5 | 122 | 400 | 400 | 0 |
| Janus-Pro-7B | direct | wprd01 | t1 | transform/mirror_h_rot180/direct | direct | 28.5 | 114 | 400 | 400 | 0 |
| Janus-Pro-7B | direct | wprd01 | t1 | transform/mirror_h_rot180/oracle | oracle | 34.5 | 138 | 400 | 400 | 0 |
| Janus-Pro-7B | direct | wprd01 | t1 | transform/mirror_h_rot270/direct | direct | 30.5 | 122 | 400 | 400 | 0 |
| Janus-Pro-7B | direct | wprd01 | t1 | transform/mirror_h_rot270/oracle | oracle | 28.0 | 112 | 400 | 400 | 0 |
| Janus-Pro-7B | direct | wprd01 | t1 | transform/mirror_h_rot90/direct | direct | 27.0 | 108 | 400 | 400 | 0 |
| Janus-Pro-7B | direct | wprd01 | t1 | transform/mirror_h_rot90/oracle | oracle | 29.2 | 117 | 400 | 400 | 0 |
| Janus-Pro-7B | direct | wprd01 | t1 | transform/rot180/direct | direct | 49.2 | 197 | 400 | 400 | 0 |
| Janus-Pro-7B | direct | wprd01 | t1 | transform/rot180/oracle | oracle | 52.8 | 211 | 400 | 400 | 0 |
| Janus-Pro-7B | direct | wprd01 | t1 | transform/rot270/direct | direct | 51.5 | 206 | 400 | 400 | 0 |
| Janus-Pro-7B | direct | wprd01 | t1 | transform/rot270/oracle | oracle | 54.5 | 218 | 400 | 400 | 0 |
| Janus-Pro-7B | direct | wprd01 | t1 | transform/rot90/direct | direct | 47.5 | 190 | 400 | 400 | 0 |
| Janus-Pro-7B | direct | wprd01 | t1 | transform/rot90/oracle | oracle | 51.8 | 207 | 400 | 400 | 0 |
| Janus-Pro-7B | direct | wprd01 | t2 | base/direct | direct | 40.5 | 162 | 400 | 400 | 0 |
| Janus-Pro-7B | direct | wprd01 | t2 | base/oracle | oracle | 42.0 | 168 | 400 | 400 | 0 |
| Janus-Pro-7B | direct | wprd01 | t2 | transform/mirror_h/direct | direct | 41.0 | 164 | 400 | 400 | 0 |
| Janus-Pro-7B | direct | wprd01 | t2 | transform/mirror_h/oracle | oracle | 37.8 | 151 | 400 | 400 | 0 |
| Janus-Pro-7B | direct | wprd01 | t2 | transform/mirror_h_rot180/direct | direct | 37.8 | 151 | 400 | 400 | 0 |
| Janus-Pro-7B | direct | wprd01 | t2 | transform/mirror_h_rot180/oracle | oracle | 40.8 | 163 | 400 | 400 | 0 |
| Janus-Pro-7B | direct | wprd01 | t2 | transform/mirror_h_rot270/direct | direct | 41.8 | 167 | 400 | 400 | 0 |
| Janus-Pro-7B | direct | wprd01 | t2 | transform/mirror_h_rot270/oracle | oracle | 39.5 | 158 | 400 | 400 | 0 |
| Janus-Pro-7B | direct | wprd01 | t2 | transform/mirror_h_rot90/direct | direct | 36.8 | 147 | 400 | 400 | 0 |
| Janus-Pro-7B | direct | wprd01 | t2 | transform/mirror_h_rot90/oracle | oracle | 41.2 | 165 | 400 | 400 | 0 |
| Janus-Pro-7B | direct | wprd01 | t2 | transform/rot180/direct | direct | 38.8 | 155 | 400 | 400 | 0 |
| Janus-Pro-7B | direct | wprd01 | t2 | transform/rot180/oracle | oracle | 38.2 | 153 | 400 | 400 | 0 |
| Janus-Pro-7B | direct | wprd01 | t2 | transform/rot270/direct | direct | 37.2 | 149 | 400 | 400 | 0 |
| Janus-Pro-7B | direct | wprd01 | t2 | transform/rot270/oracle | oracle | 37.8 | 151 | 400 | 400 | 0 |
| Janus-Pro-7B | direct | wprd01 | t2 | transform/rot90/direct | direct | 42.2 | 169 | 400 | 400 | 0 |
| Janus-Pro-7B | direct | wprd01 | t2 | transform/rot90/oracle | oracle | 40.2 | 161 | 400 | 400 | 0 |
| Janus-Pro-7B | direct | wprd01 | t3 | base/direct | direct | 40.0 | 80 | 200 | 200 | 0 |
| Janus-Pro-7B | direct | wprd01 | t3 | base/oracle | oracle | 48.5 | 97 | 200 | 200 | 0 |
| Janus-Pro-7B | direct | wprd01 | t3 | transform/mirror_h/direct | direct | 47.0 | 94 | 200 | 200 | 0 |
| Janus-Pro-7B | direct | wprd01 | t3 | transform/mirror_h/oracle | oracle | 46.0 | 92 | 200 | 200 | 0 |
| Janus-Pro-7B | direct | wprd01 | t3 | transform/mirror_h_rot180/direct | direct | 44.0 | 88 | 200 | 200 | 0 |
| Janus-Pro-7B | direct | wprd01 | t3 | transform/mirror_h_rot180/oracle | oracle | 41.5 | 83 | 200 | 200 | 0 |
| Janus-Pro-7B | direct | wprd01 | t3 | transform/mirror_h_rot270/direct | direct | 38.0 | 76 | 200 | 200 | 0 |
| Janus-Pro-7B | direct | wprd01 | t3 | transform/mirror_h_rot270/oracle | oracle | 39.5 | 79 | 200 | 200 | 0 |
| Janus-Pro-7B | direct | wprd01 | t3 | transform/mirror_h_rot90/direct | direct | 40.0 | 80 | 200 | 200 | 0 |
| Janus-Pro-7B | direct | wprd01 | t3 | transform/mirror_h_rot90/oracle | oracle | 48.0 | 96 | 200 | 200 | 0 |
| Janus-Pro-7B | direct | wprd01 | t3 | transform/rot180/direct | direct | 47.0 | 94 | 200 | 200 | 0 |
| Janus-Pro-7B | direct | wprd01 | t3 | transform/rot180/oracle | oracle | 49.0 | 98 | 200 | 200 | 0 |
| Janus-Pro-7B | direct | wprd01 | t3 | transform/rot270/direct | direct | 45.0 | 90 | 200 | 200 | 0 |
| Janus-Pro-7B | direct | wprd01 | t3 | transform/rot270/oracle | oracle | 48.0 | 96 | 200 | 200 | 0 |
| Janus-Pro-7B | direct | wprd01 | t3 | transform/rot90/direct | direct | 44.5 | 89 | 200 | 200 | 0 |
| Janus-Pro-7B | direct | wprd01 | t3 | transform/rot90/oracle | oracle | 42.5 | 85 | 200 | 200 | 0 |
| Janus-Pro-7B | direct | wprd01 | t3 | world/intervention_001/direct | direct | 19.0 | 38 | 200 | 200 | 0 |
| Janus-Pro-7B | direct | wprd01 | t3 | world/intervention_001/oracle | oracle | 16.0 | 32 | 200 | 200 | 0 |
| Janus-Pro-7B | direct | wprd01 | t3 | world/sham_001/direct | direct | 45.5 | 91 | 200 | 200 | 0 |
| Janus-Pro-7B | direct | wprd01 | t3 | world/sham_001/oracle | oracle | 51.5 | 103 | 200 | 200 | 0 |
| Janus-Pro-7B | direct | wprd01 | t4 | base/direct | direct | 8.5 | 34 | 400 | 400 | 300 |
| Janus-Pro-7B | direct | wprd01 | t4 | base/oracle | oracle | 10.5 | 42 | 400 | 400 | 300 |
| Janus-Pro-7B | direct | wprd01 | t4 | transform/mirror_h/direct | direct | 9.5 | 38 | 400 | 400 | 300 |
| Janus-Pro-7B | direct | wprd01 | t4 | transform/mirror_h/oracle | oracle | 10.5 | 42 | 400 | 400 | 300 |
| Janus-Pro-7B | direct | wprd01 | t4 | transform/mirror_h_rot180/direct | direct | 8.8 | 35 | 400 | 400 | 300 |
| Janus-Pro-7B | direct | wprd01 | t4 | transform/mirror_h_rot180/oracle | oracle | 7.0 | 28 | 400 | 400 | 300 |
| Janus-Pro-7B | direct | wprd01 | t4 | transform/mirror_h_rot270/direct | direct | 8.5 | 34 | 400 | 400 | 300 |
| Janus-Pro-7B | direct | wprd01 | t4 | transform/mirror_h_rot270/oracle | oracle | 9.2 | 37 | 400 | 400 | 300 |
| Janus-Pro-7B | direct | wprd01 | t4 | transform/mirror_h_rot90/direct | direct | 9.2 | 37 | 400 | 400 | 300 |
| Janus-Pro-7B | direct | wprd01 | t4 | transform/mirror_h_rot90/oracle | oracle | 10.5 | 42 | 400 | 400 | 300 |
| Janus-Pro-7B | direct | wprd01 | t4 | transform/rot180/direct | direct | 9.8 | 39 | 400 | 400 | 300 |
| Janus-Pro-7B | direct | wprd01 | t4 | transform/rot180/oracle | oracle | 8.8 | 35 | 400 | 400 | 300 |
| Janus-Pro-7B | direct | wprd01 | t4 | transform/rot270/direct | direct | 9.2 | 37 | 400 | 400 | 300 |
| Janus-Pro-7B | direct | wprd01 | t4 | transform/rot270/oracle | oracle | 7.0 | 28 | 400 | 400 | 300 |
| Janus-Pro-7B | direct | wprd01 | t4 | transform/rot90/direct | direct | 8.0 | 32 | 400 | 400 | 300 |
| Janus-Pro-7B | direct | wprd01 | t4 | transform/rot90/oracle | oracle | 9.2 | 37 | 400 | 400 | 300 |
| Janus-Pro-7B | direct | wprd01 | t4 | world/intervention_001/direct | direct | 0.0 | 0 | 200 | 200 | 200 |
| Janus-Pro-7B | direct | wprd01 | t4 | world/intervention_001/oracle | oracle | 0.0 | 0 | 200 | 200 | 200 |
| Janus-Pro-7B | direct | wprd01 | t4 | world/sham_001/direct | direct | 0.0 | 0 | 200 | 200 | 200 |
| Janus-Pro-7B | direct | wprd01 | t4 | world/sham_001/oracle | oracle | 0.0 | 0 | 200 | 200 | 200 |

## Draw (`results_draw`)

Same table layout as above. These runs use the `external_draw` strategy.

## 12. Overall

| Model | Strategy | Backend | Acc (%) | Direct | Oracle | Δ (pp) | N | Correct | Cells |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ThinkMorph-7B | external_draw | veomni_thinkmorph | 65.7 | 65.7 | — | — | 638 | 419 | 2 |
| Bagel-7B-MoT | external_draw | veomni_bagel | 64.8 | 64.8 | — | — | 619 | 401 | 2 |
| SenseNova-U1-8B-MoT | external_draw | veomni_u1 | 62.8 | 62.8 | — | — | 239 | 150 | 1 |
| LatentUM-Base | external_draw | veomni_latentum | 53.6 | 53.6 | — | — | 1613 | 865 | 5 |
| BLIP3o-8B | external_draw | veomni_blip3o | 36.8 | 36.8 | — | — | 1176 | 433 | 3 |

## 13. Completeness

| Model | Tasks | Views | Families | N | Cells | Files |
| --- | --- | --- | --- | --- | --- | --- |
| ThinkMorph-7B | t1,t2 | blank | base | 638 | 2 | 2 |
| Bagel-7B-MoT | t1,t2 | blank | base | 619 | 2 | 2 |
| SenseNova-U1-8B-MoT | t1 | blank | base | 239 | 1 | 1 |
| LatentUM-Base | t1,t2 | blank,sat,webrd04 | base | 1613 | 5 | 5 |
| BLIP3o-8B | t1,t2 | blank,sat | base | 1176 | 3 | 3 |

## 14. By evidence condition

| Model | Direct (%) | N_direct | Oracle (%) | N_oracle | Δ (pp) |
| --- | --- | --- | --- | --- | --- |
| ThinkMorph-7B | 65.7 | 638 | — | — | — |
| Bagel-7B-MoT | 64.8 | 619 | — | — | — |
| SenseNova-U1-8B-MoT | 62.8 | 239 | — | — | — |
| LatentUM-Base | 53.6 | 1613 | — | — | — |
| BLIP3o-8B | 36.8 | 1176 | — | — | — |

## 15. By view

| Model | blank | sat | webrd04 | Overall |
| --- | --- | --- | --- | --- |
| ThinkMorph-7B | 65.7 | — | — | 65.7 |
| Bagel-7B-MoT | 64.8 | — | — | 64.8 |
| SenseNova-U1-8B-MoT | 62.8 | — | — | 62.8 |
| LatentUM-Base | 54.6 | 52.5 | 61.5 | 53.6 |
| BLIP3o-8B | 37.0 | 36.4 | — | 36.8 |

## 16. By task

| Model | t1 | t2 | Overall |
| --- | --- | --- | --- |
| ThinkMorph-7B | 66.0 | 65.1 | 65.7 |
| Bagel-7B-MoT | 63.8 | 66.7 | 64.8 |
| SenseNova-U1-8B-MoT | 62.8 | — | 62.8 |
| LatentUM-Base | 65.1 | 42.0 | 53.6 |
| BLIP3o-8B | 35.1 | 40.2 | 36.8 |

## 17. By variant family

| Model | base | transform | world | Overall |
| --- | --- | --- | --- | --- |
| ThinkMorph-7B | 65.7 | — | — | 65.7 |
| Bagel-7B-MoT | 64.8 | — | — | 64.8 |
| SenseNova-U1-8B-MoT | 62.8 | — | — | 62.8 |
| LatentUM-Base | 53.6 | — | — | 53.6 |
| BLIP3o-8B | 36.8 | — | — | 36.8 |

## 18. T4 · base + transform (comparable subset)

Aggregated across views with `total>0`.

### Direct

_No matching cells._

### Oracle

_No matching cells._

## 19. T1 / T2 · base + transform

### Direct

| Model | base | All |
| --- | --- | --- |
| ThinkMorph-7B | 65.7 | 65.7 |
| Bagel-7B-MoT | 64.8 | 64.8 |
| SenseNova-U1-8B-MoT | 62.8 | 62.8 |
| LatentUM-Base | 53.6 | 53.6 |
| BLIP3o-8B | 36.8 | 36.8 |

### Oracle

_No matching cells._

## 20. Per-cell detail

Non-empty cells only.

| Model | Strategy | View | Task | Variant | Condition | Acc (%) | Correct | Answered | Total | Errors |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ThinkMorph-7B | external_draw | blank | t1 | base/direct | direct | 66.0 | 264 | 400 | 400 | 0 |
| ThinkMorph-7B | external_draw | blank | t2 | base/direct | direct | 65.1 | 155 | 238 | 238 | 0 |
| Bagel-7B-MoT | external_draw | blank | t1 | base/direct | direct | 63.8 | 255 | 400 | 400 | 0 |
| Bagel-7B-MoT | external_draw | blank | t2 | base/direct | direct | 66.7 | 146 | 219 | 219 | 0 |
| SenseNova-U1-8B-MoT | external_draw | blank | t1 | base/direct | direct | 62.8 | 150 | 239 | 239 | 0 |
| LatentUM-Base | external_draw | blank | t1 | base/direct | direct | 65.8 | 263 | 400 | 400 | 0 |
| LatentUM-Base | external_draw | blank | t2 | base/direct | direct | 43.5 | 174 | 400 | 400 | 0 |
| LatentUM-Base | external_draw | sat | t1 | base/direct | direct | 64.5 | 258 | 400 | 400 | 0 |
| LatentUM-Base | external_draw | sat | t2 | base/direct | direct | 40.5 | 162 | 400 | 400 | 0 |
| LatentUM-Base | external_draw | webrd04 | t1 | base/direct | direct | 61.5 | 8 | 13 | 13 | 0 |
| BLIP3o-8B | external_draw | blank | t1 | base/direct | direct | 33.8 | 135 | 400 | 400 | 0 |
| BLIP3o-8B | external_draw | blank | t2 | base/direct | direct | 40.2 | 161 | 400 | 400 | 0 |
| BLIP3o-8B | external_draw | sat | t1 | base/direct | direct | 36.4 | 137 | 376 | 376 | 0 |
