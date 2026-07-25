import "./App.css";
import { useState } from "react";
import axios from "axios";



function App() {

  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const apiBaseUrl = import.meta.env.VITE_API_URL || "http://127.0.0.1:8001";


  const uploadImage = async () => {
    if (!file) {
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    setLoading(true);

    const response = await axios.post(`${apiBaseUrl}/scan`, formData, {
      headers: {
        "Content-Type": "multipart/form-data"
      }
    });

    setResult(response.data);
    setLoading(false);
  };


  return (

    <div className="container">

      <h1>
        Steganographic Exfiltration Detector
      </h1>


      <input
        type="file"
        accept="image/*"
        onChange={
          e=>setFile(e.target.files[0])
        }
      />


      <br/><br/>


      {
        file &&
        <img
          className="preview"
          src={
            URL.createObjectURL(file)
          }
          alt="preview"
        />
      }


      <br/>


      <button
        onClick={uploadImage}
      >
        {
          loading
          ?
          "Analyzing..."
          :
          "Analyze Image"
        }

      </button>



      {
        result &&

        <div className="result">

          <h2>
            Analysis Result
          </h2>


          <pre>

          {
            JSON.stringify(
              result,
              null,
              2
            )
          }

          </pre>


        </div>

      }


    </div>

  )

}


export default App;