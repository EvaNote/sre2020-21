import json
import requests
import csv

# GitHub Authentication function
def github_auth(url, lsttoken, ct):
    jsonData = None
    try:
        ct = ct % len(lstTokens)
        headers = {'Authorization': 'Bearer {}'.format(lsttoken[ct])}
        request = requests.get(url, headers=headers)
        jsonData = json.loads(request.content)
        ct += 1
    except Exception as e:
        pass
        print(e)
    return jsonData, ct


def authorsFileTouches(lsttokens, repo):
    ipage = 1  # url page counter
    ct = 0  # token counter

    try:
        # loop though all the commit pages until the last returned empty page
        while True:
            spage = str(ipage)
            commitsUrl = 'https://api.github.com/repos/' + repo + '/commits?page=' + spage + '&per_page=100'
            jsonCommits, ct = github_auth(commitsUrl, lsttokens, ct)

            # break out of the while loop if there are no more commits in the pages
            if len(jsonCommits) == 0:
                break
            # iterate through the list of commits in  spage
            for shaObject in jsonCommits:
                sha = shaObject['sha']
                # For each commit, use the GitHub commit API to extract the files touched by the commit
                shaUrl = 'https://api.github.com/repos/' + repo + '/commits/' + sha
                shaDetails, ct = github_auth(shaUrl, lsttokens, ct)
                filesjson = shaDetails['files']
                commitObj = shaDetails['commit']
                authorObj = commitObj['author']
                author = authorObj['name']
                date = authorObj['date']
                for filenameObj in filesjson:
                    filename = filenameObj['filename']
                    if filename[-5:] != '.java':
                        continue
                    dictfiles[filename] = author
                    print(filename, ':', author, ', ', date)
            ipage += 1
    except:
        print("Error receiving data")
        exit(0)

                    #print(author)

repo = 'scottyab/rootbeer'

lstTokens = [""]

dictfiles = dict()
authorsFileTouches(lstTokens, repo)
