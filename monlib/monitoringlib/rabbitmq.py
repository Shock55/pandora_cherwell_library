import logging

from pyrabbit.api import Client


logger = logging.getLogger(__name__)


class RabbitmqMonitor:
    def __init__(self, host: str, port: int, user: str, passwd: str, thershold: int):
        logger.info("Init Base for RabbitmqMonitor")
        super().__init__(module = 'rabbitmq')
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.thershold = thershold
        self.cl = Client(
                "{}:{}".format(self.host, self.port),
                self.user,
                self.passwd)

    def list_queues(self, pandora_mode: bool = True):
        logger.info("List current RabbitMq ques.")
        for e in self.cl.get_queues():
            if pandora_mode:
                if e.get('messages') > self.thershold:
                    print("ERROR | {} | {}".format(e.get('name'), e.get('messages')))
            else:
                logger.info("cue name: {} | cue size: {}".format(
                    e.get('name'),
                    e.get('messages')))
