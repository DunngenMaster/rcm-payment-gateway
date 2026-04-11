export interface ValidationErrors {
  itemName?: string;
  itemPrice?: string;
  itemQuantity?: string;
  cardNumber?: string;
  expMonth?: string;
  expYear?: string;
  cvv?: string;
  zip?: string;
  amount?: string;
}

export const validateOrderForm = (
  itemName: string,
  itemPrice: string,
  itemQuantity: string
): ValidationErrors => {
  const newErrors: ValidationErrors = {};
  const trimmedTitle = itemName.trim();

  if (!trimmedTitle || trimmedTitle.length < 2) {
    newErrors.itemName = "Item name required, minimum 2 characters";
  }

  const price = parseFloat(itemPrice);
  if (!itemPrice || isNaN(price) || price <= 0) {
    newErrors.itemPrice = "Price must be greater than 0";
  }

  const quantity = parseInt(itemQuantity);
  if (!itemQuantity || isNaN(quantity) || quantity <= 0) {
    newErrors.itemQuantity = "Quantity must be a positive whole number";
  }

  return newErrors;
};

export const validateCardForm = (
  cardNumber: string,
  expMonth: string,
  expYear: string,
  cvv: string,
  zip: string
): ValidationErrors => {
  const newErrors: ValidationErrors = {};

  const cardDigits = cardNumber.replace(/\s/g, "");
  if (!cardDigits || !/^\d+$/.test(cardDigits) || (cardDigits.length !== 15 && cardDigits.length !== 16)) {
    newErrors.cardNumber = "Card number must be 15 or 16 digits";
  }

  const month = parseInt(expMonth);
  if (!expMonth || isNaN(month) || month < 1 || month > 12) {
    newErrors.expMonth = "Month must be between 1 and 12";
  }

  const year = parseInt(expYear);
  const currentYear = new Date().getFullYear();
  if (!expYear || isNaN(year) || year < currentYear || year > currentYear + 20) {
    newErrors.expYear = "Expiry year looks invalid. Please enter a realistic future year.";
  }

  const cvvDigits = cvv.replace(/\s/g, "");
  if (!cvvDigits || !/^\d{3,4}$/.test(cvvDigits)) {
    newErrors.cvv = "CVV must be 3 or 4 digits";
  }

  if (!zip || zip.length < 5) {
    newErrors.zip = "ZIP code required, minimum 5 characters";
  }

  return newErrors;
};

export const validateChargeForm = (totalAmount: number): ValidationErrors => {
  const newErrors: ValidationErrors = {};

  if (totalAmount <= 0) {
    newErrors.amount = "Amount must be greater than 0";
  }

  return newErrors;
};
