import os
import requests
import urllib.parse
import re
import datetime
import publicsuffixlist

psl = publicsuffixlist.PublicSuffixList()

LIST_FILENAME = "list.txt"
STATUS_FILENAME = "status.txt"
DOMAIN_FILENAME = "domains.txt"
OUTPUT_DIRECTORY = r"C:\Users\ASUS\Documents\uList\uList.txt"

lists = {
    "Dandelion Sprout's Anti-Malware List": "https://raw.githubusercontent.com/DandelionSprout/adfilt/master/Dandelion%20Sprout's%20Anti-Malware%20List.txt",
    "The malicious website blocklist": "https://raw.githubusercontent.com/iam-py-test/my_filters_001/main/Alternative%20list%20formats/antimalware_lite.txt",
    "iam-py-test's antitypo list": "https://raw.githubusercontent.com/iam-py-test/my_filters_001/main/antitypo.txt",
    "Actually Legitimate URL Shortener Tool": "https://raw.githubusercontent.com/DandelionSprout/adfilt/master/LegitimateURLShortener.txt",
    "HaGeZi ULTIMATE": "https://gitlab.com/hagezi/mirror/-/raw/main/dns-blocklists/adblock/tif.txt"
}

donelines = []
donedomains = []
excludes = requests.get("https://raw.githubusercontent.com/iam-py-test/allowlist/main/filter.txt").text.split("\n")
subdomains = requests.get("https://raw.githubusercontent.com/iam-py-test/tracker_analytics/main/kdl.txt").text.split("\n")
subdomains += requests.get("https://raw.githubusercontent.com/iam-py-test/my_filters_001/main/Alternative%20list%20formats/antimalware_domains.txt").text.split("\n")
subdomains += requests.get("https://raw.githubusercontent.com/iam-py-test/cloudflare-usage/main/cnames.txt").text.split("\n")

is_ip_v4 = r"^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"
is_ip_v6 = "((([0-9a-fA-F]){1,4})\\:){7}"\
             "([0-9a-fA-F]){1,4}"
is_ip_v4_reg = re.compile(is_ip_v4)
is_ip_v6_reg = re.compile(is_ip_v6)


def isipdomain(domain):
    if re.search(is_ip_v4_reg, domain):
        return True
    if re.search(is_ip_v6_reg, domain):
        return True
    return False


def extdomain(line):
    try:
        domain = ""
        if line.startswith("||") and line.endswith("^$all"):
            domain = line[2:-5]
        # ... (rest of the extdomain function)

        return domain
    except:
        return ""


mainlist_header = """! Title: uList
! Description: The useless List
! Script last updated: 22/11/2023
! Last updated: {}
! Homepage: https://github.com/DrQuackster/uList
! License: https://github.com/DrQuackster/uList/blob/master/LICENSE.md
! Syntax: Adblock Plus Filter List
! Maintainer: Dr. Duckenstein
! Contact: drduckenstein@protonmail.com

""".format(datetime.date.today().strftime("%d/%m/%Y"))

eadd = 0
ered = 0
parselist = None # type: ignore


def parselist(lines, curl=""):
    global donedomains
    global donelines
    global eadd
    global ered
    plist = ""
    for line in lines:
        if (line.startswith("!") or line.startswith("#")) and "include" not in line:
            continue
        elif line.startswith("[Adblock") and line.endswith("]"):
            continue
        elif line in donelines:
            ered += 1
        elif line in excludes:
            continue
        elif line == "":
            continue
        elif extdomain(line) != "" and extdomain(line) in donedomains:
            continue
        elif line.startswith("!#include "):
            try:
                incpath = urllib.parse.urljoin(curl, line[10:], allow_fragments=True)
                inccontents = requests.get(incpath).text.replace("\r", "").split("\n")
                endcontents = parselist(inccontents, incpath)
                plist += "{}\n".format(endcontents)
            except Exception as err:
                print(line, err)
        else:
            plist += "{}\n".format(line)
            eadd += 1
            donelines.append(line)
            edomain = extdomain(line)
            if edomain != "" and edomain != " ":
                donedomains.append(edomain)
    return plist


for clist in lists:
    list_url = lists[clist]
    list_content = requests.get(list_url).text.split("\n")
    mainlist_header += parselist(list_content, list_url)

with open(OUTPUT_DIRECTORY, "w", encoding="UTF-8") as f:
    f.write(mainlist_header)

justdomains = [d for d in donedomains if "/" not in d and "." in d and "*" not in d and d != "" and not d.endswith(".") and not isipdomain(d)]

with open(DOMAIN_FILENAME, "w", encoding="UTF-8") as f:
    f.write("\n".join(justdomains))

subsfound = 0
domainplussub = justdomains
for sub in subdomains:
    try:
        maindomain = psl.privatesuffix(sub)
        if maindomain in domainplussub and sub not in domainplussub:
            subsfound += 1
            domainplussub.append(sub)
    except Exception as err:
        print(err, sub)

with open("domains_subdomains.txt", "w", encoding="UTF-8") as f:
    f.write("\n".join(justdomains))

with open(STATUS_FILENAME, 'w') as status:
    status.write("""Stats:
{} entries added
{} redundant entries removed
{} domains added
{} subdomains added
""".format(eadd, ered, len(donedomains), subsfound))
