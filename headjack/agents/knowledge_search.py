import logging
from typing import Union

import lmql

from headjack.agents.registry import register_agent_function
from headjack.config import get_settings
from headjack.models.utterance import Answer, Response, Utterance
from headjack.utils import fetch

_logger = logging.getLogger("uvicorn")


async def search_for_knowledge(q):
    settings = get_settings()
    try:
        q = q.strip("\n '.")
        _logger.info("Searching knowledge collection using the headjack search service")
        results = await fetch(f"{settings.search_service}/query?collection=knowledge&text={q}", "GET", return_json=True)
        return [i for j in results["documents"] for i in j]
    except Exception as e:
        _logger.info("Error while attempting to reach headjack search " f"service knowledge collection: {str(e)}")
        return "No results"


@register_agent_function(
    "This is a general knowledge search. Provided a query, this will give a summary of information from the knowledge base.",
    "knowledge_search_agent",
)
@lmql.query
async def knowledge_search_agent(question: Utterance) -> Union[Response, Answer]:  # type: ignore
    """lmql
    argmax
        "Given the following question, use a term to search for relevant information and create a summary answer.\n"
        "Question: {question.utterance}\n"
        "Action: Let's search for the term '[TERM]\n"
        result = await search_for_knowledge(TERM)
        if result == 'No results':
            return Response(utterance=result, parent_ = question)
        "Result: {result}\n"
        "Final Answer:[ANSWER]"
        return Answer(utterance=ANSWER, parent_ = question)
    FROM
        "chatgpt"
    WHERE
        STOPS_AT(TERM, "'")
    """
