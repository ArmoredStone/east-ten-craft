# My tests of PTB library examples

Ran on Python 3.11.10

## Common solutions across files

## .env explanation

`.env` file in root of the project holds a unique BOT_TOKEN to be used by bot

## logging.basicConfig explanation

`log_filename = os.path.splitext(os.path.basename(__file__))[0]+".log"` specifies filename to be the same as module file name with .log extension

`filemode='a'` specifies mode to append to log file, not overwrite

## .gitignore explanation

A rule block to ignore files without extension, in this case used to ignore pickle persistence files
`*` ignore everything in root directory
`!*/` do not ignore directories in root directory
`!**/*.*` do not ignore files with extensions 

`**/*.log` line to ignore all files with .log extention for privacy concerns
`.env` line to ignore environmental variable file holding test bot token
`.venv` to ignore virtual environment common for test bots

## TODO
https://docs.python-telegram-bot.org/en/stable/examples.pollbot.html
https://docs.python-telegram-bot.org/en/stable/examples.deeplinking.html
https://docs.python-telegram-bot.org/en/stable/examples.inlinekeyboard.html
https://docs.python-telegram-bot.org/en/stable/examples.inlinekeyboard2.html
https://docs.python-telegram-bot.org/en/stable/examples.conversationbot.html
https://docs.python-telegram-bot.org/en/stable/examples.conversationbot2.html
https://docs.python-telegram-bot.org/en/stable/examples.nestedconversationbot.html
