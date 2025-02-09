import json
import logging

import psycopg
import requests
import tornado

from orderapi import sql_queries
from orderapi.config import Config, construct_db_string
from orderapi.redis import RedisUtil
from orderapi.utils import decode_json


PDFGEN_ENDPOINT = "/v1/pdfgen"


class OrderHandler(tornado.web.RequestHandler):
    def prepare(self):
        self.db_conn = construct_db_string()
        self.store = Config.get_config()['store']
        self.pdfgen = Config.get_config()['pdfgen']
        self.redis = Config.get_config()['cache']

    def write_order_error(self, status, message):
        self.set_status(status)
        self.finish({'msg': message})
        raise tornado.web.HTTPError(status, message)

    def make_new_order(self, req):
        with psycopg.connect(conninfo=self.db_conn,
                             row_factory=psycopg.rows.scalar_row) as conn:
            with conn.cursor() as cur:

                # This context manager block creates a DB transaction session
                # when the first SQL query is executed. The transaction ends
                # when this context block is left. Ending the transaction means
                # releasing the lock which is acquired after the first line of
                # code within this block.

                # lock wanted tables
                cur.execute(sql_queries.LOCK_TABLES)

                # check current stock
                reserved = int(cur.execute(sql_queries.CHECK_STOCK).fetchone())
                if reserved >= self.store['stock']['limit']:
                    self.write_order_error(500, "out_of_stock")

                # ensure order doesn't already exist
                id_exists = cur.execute(sql_queries.CHECK_ID,
                                        (req['order_id'],)).fetchone()
                if id_exists:
                    self.write_order_error(400, "order_exists")

                # ensure user details don't already exist
                user_exists = cur.execute(sql_queries.CHECK_USER,
                                          (req['number'],)).fetchone()
                if user_exists:
                    self.write_order_error(400, "user_exists")

                # insert new order
                cur.execute(sql_queries.INSERT_ID,
                            (req['order_id'], req['number']))

                # increment amount of reserved products
                cur.execute(sql_queries.UPDATE_STOCK, (str(reserved+1),))

            self.set_status(200)
            self.finish(json.dumps({'msg': 'reserved'}))

    def update_cache(self):
        r_client = RedisUtil(self.redis['addr'],
                             self.redis['port'],
                             self.redis['db'])

        r_client.set("stock_available", "false")

    def request_pdf(self, req):
        pdfgen_url = (
            f'http://{self.pdfgen['addr']}:{self.pdfgen['port']}'
            f'{PDFGEN_ENDPOINT}'
        )
        requests.post(pdfgen_url, json.dumps(req))

    def post(self):
        data = decode_json(self.request.body)
        if not data:
            raise tornado.web.HTTPError(400, "No data to process")

        self.make_new_order(data)
        logging.info('Requesting PDF for order %s', data['order_id'])
        self.request_pdf(data)
