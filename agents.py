from typing import List, Dict, Any

# Dummy class for RunConfig since it's not provided directly by chainlit now
class RunConfig:
    def __init__(self, model: Any, model_provider: Any, tracing_disabled: bool = True):
        self.model = model
        self.model_provider = model_provider
        self.tracing_disabled = tracing_disabled

class Agent:
    def __init__(self, name: str, instructions: str, model: Any):
        self.name = name
        self.instructions = instructions
        self.model = model

    async def a_run(self, input: List[Dict], config: RunConfig) -> str:
        messages = [{"role": "system", "content": self.instructions}] + input
        response = await self.model.acomplete(messages=messages)
        return response["choices"][0]["message"]["content"]

class Runner:
    @staticmethod
    def run_sync(starting_agent: "Agent", input: List[Dict], run_config: RunConfig):
        import asyncio

        class Result:
            def __init__(self, output: str):
                self.final_output = output
                self.history = input + [{"role": "assistant", "content": output}]

            def to_input_list(self):
                return self.history

        async def run():
            output = await starting_agent.a_run(input, run_config)
            return Result(output)

        return asyncio.run(run())

class AsyncOpenAI:
    def __init__(self, api_key: str, base_url: str):
        import openai
        self.client = openai.AsyncOpenAI(api_key=api_key, base_url=base_url)

    async def chat_completions(self, model: str, messages: List[Dict]):
        return await self.client.chat.completions.create(
            model=model,
            messages=messages
        )

class OpenAIChatCompletionsModel:
    def __init__(self, model: str, openai_client: AsyncOpenAI):
        self.model = model
        self.client = openai_client

    async def acomplete(self, messages: List[Dict]):
        return await self.client.chat_completions(
            model=self.model,
            messages=messages
        )
