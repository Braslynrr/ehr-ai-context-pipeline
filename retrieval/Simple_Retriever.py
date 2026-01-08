class SimpleRetriever:
    __chunks = None
    def __init__(self, chunks):
        super().__init__()
        self.__chunks = chunks

    def RetrieveChunks(self, query):
        relevantchunks = []

        query_lower = query.lower()

        if "medicación" in query_lower:
            return [c for c in self.__chunks if c["type"] == "current_medications"]
        
        if "condicion" in query_lower:
            return [c for c in self.__chunks if c["type"] == "chronic_conditions"]

        if "última visita" in query_lower:
            visits = [c for c in self.__chunks if c["type"] == "recent_visit"]
            return sorted(visits, key=lambda c: c["date"], reverse=True)[:1]
        elif "visita" in query_lower:
            return [c for c in self.__chunks if c["type"] == "recent_visit"]

        if "alergia" in query_lower:
            return [c for c in self.__chunks if c["type"] == "allergies"]

        if "glucosa" in query_lower:
            return [c for c in self.__chunks if c["type"] == "lab_result" and self.__wordFinder("glucose", c)]
        
        if "último" in query_lower and "laboratorio" in query_lower:
            lab = [c for c in self.__chunks if c["type"] == "lab_result"]
            return sorted(lab, key=lambda c: c["date"], reverse=True)[:1]

        return relevantchunks
    

    def __wordFinder(self, word: str, data) -> bool:
        if isinstance(data, dict):
            return (
                any(self.__wordFinder(word, k) for k in data.keys()) or
                any(self.__wordFinder(word, v) for v in data.values())
            )

        if isinstance(data, list):
            return any(self.__wordFinder(word, item) for item in data)

        if isinstance(data, str):
            return word.lower() in data.lower()

        return False
