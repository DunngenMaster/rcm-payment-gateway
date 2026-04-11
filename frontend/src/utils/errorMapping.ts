export interface PaymentErrorResponse {
  title: string;
  message: string;
  isDecline: boolean;
}

export const mapPaymentError = (errorData: any): PaymentErrorResponse => {
  const errorText = JSON.stringify(errorData);

  if (errorText.includes("card_declined") || errorText.includes("issuer_declined") || errorText.includes("Declined as sale count")) {
    return {
      title: "Payment Declined",
      message: "Declined as sale count per card amount is greater than configured amount. Try another card.",
      isDecline: true
    };
  }

  if (errorText.includes("invalid_card") || errorText.includes("card_number")) {
    return {
      title: "Invalid Card",
      message: "The card number looks invalid. Please check it and try again.",
      isDecline: true
    };
  }

  if (errorText.includes("exp_month") || errorText.includes("exp_year") || errorText.includes("invalid_expiry")) {
    return {
      title: "Invalid Expiry",
      message: "The expiry date looks invalid. Please update it and try again.",
      isDecline: true
    };
  }

  if (errorText.includes("cvc") || errorText.includes("cvv") || errorText.includes("invalid_cvv")) {
    return {
      title: "Invalid Security Code",
      message: "The security code looks invalid. Please check it and try again.",
      isDecline: true
    };
  }

  if (errorText.includes("source") || errorText.includes("token_required")) {
    return {
      title: "Tokenization Required",
      message: "Please tokenize the card before submitting payment.",
      isDecline: true
    };
  }

  if (errorText.includes("reused") || errorText.includes("already_used")) {
    return {
      title: "Token Reused",
      message: "This payment token has already been used. Please tokenize the card again.",
      isDecline: true
    };
  }

  return {
    title: "Payment Error",
    message: "Something went wrong while processing the payment. Please try again.",
    isDecline: true
  };
};
