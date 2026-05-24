"""init.py 集成测试"""
import json
import pytest
from pathlib import Path
from init import run_init


class TestInitIntegration:
    def test_preset_and_module_exclusive(self, tmp_path):
        """--preset 和 --module 不可同时使用"""
        from conftest import MODULES_DIR, PRESETS_DIR
        if not MODULES_DIR.exists():
            pytest.skip("modules directory not yet created")

        target = tmp_path / "my-project"
        with pytest.raises(ValueError, match="[Pp]reset.*[Mm]odule"):
            run_init(
                target_dir=target,
                modules_dir=MODULES_DIR,
                presets_dir=PRESETS_DIR,
                preset="preset-minimal",
                modules=["core"],
                non_interactive=True,
            )

    def test_non_interactive_missing_required_var(self, tmp_path):
        """非交互模式缺少必填变量时报错"""
        from conftest import MODULES_DIR, PRESETS_DIR
        if not MODULES_DIR.exists():
            pytest.skip("modules directory not yet created")

        target = tmp_path / "my-project"
        with pytest.raises(ValueError):
            run_init(
                target_dir=target,
                modules_dir=MODULES_DIR,
                presets_dir=PRESETS_DIR,
                preset="preset-minimal",
                non_interactive=True,
            )

    def test_diff_mode_no_files_written(self, tmp_path):
        """--diff 模式不写入文件"""
        from conftest import MODULES_DIR, PRESETS_DIR
        if not MODULES_DIR.exists():
            pytest.skip("modules directory not yet created")

        target = tmp_path / "my-project"
        run_init(
            target_dir=target,
            modules_dir=MODULES_DIR,
            presets_dir=PRESETS_DIR,
            preset="preset-minimal",
            non_interactive=True,
            cli_vars={"PROJECT_NAME": "test-proj", "PROJECT_DESCRIPTION": "Test", "TECH_STACK": "Python"},
            diff_only=True,
        )

        assert not (target / "CLAUDE.md").exists()
