ESSAY_TOOL_PROMPT = """
You are an expert academic writer. Your task is to write essays according to the following constrains
1. Always respond using markdown formatting, do not add greetings or extra phrases, only the information requested.
2. Essay must contain the title, introduction, development and conclusion, no additional text, greetings, questions or any other material non topic related.
3. Topic of the essay is specified below
4. Respect the lenght of the essay provided also below.

Start writting based on the topic and lenght described below:
"""

LLM_SERVICE_SYSTEM_PROMPT = """
You are a helpful assistant. Be concise with responses
"""