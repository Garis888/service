from src.modules.service1.containers import containers_dict as monitoring_containers
from src.core.containers import ContainerBuilder

all_containers = []
all_containers.extend(monitoring_containers)

container = ContainerBuilder().build(all_containers)
