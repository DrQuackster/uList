filter_lists = [
  'https://big.oisd.nl/'
  'https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/fakenews-gambling/readme.md'
  'https://gitlab.com/hagezi/mirror/-/raw/main/dns-blocklists/adblock/tif.txt'
  'https://gitlab.com/hagezi/mirror/-/raw/main/dns-blocklists/adblock/ultimate.txt'
  'https://gitlab.com/hagezi/mirror/-/raw/main/dns-blocklists/adblock/gambling.txt'
  'https://raw.githubusercontent.com/iam-py-test/uBlock-combo/main/list.txt'
  'https://gitlab.com/hagezi/mirror/-/raw/main/dns-blocklists/adblock/spam-tlds-ublock.txt'
  'https://gitlab.com/hagezi/mirror/-/raw/main/dns-blocklists/adblock/whitelist.txt'
  # Add more filter list URLs as needed
]

merged_rules = []

for url in filter_lists:
    response = requests.get(url)
    if response.status_code == 200:
        merged_rules.extend(response.text.split('\n'))

with open('merged_filterlist.txt', 'w') as merged_file:
    merged_file.write('\n'.join(merged_rules))