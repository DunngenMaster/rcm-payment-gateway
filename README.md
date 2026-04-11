# RCM Payment Gateway Demo

A minimal full-stack checkout prototype that demonstrates Clover integration using OAuth, merchant-specific ecommerce key retrieval, frontend card tokenization, sandbox charge creation, and local transaction logging.

## Overview

This project was built as a small, recruiter-friendly prototype to show a clean Clover payment integration without overengineering the stack.

The application supports:

- Clover OAuth2 merchant connection
- Merchant-specific ecommerce key retrieval through Clover PAKMS
- Card tokenization in the frontend using Clover sandbox
- Sandbox charge creation from the backend using the tokenized source
- Order creation and line item support
- Local transaction logging for payment attempts
- A minimal React UI for testing the full flow

## Tech Stack

### Backend
- FastAPI
- Python
- httpx
- Pydantic

### Frontend
- React
- TypeScript
- Vite

### Payment Platform
- Clover Sandbox APIs

## Requirements

- Python 3.10+
- Node.js 18+
- A Clover sandbox developer app and sandbox merchant account
- Ecommerce API integration enabled in Clover sandbox settings
- Public and private Clover ecommerce tokens generated for sandbox testing

## Clover Configuration

This project assumes the Clover app is configured as a web-based sandbox app.

### Clover App Settings

Use the following values in Clover sandbox developer settings:

- **Site URL:** `http://localhost:5173`
- **Alternate Launch Path:** `/`
- **Default OAuth Response:** `Code`
- **CORS Domain:** `http://localhost:5173`

### Permissions

Enable at least:

- Merchant Read
- Orders Read
- Orders Write
- Payments Read
- Payments Write

### Ecommerce Integration

Select:

- **Integration Type:** `API`

Generate the Clover ecommerce tokens for sandbox use:

- Public token
- Private token

## Environment Variables

Create `backend/.env` and configure values similar to the following:

```env
CLOVER_CLIENT_ID=your_app_id
CLOVER_CLIENT_SECRET=your_app_secret
CLOVER_REDIRECT_URI=http://localhost:5173/auth/callback
CLOVER_AUTH_BASE_URL=https://sandbox.dev.clover.com
CLOVER_API_BASE_URL=https://apisandbox.dev.clover.com
CLOVER_ECOMMERCE_BASE_URL=https://scl-sandbox.dev.clover.com
CLOVER_TOKEN_BASE_URL=https://token-sandbox.dev.clover.com
CLOVER_ECOMMERCE_PRIVATE_TOKEN=your_private_ecommerce_token
FRONTEND_URL=http://localhost:5173
TOKEN_ENCRYPTION_KEY=your_fernet_key