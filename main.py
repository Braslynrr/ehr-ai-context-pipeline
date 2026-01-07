from ingestion import load_ehr
from context import ehr_chunkifier

if __name__ == "__main__":
    ehr = load_ehr("data/ehr.json")
    chunks = ehr_chunkifier(ehr)
    