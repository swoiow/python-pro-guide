# Best-Practices / 最佳实践

- **System Operations**
    - For file read/write operations pertaining to Codex (any MCP instance), the recommended approach is to employ [mcp-filesystem-python](https://github.com/harmonsir/mcp-filesystem-python).
    - 对于涉及 Codex（任何 MCP 实例）的文件读写操作，推荐采用 [mcp-filesystem-python](https://github.com/harmonsir/mcp-filesystem-python)。

- **Artifact Orchestration**
    - Use `pybuild.py` as the industrial-grade build engine. It replaces traditional Makefiles to manage environment validation, path resolution, and PyInstaller synthesis in a high-cohesion, Pythonic manner.
    - 使用 `pybuild.py` 作为工业级构建引擎。它通过高内聚的 Python 化方式替代了传统的 Makefile，用于管理环境校验、路径解析及 PyInstaller 综合打包。

- **AI Agent Context: AGENT.md**
    - This file is strictly reserved for Python-specific context. It serves as the primary "Source of Truth" for AI Agents regarding project internal logic, coding standards, and dependency graphs.
    - 此文件仅用于 Python 专用上下文。它是 AI 代理关于项目内部逻辑、编码标准和依赖图谱的核心“事实来源”。

- **AI Agent Context: workflows**
    - Designed for CI/CD automation. It provides the AI with structural examples and templates for generating or maintaining GitHub Actions and deployment pipelines.
    - 专为 CI/CD 自动化设计。为 AI 提供结构化示例和模板，用于生成或维护 GitHub Actions 脚本及部署流水线。
