#Mohammad Fawzan Alim
#TP064501

def menu():
    while(True):

        #PRINT Home Menu
        print("HOME MENU:\n")

        print("  1. New Patient Registration")
        print("  2. Vaccine Administration")
        print("  3. Search Patient Record and Vaccination Status")
        print("  4. Statistical Information on Patients Vaccinated")
        print("  0. Exit")

        #INPUT - Home Menu Choice
        while(True):
            homeChoice = input("\n  Choose an option: ")
            if homeChoice in ['0', '1', '2', '3', '4']:
                break
            print("  Invalid input. Input must be a number between 0 and 4. Try again.")


        #Do task based on input
        if(homeChoice == '0'):
            print("\n  Exiting the program....")
            return

        if(homeChoice == '1'):
            registration()
            continue
        
        if(homeChoice == '2'):
            administration()
            continue
        
        if(homeChoice == '3'):
            search()
            continue
        
        if(homeChoice == '4'):
            statistics()
            continue


def registration():
    print("\nNEW PATIENT REGISTRATION MENU:")

    #Take input for new patient and assign the info to 'patient' list
    patient = regInput()

    #if the 'patient' holds no value, then return to Home Menu
    if(patient == None):
        return

    #generate next ID for new patient
    patient[0] = generateId()

    #Update new patient info in file
    writePatientData(patient)



def regInput():

    #INPUT - Vaccination Center
    while(True):
        center = input("\n  Vaccination center [1/2]: ")
        if(center == "1" or center == "2"):
            break
        print("  Invalid input. Input must be '1' or '2'. Try again.\n")

    #INPUT - Name
    while(True):
        name = input("\n  Name: ")
        if(name != ""):
            break
        print("  Please provide a name")

    #INPUT - Age
    while(True):
        try:
            age = float(input("\n  Age (in years): "))
        except:
            print("  Invalid input. Input must be a number. Try again.")
            continue

        if(age <= 0):
            print("  Invalid input. Try again.")
        else:
            break


    #PRINT - Available vaccines based on age
    print("\n  Available vaccines: ")
    if(age < 12):
        print("    Sorry. No Vaccines available for this age.\n\n")
        return None         #Return to home menu if no vaccine available
    if(age >= 12):
        print("    AF [2 Dosage with 2 weeks interval]")
    if(age >= 18):
        print("    BV [2 Dosage with 3 weeks interval]")
    if(age >= 12 and age <= 45):
        print("    CZ [2 Dosage with 3 weeks interval]")
    if(age >= 12):
        print("    DM [2 Dosage with 4 weeks interval]")
    if(age >= 18):
        print("    EC [1 Dosage]")


    #INPUT - Vaccine type/code
    while(True):
        code = input("\n  Vaccine code: ")
        if(code == "AF" and age >= 12):
            break
        if(code == "BV" and age >= 18):
            break
        if(code == "CZ" and age >= 12 and age <= 45):
            break
        if(code == "DM" and age >= 12):
            break
        if(code == "EC" and age >= 18):
            break
        print("  Invalid input. Try again.")

    #INPUT - Contact Number
    while(True):
        contactNumber = input("\n  Contact Number: ")
        if(contactNumber != ""):
            break
        print("  Please provide a contact number")

    #INPUT - Email
    while(True):
        email = input("\n  Email: ")
        if(email != ""):
            break
        print("  Please provide an email address")

    #Return all the info in a list.
    #First element of the list will be replaced later by ID
    return ['ID', center, age, code, 'NEW', name, contactNumber, email]


def generateId():

    #Try to get the last ID by reading the file in reverse
    try:
        filePatient = open("patients.txt", "r")     #Open file for reading

        for line in reversed(list(filePatient)):    #read the line of file in reverse
            lastId = int(line.split()[0])           #read the first word of last line
            break

        filePatient.close()                         #Close file
    #If the file does not exist then set it to zero
    except:
        lastId = 0


    Id = lastId + 1     #Next ID
    Id = str(Id)        #Convert it to string
    Id = Id.zfill(6)    #Add zeroes to make ID a six digit number

    return Id



