# Implementation Todo: Training-Free Visual Thinking

## Constraints

1. **GPU 限制**: 测试只能使用 GPU 2 和 GPU 3。GPU 0/1 被其他程序占用，修改和测试不可影响这两张卡。
   - `CUDA_VISIBLE_DEVICES` 必须设为 2 或 3
   - 不可使用多卡或占用 GPU 0/1

2. **输出目录**: 所有生成策略的结果写入 `/home/ximeng.czq/caoziqi/code/SpatialIntelligence/MapSpatial-EvalKit/results_draw`

3. **不破坏现有逻辑**: `direct` 和 `oracle` 的纯多模态理解已经跑完，代码修改不能破坏：
   - `DirectStrategy` 的行为和输出路径
   - `ExternalDrawStrategy` 的现有行为（可重命名但保持兼容）
   - `NativeInterleaveStrategy` 对 ThinkMorph 的现有行为
   - 现有 `run_benchmark.sh` 的 `--strategy` 参数解析
   - 现有 model YAML 中 `strategies` 字段的兼容性

4. **测试脚本**: 使用 `scripts/run_gpu2_draw.sh` 和 `scripts/run_gpu3_draw.sh` 进行测试

## Task List

### Phase 0: 基础设施修复

- [ ] **0.1 修复生成图落盘**: `NativeInterleaveStrategy` 和 `ExternalDrawStrategy` 需要确保 PIL Image 按 sample_id 落盘为 Path，写入 `Prediction.generated_images`
  - 文件: `mapspatial/strategies/native_interleave.py`, `mapspatial/strategies/external_draw.py`
  - 不改: `DirectStrategy` 无生成图，不受影响

- [ ] **0.2 修复 marker 配置贯通**: runner 从 `backend_args` 读取 marker 传入 RunContext
  - 文件: `mapspatial/runner.py` (RunContext 构造处), `mapspatial/types.py` (RunContext 字段)
  - 不改: 默认 marker 保持 `"<image_start>"`，ThinkMorph 不受影响

- [ ] **0.3 策略重命名与兼容**: `external_draw` → `self_draw_restart`（保留 legacy alias）
  - 文件: `mapspatial/strategies/external_draw.py` (类名改), `mapspatial/strategies/__init__.py` (注册 alias)
  - 不改: CLI `--strategy external_draw` 仍然可用

- [ ] **0.4 扩展 Capabilities**: 增加 `reconsume_generated`, `stateful_interleave`, `autonomous_visual_trigger`
  - 文件: `mapspatial/types.py`, `mapspatial/backends/base.py`
  - 兼容: 保留 `native_interleave` 作为 deprecated alias

- [ ] **0.5 注册 forced_interleave 策略**: 我之前已经创建了文件，需要确认与新命名体系一致
  - 文件: `mapspatial/strategies/forced_interleave.py` (已创建)
  - 注意: 按新文档应叫 `stateful_forced`，但先保持 `forced_interleave` 作为 alias

### Phase 1: Bagel stateful forced

- [ ] **1.1 inferencer 增加 forced_interleave_inference**: 在 InterleaveInferencer 中增加方法，强制生成图像不等 marker
  - 文件: `mapspatial/vendor/bagel_interleave/inferencer.py`
  - 不改: 现有 `interleave_inference` 方法保持原样

- [ ] **1.2 BagelBackend 增加 forced_interleave() 方法**: 调用新 inferencer 方法，返回 Prediction
  - 文件: `mapspatial/backends/veomni/bagel.py`
  - 不改: 现有 `interleave()` 和 `understand()` 方法

- [ ] **1.3 更新 bagel-7b.yaml**: 添加 `forced_interleave` 到 strategies

### Phase 2: U1 native interleave

- [ ] **2.1 Port interleave_gen 到 vendored modeling**: 从原始 U1 代码移植 ~350 行
  - 文件: `mapspatial/vendor/neo_chat/modeling_neo_chat.py`
  - 适配: 替换 get_conv_template, 适配 _t2i_predict_v 签名

- [ ] **2.2 U1Backend 增加 interleave() 方法**: 调用 ported interleave_gen
  - 文件: `mapspatial/backends/veomni/u1.py`
  - 不改: 现有 `understand()` 和 `draw()`

- [ ] **2.3 翻转 U1 capability**: `native_interleave=True`
  - 文件: `mapspatial/backends/veomni/u1.py`, `configs/models/sensenova-u1-8b.yaml`

### Phase 3: LatentUM native interleave

- [ ] **3.1 泛化 FrozenLakePlanner 的 save-rewind-reinject**: 写通用 interleave() 方法
  - 文件: `mapspatial/backends/veomni/latentum.py`
  - 使用: 原始 repo 的 internvl/ar_head/quantizer/visual_projector

- [ ] **3.2 翻转 LatentUM capability**: `native_interleave=True`
  - 文件: `mapspatial/backends/veomni/latentum.py`, `configs/models/latentum-base.yaml`

### Phase 4: GPU 脚本更新

- [ ] **4.1 修改 run_gpu2_draw.sh**: model:strategy 配对，输出到 results_draw
  - GPU 2: bagel-7b:forced_interleave, thinkmorph-7b:native_interleave, latentum-base:native_interleave, janus-pro-7b:external_draw

- [ ] **4.2 修改 run_gpu3_draw.sh**: model:strategy 配对，输出到 results_draw
  - GPU 3: sensenova-u1-8b:native_interleave, blip3o-8b:external_draw, show-o2-7b:external_draw, joyai-image:external_draw

- [ ] **4.3 Smoke test**: 在 GPU 2/3 上用 base/direct 变体跑通
