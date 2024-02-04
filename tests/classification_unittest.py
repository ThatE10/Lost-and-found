import unittest

from PIL import Image

from ml_model.classification import ml_core


class TestMyClass(unittest.TestCase):

    def test_local_mlcore(self):
        obj = ml_core(run_local=True)
        self.assertTrue(isinstance(obj, ml_core))
        self.assertTrue(hasattr(obj, 'model'))
        self.assertTrue(hasattr(obj, 'processor'))
        self.assertTrue(hasattr(obj, 'classification_API'))

        self.assertTrue(obj.classification_API == 'http://127.0.0.1:5000/predict')

        text = "a picture of "
        raw_image = Image.open('bike.jpg').convert('RGB')
        inputs = obj.processor(raw_image, text, return_tensors="pt").to(obj.device)
        out = obj.model.generate(**inputs, num_beams=3)
        output = obj.processor.decode(out[0], skip_special_tokens=True)

        self.assertTrue(output)

    def test_api_mlcore(self):
        obj = ml_core(run_local=False,classification_API='')
        self.assertTrue(isinstance(obj, ml_core))
        self.assertTrue(hasattr(obj, 'classification_API'))




if __name__ == '__main__':
    unittest.main()