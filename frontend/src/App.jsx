import { useState } from "react";
import "./App.css";

function App() {
  const [url, setUrl] = useState("");
  const [shortUrl, setShortUrl] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async () => {
    setError("");
    setShortUrl("");

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/urls",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            original_url: url,
          }),
        }
      );

      if (!response.ok) {
        throw new Error("Invalid URL");
      }

      const data = await response.json();

      setShortUrl(data.short_url);
    } catch (err) {
      setError("Please enter a valid URL.");
    }
  };

  const copyToClipboard = async () => {
    try {
      await navigator.clipboard.writeText(shortUrl);
      alert("Copied to clipboard!");
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="container">
      <h1>URL Shortener</h1>

      <input
        type="text"
        placeholder="Enter URL (https://example.com)"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
      />

      <button onClick={handleSubmit}>
        Shorten URL
      </button>

      {error && (
        <p className="error">
          {error}
        </p>
      )}

      {shortUrl && (
        <div className="result">
          <h3>Short URL</h3>

          <a
            href={shortUrl}
            target="_blank"
            rel="noreferrer"
          >
            {shortUrl}
          </a>

          <br />

          <button
            className="copy-btn"
            onClick={copyToClipboard}
          >
            Copy
          </button>
        </div>
      )}
    </div>
  );
}

export default App;