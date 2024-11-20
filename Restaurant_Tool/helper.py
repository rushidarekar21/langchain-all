from langchain_community.llms import Ollama
from langchain.chains import SimpleSequentialChain
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# Instantiate the model
llm = Ollama(model='llama3.1')

def generate_restaurant_name_and_items(cuisine):
    # Define the prompt for generating a restaurant name
    prompt_template_name = PromptTemplate(
        input_variables=['cuisine'],
        template='I want to open a {cuisine} restaurant. Please provide a suitable & eye-catching name. Just provide one name and nothing else in output.'
    )

    # Define the prompt for generating menu items
    prompt_template_items = PromptTemplate(
        input_variables=['restaurant_name'],
        template='I am opening a restaurant named {restaurant_name}. Please list me 10 dishes at my restaurant. In the output, I expect just a list of 10 dishes with numbering and nothing else.'
    )

    # Define the chain for generating the restaurant name
    name_chain = LLMChain(
        llm=llm,
        prompt=prompt_template_name,
        output_key="restaurant_name"
    )

    # Define the chain for generating menu items
    item_chain = LLMChain(
        llm=llm,
        prompt=prompt_template_items,
        input_key="restaurant_name",
        output_key="menu_items"
    )

    # Define the sequential chain linking name and item generation
    chain = SimpleSequentialChain(
        chains=[name_chain, item_chain]
    )

    # Run the chain with the given cuisine
    response = chain.invoke({'cuisine': cuisine})

    return response

if __name__ == '__main__':
    print(generate_restaurant_name_and_items('Italian'))
