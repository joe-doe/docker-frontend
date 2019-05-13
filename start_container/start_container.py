from docker_client.client import client


class ContainersHandler(object):
    def __init__(self):
        self.containers_list = []

    def start_new(self, image):
        new_container = client.containers.run(image, detach=True)
        self.containers_list.append(new_container)
