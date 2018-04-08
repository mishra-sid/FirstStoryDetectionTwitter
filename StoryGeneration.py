import os, re

class StoryGenerator:
    def __init__(self, sourcePath):
        self.sourcePath = sourcePath    

    def sanitize(self, dirtyString):
        return dirtyString.replace("\n", " ").replace(" Reuter &#3;", "").replace("&lt;", "<")

    #Returns an iterator of stories 
    def yieldStory(self):
        storyCount = 0
        dummyStoryCount = 0
        for root, _, files in os.walk(self.sourcePath):
            print(sorted(files))
            for file in sorted(files):
                if (file.endswith(".sgm")):
                    with open(os.path.join(root, file), encoding="utf8", errors='ignore') as data:
                        inBody = False
                        inTitle = False
                        curStory = ""
                        curTitle = ""
                        for line in data:

                            #Story Title Extraction
                            titleTagPos = line.find("<TITLE>")
                            if (titleTagPos != -1) or inTitle:

                                #Some Stories dont have body, ignoring those
                                if (line.find("Blah blah blah.") != -1):
                                    inTitle = False
                                    inBody = False
                                    curStory = ""
                                    curTitle = ""
                                    continue

                                titleEndTagPos = line.find("</TITLE>")

                                # Check for some potential unexpected data formatting while extracting title
                                if (curTitle != "") and (titleTagPos != -1):
                                    #print("\nDouble Title before body Error!\nLine is", line, "Title so far is:", curTitle, 'Body so far is :', curStory)
                                    inTitle = False
                                    curTitle = ""
                                    dummyStoryCount += 1
                                elif inBody:
                                    print("\nBody before Title Error!\nLine is", line, "Title so far is:", curTitle, 'Body so far is :', curStory)
                                    exit(1)
                                else:
                                # If no error then continue to extract title
                                    startTitleSegment = titleTagPos+len("<TITLE>") if (titleTagPos != -1) else 0
                                    if inTitle:
                                        curTitle += " "
                                    if titleEndTagPos == -1:
                                        curTitle += line[startTitleSegment : ]
                                        inTitle = True
                                    else:
                                        curTitle += line[startTitleSegment : titleEndTagPos]
                                        inTitle = False

                            # Story Body Extraction
                            if inBody:
                                if inTitle:
                                    print("\nBody before Title Error!\nLine is", line, "Title so far is:", curTitle, 'Body so far is :', curStory)
                                    exit(1)
                                pos = line.find("</BODY>")
                                curStory += line if pos == -1 else line[:pos]
                                if pos != -1:
                                    inBody = False
                                    storyCount += 1
                                    yield (re.sub(r" +", ' ', self.sanitize(curStory)), re.sub(r" +", ' ', self.sanitize(curTitle)))
                                    curStory = ""
                                    curTitle = ""
                            else:
                                pos = line.find("<BODY>")
                                if pos != -1:
                                    curStory += line[pos+len("<BODY>"):] if line.find("</BODY>") == -1 else line[pos+len("<BODY>"):line.find("</BODY>")]
                                    inBody = True
        print("True Stories:", storyCount, "Dummy Stories:", dummyStoryCount)

    def getAllStories(self):
        stories = []
        titles = []
        for ind, story in enumerate(self.yieldStory()):
            body, title = story 
            stories.append({ 'timestamp' : ind, 'story': body })
            titles.append({ 'timestamp' : ind, 'title': title })
        return (stories, titles)

#Usecase

# for i, story in enumerate(yeildStory("./Dataset")):
# 	print("-"*20, "Story", i,"-"*20)
# 	print(story)
# 	print("-"*47)
# 	if i % 10 == 0:
# 		input()
