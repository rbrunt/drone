import drone
import sys

if __name__=="__main__":
	if len(sys.argv)==2:
		if sys.argv[1]=="add":
			drone.italics = "add"
		elif sys.argv[1]=="remove":
			drone.italics = "remove"
		else:
			exit("The only valid commands are 'add' or 'remove'")
	else:
		drone.italics = "add"
	
	drone.main()