
from .LLMENum import  LLMEnum
from .providers import OpenAIPRoviders
from .providers import CoherePRoviders



class LLMProviderFactory:
    def __init__(self,conifig:dict):
        self.config=conifig
    def create_llm_provider(self,provider:str):
        if provider==LLMEnum.OPENAI.value:             
            return OpenAIPRoviders(api_key=self.config.OPENAI_API_KEY,
                                   api_url=self.config.OPENAI_API_URL,
                                   default_input_max_characters=self.config.INPUT_DAFAULT_MAX_CHARACTERS,
                                   default_output_max_tokens=self.config.GENERATION_DAFAULT_MAX_TOKENS
                                   ,default_temperature=self.config.GENERATION_DAFAULT_TEMPERATURE
                                   )
        
        
        elif provider==LLMEnum.COPHERE.value:
           
            return CoherePRoviders(api_key=self.config.COHERE_API_KEY,
                                   default_input_max_characters=self.config.INPUT_DAFAULT_MAX_CHARACTERS,
                                   default_output_max_tokens=self.config.GENERATION_DAFAULT_MAX_TOKENS
                                   ,default_temperature=self.config.GENERATION_DAFAULT_TEMPERATURE
                                   
                                   )
        else:
            raise ValueError(f"Unsupported LLM type: {provider}")

        
