import { useEffect, useState } from "react";

const API_BASE_URL = "http://localhost:8000";

function App() {
  const [message, setMessage] = useState<string>("Welcome to RCM Payment Gateway Demo");

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const merchantId = params.get("merchant_id");
    const clientId = params.get("client_id");
    const code = params.get("code");

    if (merchantId) {
      localStorage.setItem("clover_merchant_id", merchantId);
    }

    if (code) {
      const savedMerchantId = localStorage.getItem("clover_merchant_id");
      setMessage("Exchanging Clover authorization code...");

      fetch(`${API_BASE_URL}/auth/exchange`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          code,
          merchant_id: savedMerchantId
        })
      })
        .then(async (res) => {
          const data = await res.json();
          if (data.success) {
            setMessage("Clover connected successfully.");
          } else {
            setMessage("Failed to connect Clover.");
          }
        })
        .catch(() => {
          setMessage("Error while connecting Clover.");
        });

      return;
    }

    if (merchantId && clientId) {
      setMessage("Redirecting to Clover OAuth...");
      window.location.href = `${API_BASE_URL}/auth/start`;
      return;
    }
  }, []);

  const handleConnect = () => {
    window.location.href = `${API_BASE_URL}/auth/start`;
  };

  return (
    <div
      style={{
        maxWidth: "600px",
        margin: "80px auto",
        fontFamily: "Arial, sans-serif",
        textAlign: "center"
      }}
    >
      <h1>RCM Payment Gateway Demo</h1>
      <p>{message}</p>
      <button
        onClick={handleConnect}
        style={{
          padding: "10px 20px",
          fontSize: "16px",
          cursor: "pointer"
        }}
      >
        Connect Clover
      </button>
    </div>
  );
}

export default App;