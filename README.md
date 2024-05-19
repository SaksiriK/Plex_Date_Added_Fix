# Repair-Plex-Added-Date
Python code to repair Plex DB item Added Date
This python code will repair date items associated with a movie by inspecting the date to see if it is in the future (bug in Plex for some added media) and replace it with a date from a week ago as of running date
Config.py contains ID and PW to log in
Gettoken.py gets current token to test if it can get to the local Plex server
Fixsingle.py  ask for movie name
cleandb.py fixes all files by stepping through each file
Allor1.py ask for specific library or 'ALL'
Config.py should look like this
PLEX_USERNAME = 'edxxx@gmail.com'
PLEX_PASSWORD = '4vEM7ggVB5ue#'
# Plex server URL
PLEX_URL = 'http://192.168.1.52:32400'
