class Monitor(object):
    def __init__(self, containers_handler):
        self.containers_handler = containers_handler

    def get_status(self):
        running_containers = self.containers_handler.get_containers(all_containers=False)
        info = {}

        for container in running_containers:
            info[container.name] = str(next(container.stats()))

        return info
