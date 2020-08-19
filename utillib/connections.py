from utillib.util import *
from utillib.dbapiutil import *
import importlib

def load_connection_from_file(name, return_dbapi = False):
    conf_tree = get_config_tree()
    conn_elements = conf_tree.findall('./db_connections/conn')
    for conn_element in conn_elements:
        if conn_element.attrib['name'] == name:
            module_name = conn_element.attrib['module'] # can be used for other modules like cx_Oracle, sqlLite etc
            kwargs = {}
            for arg_el in conn_element.findall('./arg'):
                kwargs[arg_el.attrib['name']] = (
                    arg_el.attrib['value']
                    if arg_el.attrib.get('enc') != '1'
                    else
                    decrypt(arg_el.attrib['value'])
                )

            startup_query = [el.text for el in conn_element.findall('./startupquery')]

            if not return_dbapi:
                result = connect(lambda: importlib.import_module(module_name).connect(**kwargs),startup_query)

            else:
                result = Connection(importlib.import_module(module_name).connect(**kwargs),startup_query)

            return result


def get_test_conn():
    return load_connection_from_file('test')

def get_etl_conn():
    return load_connection_from_file('etl')




