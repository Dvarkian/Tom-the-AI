import codecs
import hashlib
import logging
import re
import time
from datetime import datetime
from typing import List, Union

import requests

from .constants import (CLEVERBOT_API_URL, CLEVERBOT_COOKIE_URL, CLEVERBOT_URL,
                        DEBOUNCE_TIME, MAX_ATTEPTS, MAX_CONTEXT_LENGTH,
                        MAX_DEBOUNCE_ATTEMPS)


class Cleverbot:
    """
    Cleverbot api wrapper

    Attributes
    ----------
    cookies : dict
        Cookies to be used in the requests.
    context : list
        List of messages representing the context of the conversation.
    proxies :
        Proxy to be used or proxies to rotate through.
    debounce: bool
        Whether to try to debounce the requests or not. If set to False it will try to use proxies immediately upon failure.
    :param use_tor_fallback:
        If set to True, whenever a request fail will try to use a new tor session as a proxy. This will override the proxy options. Even when this is set to true it will still try to make a connection without using tor at first.
    Methods
    ----------
    send(message)
        Sends a message to Cleverbot and returns the response as a string.
    """

    def __init__(
        self,
        context: List[str] = [],
        proxies: Union[dict, List[dict], List[str]] = None,
        debounce: bool = True,
        use_tor_fallback: bool = False,
    ):
        """
        Cleverbot Constructor

        :param context List[str]:List of strings to be used as the initial chat messages with the bot.
        :param proxies dict: Must have keys "http" and "https" and values of the proxies address:port to be used on the requests library format. You can also pass a list of proxies to rotate through. If an element of the list is None, it means not to use any proxy.
        :param debounce bool: Whether to try to debounce the requests or not. If set to False it will try to use proxies immediately upon failure.
        :param use_tor_fallback: If set to True, whenever a request fail will try to use a new tor session as a proxy. This will override the proxy options. Even when this is set to true it will still try to make a connection without using tor at first.
        """
        self.cookies = None
        self.context = context
        self.proxies = proxies
        self.debounce = debounce
        self.use_tor = use_tor_fallback

        if not isinstance(self.use_tor, bool):
            raise ValueError("use_tor_fallback must be a boolean")

        if proxies is None:
            self.proxies = [None]
        elif isinstance(proxies, dict):
            self.proxies = [proxies]
        elif isinstance(proxies, list):
            self.proxies = []
            for proxy in proxies:
                if isinstance(proxy, dict):
                    self.proxies.append(proxy)
                elif isinstance(proxy, str):
                    self.proxies.append({"http": proxy, "https": proxy})
                elif proxy is None:
                    self.proxies.append(None)
                else:
                    raise ValueError(
                        "Invalid proxy format. Must be a dict or a list of dicts."
                    )
        else:
            raise ValueError(
                "Invalid proxy format. Must be a dict, a list of dicts or a list of strings."
            )

        self._proxy_index = 0
        self._debounce_attempts = 0
        self._proxy = self.proxies[0]
        self._attempts = 0
        self.session = None
        self._tor_context = None
        self._start_session()

    def _start_session(self, tor=False):
        """Starts a new session refreshing the cookies"""
        logging.debug("Starting new session")
        if tor:
            try:
                from torpy.http.requests import tor_requests_session
            except ModuleNotFoundError:
                raise ModuleNotFoundError("You have to install torpy to use the tor fallback. Run: pip3 install torpy[requests]")
            logging.info("Starting tor session")
            if self._tor_context:
                self._tor_context.__exit__()
            self._tor_context = tor_requests_session()
            self.session = self._tor_context.__enter__()
            logging.info("tor session created!")
        else:
            self.session = requests.Session()
            self.session.proxies = self._proxy

        date = datetime.now().strftime("%Y%m%d")
        response = self.session.get(CLEVERBOT_COOKIE_URL + date)
        if "Set-cookie" not in response.headers:
            if not tor and self.use_tor:
                return self._start_session(self.use_tor)
            raise requests.exceptions.HTTPError(f"Api returned '{response.status_code}' for request. Try to use a proxy or use_tor_fallback")
        self.cookies = {
            "XVIS": re.search(r"\w+(?=;)", response.headers["Set-cookie"]).group()
        }

    def send(self, message: str) -> str:
        """
        Sends a message to Cleverbot and returns the response as a string.

        :param message str: The message to send to Cleverbot.
        :rtype str: Message received from Cleverbot.
        """
        payload = f"stimulus={requests.utils.requote_uri(message)}&"
        _context = self.context[:]
        reverse_context = list(reversed(_context))

        # Clear context list to keep things short and fast
        self._clear_context()
        for i in range(len(_context)):
            payload += f"vText{i + 2}={requests.utils.requote_uri(reverse_context[i])}&"

        # Append message to the context for future messages
        self.context.append(message)

        payload += "cb_settings_scripting=no&islearning=1&icognoid=wsf&icognocheck="

        # Checksum
        payload += hashlib.md5(payload[7:33].encode()).hexdigest()

        response = self.session.post(
            CLEVERBOT_API_URL,
            cookies=self.cookies,
            data=payload,
        )

        # If the request is not succesful, refresh cookies, debounce, try a new proxy
        if response.status_code != 200:
            if self._attempts > len(self.proxies) + MAX_ATTEPTS:
                logging.error(
                    f"Cleverbot failed to respond after {self._attempts} attempts. Giving up."
                )
                self._attempts = 0
                # TODO: Raise exception? Return None? idk
                return ""

            self._start_session(self.use_tor)
            if self._debounce_attempts >= MAX_DEBOUNCE_ATTEMPS or not self.debounce:
                self._debounce_attempts = 0
                self._proxy_index += 1
                if self._proxy_index >= len(self.proxies):
                    self._proxy_index = 0
                logging.info(
                    f"Cleverbot failed to respond. Trying proxy {self.proxies[self._proxy_index]}"
                )
                self._proxy = self.proxies[self._proxy_index]

            elif self.debounce:
                self._debounce_attempts += 1
                logging.info(
                    f"Cleverbot failed to respond. Trying again in {DEBOUNCE_TIME * self._debounce_attempts} seconds."
                )
                time.sleep(DEBOUNCE_TIME * self._debounce_attempts)

            self.context.pop()
            self._attempts += 1
            return self.send(message)

        response = re.split(r"\r", response.content.decode("utf-8"))[0]
        self._attempts = 0

        # Append bot's response to the context
        self.context.append(response)
        return codecs.escape_decode(bytes(response, "utf-8"))[0].decode("utf-8")

    def _clear_context(self):
        """_clear_context."""
        if len(self.context) >= MAX_CONTEXT_LENGTH:
            self.context.pop(0)
