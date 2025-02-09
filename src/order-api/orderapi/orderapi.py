import asyncio
import logging

import tornado

from orderapi.handlers import OrderHandler
from orderapi.config import Config


def make_app():
    return tornado.web.Application([
        (r"/v1/order", OrderHandler)
    ])


async def run_app():
    app_settings = Config.get_config()['api']
    app = make_app()
    app.listen(app_settings['port'])

    logging.info('Order API service start!')

    await asyncio.Event().wait()
