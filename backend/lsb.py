from PIL import Image
import numpy as np


class LSBAnalyzer:

    def __init__(self, image_path):
        self.image_path = image_path
        self.image = Image.open(image_path).convert("RGB")
        self.array = np.array(self.image)

    def extract_lsb(self):
        """
        Extract all LSB bits from every RGB value.
        Returns a NumPy array of 0s and 1s.
        """

        # Bitwise AND with 1 keeps only the last bit
        lsb = self.array & 1

        return lsb

    def bit_statistics(self):
        """
        Count how many 0s and 1s exist in the LSB plane.
        """

        lsb = self.extract_lsb()

        ones = np.sum(lsb)
        zeros = lsb.size - ones

        total = lsb.size

        return {
            "total_bits": int(total),
            "ones": int(ones),
            "zeros": int(zeros),
            "ones_percentage": round((ones / total) * 100, 2),
            "zeros_percentage": round((zeros / total) * 100, 2)
        }

    def entropy(self):
        """
        Calculate Shannon entropy of the LSB plane.
        """

        lsb = self.extract_lsb().flatten()

        values, counts = np.unique(lsb, return_counts=True)

        probabilities = counts / counts.sum()

        entropy = -np.sum(probabilities * np.log2(probabilities))

        return round(float(entropy), 4)