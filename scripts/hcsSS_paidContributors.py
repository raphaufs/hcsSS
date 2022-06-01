#requires python3
#creates an output called hcsSS_paidContributors.txt
import subprocess, os

#remove duplicate committers in a array
def remove_duplicates(original):
    unique = []
    [unique.append(n) for n in original if n not in unique]
    return(unique)

if os.path.exists("Projectnamesforanalysis.txt"):
    
    #remove codeContributors file to start a new one
    if os.path.exists("hcsSS_paidContributors.txt"):
        os.remove("hcsSS_paidContributors.txt")

    with open("Projectnamesforanalysis.txt") as projectFolders:
        for projectFolder in projectFolders:
            currentDir = os.getcwd()
            os.chdir(currentDir+"/"+projectFolder.rstrip())            

            #get all tags into a file called tags.txt
            tagsFile = open("tags.txt", "w")
            subprocess.call(["git", "tag"], stdout=tagsFile)


            with open("hcsSS_paidContributors.txt", "a") as external_file:
                add_text = "project|tag|numberOfPaidContributors"
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
            #for each tag, identify paid contributors 
            #We excludedemail  addresses  belonging  
            #to  the  following  domains, such as:
            #@gmail,  @googlemail,  @local,  @me.com,
            #@instance-1,@github, @live, @hotmail, 
            #@yahoo, @none
            with open("tags.txt") as external_file_tags:
                for tag in external_file_tags:
                    
                    #get all committers emails in a tag
                    committersEmail = open("committersEmail.txt", "w")
                    #ce: committer email ci: commit date
                    pretty = '--pretty="%ce"'
                    subprocess.call(["git", "log", "--pretty=", pretty,str(tag).rstrip()], stdout=committersEmail)

                    committersEmails = []

                    with open("committersEmail.txt", errors='ignore') as external_file_commitsDates:
                        countPaidContributors = 0
                        for line in external_file_commitsDates:
                            #remove classical non paid emails
                            if ("@gmail" not in str(line) and
                                "@googlemail" not in str(line) and
                                "@local" not in str(line) and
                                "@me.com" not in str(line) and
                                "@instance-1" not in str(line) and
                                "@github" not in str(line) and
                                "@live" not in str(line) and
                                "@hotmail" not in str(line) and
                                "@yahoo" not in str(line) and
                                "@none" not in str(line)):
                                committersEmails.append(str(line).rstrip())
                            
                        committersEmails = remove_duplicates(committersEmails)
                        
                        countPaidContributors = len(committersEmails)

                        print(str(projectName) + "|" + tag.rstrip() + "|" + str(countPaidContributors))
                        with open("hcsSS_paidContributors.txt", "a") as external_file:
                                    add_text = str(projectName) + "|" + tag.rstrip() + "|" + str(countPaidContributors)
                                    external_file.write(add_text)
                                    external_file. write("\n")
                                    external_file.close()    
                        
                external_file_tags.close()

            #remove unnecessary files
            if os.path.exists("tags.txt"):
                os.remove("tags.txt")
            if os.path.exists("committersEmail.txt"):
                os.remove("committersEmail.txt")

            os.chdir(currentDir)
        projectFolders.close()    