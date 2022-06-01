#requires python3
#creates an output called hcsSS_coreContributors.txt
import subprocess, os

if os.path.exists("Projectnamesforanalysis.txt"):
    
    #remove coreContributors file to start a new one
    if os.path.exists("hcsSS_coreContributors.txt"):
        os.remove("hcsSS_coreContributors.txt")

    with open("Projectnamesforanalysis.txt") as projectFolders:
        for projectFolder in projectFolders:
            currentDir = os.getcwd()
            os.chdir(currentDir+"/"+projectFolder.rstrip())            

            #get all tags into a file called tags.txt
            tagsFile = open("tags.txt", "w")
            subprocess.call(["git", "tag"], stdout=tagsFile)


            with open("hcsSS_coreContributors.txt", "a") as external_file:
                add_text = "project|tag|numberOfCoreContributors"
                external_file.write(add_text)
                external_file. write("\n")
                external_file.close()    
                    
            #extract the project name
            #projectName = subprocess.check_output(["git", "remote", "get-url", "origin"])
            getCommand = "--get"
            projectName = subprocess.check_output(["git", "config", getCommand, "remote.origin.url"])
            projectName = str(projectName.rstrip())
            projectName = projectName.replace("b'https://github.com/","")
            projectName = projectName.replace(".git'","")
            #for each tag, identify core contributors 
            #We consider a developer as core if the developer is
            # in the top 20% of developers in that project 
            # (calculated by the number of commits authored). 
            # Otherwise the developer is non-core
            with open("tags.txt") as external_file_tags:
                for tag in external_file_tags:
                    #get committers in a tag
                    ccTag = open("coreContributorsInATag.txt", "w")
                    subprocess.call(["git", "shortlog","-es","-n",tag.rstrip()], stdout=ccTag)   
                    ccTag.close() 

                    commits = []
                    with open("coreContributorsInATag.txt", errors='ignore') as external_file_ccTags:
                        for line in external_file_ccTags:
                            #data[0] is the total of commits from a contributor
                            data = line.split()
                            commits.append(int(data[0]))
                        sumCommits = 0
                        countContributors = 0
                        for c in commits:
                            sumCommits += c
                        #identifying commiters within the 20% 
                        for c in commits:
                            if c >= sumCommits * 20/100:
                                countContributors += 1
                        print(str(projectName) + "|" + tag.rstrip() + "|" + str(countContributors))
                        with open("hcsSS_coreContributors.txt", "a") as external_file:
                                    add_text = str(projectName) + "|" + tag.rstrip() + "|" + str(countContributors)
                                    external_file.write(add_text)
                                    external_file. write("\n")
                                    external_file.close()    
                        
                        external_file_ccTags.close()
                external_file_tags.close()

            #remove unnecessary files
            if os.path.exists("tags.txt"):
                os.remove("tags.txt")
            if os.path.exists("coreContributorsInATag.txt"):
                os.remove("coreContributorsInATag.txt")

            os.chdir(currentDir)
        projectFolders.close()      