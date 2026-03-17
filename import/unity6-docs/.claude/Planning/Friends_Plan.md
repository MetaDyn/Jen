# Friends System Plan

## Goal
Implement a persistent friends system backed by Supabase, with Photon friend lookup for presence/room status, and in-world UI actions (Add Friend, View Profile, etc.).

## Core Design
- **Canonical ID:** Supabase `userId` is the primary identifier.
- **Photon Presence:** Populate Photon friend lookup list with Supabase friend IDs for online/room status.
- **Persistence:** Store friend relationships in Supabase (not Photon), then sync to client.

## Supabase Schema (Recommended)
### Table: `friends`
- `user_id` (uuid)
- `friend_id` (uuid)
- `status` (text: `pending`, `accepted`, `blocked`)
- `created_at` (timestamp)
- `updated_at` (timestamp)

**Constraints**
- Unique: `(user_id, friend_id)`

**RLS (High level)**
- Users can read rows where they are `user_id` or `friend_id`.
- Users can insert/update rows where they are `user_id`.

## Unity Client Flow
1. On login, fetch accepted friends from Supabase.
2. Call Photon friend lookup with friend IDs to get presence/room data.
3. Cache friend status locally for UI use.

## UI Integration
### Existing Entry Point
- `Assets/MetaDyn/UserList/UserListEntry.cs` already exposes a context menu.

### Add Menu Actions
- `Add Friend` / `Remove Friend` (toggle by status)
- `View Profile` (open dashboard profile or in-world UI)
- Optional: `Invite` / `Join` if room info is available

### Avatar Click
- Add click interaction on avatar or nametag to open the same context menu.

## Incremental Implementation Steps
1. **Data plumbing:** Add `UserId` to `UserData` so UI can target the correct Supabase user.
2. **Supabase service:** Create `FriendsService` for read/write of friend status.
3. **Presence:** Use Photon friend lookup with accepted IDs.
4. **UI:** Extend context menu actions and state display.

## Open Questions
- Mutual approval vs one-way follow?
- Friend requests handled in dashboard, in-world, or both?
- View Profile opens web dashboard or Unity panel?

## Notes
Photon friend lookup is not persistent; Supabase is the source of truth.

