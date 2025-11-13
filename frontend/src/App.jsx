import { useState } from "react";
import axios from "axios";
import "./index.css";

function App() {
  const [product, setProduct] = useState("");
  const [audience, setAudience] = useState("");
  const [festival, setFestival] = useState("");
  const [result, setResult] = useState("");
  const [loading, setLoading] = useState(false);

  async function generateAds() {
    setLoading(true);
    try {
      const res = await axios.post(
        "https://YOUR-BACKEND-URL.onrender.com/generate",
        {
          product,
          audience,
          festival,
        }
      );
      setResult(res.data.result);
    } catch (e) {
      setResult("❌ Error generating ads. Check backend.");
    }
    setLoading(false);
  }

  return (
    <div className="container">
      <h1>🇮🇳 Ad Brain – Hinglish Ad Generator</h1>

      <input
        className="input"
        placeholder="Product"
        value={product}
        onChange={(e) => setProduct(e.target.value)}
      />

      <input
        className="input"
        placeholder="Audience"
        value={audience}
        onChange={(e) => setAudience(e.target.value)}
      />

      <input
        className="input"
        placeholder="Festival (optional)"
        value={festival}
        onChange={(e) => setFestival(e.target.value)}
      />

      <button className="btn" onClick={generateAds} disabled={loading}>
        {loading ? "Generating..." : "Generate Ads"}
      </button>

      <pre className="output">{result}</pre>
    </div>
  );
}

export default App;
