# Repair-Plex-Added-Date
Python code to repair Plex DB item Added Date. Added Date is not accessible via GUI.  It is an internal date.  For some reason, some movie's Added Date were set to a future date of 2098.  This continues to make these problem movies show up
as the first movie when sorted by Added Date.  The only way to fix this problem is to write code to change this date to a date in line with other movies.
Run the script in PYcharm or CMD windows.

This python code will repair date items associated with a movie by inspecting the date to see if it is in the future (bug in Plex for some added media) and replace it with a date from a week ago as of the running date
The script check all dates associated with a movie.  If they are in the future they are reset to 1 week ago on run date.  You can change the date in the code.
These are the scripts
Config.py contains ID and PW to log in
Gettoken.py gets the Plex current token to test if it can get to the local Plex server
Fixsingle.py  ask for a movie name and fixes the date.  
cleandb.py fixes all files by stepping through each file
Allor1.py ask for a specific library or 'ALL'
Config.py should look like this
PLEX_USERNAME = 'edxxx@gmail.com'
PLEX_PASSWORD = '4vEM7ggVB5ue#'
# Plex local server URL.  Find it with LAN IP scanner if you don't know what it is.
PLEX_URL = 'http://192.168.1.52:32400'
#find Plex on your own network and substitute
