import type { ValidationErrors } from "../validations";

interface CardFormProps {
  cardNumber: string;
  expMonth: string;
  expYear: string;
  cvv: string;
  zip: string;
  onCardNumberChange: (value: string) => void;
  onExpMonthChange: (value: string) => void;
  onExpYearChange: (value: string) => void;
  onCvvChange: (value: string) => void;
  onZipChange: (value: string) => void;
  onTokenizeCard: () => void;
  errors: ValidationErrors;
  onErrorClear: (field: keyof ValidationErrors) => void;
}

export const CardForm = (props: CardFormProps) => {
  const errorStyle = { color: "#d32f2f", fontSize: "12px", marginTop: "2px" };

  return (
    <div style={{ marginBottom: "20px" }}>
      <h4>Card Details</h4>

      <div style={{ marginBottom: "8px" }}>
        <input
          type="text"
          placeholder="Card Number"
          value={props.cardNumber}
          onChange={(e) => {
            props.onCardNumberChange(e.target.value);
            if (props.errors.cardNumber) props.onErrorClear("cardNumber");
          }}
          style={{ margin: "5px", padding: "8px", width: "calc(100% - 20px)" }}
        />
        {props.errors.cardNumber && <div style={errorStyle}>{props.errors.cardNumber}</div>}
      </div>

      <div style={{ display: "flex", gap: "10px", marginBottom: "8px" }}>
        <div>
          <input
            type="text"
            placeholder="MM"
            value={props.expMonth}
            onChange={(e) => {
              props.onExpMonthChange(e.target.value);
              if (props.errors.expMonth) props.onErrorClear("expMonth");
            }}
            maxLength={2}
            style={{ padding: "8px", width: "60px" }}
          />
          {props.errors.expMonth && <div style={errorStyle}>{props.errors.expMonth}</div>}
        </div>

        <div>
          <input
            type="text"
            placeholder="YYYY"
            value={props.expYear}
            onChange={(e) => {
              props.onExpYearChange(e.target.value);
              if (props.errors.expYear) props.onErrorClear("expYear");
            }}
            maxLength={4}
            style={{ padding: "8px", width: "80px" }}
          />
          {props.errors.expYear && <div style={errorStyle}>{props.errors.expYear}</div>}
        </div>

        <div>
          <input
            type="text"
            placeholder="CVV"
            value={props.cvv}
            onChange={(e) => {
              props.onCvvChange(e.target.value);
              if (props.errors.cvv) props.onErrorClear("cvv");
            }}
            maxLength={4}
            style={{ padding: "8px", width: "60px" }}
          />
          {props.errors.cvv && <div style={errorStyle}>{props.errors.cvv}</div>}
        </div>

        <div>
          <input
            type="text"
            placeholder="ZIP"
            value={props.zip}
            onChange={(e) => {
              props.onZipChange(e.target.value);
              if (props.errors.zip) props.onErrorClear("zip");
            }}
            style={{ padding: "8px", width: "80px" }}
          />
          {props.errors.zip && <div style={errorStyle}>{props.errors.zip}</div>}
        </div>
      </div>

      <button onClick={props.onTokenizeCard} style={{
        padding: "10px 20px",
        fontSize: "14px",
        cursor: "pointer",
        backgroundColor: "#FF5722",
        color: "white",
        border: "none",
        borderRadius: "4px",
        marginTop: "10px"
      }}>
        Proceed to Payment
      </button>
    </div>
  );
};
