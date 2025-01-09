from huggingface_hub import InferenceClient
# from openai import OpenAI
from config import settings
import streamlit as st
import pandas as pd


class LLMHandler:
    def __init__(self, api_key=settings.HF_TOKEN, model=settings.META_MODEL):
        self.client = InferenceClient(token=api_key)
        self.model = model

    def generate_prompt(self, data_json):
        """
        Create a prompt for the LLM to analyze the data and suggest likelihood values.
        """
        return (
            "Analyze the provided 'Lower Limit', 'Upper Limit', and 'Response Level' for each row "
            "and add one new field to the data: 'Likelihood' (a single digit from 1 to 5) . "
            "Return only the first eight rows updated data as a JSON object without any additional text or formatting.\n\n"
            f"Data: {data_json}"
        )

    def process_data(self, data):
        """
        Send the data to the LLM and retrieve likelihood suggestions.
        """
        data_json = data.to_json(orient="records")
        prompt = self.generate_prompt(data_json)
        messages = [
            {'role': 'system',
                'content': "You are an AI assistant specialized in risk assessment. Your task is to analyze the provided 'Lower Limit', 'Upper Limit', and 'Response Level' for each row of data and add one new field: 'Likelihood score' (a single digit from 1 to 5) Return only the first eight rows updated data as a JSON object without any additional text or formatting."},
            {"role": "user", "content": prompt}
        ]

        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=1290,
            )

            # Directly read the returned JSON into a DataFrame
            updated_data = completion.choices[0].message['content']
            return updated_data
        except Exception as e:
            st.error(f"Error in LLM processing: {e}")
            return None


llm_handler = LLMHandler()
