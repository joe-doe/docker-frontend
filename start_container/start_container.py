from docker_client.client import client


class ContainersHandler(object):
    def __init__(self):
        pass

    def start_new(self, image):
        client.containers.run(image, detach=True)

    def get_containers_status(self):
        status = {}
        all_containers = client.containers.list(all=True)

        for container in all_containers:
            status[container.name] = container.status

        return status
