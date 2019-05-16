from docker_client.client import client
import multiprocessing as mp
import time
from docker.errors import APIError


class ContainersHandler(object):
    def __init__(self, db):
        self.db = db
        self.running_containers = mp.Manager().list()
        self.running_containers_lock = mp.Lock()

        update_running = mp.Process(target=self.update_running_container_list)
        update_running.start()

    def update_running_container_list(self):
        lock = mp.Lock()

        while True:
            currently_running_containers = self.get_containers(all_containers=False)
            for running_container in currently_running_containers:
                if running_container not in self.running_containers:
                    self.running_containers.append(running_container)

                    p = mp.Process(
                        target=self.update_log,
                        args=(running_container, lock)
                    )
                    p.daemon = True
                    p.start()

            time.sleep(2)

    def start_new(self, image):
        client.containers.run(image, detach=True)

    def get_containers(self, all_containers):
        with self.running_containers_lock:
            container_list = client.containers.list(all=all_containers)
        return container_list

    def get_containers_status(self):
        status = {}
        all_containers = self.get_containers(all_containers=True)

        for container in all_containers:
            status[container.name] = container.status

        return status

    def update_log(self, container, lock):
        print("Watching: {}".format(container.name))
        try:
            log_generator = container.logs(stream=True, follow=True)
        except APIError as api_error:
            print("The docker API server returned error: " + api_error.explanation)
            return

        while container.status == 'running':
            try:
                entry = next(log_generator)
            except StopIteration:
                # self.running_containers.remove(container)
                print(container.name+" log stream STOPPED")
                break
            with lock:
                self.db.entry.insert({container.name: str(entry)})
            print(container.name, entry)
            time.sleep(0.5)
        if container in self.running_containers:
            self.running_containers.remove(container)
