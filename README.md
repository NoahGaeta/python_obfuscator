# **python_obfuscator**

### **Description:**
A Simple Python Obfuscator

### **Overview:**
```
usage: obfuscator_cmd.py [-h] --obfuscated_folder_path OBFUSCATED_FOLDER_PATH
                         [--directory DIRECTORY] [--file FILE]

A python obfuscator that will obfuscate names using the ast library. 

optional arguments:
  -h, --help            show this help message and exit
  --obfuscated_folder_path OBFUSCATED_FOLDER_PATH
                        Folder to save obfuscated code in
  --directory DIRECTORY
                        Directory containing python files to obfuscate(Can
                        only target either directory or file but not both)
  --file FILE           File to obfuscate(Can only target either directory or
                        file but not both)
```

### **To Do:**

- [ ] Allow for obfuscation with non-latin characters

- [ ] Add a setup.py file for pip package installation

- [ ] Do not obfuscate imports when targeting a file directly

- [ ] Allow to exclude files/directories for obfuscation
