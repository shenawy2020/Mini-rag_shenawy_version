from enum import Enum
class LLMEnum(Enum):
    OPENAI="OPENAI"
    COPHERE="COPHERE"   
    AZURE_OPENAI="AZURE_OPENAI"
    ANTHROPIC="ANTHROPIC"
class OOpenAIEnum(Enum):
    SYSTEM="SYSTEM"
    USER="USER"
    ASSISTANT="ASSISTANT"   