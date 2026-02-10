from langchain_groq import ChatGroq

llm = ChatGroq(model="llama-3.3-70b-versatile")

tool_call_llm = ChatGroq(model='qwen/qwen3-32b"')
