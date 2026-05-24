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


class TestEndToEnd:
    def test_preset_python_generates_all_files(self, tmp_path):
        """preset-python 生成所有预期文件"""
        from conftest import MODULES_DIR, PRESETS_DIR
        if not MODULES_DIR.exists():
            pytest.skip("modules directory not yet created")

        target = tmp_path / "my-api"
        run_init(
            target_dir=target,
            modules_dir=MODULES_DIR,
            presets_dir=PRESETS_DIR,
            preset="preset-python",
            non_interactive=True,
            cli_vars={
                "PROJECT_NAME": "my-api",
                "PROJECT_DESCRIPTION": "My API project",
                "TECH_STACK": "Python",
            },
        )

        # CLAUDE.md
        assert (target / "CLAUDE.md").exists()
        content = (target / "CLAUDE.md").read_text(encoding="utf-8")
        assert "my-api" in content
        assert "Python 编码规范" in content
        assert "Git 规范" in content

        # settings.json
        assert (target / ".claude" / "settings.json").exists()
        settings = json.loads((target / ".claude" / "settings.json").read_text(encoding="utf-8"))
        assert "Bash(pytest)" in settings["permissions"]["allow"]

        # .pre-commit-config.yaml
        assert (target / ".pre-commit-config.yaml").exists()

        # .gitignore
        assert (target / ".gitignore").exists()
        gitignore = (target / ".gitignore").read_text(encoding="utf-8")
        assert "__pycache__/" in gitignore

        # commands
        assert (target / ".claude" / "commands" / "commit.md").exists()
        assert (target / ".claude" / "commands" / "pytest.md").exists()

        # templates
        assert (target / "pyproject.toml").exists()

    def test_preset_cpp_generates_all_files(self, tmp_path):
        """preset-cpp 生成所有预期文件"""
        from conftest import MODULES_DIR, PRESETS_DIR
        if not MODULES_DIR.exists():
            pytest.skip("modules directory not yet created")

        target = tmp_path / "my-cpp-project"
        run_init(
            target_dir=target,
            modules_dir=MODULES_DIR,
            presets_dir=PRESETS_DIR,
            preset="preset-cpp",
            non_interactive=True,
            cli_vars={
                "PROJECT_NAME": "my-cpp-project",
                "PROJECT_DESCRIPTION": "My C++ project",
                "TECH_STACK": "C++",
            },
        )

        # CLAUDE.md
        assert (target / "CLAUDE.md").exists()
        content = (target / "CLAUDE.md").read_text(encoding="utf-8")
        assert "my-cpp-project" in content
        assert "C++ 编码规范" in content
        assert "Git 规范" in content

        # settings.json
        assert (target / ".claude" / "settings.json").exists()
        settings = json.loads((target / ".claude" / "settings.json").read_text(encoding="utf-8"))
        assert "Bash(ctest)" in settings["permissions"]["allow"]

        # .pre-commit-config.yaml
        assert (target / ".pre-commit-config.yaml").exists()

        # .gitignore
        assert (target / ".gitignore").exists()
        gitignore = (target / ".gitignore").read_text(encoding="utf-8")
        assert "build/" in gitignore

        # commands
        assert (target / ".claude" / "commands" / "commit.md").exists()
        assert (target / ".claude" / "commands" / "ctest.md").exists()

        # templates
        assert (target / "CMakeLists.txt").exists()

    def test_preset_shell_generates_all_files(self, tmp_path):
        """preset-shell 生成所有预期文件"""
        from conftest import MODULES_DIR, PRESETS_DIR
        if not MODULES_DIR.exists():
            pytest.skip("modules directory not yet created")

        target = tmp_path / "my-shell-project"
        run_init(
            target_dir=target,
            modules_dir=MODULES_DIR,
            presets_dir=PRESETS_DIR,
            preset="preset-shell",
            non_interactive=True,
            cli_vars={
                "PROJECT_NAME": "my-shell-project",
                "PROJECT_DESCRIPTION": "My Shell project",
                "TECH_STACK": "Shell",
            },
        )

        # CLAUDE.md
        assert (target / "CLAUDE.md").exists()
        content = (target / "CLAUDE.md").read_text(encoding="utf-8")
        assert "my-shell-project" in content
        assert "Shell 编码规范" in content
        assert "Git 规范" in content

        # settings.json
        assert (target / ".claude" / "settings.json").exists()
        settings = json.loads((target / ".claude" / "settings.json").read_text(encoding="utf-8"))
        assert "Bash(shellcheck)" in settings["permissions"]["allow"]

        # .pre-commit-config.yaml
        assert (target / ".pre-commit-config.yaml").exists()

        # .gitignore
        assert (target / ".gitignore").exists()
        gitignore = (target / ".gitignore").read_text(encoding="utf-8")
        assert "*.log" in gitignore

        # commands
        assert (target / ".claude" / "commands" / "commit.md").exists()
        assert (target / ".claude" / "commands" / "bats.md").exists()

        # templates
        assert (target / "scripts" / "main.sh").exists()

    def test_multi_language_coexist_e2e(self, tmp_path):
        """多语言模块可同时选中"""
        from conftest import MODULES_DIR, PRESETS_DIR
        if not MODULES_DIR.exists():
            pytest.skip("modules directory not yet created")

        target = tmp_path / "my-project"
        run_init(
            target_dir=target,
            modules_dir=MODULES_DIR,
            presets_dir=PRESETS_DIR,
            modules=["lang-python", "lang-cpp"],
            non_interactive=True,
            cli_vars={"PROJECT_NAME": "test", "PROJECT_DESCRIPTION": "test", "TECH_STACK": "test"},
        )
        # 应成功生成，两个语言的文件都存在
        assert (target / "pyproject.toml").exists()
        assert (target / "CMakeLists.txt").exists()
