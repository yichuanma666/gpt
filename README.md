# Codex 5.6 部署控制中心

这是一个面向本地 Codex 配置目录的部署与维护工具，提供 Tkinter 图形界面和命令行核心。它支持预览、部署、状态检查、卸载、事务恢复、hooks 恢复和环境诊断。

## 快速开始

### Windows

双击 `启动脚本.bat`。脚本会检查 Python 3.10+ 与 Tkinter，并启动控制中心。

### macOS

```sh
./launch-macos.command
```

### Linux

```sh
./launch-linux.sh
```

## 命令行

所有写入操作默认先预览；只有显式加入 `--yes` 才会落盘。

```sh
python codex56-orchestrator.py --codex-dir ~/.codex --dry-run
python codex56-orchestrator.py --codex-dir ~/.codex --yes
python codex56-orchestrator.py --codex-dir ~/.codex --status
python codex56-orchestrator.py --codex-dir ~/.codex --doctor
python codex56-orchestrator.py --codex-dir ~/.codex --recover --yes
python codex56-orchestrator.py --codex-dir ~/.codex --uninstall --yes
```

`--doctor` 是只读操作，会输出 Python、平台、核心脚本 SHA-256，以及目标目录的部署审计结果。GUI 的“运行环境诊断”操作使用同一条命令。

## 测试

项目测试仅使用 Python 标准库：

```sh
python -m unittest discover -s tests -v
```

## 目录说明

- `codex56-orchestrator.py`：部署事务核心与 CLI。
- `codex56-control-center.py`：Tkinter 控制中心。
- `tests/`：核心纯函数与 CLI 回归测试。
- `launch-*.command|.sh`、`启动脚本.bat`：平台启动入口。

版本：`0.2.0`
