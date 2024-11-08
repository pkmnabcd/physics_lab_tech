import os

"""
I apologize if this code is hard to read...
The purpose of this code was to look in each night folder in a user inputted month and year and determine which processes have been done (Whether sr, srff, srffcaun, or none). 
It would then print out details to the screen, which I would record the important info in a spreadsheet, and take a closer look if necessary.
"""
def main():
    # This loop iterates on each folder in a certain [month][year] path and it checks to make sure that the unprocessed and processed folders are both present.
    # It also checks to see which processes have been done in a certain folder
    unprocessedCount = 0
    processedCount = 0
    srProcessingMissing = []
    additionalProcessingList = []
    otherFilesList = []

    # Set the path
    # Receives input for year and (shortened) month
    year = input("Enter the year: ")
    month = input("Enter the month (First 3 letters): ")

    for i in range(31):
        # This if-else-if series determines which ending to put on the path name
        # Path name in the form 10-11
        pathEnding = 0
        if i < 8:
            pathEnding = "0" + str(i + 1) + "-0" + str(i + 2)
        elif i == 8:
            pathEnding = "09-10"
        elif i == 30:
            pathEnding = "31-01"
        else:
            pathEnding = str(i + 1) + "-" + str(i + 2)
    # Adding a case just below for when it's the end of the month on the 28th 29th or 30th
        
        # makes the path where the directory is taken using the previous user input
        
        # path = "C://Users//Domi//Desktop//Chile_ALO//ChileMTM//" + year + "//" + month + year + "//" + month + pathEnding
        path = "I://ChileMTM//" + year + "//" + month + year + "//" + month + pathEnding
        if os.path.exists(path):
            unprocessedCount += 1
        elif not os.path.exists(path) and (i == 27 or i == 28 or i == 29):  # Tests to see if it's the end of the month
            path = "I://ChileMTM//" + year + "//" + month + year + "//" + month + str(i + 1) + "-01"
            if os.path.exists(path):
                unprocessedCount += 1
                pathEnding = str(i + 1) + "-01"
        # path = "C://Users//Domi//Desktop//Chile_ALO//ChileMTM//" + year + "//" + month + year + "//processed//" + month + pathEnding
        path = "I://ChileMTM//" + year + "//" + month + year + "//processed//" + month + pathEnding
        if os.path.exists(path):
            processedCount += 1
        elif not os.path.exists(path) and (i == 27 or i == 28 or i == 29):  # Tests to see if it's the end of the month
            path = "I://ChileMTM//" + year + "//" + month + year + "//processed//" + month + str(i + 1) + "-01"
            if os.path.exists(path):
                processedCount += 1
                pathEnding = str(i + 1) + "-01"
        
        if not os.path.exists(path): #and (i != 27 or i != 28 or i != 29):  # Makes it so if a folder doesn't exist, it doesn't attempt to count the files inside
            continue
            
        directoryList = os.listdir(path)

        # Initialize count variables to count the number of each file type
        BG_sr_count = 0
        BG_srff_count = 0
        BG_srffcaun_count = 0
        BG_other_count = 0
        
        Dark_sr_count = 0
        Dark_srff_count = 0
        Dark_srffcaun_count = 0
        Dark_other_count = 0
        
        P12A_sr_count = 0
        P12A_srff_count = 0
        P12A_srffcaun_count = 0
        P12A_other_count = 0
        
        P14A_sr_count = 0
        P14A_srff_count = 0
        P14A_srffcaun_count = 0
        P14A_other_count = 0
        
        other_count = 0

        # Categorize each file in the directory
        for file in directoryList:
            # BG file options
            if file.startswith("BG_sr") and not file.startswith("BG_srf"):
                BG_sr_count += 1
            elif file.startswith("BG_srff") and not file.startswith("BG_srffcaun"):
                BG_srff_count += 1
            elif file.startswith("BG_srffcaun"):
                BG_srffcaun_count += 1
            elif file.startswith("BG") and not file.startswith("BG_srffcaun"):
                BG_other_count += 1
            
            # Dark file options
            elif file.startswith("Dark_sr") and not file.startswith("Dark_srf"):
                Dark_sr_count += 1
            elif file.startswith("Dark_srff") and not file.startswith("Dark_srffcaun"):
                Dark_srff_count += 1
            elif file.startswith("Dark_srffcaun"):
                Dark_srffcaun_count += 1
            elif file.startswith("Dark") and not file.startswith("Dark_srffcaun"):
                Dark_other_count += 1
                
            # P12A file options
            elif file.startswith("P12A_sr") and not file.startswith("P12A_srf"):
                P12A_sr_count += 1
            elif file.startswith("P12A_srff") and not file.startswith("P12A_srffcaun"):
                P12A_srff_count += 1
            elif file.startswith("P12A_srffcaun"):
                P12A_srffcaun_count += 1
            elif file.startswith("P12A") and not file.startswith("P12A_srffcaun"):
                P12A_other_count += 1
                
            # P14A file options
            elif file.startswith("P14A_sr") and not file.startswith("P14A_srf"):
                P14A_sr_count += 1
            elif file.startswith("P14A_srff") and not file.startswith("P14A_srffcaun"):
                P14A_srff_count += 1
            elif file.startswith("P14A_srffcaun"):
                P14A_srffcaun_count += 1
            elif file.startswith("P14A") and not file.startswith("P14A_srffcaun"):
                P14A_other_count += 1
                
            else:
                other_count += 1

        # Print path ending to organize the following info that will be printed
        print(pathEnding)        

        # Making the message to determine what processes have been done to BG
        BG_message = "BG status:  " + str(BG_sr_count) + " sr only,   " + str(BG_srff_count) + " srff,   " + str(BG_srffcaun_count) + " srffcaun,   " + str(BG_other_count) + " other"
        print(BG_message)
        
        # Message to show Dark processes
        Dark_message = "Dark status:  " + str(Dark_sr_count) + " sr only,   " + str(Dark_srff_count) + " srff,   " + str(Dark_srffcaun_count) + " srffcaun,   " + str(Dark_other_count)
        print(Dark_message)

        # Message to show P12A processes
        P12A_message = "P12A status:  " + str(P12A_sr_count) + " sr only,   " + str(P12A_srff_count) + " srff,   " + str(P12A_srffcaun_count) + " srffcaun,   " + str(P12A_other_count) + " other"
        print(P12A_message)
        
        # Message to show P14A processes
        P14A_message = "P14A status:  " + str(P14A_sr_count) + " sr only,   " + str(P14A_srff_count) + " srff,   " + str(P14A_srffcaun_count) + " srffcaun,   " + str(P14A_other_count) + " other"
        print(P14A_message)
        
        # Shows that there are other files inside
        print("Other files: " + str(other_count))
        print()

        # Decide which additional processing has been completed
        final_msg = ""
        additionalProcessingBoolean = 0

        if BG_srff_count > BG_sr_count / 4 or BG_srffcaun_count > BG_sr_count / 4:
            final_msg += "BG has had additional processing.\n"
            additionalProcessingBoolean = True
        
        if Dark_srff_count > Dark_sr_count / 4 or Dark_srffcaun_count > Dark_sr_count / 4:
            final_msg += "Dark has had additional processing.\n"
            additionalProcessingBoolean = True
        
        if P12A_srff_count > P12A_sr_count / 4 or P12A_srffcaun_count > P12A_sr_count / 4:
            final_msg += "P12A has had additional processing.\n"
            additionalProcessingBoolean = True
        
        if P14A_srff_count > P14A_sr_count / 4 or P14A_srffcaun_count > P14A_sr_count / 4:
            final_msg += "P14A has had additional processing.\n"
            additionalProcessingBoolean = True
        
        # Decide if there are enough other files to make a note of
        if other_count > 20:
            final_msg += "There are other files inside.\n"
            otherFilesList.append(pathEnding)
            
        # Add relevant days to the proper categories to be displayed at the end
        if additionalProcessingBoolean:
            additionalProcessingList.append(pathEnding)
        if BG_sr_count < 6 or P12A_sr_count < 6 or P14A_sr_count < 6:
            srProcessingMissing.append(pathEnding)

        print(final_msg)


    # A little header to make sure to clarify the month and year
    print("\nResults for", month + year, end = "\n\n")
    
    
    # Interprets whether or not each unprocessed has a corresponding processed folder.
    print("Unprocessed Count: " + str(unprocessedCount))
    print("Processed Count: " + str(processedCount))
    if processedCount == unprocessedCount:
        print("\nunprocessed = processed is TRUE\n\n")
    else:
        print("\nunprocessed = processed is FALSE\n\n")
        
        
    # Prints which folders have processing or other files inside
    msg = ""
    msg += "Folders missing sr: " + str(srProcessingMissing)
    msg += "\nFolders with additional processing: " + str(additionalProcessingList)
    msg += "\nFolders with other files inside: " + str(otherFilesList)
    print(msg)




# Loop to repeat the whole program as often as user wants
userContinue = True
while userContinue:
    main()
    userInput = input("Continue? (yes or no) ")
    if userInput.lower() == "yes":
        userContinue = True
    else:
        userContinue = False
    print("\n\n\n")