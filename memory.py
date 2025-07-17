from langchain.memory import ConversationBufferMemory

# Keeps the last N exchanges in RAM
CONV_MEMORY = ConversationBufferMemory(
    memory_key="history",
    input_key="input",
    output_key="response"
)
