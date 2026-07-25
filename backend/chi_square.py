from PIL import Image
import numpy as np


class ChiSquareAnalyzer:
    """
    Performs Chi-Square steganalysis on grayscale image histograms.
    """

    PAIR_DIFFERENCE_THRESHOLD = 5

    def __init__(self, image_path):
        self.image_path = image_path

    def calculate_histogram(self):
        """
        Generate a grayscale histogram with 256 intensity bins.

        Returns:
            numpy.ndarray: Histogram of pixel frequencies.
        """
        image = Image.open(self.image_path).convert("L")
        pixels = np.array(image).flatten()

        histogram = np.bincount(pixels, minlength=256)

        return histogram

    def chi_square_test(self, histogram):
        """
        Compute the Chi-Square statistic using 128 even-odd pixel pairs.

        Args:
            histogram (numpy.ndarray): 256-bin grayscale histogram.

        Returns:
            dict: Chi-Square analysis results.
        """
        chi_square = 0.0
        suspicious_pairs = 0
        total_difference = 0
        pairs_analyzed = 0

        for i in range(0, 256, 2):
            even_count = histogram[i]
            odd_count = histogram[i + 1]

            expected = (even_count + odd_count) / 2

            if expected == 0:
                continue

            pairs_analyzed += 1

            pair_chi = (
                ((even_count - expected) ** 2) / expected
                + ((odd_count - expected) ** 2) / expected
            )

            chi_square += pair_chi

            difference = abs(even_count - odd_count)
            total_difference += difference

            if difference < self.PAIR_DIFFERENCE_THRESHOLD:
                suspicious_pairs += 1

        average_difference = (
            total_difference / pairs_analyzed
            if pairs_analyzed > 0
            else 0
        )

        return {
            "chi_square": round(chi_square, 2),
            "average_pair_difference": round(average_difference, 2),
            "suspicious_pairs": suspicious_pairs,
            "pairs_analyzed": pairs_analyzed
        }

    def analyze(self):
        """
        Run the complete Chi-Square analysis.

        Returns:
            dict: Analysis results.
        """
        histogram = self.calculate_histogram()
        return self.chi_square_test(histogram)