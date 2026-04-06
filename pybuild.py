"""
================================================================================
PROJECT: PyBuild - Industrial Build Engine
VERSION: 2.0.0
AUTHOR: Gemini Adaptive AI
LICENSE: MIT
--------------------------------------------------------------------------------
DESCRIPTION (English):
This script provides an engine for
building Python projects into standalone executables using PyInstaller.
It features a declarative configuration, absolute path resolution for Windows
environments, and automated cleanup. It is specifically optimized for projects
with C-extensions (like poptrie) and complex virtual environment structures.

DESCRIPTION (中文):
本脚本提供了一个自动化构建引擎，用于将 Python 项目通过 PyInstaller
打包为独立可执行文件。其核心特性包括声明式配置、针对 Windows 环境的绝对路径解析
以及自动化的构建环境清理。本脚本特别针对包含 C 扩展库（如 poptrie）及复杂虚拟环境
的项目进行了深度优化。

ARCHITECTURE (架构):
1. TerminalUI:     Decoupled logging and ANSI coloring. (UI 与日志解耦)
2. BuildContext:   Centralized filesystem and path strategy. (路径与环境策略)
3. PyInstallerEngine: Execution logic and command construction. (构建执行引擎)
4. Main/Config:    Declarative interface for project settings. (声明式配置接口)

USAGE (用法):
- Build:  python pybuild.py
- Clean:  python pybuild.py clean
================================================================================
"""

import os
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Dict, List


# --- 1. UI Strategy ---
class TerminalUI:
    """Handles all user-facing communication with standardized styling."""
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    RESET = "\033[0m"

    @staticmethod
    def header(msg: str):
        print(f"\n{TerminalUI.BOLD}{TerminalUI.CYAN}🚀 {msg.upper()}{TerminalUI.RESET}")
        print(f"{TerminalUI.CYAN}{"=" * 60}{TerminalUI.RESET}")

    @staticmethod
    def step(msg: str):
        print(f"{TerminalUI.BLUE}🔹 {msg}{TerminalUI.RESET}")

    @staticmethod
    def info(key: str, value: Any):
        print(f"   {TerminalUI.BOLD}{key:<15}:{TerminalUI.RESET} {value}")

    @staticmethod
    def status(msg: str, success: bool = True):
        color = TerminalUI.GREEN if success else TerminalUI.YELLOW
        symbol = "✔" if success else "!"
        print(f"   {color}{symbol} {msg}{TerminalUI.RESET}")

    @staticmethod
    def error(msg: str):
        print(f"\n{TerminalUI.BOLD}{TerminalUI.RED}✘ ERROR: {msg}{TerminalUI.RESET}")


# --- 2. Path & Environment Manager ---
class BuildContext:
    """Manages path resolution and environment metadata."""

    def __init__(self, app_name: str, entry_point: str):
        self.root = Path(__file__).resolve().parent
        self.app_name = app_name
        self.entry_path = (self.root / entry_point).resolve()
        self.work_dir = self.root / "build"
        self.dist_dir = self.root / "dist"
        self.spec_file = self.root / f"{app_name}.spec"
        self.output_exe = self.root / app_name

    def get_search_paths(self, relative_list: List[str]) -> str:
        """Resolves a list of relative paths to absolute strings."""
        return ",".join([str((self.root / p).resolve()) for p in relative_list])

    def get_cleanup_targets(self) -> List[Path]:
        """Defines what should be removed during a clean cycle."""
        return [self.work_dir, self.dist_dir, self.spec_file, self.output_exe]


# --- 3. Execution Engine ---
class PyInstallerEngine:
    """Orchestrates the actual PyInstaller process."""

    def __init__(self, ctx: BuildContext, config: Dict[str, Any]):
        self.ctx = ctx
        self.config = config

    def run_clean(self):
        TerminalUI.step("Cleaning Workspace")
        for target in self.ctx.get_cleanup_targets():
            if target.exists():
                try:
                    if target.is_dir():
                        shutil.rmtree(target)
                    else:
                        target.unlink()
                    TerminalUI.status(f"Removed: {target.name}")
                except Exception as e:
                    TerminalUI.status(f"Skipped: {target.name} ({e})", success=False)

    def run_build(self):
        TerminalUI.header(f"Build Phase: {self.ctx.app_name}")

        # Build Command Construction
        cmd = [
            sys.executable, "-m", "PyInstaller",
            "--onefile" if self.config.get("onefile", True) else "--onedir",
            "--clean",
            "--name", self.ctx.app_name,
            "--distpath", str(self.ctx.root),
            "--workpath", str(self.ctx.work_dir),
            "--paths", self.ctx.get_search_paths(self.config.get("search_paths", []))
        ]

        if self.config.get("no_console", True):
            cmd.append("--noconsole")

        if self.config.get("no_upx", False):
            cmd.append("--noupx")

        for pkg in self.config.get("collect_packages", []):
            cmd.extend(["--collect-all", pkg, "--copy-metadata", pkg])

        cmd.append(str(self.ctx.entry_path))

        # Execution
        TerminalUI.step("Invoking PyInstaller Process")
        start_time = time.time()
        try:
            subprocess.run(cmd, check=True, env=os.environ.copy())
            duration = time.time() - start_time
            TerminalUI.status(f"Build successful in {duration:.2f}s")
            TerminalUI.info("Output Path", self.ctx.output_exe)
        except subprocess.CalledProcessError:
            TerminalUI.error("PyInstaller execution failed.")
            sys.exit(1)


# --- 4. Main Entry Point ---
def main():
    # Declarative Project Configuration
    config = {
        "app_name": "next_dns.exe",
        "entry_point": "main.py",
        "onefile": True,
        "no_console": False,
        "no_upx": True,
        "search_paths": [".."],
        "collect_packages": ["poptrie"],
    }

    # Initialize Components
    ctx = BuildContext(config["app_name"], config["entry_point"])
    engine = PyInstallerEngine(ctx, config)

    # Command Line Interface Logic
    if len(sys.argv) > 1 and sys.argv[1].lower() == "clean":
        engine.run_clean()
    else:
        engine.run_clean()
        engine.run_build()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        TerminalUI.error("Process aborted by user.")
        sys.exit(0)
