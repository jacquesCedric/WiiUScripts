#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "Jacob Gold"
__copyright__ = "Copyright 2007, Jacob Gold"
__credits__ = ["Jacob Gold"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Jacob Gold"
__status__ = "Prototype"

"""
   Generating 1stNUP.xml files for use with Nintendo Wii U's Wara Wara Plaza
"""

from lxml import etree

def generateBase():
    root = etree.Element('result')
    version = subElementWithText(root, 'version', "1")
    has_error = subElementWithText(root, 'has_error', "0")
    request_name = subElementWithText(root, 'request_name', "topics")
    expire = subElementWithText(root, 'expire', "2100-01-01 10:00:00")

    # the meat
    topics = etree.SubElement(root, 'topics')

    for x in range(0,10):
        t1 = generateTopic(dummyicon, dummyID + x, dummyName + str(x))
        topics.append(t1)

    return root


def generateTopic(icon, titleID, name):
    topic = etree.Element('topic')
    iconfield = subElementWithText(topic, 'icon', icon)
    titleid = subElementWithText(topic, 'title_id', str(titleID))
    communityid = subElementWithText(topic, 'community_id', "4294967295")
    isrecommended = subElementWithText(topic, 'is_recommended', "0")
    namefield = subElementWithText(topic, 'name', name)
    participantcount = subElementWithText(topic, 'participant_count', "0")

    # Add people
    people = etree.SubElement(topic, "people")
    people.text = "" #dummy

    # End add people
    empathyCount = subElementWithText(topic, "empathy_count", "0")
    hasShopPage = subElementWithText(topic, "has_shop_page", "0")
    modifiedAt = subElementWithText(topic, "modified_at", "2012-04-23 06:35:47")
    position = subElementWithText(topic, "position", "2")

    return topic
    

def generatePerson():
    print("not implemented yet")

def generateTextPost(text):
    print("not implemented yet")

def generateImagePost(image):
    print("not implemented yet")

# Makes one-offs easier
def subElementWithText(root, tag, content):
    node = etree.SubElement(root, tag)
    node.text = content
    return node

base = generateBase()
tree = etree.ElementTree(base)
with open('1stNUP.xml', 'wb') as f:
    f.write(etree.tostring(tree, pretty_print=True, xml_declaration=True, encoding='UTF-8'))