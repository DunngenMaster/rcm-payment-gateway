import { useEffect, useState } from "react";

const API_BASE_URL = "http://localhost:8000";

interface Order {
  id: string;
  title: string;
  currency: string;
}

interface LineItem {
  id: string;
  name: string;
  price: number;
  quantity: number;
}

interface Payment {
  id: string;
  amount: number;
  result: string;
}

function App() {
  const [message, setMessage] = useState<string>("Welcome to RCM Payment Gateway Demo");
  const [isConnected, setIsConnected] = useState<boolean>(false);
  const [currentOrder, setCurrentOrder] = useState<Order | null>(null);
  const [lineItems, setLineItems] = useState<LineItem[]>([]);
  const [itemName, setItemName] = useState<string>("");
  const [itemPrice, setItemPrice] = useState<string>("");
  const [itemQuantity, setItemQuantity] = useState<string>("1");

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
            setMessage("Clover connected successfully!");
            setIsConnected(true);
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

  const createOrder = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/payment/order`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title: "Demo Checkout", currency: "USD" })
      });
      const data = await response.json();
      if (data.success) {
        setCurrentOrder(data.order);
        setLineItems([]);
        setMessage(`Order created: ${data.order.id}`);
      }
    } catch (error) {
      setMessage("Failed to create order");
    }
  };

  const addLineItem = async () => {
    if (!currentOrder || !itemName || !itemPrice) return;

    try {
      const response = await fetch(`${API_BASE_URL}/payment/line-item`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          order_id: currentOrder.id,
          name: itemName,
          price: Math.round(parseFloat(itemPrice) * 100), // Convert to cents
          quantity: parseInt(itemQuantity)
        })
      });
      const data = await response.json();
      if (data.success) {
        setLineItems([...lineItems, {
          id: data.line_item.id,
          name: itemName,
          price: Math.round(parseFloat(itemPrice) * 100),
          quantity: parseInt(itemQuantity)
        }]);
        setItemName("");
        setItemPrice("");
        setItemQuantity("1");
        setMessage("Item added to order");
      }
    } catch (error) {
      setMessage("Failed to add item");
    }
  };

  const processPayment = async () => {
    if (!currentOrder) return;

    const totalAmount = lineItems.reduce((sum, item) => sum + (item.price * item.quantity), 0);

    try {
      const response = await fetch(`${API_BASE_URL}/payment/pay`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          order_id: currentOrder.id,
          amount: totalAmount
        })
      });
      const data = await response.json();
      if (data.success) {
        setMessage(`Payment successful! ID: ${data.payment.id}`);
        setCurrentOrder(null);
        setLineItems([]);
      }
    } catch (error) {
      setMessage("Payment failed");
    }
  };

  const totalAmount = lineItems.reduce((sum, item) => sum + (item.price * item.quantity), 0);

  return (
    <div style={{
      maxWidth: "600px",
      margin: "40px auto",
      fontFamily: "Arial, sans-serif",
      padding: "20px"
    }}>
      <h1>RCM Payment Gateway Demo</h1>
      <p>{message}</p>

      {!isConnected ? (
        <button onClick={handleConnect} style={{
          padding: "10px 20px",
          fontSize: "16px",
          cursor: "pointer",
          backgroundColor: "#4CAF50",
          color: "white",
          border: "none",
          borderRadius: "4px"
        }}>
          Connect Clover
        </button>
      ) : (
        <div>
          {!currentOrder ? (
            <button onClick={createOrder} style={{
              padding: "10px 20px",
              fontSize: "16px",
              cursor: "pointer",
              backgroundColor: "#2196F3",
              color: "white",
              border: "none",
              borderRadius: "4px"
            }}>
              Create New Order
            </button>
          ) : (
            <div>
              <h3>Order: {currentOrder.title}</h3>

              <div style={{ marginBottom: "20px" }}>
                <h4>Add Item</h4>
                <input
                  type="text"
                  placeholder="Item name"
                  value={itemName}
                  onChange={(e) => setItemName(e.target.value)}
                  style={{ margin: "5px", padding: "5px" }}
                />
                <input
                  type="number"
                  placeholder="Price ($)"
                  value={itemPrice}
                  onChange={(e) => setItemPrice(e.target.value)}
                  style={{ margin: "5px", padding: "5px" }}
                />
                <input
                  type="number"
                  placeholder="Quantity"
                  value={itemQuantity}
                  onChange={(e) => setItemQuantity(e.target.value)}
                  min="1"
                  style={{ margin: "5px", padding: "5px", width: "60px" }}
                />
                <button onClick={addLineItem} style={{
                  padding: "5px 10px",
                  cursor: "pointer",
                  backgroundColor: "#FF9800",
                  color: "white",
                  border: "none",
                  borderRadius: "4px"
                }}>
                  Add Item
                </button>
              </div>

              {lineItems.length > 0 && (
                <div style={{ marginBottom: "20px" }}>
                  <h4>Order Items</h4>
                  {lineItems.map((item, index) => (
                    <div key={index} style={{ padding: "5px", borderBottom: "1px solid #ccc" }}>
                      {item.name} - ${(item.price / 100).toFixed(2)} x {item.quantity} = ${(item.price * item.quantity / 100).toFixed(2)}
                    </div>
                  ))}
                  <div style={{ fontWeight: "bold", marginTop: "10px" }}>
                    Total: ${(totalAmount / 100).toFixed(2)}
                  </div>
                </div>
              )}

              {lineItems.length > 0 && (
                <button onClick={processPayment} style={{
                  padding: "10px 20px",
                  fontSize: "16px",
                  cursor: "pointer",
                  backgroundColor: "#4CAF50",
                  color: "white",
                  border: "none",
                  borderRadius: "4px"
                }}>
                  Process Payment
                </button>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default App;