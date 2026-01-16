from ..LLMInterfacy import  LLMInterfacy
from ..LLMENum import OOpenAIEnum

from openai import OpenAI
import logging

class OpenAIPRoviders(LLMInterfacy):
    def __init__(self,api_key:str,api_url:str=None,
                 default_input_max_characters:int=1000
                 ,default_output_max_tokens:int=1000
                 ,default_temperature:float=0.1):
        
        self.api_key=api_key
        self.api_url=api_url
        self.default_input_max_characters=default_input_max_characters
        self.default_output_max_tokens=default_output_max_tokens
        self.default_temperature=default_temperature
        self.set_generatuion_model_id=None
        self.embedding_model_id=None
        self.embedding_size=None
        
        self.client=OpenAI(
            api_key=self.api_key,
            base_url=self.api_url
        )
        self.logger=logging.getLogger(__name__)
    def set_generatuion_model(self,mode_id:str):
        self.set_generatuion_model_id=mode_id
    def set_embedding_model(self,model_id:str,embedding_size:int):
        self.embedding_model_id=model_id
        self.embedding_size=embedding_size

    def process_text(self,text:str):
        if len(text)>self.default_input_max_characters:
            return text[:self.default_input_max_characters].strip
        return text.strip()
    

    def generate_text(self,prompt:str,chat_history:list ={},max_output_tokens:int=None,temperature:float=None):
          if not self.client:
            self.logger.error("OpenAI client is not initialized.")
            return None
          if not self.embedding_model_id:
            self.logger.error("Embedding model is not set.")
            return None
          max_tokens=max_output_tokens if max_output_tokens is not None else self.default_output_max_tokens
          max_temoperature=temperature if temperature is not None else self.default_temperature
          chat_history.append(self.constuct_prompt(prompt=prompt,role=OOpenAIEnum.USER.value))  
          
          response=self.client.chat.completions.create(
              model=self.set_generatuion_model_id,
              messages=chat_history,
              max_tokens=max_tokens,
              temperature=max_temoperature
          )
          if not response or not response.choices or len(response.choices)==0:
            self.logger.error("No completion returned from OpenAI.")
            return None
          return response.choices[0].message.content
    

    def emded_text(self,text:str,doccument_type:str=None):
        if not self.client:
            self.logger.error("OpenAI client is not initialized.")
            return None
        if not self.embedding_model_id:
            self.logger.error("Embedding model is not set.")
            return None
        response=self.client.embeddings.create(
            input=text,moedel=self.embedding_model_id

        )
        if not response or not response.data or len(response.data)==0:
            self.logger.error("No embedding data returned from OpenAI.")
            return None
        embedding_vector=response.data[0].embedding
        return embedding_vector 
    
    
    
    def constuct_prompt(self,prompt:str,role:str="user"):
            return {
                "role":role,
                "content":self.process_text(prompt)
            }   
        

    

        
        