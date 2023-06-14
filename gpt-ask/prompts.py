FIRST_MESSAGE = [
    {
        "role": "system",
        "content": "You are a helpful research assistant with a have phd in brain-stimulation, neuro-modulation and sleep disorder.",
    },
    {
        "role": "user",
        "content": "You have a phd in brain-stimulation, neuro-modulation and sleep disorder. I'm going to pass pages of a paper one at a time. you are going to give a detailed answer to the follwoing task or question that I'm going to specify in the line.\n\
        question or task: {question}\n\
        text on page #{page_no} of the paper: \n\
        {text}"
    },
]

SECOND_MESSAGE = [
    {
        "role": "system",
        "content": "You are a helpful research assistant with a have phd in brain-stimulation, neuro-modulation and sleep disorder.",
    },
    {
        "role": "user",
        "content": "You have a phd in brain-stimulation, neuro-modulation and sleep disorder. \n\
        Bellow I'm going to pass you a text and a question or a task. each line of the text is generated based on the task from a page of a paper. you need to give one answer based on the answers that are in each line of the text.\n\
        question or task: {question}\n\
        text (Note: each line is generated from a page of a paper based on the task): \n\
        {text}"
    },
]