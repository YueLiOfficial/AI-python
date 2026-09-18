def load_markdown():
    from langchain_community.document_loaders import UnstructuredMarkdownLoader
    from pathlib import Path

    loader = UnstructuredMarkdownLoader(
        file_path=Path(__file__).parent / "assets" / "sample.md",
        mode="single"
    )

    res = loader.load()

    print(res[0].page_content)

def load_docx():
    from langchain_community.document_loaders import UnstructuredWordDocumentLoader
    from pathlib import Path

    loader = UnstructuredWordDocumentLoader(
        file_path=Path(__file__).parent / "assets" / "sample.docx",
        mode="single"
    )

    res = loader.load()

    print(res[0].page_content)

if __name__ == "__main__":
    # load_markdown()
    load_docx()
