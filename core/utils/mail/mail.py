import time
import asyncio
from datetime import datetime, timezone, timedelta
from typing import Optional, Dict

from imap_tools import AND #, MailBox
from loguru import logger

from core.utils.mail.mailbox import MailBox
from data.config import EMAIL_FOLDER, IMAP_DOMAIN, SINGLE_IMAP_ACCOUNT, USE_PROXY_FOR_IMAP


class MailUtils:
    def __init__(self, email: str, imap_pass: str, proxy: str = None) -> None:
        if SINGLE_IMAP_ACCOUNT:
            self.email: str = SINGLE_IMAP_ACCOUNT.split(":")[0]
        else:
            self.email: str = email
        self.imap_pass: str = imap_pass
        self.domain: str = IMAP_DOMAIN or self.parse_domain()

        self.proxy = proxy if USE_PROXY_FOR_IMAP else None

    def parse_domain(self) -> str:
        domain: str = self.email.split("@")[-1]

        if "hotmail" in domain or "live" in domain:
            domain = "outlook.com"
        elif "yahoo" in domain:
            domain = "mail.yahoo.com"
        elif "firstmail" in domain:
            domain = "firstmail.ltd"
        elif any(sub in domain for sub in ["rambler", "myrambler", "autorambler", "ro.ru"]):
            domain = "rambler.ru"
        elif "icloud" in domain:
            domain = "mail.me.com"
        elif "gazeta" in domain:
            domain = "gazeta.pl"
        elif "onet" in domain:
            domain = "poczta.onet.pl"
        elif "gmx" in domain:
            domain = "gmx.net"
        elif "firemail" in domain:
            domain = "firemail.de"

        return f"imap.{domain}"

    def get_msg(
            self,
            to: Optional[str] = None,
            subject: Optional[str] = None,
            from_: Optional[str] = None,
            seen: Optional[bool] = None,
            limit: Optional[int] = None,
            reverse: bool = True,
            delay: int = 60
    ) -> Dict[str, any]:


        if EMAIL_FOLDER:
            email_folders = [EMAIL_FOLDER]
        else:
            email_folders = ["INBOX", "Junk", "JUNK", "Spam", "SPAM", "TRASH", "Trash"]

        with MailBox(
                self.domain,
                proxy=self.proxy
        ).login(self.email, self.imap_pass, initial_folder=None) as mailbox:
            actual_folders = [mailbox.name for mailbox in list(mailbox.folder.list())]
            folders = [folder for folder in email_folders if folder in actual_folders]

            for _ in range(delay // 3):
                time.sleep(3)
                try:
                    for folder in folders:
                        mailbox.folder.set(folder)
                        criteria = AND(subject=subject, to=to, from_=from_, seen=seen)

                        for msg in mailbox.fetch(criteria, limit=limit, reverse=reverse):
                            logger.success(f'{self.email} | Successfully found new msg by subject: {msg.subject}')
                            return {
                                "success": True,
                                "msg": msg.html,
                                "subject": msg.subject,
                                "from": msg.from_,
                                "to": msg.to
                            }
                except Exception as error:
                    logger.error(f'{self.email} | Error when fetching new message by subject: {str(error)}')

        return {"success": False, "msg": "New message not found by subject"}

    async def get_msg_async(
            self,
            to: Optional[str] = None,
            subject: Optional[str] = None,
            from_: Optional[str] = None,
            seen: Optional[bool] = None,
            limit: Optional[int] = None,
            reverse: bool = True,
            delay: int = 60
    ) -> Dict[str, any]:
        return await asyncio.to_thread(self.get_msg, to, subject, from_, seen, limit, reverse, delay)


# if __name__ == '__main__':
#     email = ""
#     imap_pass = ""
#     mail_utils = MailUtils(email, imap_pass)
#
#     # Asynchronous call
#     async def main():
#         result = await mail_utils.get_msg_async(to=email, from_="support@wynd.network", subject="Verify Your Email for Grass")
#         print(result)
#         if result['success']:
#             verify_link = result['msg'].split('<![endif]-->\r\n    <a href="')[1].split('"')[0]
#             print(verify_link)
#
#
#     asyncio.run(main())
