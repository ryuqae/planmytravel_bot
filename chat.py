import openai
import os
import dotenv

dotenv.load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
openai.organization = os.getenv("OPENAI_ORGANIZATION")


class MyTravelAgent:
    def __init__(self, prompt_file):
        self.promt_dir = "prompts"
        self.prompt = self.read_prompt(prompt_file)
        self.messages = [{"role": "user", "content": self.prompt}]
        self.temperature = 0.9
        # self.max_tokens=100
        self.top_p = 1
        self.frequency_penalty = 0.0
        self.presence_penalty = 0.6
        self.emoji = True
        self.polite = True
        self.verbose = True
        # self.style = "normal"  TBD -> 스타일 어떻게 넣어줄건지

    def read_prompt(self, prompt_file):
        with open(f"{self.promt_dir}/{prompt_file}.txt", "r") as f:
            prompt = f.read()
        return prompt

    def response(self, message, last_n=10):
        # print(self.messages)
        self.messages.append({"role": "user", "content": message})
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=self.messages[-last_n:],
            temperature=self.temperature,
            # max_tokens=self.max_tokens,
            top_p=self.top_p,
            frequency_penalty=self.frequency_penalty,
            presence_penalty=self.presence_penalty,
            # stop=["\n"],
        )
        self.messages.append(
            {"role": "assistant", "content": response.choices[0].message.content}
        )

        return response.choices[0].message.content


if __name__ == "__main__":
    agent = MyTravelAgent("template_01")
    agent.response("제주도 여행을 가려고 하는데 어떻게 가면 좋을까?")
