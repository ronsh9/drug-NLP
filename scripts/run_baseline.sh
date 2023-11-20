export OPENAI_API_KEY="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"
prompt_template="baseline1"

python drug_nlp/main.py \
    --seed 1 \
    --dataset_path scraper/eval_cases.yaml \
    --num_shots 10 \
    --llm_engine openai/gpt-3.5-turbo-0301	 \
    --llm_prompt_template ${prompt_template} \
    --llm_temperature 0.1 \
    --llm_num_completions 10 \
    --debug \
    --output_path results/${prompt_template}_16shot.csv 
