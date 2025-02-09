import asyncio
import logging

import tornado

from pdfgen.config import Config
from pdfgen.handlers import PDFHandler


def make_app():
    return tornado.web.Application([
        (r"/v1/pdfgen", PDFHandler)
    ])


async def run_app():
    app_settings = Config.get_config()['service']
    app = make_app()
    app.listen(app_settings['port'])

    logging.info('PDF generator service start!')

    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(run_app())
