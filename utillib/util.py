import os
import logging

LOGGER = logging.getLogger(__name__)

def get_config_tree():
    import xml.etree.ElementTree as ET

    CONFIG_PATH = os.environ['CONF_FILE']
    tree = ET.parse(CONFIG_PATH)

    return tree

def get_conf_dict():
    conf_dict = {}
    for elem in get_config_tree().findall(r"./variable"):

        conf_dict[elem.attrib['name']] = elem.find("value").text

    return conf_dict


def get_conf_value(name):
    value = get_conf_dict()[name]
    LOGGER.info('Loaded from config file : {} = {}'.format(name, value))
    return value


class FernetEnc():
    """ Ecrypting/decrypting class"""

    def __init__(self):
        from cryptography.fernet import Fernet
        with open(get_conf_dict()['ENCRYPRTION_KEY_FILE'], 'rb') as key_file:
            self.key = key_file.read()

        self.fernet = Fernet(self.key)

    def encrypt(self, value):
        enc = self.fernet.encrypt(str.encode(value))
        return enc.decode()

    def decrypt(self, enc):
        raw = self.fernet.decrypt(str.encode(enc))
        return raw.decode()


def encrypt(raw):
    return FernetEnc().encrypt(raw)

def decrypt(enc):
    return FernetEnc().decrypt(enc)





