#!/bin/bash

# GitHub repository information
repo_user="DrQuackster"
repo_name="uList"
repo_url="https://github.com/DrQuackster/uList.git"
repo_token="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"

# Metadata for uList.txt
metadata="
! Title: uList
! Description: useless List
! Last modified: $(date +"%Y-%m-%d")
! Expires: 1 day
! Homepage: https://github.com/DrQuackster/uList
! License: https://github.com/DrQuackster/uList/blob/main/LICENSE
! Syntax: Adblock Plus Filter List
! Maintainer: Dr. Duckenstein
! Contact: drduckenstein@protonmail.com
"

# Initialize an array with the URLs of the filter lists
filter_lists=(
  "https://big.oisd.nl/"
  "https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/fakenews-gambling/readme.md"
  "https://gitlab.com/hagezi/mirror/-/raw/main/dns-blocklists/adblock/tif.txt"     
  "https://gitlab.com/hagezi/mirror/-/raw/main/dns-blocklists/adblock/ultimate.txt"
  "https://gitlab.com/hagezi/mirror/-/raw/main/dns-blocklists/adblock/gambling.txt"
  "https://raw.githubusercontent.com/iam-py-test/uBlock-combo/main/list.txt"
  "https://gitlab.com/hagezi/mirror/-/raw/main/dns-blocklists/adblock/spam-tlds-ublock.txt"
)

# Create a directory for storing the filter list file
output_dir="~/uList"
mkdir -p "$output_dir"

# Download and concatenate the filter lists
for url in "${filter_lists[@]}"; do
  curl -sSL "$url" >> "$output_dir/uList_temp.txt"
done

# Remove metadata from the previous uList.txt and add new metadata
grep -v '^!' "$output_dir/uList_temp.txt" > "$output_dir/uList.txt"
echo "$metadata" | cat - "$output_dir/uList.txt" > "$output_dir/uList_temp.txt"
mv "$output_dir/uList_temp.txt" "$output_dir/uList.txt"

# Remove duplicate lines in the merged filter list
sort -u "$output_dir/uList.txt" -o "$output_dir/uList.txt"

# Commit and push changes to the GitHub repository using the token
cd "$output_dir"
git init
git add uList.txt
git commit -m "Update uList.txt"
git remote add origin "$repo_url"
git push -u origin master

# Clean up temporary files and directories
rm -rf "$output_dir"