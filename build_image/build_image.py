from docker_client.client import client


class BuildImage(object):
    def __init__(self):
        self.image = None
        self.image_build_output = None

    def build(self, dockerfile_path):
        self.image, self.image_build_output = \
            client.images.build(path=dockerfile_path)
        return self.image, self.image_build_output
