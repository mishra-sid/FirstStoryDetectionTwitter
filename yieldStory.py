import os, re

def yieldStory(sourcePath):
	for root, _, files in os.walk(sourcePath):
		for file in files:
			if (file.endswith(".sgm")):
				with open(os.path.join(root, file), 'r') as data:
					inBody = False
					curStory = ""
					for line in data:
						if inBody:
							pos = line.find("</BODY>")
							curStory += line if pos == -1 else line[:pos]
							if pos != -1:
								inBody = False
								yield re.sub(r" +", ' ', curStory.replace("\n", " ").replace(" Reuter &#3;", "").replace("&lt;", "<"))
								curStory = ""
						else:
							pos = line.find("<BODY>")
							if pos != -1:
								curStory += line[pos+6:]
								inBody = True



# Testcase

for i, story in enumerate(yeildStory("./Dataset")):
	print("-"*20, "Story", i,"-"*20)
	print(story)
	print("-"*47)
	if i % 10 == 0:
		input()
