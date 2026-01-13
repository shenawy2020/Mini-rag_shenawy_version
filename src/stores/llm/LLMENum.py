from enum import Enum
class LLMEnum(Enum):
    OPENAI="OPENAI"
    COPHERE="COPHERE"   
    AZURE_OPENAI="AZURE_OPENAI"
    ANTHROPIC="ANTHROPIC"
class OOpenAIEnum(Enum):
    SYSTEM="system"
    USER="user"
    ASSISTANT="assistant"   
class CophereEnum(Enum):
    SYSTEM="SYSTEM"
    USER="USER"
    ASSISTANT="CHATBOT"
    document="search_document"
    Query="search_query"

class documentTypeEnum(Enum):
    document="document"
    Query="query"
    