import time
import praw

# CONFIG START
user_agent = ("Find deleted 0.3 by /u/?")
checktop = 100			# check top 100
insubreddit = "all"		# subreddit
checkevery = 10 		# 10s
# CONFIG DONE

r = praw.Reddit(user_agent=user_agent)
print("Logging in...")
#r.login()
lastrun = []
allhot = []
moreallhot = []
firstround = False

while True:
	print("Waiting...")
	time.sleep(checkevery)
	print("Tick")
	print(" > Loading new data...")
	subreddit = r.get_subreddit(insubreddit)
	allhot = subreddit.get_hot(limit=checktop)
	moreallhot = subreddit.get_hot(limit=checktop+100)
	print(" > Finding differences...")
	if firstround:
		print("   First round, no action")
		firstround = False
	else:
		found = False
		for submission in lastrun:
			with open("deletions.txt", "a") as resultfile:
				resultfile.write((lastrun.index(submission)+1)+",")
				resultfile.write(submission.score+",")
				resultfile.write(submission.title+",")
				resultfile.write(submission.subreddit+",")
				resultfile.write(submission.short_link+",")
				resultfile.write(submission.author+",")
				resultfile.write(submission.selftext+",")
				resultfile.write(submission.created_utc+",")
				resultfile.write("\n")
			print((lastrun.index(submission)+1)+",")
			print(submission.score+",")
			print(submission.title+",")
			print(submission.subreddit+",")
			print(submission.short_link+",")
			print(submission.author+",")
			print(submission.selftext+",")
			print(submission.created_utc+",")
			print("\n")
		for submission in list(set(lastrun) - set(allhot)):
			found = True
			print(" > Found difference")
			if submission in moreallhot:
				print(" > False alarm")
			else:
				print("!> Deletion found")
				#print(" > Title: "+submission.title)
				print(" > Short link: "+submission.short_link)
				with open("deletions.txt", "a") as resultfile:
					resultfile.write((lastrun.index(submission)+1)+",")
					resultfile.write(submission.score+",")
					resultfile.write(submission.title+",")
					resultfile.write(submission.subreddit+",")
					resultfile.write(submission.short_link+",")
					resultfile.write(submission.author+",")
					resultfile.write(submission.selftext+",")
					resultfile.write(submission.created_utc+",")
					resultfile.write("\n")
		if not found:
			print("   None found")
	lastrun = allhot
