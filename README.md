# 🌐 MultimodalChat

> MultimodalChat 是一个多模态对话系统开源项目，旨在帮助大家通过一个简单易懂的案例学习多模态对话机器人的构建与实现。本项目支持文字、语音、图片和视频输入，并提供 Gradio 网页界面，方便用户使用。此外，项目还具备聊天记录保存、上下文修剪与摘要记忆功能，以及流式输出和在大模型回复时禁用输入提交等高级特性，为用户提供流畅且高效的交互体验。

---

## 🔍 功能亮点

- ✅ **多模态输入支持**：接受文本、音频、图像和视频作为输入。
- 🧠 **多模型调用接口**：
  - 支持多种大语言模型或视觉模型（本地部署 / API 接口）。
- 💬 **历史记录管理**：
  - 完整保存聊天记录。
  - 智能修剪上下文长度。
  - 自动生成长期记忆摘要。
- 🎤 **在线语音录制**：
  - 浏览器中可直接录音并识别。
- 🖼️ **多媒体处理能力**：
  - 支持两条技术路径：
    - **ModuText**：各模态转为文字后送入 LLM
    - **MultiFlow**：多模态内容直接送入多模态大模型
- 🌐 **Gradio Web 界面**：
  - 提供交互式网页体验，便于演示与测试
- ⏱️ 流式输出（Streaming Output）： 
  - 大语言模型回复时逐字生成，提升交互流畅性和实时感。
- 🔒 回复时禁用输入提交（Input Locking）： 
  - 在模型生成回复期间自动禁用输入提交，防止重复请求和界面混乱。
---

## 🧩 项目架构概览

```
Qwen-Multimodal-Demo/
├── README.md                 # 项目总说明文档，介绍功能、依赖和使用方式
├── .env                      # 环境变量配置文件（如 API Key、模型路径等）
├── config.py                 # 配置中心：包含 SESSION_ID、Prompt参数
├── env_utils.py              # 环境变量工具类：用于读取 `.env` 文件内容
├── my_llm.py                 # 自定义 LLM 模块：封装本地模型或远程调用逻辑
├── modelText/                # 子模块：模态识别 → 文字 → 调用 LLM
│   ├── README.md             # ModuText 技术路径说明
│   ├── chains.py             # LangChain 构建提示词模板 + LLM 调用链
│   ├── handlers.py           # 用户交互处理：消息添加、提交、多媒体解析
│   ├── main.py               # Gradio 界面入口：ModuText 模式界面启动
│   ├── models.py             # 数据库连接、历史记录管理、会话状态维护
│   └── __init__.py           # 标识为 Python 包
└── multiFlow/                # 子模块：多模态输入 → 多模态 LLM
    ├── README.md             # MultiFlow 技术路径说明
    ├── chains.py             # LangChain 构建多模态提示链
    ├── handlers.py           # 用户交互处理：支持图像、语音、文本混合输入
    ├── main.py               # Gradio 界面入口：MultiFlow 模式界面启动
    ├── models.py             # 多模态模型调用逻辑、数据库连接等
    └── __init__.py           # 标识为 Python 包
```

---

## 🚀 快速开始

### 前提条件：

- Python 3.12+
- pip
- 可选：GPU 加速推理

### 安装步骤：

```bash
git clone https://github.com/AnchorYYC/MultimodelChat.git
cd MultimodalChat
pip install -r requirements.txt
```

---
## ⚙️ 项目配置指南

本指南旨在帮助你快速完成项目的环境与模块配置，确保系统能够顺利运行并支持多模态对话功能。通过以下步骤，你可以轻松设置 API 密钥、模型参数以及核心功能模块。

### 1. 配置 `.env` 环境变量文件

在项目根目录下创建或编辑 `.env` 文件，添加如下环境变量以支持不同平台的大模型调用：

```
LOCAL_BASE_URL=https://your-local-server-url.com
ZHIPU_API_KEY=your_zhipu_api_key_here
ZHIPU_BASE_URL=https://example.url
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_BASE_URL=https://example.url
```

这些变量可通过 `utils/env_utils.py` 被导入到 Python 代码中，用于动态加载 API 地址和密钥，提升配置灵活性与安全性。

### 2. 配置大语言模型（LLM）

在 `my_llm.py` 中，已预设多个大模型的调用接口，并通过 `model` 参数指定当前使用的大模型。你可以根据需要切换或扩展支持的模型类型。

### 3. 配置语音识别模块

在 `modelText/handlers.py` 中，可配置语音转文字所使用的模型服务。目前默认集成的是智谱 AI 的 `glm-asr` 语音识别接口，你也可以替换为你偏好的 ASR 模型。

### 4. 配置会话与提示词逻辑

在 `config.py` 中，可设置以下关键参数：

- **会话 ID**：用于区分不同用户的聊天记录。
- **提示词模板**：定义模型响应时的初始指令和格式规范。

该配置文件是实现个性化对话记忆和上下文管理的基础组件之一。

------

通过以上配置，你可以快速启动并自定义这个开源项目，非常适合用于学习多模态对话系统的构建流程与关键技术实践。如果你希望进一步扩展功能或对接更多模型服务，欢迎参考项目文档或贡献代码！

