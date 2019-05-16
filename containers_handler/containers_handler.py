import copy
import multiprocessing as mp
from docker.errors import APIError

from docker_client.client import client


class ContainersHandler(object):
    def __init__(self):
        self.lock = mp.Lock()

    def start_new(self, image):
        container = client.containers.run(image, detach=True)

        p = mp.Process(
            target=self.consolidate_log,
            args=(container, )
        )
        p.start()

    def get_containers(self, all_containers):
        return client.containers.list(all=all_containers)

    def get_containers_status(self):
        status = {}
        all_containers = self.get_containers(all_containers=True)

        for container in all_containers:
            status[container.name] = container.status

        return status

    def get_logs(self):
        all_logs = {}
        for running_container in self.get_containers(all_containers=False):
            all_logs[running_container.name] = running_container.logs().decode("utf-8").split('\n')

        return all_logs

    def consolidate_log(self, container):
        container_copy = copy.deepcopy(container)

        try:
            log_generator = container_copy.logs(stream=True, follow=True)
        except APIError as api_error:
            print("The docker API server returned error: " + api_error.explanation)
            return

        while True:
            try:
                entry = next(log_generator)
            except StopIteration:
                print(container.name+" log stream STOPPED")
                break
            with self.lock:
                write_this = container_copy.name + ': ' + entry.decode("utf-8")
                self.write_to_log_file(write_this)

    def write_to_log_file(self, entry):
        with open('logs.txt', 'a') as log_file:
            log_file.write(entry)

    def read_log_file(self):
        with self.lock:
            with open('logs.txt', 'r') as log_file:
                response = log_file.readlines()
        return response
