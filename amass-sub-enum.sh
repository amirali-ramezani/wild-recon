#!/usr/bin/env fish

# Check if the domain argument is provided
if test (count $argv) -lt 1
    echo "Usage: $argv[0] domain"
    exit 1
end

# Assign input domain to a variable
set domain $argv[1]

# Print a message to indicate the process is starting
echo "Running amass enumeration for subdomains on: $domain"

# Run amass enumeration and extract only subdomains
amass enum -d $domain | grep -Eo "([a-zA-Z0-9-]+\.)+$domain" | sort -u

# End of script
