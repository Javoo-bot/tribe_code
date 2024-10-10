from langchain_anthropic import ChatAnthropic
from langchain_cohere import ChatCohere
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_together import ChatTogether

# Define a dictionary to store all models
all_models: dict[str, type[BaseChatModel]] = {
    "ChatOpenAI": ChatOpenAI,
    "ChatAnthropic": ChatAnthropic,
    "ChatCohere": ChatCohere,
    "ChatGoogleGenerativeAI": ChatGoogleGenerativeAI,
    "ChatTogetherAI": ChatTogether
}
