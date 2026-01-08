from dataclasses import dataclass
from typing import Dict, Any, List

@dataclass
class VectorEntry:
    embedding: List[float]
    payload: Dict[str, Any]   # your original chunk