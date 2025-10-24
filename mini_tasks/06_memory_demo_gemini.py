from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.runnables import RunnableSequence
import os
from dotenv import load_dotenv
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", api_key=GOOGLE_API_KEY)

parser = StrOutputParser()

prompt = PromptTemplate.from_template(
    "Conversation history:\n{history}\nUser: {user}\nAssistant:"
)

memory = []

def chat(user_input):
    history_text = "\n".join(memory[-6:])
    chain = RunnableSequence(prompt | llm | parser)
    result = chain.invoke({"history": history_text, "user": user_input})
    # append to memory
    memory.append(f"User: {user_input}")
    memory.append(f"Assistant: {result}")
    return result

# example interaction:
print(chat("Hello, my name is Sanjarbek."))
print(chat("Can you remember my name?"))