---

## 📦 支持的模型列表

| 模型名称        | 描述                                                         |
| --------------- | ------------------------------------------------------------ |
| Qwen2.5-Omni-3B | 本地私有化的大语言模型，适用于多种自然语言处理任务。         |
| glm-4-plus      | 智谱提供的大语言模型，具有强大的文本生成和理解能力(详见 [GLM-4官方文档](https://bigmodel.cn/dev/api/normal-model/glm-4))。 |
| glm-asr         | 智谱提供的语音识别模型，能够将语音转换为流畅的文字输出，支持多种方言和嘈杂环境下的语音识别（详见 [GLM-ASR官方文档](https://bigmodel.cn/dev/api/rtav/glm-asr)）。 |

---

## 🛠️ 贡献指南

我们欢迎任何形式的贡献！无论是优化 UI、新增模型支持、还是增强多媒体处理模块，都非常欢迎！

祝你开源顺利，收获满满 Star⭐！🎉

# 附：本地部署大模型指南

本节介绍如何在本地服务器上部署 Qwen 系列多模态大模型（如 Qwen2.5-Omni-3B），以便在本项目中实现高性能、低延迟的推理服务。

## 1. 下载模型（以魔塔社区模型为例）

使用 ModelScope 的 SDK 方式下载模型，推荐使用如下命令获取 Qwen2.5-Omni-3B 模型：

```
from modelscope.hub.snapshot_download import snapshot_download

model_dir = snapshot_download('Qwen/Qwen2.5-Omni-3B', cache_dir='/root/autodl-tmp/models', revision='master')
```

该命令会将模型文件下载至指定目录，供后续部署使用。

## 2. 安装音频支持库

若需支持语音输入处理，请安装带有音频模块的 vLLM：

bash

浅色版本



```
pip install vllm[audio]
```

## 3. 启动模型服务

使用以下命令启动基于 vLLM 的 OpenAI 兼容 API 服务：

```
python -m vllm.entrypoints.openai.api_server \
--model /root/autodl-tmp/models/Qwen/Qwen2___5-Omni-3B \
--served-model-name qwen2.5-omni-3b \
--max-model-len 8k \
--host 0.0.0.0 \
--port 6006 \
--dtype bfloat16 \
--gpu-memory-utilization 0.8 \
--enable-auto-tool-choice \
--tool-call-parser hermes
```

> ⚠️ 注意：模型路径中的版本名 `Qwen2___5-Omni-3B` 是由模型仓库名称转换而来，请确保路径正确。
>
> 以上启动命令一般情况下即可启动成功。
>
> 自定义部署本地大模型服务时，您可能需要根据实际硬件环境和需求调整一些关键参数。以下是如何配置这些参数以及如何确认部署成功的详细步骤。
>
> #### 1. 根据实际情况配置部署参数
>
> **模型文件路径 (`--model`)**
>
> 指定要加载的大模型文件路径。例如，使用 Qwen2.5-Omni-3B 模型时：
>
> ```
> --model /root/autodl-tmp/models/Qwen/Qwen2___5-Omni-3B
> ```
>
> 请确保路径指向正确的模型目录。
>
> **部署端口 (`--port`)**
>
> 指定服务器监听的端口号，默认为 `6006`。如果该端口已被占用或有其他需求，可以更改此参数：
>
> ```
> --port 7007
> ```
>
> 同时，请记得更新 `.env` 文件中的 `LOCAL_BASE_URL` 相应地指向新端口：
>
> ```
> LOCAL_BASE_URL=http://localhost:7007/v1
> ```
>
> **最大上下文长度 (`--max-model-len`)**
>
> 设置最大上下文长度（以 token 数量表示），这取决于您的 GPU 显存大小。对于一张 NVIDIA RTX 4090D 显卡，建议值为 `8k`：
>
> ```
> --max-model-len 8k
> ```
>
> #### 2. 替换其它模型的配置
>
> 如果您希望部署其他模型，请替换以下参数：
>
> **模型名称 (`--served-model-name`)**
>
> 为每个部署的模型指定一个唯一的服务名称，以便于管理和调用：
>
> ```
> --served-model-name your_model_name
> ```
>
> **参数精度 (`dtype`)**
>
> 选择适合您硬件的最佳参数精度类型。常见的选项包括 `float32`、`bfloat16` 和 `float16`。对于大多数现代 GPU，推荐使用 `bfloat16`：
>
> ```
> --dtype bfloat16
> ```
>
> #### 3. 确认部署成功
>
> 当所有配置正确无误且服务器启动成功后，终端会打印如下信息：
>
> ```
> INFO:     Started server process [PID]
> INFO:     Waiting for application startup.
> INFO:     Application startup complete.
> INFO:     Uvicorn running on http://0.0.0.0:6006 (Press CTRL+C to quit)
> ```
>
> 这表明服务器已成功启动，并准备接受请求。

## 4. 配置本地 API 地址

如果本地部署的服务运行在默认端口 `6006` 上，请在 `.env` 文件中配置如下地址：

```
LOCAL_BASE_URL=http://localhost:6006/v1
```

这样，项目即可自动识别并调用本地部署的大模型服务。