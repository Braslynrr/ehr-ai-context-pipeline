import sys
import traceback
from dotenv import load_dotenv
from ehr_ai_core.services import RagService, EHRService
from ehr_ai_core.aiagent import EHRAgent
from ehr_ai_core.configuration import Config
from ehr_ai_core.api import create_app


def main():
    try:
        load_dotenv()
        config: Config = Config()

        rag = RagService()
        agent = EHRAgent(config)

        medical_service = EHRService(rag, agent)

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