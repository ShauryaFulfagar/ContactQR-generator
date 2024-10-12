from flask import Flask, render_template, request, send_file
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
from io import BytesIO
from PIL import Image

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate_qr', methods=['POST'])
def generate_qr():
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    phone = request.form.get('phone_number')
    email = request.form.get('email')
    job_title = request.form.get('job_title')
    company_name = request.form.get('company_name')
    address = request.form.get('address')
    website = request.form.get('website')
    logo = request.files.get('logo')

    # Create vCard content
    vcard = (
        f"BEGIN:VCARD\n"
        f"VERSION:3.0\n"
        f"N:{last_name};{first_name}\n"
        f"FN:{first_name} {last_name}\n"
        f"TEL:{phone}\n"
        f"EMAIL:{email}\n"
        f"ORG:{company_name}\n"
        f"TITLE:{job_title}\n"
        f"ADR:{address}\n"
        f"URL:{website}\n"
        f"END:VCARD"
    )

    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(vcard)
    qr.make(fit=True)

    if logo:
        logo_image = Image.open(logo)
        logo_image.thumbnail((80, 80))
        img = qr.make_image(image_factory=StyledPilImage,
                            module_drawer=RoundedModuleDrawer())
        pos = ((img.size[0] - logo_image.size[0]) // 2,
               (img.size[1] - logo_image.size[1]) // 2)
        img.paste(logo_image, pos)
    else:
        img = qr.make_image(fill_color="black", back_color="white")

    # Convert to in-memory file
    img_io = BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)

    return send_file(img_io, mimetype='image/png', as_attachment=True, download_name='qrcode.png')


if __name__ == '__main__':
    app.run(debug=True)
