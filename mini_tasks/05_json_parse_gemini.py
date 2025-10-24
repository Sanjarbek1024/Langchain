from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSequence
from langchain_google_genai import ChatGoogleGenerativeAI
import os, json
from dotenv import load_dotenv
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

prompt = PromptTemplate.from_template(
    "You are a JSON-only responder.\n"
    "Input: {text}\n\n"
    "Return JSON with keys: translation (string), length (int)."
)

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", api_key=GOOGLE_API_KEY)

chain = RunnableSequence(prompt | llm | StrOutputParser())

result = chain.invoke({"text": "Translate 'Hello, how are you?' to French."})

print("Raw llm output:\n", result)

# try to parse JSON from output
try:
    parsed_result = json.loads(result)
    print("\nParsed JSON output:\n", parsed_result)
except json.JSONDecodeError as e:
    print("\nFailed to parse JSON:", e)

