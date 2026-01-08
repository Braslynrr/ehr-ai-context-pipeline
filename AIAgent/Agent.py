import dspy

class EHRAgent:

    __llm = None

    class MedicalSignature(dspy.Signature):
        context = dspy.InputField()
        question = dspy.InputField()
        answer = dspy.OutputField(desc="Actua como un asistente de medico general. Limita la respuesta al contexto y asegurate de mencionar la referencia; Cualquier otra pregunta o comentario fuera del ambito medico o fuera del contexto, debe de ser rechazada cordialmente.")


    def __init__(self, llm):
        self.__llm = llm

    def Predict(self, question: str, context: str) -> str:
        ##predictor = dspy.Predict(
        ##    self.MedicalSignature,
        ##    lm=self.__llm
        ##)
        ##result = predictor(context=context, question=question)
        result = self.__llm(f"""Actua como un asistente de medico general. Limita la respuesta al contexto y asegurate de mencionar la referencia; Cualquier otra pregunta o comentario fuera del ambito medico o fuera del contexto, debe de ser rechazada cordialmente.
                       Question: {question}
                        context: {context}
                   """)
        
        
        return result[0]