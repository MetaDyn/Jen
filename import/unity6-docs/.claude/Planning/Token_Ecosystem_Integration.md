# Token Ecosystem Integration Plan (Base)

## Goal
Integrate a token‑powered economy for trading, buying/selling digital assets, and in‑game transactions across the dashboard and Unity client, while keeping wallet custody on the user side.

## Principles
- Wallet connect handled on the dashboard; Unity consumes authenticated wallet state.
- Fast UX via off‑chain services; on‑chain settlement where needed.
- Clear separation: identity/auth (Supabase) vs asset/transaction logic.

## High‑Level Architecture
### 1) Identity & Wallet Link
- Dashboard links wallet via signature challenge.
- Supabase profile stores `wallet_address`, `wallet_chain`, and timestamps.
- Unity reads wallet status and displays balance + transaction state.

### 2) Asset Registry
- Supabase tables for asset metadata (name, type, creator, URIs, tags).
- Optional on‑chain token IDs for NFTs or transferable items.
- Versioning and ownership history recorded in Supabase.

### 3) Marketplace Service
- Listing creation, pricing, and availability stored in Supabase.
- Order book and escrow logic handled by backend.
- Settlement handled on‑chain when transferring ownership (NFT) or funds.

### 4) Transaction Service
- In‑game purchases call a backend endpoint to:
  1) Validate user identity and wallet link
  2) Refresh on‑chain balance
  3) Create a transaction intent
  4) Return signed receipt or transaction payload

### 5) Receipts & Audit
- Every transaction emits a signed receipt stored in Supabase.
- Receipt references item ID, price, wallet address, timestamp, tx hash (if on‑chain).

## On‑Chain vs Off‑Chain Strategy
### Hybrid Recommendation
- **Off‑chain** for speed (UI checkout, confirmations, inventory updates).
- **On‑chain** for ownership transfers or withdrawals.
- Periodic reconciliation from chain to Supabase.

## Supabase Data Model (Suggested)
- `profiles`: wallet fields + balance snapshot
- `assets`: asset metadata + creator + ownership
- `listings`: price, currency, seller, status
- `orders`: buyer, seller, item, status
- `transactions`: receipt, tx hash, status

## Dashboard Responsibilities
- Wallet connect + signature verification
- Marketplace UI (listings, offers, purchases)
- Transaction history + receipts

## Unity Responsibilities
- Display wallet link status + balance
- Trigger purchase intent via backend
- Render owned assets and unlock in‑world items

## Security & Integrity
- Never expose private keys in Unity.
- Verify signatures server‑side.
- Refresh balance before any purchase.
- Rate‑limit refresh endpoints.
- Ensure receipts are signed and tamper‑evident.

## Implementation Steps
1) Wallet link + signature verification endpoints.
2) Balance refresh service (Base RPC provider).
3) Asset registry + ownership tracking.
4) Marketplace listing + order flow.
5) Unity integration for purchase intents.
6) On‑chain settlement (token/NFT) where required.
7) Audit + receipt dashboard.

## Open Questions
- On‑chain only vs hybrid?
- NFTs for assets or off‑chain ownership?
- Single token vs multi‑token (stablecoin for pricing)?
- Refund and dispute handling?

