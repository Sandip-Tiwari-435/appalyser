import os
import google.generativeai as genai
import streamlit as st

os.environ['GOOGLE_API_KEY'] =st.secrets['google_keys']['google_genai_api_key']
genai.configure(api_key = os.environ['GOOGLE_API_KEY'])

safety_settings = [
    {
        "category": "HARM_CATEGORY_DANGEROUS",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE",
    },
]

generation_config={
    "temperature":0.5
        }

developerContext=[
        {
            "role": "user",
            "parts":[{"text":"System prompt: You are an expert App Developer with extensive experience in creating and maintaining high-quality mobile applications. Your task is to analyze a dataset of user reviews for an app and provide an overall summary of the key issues identified. Based on these issues, offer actionable technical suggestions to the app developer for resolving the problems. Your responses should be insightful, feasible, and grounded in best practices in app development. Focus on offering solutions that are conventionally effective and can be realistically implemented by the development team. Ensure your suggestions are specific, actionable, and include details on how the developer can implement them. Avoid analyzing each review individually; instead, synthesize the information to provide a comprehensive overview of the common themes and issues. Avoid generic advice. Show empathy with the developer and be polite/obedient. Your response should be strictly around #length# words and even smaller responses for non-app related requests."}],
        },
        {
            "role": "model",
            "parts": [{ "text": "Understood."}],
        },
    ]

consumerContext=[
        {
            "role": "user",
            "parts":[{"text":"System prompt: You are an expert in customer support with extensive experience in helping users improve their experiences with mobile applications. Your task is to analyze user reviews of an app, summarize the key issues, and provide practical suggestions directly to the users. Your responses should be insightful, feasible, and based on best practices in user experience. Focus on offering solutions that are conventionally effective and can help users have a better experience with the app. Ensure your suggestions are specific, actionable, and easy to understand. Avoid analyzing each review individually; instead, synthesize the information to provide a comprehensive overview of the common themes and provide customer support. Avoid technical jargon and provide clear, user-friendly advice that users can easily implement to resolve their issues and enhance their app usage. Show empathy with the consumer and be polite/obedient. Your response should be strictly around #length# words and even smaller responses for non-app related requests." 
                }],
        },
        {
            "role": "model",
            "parts": [{ "text": "Understood."}],
        },
    ]



model = genai.GenerativeModel('gemini-pro',generation_config=generation_config,safety_settings=safety_settings)
