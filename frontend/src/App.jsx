import "./App.css";
import { useState } from "react";
import axios from "axios";

function App() {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const apiBaseUrl =
    import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

  const handleFile = (e) => {
    const selected = e.target.files[0];
    if (!selected) return;

    setFile(selected);
    setPreview(URL.createObjectURL(selected));
    setResult(null);
  };

  const uploadImage = async () => {
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    setLoading(true);

    try {
      const response = await axios.post(
        `${apiBaseUrl}/scan`,
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );

      setResult(response.data);
    } catch (error) {
      console.error(error);

      setResult({
        verdict: "Error",
        risk_score: 0,
        lsb_risk: 0,
        chi_risk: 0,
        entropy_risk: 0,
        lsb_message: "Backend unavailable.",
        chi_message: "Backend unavailable.",
        entropy_message: "Backend unavailable.",
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page">

      <section className="hero">

        <p className="badge">
          AI Powered Detection
        </p>

        <h1>
          Steganographic
          <br />
          Exfiltration Detector
        </h1>

        <p className="subtitle">
          Detect hidden data inside digital images using
          statistical steganalysis and machine learning.
        </p>

      </section>

      <section className="card upload-card">

        <label className="upload-box">

          <input
            type="file"
            accept="image/*"
            onChange={handleFile}
          />

          <div className="upload-icon">
            ⬆
          </div>

          <h3>Upload Image</h3>

          <p>
            Click to browse your computer
          </p>

        </label>

        {preview && (
          <div className="preview-wrapper">
            <img
              src={preview}
              alt="preview"
              className="preview"
            />
          </div>
        )}

        <button
          className="scan-btn"
          onClick={uploadImage}
          disabled={!file || loading}
        >
          {loading ? "Analyzing..." : "Analyze Image"}
        </button>

      </section>

      {result && (

        <section className="card">

          <div className="verdict">

            <span>Verdict</span>

            <h2>{result.verdict}</h2>

          </div>

          <div className="risk">

            <div className="metric">

              <div className="metric-header">
                <span>Overall Risk</span>
                <span>{result.risk_score}%</span>
              </div>

              <div className="bar">
                <div
                  className="fill"
                  style={{
                    width: `${result.risk_score}%`,
                  }}
                />
              </div>

            </div>

            <div className="metric">

              <div className="metric-header">
                <span>LSB Analysis</span>
                <span>{result.lsb_risk}%</span>
              </div>

              <div className="bar">
                <div
                  className="fill"
                  style={{
                    width: `${result.lsb_risk}%`,
                  }}
                />
              </div>

              <small>{result.lsb_message}</small>

            </div>

            <div className="metric">

              <div className="metric-header">
                <span>Chi Square</span>
                <span>{result.chi_risk}%</span>
              </div>

              <div className="bar">
                <div
                  className="fill"
                  style={{
                    width: `${result.chi_risk}%`,
                  }}
                />
              </div>

              <small>{result.chi_message}</small>

            </div>

            <div className="metric">

              <div className="metric-header">
                <span>Entropy</span>
                <span>{result.entropy_risk}%</span>
              </div>

              <div className="bar">
                <div
                  className="fill"
                  style={{
                    width: `${result.entropy_risk}%`,
                  }}
                />
              </div>

              <small>{result.entropy_message}</small>

            </div>

          </div>

        </section>

      )}

    </div>
  );
}

export default App;