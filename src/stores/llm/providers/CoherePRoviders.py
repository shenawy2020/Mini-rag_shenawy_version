from ..LLMInterfacy import  LLMInterfacy
import logging
import cohere

from ..LLMENum import CophereEnum
from ..LLMENum import documentTypeEnum

class CoherePRoviders(LLMInterfacy):
    def __init__(self,api_key:str,
                 default_input_max_characters:int=1000
                 ,default_output_max_tokens:int=1000
                 ,default_temperature:float=0.1):
        self.api_key=api_key
        
        self.default_input_max_characters=default_input_max_characters
        self.default_output_max_tokens=default_output_max_tokens
        self.default_temperature=default_temperature
        self.set_generatuion_model_id=None
        self.embedding_model_id=None
        self.embedding_size=None

        self.client=cohere.Client(api_key=self.api_key)
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
            self.logger.error("Cohere client is not initialized.")
            return None
          if not self.embedding_model_id:
            self.logger.error("Embedding model is not set.")
            return None
          max_tokens=max_output_tokens if max_output_tokens is not None else self.default_output_max_tokens
          max_temoperature=temperature if temperature is not None else self.default_temperature
          chat_history.append(self.constuct_prompt(prompt=prompt,role=CophereEnum.USER.value))  
          
          response=self.client.chat(
              model=self.set_generatuion_model_id,
              chat_history=chat_history,
              max_tokens=max_tokens,
              temperature=max_temoperature
              ,message=self.process_text(prompt)
          )
          if not response or not response.text or len(response.text)==0:
            self.logger.error("No completion returned from Cohere.")
            return None
          return response.text

    def constuct_prompt(self, prompt, role):
         return {"role": role, "text": self.process_text(prompt)}
    
    def generate_embedding(self,text:str,documnet_type:str=None):
        if not self.client:
            self.logger.error("Cohere client is not initialized.")
            return None
        if not self.embedding_model_id:
            self.logger.error("Embedding model is not set.")
            return None
        input_type=CophereEnum.document.value
        if documnet_type==documentTypeEnum.Query.value:
            input_type=CophereEnum.Query.value
        


        response=self.client.embed(
            model=self.embedding_model_id,
            texts=[self.process_text(text)]
            ,input_type=input_type
            ,embedding_type="[float]"
        )
        if not response or not response.embeddings   or not response.embeddings.float or len(response.embeddings.float)==0:
            self.logger.error("No embeddings returned from Cohere.")
            return None
        return response.embeddings.float[0];
    def emded_text(self,text:str,doccument_type:str=None):
        pass