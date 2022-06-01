#requires python3
#creates an output called hcsSS_developerRetention.txt
#git log --pretty="%ce|%ci"
import subprocess, os
from datetime import date, datetime

#remove duplicate committers in a array
def remove_duplicates(original):
    unique = []
    [unique.append(n) for n in original if n not in unique]
    return(unique)

if os.path.exists("Projectnamesforanalysis.txt"):
    
    #remove codeContributors file to start a new one
    if os.path.exists("hcsSS_developerRetention.txt"):
        os.remove("hcsSS_developerRetention.txt")


    with open("Projectnamesforanalysis.txt") as projectFolders:
        for projectFolder in projectFolders:
            currentDir = os.getcwd()
            os.chdir(currentDir+"/"+projectFolder.rstrip())            


            with open("hcsSS_developerRetention.txt", "a") as external_file:
                add_text = "project|developerRetention"
                external_file.write(add_text)
                external_file. write("\n")
                external_file.close()    
                    
            #get all committers and dates into a file called commitsDate.txt
            commitsDate = open("commitsDate.txt", "w")
            #ce: committer email ci: commit date
            pretty = '--pretty="%ce|%ct"'
            subprocess.call(["git", "log", "--pretty=", pretty], stdout=commitsDate)

            #get project name
            #projectName = subprocess.check_output(["git", "remote", "get-url", "origin"])
            getCommand = "--get"
            projectName = subprocess.check_output(["git", "config", getCommand, "remote.origin.url"])
            projectName = str(projectName.rstrip())
            # projectName = projectName.replace("b'https://github.com/","")
            if (projectName.find('https') != -1):
                projectName = projectName.replace("b'https://github.com/","")
            elif (projectName.find('http') != -1):
                projectName = projectName.replace("b'http://github.com/","")
            
            projectName = projectName.replace(".git'","")

            # A developer retention is defined as a developer
            # that has a commit within the last 180 days and
            # had at least one commit before these 180 days
            committersUntil180DaysAgo = []
            committersBefore180DaysAgo = []

            #variable to identify the last commit date
            first = True

            with open("commitsDate.txt", errors='ignore') as external_file_commitsDates:
                for line in external_file_commitsDates:
                    #get committers and dates
                    lineFormated = str(line.rstrip())
                    lineFormated = lineFormated.replace('"','')
                    committer, commitDate = lineFormated.split('|')
                    
                    #calcultate how many days this commit was created        
                    if first:
                        firstCommitDate = commitDate
                        first = False
                    days = (int(firstCommitDate)-int(commitDate))/(60*60*24)
                    
                    if days <= 180:            
                        committersUntil180DaysAgo.append(committer)
                    else:
                        committersBefore180DaysAgo.append(committer)
                    
                external_file_commitsDates.close()

            #remove duplicated committers in both arrays
            committersUntil180DaysAgo = remove_duplicates(committersUntil180DaysAgo)
            committersBefore180DaysAgo = remove_duplicates(committersBefore180DaysAgo)

            with open("hcsSS_developerRetention.txt", "a") as external_file:
                if len(committersUntil180DaysAgo) == 0:
                    add_text = str(projectName) + "|0" 
                else:
                    retention = 0
                    
                    #count how many committers are in both arrays
                    for c1 in committersUntil180DaysAgo:
                        for c2 in committersBefore180DaysAgo:
                            if (str(c1)==str(c2)):
                                retention += 1
                        
                    add_text = str(projectName) + "|" +  str(retention)
                print(add_text)
                external_file.write(add_text)
                external_file. write("\n")
                external_file.close()    

            # remove unnecessary files
            if os.path.exists("commitsDate.txt"):
                os.remove("commitsDate.txt")

            os.chdir(currentDir)
        projectFolders.close()      