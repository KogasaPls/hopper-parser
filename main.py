#!/bin/python3
import regex as re
import argparse
parser = argparse.ArgumentParser(
    description='Parse Chatterino logs and create a list of users who were permabanned after sending a small number of recent messages. These users might be hoppers.')

parser.add_argument("-i", "--input", help="(required) the file to read", type=str, required=True)
parser.add_argument(
    "-o",
    "--output",
    help="the file to write to (if unset, print to stdout)",
    type=str)
parser.add_argument("--hideUsers", help="hide usernames", action="store_true")
parser.add_argument(
    "--numMessages",
    help="(default: 5) the maximum number of recent messages before a chatter is considered 'not a hopper'",
    type=int,
    default=5)
parser.add_argument(
    "--recentLength",
    help="(default: 500) the number of messages to check prior to each permaban",
    type=int,
    default=500)
parser.add_argument(
    "-a",
    "--all",
    help="show all first time chatters in addition to banned users",
    action="store_true")

arg = parser.parse_args()

# read lines from file


def readLines(file):
    # open the file
    f = open(file, "r", encoding='utf-8')
    # read the file
    lines = f.readlines()
    # close the file
    f.close()
    return lines

# write lines to file


def flush(lines, file):
    f = open(file, "w", encoding='utf-8')
    for line in lines:
        f.write(line)
    f.close()

# list of all lines sent by chatter


def messagesFromChatterBefore(lines, chatter, index, newChatters):
    # my Chatterino is patched to log first-time chatters with "[First Message]"
    p = re.compile(r"^(\[\d\d:\d\d:\d\d\](?: \[First Message\])?)  " + chatter + ": (.*)\n")
    # create a list to store the matching lines
    matchingLines = []

    if chatter in newChatters:
        start = chatter[1]
    else:
        start = max(index - arg.recentLength, 0)

    # all messages in the last (default: 500) total lines, or until the first message
    recentMessages = lines[start:index]

    # loop through the lines
    for line in recentMessages:
        m = p.match(line)
        if m:
            if arg.hideUsers:
                chatter = "chatter"
            matchingLines.append(m.group(1) + " " + chatter + ": " + m.group(2) + "\n")
    return matchingLines

# list of strings to be written to file or printed
# input: list of tuples of [chatter, index]


def listBannedChatters(lines, tuples, newChatters):
    out = []
    i = 0
    for pair in tuples:
        chatter = pair[0]
        index = pair[1]

        messages = messagesFromChatterBefore(lines, chatter, index, newChatters)
        if len(messages) == 0 or (len(messages) > arg.numMessages and chatter not in newChatters):
            continue

        i += 1
        if arg.hideUsers:
            out.append("Banned Chatter #" + str(i) + "\n")
        else:
            out.append("Banned Chatter #" + str(i) + ": " + chatter + "\n")

        for line in messages:
            out.append(line)

        out.append("\n")

    return out


def listNewChatters(lines, tuples):
    out = []
    i = 0
    for pair in tuples:
        chatter = pair[0]
        index = pair[1]
        i += 1

        if arg.hideUsers:
            message = lines[index].replace(chatter, "user")
        else:
            message = lines[index]

        if arg.hideUsers:
            out.append("New Chatter #" + str(i) + "\n")
        else:
            out.append("New Chatter #" + str(i) + ": " + chatter + "\n")

        out.append(message)

        out.append("\n")
    return out


def main():
    lines = readLines(arg.input)
    chatters = []
    bannedChatters = []
    newChatters = []
    p = re.compile(r"^\[\d\d:\d\d:\d\d\] (.*) has been permanently banned. \n")
    r = re.compile(r"^\[\d\d:\d\d:\d\d\] (?:.*) banned (.*).*\n")
    # match all bans
    # p = re.compile(r"^\[\d\d:\d\d:\d\d\] (.*) has been (?:permanently banned|timed out for .*). \n")
    q = re.compile(r"^\[\d\d:\d\d:\d\d\] \[First Message\]  (.*): .*\n")
    # loop through the lines
    i = 0
    for line in lines:
        if p.match(line):
            chatter = p.match(line).group(1)
            bannedChatters.append([chatter, i])
        elif r.match(line):
            chatter = r.match(line).group(1)
            bannedChatters.append([chatter, i])
        elif q.match(line):
            chatter = q.match(line).group(1)
            newChatters.append([chatter, i])
        i += 1
    out = listBannedChatters(lines, bannedChatters, newChatters)

    if (arg.all):
        out += "\n"
        out += listNewChatters(lines, newChatters)

    # remove trailing newline if out is not empty
    if len(out) > 0:
        out.pop()

    if arg.output:
        flush(out, arg.output)
    else:
        for line in out:
            print(line, end='')


main()
