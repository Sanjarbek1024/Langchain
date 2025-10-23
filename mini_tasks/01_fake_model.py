from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Query method
prompt = PromptTemplate.from_template("Translate this sentence to Uzbek: {sentence}")

# A fake model function
def fake_model(prompt_text):
    return f"\nFake model's answer: \n\nOriginal text: '{prompt_text}' \n\nTranslated text: 'Bu so'zning o'zbek tiliga tarjimasi.'\n"

# Result parser
parser = StrOutputParser()

# Chain – Prompt + Model + Parser
def simple_chain(sentence):
    prompt_text = prompt.format(sentence=sentence)
    result = fake_model(prompt_text)
    return parser.invoke(result)

# Example usage
print(simple_chain("Good morning, how are you?"))
