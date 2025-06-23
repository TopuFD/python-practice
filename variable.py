# from flask import Flask, request, send_file
# from flask_cors import CORS
# import cv2
# import numpy as np
# import io

# app = Flask(__name__)
# CORS(app)

# face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# def subtle_smooth_face(img, face_rects):
#     for (x, y, w, h) in face_rects:
#         face_roi = img[y:y+h, x:x+w]

#         smooth = cv2.bilateralFilter(face_roi, d=9, sigmaColor=50, sigmaSpace=50)

#         gray = cv2.cvtColor(smooth, cv2.COLOR_BGR2GRAY)
#         _, mask = cv2.threshold(gray, 70, 255, cv2.THRESH_BINARY_INV)

#         inpainted = cv2.inpaint(smooth, mask, 3, cv2.INPAINT_TELEA)

#         blended = cv2.addWeighted(inpainted, 0.3, face_roi, 0.7, 0)

#         img[y:y+h, x:x+w] = blended

#     return img

# @app.route("/enhance", methods=["POST"])
# def enhance_route():
#     if "image" not in request.files:
#         return {"error": "No image found in request"}, 400

#     file = request.files["image"]
#     in_memory_file = file.read()
#     npimg = np.frombuffer(in_memory_file, np.uint8)
#     img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

#     if img is None:
#         return {"error": "Failed to decode image"}, 400

#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

#     if len(faces) > 0:
#         img = subtle_smooth_face(img, faces)

#     # Do NOT apply global enhancement to keep original quality

#     _, img_encoded = cv2.imencode('.jpg', img)
#     byte_io = io.BytesIO(img_encoded.tobytes())
#     return send_file(byte_io, mimetype='image/jpeg')

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000, debug=True)

from flask import Flask, request, send_file
from flask_cors import CORS
from PIL import Image
import io
import numpy as np
import torch
from gfpgan import GFPGANer

app = Flask(__name__)
CORS(app)

# Initialize GFPGANer (adjust path accordingly)
gfpganer = GFPGANer(
    model_path='model_weights/GFPGANv1.3.pth',
    upscale=1,
    arch='clean',
    channel_multiplier=2,
    bg_upsampler=None
)

@app.route('/enhance', methods=['POST'])
def enhance():
    if 'image' not in request.files:
        return {'error': 'No image file provided'}, 400

    file = request.files['image']
    img = Image.open(file.stream).convert('RGB')
    img_np = np.array(img)

    # Enhance using GFPGAN
    cropped_faces, restored_faces, restored_img = gfpganer.enhance(
        img_np,
        has_aligned=False,
        only_center_face=False,
        paste_back=True
    )

    restored_img_pil = Image.fromarray(restored_img)

    img_bytes = io.BytesIO()
    restored_img_pil.save(img_bytes, format='JPEG')
    img_bytes.seek(0)

    return send_file(img_bytes, mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
