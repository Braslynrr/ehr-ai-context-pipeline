from .llm_factory import createLLm
from ehr_ai_core.configuration import Config

class EHRAgent:
    """
    Handles clinicians questions through use of context and llm response 
    """

    __llm = None

    def __init__(self, config:Config):
        self.__llm = createLLm(config)

    def Predict(self, question: str, context: str) -> str:

        result = self.__llm(f"""
                            Act as a doctor assistant. 
                            Each answer should have the context from which was taken, if the question is out of context the references can be omitted; So,
                            *Any question out the context should be decline due to it's not in the EHR*.
                            Ensure you are mention the source/reference and refactor it to be read by the user,
                            however don't show the content of the EHR like a json or any similar structure.
                            
                            [Ensure to identify the question language to answer correctly.]

                            Question: {question}
                            context: {context}
                   """)
        
        return "".join(result)