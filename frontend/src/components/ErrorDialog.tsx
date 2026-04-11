interface ErrorDialogProps {
  show: boolean;
  title: string;
  message: string;
  isDecline: boolean;
  onUseAnotherCard: () => void;
  onClose: () => void;
}

export const ErrorDialog = (props: ErrorDialogProps) => {
  if (!props.show) return null;

  return (
    <div style={{
      position: "fixed",
      top: 0,
      left: 0,
      width: "100%",
      height: "100%",
      backgroundColor: "rgba(0,0,0,0.5)",
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      zIndex: 1000
    }}>
      <div style={{
        backgroundColor: "white",
        padding: "30px",
        borderRadius: "8px",
        maxWidth: "400px",
        textAlign: "center",
        boxShadow: "0 2px 10px rgba(0,0,0,0.2)"
      }}>
        <h3 style={{ color: "#d32f2f", marginBottom: "15px" }}>{props.title}</h3>
        <p style={{ marginBottom: "25px", color: "#333" }}>{props.message}</p>
        <div style={{ display: "flex", gap: "10px", justifyContent: "center" }}>
          {props.isDecline && (
            <button onClick={props.onUseAnotherCard} style={{
              padding: "10px 20px",
              fontSize: "14px",
              cursor: "pointer",
              backgroundColor: "#2196F3",
              color: "white",
              border: "none",
              borderRadius: "4px"
            }}>
              Use Another Card
            </button>
          )}
          <button onClick={props.onClose} style={{
            padding: "10px 20px",
            fontSize: "14px",
            cursor: "pointer",
            backgroundColor: "#757575",
            color: "white",
            border: "none",
            borderRadius: "4px"
          }}>
            Close
          </button>
        </div>
      </div>
    </div>
  );
};
