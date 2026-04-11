import { useEffect, useState } from "react";
import {
  API_BASE_URL,
  AUTH_START,
  AUTH_EXCHANGE,
  PAYMENT_ORDER,
  PAYMENT_LINE_ITEM,
  PAYMENT_ECOMMERCE_KEY,
  PAYMENT_TOKENIZE_CARD,
  PAYMENT_CHARGE,
  METHOD_POST,
  HEADER_CONTENT_TYPE,
  CONTENT_TYPE_JSON,
  DEFAULT_CARD_NUMBER,
  DEFAULT_EXP_MONTH,
  DEFAULT_EXP_YEAR,
  DEFAULT_CVV,
  DEFAULT_ZIP,
  DEFAULT_QUANTITY,
  DEFAULT_CURRENCY,
  MSG_WELCOME,
  MSG_CONNECTING,
  MSG_CONNECTED,
  MSG_CONNECT_FAILED,
  MSG_CONNECT_ERROR,
  MSG_ORDER_CREATE,
  MSG_ORDER_FAILED,
  MSG_ITEM_ADDED,
  MSG_ITEM_FAILED,
  MSG_ECOMMERCE_KEY_FETCH,
  MSG_ECOMMERCE_KEY_READY,
  MSG_ECOMMERCE_KEY_FAILED,
  MSG_ECOMMERCE_KEY_REQUIRED,
  MSG_CARD_TOKENIZING,
  MSG_CARD_TOKENIZED,
  MSG_CARD_TOKENIZE_FAILED,
  MSG_CARD_TOKENIZE_ERROR,
  MSG_PAYMENT_PROCESSING,
  MSG_PAYMENT_SUCCESSFUL,
  MSG_PAYMENT_FAILED,
  MSG_PAYMENT_ERROR,
  STORAGE_MERCHANT_ID,
  PARAM_CODE,
  PARAM_MERCHANT_ID,
} from "./constants";

interface Order {
  id: string;
  title: string;
}

interface LineItem {
  id: string;
  name: string;
  price: number;
  quantity: number;
}

