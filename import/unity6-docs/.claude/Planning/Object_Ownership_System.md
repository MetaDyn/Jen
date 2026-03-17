# Object Ownership & Marketplace System Plan

**Status:** Draft | **Date:** 2026-01-07

## Overview
This document outlines the architecture for implementing Object Ownership, User Inventory, and a Marketplace system for MetaDyn. The goal is to allow users to own digital assets (items), view them in a persistent inventory, and spawn them into the world (Unity). Additionally, a marketplace will allow users to acquire these items.

## 1. Database Schema (Supabase)

We will extend the existing Supabase schema with the following tables.

### `items` (Global Catalog)
Defines all unique items available in the system.
*   `id` (UUID, Primary Key)
*   `name` (Text)
*   `description` (Text)
*   `type` (Text) - e.g., "Furniture", "Wearable", "Gadget"
*   `prefab_path` (Text) - Resource path or Addressable key in Unity
*   `icon_url` (Text) - URL for dashboard/UI display
*   `metadata` (JSONB) - Custom properties (weight, rarity, etc.)
*   `is_active` (Boolean) - For soft deletion
*   `created_at` (Timestamp)

### `user_inventory` (Ownership)
Links users to items they own.
*   `id` (UUID, Primary Key)
*   `user_id` (UUID, FK to `auth.users`)
*   `item_id` (UUID, FK to `items`)
*   `quantity` (Integer) - Default 1
*   `instance_metadata` (JSONB) - Specific data for this instance (e.g., color customization, durability)
*   `acquired_at` (Timestamp)

### `marketplace_listings` (Store)
Items listed for sale (initially System-to-User).
*   `id` (UUID, Primary Key)
*   `item_id` (UUID, FK to `items`)
*   `seller_id` (UUID, FK to `auth.users`, NULL for System)
*   `price` (Integer/Decimal) - Currency amount (needs currency system definition)
*   `currency_type` (Text) - "USD", "Gold", etc.
*   `stock` (Integer) - NULL for infinite (digital goods)
*   `is_active` (Boolean)

### `transactions` (Audit Log)
Record of all transfers/purchases.
*   `id` (UUID, Primary Key)
*   `buyer_id` (UUID)
*   `seller_id` (UUID)
*   `listing_id` (UUID)
*   `amount` (Decimal)
*   `created_at` (Timestamp)

## 2. Dashboard Implementation (Web)

The dashboard (React/Next.js) will be the primary interface for management and purchasing.

### Features
*   **Inventory View:** A new page `/inventory` displaying a grid of cards for owned items.
*   **Marketplace View:** A new page `/market` displaying active listings.
*   **Admin Item Creator:** (Admin only) Form to add new rows to the `items` table.
*   **Purchase Flow:**
    *   Click "Buy" on Marketplace item.
    *   Call Supabase Edge Function `purchase_item`.
    *   Function verifies funds (if applicable), creates `transaction`, decrements `stock`, and inserts/updates `user_inventory`.

## 3. Unity Implementation (Client)

The Unity client handles the visualization and usage of items.

### Data Structures
*   **`InventoryItem` (ScriptableObject):** Client-side definition.
    *   `string id` (Matches Supabase UUID)
    *   `string displayName`
    *   `Sprite icon`
    *   `GameObject prefab`
*   **`ItemCatalog` (ScriptableObject):** Registry mapping IDs to `InventoryItem` assets.

### Managers
*   **`InventoryManager` (Singleton):**
    *   `FetchInventory()`: Calls Supabase `user_inventory` table on login (via `SupabaseAuthManager`).
    *   `List<UserItem> OwnedItems`: C# list of owned items.
    *   `SyncInventory()`: Re-fetches data (called after purchase or explicit refresh).
*   **`MarketplaceManager` (Singleton):**
    *   `FetchListings()`: Gets data from `marketplace_listings`.
    *   `PurchaseItem(string listingId)`: Calls Supabase Edge Function or RPC.

### UI
*   **Inventory UI:** Tab in the `UIGameMenu` or a dedicated panel.
    *   Grid of icons.
    *   Selection details (Name, Desc).
    *   **"Spawn" / "Equip" Button.**

### Spawning Logic
1.  User clicks "Spawn" in UI.
2.  `InventoryManager` verifies ownership locally (and optionally via server check).
3.  `NetworkSpawner` requests `NetworkRunner.Spawn`.
4.  Spawned object has `NetworkObject` and `OwnershipComponent`.
    *   `OwnershipComponent` syncs `owner_id` (Supabase UUID).
    *   Only `owner_id` can pickup/move/despawn (unless permissions allow otherwise).

## 4. Workflows

### A. Initialization
1.  **Unity Start:** `SupabaseAuthManager` logs in.
2.  **Event:** `OnLoginSuccess` triggers `InventoryManager.FetchInventory()`.
3.  **Result:** `InventoryManager` populates internal list and UI.

### B. Spawning an Item
1.  **UI:** User selects "Red Chair" -> Clicks Spawn.
2.  **Check:** `InventoryManager` confirms `quantity > 0` (if consumables) or simple ownership.
3.  **Action:** `Runner.Spawn(prefab, position, rotation, inputAuthority: LocalPlayer)`.
4.  **Setup:** `OnSpawned()` on object sets `OwnerID` to local player's UUID.

## 5. Next Steps
1.  **Database:** Run SQL migrations in Supabase to create tables.
2.  **Dashboard:** Create basic Inventory/Market pages.
3.  **Unity:**
    *   Create `InventoryItem` ScriptableObject definition.
    *   Implement `InventoryManager`.
    *   Build `InventoryUI`.
