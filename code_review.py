import streamlit as st
import os
import google.generativeai as genai

# Set up the model
generation_config = {
    "temperature": 0,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    }
]

# Set Google API key
os.environ['GOOGLE_API_KEY'] = "AIzaSyC6gNsbu9viro7Vbcl5p7mpXkVlifkiMk0"
genai.configure(api_key=os.environ['GOOGLE_API_KEY'])

model = genai.GenerativeModel(model_name="gemini-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

# Define Streamlit UI
st.title("Code Review ChatBot")

# Prompt the user to paste their code
user_input = st.text_area("Paste your code here:")

if st.button("Submit"):
    # Check if the user input is empty or contains only whitespace
    if user_input.strip() == "":
        st.error("Input is out of context. Please provide valid code.")
    else:
        prompt_parts = [
            """Please review the code below and identify any syntax or logical errors, suggest
        ways to refactor and improve code quality, enhance performance, address security
        concerns, and align with best practices. Provide specific examples for each area
        and limit your recommendations to three per category.

        Use the following response format, keeping the section headings as-is, and provide
        your feedback. Use bullet points for each response. The provided examples are for
        illustration purposes only and should not be repeated.

        **Syntax and logical errors (example)**:
        - Incorrect indentation on line 12
        - Missing closing parenthesis on line 23

        **Code refactoring and quality (example)**:
        - Replace multiple if-else statements with a switch case for readability
        - Extract repetitive code into separate functions

        **Performance optimization (example)**:
        - Use a more efficient sorting algorithm to reduce time complexity
        - Cache results of expensive operations for reuse

        **Security vulnerabilities (example)**:
        - Sanitize user input to prevent SQL injection attacks
        - Use prepared statements for database queries

        **Best practices (example)**:
        - Add meaningful comments and documentation to explain the code
        - Follow consistent naming conventions for variables and functions

        if user enters text other than code then, then provide the response as Input is out of context. Please provide valid code.  

        Code:
        """ + user_input + """

        Your review:"""]

        response = model.generate_content(prompt_parts)
        st.markdown(response.text)
