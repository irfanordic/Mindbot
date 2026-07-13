from langchain_text_splitters import RecursiveCharacterTextSplitter



class TextProcessor:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            model_name="text-embedding-3-small",
            chunk_size=512,
            chunk_overlap=50
        )
        
    def split_text(self, text: str):
        return self.text_splitter.split_text(text)    