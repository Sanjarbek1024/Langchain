from langchain_core.prompts import PromptTemplate

prompt_template = PromptTemplate.from_template("Tell me a joke about {topic}")

# Example usage
print(prompt_template.format(topic="cats"))