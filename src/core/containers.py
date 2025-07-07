from typing import List
from dependency_injector import containers, providers
from src.core.utils import Singleton


class ContainerBuilder(metaclass=Singleton):
    def __init__(self):
        self.containers = []
        self.container = None

    def build(self, _containers: List[dict]):
        self.container = None
        self.containers = _containers
        self.container = containers.DynamicContainer()
        for container in self.containers:
            setattr(
                self.container,
                container['name'],
                providers.Container(container['class']),
            )
        self.container.wire(packages=["src"])
        return self.container
