#leer archivo desde ruta local
#https://docs.python.org/es/3/tutorial/inputoutput.html#reading-and-writing-files

#leer el archivo de información del cliente
#https://www.w3schools.com/python/python_file_open.asp

#encontrar marcadores
#https://www.programiz.com/python-programming/regex
#usar llm 

#reemplazar marcadores 
#https://docs.python.org/es/3/library/re.html#re.sub

#crear nuevo archivo
#https://docs.python.org/es/3/tutorial/inputoutput.html#reading-and-writing-files

import re

file_path = 'backend/app/core/graph/skills/markers/template.txt'
file_path2 = 'backend/app/core/graph/skills/markers/template.txt'
file_path3 = 'backend/app/core/graph/skills/markers/schema.txt'

#open 1st file
with open(file_path, 'r', encoding="utf-8") as f:
   for line in range(5):
        line = f.readline()   
        print(line, end='')
f.closed

#open 2nd file 
f = open(file_path2, "r")
print(f.read(20))
f.close

#patterns
file_path = 'backend/app/core/graph/skills/markers/template.txt'
pattern_a = r'\{{([a-zA-Z_]+)\}}'

a_values = []

with open(file_path, 'r') as file:
 for line in file:
  matches_a = re.findall(pattern_a, line)
  a_values.extend(matches_a) 
  
print("A values:", a_values) 

#save markers
with open(file_path3, 'w') as file:
  for valores in a_values:
      file.write(valores + '\n')

