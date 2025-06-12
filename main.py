import os
from dotenv import load_dotenv
from typing import cast
import chainlit as cl
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel ,RunConfig

# Load environment variables from .env file
load_dotenv()

# Get Gemini API key
gemini_api_key = os.getenv("GEMINI_API_KEY")


@cl.on_chat_start
async def start():
    # Setup Gemini as OpenAI-compatible client
    external_client = AsyncOpenAI(
        api_key=gemini_api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    )

    model = OpenAIChatCompletionsModel(
        model="gemini-2.0-flash",
        openai_client=external_client
    )

    config = RunConfig(
        model=model,
        model_provider=external_client,
        tracing_disabled=True
    )

    # Initialize session
    cl.user_session.set("chat_history", [])
    cl.user_session.set("config", config)

    # Create article-writing agent
    agent: Agent = Agent(
        name="articles writer",
        instructions="You have to write complete articles on any topic which is given to you.",
        model=model
    )
    cl.user_session.set("agent", agent)

    await cl.Message(content="👋 Welcome! Ask me to write an article on any topic.").send()


@cl.on_message
async def main(message: cl.Message):
    # Show thinking message
    msg = cl.Message(content="🧠 Thinking...")
    await msg.send()

    agent: Agent = cast(Agent, cl.user_session.get("agent"))
    config: RunConfig = cast(RunConfig, cl.user_session.get("config"))

    # Retrieve and update chat history
    history = cl.user_session.get("chat_history") or []
    history.append({"role": "user", "content": message.content})

    
    

        # Run agent with full history
    result = Runner.run_sync(
            starting_agent=agent,
            input=history,
            run_config=config
        )

    response_content = result.final_output

        # Update message with agent's response
    msg.content = response_content
    await msg.update()

        # Save updated history
    cl.user_session.set("chat_history", result.to_input_list())

        