from abc import ABC, abstractmethod


class ITool(ABC):
    name: str
    description:str

    @abstractmethod
    async def run(self, input: dict) -> dict:
        ...