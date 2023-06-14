import os
import sys
import argparse
import pandas as pd
from files import process_folder, process_file
from chat import ask_model_page_by_page, ask_model_final_results
from downloader import download_paper, extract_DOIs
from prompts import FIRST_MESSAGE, SECOND_MESSAGE
from getpass import getpass
from dotenv import load_dotenv
import openai


ENV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")


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
        "--scihub-mirror",
        default=None,
        type=str,
        help="Mirror for downloading papers from sci-hub. If not set, it is selected automatically",
    )
    args = parser.parse_args()
    return args


def save_api_key():
    api_key = getpass("please enter your OpenAI API Key: ")
    with open(ENV_PATH, "w+") as f:
        f.write(f"OPENAI_API_KEY={api_key}")


def set_api_key():
    load_dotenv()
    openai_api_key = os.getenv(ENV_PATH)
    openai.api_key = openai_api_key


if __name__ == "__main__":
    # parse input arguments
    args = parse_args()

    # set API key
    if args.set_api_key:
        save_api_key()
        sys.exit()

    if not os.path.exists(ENV_PATH):
        print("Please set the API key. using: python main.py --set-api-key")
        sys.exit()

    # check input file
    if not args.file:
        print("Please specify an input file using the -f or --file input argument")
        sys.exit()

    if not os.path.exists(args.file):
        print("The input file/folder doesn't exist.")
        sys.exit()

    files = []
    # download papers if the input file is a csv
    if os.path.isfile(args.file) and ".csv" in args.file:
        if not os.path.exists(args.dwn_dir):
            os.makedirs(args.dwn_dir)

        dois = extract_DOIs(args.file)
        download_paper(dois, args.dwn_dir, SciHub_URL=args.scihub_mirror)
        files = process_folder(args.dwn_dir)

    # read files in the input folder
    if os.path.isdir(args.file):
        files = process_folder(args.file)

    # read input pdf file
    if os.path.isfile(args.file) and ".pdf" in args.file:
        files = [process_file("", args.file)]

    # create summary dir if not exists
    if not os.path.exists(args.ans_dir):
        os.makedirs(args.ans_dir)

    # read question file
    questions = []
    if args.question_file:
        if not os.path.exists(args.question_file):
            print("question file doesn't exist.")
            sys.exit()
        with open(args.question_file, "r") as f:
            lines = f.read()
            questions = lines.split("\n")
            if "" in questions:
                questions.remove("")
    else:
        questions = ["summary the following text."]

    set_api_key()

    answers = pd.DataFrame(columns=["paper name", *questions])
    answers["paper name"] = [paper["name"] for paper in files]  # type: ignore

    for i, question in enumerate(questions):
        for j, paper in enumerate(files):
            print(f'question: {question}\npaper:{paper["name"]}')  # type: ignore
            response = ask_model_page_by_page(
                pages=paper["text"],  # type: ignore
                question=question,
                messages=FIRST_MESSAGE,
            )
            print(f"feeding answers to the model to get the final answer")
            response = ask_model_final_results(
                answers=response, question=question, messages=SECOND_MESSAGE
            )
            answers.iloc[j, i + 1] = response

    res = answers.to_markdown(tablefmt="grid")
    with open(os.path.join(args.ans_dir, "answers.txt"), "w+") as f:
        f.write(res)
