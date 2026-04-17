interface LineItem {
  id: string;
  name: string;
  price: number;
  quantity: number;
}

interface PaymentSummaryProps {
  lineItems: LineItem[];
  totalAmount: number;
  onAddCardDetails: () => void;
  onProcessPayment: () => void;
  onRemoveLineItem: (lineItemId: string) => void;
  sourceToken: string | null;
  ecommerceKey: string | null;
}

export const PaymentSummary = (props: PaymentSummaryProps) => {
  return (
    <>
      {props.lineItems.length > 0 && (
        <div style={{ marginBottom: "20px" }}>
          <h4>Order Items</h4>
          {props.lineItems.map((item) => (
            <div key={item.id} style={{ padding: "5px", borderBottom: "1px solid #ccc", display: "flex", justifyContent: "space-between", alignItems: "center" }}>
              <span>{item.name} - ${(item.price / 100).toFixed(2)} x {item.quantity}</span>
              <button onClick={() => props.onRemoveLineItem(item.id)} style={{
                padding: "4px 8px",
                fontSize: "12px",
                cursor: "pointer",
                backgroundColor: "#f44336",
                color: "white",
                border: "none",
                borderRadius: "3px"
              }}>
                Remove
              </button>
            </div>
          ))}
          <div style={{ fontWeight: "bold", marginTop: "10px" }}>
            Total: ${(props.totalAmount / 100).toFixed(2)}
          </div>
        </div>
      )}

      {props.lineItems.length > 0 && !props.ecommerceKey && (
        <button onClick={props.onAddCardDetails} style={{
          padding: "10px 20px",
          fontSize: "14px",
          cursor: "pointer",
          backgroundColor: "#9C27B0",
          color: "white",
          border: "none",
          borderRadius: "4px",
          marginRight: "10px"
        }}>
          Add Card Details
        </button>
      )}

      {props.sourceToken && (
        <button onClick={props.onProcessPayment} style={{
          padding: "10px 20px",
          fontSize: "16px",
          cursor: "pointer",
          backgroundColor: "#4CAF50",
          color: "white",
          border: "none",
          borderRadius: "4px"
        }}>
          Charge ${(props.totalAmount / 100).toFixed(2)}
        </button>
      )}
    </>
  );
};
