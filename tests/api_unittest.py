import unittest
import requests
from io import BytesIO
from PIL import Image  # Install the Pillow library if not installed

class TestPredictEndpoint(unittest.TestCase):

    def test_predict_endpoint(self):
        # Assume you have an image file named "test_image.jpg" in the same directory as the test script
        image_path = "bike.jpg"

        # Load the image
        with open(image_path, "rb") as image_file:
            image_data = image_file.read()

        # Create a BytesIO object to simulate a file-like object
        image_file_object = BytesIO(image_data)

        # Create a dictionary to represent form data with the image file
        files = {'image': ('test_image.jpg', image_file_object, 'image/jpg')}

        # Make a POST request to the predict endpoint
        response = requests.get("http://127.0.0.1:5000/predict", files=files)
        print(response.text)

        # Assert the expected response status code (e.g., 200 OK)
        self.assertEqual(response.status_code, 200)

        # You can further assert the content of the response, depending on your API design
        # For example, if your API returns a JSON response, you can assert the content as follows:
        # expected_response = {"prediction": "some_value"}
        # self.assertEqual(response.json(), expected_response)

if __name__ == '__main__':
    unittest.main()
