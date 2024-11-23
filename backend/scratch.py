import os

from dotenv import load_dotenv

from autogen import ConversableAgent

load_dotenv()

config_list = [
    {
        "model": "meta-llama/Meta-Llama-3.1-8B-Instruct",
        "api_key": os.environ.get("NEBIUS_API_KEY"),
        'base_url':"https://api.studio.nebius.ai/v1/"
    },
    {
        "model": "meta-llama/Meta-Llama-3.1-70B-Instruct",
        "api_key": os.environ.get("NEBIUS_API_KEY"),
        'base_url':"https://api.studio.nebius.ai/v1/"
    }
]
agent = ConversableAgent(
    "chatbot",
    llm_config={"config_list": config_list},
    code_execution_config=False,  # Turn off code execution, by default it is off.
    function_map=None,  # No registered functions, by default it is None.
    human_input_mode="NEVER",  # Never ask for human input.
)

reply = agent.generate_reply(messages=[{"content": "Tell me a joke.", "role": "user"}])
print(reply)