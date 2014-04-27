#!/usr/bin/python
# -*- coding: utf-8 -*-

import grammar

parser = grammar.CorrectionManager()


def english_join(x, conjunction='and'):
    """English-join a list of strings with a serial comma"""
    if len(x) <= 2:
        return (' %s ' % (conjunction)).join(x)
    else:
        return '%s, %s %s' % (', '.join(x[:-1]), conjunction, x[-1])


def correctBolded(units):
    ret = []
    lastCorrected = False
    i = 0
    end = len(units)
    currentCorrection = None
    while i <= end:
        if i != end and units[i].flags == 1 and units[i].original != ' ':
            if currentCorrection:
                currentCorrection = (
                    currentCorrection[0] + units[i].original, currentCorrection[1] + units[i].new_text)
            else:
                currentCorrection = (units[i].original, units[i].new_text)
        else:
            if i == end:
                if currentCorrection:
                    ret.append('~~%s~~ [**%s**]' % currentCorrection)
            else:
                if i + 1 != end and units[i + 1].flags == 1 and currentCorrection:
                    currentCorrection = (
                        currentCorrection[0] + units[i].original, currentCorrection[1] + units[i].original)
                else:
                    if currentCorrection:
                        ret.append('~~%s~~ [**%s**]' % currentCorrection)
                        currentCorrection = None
                    ret.append(units[i].original)
        i += 1
    return ''.join(ret)


def quoteLine(line):
    if line:
        return '> %s  ' % (line)
    return ''


def MakeWording(title, text, author):
    if parser.load_text(title):
        originalTitle = correctBolded(parser.sequence)
        correctedTitle = english_join(map(u'“{0}”'.format, parser.corrections))
        if parser.load_text(text):
            original = '\n'.join(
                map(quoteLine, correctBolded(parser.sequence).splitlines()))
            corrected = english_join(map(u'“{0}”'.format, parser.corrections))
            return CORRECTION_TITLE_TEXT % (author, originalTitle, original, correctedTitle, corrected)
        else:
            return CORRECTION_TITLE % (author, originalTitle, correctedTitle)
    elif parser.load_text(text):
        original = '\n'.join(
            map(quoteLine, correctBolded(parser.sequence).splitlines()))
        corrected = english_join(map(u'“{0}”'.format, parser.corrections))
        return CORRECTION_TEXT % (author, original, corrected)
    return False

CORRECTION_TITLE = """/u/%s, the Reddit Grammar Police Bot has detected an error in the title of your link:

> %s

As indicated above, we recommend that you use %s instead.
"""

CORRECTION_TITLE_TEXT = """/u/%s, the Reddit Grammar Police Bot has detected an error in the title of your link:

> %s

Additionally, we detected an error in the description of your link:

%s

As indicated above, we recommend that you use %s in the title, and for the description, we recommend %s instead.
"""

CORRECTION_TEXT = """/u/%s, the Reddit Grammar Police Bot has detected an error in the description of your link:

%s

As indicated above, we recommend that you use %s instead.
"""
