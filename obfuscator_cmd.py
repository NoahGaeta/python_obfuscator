import argparse
from obfuscator_source.file_handler import ObfuscationFileHandler


def main():
    arg_parser = argparse.ArgumentParser(description='A python obfuscator that will obfuscate names using the ast library.')
    arg_parser.add_argument('--obfuscated_folder_path', required=True, help='Folder to save obfuscated code in')
    arg_parser.add_argument('--directory', help='Directory containing python files to obfuscate(Can only target either directory or file but not both)')
    arg_parser.add_argument('--file', help='File to obfuscate(Can only target either directory or file but not both)')
    args = arg_parser.parse_args()
    assert_valid_arguments(args)
    obfuscation_handler = ObfuscationFileHandler(args.obfuscated_folder_path)
    if args.directory:
        obfuscation_handler.run_obfuscator_directory(args.directory)
    else:
        obfuscation_handler.run_obfuscator_file(args.file)


def assert_valid_arguments(args):
    assert args.directory or args.file, "No File or Directory provided."
    assert not (args.directory and args.file), "Can only target either directory or file but not both"


if __name__ == '__main__':
    exit(main())
