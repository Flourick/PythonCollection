# Python Scripts Collection

Collection of various python scripts, may be useful to someone.

### BackpackBumper

Used to bump your classified listings on backpack.tf site. You need to launch the script without the headless option first and login, also don't forget to fill in your steamID64 in the script. I'm not even sure this still works as I have not used this in a year or two.

Requires WebDriver for Chrome [(link here)](https://sites.google.com/a/chromium.org/chromedriver/).

You also need an additional python package: `selenium`

### Busyfier

Creates a file every N seconds in it's directory then deletes it immediately after. Does not require any external tools or packages. (I used this for an old broken disk that kept disconnecting)

### EdgeSeleniumTemplate

A template for any selenium script using Edge based on chromium.

Requires WebDriver for Edge [(link here)](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/).

You also need two additional python packages: `selenium` and `msedge-selenium-tools`

### MCStatusDiscordBot

Discord bot that show the amount of players on minecraft server of your choice. Also has a '/status' command that shows more detailed server information (current players, version and favicon) the message also gets automatically deleted after a minute. Inspired by this: https://github.com/tedztar/mcstatusbot

You need two additional python packages: `mcstatus` and `discord.py`

### IMAPDownloader

Downloads all emails from given email account through IMAP in eml format. Configuration is on top of the script. Creates a directory structure with all the emails in their corresponding mailboxes, you can optionally let it zip for you after it finishes downloading. It can also resume previous downloads and skip already downloaded emails.

You need an additional python package: `imap_tools`
