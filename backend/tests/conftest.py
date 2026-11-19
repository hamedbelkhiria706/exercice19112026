import sys
from pathlib import Path

root_dir = Path(__file__).resolve().parents[2]
backend_dir = Path(__file__).resolve().parents[1]

for directory in (root_dir, backend_dir):
    if str(directory) not in sys.path:
        sys.path.insert(0, str(directory))

import backend.app as backend_app
import backend.app.routers as backend_routers
import backend.app.routers.chat as backend_chat
import backend.app.routers.quizz as backend_quizz
import backend.app.routers.summarize as backend_summarize
import backend.app.routers.flashcard as backend_flashcard
import backend.app.services as backend_services
import backend.app.services.ai as backend_ai
import backend.app.services.quizz as backend_service_quizz
import backend.app.services.summarize as backend_service_summarize
import backend.app.services.flashcard as backend_service_flashcard

sys.modules.setdefault("app", backend_app)
sys.modules.setdefault("app.routers", backend_routers)
sys.modules["app.routers.chat"] = backend_chat
sys.modules["app.routers.quizz"] = backend_quizz
sys.modules["app.routers.summarize"] = backend_summarize
sys.modules["app.routers.flashcard"] = backend_flashcard
sys.modules.setdefault("app.services", backend_services)
sys.modules["app.services.ai"] = backend_ai
sys.modules["app.services.quizz"] = backend_service_quizz
sys.modules["app.services.summarize"] = backend_service_summarize
sys.modules["app.services.flashcard"] = backend_service_flashcard
