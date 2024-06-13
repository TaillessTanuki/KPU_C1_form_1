from flask import Flask, request, jsonify
import base64
import ocr_lembar_1_v2_api
import ocr_lembar_2
import ocr_lembar_3

app = Flask(__name__)

def decode_base64_to_image(base64_string):
    image_data = base64.b64decode(base64_string)
    # Here you would convert this to an image if necessary,
    # for now, we're just decoding the base64 string.
    return image_data

@app.route('/process_image', methods=['POST'])
def process_image():
    data = request.json
    base64_image = data.get('base64')
    lembar = data.get('lembar')

    if not base64_image or not lembar:
        return jsonify({'error': 'Invalid input'}), 400

    image_data = decode_base64_to_image(base64_image)

    if lembar == 'lembar_1':
        result = ocr_lembar_1_v2_api.show_detected_boxes_lembar_1(image_data)
    elif lembar == 'lembar_2':
        result = ocr_lembar_2.show_detected_boxes_lembar_2(image_data)
    elif lembar == 'lembar_3':
        result = ocr_lembar_3.show_detected_boxes_lembar_3(image_data)
    else:
        return jsonify({'error': 'Invalid lembar value'}), 400

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
