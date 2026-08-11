from flask import render_template, Flask, request
from io import BytesIO
from PIL import Image
import numpy as np
import base64

from .qrcode import Qrcode


def create_app():
    """
    Flask app creation factory; adds routes to the app.

    Returns
    -------
    { Flask }
      The built flask app.
    """
    app = Flask(__name__)
    # QoL param for enabling debugging logging/mode
    debug = app.config["DEBUG"]

    def create_image_string(array, scale_factor):
        """
        Process a numpy array into a b64 encoded image.

        Parameters
        ----------
        array: list of np.uint8

        Returns
        -------
        { str }
          The base64 encoded image
        """
        # pillow does not support np.uint8
        downcasted = (array * 255).astype(bool)
        # code must be inverted as pillow 0 is black and 1 is white - code needs opposite
        inverted = np.invert(downcasted)
        # repeat items by n to increase the visual size - semantics remain identical
        scaled = np.repeat(
            np.repeat(inverted, scale_factor, axis=1), scale_factor, axis=0
        )
        image = Image.fromarray(scaled)
        image_io = BytesIO()
        image.save(image_io, "PNG", quality=100)

        return base64.b64encode(image_io.getvalue()).decode("utf-8")

    def create_image_string_col(array, scale_factor, bg, fg):
        """
        Process a numpy array into a b64 encoded image.

        Parameters
        ----------
        array: list of np.uint8

        Returns
        -------
        { str }
          The base64 encoded image
        """
        # pillow does not support np.uint8
        downcasted = (array * 255).astype(bool)
        # code must be inverted as pillow 0 is black and 1 is white - code needs opposite
        inverted = np.invert(downcasted)
        # repeat items by n to increase the visual size - semantics remain identical
        scaled = np.repeat(
            np.repeat(inverted, scale_factor, axis=1), scale_factor, axis=0
        )
        # convert hex to rgb cols
        bg_rgb = tuple(int(bg.lstrip("#")[i : i + 2], 16) for i in (0, 2, 4))
        fg_rgb = tuple(int(fg.lstrip("#")[i : i + 2], 16) for i in (0, 2, 4))

        # https://stackoverflow.com/a/3753428
        image = Image.fromarray(scaled).convert("RGBA")
        data = np.array(image)
        r, g, b, a = data.T
        white = (r == 255) & (b == 255) & (g == 255)
        data[..., :-1][white.T] = bg_rgb
        black = (r == 0) & (b == 0) & (g == 0)
        data[..., :-1][black.T] = fg_rgb
        image_col = Image.fromarray(data)

        image_io = BytesIO()
        image_col.save(image_io, "PNG", quality=100)

        return base64.b64encode(image_io.getvalue()).decode("utf-8")

    @app.route("/", methods=["POST", "GET"])
    def index():
        if request.method == "POST":
            data = [request.form.get("data")]
            print(data)
        return render_template("index.html")

    @app.route("/generate", methods=["POST"])
    def generate_code():
        data = request.form.get("data")
        scale_factor = request.form.get("scale_factor", default=10, type=int)
        bg_colour = request.form.get("bg_colour", default="#FFFFFF", type=str)
        fg_colour = request.form.get("fg_colour", default="#000000", type=str)
        # Generator parameters
        force_byte_mode = request.form.get("force_byte_mode", default=False, type=bool)
        step_by_step = request.form.get("step_by_step", default=False, type=bool)

        qrcode = Qrcode(
            data,
            debug=debug,
            force_byte_mode=force_byte_mode,
        )

        if not step_by_step:
            return f'<img src="data:image/png;base64,{create_image_string_col(qrcode.code, scale_factor, bg_colour, fg_colour)}" alt="qr code generated for {data}">'
        else:
            html = f"""
            <h2>Data Analysis</h2>
            <p><strong>Data mode: </strong>{qrcode.data_modes[0]}</p>
            <hr>

            <!-- # Data Encoding -->
            <h2>Data Encoding</h2>
            <p><strong>Version:</strong> {qrcode.version.number}</p>
            <p><strong>Mode Indicator:</strong> {qrcode.data_mode_indicators[0]}</p>
            <p><strong>Character Count Indicator:</strong> {qrcode.character_count_indicators[0]}</p>
            <p><strong>Encoded Data:</strong> {" ".join(qrcode.encoded_data)}</p>
            <p><strong>Raw Bit String:</strong> {qrcode.raw_data_bit_string}</p>
            <hr>

            <!-- Error Correction Encoding -->
            <h2>Error Correction Encoding</h2>
            <p><strong>Data Padded:</strong> {qrcode.data_padded}</p>
            <p><strong>ECC:</strong> {qrcode.ecc}</p>
            <p><strong>Final Codewords:</strong> {qrcode.codewordsful}</p>
            <hr>
            <!-- # Structuring Final Message -->
            <h2>Structuring Final Message</h2>
            <p><strong>Final Bit String:</strong> {qrcode.final_bit_string}</p>
            <hr>
            """

            images = [
                (
                    "Placement",
                    create_image_string_col(
                        qrcode.matrix, scale_factor, bg_colour, fg_colour
                    ),
                ),
                (
                    "Masked",
                    create_image_string_col(
                        qrcode.masked, scale_factor, bg_colour, fg_colour
                    ),
                ),
                (
                    "Final",
                    create_image_string_col(
                        qrcode.code, scale_factor, bg_colour, fg_colour
                    ),
                ),
            ]

            for image_name, img_b64 in images:
                html += f'''
                <h2>{image_name}</h2>
                <img src="data:image/png;base64,{img_b64}" alt="{image_name}" style="border:1px solid black; image-rendering: pixelated;">
                <hr>
                '''

            return html

    return app
