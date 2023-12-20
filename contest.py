from ContestParser import ContestParser
from CFDownloader import CFDownloader
import codecs
import json
import time
from os import system, name, makedirs, path, chdir

settings = json.load(open("settings.json"))
apiKey = settings["api"]["key"]
apiSecret = settings["api"]["secret"]
groupId = settings["groupId"]
contestId = settings["contestId"]

def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')

def displayMenu():
    clear()
    print("=========Codeforces Contest Downloader=========")
    print("=============Created by LordierClaw============")
    handle = settings["login"]["handle"]
    print(f"Your handle: {handle}")
    print(f"Group ID: {groupId}  \t   Contest ID: {contestId}")
    print("-----------------------------------------------")
    print("1. Get contest's information - generate database.json")
    print("2. Download all submission (only the first solved)")
    print("3. Run Dolos from download folder (dolos required)")
    print("4. Let me do everything (1->2->3)")
    print("0. Exit")
    print("-----------------------------------------------")
    return input("Select an option: ")

def displayReturn():
    print("-----------------------------------------------")
    input("Press Enter to continue...")

def getContestInformation(returnable=True):
    clear()
    cp = ContestParser(groupId, contestId, apiKey, apiSecret)
    data = cp.get()
    print("Saving database.json ...", end="")
    try:
        with codecs.open(f"database.json", "w", encoding="utf-8") as output:
            json.dump(data, output, indent=2)
            print("Completed")
            if returnable == False:
                return
    except:
        print("Failed")
    displayReturn()

def downloadAllSubmission(returnable=True):
    clear()
    print("Start scraping and saving code...")
    #checking download folder and database.json exists
    makedirs("./download/", exist_ok=True)
    if path.exists("database.json") == False:
        print("database.json not found! Please return to the menu and get contest's information first!")
        displayReturn()
        return
    data = json.load(codecs.open("database.json", "r", encoding="utf-8"))
    print("database.json is loaded successfully.")

    cf = CFDownloader()
    cf.login(settings["login"]["handle"], settings["login"]["password"])

    completedCount = 0
    for user in data["solved"]:
        handle = user["handle"]
        print(f"Working on handle: {handle}")
        for sub in user["submission"]:
            subId = user["submission"][sub]
            if (subId != 0):
                name = f"./download/{sub}_{handle}_{subId}.cpp"
                if path.exists(name): continue
                with codecs.open(name, "w", encoding="utf-8") as output:
                    output.write(cf.getSourceCode(groupId, contestId, subId))
                completedCount += 1
                print(f"Saved: {name}, {completedCount} files downloaded and saved, waiting 1 second to avoid being banned")
                time.sleep(1)
    print(f"Completed: {completedCount} files downloaded and saved")
    if (returnable == True):
        displayReturn()

def runDolos():
    clear()
    print("Running dolos ...")
    lang = settings["dolos"]["language"]
    fileExt = settings["dolos"]["file_ext"]
    command = f"dolos -f web -l {lang} *.{fileExt}"
    chdir(path.abspath("download"))
    system(command)

def doEverything():
    getContestInformation(returnable=False)
    downloadAllSubmission(returnable=False)
    runDolos()

def main():
    while(True):
        option = displayMenu()
        if option == '1':
            getContestInformation()
        elif option == '2':
            downloadAllSubmission()
        elif option == '3':
            runDolos()
            return
        elif option == '4':
            doEverything()
            return
        elif option == '0':
            return
        else:
            print("Invalid selection. Please try again.")
            displayReturn()

if __name__ == "__main__":
    main()