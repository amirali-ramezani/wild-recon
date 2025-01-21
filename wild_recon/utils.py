from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
import os
import subprocess
import re


class SubdomainFinderBasic:
    @staticmethod
    def find_subdomains(domain):
        try:
            amass_bin = os.path.join(settings.MEDIA_ROOT, 'amass.exe') 
            subfinder_bin = os.path.join(settings.MEDIA_ROOT, 'subfinder.exe')  

            if not os.path.exists(amass_bin) or not os.path.exists(subfinder_bin):
                return None, "amass or subfinder binaries not found in media folder"

            # Run amass
            amass_command = [amass_bin, 'enum', '-brute', '-min-for-recursive', '2', '-d', domain]
            amass_process = subprocess.Popen(amass_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            amass_stdout, amass_stderr = amass_process.communicate()

            if amass_stderr:
                print(f"Amass Error: {amass_stderr}")

            # Run subfinder
            subfinder_command = [subfinder_bin, '-d', domain, '-all']
            subfinder_process = subprocess.Popen(subfinder_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            subfinder_stdout, subfinder_stderr = subfinder_process.communicate()

            if subfinder_stderr:
                print(f"Subfinder Error: {subfinder_stderr}")

            # Combine results
            combined_result = amass_stdout + "\n" + subfinder_stdout

            # Extract unique subdomains
            # Adjusted regex to include the full domain
            subdomains = re.findall(rf"([a-zA-Z0-9-]+\.)*{re.escape(domain)}", combined_result)
            unique_subdomains = sorted(set(subdomains))

            # Debug output
            print(f"Unique Subdomains: {unique_subdomains}")
            return unique_subdomains, None
        except Exception as e:
            return None, str(e)