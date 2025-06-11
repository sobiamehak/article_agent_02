
## 📄 Project Overview

This project is a **Chainlit-based AI chatbot** that uses **Gemini (by Google)** through an OpenAI-compatible interface. The chatbot acts as an article writer: when a user gives it a topic, it generates a complete article.

---

## 🧠 What This Code Does

### 🔧 1. **Imports and Setup**

```python
import os
from dotenv import load_dotenv
from typing import cast
import chainlit as cl
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel ,RunConfig
```

* Loads necessary Python libraries.
* Imports `Chainlit` (a framework to build chat-based UIs).
* Imports custom classes for creating and running AI agents.

---

### 🔐 2. **Load API Key**

```python
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
```

* Loads the Gemini API key from a `.env` file.

---

### 💬 3. **When Chat Starts**

```python
@cl.on_chat_start
async def start():
```

This function runs **once when the chat starts.** It sets up the Gemini AI client and initializes the article-writing agent.

#### ✅ Gemini Client Setup

```python
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)
```

* Creates an OpenAI-compatible client using the Gemini API.

#### 🤖 Define the AI Model

```python
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)
```

* Defines the AI model to use (`gemini-2.0-flash`).

#### ⚙️ Run Configuration

```python
config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)
```

* Configures the model for usage.

#### 💾 Save to User Session

```python
cl.user_session.set("chat_history", [])
cl.user_session.set("config", config)
```

* Initializes chat history and stores model config.

#### ✍️ Create the Agent

```python
agent: Agent = Agent(
    name="articles writer",
    instructions="You have to write complete articles on any topic which is given to you.",
    model=model
)
cl.user_session.set("agent", agent)
```

* Creates an agent with the role of writing full articles.

#### 👋 Welcome Message

```python
await cl.Message(content="👋 Welcome! Ask me to write an article on any topic.").send()
```

* Sends a welcome message to the user.

---

### 📩 4. **When User Sends a Message**

```python
@cl.on_message
async def main(message: cl.Message):
```

This function handles each user message.

#### 🧠 Show Thinking Message

```python
msg = cl.Message(content="🧠 Thinking...")
await msg.send()
```

* Displays a temporary message while the AI generates a response.

#### 🧠 Retrieve Session Data

```python
agent: Agent = cast(Agent, cl.user_session.get("agent"))
config: RunConfig = cast(RunConfig, cl.user_session.get("config"))
```

* Retrieves the agent and config from the session.

#### 📜 Update Chat History

```python
history = cl.user_session.get("chat_history") or []
history.append({"role": "user", "content": message.content})
```

* Adds the user's message to the chat history.

#### 🤖 Run the AI Agent

```python
result = Runner.run_sync(
    starting_agent=agent,
    input=history,
    run_config=config
)
```

* Passes the full chat history to the AI and gets the response.

#### 📤 Show Final Response

```python
msg.content = result.final_output
await msg.update()
```

* Updates the message with the AI-generated article.

#### 💾 Save Updated History

```python
cl.user_session.set("chat_history", result.to_input_list())
```

* Saves the updated chat history.

---

## ✅ Summary

* This chatbot uses **Gemini** in an **OpenAI-compatible format**.
* It is built with **Chainlit** for an interactive web-based chat interface.
* The AI is instructed to **write full articles** based on the user's input.
* **Chat history is saved** for context-aware replies.
