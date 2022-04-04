from typing import Optional, Tuple

from mcdreforged.api.all import *
from parse import parse

from minecraft_version_api import normalizer

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


def get_mcdr_parsed_minecraft_version() -> Optional[str]:
    try:
        return ServerInterface.get_instance().get_server_information().version
    except NameError:
        # MCDR 2.1-
        return None


# API
def get_minecraft_version() -> Optional[Tuple[str, str]]:
    """
    Get the version of the minecraft server
    :return: a tuple contains the raw version name and the normalized version, or None if the plugin failed to fetch the version
    """
    fetched_version = version or get_mcdr_parsed_minecraft_version()
    if fetched_version is None:
        return None
    return version, normalizer.normalize(version)

