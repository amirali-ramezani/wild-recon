#!/bin/bash

# Check if a file containing subdomains is provided
if [ -z "$1" ]; then
    echo "Usage: $0 subdomains.txt"
    exit 1
fi

# Assign the input file to a variable
subdomain_file=$1

# Check if the file exists
if [ ! -f "$subdomain_file" ]; then
    echo "File not found!"
    exit 1
fi

# Run httpx with the input subdomain file and output the results
httpx -l "$subdomain_file" -o httpx_output.txt -sc -server -td -ip -cdn 

# Display a message that the process is complete
echo "HTTP probing completed. Results saved in httpx_output.txt"
