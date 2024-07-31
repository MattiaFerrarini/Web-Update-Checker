'''
This is a simple Python script that can be used to monitor websites of interest and
be notified of changes to them. It probably doesn't work for website that load content 
dynamically. In this case, the websites will always appear to have been updated.

The urls of the websites should be written in 'urls_file', each on a separate line without
any formatting (especially not tabs). 

The script works by getting the content of each website listed in 'urls_file'
and computing the hash of it. If the hash differs from a previously computed and
saved one, the user is notified of the website's modification. The computed hashes are
memorized in urls.txt, on the same line of the corresponding url.

The user is also notified of errors encountered during the process, i.e. lines of urls.txt 
that could not be parsed and urls for which it was not possible to compute the hash.
Error logs are stored in 'errors_file' in the working directory.

The user is notified via the os notification system.
'''

import requests
from plyer import notification
import hashlib
import os
import subprocess
from datetime import datetime


urls_file = "urls.txt" # the file containing the urls (and hashes) that will be monitored
errors_file = "errors.txt" # the file that will contain logs for potential errors


'''
Parses the urls_file, returning three lists:
one with urls, one with hashes and one with the lines that couldn't be parsed.
'''
def parse_urls_file():
    urls, hashes, errors = [], [], []

    with open(urls_file, "r") as fin:
        for line in fin:
            try:
                parts = line.strip().split('\t')
                
                if len(parts) == 2:
                    url, hash = parts[0].strip(), parts[1].strip()
                else:
                    url, hash = parts[0].strip(), None

                urls.append(url)
                hashes.append(hash)
            except:
                errors.append(line)
                print(f"An error occurred parsing line: {line}")

    return urls, hashes, errors


'''
Updates the hashes for all urls. Returns the updated list of hashes,
a list of urls whose associated hashes have been updated and a list of urls 
for which hash computation resulted in an error.
'''
def update_hashes(urls, hashes):
    updated, errors = [], []

    for i in range(0, len(urls)):
        try:
            response = requests.get(urls[i])
            new_hash = hashlib.sha256(response.text.encode('utf-8')).hexdigest()
            if hashes[i] == None or new_hash != hashes[i]:
                hashes[i] = new_hash
                updated.append(urls[i])
        except requests.RequestException as e:
            print(f"An error occurred: {e}")
            errors.append(urls[i])

    return hashes, updated, errors


'''
Notifies the user of updates and errors found while checking for modifications to 
the specified urls. The os notification system is used.
'''
def notify_updates(checked, updated, unparsed, errors):
    # notify updates
    if len(updated) > 0:
        updated_str = "The following urls have been updated:\n" + '\n'.join(updated)
        subprocess.run(['notify-send', "Website Update Report", updated_str])

    # notify errors
    if len(unparsed) + len(errors) > 0:

        title = "Errors when checking website updates"
        message = f"Some urls could not be checked. Please see the file error.txt in {os.getcwd()}."
        subprocess.run(['notify-send', title, message])

        checked_str = "The following urls where checked for updates:\n" + '\n'.join(checked)
        unparsed_str = f"The following lines in {urls_file} could not be parsed:\n" + '\n'.join(unparsed)
        errors_str = f"Checking the following urls resulted in error:\n" + '\n'.join(errors)

    with open(errors_file, 'a') as fout:
        fout.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n\n")
        fout.write(checked_str + "\n\n")
        fout.write(updated_str + "\n\n")
        fout.write(unparsed_str + "\n\n")
        fout.write(errors_str + "\n")
        fout.write("-------------------\n")
        


'''
Saves the newly computed hashes to urls_file.
'''
def update_urls_file(urls, hashes):
    with open(urls_file, "w") as fout:
        for i in range(len(urls)):
            if hashes[i] != None:
                fout.write(urls[i] + "\t" + hashes[i] + "\n")
            else:
                fout.write(urls[i] + "\n")


'''
Main function of the script. It parses the urls_file to get the urls of interested and,
if present, the saved hashes. It then computes a new hash for all urls. If differences 
are found between the new hash and the saved one, the user is notified about an update
to the associated website. The user is also notified of errors encountered during the process.
Finally, the newly computed hashes are saved.
'''
def checkForUpdates():
    urls, hashes, unparsed = parse_urls_file()

    hashes, updated, errors = update_hashes(urls, hashes)

    notify_updates(urls, updated, unparsed, errors)

    update_urls_file(urls, hashes)


if __name__ == "__main__":
    checkForUpdates()
    print("Update check concluded successfully.")