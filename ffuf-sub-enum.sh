#!/usr/bin/env fish

# Check if the domain argument is provided
if test (count $argv) -lt 1
    echo "Usage: $argv[0] domain"
    exit 1
end

set domain $argv[1]

echo "ffuf is runing on : $domain"

ffuf -u https://FUZZ.$domain -w /home/amirali/hunttool/word-list/param.txt