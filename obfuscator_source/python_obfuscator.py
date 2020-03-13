import ast
import random
import string
import astunparse
import builtins


class Obfuscator(ast.NodeTransformer):
    def __init__(self, all_file_names=[], previous_name_map={}):
        self.name_map = previous_name_map
        self.all_file_names = all_file_names
        self.non_obfuscated_names = []

    def run_obfuscator(self, source):
        tree = ast.parse(source)
        self.visit(tree)
        obfuscated_code = astunparse.unparse(tree)
        return obfuscated_code

    def visit_Import(self, node):
        for name in node.names:
            if name.name not in self.all_file_names:
                self.non_obfuscated_names.append(name.name)
                if name.asname:
                    self.non_obfuscated_names.append(name.asname)
        return node

    def visit_ImportFrom(self, node):
        self.generic_visit(node)
        file_name = node.module.split('.')[-1] if node.module else None
        if not file_name:
            return node
        for name in node.names:
            if file_name in self.all_file_names:
                if name.name in self.all_file_names:
                    self.all_file_names.remove(name.name)
                attr = 'asname' if name.asname else 'name'
                obf_name = self.__obfuscate_name(name, attr)
                if obf_name:
                    name.name = obf_name if not name.asname else name.name
                    name.asname = obf_name if name.asname else name.asname
            else:
                self.non_obfuscated_names.append(name.name)
                self.non_obfuscated_names.append(name.asname)
        return node

    def visit_Return(self, node):
        self.generic_visit(node)
        return node

    def visit_FunctionDef(self, node):
        self.generic_visit(node)
        obf_name = self.__obfuscate_name(node, 'name')
        if obf_name:
            return ast.FunctionDef(
                name=obf_name,
                args=node.args,
                body=node.body,
                decorator_list=node.decorator_list,
                returns=node.returns,
            )
        return node

    def visit_arg(self, node):
        self.generic_visit(node)
        obf_name = self.__obfuscate_name(node, 'arg')
        if obf_name:
            return ast.arg(
                arg=obf_name,
                col_offset=node.col_offset,
                lineno=node.lineno,
                annotation=node.annotation
            )
        return node

    def visit_Attribute(self, node):
        self.generic_visit(node)
        if hasattr(node, 'value'):
            if hasattr(node.value, 'id'):
                parent_attr = node.value.id
                if parent_attr and parent_attr not in self.non_obfuscated_names:
                    obf_name = self.__obfuscate_name(node, 'attr')
                    if obf_name:
                        return ast.Attribute(
                            attr=obf_name,
                            value=node.value,
                            ctx=node.ctx
                        )
        return node

    # treat coroutines the same way
    visit_AsyncFunctionDef = visit_FunctionDef

    def visit_ClassDef(self, node):
        self.generic_visit(node)
        obf_name = self.__obfuscate_name(node, 'name')
        if obf_name:
            return ast.ClassDef(
                name=obf_name,
                bases=node.bases,
                keywords=node.keywords,
                body=node.body,
                decorator_list=node.decorator_list
            )
        return node

    def visit_Assign(self, node):
        self.generic_visit(node)
        return node

    def visit_keyword(self, node):
        self.generic_visit(node)
        if hasattr(node, 'value'):
            return node

    def visit_Lambda(self, node):
        # lambdas are just functions, albeit with no statements, so no assignments
        self.generic_visit(node)

    def visit_Global(self, node):
        self.generic_visit(node)
        obf_name = self.__obfuscate_name(node, 'name')
        if obf_name:
            return ast.Global(
                names=obf_name
            )
        return node

    def visit_Name(self, node):
        self.generic_visit(node)
        obf_name = self.__obfuscate_name(node, 'id')
        if obf_name:
            return ast.Name(
                id=obf_name,
                ctx=node.ctx
            )
        return node

    def __random_string_generator(self, str_size):
        """
        :param str_size: Size of string to generate
        :param allowed_chars: Allowed characters
        :return: A random string
        """
        return ''.join(random.choice(string.ascii_letters) for _ in range(str_size))

    def __check_if_obfuscatable(self, name):
        return name in self.non_obfuscated_names or name in self.all_file_names

    def __obfuscate_name(self, node, attr):
        name = getattr(node, attr) if hasattr(node, attr) else None
        built_in = hasattr(builtins, name) if name else False
        if not self.name_map.get(name) and not built_in and not self.__check_if_obfuscatable(name):
            self.name_map.update({name: self.__random_string_generator(15)})
        if name and not built_in and not self.__check_if_obfuscatable(name):
            return self.name_map.get(name)
        return None
