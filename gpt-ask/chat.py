import os
import openai
import copy
from alive_progress import alive_it
from dotenv import load_dotenv
from tiktoken import encoding_for_model
import itertools
from openai.error import APIConnectionError, RateLimitError


def split_list(lst, val):
    return [
        list(group) for k, group in itertools.groupby(lst, lambda x: x == val) if not k
    ]


def set_api_key():
    load_dotenv()
    openai_api_key = os.getenv("OPENAI_API_KEY")
    openai.api_key = openai_api_key


def ask_model_page_by_page(pages, question, messages, model="gpt-3.5-turbo"):
    responses = ""
    for i, page in enumerate(alive_it(pages)):
        message = format_message(messages, text=page, question=question, page_no=i + 1)
        response = get_response_from_model(messages=message, model=model)
        response = format_response(response, page_no=i + 1)
        responses += response
    return responses


def ask_model_final_results(answers, question, messages, model="gpt-3.5-turbo"):
    splited_answers = split_response_by_len(answers)
    responses = ""
    start_page = 1
    for i, page in enumerate(alive_it(splited_answers)):
        message = format_message(messages, text=page, question=question)
        response = get_response_from_model(messages=message, model=model)
        end_page = start_page + len(page.split("\n")) - 2
        response = format_final_response(response, start=start_page, end=end_page)
        responses += response
        start_page = end_page + 1
    return responses


def split_response_by_len(answers, model="gpt-3.5-turbo"):
    answers = answers.split("\n")
    for i in reversed(range(len(answers))):
        if not answers[i]:
            del answers[i]
    for i in range(len(answers)):
        answers[i] += "\n"
    enc = encoding_for_model(model)
    encoded = [enc.encode(answer) for answer in answers]
    encoded_len = [len(x) for x in encoded]
    token_lim = 4096 - 150
    sum = 0
    pages = [""]
    for i, elem_len in enumerate(encoded_len):
        if sum + elem_len < token_lim:
            sum += elem_len
            pages[-1] += answers[i]
        else:
            sum = elem_len
            pages.append(answers[i])
    return pages


def format_message(messages, **kwargs):
    message = copy.deepcopy(messages)
    message[1]["content"] = message[1]["content"].format(**kwargs)[:4096]
    return message


def format_final_response(response, start, end):
    return f"answer based on pages {start} to {end}: {response}"


def format_response(response, page_no=0):
    return f"page {page_no} response: {response}\n"


def get_response_from_model(messages, model="gpt-3.5-turbo"):
    flag = True
    while flag:
        try: 
            response = openai.ChatCompletion.create(model=model, messages=messages)
            flag = False
        except (APIConnectionError, RateLimitError) as e: 
            print(e)
    return response["choices"][0]["message"]["content"]  # type: ignore


if __name__ == "__main__":
    set_api_key()
    TEST_MESSAGES = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "This is just a test"},
    ]
    response = get_response_from_model(messages=TEST_MESSAGES)
    print(response)
