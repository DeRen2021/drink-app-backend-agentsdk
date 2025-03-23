from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
from dotenv import load_dotenv
from utils.config import OPENAI_API_KEY
from dataclasses import dataclass

from utils.sql_function import UserInfo,triage_agent
from agents import Runner
# 加载环境变量
load_dotenv()


# 创建FastAPI应用
app = FastAPI(
    title="OpenAI API集成",
    description="一个使用FastAPI集成OpenAI API的简单服务",
    version="0.1.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应限制来源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 定义请求模型
class ChatRequest(BaseModel):
    messages: List[dict] = Field(..., example=[
        {"role": "system", "content": "你是一个有用的助手。"},
        {"role": "user", "content": "你好，请介绍一下自己。"}
    ])
    model: Optional[str] = Field(default="gpt-4o", example="gpt-4o")

# 定义响应模型
class ChatResponse(BaseModel):
    response: str
    #usage: dict

# 健康检查端点
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# 聊天端点
@app.post("/chat", response_model=ChatResponse)
async def create_chat_completion(request: ChatRequest, req: Request):
    try:
        # 提取JWT令牌
        auth_header = req.headers.get("authorization", "")
        jwt_token = None
        if auth_header and auth_header.startswith("Bearer "):
            jwt_token = auth_header[7:]  # 删除"Bearer "前缀
            print(f"已提取JWT令牌: {jwt_token}")
        
        user_info = UserInfo(jwt_token=jwt_token)
        
        result = await Runner.run(
            starting_agent=triage_agent,
            input=request.messages,
            context=user_info
        )

        return ChatResponse(response=result.final_output)
    
    except Exception as e:
        # 处理错误
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"OpenAI API错误: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    # 启动服务器
    uvicorn.run("app:app", host="0.0.0.0", port=8334, reload=True)
