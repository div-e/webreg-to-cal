WebReg to Calendar Events 
========================

# How to use

## Step 1: 
Open WebReg to the page that displays your schedule. It should be the default page after you have selected "a term to begin" and clicked "go" (the view that displays a table: "List" rather than a graphic schedule: "Calendar"). Select All (Command + A) and then copy (Command + C) to save the html representation of the page to your pasteboard. 
## Step 2:
In terminal, go to the root directory of the project and run ```python3 quickstart.py ```  
## Step 3: 
Follow the instruction to login. Please watch out for privacy notices as you login. (It is recommended that you purge ```token.json``` after use as it grants read/write access to your calendar) 
## Step 4: 
The program will read the data from your pasteboard. The schedule should have been populated in a new calendar called "Schedule 1" in your 
Google Calendar account. If not, delete the calendar, find out what is wrong with code, and
submit an issue or try to fix it and make a pull request. Any contribution is encouraged. 

# Limitations
Note that this is an open source software. No one is liable for the code. Code doesn't work? Please help by submitting an issue. 

# Known issues
Note that Google Calendar API credentials as specified in ```credentials.json``` is subject to cancellation. In which case, follow [Google Calendar Guide](https://developers.google.com/calendar/quickstart/python). 
