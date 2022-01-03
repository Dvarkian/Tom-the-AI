import codecs
import hashlib
import re
from typing import List

import requests

cookies = None
sessions = dict()


def cleverbot(stimulus: str, context: List[str] = [], session: str = None) -> str:
    """Establishs communication with cleverbot and returns the decoded response
    string.

    :param stimulus: Message to add to this cleverbot session and get a direct answer for.
    :type stimulus: str
    :param context: List of messages to preload on the bot.
    :type context: List[str]
    :param session: Session name to differenciate from other conversations. Each session is a separate conversation.
    :type session: str
    :rtype: str
    """

    global cookies, sessions
    if cookies is None:
        req = requests.get("https://www.cleverbot.com/")
        cookies = {"XVIS": re.search(r"\w+(?=;)", req.headers["Set-cookie"]).group()}
    payload = f"stimulus={requests.utils.requote_uri(stimulus)}&"

    _context = context[:]
    reverse_context = list(reversed(_context))

    for i in range(len(_context)):
        payload += f"vText{i + 2}={requests.utils.requote_uri(reverse_context[i])}&"

    if session:
        # Creates new session if not exist
        if session not in sessions.keys():
            sessions[session] = list()

        _session = list(reversed(sessions[session]))
        # Adding the session to the payload
        for i in range(len(sessions[session])):
            payload += f"vText{i + len(_context) + 2}={requests.utils.requote_uri(_session[i])}&"

        # Adds the context to the session
        sessions[session] = _context + sessions[session]

    payload += "cb_settings_scripting=no&islearning=1&icognoid=wsf&icognocheck="

    payload += hashlib.md5(payload[7:33].encode()).hexdigest()

    req = requests.post(
        "https://www.cleverbot.com/webservicemin?uc=UseOfficialCleverbotAPI",
        cookies=cookies,
        data=payload,
    )
    getresponse = re.split(r"\\r", str(req.content))[0]
    response = getresponse[2:-1]
    if session:
        sessions[session].extend([stimulus, response])
    return codecs.escape_decode(bytes(response, "utf-8"))[0].decode("utf-8")
