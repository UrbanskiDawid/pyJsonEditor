"""
Callable methods for replacing nodes
"""
import os

def build_node_modify_action(file_name_or_string):
    """
    select NodeModifyActionByCode or NodeModifyActionByString
    """
    if NodeModifyActionByCode.check(file_name_or_string):
        return NodeModifyActionByCode(file_name_or_string)

    if NodeModifyActionByString.check(file_name_or_string):
        return NodeModifyActionByString(file_name_or_string)

    raise ValueError('unknown file_name_or_string')


class NodeModifyActionByCode:
    """
    action to perform on node:
    replace node with result of code execution:
    a pyton3 file with 'modif(node)' method that returns string
    """
    def __init__(self, template_code_file_name):
        self.code = self.compile_template_file(template_code_file_name)

    @staticmethod
    def check(file_name_or_string):
        """ check if this class can be build with this arg"""
        return isinstance(file_name_or_string, str) and \
               file_name_or_string.endswith('.py') and \
               os.path.isfile(file_name_or_string)

    @staticmethod
    def compile_template_file(file_name):
        """
        compile code from template file
        add 'modify' method calling
        """
        with open(file_name) as file:
            code = compile( file.read()+
                            '\nmodify_ret_val = modify(node,context)',
                            "template code",
                            'exec')
        return code

    def __call__(self, node, context):
        env = {'modify_ret_val':"",
               'node': node,
               'context': context}
        exec(self.code, {}, env)
        return env['modify_ret_val']


class NodeModifyActionByString:
    """
    action to perform on node:
    replace node with predefined string.
    """
    def __init__(self, template_str):
        self.template = template_str

    @staticmethod
    def check(file_name_or_string):
        """ check if this class can be build with this arg"""
        return isinstance(file_name_or_string, str)

    def __call__(self, _node, _context):
        return self.template
