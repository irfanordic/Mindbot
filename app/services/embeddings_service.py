from google import genai
from dotenv import load_dotenv
import os

load_dotenv()



class EmbeddingsService:
    def __init__(self):
        self.model = "gemini-embedding-001"
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        
    async def get_embeddings(self, text:str) -> list[float]:
        
        response =  await self.client.aio.models.embed_content(
            model=self.model,
            contents=text,
            config={"output_dimensionality": 768}
        )   
        
        return response.embeddings[0].values
        

