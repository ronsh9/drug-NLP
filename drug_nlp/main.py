import random
import yaml
import os
from utils import logger, score_against_known_drugs
from flags import FLAGS, parse_flags
from prompts import prompt_templates
import openai

from ipdb import set_trace as st

if __name__ == "__main__":
    parse_flags()
    logger.info("FLAGS: {}".format(FLAGS))
    random.seed(FLAGS.seed)
    prompt_template = prompt_templates[FLAGS.llm_prompt_template]

    openai.api_key = os.environ.get("OPENAI_API_KEY")

    # Load yaml data
    with open(FLAGS.dataset_path) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)

    data = data['01']
    print(f"Investigating {data['disease_name']}")

    prompt = prompt_template["instruction"]

    test_example_dict = {"disease_text": data["disease_description"]}
    prompt += prompt_template["prediction"].format_map(test_example_dict)
    
    response = openai.Completion.create(
	    engine = 'text-davinci-003', ## 
	    prompt = prompt, 
	    temperature = 1.0, 
	    max_tokens = 200, 
	    n=1, 
	    stop = None, 
	    timeout=20, )
    
    initial_gues = response.choices[0].text

    score = score_against_known_drugs(initial_gues, data["drug_list"])

    print(f"Initial guess: {initial_gues}")
    print(f"Score: {score}")

