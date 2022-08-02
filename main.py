#!/bin/python3
import regex as re
import argparse
parser = argparse.ArgumentParser(description='Parse Chatterino logs and create a list of users who were permabanned after sending a small number of recent messages. These users might be hoppers.')

parser.add_argument("-i", "--input", help="(required) the file to read", type=str, required=True)
parser.add_argument("-o", "--output", help="the file to write to (if unset, print to stdout)", type=str)
parser.add_argument("--hideUsers", help="hide usernames", action="store_true")
parser.add_argument("--numMessages", help="(default: 5) the maximum number of recent messages before a chatter is considered 'not a hopper'", type=int, default=5)
parser.add_argument("--recentLength", help="(default: 500) the number of messages to check prior to each permaban", type=int, default=500)

arg = parser.parse_args()

# read lines from file
def readLines(file):
    # open the file
    f = open(file, "r")
    # read the file
    lines = f.readlines()
    # close the file
    f.close()
    return lines

# write lines to file
def flush(lines, file):
    f = open(file, "w")
    for line in lines:
        f.write(line)
    f.close()

# list of all lines sent by chatter
def messagesFromChatter(lines, chatter):
    p = re.compile(r"^(\[\d\d:\d\d:\d\d\])  " + chatter + ": (.*)\n")
    # create a list to store the matching lines
    matchingLines = []
    # loop through the lines
    for line in lines:
        m = p.match(line)
        # if the line matches the regex
        if m:
            if arg.hideUsers:
                chatter = "chatter"
            # add the line to the list
            matchingLines.append(m.group(1) + " " + chatter + ": " + m.group(2) + "\n")
    return matchingLines

# output string to be written to file or printed
def buildOutput(list, hideUsers=True):
    out = []

    info = "This is a list of chatters who were permabanned after sending at most " + str(arg.numMessages) + " messages out of the last " + str(arg.recentLength) + " lines.\n"
    if hideUsers:
        info += "The names of the chatters are hidden.\n"

    info += "\n"
    out.append(info)

    i = 0
    for pair in list:
        chatter = pair[0]
        messages = pair[1]
        i += 1
        if hideUsers:
            out.append("Chatter #" + str(i) + "\n")
        else:
            out.append("Chatter #" + str(i) + ": " + chatter + "\n")

        for line in messages:
            out.append(line)

        out.append("\n")


    # remove trailing newline
    out.pop()
    return out

def main():
    lines = readLines(arg.input)
    # create an empty array
    chatters = []
    p = re.compile(r"^\[\d\d:\d\d:\d\d\] (.*) has been permanently banned. \n")
    # loop through the lines
    i = 0
    numchatters = 0
    for line in lines:
        i += 1
        m = p.match(line)
        if m:
            chatter = m.group(1)

            # all messages in the last 500 total lines
            start = max(i-arg.recentLength, 0)
            recentMessages = lines[start:i]

            # messages sent by the chatter
            chatterMessages = messagesFromChatter(recentMessages, chatter)

            # the chatter sent at most 5 recent messages before being permabanned, probably a chatter
            if 0 < len(chatterMessages) <= arg.numMessages:
                chatters.append([chatter, chatterMessages])

    out = buildOutput(chatters, arg.hideUsers)

    if arg.output:
        flush(out, arg.output)
    else:
        for line in out:
            print(line, end='')

main()
