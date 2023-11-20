import argparse

FLAGS = argparse.Namespace() 


def parse_flags() -> None:
    parser = argparse.ArgumentParser()

    parser.add_argument("--seed", required=True, type=int)
    parser.add_argument("--dataset_path", required=True, type=str)

    parser.add_argument("--num_shots", type=int)

    parser.add_argument("--llm_engine", required=True, type=str)
    parser.add_argument("--llm_prompt_template", required=True, type=str)
    parser.add_argument("--llm_cache_dir", type=str, default="llm_cache")
    parser.add_argument("--llm_temperature", required=True, type=float, default=0.0)
    parser.add_argument("--llm_num_completions", required=True, type=int, default=1)
    parser.add_argument("--llm_max_tokens", type=int, default=256)
    parser.add_argument("--llm_freq_penalty", type=float, default=0.0)

    parser.add_argument("--debug", action="store_true", default=False)

    parser.add_argument("--output_path", required=True, type=str)
    args = parser.parse_args()
    FLAGS.__dict__.update(args.__dict__)