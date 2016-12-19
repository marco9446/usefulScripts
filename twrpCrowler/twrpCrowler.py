from lxml import html
import requests
import tokens
from pathlib import Path
from pushbullet import Pushbullet


pb = Pushbullet(tokens.PUSHBULLET_AUTH_TOKEN)
link = "https://dl.twrp.me/oneplus3/"
page = requests.get(link)
tree = html.fromstring(page.content)
filename = "twrpVersionsOP3.txt"
my_file = Path(filename)


def writeOnFile(value="", doErase=False):
    fl = open(filename, "w")
    if doErase:
        fl.truncate()
    fl.write(value)
    fl.close()


# parse the page in search of all "a" tags and retrive the first one containg
# the extension ".img"
links = tree.cssselect("a")
lastTwrp = ""
for i in links:
    if ".img" in i.text_content():
        lastTwrp = i.text_content()
        break

if my_file.is_file():
    twrpOld = open(filename, 'r').read().split('\n')
    if len(twrpOld) > 0 and twrpOld[0] != lastTwrp and "twrp" in twrpOld[0]:
        push = pb.push_link("New TWRP version: "+lastTwrp, link)
    writeOnFile(lastTwrp, True)
else:
    writeOnFile(lastTwrp)
