from ehr_ai_core.configuration import Config
from dspy import configure, LM, JSONAdapter


def createLLm(config:Config):
        llm = LM(
            model= f"{config.provider}/{config.model}",
            max_tokens=config.max_tokens,
            num_retries=15,
            temperature=0.2
        )

        configure(lm= llm, async_max_workers=2, adapter=JSONAdapter())

        return llm