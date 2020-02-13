import os
from python_obfuscator import Obfuscator
from shutil import copy
import ntpath


class ObfuscationFileHandler:

    def __init__(self, obfuscated_folder_path):
        self.obfuscated_folder_path = obfuscated_folder_path

    def run_obfuscator_directory(self, target_path):
        current_dict = {}
        for dir_path, dir_names, file_names in os.walk(target_path):
            obf_folder_path = ntpath.join(self.obfuscated_folder_path, dir_path[len(target_path) + 1:])
            if not os.path.isdir(obf_folder_path):
                os.mkdir(obf_folder_path)
            for filename in file_names:
                if filename.endswith('.py'):
                    obfuscator = Obfuscator(current_dict)
                    obf_code = obfuscator.run_obfuscator(self.__read_source(ntpath.join(dir_path, filename)))
                    current_dict = obfuscator.name_map
                    self.__write_obfuscated_source(obf_code, ntpath.join(obf_folder_path, filename))
                else:
                    copy(ntpath.join(dir_path, filename), ntpath.join(obf_folder_path, filename))

    def run_obfuscator_file(self, target_path):
        assert ntpath.split(target_path)[-1].endswith('.py'), "Not a Valid Python File"
        obfuscator = Obfuscator()
        obf_code = obfuscator.run_obfuscator(self.__read_source(target_path))
        self.__write_obfuscated_source(obf_code, ntpath.join(self.obfuscated_folder_path, target_path))

    def __read_source(self, file_path):
        with open(file_path, "r", encoding='utf-8') as source:
            source_str = source.read()
        return source_str

    def __write_obfuscated_source(self, obfuscated_code, file_path):
        file_name = ntpath.split(file_path)[-1]
        if not ntpath.isdir(self.obfuscated_folder_path):
            os.mkdir(self.obfuscated_folder_path)
        with open(ntpath.join(self.obfuscated_folder_path, file_name), 'w', encoding='utf-8') as obf_file:
            obf_file.write(obfuscated_code)
