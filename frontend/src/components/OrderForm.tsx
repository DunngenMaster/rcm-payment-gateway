import { validateOrderForm } from "../validations";
import type { ValidationErrors } from "../validations";

interface OrderFormProps {
  itemName: string;
  itemPrice: string;
  itemQuantity: string;
  onItemNameChange: (value: string) => void;
  onItemPriceChange: (value: string) => void;
  onItemQuantityChange: (value: string) => void;
  onAddItem: () => void;
  errors: ValidationErrors;
  onErrorClear: (field: keyof ValidationErrors) => void;
}

export const OrderForm = (props: OrderFormProps) => {
  const errorStyle = { color: "#d32f2f", fontSize: "12px", marginTop: "2px" };

  return (
    <div style={{ marginBottom: "20px" }}>
      <h4>Add Item</h4>
      <div style={{ marginBottom: "8px" }}>
        <input
          type="text"
          placeholder="Item name"
          value={props.itemName}
          onChange={(e) => {
            props.onItemNameChange(e.target.value);
            if (props.errors.itemName) props.onErrorClear("itemName");
          }}
          style={{ margin: "5px", padding: "5px", width: "calc(100% - 20px)" }}
        />
        {props.errors.itemName && <div style={errorStyle}>{props.errors.itemName}</div>}
      </div>

      <div style={{ marginBottom: "8px" }}>
        <input
          type="number"
          placeholder="Price ($)"
          value={props.itemPrice}
          onChange={(e) => {
            props.onItemPriceChange(e.target.value);
            if (props.errors.itemPrice) props.onErrorClear("itemPrice");
          }}
          style={{ margin: "5px", padding: "5px" }}
        />
        {props.errors.itemPrice && <div style={errorStyle}>{props.errors.itemPrice}</div>}
      </div>

      <div style={{ marginBottom: "8px" }}>
        <input
          type="number"
          placeholder="Quantity"
          value={props.itemQuantity}
          onChange={(e) => {
            props.onItemQuantityChange(e.target.value);
            if (props.errors.itemQuantity) props.onErrorClear("itemQuantity");
          }}
          min="1"
          style={{ margin: "5px", padding: "5px", width: "60px" }}
        />
        {props.errors.itemQuantity && <div style={errorStyle}>{props.errors.itemQuantity}</div>}
      </div>

      <button onClick={props.onAddItem} style={{
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
  );
};
