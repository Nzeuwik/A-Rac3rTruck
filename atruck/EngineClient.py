import cStringIO
import logging
import json
from requests import post, codes
from PIL import Image
from ProbeDaemon import ProbeDaemon
from CommandFactory import CommandFactory


class NoServerException(Exception):
    pass


class FailedRequestException(Exception):
    pass


class EngineClient(object):
    def __init__(self, server_url, port, endpoint="/process"):
        self.process_url = "{url}:{port}{endpoint}"\
            .format(url=server_url, port=port, endpoint=endpoint)
        self.probe = ProbeDaemon(server_url, port)
        self.probe.start()
        logging.debug("EngineClient running")

    def get_command(self, im_bgr, timestamp_s, status):
        logging.debug("Get command client")
        if not self.probe.up():
            raise NoServerException("Server {url} not available".format(url=self.process_url))

        im_buffer = self.get_im_buffer(im_bgr)
        json_data = self.get_data_json(status, timestamp_s)
        request = post(self.process_url,
                       files={'file': im_buffer,
                              'data': json_data}
                       )
        if request.status_code != codes.ok:
            raise FailedRequestException("Response: {r}".format(r=request.text))

        cmd = request.json()
        logging.info("Received json: ", cmd)
        return CommandFactory.from_dict(cmd)

    @staticmethod
    def get_im_buffer(im_bgr):
        pil_image = Image.fromarray(im_bgr)
        im_buffer = cStringIO.StringIO()
        pil_image.save(im_buffer, format='JPEG')
        im_buffer.seek(0)
        return {'file': im_buffer}

    @staticmethod
    def get_data_json(status, timestamp_s):
        data = dict()
        data["image_timestamp_ms"] = int(timestamp_s * 1000)
        data["status"] = status.to_dict()
        return json.dumps(data)
