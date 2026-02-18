import os
import pandas as pd
from langchain_openai import ChatOpenAI
from langchain_experimental.agents import create_pandas_dataframe_agent


def create_agent(dataframe: pd.DataFrame, tools, system_prompt: str):
    llm = ChatOpenAI(
        api_key=os.getenv("API_KEY"),
        base_url="https://api.deepseek.com/beta",
        model="deepseek-chat",
        temperature=0.3,
    )

    return create_pandas_dataframe_agent(
        llm,
        dataframe,
        extra_tools=tools,
        verbose=True,
        allow_dangerous_code=True,
        prefix=system_prompt,
        agent_executor_kwargs={"handle_parsing_errors": True}
    )

