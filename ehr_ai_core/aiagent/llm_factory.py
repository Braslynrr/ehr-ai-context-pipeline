from dspy import configure, LM, JSONAdapter


def createLLm(provider:str, model:str, max_tokens:str):
    llm = LM(
        model= f"{provider}/{model}",
        max_tokens=max_tokens,
        num_retries=15,
        temperature=0.2
    )

    configure(lm= llm, async_max_workers=2, adapter=JSONAdapter())

    return llm


def createOllamaStreaming(model:str):
        pass