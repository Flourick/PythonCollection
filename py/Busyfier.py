import time, os

if __name__ == "__main__":
	count = 0
	sleep_time = 240 # seconds

	while True:
		time.sleep(sleep_time)

		file = open("tmp.tmp", "w")
		file.write("Eyoo")
		file.close()
		
		os.remove("tmp.tmp")

		count = count + sleep_time
		if(count % 60 == 0):
			print("Running for " + str(int(count / 60)) + " minutes!")
