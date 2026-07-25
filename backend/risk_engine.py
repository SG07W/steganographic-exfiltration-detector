class RiskEngine:

    def __init__(self, lsb_result, chi_result):
        self.lsb = lsb_result
        self.chi = chi_result

    def calculate(self):

        # -----------------------------
        # LSB Risk
        # -----------------------------
        entropy = self.lsb["entropy"]

        if entropy >= 0.98:
            lsb_risk = 90
            lsb_message = "Very high randomness detected in LSBs."
        elif entropy >= 0.90:
            lsb_risk = 70
            lsb_message = "High randomness detected."
        elif entropy >= 0.75:
            lsb_risk = 50
            lsb_message = "Moderate randomness."
        else:
            lsb_risk = 20
            lsb_message = "LSB distribution appears normal."

        # -----------------------------
        # Chi-Square Risk
        # -----------------------------
        suspicious_pairs = self.chi["suspicious_pairs"]

        if suspicious_pairs >= 100:
            chi_risk = 90
            chi_message = "Many suspicious histogram pairs detected."
        elif suspicious_pairs >= 70:
            chi_risk = 70
            chi_message = "Large histogram deviations detected."
        elif suspicious_pairs >= 40:
            chi_risk = 50
            chi_message = "Moderate histogram anomalies."
        else:
            chi_risk = 20
            chi_message = "Histogram appears normal."

        # -----------------------------
        # Entropy Risk
        # -----------------------------
        if entropy >= 0.99:
            entropy_risk = 95
            entropy_message = "Entropy is extremely high."
        elif entropy >= 0.95:
            entropy_risk = 75
            entropy_message = "Entropy is above normal."
        elif entropy >= 0.80:
            entropy_risk = 50
            entropy_message = "Entropy is slightly elevated."
        else:
            entropy_risk = 20
            entropy_message = "Entropy is within expected range."

        # -----------------------------
        # Overall Risk
        # -----------------------------
        risk_score = round(
            (
                lsb_risk * 0.40 +
                chi_risk * 0.40 +
                entropy_risk * 0.20
            )
        )

        # -----------------------------
        # Verdict
        # -----------------------------
        if risk_score <= 20:
            verdict = "🟢 SAFE"

        elif risk_score <= 70:
            verdict = "🟡 LOW RISK"

        elif risk_score <= 90:
            verdict = "🟠 SUSPICIOUS"

        else:
            verdict = "🔴 HIGH RISK"

        return {
            "risk_score": risk_score,
            "verdict": verdict,

            "lsb_risk": lsb_risk,
            "lsb_message": lsb_message,

            "chi_risk": chi_risk,
            "chi_message": chi_message,

            "entropy_risk": entropy_risk,
            "entropy_message": entropy_message
        }