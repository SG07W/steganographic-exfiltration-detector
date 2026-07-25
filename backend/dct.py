from PIL import Image
import numpy as np
import math


class DCTAnalyzer:
    """
    JPEG DCT Analysis (Step 1 & Step 2)

    Responsibilities:
    - Load image
    - Convert to grayscale
    - Split into 8x8 blocks
    - Compute 2D DCT
    """

    def __init__(self, image_path):
        self.image_path = image_path
        self.image = None
        self.image_array = None
        self.blocks = []
        self.quantization_matrix = np.array([
        [16, 11, 10, 16, 24, 40, 51, 61],
        [12, 12, 14, 19, 26, 58, 60, 55],
        [14, 13, 16, 24, 40, 57, 69, 56],
        [14, 17, 22, 29, 51, 87, 80, 62],
        [18, 22, 37, 56, 68, 109, 103, 77],
        [24, 35, 55, 64, 81, 104, 113, 92],
        [49, 64, 78, 87, 103, 121, 120, 101],
        [72, 92, 95, 98, 112, 100, 103, 99]
            
        ], dtype=np.float64)
        
    def load_image(self):
        """
        Load image and convert to grayscale.
        """

        self.image = Image.open(self.image_path).convert("L")
        self.image_array = np.array(self.image, dtype=np.float64)

    def split_blocks(self):
        """
        Split image into non-overlapping 8x8 blocks.
        Ignore incomplete edge blocks.
        """

        if self.image_array is None:
            raise ValueError("Image not loaded.")

        height, width = self.image_array.shape

        self.blocks = []

        for y in range(0, height - 7, 8):
            for x in range(0, width - 7, 8):
                self.blocks.append(self.image_array[y:y + 8, x:x + 8])

    def compute_dct(self, block):
        """
        Compute the 2D DCT of one 8x8 block.
        """

        block = block.astype(np.float64) - 128.0

        dct = np.zeros((8, 8), dtype=np.float64)

        for u in range(8):
            for v in range(8):

                cu = 1 / math.sqrt(2) if u == 0 else 1.0
                cv = 1 / math.sqrt(2) if v == 0 else 1.0

                coefficient = 0.0

                for x in range(8):
                    for y in range(8):

                        coefficient += (
                            block[x, y]
                            * math.cos(((2 * x + 1) * u * math.pi) / 16)
                            * math.cos(((2 * y + 1) * v * math.pi) / 16)
                        )

                dct[u, v] = 0.25 * cu * cv * coefficient

        return dct

    def quantize(self, dct_block):

         quantized = np.round(
        dct_block / self.quantization_matrix
         )

         return quantized.astype(np.int32)
    def analyze(self):
        """
        Execute the DCT pipeline.
        """

        self.load_image()
        self.split_blocks()

        return {
            "image_size": self.image_array.shape,
            "total_blocks": len(self.blocks),
            "block_shape": self.blocks[0].shape if self.blocks else None
        }