import sys
import traceback
from dotenv import load_dotenv
from services import RagService, MedicalService
from aiagent import EHRAgent
from configuration import Config
from api import create_app


def main():
    try:
        load_dotenv()
        config: Config = Config()

        rag = RagService()
        agent = EHRAgent(config.llm)

        medical_service = MedicalService(rag, agent)

        app = create_app(medical_service, config)
        app.run(debug=True)

    except RuntimeError as e:
        print(f"[STARTUP ERROR] {e}")
        sys.exit(1)

    except Exception:
        print("[FATAL ERROR] Application failed to start")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()