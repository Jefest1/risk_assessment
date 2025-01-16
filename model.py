from config import settings
import anthropic


class LLMHandler:
    def __init__(self, api_key=settings.CLAUDE_API_KEY, model=settings.CLAUDE):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model

    def generate_prompt(self, data_json):
        """
        Create a prompt for the LLM to analyze the data and suggest likelihood values.
        """
        return (
            "Analyze provided 'Lower Limit', 'Upper Limit', and 'Response Level' for each row "
            "and add one new field to the data: 'Likelihood Score' (a single digit from 1 to 5) . "
            "Return only the updated data as a JSON object without any additional text or formatting.\n\n"
            f"Data: {data_json}"
        )

    def process_data(self, data):
        """
        Send the data to the LLM and retrieve likelihood suggestions.
        """
        data_json = data.to_json(orient="records")
        prompt = self.generate_prompt(data_json)
        messages = [
            {"role": "user", "content": prompt}
        ]

        try:
            completion = self.client.messages.create(
                model=self.model,
                system="You are an AI assistant specialized in risk assessment. Your task is to analyze the provided 'Lower Limit', 'Upper Limit', and 'Response Level' for each row of data and add one new field: 'Likelihood Score' (a single digit from 1 to 5) Return the updated data as a JSON object without any additional text or formatting.",
                messages=messages,
                max_tokens=4000
            )

            # Directly read the returned JSON into a DataFrame
            updated_data = completion.content[0].text
            return updated_data
        except Exception as e:
            print(f"Error in LLM processing: {e}")
            return None


llm_handler = LLMHandler()
