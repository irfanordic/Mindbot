from openai import AsyncOpenAI
from dotenv import load_dotenv
import os

load_dotenv()



class EmbeddingsService:
    def __init__(self):
        self.model = "text-embedding-3-small"
        self.client = AsyncOpenAI(api_key=os.getenv("OPEN_AI_API_KEY"))
        
    async def get_embeddings(self, text:str) -> list[float]:
        
        response =  await self.client.embeddings.create(
            model=self.model,
            input=text
        )   
        
        return response.data[0].embedding
        

