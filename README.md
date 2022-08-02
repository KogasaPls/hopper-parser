# hopper-parser
Parses Chatterino logs and creates a list of users who were permabanned after posting only a couple messages, along with those messages. This builds a fairly good list of hoppers and spammers/bots.

Usage:

    > ./main.py --input demo.log
    Chatter #1: user
    [00:00:01] user: hello
    [00:03:13] user: fuk u


Optional arguments:

    -i, --input: (required) the file to read

    -o, --output: the file to write to. if unset, print to stdout

    --hideUsers: hide usernames

    --numMessages: (default: 5)  the maximum number of recent messages before a chatter is omitted from the list

    --recentLength: (default: 500) the maximum number of messages to check prior to each permaban
