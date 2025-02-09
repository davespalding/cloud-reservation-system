import argparse
import asyncio
import logging

from pdfgen.pdfgen import run_app
from pdfgen.config import Config


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', default='pdfgen/config.yaml',
                        required=False)

    arguments = parser.parse_args()
    settings = Config(arguments.config)

    logging.basicConfig(
        format='%(asctime)s - %(levelname)s - %(module)s - %(message)s',
        level=logging.INFO)

    asyncio.run(run_app())
