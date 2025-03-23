# OpenAI FastAPI 集成服务

这是一个使用FastAPI框架集成OpenAI API的简单服务。

## 功能

- 提供健康检查接口
- 提供聊天接口，连接到OpenAI的GPT模型
- 支持自定义模型参数

## 安装

1. 克隆仓库
```bash
git clone <repository-url>
cd <repository-directory>
```

2. 创建并激活虚拟环境
```bash
python3 -m venv --clear backend_venv
source backend_venv/bin/activate
```

3. 安装依赖
```bash
pip install fastapi uvicorn openai python-dotenv
```

4. 设置环境变量

将您的OpenAI API密钥添加到`.env`文件中：
```
OPENAI_API_KEY=your_openai_api_key_here
```

## 运行服务

```bash
python app.py
```

或者使用uvicorn直接运行：
```bash
uvicorn app:app --reload
```

服务将在 http://127.0.0.1:8000 上运行。

## API 文档

服务启动后，可以访问以下链接查看交互式API文档：
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## API 端点

### 健康检查

```
GET /health
```

### 聊天接口

```
POST /chat
```

请求体示例：
```json
{
  "messages": [
    {"role": "system", "content": "你是一个有用的助手。"},
    {"role": "user", "content": "你好，请介绍一下自己。"}
  ],
  "model": "gpt-3.5-turbo",
  "temperature": 0.7,
  "max_tokens": 1000
}
```

响应示例：
```json
{
  "response": "你好！我是一个AI助手，旨在帮助回答问题、提供信息和支持各种任务...",
  "usage": {
    "prompt_tokens": 33,
    "completion_tokens": 64,
    "total_tokens": 97
  }
}
```

## 注意事项

- 在生产环境中，请确保适当配置CORS和安全措施
- 本服务需要有效的OpenAI API密钥才能工作 