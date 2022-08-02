# hopper-parser
Parses Chatterino logs and creates a list of users who were permabanned after posting only a couple messages. This builds a fairly good list of hoppers and spammers/bots.

Usage:
./main.py --input channel-2000-01-31.log

Optional arguments:
-i, --input: (required) the file to read
-o, --output: the file to write to. if unset, print to stdout
--hideUsers: hide usernames
--numMessages: (default: 5)  the maximum number of recent messages before a chatter is omitted from the list
--recentLength: (default: 500) the maximum number of messages to check prior to each permaban
