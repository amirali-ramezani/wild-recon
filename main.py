import subprocess

# Function to run a bash script with domain input and capture its output
def run_bash_script(script, domain):
    try:
        # Run the bash script with domain as an argument and capture the output
        result = subprocess.run(['bash', script, domain], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        # Return the output (stdout)
        return result.stdout
    except Exception as e:
        print(f"Error running {script}: {e}")
        return ""

# Function to save subdomains to a file
def save_to_file(filename, data):
    with open(filename, 'w') as f:
        f.write(data)

# Function to remove duplicate subdomains from a file
def remove_duplicates(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()

    # Remove duplicates by converting to a set, then sorting the set
    unique_lines = sorted(set([line.strip() for line in lines]))

    # Write the unique subdomains back to the file
    with open(filename, 'w') as f:
        for line in unique_lines:
            f.write(f"{line}\n")

# Main function to run the recon process
def main():
    # Get the domain from the client (user input)
    domain = input("Enter the domain for recon: ")

    # Run each bash script with the client domain input and capture the subdomains
    output1 = run_bash_script('amass-brute-sub.sh', domain)
    output2 = run_bash_script('amass-sub-enum.sh', domain)
    output3 = run_bash_script('subfinder-automate.sh', domain)

    # Combine all the outputs from the three bash scripts
    combined_output = output1 + output2 + output3

    # Save the combined output to a file
    save_to_file('subdomains.txt', combined_output)

    # Remove duplicate subdomains from the file
    remove_duplicates('subdomains.txt')

    # Forward the unique subdomains to another bash script
    subprocess.run(['bash', 'httpx.sh', 'subdomains.txt'])

if __name__ == "__main__":
    main()
