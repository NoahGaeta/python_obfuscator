import os
from obfuscator_source.python_obfuscator import Obfuscator
from shutil import copy
import ntpath


class File:
    def __init__(self, file_path, new_file_path):
        self.file_path = file_path
        self.extension = self.__extract_file_extension()
        self.file_name = self.__extract_file_name()
        self.new_file_path = new_file_path

    def is_python_file(self):
        return self.extension == '.py'

    def copy_to_new_path(self):
        copy(self.file_path, self.new_file_path)

    def __extract_file_extension(self):
        file_name = ntpath.basename(self.file_path)
        return ntpath.splitext(file_name)[1]

    def __extract_file_name(self):
        file_name = ntpath.basename(self.file_path)
        return ntpath.splitext(file_name)[0]


class ObfuscationFileHandler:

    def __init__(self, obfuscated_folder_path):
        self.obfuscated_folder_path = obfuscated_folder_path

    def run_obfuscator_directory(self, target_path):
        current_dict = {}
        obfuscatable_list = self.__collect_all_files(target_path)

        import_list = list(map(lambda x: x.file_name, obfuscatable_list))

        for file_object in obfuscatable_list:
            obfuscator = Obfuscator(import_list, current_dict)
            obf_code = obfuscator.run_obfuscator(self.__read_source(file_object.file_path))
            current_dict = obfuscator.name_map
            self.__write_obfuscated_source(obf_code, file_object.new_file_path)

    def run_obfuscator_file(self, target_path):
        assert ntpath.split(target_path)[-1].endswith('.py'), "Not a Valid Python File"
        obfuscator = Obfuscator()
        obf_code = obfuscator.run_obfuscator(self.__read_source(target_path))
        self.__write_obfuscated_source(obf_code, target_path)

    def __collect_all_files(self, target_path):
        obfuscatable_list = []
        for dir_path, dir_names, file_names in os.walk(target_path):
            obf_folder_path = ntpath.join(self.obfuscated_folder_path, dir_path[len(target_path) + 1:])
            self.__verify_directory(obf_folder_path)
            for file_name in file_names:
                file_object = File(ntpath.join(dir_path, file_name), ntpath.join(obf_folder_path, file_name))
                if file_object.is_python_file():
                    obfuscatable_list.append(file_object)
                else:
                    file_object.copy_to_new_path()
        return obfuscatable_list

    def __verify_directory(self, obf_folder_path):
        if not os.path.isdir(obf_folder_path):
            os.mkdir(obf_folder_path)

    def __read_source(self, file_path):
        with open(file_path, "rb") as source:
            source_str = source.read()
        return source_str

    def __write_obfuscated_source(self, obfuscated_code, target_path):
        print(target_path)
        with open(target_path, 'w', encoding='utf-8') as obf_file:
            obf_file.write(obfuscated_code)
