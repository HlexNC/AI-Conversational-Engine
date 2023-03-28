import json
from gtp_3_fine_tuning.openai import fine_tune


def prepare_data(file_path):
    data = []
    with open(file_path, "r") as f:
        for line in f:
            example = json.loads(line)
            data.append({
                "inputs": example["question"],
                "outputs": example["answer"]
            })
    return data


if __name__ == "__main__":
    file_path = "qa.jsonl"
    data = prepare_data(file_path)
    responses = fine_tune(data)
    print(responses)
