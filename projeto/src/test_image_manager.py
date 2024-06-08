
import unittest
from src import image_manager

class TestImageManager(unittest.TestCase):
    def test_load_image(self):
        img = image_manager.load_image('path/to/template.png')
        self.assertIsNotNone(img)

if __name__ == '__main__':
    unittest.main()
