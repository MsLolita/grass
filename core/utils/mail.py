import time
import asyncio
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
            email_folder = EMAIL_FOLDER
        elif "outlook" in self.domain:
            email_folder = "JUNK"
        elif "rambler" in self.domain:
            email_folder = "Spam"
        else:
            email_folder = "INBOX"

        with MailBox(self.domain).login(self.email, self.imap_pass, initial_folder=email_folder) as mailbox:
            for _ in range(delay // 3):
                time.sleep(3)
                try:
                    for msg in mailbox.fetch(AND(to=to, from_=from_, seen=seen), limit=limit, reverse=reverse):
                        if subject is not None and msg.subject != subject:
                            continue

                        logger.success(f'{self.email} | Successfully received msg: {msg.subject}')
                        return {"success": True, "msg": msg.html}
                except Exception as error:
                    logger.error(f'{self.email} | Unexpected error when getting code: {str(error)}')
        return {"success": False, "msg": "Didn't find msg"}

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
