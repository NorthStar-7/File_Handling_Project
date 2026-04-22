import sys

def save_to_list(filename):
   #Converts .csv or .txt files to a list of unformatted strings
   listOfEntries = [] 
   try:
      with open(filename, "r") as file:
         for line in file:
            listOfEntries.append(line.strip())
      
   except FileNotFoundError:
      sys.exit("File not found.")
      
   return listOfEntries
        

def convert_list(listOfEntries):
   #Converts list of strings to list of lists of values (being entry elements/attribute values)
   remove_header(listOfEntries)v
   
   listOfElements = []
   seperator = input("Enter seperator string (e.g: ','):")
   for entry in listOfEntries:
      values = entry.split(seperator)
      listOfElements.append(values)
      
   return listOfElements


def remove_header(listOfEntries):
   print("Printing the first five lines of your dataset:")
   for i in range(5):
      print(listOfEntries[i])
      
   print("How many lines does the header take?")
   headerLength = int(input("Enter a value >= 0 here : "))
   
   if headerLength > 0:
      del listOfEntries[:headerLength]
   
def get_key_names(listOfElements):
   #Asks for key name and data type for each attribute in an entry
   
   elementAmount = len(listOfElements[0])
   
   presetChoice = int(input("Do you wish to load a key/type preset? Type 1 for yes, 0 for no : "))
   if presetChoice:
      filename = input("Enter preset filename:")
      keyPresets = load_presets(filename)
      if keyPresets == None:
         sys.exit("Preset file not found.")
         
      validPresets = []
      
      for preset in keyPresets:
         if len(preset) == elementAmount:
            validPresets.append(preset)
      
      print("Valid presets for this data type are:")
      for preset in range(len(validPresets)):
         print(f"{preset} : {validPresets[preset]}")
         
      presetNumber = int(input(f"Enter a number between 0 and {len(validPresets)} corresponding to the preset you wish to take."))
      keyNames = validPresets[presetNumber]
      
   else:
      keyNames = []
      print(f"\nYou will need to input {elementAmount} unique key names for your dictionary.")
      print("Enter data types as int, float, str or bool.")
      print("Here is a sample entry of your dataset:")
      print(listOfElements[1])
      print()
      
      for i in range(elementAmount):
         keyName = input(f"Enter key name for element {i+1} : ")
         keyType = input(f"Enter data type for element {i+1} :")
         print()
         keyNames.append((keyName, keyType))
         
      saveChoice = int(input("Do you wish to save this key/type preset? Type 1 for yes, 0 for no : "))
      if saveChoice:
         filename = input("Enter destination filename:")
         save_preset(keyNames, filename)
      
   return keyNames


def type_cast(value, elementType):
   if elementType == 'int':
      return int(value)
      
   elif elementType == 'float':
      return float(value)
   
   elif elementType == 'str':
      return str(value)
   
   elif elementType == 'bool':
      return bool(value)
   

def save_preset(keyNames, filename):
   try:
      with open(filename, "a") as file:
         pairs = "\n"
         
         for key, dType in keyNames:
            pairs += f"{key}/{dType},"
            
         pairs = pairs[:-1] #remove last comma
         file.write(pairs)
         
   except: 
      with open(filename, "w") as file:
         pairs = "\n"
         
         for key, dType in keyNames:
            pairs += f"{key}/{dType},"
            
         pairs = pairs[:-1] #remove last comma
         file.write(pairs)
         
         
def load_presets(filename):
      try: 
         with open(filename, "r") as file:
            keyPresets = []
            for line in file:
               keyNames = []
               pairs = line.strip().split(",")
               
               for pair in pairs:
                  keyName, keyType = pair.split("/")
                  keyNames.append((keyName, keyType))
                  
               keyPresets.append(keyNames)
               
         return keyPresets
                  
      except:
         return None


def save_to_dicts(keyNames, listOfElements):
   listOfDicts = []
   elementAmount = len(keyNames)
   
   for entry in listOfElements:
      entryDict = {}
      for i in range(elementAmount):
         entryDict[keyNames[i][0]] = type_cast(entry[i], keyNames[i][1])
      listOfDicts.append(entryDict)
         
   return listOfDicts

students = save_to_list("data.txt")
students = convert_list(students)
keyNames = get_key_names(students)
students = save_to_dicts(keyNames, students)

for i in range(5):
   print(students[i])
      