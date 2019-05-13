from docker_client.client import client


class ImageHandler(object):
    def __init__(self):
        self.image = None
        self.image_list = None
        self.image_build_output = None

    def build(self, dockerfile_path):
        self.image, self.image_build_output = \
            client.images.build(path=dockerfile_path,
                                rm=True)
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
