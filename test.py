import pandas as pd
from huggingface_hub import InferenceClient
from config import settings
import json


class LLMHandler:
    def __init__(self, api_key=settings.HF_TOKEN, model=settings.MODEL_ID):
        self.client = InferenceClient(token=api_key)
        self.model = model

    def generate_prompt(self, data_json):
        """
        Create a prompt for the LLM to analyze the data and suggest likelihood values.
        """
        return (
            "Analyze the provided 'Lower Limit', 'Upper Limit', and 'Response Level' for each row "
            "and add two new fields to the data: 'Likelihood' (a single digit from 1 to 5) and 'Reason for Likelihood Suggestion'. "
            "Return only the updated data as a JSON object without any additional text or formatting.\n\n"
            f"Data: {data_json}"
        )

    def process_data(self, data):
        """
        Send the data to the LLM and retrieve likelihood suggestions.
        """
        data_json = data.to_json(orient="records")
        prompt = self.generate_prompt(data_json)
        print(f"Generated prompt \n{prompt}")
        messages = [
            {'role': 'system',
                'content': "You are an AI assistant specialized in risk assessment. Your task is to analyze the provided 'Lower Limit', 'Upper Limit', and 'Response Level' for each row of data and add two new fields: 'Likelihood' (a single digit from 1 to 5) and 'Reason for Likelihood Suggestion'. Return only the updated data as a JSON object without any additional text or formatting or ```."},
            {"role": "user", "content": prompt}
        ]

        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=1024,
            )

            # Directly read the returned JSON into a DataFrame
            updated_data = completion.choices[0].message['content']
            return updated_data
        except Exception as e:
            print(f"Error in LLM processing: {e}")
            return None


# Example Usage
if __name__ == "__main__":

    # Initialize the LLM Handler
    llm_handler = LLMHandler()

    # Example DataFrame
    data = pd.DataFrame({
        "Risk ID": ["R001", "R002"],
        "Description": ["Risk of server downtime", "Risk of data breach"],
        "Indicator": ["days", "percent"],
        "Lower Limit": ["2 days", "10%"],
        "Upper Limit": ["5 days", "20%"],
        "Response Level": ["Moderate", "High"]
    })

    # Process the data using the LLM
    updated_data = llm_handler.process_data(data)

    print("Updated Data:")
    print(updated_data)