def writePatientData(patient):

    #Open file for appending
    filePatient = open("patients.txt", "a")

    #Print Header Row for the first time
    if(patient[0] == "1".zfill(6)):
        filePatient.write("ID\tCenter\tAge\tVaccine\tStatus\tName\tContact Number\tEmail\n")

    #Write ever info about patient with TAB between them
    for info in patient:
        filePatient.write(str(info))
        filePatient.write("\t")

    #Insert a new line
    filePatient.write("\n")

    #Close file
    filePatient.close()

    #Print patient information for confirmation
    print("\n  New patient registered successfully\n")
    print("  ID:", patient[0])
    print("  Name:", patient[5])
    print("  Age:", str(patient[2]), "Y")
    print("  Center: VC" + patient[1])
    print("  Vaccine:", patient[3])
    print("  Status:", patient[4])
    print("  Contact Number:", patient[6])
    print("  Email:", patient[7])
    print("")



def administration():
    print("\nVACCINE ADMINISTRATION MENU:\n")

    #Read all patient data from patients.txt inside of patients 2D list
    patients = readAllPatientData()

    #If its empty return to home menu
    if (patients == None):
        return

    #Get the ID of the patient who came to take their first/second dose
    Id = getPatientId(patients)

    #Print patient info for confirmation
    printPatientInfo(patients, Id)

    #If the patient completed vaccination already return to home menu
    if (patients[int(Id)][4] == 'COMPLETED'):
        print("\n  Vaccination Completed already\n")
        return

    #Update the Status of the specific patient inside of patients 2D list
    patients[int(Id)] = updatePatientStatus(patients[int(Id)])

    #Rewrite the patients.txt using patients 2D list
    writeAllPatientData(patients)

    #Update vaccination.txt
    updateVaccineData(patients[int(Id)])


def readAllPatientData():

    #Try opening patients.txt file
    try:
        filePatient = open("patients.txt", "r")
    except:
        print("  Zero patient registered so far.")
        return None

    #Initialize patients list
    patients = []

    #Update the patients 2D list with all data from patientx.txt
    for line in filePatient:
        patient = []

        for info in line.split("\t"):
            patient.append(info.rstrip())
        patients.append(patient)

    filePatient.close()

    return patients


def getPatientId(patients):
    #INPUT - Patient ID
    while(True):
        Id = input("  Enter patient ID: ")
        if(len(Id) == 6):
            try:
                if(int(Id) > 0 and int(Id) < len(patients)):
                    break
                else:
                    print("  Invalid ID. ID does not exist. Try again.\n")
            except:
                print("  Invalid ID. ID should be a six digit number. Try again.\n")
        else:
            print("  Invalid ID. ID should be a six digit number. Try again.\n")

    return Id


def printPatientInfo(patients, Id):
    patient = patients[int(Id)]

    print("\n  Patient Information:")
    print("    ID: " + patient[0])
    print("    Name: " + patient[5])
    print("    Age: " + patient[2] + " Y")
    print("    Vaccine: " + patient[3])
    print("    Current Status: " + patient[4])

def updatePatientStatus(patient):
    if(patient[4] == 'COMPLETED-D1'):
        patient[4] = 'COMPLETED'
        print("\n  Status Updated to 'COMPLETED'\n")
        return patient
    
    if(patient[4] == 'NEW' and patient[3] == 'AF'):
        patient[4] = 'COMPLETED-D1'
        print("\n  Status Updated to 'COMPLETED-D1'")
        print("  Please come back after 2 weeks for second dose\n")
        return patient
    
    if(patient[4] == 'NEW' and patient[3] == 'BV'):
        patient[4] = 'COMPLETED-D1'
        print("\n  Status Updated to 'COMPLETED-D1'")
        print("  Please come back after 3 weeks for second dose\n")
        return patient
    
    if(patient[4] == 'NEW' and patient[3] == 'CZ'):
        patient[4] = 'COMPLETED-D1'
        print("\n  Status Updated to 'COMPLETED-D1'")
        print("  Please come back after 3 weeks for second dose\n")
        return patient
    
    if(patient[4] == 'NEW' and patient[3] == 'DM'):
        patient[4] = 'COMPLETED-D1'
        print("\n  Status Updated to 'COMPLETED-D1'")
        print("  Please come back after 4 weeks for second dose\n")
        return patient
    
    if(patient[4] == 'NEW' and patient[3] == 'EC'):
        patient[4] = 'COMPLETED'
        print("\n  Status Updated to 'COMPLETED'\n")
        return patient



