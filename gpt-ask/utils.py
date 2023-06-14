import os
import argparse
import openai
import pandas as pd
from getpass import getpass
from dotenv import load_dotenv


def parse_args():
    parser = argparse.ArgumentParser(
        description="This tool can download papers and summarize them using chatGPT."
    )
    parser.add_argument(
        "-f",
        "--file",
        help="CSV/PDF/Folder that the program is going to process. "
        "CSV: papers will be downloaded from csv file and summarized (file should contain a column named DOI). "
        "PDF: paper will be summarized. "
        "Folder: papers inside the folder will be summarized. ",
    )
    parser.add_argument(
        "--set-api-key",
        action="store_true",
        default=False,
        # type=bool,
        help="Get API key as input and save it in a .env file",
    )
    parser.add_argument(
        "--question-file",
        type=str,
        help="Path to a text file where each line is a question you have from the papers",
    )
    parser.add_argument(
        "--dwn-dir",
        default="papers",
        type=str,
        help="Directory path in which to download the papers",
    )
    parser.add_argument(
        "--ans-dir",
        default="answers",
        type=str,
        help="Directory path in which to save the answers",
    )
    parser.add_argument(
        "--load-checkpoint",
        action="store_true",
        default=False,
        help="Loads previous answers from backup.json. Each time a new answer is generated the programs saves a backup of all answers. The backup is saved in ans-dir.",
    )
    parser.add_argument(
        "--scihub-mirror",
        default=None,
        type=str,
        help="Mirror for downloading papers from sci-hub. If not set, it is selected automatically",
    )
    args = parser.parse_args()
    return args


def save_api_key(env_path):
    api_key = getpass("Please enter your OpenAI API Key: ")
    with open(env_path, "w+") as f:
        f.write(f"OPENAI_API_KEY={api_key}")


def set_api_key(env_path):
    load_dotenv(env_path)
    openai_api_key = os.getenv("OPENAI_API_KEY")
    print(openai_api_key)
    openai.api_key = openai_api_key


def save_checkpoint(ans_dir, answers):
    res = answers.to_markdown(tablefmt="grid")
    with open(os.path.join(ans_dir, "answers.txt"), "w+") as f:
        f.write(res)
    answers.to_json(os.path.join(ans_dir, "backup.json"))


def load_checkpoint(ans_dir):
    return pd.read_json(os.path.join(ans_dir, "backup.json"))
