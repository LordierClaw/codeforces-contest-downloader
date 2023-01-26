import requests, hashlib, random, time

class ContestParser:
    def __init__(self, groupId, contestId, APIKey, APISecret) -> None:
        self.groupId = groupId
        self.contestId = contestId
        self.apiKey = APIKey
        self.apiSecret = APISecret
    
    def __request(self, methodName, optionalMethod=""):
        rand = random.randint(0, 100000)
        rand = str(rand).zfill(6)
        currentTime = str(int(time.time()))
        apiSig = rand + "/" + methodName + "?apiKey=" + self.apiKey + \
            "&contestId=" + self.contestId + "&groupCode=" + self.groupId + optionalMethod + \
            "&time=" + currentTime + "#" + self.apiSecret
        hash = hashlib.sha512(apiSig.encode()).hexdigest()
        apiCommand = f"https://codeforces.com/api/{methodName}?groupCode={self.groupId}&contestId={self.contestId}{optionalMethod}&apiKey={self.apiKey}&time={currentTime}&apiSig={rand+hash}"
        data = requests.get(apiCommand).json()
        return data["status"], data["result"]

    def __getStandings(self):
        status, data = self.__request("contest.standings")
        problems = []
        for problem in data["problems"]:
            problems.append(problem["index"])
        handles = []
        for row in data["rows"]:
            handles.append(row["party"]["members"][0]["handle"]) #index is 0 because there is only 1 member (not a team)
        return problems, handles

    def __getFirstAC(self, handle, problemList):
        status, submissions = self.__request("contest.status", f"&handle={handle}")
        ACSubs = {}
        for problem in problemList:
            ACSubs[problem] = 0;
        for i in range(len(submissions)-1, -1, -1):
            if submissions[i]["verdict"] == "OK":
                problemId = submissions[i]["problem"]["index"] #in alphabet
                subId = submissions[i]["id"]
                if (ACSubs[problemId] == 0):
                    ACSubs[problemId] = subId
        return ACSubs
    
    def __getData(self):
        problems, handles = self.__getStandings()
        data = {
            "groupId": self.groupId,
            "contestId": self.contestId,
            "problems": problems,
            "handles": handles,
            "solved": []
        }
        print("Start generating database...")
        for handle in handles:
            print(f"Analyzing {handle}...", end="")
            time.sleep(1)
            try:
                subs = self.__getFirstAC(handle, problems)
                print("done")
            except:
                print("failed")
            finally:
                userdata = {
                    "handle": handle,
                    "submission": subs
                }
                data["solved"].append(userdata)
        print("Done.")
        return data
    
    def get(self):
        return self.__getData()