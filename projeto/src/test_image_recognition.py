
import unittest
import cv2
import numpy as np
from src import image_recognition

class TestImageRecognition(unittest.TestCase):
    def test_match_template(self):
        screen = np.zeros((600, 800, 3), dtype=np.uint8)
        template = np.zeros((100, 100, 3), dtype=np.uint8)
        loc, val = image_recognition.match_template(screen, template)
        self.assertTrue(val >= 0.0)

if __name__ == '__main__':
    unittest.main()
