# gpt-ask

A Paper Downloader and Question Answering Tool.  
The program is a tool that allows you to download papers and generate answers using chatGPT. It provides various options for processing papers, such as downloading papers from CSV a file, extracting answers from papers, and managing the generated answers. Additionally, it offers features like setting the OpenAI API key, specifying question files, selecting download and answer directories, loading previous answers, and choosing a sci-hub mirror for paper downloads. With this program, you can efficiently retrieve papers and obtain insightful answers using chatGPT's capabilities.

## Usage

```
usage: main.py [-h] [-f FILE] [--set-api-key] [--question-file QUESTION_FILE] [--dwn-dir DWN_DIR]
               [--ans-dir ANS_DIR] [--load-checkpoint] [--scihub-mirror SCIHUB_MIRROR]
```

### Options

- `-h`, `--help`: Show the help message and exit.
- `-f FILE`, `--file FILE`: Specifies the CSV/PDF/Folder that the program is going to process. 
   - CSV: Papers will be downloaded from a CSV file and summarized. The file should contain a column named "DOI".
   - PDF: A single paper will be summarized.
   - Folder: Papers inside the folder will be summarized.
- `--set-api-key`: Prompts the user to input an API key and saves it in a `.env` file.
- `--question-file QUESTION_FILE`: Path to a text file where each line represents a question related to the papers.
- `--dwn-dir DWN_DIR`: Directory path to specify where to download the papers.
- `--ans-dir ANS_DIR`: Directory path to specify where to save the answers.
- `--load-checkpoint`: Loads previous answers from `backup.json`. Each time a new answer is generated, the program saves a backup of all answers in the answer directory.
- `--scihub-mirror SCIHUB_MIRROR`: Specifies the mirror to download papers from sci-hub. If not set, it is automatically selected.

## Dependancies
For installing the dependencies, run the following command. 
```
pip install -r requirements.txt
```
