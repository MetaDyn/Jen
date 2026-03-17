# Wallet Connect Integration (ETH + SOL)

## Goal
Allow users to link an Ethereum or Solana wallet on the dashboard, store wallet data in Supabase, and use fresh balances inside Unity for balance‑gated actions.

## Scope
- Wallet connect handled **on the dashboard only**.
- Unity reads wallet link + balance from Supabase.
- Balances refreshed **on demand** whenever a balance‑gated action is attempted.

## Dashboard Flow
1. User clicks “Connect Wallet”.
2. WalletConnect (ETH) or Solana wallet adapter prompts connection.
3. User signs a nonce challenge to prove ownership.
4. Backend verifies signature and upserts wallet info into Supabase.

## Supabase Schema (profiles)
Add fields:
- `wallet_address` (text)
- `wallet_chain` (text: `ethereum` | `solana`)
- `wallet_linked_at` (timestamp)
- `wallet_balance` (numeric)
- `wallet_balance_updated_at` (timestamp)

## Balance Refresh (On Demand)
- Before any balance‑gated action, call a backend endpoint to:
  1) Fetch current balance from chain
  2) Update Supabase fields
  3) Return the updated balance

## Unity Usage
- Read wallet status via Supabase profile fields.
- If not linked, prompt user to open dashboard.
- For balance‑gated actions, call refresh endpoint first, then proceed.

## Backend Components
- **Signature verification** endpoint:
  - ETH: verify EIP‑191/EIP‑712 signature for nonce
  - SOL: verify signature with public key
- **Balance refresh** endpoint:
  - ETH: query provider (Infura/Alchemy)
  - SOL: query RPC (Helius/QuickNode)

## Security Notes
- Always verify wallet ownership via signature.
- Do not accept wallet address from client without verification.
- Store refresh timestamps to prevent abuse.

## Open Questions
- Which providers to use for ETH/SOL RPC?
- Do we allow multiple wallets per user?
- Do we need support for NFTs vs token balances?

