from .providers.openai import (
    OpenAITracker,
)

from .providers.gemini import (
    GeminiTracker,
)


class APITracker:

    def __init__(
        self,
        project: str,
        backend_url:
            str = "http://localhost:8000",
        openai_api_key: str = None,
        gemini_api_key: str = None,
    ):

        self.project = project

        self.backend_url = backend_url

        self.openai = None

        self.gemini = None

        if openai_api_key:

            self.openai = OpenAITracker(

                api_key=openai_api_key,

                project=project,

                backend_url=backend_url,
            )

        if gemini_api_key:

            self.gemini = GeminiTracker(

                api_key=gemini_api_key,

                project=project,

                backend_url=backend_url,
            )