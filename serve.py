from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from langserve import add_routes
from dotenv import load_dotenv
import os
load_dotenv()

model = ChatGroq(model="Gemma2-9b-It")

# Create prompt template
system_template = "Translate the following into {language}: "

prompt_template = ChatPromptTemplate.from_messages([
    ("system", system_template),
    ("human", "{text}"),
])

parser = StrOutputParser()

## Create Chain

chain = prompt_template | model | parser

## App Definition

app = FastAPI(
    title="LangChain Server",
    version="1.0",
    description="A simple API server using LangChain's Runnable interfaces.",
)

## adding chain route
add_routes(
    app, 
    chain, 
    path="/chain"
)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
