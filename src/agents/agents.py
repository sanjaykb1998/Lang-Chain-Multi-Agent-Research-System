from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from src.tools.tools import web_search, scrape_url
from dotenv import load_dotenv

load_dotenv()

# Model Initialization
#llm = ChatGroq(model = "qwen/qwen3.8-27b",temperature=0)
llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0,
)

# 1st Agent : Search Agent
def build_search_agent():
    return create_agent(
        model=llm,
        tools=[web_search],
        system_prompt="""
You are a web research assistant.

Rules:
1. Call web_search exactly once.
2. The web_search tool requires one argument named 'query'.
3. After receiving the search results, summarize them.
4. Do not call web_search again.
5. Do not perform follow-up searches.
"""
    )

# 2nd Agent : Reader Agent
def build_reader_agent():
    return create_agent(
        model= llm,
        tools=[scrape_url],
        system_prompt=(
            "You are a web content reader. "
            "Use the registered scrape_url tool to extract content from web pages. "
            "Its required argument is url. Never invent tool names."
        ),
    )


#writer chain 

writer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert research writer. Write clear, structured and insightful reports."),
    ("human", """Write a detailed research report on the topic below.

Topic: {topic}

Research Gathered:
{research}

Structure the report as:
- Introduction
- Key Findings (minimum 3 well-explained points)
- Conclusion
- Sources (list all URLs found in the research)

Be detailed, factual and professional."""),
])

writer_chain = writer_prompt | llm | StrOutputParser()




#critic_chain 

critic_prompt = ChatPromptTemplate.from_messages([
     ("system", "You are a sharp and constructive research critic. Be honest and specific."),
    ("human", """Review the research report below and evaluate it strictly.

Report:
{report}

Respond in this exact format:

Score: X/10

Strengths:
- ...
- ...

Areas to Improve:
- ...
- ...

One line verdict:
..."""),
])

critic_chain = critic_prompt | llm | StrOutputParser()