function App() {
  const [message, setMessage] = useState<string>(MSG_WELCOME);
  const [isConnected, setIsConnected] = useState<boolean>(false);
  const [currentOrder, setCurrentOrder] = useState<Order | null>(null);
  const [lineItems, setLineItems] = useState<LineItem[]>([]);
  const [itemName, setItemName] = useState<string>("");
  const [itemPrice, setItemPrice] = useState<string>("");
  const [itemQuantity, setItemQuantity] = useState<string>(DEFAULT_QUANTITY);

  const [cardNumber, setCardNumber] = useState<string>(DEFAULT_CARD_NUMBER);
  const [expMonth, setExpMonth] = useState<string>(DEFAULT_EXP_MONTH);
  const [expYear, setExpYear] = useState<string>(DEFAULT_EXP_YEAR);
  const [cvv, setCvv] = useState<string>(DEFAULT_CVV);
  const [zip, setZip] = useState<string>(DEFAULT_ZIP);
  const [ecommerceKey, setEcommerceKey] = useState<string | null>(null);
  const [sourceToken, setSourceToken] = useState<string | null>(null);

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const code = params.get(PARAM_CODE);
    const merchantId = params.get(PARAM_MERCHANT_ID);

    if (merchantId) {
      localStorage.setItem(STORAGE_MERCHANT_ID, merchantId);
    }

    if (code) {
      const savedMerchantId = localStorage.getItem(STORAGE_MERCHANT_ID);
      setMessage(MSG_CONNECTING);

      fetch(`${API_BASE_URL}${AUTH_EXCHANGE}`, {
        method: METHOD_POST,
        headers: { [HEADER_CONTENT_TYPE]: CONTENT_TYPE_JSON },
        body: JSON.stringify({ code, merchant_id: savedMerchantId })
      })
        .then(async (res) => {
          const data = await res.json();
          if (data.success) {
            setMessage(MSG_CONNECTED);
            setIsConnected(true);
          } else {
            setMessage(MSG_CONNECT_FAILED);
          }
        })
        .catch(() => setMessage(MSG_CONNECT_ERROR));
    }
  }, []);

  const handleConnect = () => {
    window.location.href = `${API_BASE_URL}${AUTH_START}`;
  };

  const createOrder = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}${PAYMENT_ORDER}`, {
        method: METHOD_POST,
        headers: { [HEADER_CONTENT_TYPE]: CONTENT_TYPE_JSON },
        body: JSON.stringify({ title: "Demo Checkout", currency: "USD" })
      });
      const data = await response.json();
      if (data.success) {
        setCurrentOrder(data.order);
        setLineItems([]);
        setMessage(`${MSG_ORDER_CREATE}${data.order.id}`);
      }
    } catch (error) {
      setMessage(MSG_ORDER_FAILED);
    }
  };

  const addLineItem = async () => {
    if (!currentOrder || !itemName || !itemPrice) return;

    try {
      const response = await fetch(`${API_BASE_URL}${PAYMENT_LINE_ITEM}`, {
        method: METHOD_POST,
        headers: { [HEADER_CONTENT_TYPE]: CONTENT_TYPE_JSON },
        body: JSON.stringify({
          order_id: currentOrder.id,
          name: itemName,
          price: Math.round(parseFloat(itemPrice) * 100),
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
        setItemQuantity(DEFAULT_QUANTITY);
        setMessage(MSG_ITEM_ADDED);
      }
    } catch (error) {
      setMessage(MSG_ITEM_FAILED);
    }
  };

  const getEcommerceKey = async () => {
    try {
      setMessage(MSG_ECOMMERCE_KEY_FETCH);
      const response = await fetch(`${API_BASE_URL}${PAYMENT_ECOMMERCE_KEY}`);
      const data = await response.json();
      if (data.success) {
        setEcommerceKey(data.key_data.apiAccessKey);
        setMessage(MSG_ECOMMERCE_KEY_READY);
      }
    } catch (error) {
      setMessage(MSG_ECOMMERCE_KEY_FAILED);
    }
  };

  const tokenizeCard = async () => {
    if (!ecommerceKey) {
      setMessage(MSG_ECOMMERCE_KEY_REQUIRED);
      return;
    }

    try {
      setMessage(MSG_CARD_TOKENIZING);
      const response = await fetch(`${API_BASE_URL}${PAYMENT_TOKENIZE_CARD}`, {
        method: METHOD_POST,
        headers: { [HEADER_CONTENT_TYPE]: CONTENT_TYPE_JSON },
        body: JSON.stringify({
          ecommerce_key: ecommerceKey,
          number: cardNumber.replace(/\s/g, ""),
          exp_month: parseInt(expMonth),
          exp_year: parseInt(expYear),
          cvc: cvv,
          zip: zip
        })
      });
      const data = await response.json();
      if (data.success && data.token_data && data.token_data.id) {
        setSourceToken(data.token_data.id);
        setMessage(`${MSG_CARD_TOKENIZED}${data.token_data.id}`);
      } else {
        setMessage(`${MSG_CARD_TOKENIZE_FAILED}${JSON.stringify(data)}`);
      }
    } catch (error) {
      setMessage(`${MSG_CARD_TOKENIZE_ERROR}${String(error)}`);
    }
  };

  const processPayment = async () => {
    if (!currentOrder || !sourceToken) return;

    const totalAmount = lineItems.reduce((sum, item) => sum + (item.price * item.quantity), 0);

    try {
      setMessage(MSG_PAYMENT_PROCESSING);
      const response = await fetch(`${API_BASE_URL}${PAYMENT_CHARGE}`, {
        method: METHOD_POST,
        headers: { [HEADER_CONTENT_TYPE]: CONTENT_TYPE_JSON },
        body: JSON.stringify({
          amount: totalAmount,
          source: sourceToken,
          currency: DEFAULT_CURRENCY,
          description: "Demo Clover payment"
        })
      });
      const data = await response.json();

      if (data.success) {
        setMessage(`${MSG_PAYMENT_SUCCESSFUL}${data.payment.id}`);
        setCurrentOrder(null);
        setLineItems([]);
        setSourceToken(null);
        setEcommerceKey(null);
      } else {
        setMessage(`${MSG_PAYMENT_FAILED}${JSON.stringify(data)}`);
      }
    } catch (error) {
      setMessage(`${MSG_PAYMENT_ERROR}${String(error)}`);
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
                      {item.name} - ${(item.price / 100).toFixed(2)} x {item.quantity}
                    </div>
                  ))}
                  <div style={{ fontWeight: "bold", marginTop: "10px" }}>
                    Total: ${(totalAmount / 100).toFixed(2)}
                  </div>
                </div>
              )}

              {lineItems.length > 0 && !ecommerceKey && (
                <button onClick={getEcommerceKey} style={{
                  padding: "10px 20px",
                  fontSize: "14px",
                  cursor: "pointer",
                  backgroundColor: "#9C27B0",
                  color: "white",
                  border: "none",
                  borderRadius: "4px",
                  marginRight: "10px"
                }}>
                  Get Ecommerce Key
                </button>
              )}

              {ecommerceKey && !sourceToken && (
                <div style={{ marginBottom: "20px" }}>
                  <h4>Card Details</h4>
                  <input
                    type="text"
                    placeholder="Card Number"
                    value={cardNumber}
                    onChange={(e) => setCardNumber(e.target.value)}
                    style={{ margin: "5px", padding: "8px", width: "100%" }}
                  />
                  <div style={{ display: "flex", gap: "10px" }}>
                    <input
                      type="text"
                      placeholder="MM"
                      value={expMonth}
                      onChange={(e) => setExpMonth(e.target.value)}
                      maxLength={2}
                      style={{ padding: "8px", width: "60px" }}
                    />
                    <input
                      type="text"
                      placeholder="YYYY"
                      value={expYear}
                      onChange={(e) => setExpYear(e.target.value)}
                      maxLength={4}
                      style={{ padding: "8px", width: "80px" }}
                    />
                    <input
                      type="text"
                      placeholder="CVV"
                      value={cvv}
                      onChange={(e) => setCvv(e.target.value)}
                      maxLength={4}
                      style={{ padding: "8px", width: "60px" }}
                    />
                    <input
                      type="text"
                      placeholder="ZIP"
                      value={zip}
                      onChange={(e) => setZip(e.target.value)}
                      style={{ padding: "8px", width: "80px" }}
                    />
                  </div>
                  <button onClick={tokenizeCard} style={{
                    padding: "10px 20px",
                    fontSize: "14px",
                    cursor: "pointer",
                    backgroundColor: "#FF5722",
                    color: "white",
                    border: "none",
                    borderRadius: "4px",
                    marginTop: "10px"
                  }}>
                    Tokenize Card
                  </button>
                </div>
              )}

              {sourceToken && (
                <button onClick={processPayment} style={{
                  padding: "10px 20px",
                  fontSize: "16px",
                  cursor: "pointer",
                  backgroundColor: "#4CAF50",
                  color: "white",
                  border: "none",
                  borderRadius: "4px"
                }}>
                  Charge ${(totalAmount / 100).toFixed(2)}
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