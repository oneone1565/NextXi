from nexi import nextxi, show_algo_plan
from addon import nextxi as nextxi_full

# ===== NextXi v2.0 多算法加密演示 =====
print("🔑 NextXi 多算法加密引擎 v2.0")
print("=" * 40)

key = b"\x01\x02\x03\x04"
msg = "Hello NextXi!"

# 展示算法轮转
print("\n📋 算法轮转：")
print(show_algo_plan(8))

# 加密解密
print(f"\n📝 明文: {msg}")
enc = nextxi(msg, key=key)
print(f"🔐 密文: {enc.hex()}")
dec = nextxi(enc, key=key, decrypt=True)
print(f"🔓 解密: {dec.decode()}")

# Nesh 增强模式
print(f"\n🔮 Nesh 增强加密:")
nesh_enc = nextxi_full(msg, key=key, use_nesh=True)
print(f"🔐 密文: {nesh_enc.hex()}")
