import sys, time, os

def exit():
	print()
	print()

	input("Press enter to exit...")
	
def main():
	count = 0
	sleep_time = 240

	while True:
		time.sleep(sleep_time)

		file = open("tmp.tmp", "w")
		file.write("Eyoo")
		file.close()
		
		os.remove("tmp.tmp")

		count = count + sleep_time
		if(count % 60 == 0):
			print("Running for " + str(int(count / 60)) + " minutes!")

if __name__ == "__main__":
	if sys.version_info[0] < 3:
		raise Exception("You must use Python 3.4 or higher.")
	elif sys.version_info[1] <  4:
		raise Exception("You must use Python 3.4 or higher.")
	
	main()
	exit()
