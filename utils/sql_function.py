# agent package
from agents import Agent,function_tool,WebSearchTool,RunContextWrapper, Runner
from pydantic import BaseModel, Field, FieldValidationInfo, field_validator
from .config import SQL_BACKEND_API_URL
from typing import List

#web package
import aiohttp
import requests


# 获取酒类列表
API_ENDPOINT = "https://drink1.deren.life/api/liquors/"
try:
    response = requests.get(API_ENDPOINT)
    LIQUOR_LIST = [i['name'] for i in response.json()["data"]]
except Exception as e:
    print(f"无法获取酒类列表: {e}")
    LIQUOR_LIST = ["未能加载酒类列表"]  # 提供默认值以防API调用失败


class insert_liquor_request(BaseModel):
    liquor_name: str = Field(..., description="酒类名称")
    jwt_token: str = Field(..., description="JWT认证令牌")
    
    # 使用pydantic验证器
    @field_validator('liquor_name')
    @classmethod
    def validate_liquor_name(cls, v):
        if v not in LIQUOR_LIST:
            raise ValueError(f"""invalid liquor name: {v}, 
            maybe has a different spelling or the ingredient is not in the list.
            The current ingredients in db are: {', '.join(LIQUOR_LIST)}""")
        return v

@function_tool
async def insert_liquor(insert_liquor_request:insert_liquor_request):
    # 验证器会自动运行，无需手动调用
    
    # get liquor id
    liquor_endpoint = f"{SQL_BACKEND_API_URL}/api/liquors/name/{insert_liquor_request.liquor_name}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(liquor_endpoint) as response:
                resp_json = await response.json()
                liquor_id = resp_json["data"]["id"]
    except Exception as e:
        print(e)
        return {"error": f"获取酒类ID失败: {str(e)}"}

    # add liquor to user
    add_liquor_endpoint = f"{SQL_BACKEND_API_URL}/api/user-liquors/cabinet"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {insert_liquor_request.jwt_token}"
    }

    payload = {
        "liquorId": liquor_id
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(add_liquor_endpoint, headers=headers, json=payload) as response:
                return await response.json()
    except Exception as e:
        return {"error": f"添加酒类失败: {str(e)}"}


class remove_liquor_request(BaseModel):
    liquor_name: str = Field(..., description="酒类名称")
    jwt_token: str = Field(..., description="JWT认证令牌")
    
    @field_validator('liquor_name')
    @classmethod
    def validate_liquor_name(cls, v):
        if v not in LIQUOR_LIST:
            raise ValueError(f"""invalid liquor name: {v}, 
            maybe has a different spelling or the ingredient is not in the list.
            The current ingredients in db are: {', '.join(LIQUOR_LIST)}""")
        return v

@function_tool
async def remove_liquor(remove_liquor_request:remove_liquor_request):
    # get liquor id
    liquor_endpoint = f"{SQL_BACKEND_API_URL}/api/liquors/name/{remove_liquor_request.liquor_name}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(liquor_endpoint) as response:
                resp_json = await response.json()
                liquor_id = resp_json["data"]["id"]
    except Exception as e:
        print(e)
        return {"error": f"获取酒类ID失败: {str(e)}"}
    
    # remove liquor from user
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {remove_liquor_request.jwt_token}"
    }

    remove_liquor_endpoint = f"{SQL_BACKEND_API_URL}/api/user-liquors/cabinet/{liquor_id}"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.delete(remove_liquor_endpoint, headers=headers) as response:
                # 处理204 No Content响应
                if response.status == 204:
                    return {"success": True, "message": "酒类已成功从酒柜中移除"}
                # 处理其他状态码的响应
                try:
                    return await response.json()
                except:
                    return {"status": response.status, "message": f"服务器返回状态码: {response.status}"}
    except Exception as e:
        return {"error": f"移除酒类失败: {str(e)}"}



from agents import Agent
from dataclasses import dataclass
@dataclass
class UserInfo:  
    jwt_token:str

@function_tool
async def return_jwt_token(wrapper: RunContextWrapper[UserInfo]) -> str:  
    return wrapper.context.jwt_token

sql_db_agent = Agent(
    name="sql_db_agent",
    handoff_description="Specialist agent for add liquor into user's collection or remove liquor from user's collection",
    instructions="You are a assistant, you can help user to add liquor into user's collection or remove liquor from user's collection",
    tools=[insert_liquor, remove_liquor,return_jwt_token],
)

general_info_agent = Agent(
    name="general_info_agent",
    handoff_description="Specialist agent for provide general information about liquor and cocktail",
    instructions="You are a assistant, you can provide general information about liquor and cocktail",
    tools=[WebSearchTool()]
)

triage_agent = Agent[UserInfo](
            name="Triage Agent",
            instructions="""
            You determine which agent to use based on the user's question, 
            if user want to add liquor into user's collection, you should handoff to sql_db_agent,
            if user want some general information about liquor, you should handoff to general_info_agent
            """,
            handoffs=[sql_db_agent, general_info_agent]
        )