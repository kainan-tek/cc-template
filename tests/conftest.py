"""共享测试 fixtures"""
import sys
from pathlib import Path

# 将项目根目录加入 sys.path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

MODULES_DIR = PROJECT_ROOT / "modules"
PRESETS_DIR = PROJECT_ROOT / "presets"
