import argparse
import asyncio
import logging

import psycopg

from orderapi.config import Config, construct_db_string
from orderapi.orderapi import run_app
from orderapi.redis import RedisUtil
from orderapi.sql_queries import CHECK_STOCK


def get_reserved_count():
    db_str = construct_db_string()
    with psycopg.connect(conninfo=db_str,
                         row_factory=psycopg.rows.scalar_row) as conn:
        with conn.cursor() as cur:
            reserved = int(cur.execute(CHECK_STOCK).fetchone())

    return reserved


def init_redis():
    r_config = Config.get_config()['cache']
    r_client = RedisUtil(r_config['addr'], r_config['port'], r_config['db'])
    reserved_count = get_reserved_count()
    reserved_limit = Config.get_config()['store']['stock']['limit']

    if reserved_count < reserved_limit:
        r_client.set("stock_available", "true")
    else:
        r_client.set("stock_available", "false")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', default='orderapi/config.yaml',
                        required=False)

    arguments = parser.parse_args()
    settings = Config(arguments.config)

    logging.basicConfig(
        format='%(asctime)s - %(levelname)s - %(module)s - %(message)s',
        level=logging.INFO)

    init_redis()
    asyncio.run(run_app())