def writeAllPatientData(patients):
    filePatient = open("patients.txt", "w")

    for patient in patients:
        for info in patient:
            filePatient.write(str(info))
            filePatient.write("\t")

        filePatient.write("\n")

    filePatient.close()

def updateVaccineData(patient):
    fileVaccine = open("vaccination.txt", "a")

    fileVaccine.write(patient[1] + "\t")    #Center
    fileVaccine.write(patient[3] + "\t")    #Vaccine
    fileVaccine.write(patient[0] + "\t")    #ID
    fileVaccine.write(patient[4] + "\n")    #Status

    fileVaccine.close()

def search():
    print("\nSEARCH MENU:\n")

    #OPEN file
    try:
        filePatient = open("patients.txt", "r")
        next(filePatient)
    except:
        print("  Zero patient registered so far\n")
        return

    #INPUT - Search Keyword
    searchKey = input("  Enter Search Keyword: ")

    #PRINT - header row
    print("\n  ID\t\tCenter\tAge\tVaccine\tStatus\tName\tContact Number\tEmail")

    #Keep track of the match found
    matchFound = 0

    #Iterate through every line in the file
    #If match found, print the line and increase matchFound
    for line in filePatient:
        line = line.rstrip()

        if searchKey.lower() in line.lower():
            print("  " + line)
            matchFound += 1

    #PRINT - found matches
    print("\n  Total Match Found = ", matchFound, "\n")

    #CLOSE file
    filePatient.close()

def statistics():
    print("\nSTATISTICAL INFORMATION:\n")

    #Read all data from vaccinations.txt into vaccinations list
    vaccinations = readAllVaccinationData()

    #if the list is empty return to home menu
    if(vaccinations == None):
        return

    #Print 3 statatistics table: Center 1, Center 2, Total
    printStat(vaccinations, 'VC1')
    printStat(vaccinations, 'VC2')
    printStat(vaccinations, 'TOTAL')

def readAllVaccinationData():
    #Initializing an empty list
    vaccinations = []
    
    #OPEN file for reading
    try:
        fileVaccine = open("vaccination.txt", "r")
    except:
        print("  Zero patient vaccinated so far")
        return None

    #Iterate through every line in the file
    #Convert line into lists
    for line in fileVaccine:
        vaccination = []

        for info in line.split("\t"):
            vaccination.append(info.rstrip())

        vaccinations.append(vaccination)

    #CLOSE file
    fileVaccine.close()

    return vaccinations

def printStat(vaccinations, center):
    #Initialize the data with header row and necessary info
    data = []

    data.append(["\t", "AF", "BV", "CZ", "DM", "EC"])
    data.append(["COMPLETED-D1", 0, 0, 0, 0, 0])
    data.append(["COMPLETED", 0, 0, 0, 0, 0])
    data.append([center + "\t", 0, 0, 0, 0, 0])

    #Update the number inside of data
    for vaccination in vaccinations:
        if(center[2] == vaccination[0] or center == 'TOTAL'):
            if(vaccination[1] == 'AF'):
                if(vaccination[3] == 'COMPLETED-D1'):
                    data[1][1] += 1
                else:
                    data[2][1] += 1
                    data[1][1] -= 1

            elif(vaccination[1] == 'BV'):
                if(vaccination[3] == 'COMPLETED-D1'):
                    data[1][2] += 1
                else:
                    data[2][2] += 1
                    data[1][2] -= 1

            elif(vaccination[1] == 'CZ'):
                if(vaccination[3] == 'COMPLETED-D1'):
                    data[1][3] += 1
                else:
                    data[2][3] += 1
                    data[1][3] -= 1

            elif(vaccination[1] == 'DM'):
                if(vaccination[3] == 'COMPLETED-D1'):
                    data[1][4] += 1
                else:
                    data[2][4] += 1
                    data[1][4] -= 1

            elif(vaccination[1] == 'EC'):
                data[2][5] += 1

    #Add the numbers
    for i in range(1, 6):
        data[3][i] = data[1][i] + data[2][i]

    #Print 3 rows
    for line in data[0:3]:
        print("  ", end="")

        for info in line:
            print(info, end="\t")

        print("")

    #Print a dashed line
    print("  " + "-"*50)

    #Print the sum
    print("  ", end="")
    for info in data[3]:
        print(info, end="\t")

    print("\n")



print("Welcome to COVID-19 Vaccination Record Management System\n")
menu()

