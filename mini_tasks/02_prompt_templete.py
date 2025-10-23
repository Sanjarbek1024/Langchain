from langchain_core.prompts import PromptTemplate

# Making a prompt template
prompt = PromptTemplate.from_template("Translate this to Uzbek: {text}")

# Filling the template
filled = prompt.format(text="Hello world")

print(filled)
