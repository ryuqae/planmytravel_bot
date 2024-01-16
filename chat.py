import openai
import os
import dotenv
import logging

dotenv.load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
openai.organization = os.getenv("OPENAI_ORGANIZATION")

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


class MyTravelAgent:
    def __init__(
        self,
        user,
        prompt_file=None,
        model="gpt-4-1106-preview",
        style={"emoji": False, "polite": False, "verbose": False, "warm": False},
    ):
        self.prompt = self.read_prompt(prompt_file) if prompt_file else ""
        self.style_prompt = ""
        self.user = user
        self.messages = []
        logger.info(f"{user} history initialized: {self.messages}")
        self.temperature = 0.9
        self.top_p = 1
        self.frequency_penalty = 0.0
        self.presence_penalty = 0.6
        self.style = style

    def read_prompt(self, prompt_file):
        with open(f"prompts/{prompt_file}.txt", "r") as f:
            prompt = f.read()

        return prompt

    def set_style(self):
        self.style_prompt = f"\n## 대답 스타일은 꼭 아래 사항을 명심하고 반영해서 대답해줘.\n"
        self.style_prompt += (
            "\n- 이모티콘을 풍부하게 사용해서 대답해 주세요."
            if self.style["emoji"]
            else "\n- 이모티콘은 절대 사용하지 마세요."
        )
        self.style_prompt += (
            "\n- 존댓말로 공손하게 대답해주세요." if self.style["polite"] else "\n- 반말로 친근하게 대답해주세요."
        )
        self.style_prompt += (
            "\n- 대답은 최대한 자세하고 길게 해주세요."
            if self.style["verbose"]
            else "\n- 대답은 최대한 간결하게 요점만 정리 해주세요."
        )
        self.style_prompt += (
            "\n- 대답은 최대한 따뜻하고 공감하는 말투로 해주세요."
            if self.style["warm"]
            else "\n- 대답은 최대한 냉정하게 해주세요.\n\n"
        )
        logger.info(f"Style prompt: {self.style_prompt}")

    def response(self, message, model="gpt-4", last_n=15):
        if self.style_prompt == "":
            self.set_style()

        if len(self.messages) == 0:
            content = (
                self.prompt + "\n\n" + self.style_prompt + "\n\n## 메시지: " + message
            )
        else:
            content = message
        self.messages.append({"role": "user", "content": content})

        logger.info(self.messages)

        response = openai.chat.completions.create(
            model=model,
            messages=self.messages,
            temperature=self.temperature,
            # max_tokens=self.max_tokens,
            top_p=self.top_p,
            frequency_penalty=self.frequency_penalty,
            presence_penalty=self.presence_penalty,
        )

        logger.info(response.choices)
        self.messages.append(
            {"role": "assistant", "content": response.choices[0].message.content}
        )

        return response.choices[0].message.content


if __name__ == "__main__":
    agent = MyTravelAgent("template_01")
    agent.response("제주도 여행을 가려고 하는데 어떻게 가면 좋을까?")
