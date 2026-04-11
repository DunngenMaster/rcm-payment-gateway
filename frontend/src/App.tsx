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
  MSG_PAYMENT_PROCESSING,
  MSG_PAYMENT_SUCCESSFUL,
  MSG_PAYMENT_ERROR,
  STORAGE_MERCHANT_ID,
  PARAM_CODE,
  PARAM_MERCHANT_ID,
} from "./constants";
import { OrderForm } from "./components/OrderForm";
import { CardForm } from "./components/CardForm";
import { PaymentSummary } from "./components/PaymentSummary";
import { ErrorDialog } from "./components/ErrorDialog";
import { validateOrderForm, validateCardForm, validateChargeForm } from "./validations";
import { mapPaymentError } from "./utils/errorMapping";
import type { ValidationErrors } from "./validations";

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

interface ErrorDialog {
  show: boolean;
  title: string;
  message: string;
  isDecline: boolean;
}

function App() {
  const [message, setMessage] = useState<string>(MSG_WELCOME);
  const [isConnected, setIsConnected] = useState<boolean>(false);
  const [currentOrder, setCurrentOrder] = useState<Order | null>(null);
  const [lineItems, setLineItems] = useState<LineItem[]>([]);
  const [itemName, setItemName] = useState<string>("");
  const [itemPrice, setItemPrice] = useState<string>("");
  const [itemQuantity, setItemQuantity] = useState<string>(DEFAULT_QUANTITY);

  const [cardNumber, setCardNumber] = useState<string>("");
  const [expMonth, setExpMonth] = useState<string>(DEFAULT_EXP_MONTH);
  const [expYear, setExpYear] = useState<string>(DEFAULT_EXP_YEAR);
  const [cvv, setCvv] = useState<string>(DEFAULT_CVV);
  const [zip, setZip] = useState<string>(DEFAULT_ZIP);
  const [ecommerceKey, setEcommerceKey] = useState<string | null>(null);
  const [sourceToken, setSourceToken] = useState<string | null>(null);

  const [errors, setErrors] = useState<ValidationErrors>({});
  const [errorDialog, setErrorDialog] = useState<ErrorDialog>({ show: false, title: "", message: "", isDecline: false });

  const validateCurrency = (value: string): { valid: boolean; cents?: number; error?: string } => {
    if (!value || value.trim() === "") {
      return { valid: false, error: "Price is required" };
    }

    const num = parseFloat(value);
    if (isNaN(num)) {
      return { valid: false, error: "Price must be numeric" };
    }

    if (num < 0.01) {
      return { valid: false, error: "Price must be at least 0.01" };
    }

    const decimalMatch = value.match(/\.(\d+)$/);
    const decimalPlaces = decimalMatch ? decimalMatch[1].length : 0;
    if (decimalPlaces > 2) {
      return { valid: false, error: "Price must have at most 2 decimal places" };
    }

    const cents = Math.round(num * 100);
    return { valid: true, cents };
  };

  const closeErrorDialog = () => {
    setErrorDialog({ ...errorDialog, show: false });
  };

  const handleUseAnotherCard = () => {
    setSourceToken(null);
    closeErrorDialog();
    setTimeout(() => {
      const cardInput = document.querySelector('input[placeholder="Card Number"]') as HTMLInputElement;
      if (cardInput) {
        cardInput.focus();
      }
    }, 100);
  };

  const checkCloverConnection = async (): Promise<boolean> => {
    try {
      const response = await fetch(`${API_BASE_URL}/auth/status`);
      const data = await response.json();

      if (!data.connected) {
        setMessage("Clover session expired. Redirecting to reconnect...");
        setTimeout(() => {
          window.location.href = `${API_BASE_URL}/auth/start`;
        }, 1500);
        return false;
      }

      return true;
    } catch (error) {
      setMessage("Could not verify Clover connection. Please try again.");
      return false;
    }
  };

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
    const isConnected = await checkCloverConnection();
    if (!isConnected) return;

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
    const priceValidation = validateCurrency(itemPrice);
    if (!priceValidation.valid) {
      setErrors({ ...errors, itemPrice: priceValidation.error });
      return;
    }

    const validationErrors = validateOrderForm(itemName, itemPrice, itemQuantity);
    if (Object.keys(validationErrors).length > 0) {
      setErrors(validationErrors);
      return;
    }

    if (!currentOrder) return;

    try {
      const response = await fetch(`${API_BASE_URL}${PAYMENT_LINE_ITEM}`, {
        method: METHOD_POST,
        headers: { [HEADER_CONTENT_TYPE]: CONTENT_TYPE_JSON },
        body: JSON.stringify({
          order_id: currentOrder.id,
          name: itemName.trim(),
          price: priceValidation.cents,
          quantity: parseInt(itemQuantity)
        })
      });
      const data = await response.json();
      if (data.success) {
        setLineItems([...lineItems, {
          id: data.line_item.id,
          name: itemName,
          price: priceValidation.cents!,
          quantity: parseInt(itemQuantity)
        }]);
        setItemName("");
        setItemPrice("");
        setItemQuantity(DEFAULT_QUANTITY);
        setErrors({});
        setMessage(MSG_ITEM_ADDED);
      }
    } catch (error) {
      setMessage(MSG_ITEM_FAILED);
    }
  };

  const removeLineItem = async (lineItemId: string) => {
    if (!currentOrder) return;

    try {
      const response = await fetch(
        `${API_BASE_URL}${PAYMENT_LINE_ITEM}?order_id=${currentOrder.id}&line_item_id=${lineItemId}`,
        { method: "DELETE" }
      );
      const data = await response.json();
      if (data.success) {
        setLineItems(lineItems.filter(item => item.id !== lineItemId));
        setMessage("Item removed from order");
      }
    } catch (error) {
      setMessage("Failed to remove item");
    }
  };

  const getEcommerceKey = async () => {
    const isConnected = await checkCloverConnection();
    if (!isConnected) return;

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
    const isConnected = await checkCloverConnection();
    if (!isConnected) return;

    // Check for existing real-time validation errors
    const hasErrors = Object.values(errors).some(error => error);
    if (hasErrors) {
      return;
    }

    const validationErrors = validateCardForm(cardNumber, expMonth, expYear, cvv, zip);
    if (Object.keys(validationErrors).length > 0) {
      setErrors(validationErrors);
      return;
    }

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
      
      // Check if it's a Clover tokenization error (400 Bad Request)
      if (!response.ok && data.detail && data.detail.includes("400 Bad Request")) {
        setErrorDialog({
          show: true,
          title: "Invalid Card",
          message: "The card details are invalid. Please use a valid card.",
          isDecline: false
        });
        setMessage("");
        setCardNumber("");
        return;
      }
      
      if (data.success && data.token_data && data.token_data.id) {
        setSourceToken(data.token_data.id);
        setErrors({});
        setMessage(`${MSG_CARD_TOKENIZED}${data.token_data.id}`);
      } else if (!response.ok) {
        setErrorDialog({
          show: true,
          title: "Tokenization Error",
          message: "Unable to tokenize card. Please use another card and try again.",
          isDecline: false
        });
        setMessage("");
        setCardNumber("");
      } else {
        setMessage(`${MSG_CARD_TOKENIZE_FAILED}${JSON.stringify(data)}`);
      }
    } catch (error) {
      setErrorDialog({
        show: true,
        title: "Tokenization Error",
        message: "Unable to tokenize card. Please use another card and try again.",
        isDecline: false
      });
      setMessage("");
      setCardNumber("");
    }
  };

  const processPayment = async () => {
    const isConnected = await checkCloverConnection();
    if (!isConnected) return;

    const totalAmount = lineItems.reduce((sum, item) => sum + (item.price * item.quantity), 0);
    
    if (totalAmount < 1) {
      setErrors({ ...errors, amount: "Payment amount must be at least 0.01" });
      return;
    }

    const validationErrors = validateChargeForm(totalAmount);
    if (Object.keys(validationErrors).length > 0) {
      setErrors(validationErrors);
      return;
    }

    if (!currentOrder || !sourceToken) return;

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
        setErrors({});
      } else {
        const mappedError = mapPaymentError(data);
        setErrorDialog({
          show: true,
          title: mappedError.title,
          message: mappedError.message,
          isDecline: mappedError.isDecline
        });
        setMessage("");
      }
    } catch (error) {
      setMessage(`${MSG_PAYMENT_ERROR}${String(error)}`);
    }
  };

  const handleClearError = (field: keyof ValidationErrors) => {
    setErrors({ ...errors, [field]: undefined });
  };

  const handleExpMonthChange = (value: string) => {
    setExpMonth(value);
    
    setErrors(prevErrors => {
      const newErrors = { ...prevErrors };
      
      if (value) {
        const month = parseInt(value);
        if (isNaN(month) || month < 1 || month > 12) {
          newErrors.expMonth = "Month must be between 1 and 12";
        } else {
          delete newErrors.expMonth;
        }
      } else {
        delete newErrors.expMonth;
      }
      
      return newErrors;
    });
  };

  const handleExpYearChange = (value: string) => {
    setExpYear(value);
    
    setErrors(prevErrors => {
      const newErrors = { ...prevErrors };
      
      if (value) {
        const year = parseInt(value);
        const currentYear = new Date().getFullYear();
        
        if (isNaN(year) || year < currentYear || year > currentYear + 20) {
          newErrors.expYear = "Expiry year looks invalid. Please enter a realistic future year.";
        } else {
          delete newErrors.expYear;
        }
      } else {
        delete newErrors.expYear;
      }
      
      return newErrors;
    });
  };

  const handleZipChange = (value: string) => {
    setZip(value);
    
    setErrors(prevErrors => {
      const newErrors = { ...prevErrors };
      
      if (value) {
        const isValidZip = /^\d+$/.test(value) && (value.length === 5 || value.length === 9);
        
        if (!isValidZip) {
          newErrors.zip = "ZIP code must be 5 or 9 digits.";
        } else {
          delete newErrors.zip;
        }
      } else {
        delete newErrors.zip;
      }
      
      return newErrors;
    });
  };

  const totalAmount = lineItems.reduce((sum, item) => sum + (item.price * item.quantity), 0);

  return (
    <div style={{
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

              <OrderForm
                itemName={itemName}
                itemPrice={itemPrice}
                itemQuantity={itemQuantity}
                onItemNameChange={setItemName}
                onItemPriceChange={setItemPrice}
                onItemQuantityChange={setItemQuantity}
                onAddItem={addLineItem}
                errors={errors}
                onErrorClear={handleClearError}
              />

              <PaymentSummary
                lineItems={lineItems}
                totalAmount={totalAmount}
                ecommerceKey={ecommerceKey}
                sourceToken={sourceToken}
                onGetEcommerceKey={getEcommerceKey}
                onProcessPayment={processPayment}
                onRemoveLineItem={removeLineItem}
              />

              {ecommerceKey && !sourceToken && (
                <CardForm
                  cardNumber={cardNumber}
                  expMonth={expMonth}
                  expYear={expYear}
                  cvv={cvv}
                  zip={zip}
                  onCardNumberChange={setCardNumber}
                  onExpMonthChange={handleExpMonthChange}
                  onExpYearChange={handleExpYearChange}
                  onCvvChange={setCvv}
                  onZipChange={handleZipChange}
                  onTokenizeCard={tokenizeCard}
                  errors={errors}
                  onErrorClear={handleClearError}
                />
              )}
            </div>
          )}
        </div>
      )}

      <ErrorDialog
        show={errorDialog.show}
        title={errorDialog.title}
        message={errorDialog.message}
        isDecline={errorDialog.isDecline}
        onUseAnotherCard={handleUseAnotherCard}
        onClose={closeErrorDialog}
      />
    </div>
  );
}

export default App;
