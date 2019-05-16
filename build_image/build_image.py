from docker_client.client import client
from docker.errors import BuildError


class ImageHandler(object):
    def __init__(self):
        self.image = None
        self.image_list = None
        self.image_build_output = None

    def build(self, dockerfile_path):
        try:
            self.image, self.image_build_output = \
                client.images.build(path=dockerfile_path,
                                    rm=True)
        except BuildError as build_error:
            for line in build_error.build_log:
                if 'stream' in line:
                    self.image_build_output = (line['stream'].strip())

        return self.image, self.image_build_output

    def get_image(self):
        return self.image

    def get_image_list(self):
        self.image_list = client.images.list()
        return self.image_list

    def get_id(self):
        return self.image.id

    def get_image_by_id(self, id):
        a = client.images.get(id)
        return a

    def set_image(self, image_id):
        self.image = client.images.get(image_id)
