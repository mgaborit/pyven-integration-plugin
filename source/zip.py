import zipfile, os
import integration_plugin.constants

def zip_pvn():
    if not os.path.isdir(os.path.join(os.environ.get('PVN_HOME'), 'plugins')):
        os.makedirs(os.path.join(os.environ.get('PVN_HOME'), 'plugins'))
    zf = zipfile.ZipFile(os.path.join(os.environ.get('PVN_HOME'), 'plugins', 'integration-plugin_' + integration_plugin.constants.VERSION + '.zip'), mode='w')
    
    zf.write('__init__.py')
    
    zf.write('integration_plugin/__init__.py')
    zf.write('integration_plugin/constants.py')
    zf.write('integration_plugin/parser.py')
    zf.write('integration_plugin/integration.py')
    
if __name__ == '__main__':
    zip_pvn()
