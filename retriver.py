%pip install -qU langchain langchain-openai langchain-chroma beautifulsoup4

from langchain_community.document_loaders import WebBaseLoader

loader = WebBaseLoader("https://docs.smith.langchain.com/overview")
data = loader.load()