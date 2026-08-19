"""Debug LatentUM vision path on a failing image."""
import os, sys
os.environ.setdefault("CUDA_VISIBLE_DEVICES", "2")
os.environ.setdefault("PYTHONNOUSERSITE", "1")
import torch
PROJECT = "/mnt/nas-tbt/caoziqi/code/SpatialIntelligence/MapSpatial-EvalKit"
sys.path.insert(0, PROJECT)

from mapspatial.loader import load_model, load_tokenizer
from mapspatial.vendor.latentum.modeling_latentum import LatentUMModel
from PIL import Image

MODEL_PATH = "/mnt/nas-tbt/tbt/checkpoint/hf_cache/LatentUM-Base"
model, _ = load_model(MODEL_PATH, LatentUMModel, device="cuda", dtype="bfloat16")
model.eval()

# Failing image
DATA = "/home/ximeng.czq/caoziqi/code/SpatialIntelligence/SpatialIntelligence-gate2building/data"
img_path = os.path.join(DATA, "benchmark_images_t1/B000A09B8C_from_B0FFFDC4BP_to_B000A9NO8R/方案三/B000A09B8C_from_B0FFFDC4BP_to_B000A9NO8R_T1_angular_order_q0/base/direct/wprd01_direct.png")
img = Image.open(img_path).convert("RGB")
print(f"Original image: {img.size}")

# Resize using backend logic
from mapspatial.backends.veomni.latentum import LatentUMBackend
img_resized = LatentUMBackend._resize_image(img, 448, 224, 14, downsample_ratio=0.5)
print(f"Resized: {img_resized.size}")

# Convert to tensor
import numpy as np
pixel_values = torch.tensor(np.array(img_resized)).permute(2, 0, 1).float() / 255.0
pixel_values = pixel_values.unsqueeze(0).to("cuda").to(model.internvl.vision_model.dtype if hasattr(model.internvl.vision_model, 'dtype') else torch.bfloat16)
print(f"pixel_values shape: {pixel_values.shape}")

# Run through vision model directly
with torch.no_grad():
    vit_features = model.internvl.vision_model(pixel_values)
    print(f"vit_features shape: {vit_features.shape} (dim={vit_features.dim()})")

# Run through get_vit_feature
with torch.no_grad():
    vit_features2 = model.internvl.get_vit_feature(pixel_values)
    print(f"get_vit_feature shape: {vit_features2.shape}")

# Check config
ivcfg = model.internvl.config
print(f"\nInternVL config: downsample_ratio={ivcfg.downsample_ratio}")
print(f"  vision_config patch_size={ivcfg.vision_config.patch_size}, image_size={ivcfg.vision_config.image_size}")
print(f"  dynamic_image_size={getattr(ivcfg, 'dynamic_image_size', 'N/A')}")
print(f"  force_image_size={getattr(ivcfg, 'force_image_size', 'N/A')}")

# Check vision_model
vm = model.internvl.vision_model
print(f"\nVision model type: {type(vm).__name__}")
print(f"  patch_size: {vm.config.patch_size if hasattr(vm, 'config') else 'N/A'}")

del model
torch.cuda.empty_cache()
