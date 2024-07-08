# Grass Auto Reger&Farm 🔹


Discover the latest `<crypto/>` moves in my Telegram Channel:

[![My Channel 🥰](https://img.shields.io/badge/Web3_Enjoyer_|_Subscribe_🥰-0A66C2?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/web3_enjoyer_club) 

Cheapest [proxies and servers](https://teletype.in/@web3enjoyer/4a2G9NuHssy) which fits for  on [grass.io](https://app.getgrass.io/register/?referralCode=erxggzon61FWrJ9).

![image](https://github.com/MsLolita/grass/assets/58307006/610b95b4-369f-4a71-ac24-f45e8dee6380)


### What is bot for?
   - Create Accounts
   - Farm Points
   - Check Points
   - Approve Emails without access to it (no need imap, etc)

> You can put as many proxies as u can, bot uses database and will load up proxies from extra ones

🔹**To say thanks for work: 0x000007c73a94f8582ef95396918dcd04f806cdd8**


## Quick Start 📚
   1. To install libraries on Windows click on `INSTALL.bat` (or in console: `pip install -r requirements.txt`).
   2. To start bot use `START.bat` (or in console: `python main.py`).

### Options 📧

1. CREATE ACCOUNTS:
 - In `data/config.py` put `REGISTER_ACCOUNT_ONLY = True`
 - Throw the api key into `data/config.py`. Since there is a captcha there, you need a service for solving captchas - [AntiCaptcha](http://getcaptchasolution.com/t8yfysqmh3) or [Twocaptcha](https://2captcha.com/?from=12939391).
 - Provide emails and passwords (OPTIONAL) and proxies to register accounts as below!

  ![image](https://github.com/MsLolita/grass/assets/58307006/67740c9b-07d6-4f78-a87d-27b09c0303e8)

2. FARM POINTS:
 - in `data/config.py` put `REGISTER_ACCOUNT_ONLY = False`
 - Provide emails and passwords and proxies to register accounts as shown below!

3. APPROVE EMAILS:
 - in `data/config.py`:
   - `APPROVE_EMAIL = True` approve email (NEEDED IMAP AND ACCESS TO EMAIL)
   - `CONNECT_WALLET = True` connect wallet (put private keys in wallets.txt)
   - `SEND_WALLET_APPROVE_LINK_TO_EMAIL = True`  # send approve link to email
   - `APPROVE_WALLET_ON_EMAIL = True`  # get approve link from email (NEEDED IMAP AND ACCESS TO EMAIL)
 - Provide emails and passwords and imap password (access to email) in format email:password:imap_password!
 - Need IMAP access to email
 -  `SINGLE_IMAP_ACCOUNT = False `  # if you have possibility to forward all approve mails to single IMAP address. Usage: change False to "name@domain.com:password" of your main IMAP address
 -  `EMAIL_FOLDER = "" `  # skip for auto, folder where mails comes
 -  `IMAP_DOMAIN = "" `  # skip for auto domain, not always works
- `ACCOUNTS_TO_WORK = False` # useful if you want to select specific accounts that have failed:
  - `ACCOUNTS_TO_WORK = False` # all accounts
  - `ACCOUNTS_TO_WORK = 3` # single account e.g. 3
  - `ACCOUNTS_TO_WORK: list = [1, 3, 7]` # specific accounts (e.g. accounts 1, 3, 7)
  - `ACCOUNTS_TO_WORK: tuple = (3, 6)` # range of accounts (e.g. accounts 3, 4, 5, 6)

![image](https://github.com/MsLolita/grass/assets/58307006/e28fba4c-1809-48f9-9475-d881a26beab5)
![image](https://github.com/opensolmap/solmap/assets/58307006/edf3ad67-37b4-434c-acfb-98cf58801c61)


### Configuration 📧

1. Accounts Setup 🔒

   Put in `data/accounts.txt` accounts in format email:password (cool_aster@gmail.com:my_password123)
   
   ![image](https://github.com/MsLolita/grass/assets/58307006/2f8bacaa-0212-49fe-b362-fe764230f47c)

2. Proxy Setup 🔒

   Configure your proxies with the *ANY* (socks, http/s, ...) format in `data/proxies.txt` 🌐

   ![Proxy Configuration](https://github.com/MsLolita/VeloData/assets/58307006/a2c95484-52b6-497a-b89e-73b89d953d8c)

## Quick Start By Docker
   1. Install Docker-CE: `curl -sSL -k https://get.docker.com | sh`
   2. Install Docker Compose: `curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose && chmod +x /usr/local/bin/docker-compose`
   3. Clone Source Code: `git clone https://github.com/MsLolita/grass.git`
   4. Configuration: Modify `data/accounts.txt` and `data/proxies.txt`
   5. Start Container: `docker-compose up -d`

   PS: Could see more configuration in `docker-compose.yml`

