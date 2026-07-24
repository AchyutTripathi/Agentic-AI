import os
import asyncio
from urllib import response

from dotenv import load_dotenv

from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_groq import ChatGroq
from langchain.agents import create_agent

load_dotenv()


async def main():
    client = MultiServerMCPClient(
        {
            "math": {
                "command": "python",
                "args": ["mathserver.py"],
                "transport": "stdio",
            },
            "weather": {
                "url": "http://localhost:8000/mcp",
                "transport": "streamable-http",
            },
        }
    )

    # Load MCP tools
    tools = await client.get_tools()

    # Groq API Key
    os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

    # Groq Model
    model = ChatGroq(
        model="openai/gpt-oss-120b"
    )

    # Create Agent
    agent = create_agent(
        model=model,
        tools=tools,
        system_prompt=(
            "You are a helpful AI assistant. "
            "Use the available tools whenever necessary."
        ),
    )

    # Invoke Agent
    math_response = await agent.ainvoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "What is (3 + 5) * 12?",
                }
            ]
        }
    )

    print("\nAssistant:\n")
    print("math_response:", math_response["messages"][-1].content)



    # Invoke Agent
    weather_response = await agent.ainvoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "What is the weather like in California?",
                }
            ]
        }
    )

    print("\nAssistant:\n")
    print("weather_response:", weather_response["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())