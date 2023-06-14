import os
from pypdf import PdfReader
from alive_progress import alive_it


def process_folder(path):
    files = []
    for f in alive_it(sorted(os.listdir(path))):
        content = process_file(path, f)
        if content:
            files.append(content)
    return files


def process_file(folder, file):
    current = os.path.join(folder, file)
    if not (os.path.isfile(current) and ".pdf" in file):
        return None
    content = {"name": file, "text": read_pdf(current)}
    return content


def read_pdf(path):
    reader = PdfReader(path)
    paper_pages = []
    for page in reader.pages:
        paper_pages.append(page.extract_text().lower())
    return paper_pages


if __name__ == "__main__":
    files = process_folder("papers")
    for f in files:
        print(f["name"], len(f["text"]))
