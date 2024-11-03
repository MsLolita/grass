import time
import asyncio
from datetime import datetime, timezone, timedelta
from typing import Optional, Dict

from imap_tools import MailBox, AND
from loguru import logger

from data.config import EMAIL_FOLDER, IMAP_DOMAIN, SINGLE_IMAP_ACCOUNT


class MailUtils:
    def __init__(self, email: str, imap_pass: str) -> None:
        if SINGLE_IMAP_ACCOUNT:
            self.email: str = SINGLE_IMAP_ACCOUNT.split(":")[0]
        else:
            self.email: str = email
        self.imap_pass: str = imap_pass
        self.domain: str = IMAP_DOMAIN or self.parse_domain()

    def parse_domain(self) -> str:
        domain: str = self.email.split("@")[-1]

        if "hotmail" in domain or "live" in domain:
            domain = "outlook.com"
        elif "firstmail" in domain:
            domain = "firstmail.ltd"
        elif any(sub in domain for sub in ["rambler", "myrambler", "autorambler", "ro.ru"]):
            domain = "rambler.ru"
        elif "icloud" in domain:
            domain = "mail.me.com"

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

        email_folder = ["INBOX"]

        if EMAIL_FOLDER:
            email_folder = [EMAIL_FOLDER]
        elif "outlook" in self.domain:
            email_folder.append("JUNK")
        # elif "rambler" in self.domain:
        else:
            email_folder.append("Spam")


        start_time = datetime.now(timezone.utc) - timedelta(seconds=5)
        end_time = time.time() + delay

        while time.time() < end_time:
            time.sleep(5)
            for folder in email_folder:
                with MailBox(self.domain).login(self.email, self.imap_pass, initial_folder=folder) as mailbox:
                    try:
                        criteria = AND(subject=subject, to=to, from_=from_, seen=seen)
                        for msg in mailbox.fetch(criteria, limit=limit, reverse=reverse):
                            if msg.date > start_time:
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
