import os
from flask import Flask, request
from werkzeug.utils import secure_filename
import easyocr
from flask_restx import Api, Resource, fields
from werkzeug.datastructures import FileStorage
import re
import datetime

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize EasyOCR for Arabic + English
reader = easyocr.Reader(['ar', 'en'], gpu=False)

api = Api(app, version='1.0', title='CNI OCR API',
          description='API for OCR extraction from Arabic CNI images')

ns = api.namespace('ocr', description='OCR operations')

upload_parser = api.parser()
upload_parser.add_argument('cni_image', location='files',
                          type=FileStorage, required=True, help='CNI image file (png, jpg, jpeg)')

ocr_result_model = api.model('OCRResult', {
    'extracted_text': fields.List(fields.String, description='List of extracted text lines'),
    'expiry_date': fields.String(description='Extracted expiry date (تاريخ الإنتهاء)'),
    'identifier_number': fields.String(description='Extracted identifier number (رقم التعريف)'),
    'id_valid': fields.Boolean(description='Is identifier number valid'),
    'expiry_valid': fields.Boolean(description='Is expiry date valid'),
    'is_card_valid': fields.Boolean(description='Is card valid'),
    'status': fields.String(description='Verification status')
})

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_expiry_and_identifier(ocr_lines):
    expiry_date = ''
    identifier_number = ''
    for idx, line in enumerate(ocr_lines):
        # Extract expiry date
        if 'الإنتهاء' in line:
            date_match = re.search(r'(\d{2,4}[./-]\d{1,2}[./-]\d{1,4})', line)
            if date_match:
                expiry_date = date_match.group(1)
            else:
                if idx + 1 < len(ocr_lines):
                    date_match = re.search(r'(\d{2,4}[./-]\d{1,2}[./-]\d{1,4})', ocr_lines[idx+1])
                    if date_match:
                        expiry_date = date_match.group(1)
                if not expiry_date and idx - 1 >= 0:
                    date_match = re.search(r'(\d{2,4}[./-]\d{1,2}[./-]\d{1,4})', ocr_lines[idx-1])
                    if date_match:
                        expiry_date = date_match.group(1)
        # Extract identifier number (18 digits)
        if 'رقم التعريف' in line:
            id_match = re.search(r'(\d{18})', line)
            if id_match:
                identifier_number = id_match.group(1)
            else:
                idx = ocr_lines.index(line)
                if idx + 1 < len(ocr_lines):
                    id_match = re.search(r'(\d{18})', ocr_lines[idx+1])
                    if id_match:
                        identifier_number = id_match.group(1)
        if not identifier_number:
            id_match = re.search(r'(\d{18})', line)
            if id_match:
                identifier_number = id_match.group(1)
    return expiry_date, identifier_number

def is_valid_identifier(identifier):
    return bool(re.fullmatch(r'^\d{18}$', identifier))

def parse_date(date_str):
    # Try parsing with different formats
    for fmt in ("%Y.%m.%d", "%Y-%m-%d", "%Y/%m/%d", "%d.%m.%Y", "%d-%m-%Y", "%d/%m/%Y"):
        try:
            return datetime.datetime.strptime(date_str, fmt).date()
        except Exception:
            continue
    return None

def is_valid_expiry(expiry_date_str):
    date_obj = parse_date(expiry_date_str)
    if not date_obj:
        return False
    return date_obj > datetime.date.today()

@ns.route('/')
class OCRResource(Resource):
    @api.expect(upload_parser)
    @api.marshal_with(ocr_result_model)
    def post(self):
        """Extract text from an uploaded CNI image (Arabic) and extract expiry date and identifier number, and verify them"""
        args = upload_parser.parse_args()
        cni_file = args['cni_image']
        if cni_file and allowed_file(cni_file.filename):
            cni_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(cni_file.filename))
            cni_file.save(cni_path)
            ocr_result = reader.readtext(cni_path, detail=0)
            expiry_date, identifier_number = extract_expiry_and_identifier(ocr_result)
            id_valid = is_valid_identifier(identifier_number)
            expiry_valid = is_valid_expiry(expiry_date)
            is_card_valid = id_valid and expiry_valid
            status = 'verified' if is_card_valid else 'not verified'
            return {
                'extracted_text': ocr_result,
                'expiry_date': expiry_date,
                'identifier_number': identifier_number,
                'id_valid': id_valid,
                'expiry_valid': expiry_valid,
                'is_card_valid': is_card_valid,
                'status': status
            }
        api.abort(400, 'Invalid or missing CNI image file.')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 
