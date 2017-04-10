import os

from pyven.exceptions.parser_exception import ParserException
from pyven.plugins.plugin_api.parser import Parser

from integration_plugin.integration import Integration

class IntegrationParser(Parser):
    COUNT = 0
    SINGLETON = None
    
    def __init__(self, cwd):
        IntegrationParser.COUNT += 1
        super(IntegrationParser, self).__init__(cwd)
    
    def parse(self, node, project):
        objects = []
        members = self.parse_process(node)
        errors = []
        file = node.find('file').text
        if file == '':
            errors.append('Missing test executable file')
        (path, filename) = os.path.split(file)
        arguments = []
        for argument in node.xpath('arguments/argument'):
            arguments.append(argument.text)
        format = 'cppunit'
        package_nodes = node.xpath('package')
        if len(package_nodes) == 0:
            errors.append('Integration test : missing package')
        if len(package_nodes) > 1:
            errors.append('Integration test : to many packages declared')
            errors.append('Only one package can be added to an integration test')
        package = package_nodes[0].text
        if package is None or package == '':
            errors.append('Integration test : missing package')
        package = project.replace_constants(package)
        if package not in project.packages.keys():
            errors.append('Package not declared --> ' + package)
        if len(errors) > 0:
            e = ParserException('')
            e.args = tuple(errors)
            raise e
        objects.append(Integration(self.cwd, members[0], path, filename, arguments, format, project.packages[package]))
        return objects
        
def get(cwd):
    if IntegrationParser.COUNT <= 0 or IntegrationParser.SINGLETON is None:
        IntegrationParser.SINGLETON = IntegrationParser(cwd)
    IntegrationParser.SINGLETON.cwd = cwd
    return IntegrationParser.SINGLETON