import sys
import itertools
from typing import List, Dict, Tuple, Any, Iterator, Any

def give_entry_string(filename: str) -> str:
   """
   Generates one line from the given .txt or .csv file
   """
   
   try:
      with open(filename, "r") as file:
         for line in file:
            yield line.strip()
      
   except:
      sys.exit(f"{filename} could not be opened.")
      
       
def remove_header(generator: Iterator) -> Iterator:
   """
   Removes a specified amount of lines from the generator.
   """
   
   previewBuffer = []
   try: #Save first five lines of file content if needed to repair generator
      for _ in range(5):
         previewBuffer.append(next(generator))  
   except StopIteration: #If file < 5 lines, stop saving
      pass
   
   if not previewBuffer:
      return Generator
      
   print("=== FIRST 5 LINES ===") #Give preview for the user to determine buffer length
   for line in previewBuffer:
      print(line)   
   
   headerLength = int(input("Insert header length (type 0 to keep all) : "))
   
   if headerLength < len(previewBuffer): #If header has less line than preview buffer,
      withoutBuffer = previewBuffer[headerLength:] #Remove said header
      return itertools.chain(withoutBuffer, generator) #And glue the remaining pieces together
   
   else: #If header is longer than preview buffer,
      headerOverPreview = headerLength - len(previewBuffer) #Take remaining amount of lines to remove
      del previewBuffer #Then discard previewBuffer entirely
      
      for _ in range(headerOverPreview): #Burn through remaining lines of header
         try:
            next(file_generator)
         except StopIteration: #Stop the loop if generator is emptied
            break

      print()
      return generator
   
   
def get_key_names(
   generator: Iterator, 
   keyNames: List[Tuple[str,str]],
   seperator: str = ","
   ) -> Iterator:
   """
   Obtain key name/data type pairs corresponding to each attribute and saves it to keyNames. Returns repaired generator
   """
   previewItem = [next(generator)] #Save previewed item for later repair
   elementAmount = len(previewItem[0].split(seperator)) #Take the amount of attributes
   
   print("=== ENTRY PREVIEW ===")
   print(previewItem) #Give preview of first entry to aid in choosing key names and data types
   print(f"Attribute amount : {elementAmount}\n")
   
   presetChoice = int(input("Do you wish to load a key/type preset? Type 1 for yes, 0 for no : "))
   
   if presetChoice: 
      filename = input("Enter preset filename:")
      keyPresets = load_presets(filename)
      
      if keyPresets == None:
         sys.exit("Preset file not found.")
         
      validPresets = []
      
      for preset in keyPresets: #Save valids presets considering length of entry
         if len(preset) == elementAmount:
            validPresets.append(preset)
      
      print("Valid presets for this data type are:") #Present valid presents
      for preset in range(len(validPresets)):
         print(f"{preset} : {validPresets[preset]}")
         
      presetNumber = int(input(f"Enter a number between 0 and {len(validPresets)-1} corresponding to the preset you wish to take : "))
      keyNames.extend(validPresets[presetNumber]) #Ask for and save desired preset
      
   else: 
      print("Enter data types as int, float, str or bool.")
      
      for i in range(elementAmount):
         keyName = input(f"Enter key name for element {i+1} : ") #Input dictionary key,
         keyType = input(f"Enter data type for element {i+1} :") #And data type for each attribute
         print()
         keyNames.append((keyName, keyType)) #Save as key/type pair in a tuple.
         
      saveChoice = int(input("Do you wish to save this key/type preset? Type 1 for yes, 0 for no : "))
      if saveChoice: #Ask to save list of key/chain pairs
         filename = input("Enter destination filename : ")
         save_preset(keyNames, filename)
         
   return itertools.chain(previewItem, generator) #Repair generator
   

def convert_to_dicts(
   generator: Iterator, 
   seperator: str, 
   keyNames: List[Tuple[str,str]], 
   listOfDicts: List
   ) -> List[Dict[str, Any]]:
   """
   Convert the strings generated into a list of attributes, then to dicts
   """
   elementAmount = len(keyNames)
   
   for entry in generator: #Gen is iterable object
      
      entryDict = {}
      values = entry.split(seperator) #Seperate string into list of attributes
      
      for attribute in range(elementAmount): #Convert and save every attribute in dictionary
         entryDict[keyNames[attribute][0]] = type_cast(values[attribute], keyNames[attribute][1])
         
      listOfDicts.append(entryDict) #Append to final list
   
  
def save_preset(
   keyNames: List[Tuple[str, str]], 
   filename: str
   ) -> None:
   """
   Saves key name/data type pairs into destination file
   """
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
       
def load_presets(filename: str) -> List[Tuple[str, str]] | None:
   """
   Loads key name/data type pairs from specified filename. Returns None if file is not found.
   """
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
  
def type_cast(value: str, elementType: str) -> Any:
   """
   Casts input values towards the desired data type for ease of use.
   """
   if elementType == 'int':
      return int(value)
      
   elif elementType == 'float':
      return float(value)
   
   elif elementType == 'str':
      return str(value)
   
   elif elementType == 'bool':
      return bool(value)
   
   return str(value)
   

def convert(
   filename: str,
   keyNames: List[Tuple[str, str]],  
   listOfDicts: List,
   seperator: str = ",",
   ) -> List[Dict[str, any]]:
   """
   Converts datasets from a file to a list of dictionaries, guided by user inputs for maximum customizability.
   """
   
   generator = remove_header(give_entry_string(filename))
   get_key_names(generator, keyNames)
   convert_to_dicts(generator, seperator, keyNames, listOfDicts)
