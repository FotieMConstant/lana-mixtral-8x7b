import json
import subprocess
from pathlib import Path


if __name__ == "__main__":
    dataset = "lanadoc.subsample.jsonl"
    dataset_path = Path(__file__).parent.parent / "data" / dataset
    example = json.loads(dataset_path.read_text().strip().split("\n")[0])

    prompt = "[INST] Using the code below, generate a valid JSON file API specification adhering to the OpenAPI 3.0.0 standard."
    prompt += f"\n{example['context']}"
    prompt += f"\n{example['question']}"
    prompt += " [/INST]"

    p = subprocess.Popen(
        ["modal", "run", "src.inference", "--prompt", prompt],
        stdout=subprocess.PIPE,
    )
    output = ""

    for line in iter(p.stdout.readline, b""):
        output += line.decode()
        print(line.decode())

    print("Asserting that the output contains the expected format")
    assert "[SPEC]" in output and "[/SPEC]" in output
