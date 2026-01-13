from abc import  ABC, abstractmethod


class LLMInterfacy(ABC):

    @abstractmethod
    def set_generatuion_model(self,mode_id:str):
        pass

    @abstractmethod
    def set_embedding_model(self,model_id:str,embedding_size:int):
       pass

    @abstractmethod
    def generate_text(self,prompt:str,chat_history:list ,max_output_tokens:int,temperature:float=None):
        pass
    @abstractmethod
    def emded_text(self,text:str,doccument_type:str=None):
        pass
    @abstractmethod
    def constuct_prompt(self,prompt:str,role:str):
        pass
