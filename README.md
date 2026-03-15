# LangChain DeepSeek Agent

这是一个基于 **LangChain**、**Typer** 和 **Rich** 构建的交互式简单 AI Agent 命令行工具。它使用 **DeepSeek**大模型作为底层智能体，并以猫娘的傲娇可爱性格与用户互动。

## 功能特性

- **交互式命令行**：基于 Typer 和 Rich 实现美观的终端交互界面。
- **本地文件操作**：Agent 具备读取文件和写入文件的能力。
- **终端命令执行**：Agent 可以在获取用户许可后，在当前的系统环境中执行终端命令。
- **RAG 知识库检索**：集成了 Chroma 向量数据库和 HuggingFace Embeddings，支持将本地知识检索并作为 Agent 的上下文补充。
- **丰富的内置工具**：包括基础工具与高级文本分析工具。

## 核心文件结构

- `Agent.py`：Agent 的主程序入口，包含了交互逻辑、提示词定义和 LangChain Agent 的创建。
- `Rag_tools.py`：RAG 相关的工具集，负责加载本地 Chroma 数据库以提供知识库查询（`query_knowledge_base`）功能。
- `my_tools.py`：通用的基础工具函数定义。
- `advanced_tools.py`：更高级深入的分析处理工具定义（如文本分析、代码块提取等）。

*注意：本项目的一些测试文件、展示 Demo 和第三方网关代码均已在 `.gitignore` 中忽略。*

## 快速开始

### 1. 安装依赖

请确保你已经安装了 Python 3.9+ 环境，并安装相关的依赖包（如 `langchain`, `langchain-deepseek`, `langchain-huggingface`, `typer`, `rich`, `chromadb` 等）。

### 2. 配置环境变量

在项目根目录下创建一个 `.env` 文件，并存入你的 API Key 等环境变量：
```env
DEEPSEEK_API_KEY=your_api_key_here
```

### 3. 启动应用

在终端中执行以下命令并传入项目路径即可启动 Agent：

```bash
python Agent.py ./
```

进入交互界面后，你可以向 Agent 提问或派发任务，输入 `exit` 或 `quit` 即可退出。
# langchaindemo-cat
