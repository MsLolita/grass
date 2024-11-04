import re
from datetime import datetime
from typing import Iterator, Sequence

from imaplib import IMAP4_SSL
from better_proxy import Proxy
from bs4 import BeautifulSoup
from imap_tools import AND, MailMessage, MailBox as BaseMailBox

from .proxy import IMAP4SSlProxy


def get_message_text(mail_message: MailMessage) -> str:
    if mail_message.text:
        return mail_message.text
    else:
        soup = BeautifulSoup(mail_message.html, 'html.parser')
        return soup.get_text()


class MailBox(BaseMailBox):
    def __init__(
        self,
        host: str,
        *,
        proxy: Proxy | str = None,
        port: int = 993,
        timeout: float = None,
        rdns: bool = True,
        ssl_context=None,
    ):
        self._proxy = Proxy.from_str(proxy) if proxy else None
        self._rdns = rdns
        super().__init__(host=host, port=port, timeout=timeout, ssl_context=ssl_context)

    def _get_mailbox_client(self):
        if self._proxy:
            return IMAP4SSlProxy(
                self._host,
                self._proxy,
                port=self._port,
                rdns=self._rdns,
                timeout=self._timeout,
                ssl_context=self._ssl_context,
            )
        else:
            return IMAP4_SSL(
                self._host,
                port=self._port,
                timeout=self._timeout,
                ssl_context=self._ssl_context,
            )

    def login(self, username: str, password: str, initial_folder: str | None = 'INBOX'):
        if self._host == "imap.rambler.ru" and "%" in password:
            raise ValueError(
                f"IMAP password contains '%' character. Change your password."
                f" It's a specific rambler.ru error"
            )

        return super().login(username, password, initial_folder)

    def fetch_messages(
            self,
            folders: Sequence[str] = ("INBOX", ),
            *,
            since: datetime = None,
            allowed_senders: Sequence[str] = None,
            allowed_receivers: Sequence[str] = None,
            sender_regex: str | re.Pattern[str] = None,
            limit: int = 10,
            reverse: bool = True,
    ) -> Iterator[MailMessage]:
        for folder in folders:
            self.folder.set(folder)

            criteria = AND(
                date_gte=since.date() if since else None,
                from_=allowed_senders if allowed_senders else None,
                to=allowed_receivers if allowed_receivers else None,
                all=True  # Условие для выборки всех сообщений при отсутствии других фильтров
            )

            for message in self.fetch(criteria, limit=limit, reverse=reverse):  # type: MailMessage
                # Фильтрация по дате
                if since and message.date < since:
                    continue

                # Фильтрация по регулярному выражению
                if sender_regex and not re.search(sender_regex, message.from_, re.IGNORECASE):
                    continue

                yield message

    def search_matches(
        self,
        regex: str | re.Pattern[str],
        folders: Sequence[str] = None,
        *,
        since: datetime = None,
        allowed_senders: Sequence[str] = None,
        allowed_receivers: Sequence[str] = None,
        sender_regex: str | re.Pattern[str] = None,
        limit: int = 10,
        reverse: bool = True,
    ) -> list[tuple[MailMessage, str]]:
        matches = []
        messages = self.fetch_messages(
            folders,
            since=since,
            allowed_senders=allowed_senders,
            allowed_receivers=allowed_receivers,
            sender_regex=sender_regex,
            limit=limit,
            reverse=reverse,
        )

        for message in messages:
            if found := re.findall(regex, get_message_text(message)):
                matches.append((message, found[0]))

        return matches
