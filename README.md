# OpenAI FastAPI Integration Service

This is a simple service that integrates OpenAI API with FastAPI framework.

## Features

- Health check endpoint
- Chat interface connected to OpenAI's GPT models
- Support for custom model parameters
- SQL backend integration
- JWT authentication support

## Installation

1. Clone the repository
```bash
git clone <repository-url>
cd <repository-directory>
```

2. Create and activate virtual environment
```bash
python3 -m venv --clear backend_venv
source backend_venv/bin/activate
```

3. Install dependencies

All the required dependencies are listed in `requirements.txt`. Install them with:
```bash
pip install -r requirements.txt
```

4. Set up environment variables

Create a `.env` file in the project root with the following variables:
```
OPENAI_API_KEY=your_openai_api_key_here
SQL_BACKEND_API_URL=your_sql_backend_api_url
```

## Project Structure

```
project_root/
├── app.py             # Main application file
├── requirements.txt   # Project dependencies
├── utils/
│   ├── config.py      # Configuration loading
│   └── sql_function.py # SQL backend integration
└── agents/            # Agents implementation
```

## Running the Service

```bash
python app.py
```

Or run directly with uvicorn:
```bash
uvicorn app:app --host="0.0.0.0" --port=8334 --reload
```

The service will run on http://0.0.0.0:8334.

## API Documentation

After starting the service, you can access the interactive API documentation at:
- Swagger UI: http://0.0.0.0:8334/docs
- ReDoc: http://0.0.0.0:8334/redoc

## API Endpoints

### Health Check

```
GET /health
```

Returns:
```json
{
  "status": "healthy"
}
```

### Chat Interface

```
POST /chat
```

Example request body:
```json
{
  "messages": [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello, please introduce yourself."}
  ],
  "model": "gpt-4o"
}
```

Headers:
```
Authorization: Bearer your_jwt_token
```

Example response:
```json
{
  "response": "Hello! I am an AI assistant designed to help answer questions, provide information and support various tasks..."
}
```

## Notes

- In production environments, ensure proper CORS and security measures are configured
- This service requires a valid OpenAI API key to work
- JWT authentication is supported for user identification

---

# OpenAI FastAPI 集成服务

这是一个使用FastAPI框架集成OpenAI API的简单服务。

## 功能

- 提供健康检查接口
- 提供聊天接口，连接到OpenAI的GPT模型
- 支持自定义模型参数
- SQL后端集成
- JWT身份验证支持

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

所有必需的依赖项都列在`requirements.txt`中。使用以下命令安装它们：
```bash
pip install -r requirements.txt
```

4. 设置环境变量

在项目根目录创建一个`.env`文件，包含以下变量：
```
OPENAI_API_KEY=你的OpenAI_API密钥
SQL_BACKEND_API_URL=你的SQL后端API地址
```

## 项目结构

```
project_root/
├── app.py             # 主应用程序文件
├── requirements.txt   # 项目依赖
├── utils/
│   ├── config.py      # 配置加载
│   └── sql_function.py # SQL后端集成
└── agents/            # 代理实现
```

## 运行服务

```bash
python app.py
```

或者使用uvicorn直接运行：
```bash
uvicorn app:app --host="0.0.0.0" --port=8334 --reload
```

服务将在 http://0.0.0.0:8334 上运行。

## API 文档

服务启动后，可以访问以下链接查看交互式API文档：
- Swagger UI: http://0.0.0.0:8334/docs
- ReDoc: http://0.0.0.0:8334/redoc

## API 端点

### 健康检查

```
GET /health
```

返回：
```json
{
  "status": "healthy"
}
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
  "model": "gpt-4o"
}
```

请求头：
```
Authorization: Bearer 你的JWT令牌
```

响应示例：
```json
{
  "response": "你好！我是一个AI助手，旨在帮助回答问题、提供信息和支持各种任务..."
}
```

## 注意事项

- 在生产环境中，请确保适当配置CORS和安全措施
- 本服务需要有效的OpenAI API密钥才能工作
- 支持JWT身份验证用于用户识别 