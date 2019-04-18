"""
Kurt Weatherford
3/17/2019
Web Scraping program to track the appointments of high level UN staff
"""

from bs4 import BeautifulSoup
import requests


def getdate(appt):
    ogdate = appt.find("div", class_="views-field-field-dated")
    brokenogdate = ogdate.text.split()
    wordmonth = brokenogdate[1]
    if wordmonth == "January":
        brokenogdate[1] = "1"
    elif wordmonth == "February":
        brokenogdate[1] = "2"
    elif wordmonth == "March":
        brokenogdate[1] = "3"
    elif wordmonth == "April":
        brokenogdate[1] = "4"
    elif wordmonth == "May":
        brokenogdate[1] = "5"
    elif wordmonth == "June":
        brokenogdate[1] = "6"
    elif wordmonth == "July":
        brokenogdate[1] = "7"
    elif wordmonth == "August":
        brokenogdate[1] = "8"
    elif wordmonth == "September":
        brokenogdate[1] = "9"
    elif wordmonth == "October":
        brokenogdate[1] = "10"
    elif wordmonth == "November":
        brokenogdate[1] = "11"
    elif wordmonth == "December":
        brokenogdate[1] = "12"
    brokendate = [brokenogdate[1], brokenogdate[0], brokenogdate[2]]
    date = "/".join(brokendate)
    return date

def getname(appt):
    summary = appt.find("div", class_="views-field-body")
    headline = appt.find("div", class_="views-field-title")
    brokenheadline = headline.text.split()
    brokensummary = summary.text.split()
    if "appointment" in brokensummary and brokensummary[brokensummary.index("appointment")+1] == "of":
        index = brokensummary.index("appointment") + 2
        brokenname = []
        while brokensummary[index] != "of" and brokensummary[index] != "as" and brokensummary[index] != "to":
            brokenname.append(brokensummary[index])
            index = index+1
        name = " ".join(brokenname)
    elif "elected" in brokensummary:
        index = brokensummary.index("elected")+1
        brokenname = []
        while brokensummary[index] != "of":
            brokenname.append(brokensummary[index])
            index = index+1
        name = " ".join(brokenname)
    elif "Nominates" in brokenheadline:
        index = brokenheadline.index("Nominates") + 1
        brokenname = []
        while brokenheadline[index] != "of":
            brokenname.append(brokenheadline[index])
            index = index + 1
        name = " ".join(brokenname)
    elif "appointed" in brokensummary:
        index = brokensummary.index("appointed") + 1
        brokenname = []
        while brokensummary[index] != "of" and brokensummary[index] != "as":
            brokenname.append(brokensummary[index])
            index = index + 1
        name = " ".join(brokenname)
    elif "reappointed" in brokensummary:
        index = brokensummary.index("reappointed") + 1
        brokenname = []
        while brokensummary[index] != "of":
            brokenname.append(brokensummary[index])
            index = index + 1
        name = " ".join(brokenname)
    else:
        name = "NONE"
    return name

def getnation(appt, name):
    headline = appt.find("div", class_="views-field-title")
    brokenheadline = headline.text.split()
    summary = appt.find("div", class_="views-field-body")
    brokensummary = summary.text.split()
    if "Appoints" in brokenheadline or "Nominates" in brokenheadline or "Elects" in brokenheadline or "Reappoints" \
    in brokenheadline or "Appointed" in brokenheadline or "Appoint" in brokenheadline or "appoints" in brokenheadline:
        brokenname = name.split()
        lastname = brokenname[len(brokenname)-1]
        index = brokensummary.index(lastname) + 1
        if brokensummary[index] == "of":
            index = index + 1
            brokennation = []
            while brokensummary[index] != "as" and brokensummary[index] != "to" and brokensummary[index] != "Chair"\
                and brokensummary[index] != "President" and brokensummary[index] != "next":
                brokennation.append(brokensummary[index])
                index = index+1
            nation = " ".join(brokennation)
        else:
            nation = "NONE"
    else:
        nation = "NONE"
    return nation

def getpositiontype(appt):
    headline = appt.find("div", class_="views-field-title")
    brokenheadline = headline.text.split()
    if brokenheadline[1] == "Appoints" or brokenheadline[1] == "Designates" or brokenheadline[1] == "Announces" or \
    brokenheadline[1] == "appoints" or "Appointed" in brokenheadline or "Appoint" in brokenheadline:
        positiontype = "Appointed"
    elif brokenheadline[1] == "Nominates" or brokenheadline[1] == "Elects":
        positiontype = "Elected"
    elif brokenheadline [1] == "Reappoints":
        positiontype = "Reappointed"
    else:
        positiontype = "???"
    return positiontype

def getterm(appt, nation):
    summary = appt.find("div", class_="views-field-body")
    brokensummary = summary.text.split()
    if "term" in brokensummary:
        brokennation = nation.split()
        index = brokensummary.index(brokennation[len(brokennation)-1])+3
        brokenterm = []
        while brokensummary[index] != "term":
            brokenterm.append(brokensummary[index])
            index = index+1
        term = " ".join(brokenterm)
    else:
        term = "NONE"
    return term

def getposition(appt, nation):
    summary = appt.find("div", class_="views-field-body")
    brokensummary = summary.text.split()
    brokennation = nation.split()
    lastword = brokennation[len(brokennation)-1]
    brokenposition = []
    if lastword == "NONE":
        position = "????"
    elif brokensummary[brokensummary.index(lastword)+1] == "as":
        index = brokensummary.index(lastword)+2
        while brokensummary[index] != "bitch":
            brokenposition.append(brokensummary[index])
            if index == len(brokensummary)-1 or "." in list(brokensummary[index]):
                break
            else:
                index = index+1
        position = " ".join(brokenposition)
    else:
        position = "????"
    return position

def main():
    page = 0
    while page < 11:
        url = "https://www.un.org/press/en/content/appointments?page=" + str(page)
        source = requests.get(url).text
        soup = BeautifulSoup(source, "html.parser")
        appts = soup.findAll("div", class_="views-row")
        for appt in appts:
            name = getname(appt)
            if name == "NONE":
                nation = "NONE"
                positiontype = "NONE"
                term = "NONE"
                date = "NONE"
                position = "NONE"
            else:
                date = getdate(appt)
                nation = getnation(appt, name)
                positiontype = getpositiontype(appt)
                term = getterm(appt, nation)
                position = getposition(appt, nation)
            print(name + ", " + nation + ", " + date + ", " + positiontype + ", " + term + ", " + position)
        page = page+1

main()
