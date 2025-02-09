import io

import minio
import tornado

from fpdf import FPDF

from pdfgen.config import Config
from pdfgen.utils import decode_json


class PDFHandler(tornado.web.RequestHandler):
    def prepare(self):
        self.minio = Config.get_config()['s3']

    def create_pdf_obj(self, req):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('helvetica', size=48)
        pdf.cell(text=f'{req['order_id']}', new_x='LMARGIN', new_y='NEXT')
        pdf.cell(text=f'{req['firstname']} {req['lastname']}',
                 new_x='LMARGIN', new_y='NEXT')
        pdf.cell(text=f'{req['number']}')

        pdf_buffer = io.BytesIO(pdf.output())
        pdf_buffer.seek(0)

        return pdf_buffer

    def put_to_minio(self, obj, target, cont_type):
        endpoint = f'{self.minio['addr']}:{self.minio['port']}'

        minio_client = minio.Minio(endpoint,
                                   self.minio['access_key'],
                                   self.minio['secret_key'],
                                   secure=self.minio['secure'])

        minio_client.put_object(
            self.minio['bucket'],
            target,
            data=obj,
            length=obj.getbuffer().nbytes,
            content_type=cont_type
        )

    def post(self):
        data = decode_json(self.request.body)
        if not data:
            raise tornado.web.HTTPError(400, "No data to process")

        filename = f'{data['order_id']}.pdf'

        pdf_bytes = self.create_pdf_obj(data)
        self.put_to_minio(pdf_bytes, filename, 'application/pdf')
