from ContestParser import ContestParser
from CFDownloader import CFDownloader

import codecs
import json
import time
settings = json.load(open("settings.json"))

def main():
    apiKey = settings["api"]["key"]
    apiSecret = settings["api"]["secret"]
    groupId = settings["groupId"]
    contestId = settings["contestId"]
    cf = CFDownloader()
    cf.login(settings["login"]["handle"], settings["login"]["password"])
    cp = ContestParser(groupId, contestId, apiKey, apiSecret)
    data = cp.get()
    with open(f"database.json", "w", encoding="utf-8") as output:
        json.dump(data, output, indent=2)
    print("Start scraping and saving code...")
    #
    for user in data["solved"]:
        handle = user["handle"]
        print(f"Working on handle: {handle}")
        for sub in user["submission"]:
            subId = user["submission"][sub]
            if (subId != 0):
                name = f"{sub}_{handle}_{subId}.cpp"
                with codecs.open(f"./download/{name}", "w", encoding="utf-8") as output:
                    output.write(cf.getSourceCode(groupId, contestId, subId))
                time.sleep(1)
    print("Done.")

if __name__ == "__main__":
    main()