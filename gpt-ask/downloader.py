from PyPaperBot.Crossref import getPapersInfoFromDOIs
from PyPaperBot.Downloader import downloadPapers
import pandas as pd


def download_paper(doi_list, download_dir, SciHub_URL):
    paper_info = []
    for doi in doi_list:
        paper_info.append(getPapersInfoFromDOIs(doi, restrict=None))
    downloadPapers(paper_info, download_dir, num_limit=None, SciHub_URL=SciHub_URL)


def extract_DOIs(file_name):
    df = pd.read_csv(file_name)
    return df.DOI[df.DOI.notna()].tolist()


if __name__ == "__main__":
    dois = extract_DOIs("EEG Dynamics.csv")
    download_paper(dois, "papers/", SciHub_URL=None)
