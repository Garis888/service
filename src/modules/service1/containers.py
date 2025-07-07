from dependency_injector import containers, providers
from .gw.cpe_gw import CpeGW


class GWContainer(containers.DeclarativeContainer):
    cpe_gw = providers.Factory(
        CpeGW
    )


containers_dict = [
    {'name': 'cpe', 'class': GWContainer},
]
