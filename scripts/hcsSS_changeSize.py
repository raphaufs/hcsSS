#requires python3
#creates an output called hcsSS_changeSize.txt
import subprocess, os

if os.path.exists("Projectnamesforanalysis.txt"):
    #remove codeContributors file to start a new one
    if os.path.exists("hcsSS_changeSize.txt"):
        os.remove("hcsSS_changeSize.txt")

    with open("Projectnamesforanalysis.txt") as projectFolders:
        for projectFolder in projectFolders:
            currentDir = os.getcwd()
            os.chdir(currentDir+"/"+projectFolder.rstrip())            

            #get all tags into a file called tags.txt
            tagsFile = open("tags.txt", "w")
            subprocess.call(["git", "tag"], stdout=tagsFile)

            with open(currentDir+"/"+"hcsSS_changeSize.txt", "a") as external_file:
                add_text = "project|tag|insertions|deletions"
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

            firstTag = True
            tagOld = ""

            #for each pair of tags, identify changes 
            with open("tags.txt") as external_file_tags:
                for tag in external_file_tags:

                    if firstTag:
                        firstTag = False
                        tagOld = tag
                        print(str(projectName) + "|" + tag.rstrip() + "|0|0")
                        with open(currentDir+"/"+"hcsSS_changeSize.txt", "a") as external_file:
                                    add_text = str(projectName) + "|" + tag.rstrip() + "|0|0"
                                    external_file.write(add_text)
                                    external_file. write("\n")
                                    external_file.close() 
                        continue
                    #get committers in a tag
                    tagDiff = open("tagDiffs.txt", "w")
                    numStat = "--numstat"
                    subprocess.call(["git", "diff",str(tag.rstrip()),str(tagOld.rstrip()),numStat], stdout=tagDiff)   
                    tagDiff.close()

                    tagOld = tag 

                    insertions = 0
                    deletions = 0
                    with open("tagDiffs.txt", errors='ignore') as external_file_tagDiff:
                        for line in external_file_tagDiff:
                            #data[0] is the total of insertions
                            #data[1] is the total of deletions
                            data = line.split()
                            if str(data[0]) not in "-": 
                                insertions += int(data[0])
                            else:
                                insertions += 0
                            
                            if str(data[1]) not in "-": 
                                deletions += int(data[1])
                            else:
                                deletions += 0
                        
                        print(str(projectName) + "|" + tag.rstrip() + "|" + str(insertions) + "|" + str(deletions))
                        with open(currentDir+"/"+"hcsSS_changeSize.txt", "a") as external_file:
                                    add_text = str(projectName) + "|" + tag.rstrip() + "|" + str(insertions) + "|" + str(deletions)
                                    external_file.write(add_text)
                                    external_file. write("\n")
                                    external_file.close()    
                        
                        external_file_tagDiff.close()
                external_file_tags.close()

            #remove unnecessary files
            if os.path.exists("tags.txt"):
                os.remove("tags.txt")
            if os.path.exists("tagDiffs.txt"):
                os.remove("tagDiffs.txt")

            os.chdir(currentDir)
        projectFolders.close()                    