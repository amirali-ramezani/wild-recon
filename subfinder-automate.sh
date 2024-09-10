if [ -z "$1" ]; then
    echo "Usage: $0 domain"
    exit 1
fi

# Assign input domain to a variable
domain=$1

# Run subfinder with the provided domain
echo "Running subfinder for domain: $domain"
subfinder -d $domain -all 



