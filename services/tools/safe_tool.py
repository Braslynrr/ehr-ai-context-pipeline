from ehr_ai_core.error.app_error import AppError
from services.tools.Itool import ITool


class safe_tool(ITool):

    def run(self, input):
        raise AppError("Undefined Tool", 500)