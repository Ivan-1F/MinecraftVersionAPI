from typing import Optional

from mcdreforged.api.all import *
from parse import parse


version: Optional[str] = None


def on_info(server: PluginServerInterface, info: Info):
    global version
    if not info.is_user:
        result = parse('Starting minecraft server version {version}', info.content)
        if result:
            server.logger.info('Minecraft version fetched: {}'.format(result['version']))
            version = result['version']


def on_load(server: PluginServerInterface, old):
    if old is not None:
        global version
        version = old.version


# API
def get_minecraft_version() -> Optional[str]:
    """
    Get the version of the minecraft server
    :return:
    """
    return version
