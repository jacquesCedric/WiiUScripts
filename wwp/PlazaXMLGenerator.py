#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "Jacob Gold"
__copyright__ = "Copyright 2021, Jacob Gold"
__credits__ = ["Jacob Gold"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Jacob Gold"
__status__ = "Prototype"

"""
   Generating 1stNUP.xml files for use with Nintendo Wii U's Wara Wara Plaza
"""

from lxml import etree
import collections
import random

messages = []
ids = []
communityid = 4294967295 #this is random, but they need to be unique for each topic

# Process all the data we've been collating from discord
def grabContent():
    m_common = []
    raw_messages = []

    # First we process messages
    with open("text/msg.txt") as f:
        for line in f:
            raw_messages.append(line.strip())

    for i in list(chunks(raw_messages, 10)):
        messages.append(i)

    # Then votes
    with open("text/vote.txt") as f:
        split = f.read().split()
        counts = collections.Counter(split)
        m_common = counts.most_common(10)

    # Lets refine those votes and get some details
    for tup in m_common:
        ids.append(detailsFromID(tup[0]))


def generateBase():
    root = etree.Element('result')
    version = subElementWithText(root, 'version', "1")
    has_error = subElementWithText(root, 'has_error', "0")
    request_name = subElementWithText(root, 'request_name', "topics")
    expire = subElementWithText(root, 'expire', "2100-01-01 10:00:00")

    # the meat
    topics = etree.SubElement(root, 'topics')

    for x in range(0,len(ids)):
        icon = ""

        t = ids[x]
        s = t.split(';')

        with open("images/data/" + s[0]) as i:
            icon = i.read()

        t1 = generateTopic(icon, s[0], 4294967295 + x, s[1], messages[x])
        topics.append(t1)

    return root


def generateTopic(icon, titleID, commID, name, msgs):
    topic = etree.Element('topic')
    iconfield = subElementWithText(topic, 'icon', icon)
    titleid = subElementWithText(topic, 'title_id', str(titleID))
    communityid = subElementWithText(topic, 'community_id', str(commID))
    isrecommended = subElementWithText(topic, 'is_recommended', "0")
    namefield = subElementWithText(topic, 'name', name)
    participantcount = subElementWithText(topic, 'participant_count', "0")

    # Add people
    people = etree.SubElement(topic, "people")

    for message in msgs:
        person = generatePerson(titleID, message, commID)
        people.append(person)

    # End add people
    empathyCount = subElementWithText(topic, "empathy_count", "0")
    hasShopPage = subElementWithText(topic, "has_shop_page", "0")
    modifiedAt = subElementWithText(topic, "modified_at", "2019-04-23 06:35:47")
    position = subElementWithText(topic, "position", "2")

    return topic
    

def generatePerson(titleID, message, communityid):
    s = message.split(';;')

    person = etree.Element('person')
    posts = generateTextPost(titleID, s[1], s[2], s[0], communityid)

    person.append(posts)

    return person

def generateTextPost(titleID, text, author, time, communityid):
    posts = etree.Element('posts')
    post = etree.SubElement(posts, 'post')

    body = subElementWithText(post, 'body', text)
    communityid = subElementWithText(post, 'community_id', str(communityid))
    countryid = subElementWithText(post, 'country_id', "110")
    createdat = subElementWithText(post, 'created_at', str(time))
    feelingid = subElementWithText(post, 'feeling_id', "1")
    postid = subElementWithText(post, 'id', "AYMHAAADAAADV44piZWWdw")
    autopost = subElementWithText(post, 'is_autopost', "0")
    commprivate = subElementWithText(post, 'is_community_private_autopost', "0")
    spoiler = subElementWithText(post, 'is_spoiler', "0")
    jumpy = subElementWithText(post, 'is_app_jumpable', "0")
    empathy =subElementWithText(post, 'empathy_count', "5")
    lang = subElementWithText(post, 'language_id', "1")
    mii = subElementWithText(post, 'mii', randomMii())
    face = subElementWithText(post, 'mii_face_url', "")
    number = subElementWithText(post, 'number', "0")
    pid = subElementWithText(post, 'pid', "")
    platf = subElementWithText(post, 'platform_id', "1")
    region = subElementWithText(post, 'region_id', "4")
    reply = subElementWithText(post, 'reply_count', "0")
    screen = subElementWithText(post, 'screen_name', author)
    titleid = subElementWithText(post, 'title_id', str(titleID))

    return posts



def generateImagePost(image):
    print("not implemented yet")


# Helper functions
# Grab details using a titleID
def detailsFromID(titleID):
    with open("text/titleinfo.txt") as f:
        for line in f:
            if line[8:16] == titleID[8:16]:
                return line.strip()
    return 0


# Syntactic sugar for etree stuff
def subElementWithText(root, tag, content):
    node = etree.SubElement(root, tag)
    node.text = content
    return node

# Grab a random mii, needs to be refined
def randomMii():
    with open("text/miiArray.txt") as f:
        line = next(f)
        for num, aline in enumerate(f, 2):
            if random.randrange(num):
                continue
            line = aline
        return line

# Divide list into n equal-ish groups
def chunks(seq, size):
    return (seq[i::size] for i in range(size))


#  Main script
def main():
    grabContent()
    base = generateBase()
    tree = etree.ElementTree(base)
    with open('1stNUP.xml', 'wb') as f:
        f.write(etree.tostring(tree, pretty_print=True, xml_declaration=True, encoding='UTF-8'))

if __name__ == "__main__":
    main()
