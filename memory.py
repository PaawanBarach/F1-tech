from langchain.memory import ConversationBufferMemory

CONV_MEMORY = ConversationBufferMemory(
    memory_key="history",
    input_key="input",
    output_key="response"
)
