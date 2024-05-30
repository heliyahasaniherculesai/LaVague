from lavague.core import WorldModel, ActionEngine
from lavague.core.agents import WebAgent
from lavague.drivers.selenium import SeleniumDriver
from lavague.contexts.openai import AzureOpenaiContext


context = AzureOpenaiContext()
context.mm_llm = AzureOpenaiContext().mm_llm
selenium_driver = SeleniumDriver()
world_model = WorldModel.from_context(context)
action_engine = ActionEngine.from_context(context, selenium_driver)
agent = WebAgent(world_model, action_engine)
agent.get("https://huggingface.co/docs")
agent.run("Go on the quicktour of PEFT", display=True)
