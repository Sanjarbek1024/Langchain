import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSequence
from langchain_google_genai import ChatGoogleGenerativeAI


prompt = PromptTemplate.from_template("Answer to this question:\n\n{text}")

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", api_key=GOOGLE_API_KEY)

chain = RunnableSequence(prompt | llm | StrOutputParser())

result = chain.invoke({"text": "Who I am?"})

print(result)


