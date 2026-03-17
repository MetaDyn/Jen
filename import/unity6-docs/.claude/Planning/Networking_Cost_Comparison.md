# Networking Cost Comparison

Side-by-side cost analysis of multiplayer networking options for MetaDyn.

**Created:** 2026-01-20
**Related:**
- [Custom_WebSocket_Networking_Plan.md](Custom_WebSocket_Networking_Plan.md)
- [Cloudflare_Realtime_Infrastructure.md](Cloudflare_Realtime_Infrastructure.md)
- [UGS_Networking_Plan.md](UGS_Networking_Plan.md)

---

## Pricing Models

| Solution | Pricing Model | Base Cost |
|----------|---------------|-----------|
| **Photon Fusion** | Per CCU (concurrent user) | $50 for first 50, then $1/CCU |
| **Unity Gaming Services** | Per CCU + bandwidth | 50 CCU free, then $0.16/CCU + $0.09/GiB |
| **Cloudflare DO** | Per message | $0.15 per million messages |
| **Custom WebSocket** | Server hosting | $6-192/month (VPS) |

---

## UGS Pricing Breakdown

### Unity Relay
- **Free tier:** 50 average monthly CCU (~2.16M connectivity minutes)
- **Per CCU:** $0.16 per additional CCU
- **Bandwidth:** 3 GiB free per CCU (max 150 GiB), then $0.09/GiB (US+EU) or $0.16/GiB (Asia)

### Unity Lobby
- **Free tier:** 10 GiB/month per region
- **Overage:** $0.09/GiB (US+EU) or $0.16/GiB (Asia)

### Vivox (Voice + Text)
- **Free tier:** 5,000 PCU (Peak Concurrent Users)
- **Paid tiers:**
  - 5,001-50,000 PCU: $2,000 per 5,000 PCU ($0.40/user)
  - 50,001-100,000 PCU: $1,500 per 5,000 PCU ($0.30/user)
  - 100,001+: $1,000 per 5,000 PCU ($0.20/user)

**Note:** Vivox's 5,000 PCU free tier covers most indie/small projects entirely.

---

## Cost Comparison Table

### All Solutions Compared (assumes ~100-200 GB bandwidth/100 CCU)

| CCU | Photon | UGS (Relay+Lobby) | UGS + Vivox | Cloudflare (5 msg/s) | Custom VPS |
|-----|--------|-------------------|-------------|----------------------|------------|
| 50 | $50 | **$0** | **$0** | $32 | $6 |
| 100 | $100 | ~$13 | ~$13 | $65 | $12 |
| 200 | $200 | ~$39 | ~$39 | $130 | $24 |
| 500 | $500 | ~$117 | ~$117 | $325 | $48 |
| 1000 | $1,000 | ~$242 | ~$242 | $650 | $96 |
| 2000 | $2,000 | ~$492 | ~$492 | $1,300 | $192 |
| 5000 | $5,000 | ~$1,200 | ~$3,200* | $3,250 | ~$500 |

*At 5000 CCU, Vivox exceeds free tier: add $2,000 for voice

---

### UGS Cost Breakdown by Component

| CCU | Relay CCU Cost | Est. Bandwidth Cost | Lobby | Vivox | **Total** |
|-----|----------------|---------------------|-------|-------|-----------|
| 50 | $0 (free) | $0 (free) | $0 | $0 | **$0** |
| 100 | $8 | ~$5 | $0 | $0 | **~$13** |
| 200 | $24 | ~$15 | $0 | $0 | **~$39** |
| 500 | $72 | ~$45 | $0 | $0 | **~$117** |
| 1000 | $152 | ~$90 | $0 | $0 | **~$242** |
| 2000 | $312 | ~$180 | $0 | $0 | **~$492** |

---

## Visual Comparison (1000 CCU)

```
Monthly Cost at 1000 Concurrent Users:

Photon Fusion     ████████████████████████████████████████  $1,000

UGS (Relay+Vivox) ██████████  $242

Cloudflare DO
  @ 5 msg/s       ██████████████████████████  $650

Custom VPS        ████  $96
```

---

### At Default Message Rates (20 msg/s per player, 8hrs/day)

| CCU | Photon | UGS | Cloudflare DO | Custom VPS |
|-----|--------|-----|---------------|------------|
| 50 | $50 | $0 | $130 | $6 |
| 100 | $100 | $13 | $260 | $12 |
| 200 | $200 | $39 | $520 | $24 |
| 500 | $500 | $117 | $1,300 | $48 |
| 1000 | $1,000 | $242 | $2,600 | $96 |
| 2000 | $2,000 | $492 | $5,200 | $192 |

**Winner at 20 msg/s:** Custom VPS cheapest, UGS best managed option

---

### At Optimized Message Rates (10 msg/s, client interpolation)

| CCU | Photon | UGS | Cloudflare DO | Custom VPS |
|-----|--------|-----|---------------|------------|
| 50 | $50 | $0 | $65 | $6 |
| 100 | $100 | $13 | $130 | $12 |
| 200 | $200 | $39 | $260 | $24 |
| 500 | $500 | $117 | $650 | $48 |
| 1000 | $1,000 | $242 | $1,300 | $96 |
| 2000 | $2,000 | $492 | $2,600 | $192 |

**Winner at 10 msg/s:** Custom VPS cheapest, UGS beats both Photon and Cloudflare

---

### At Aggressive Optimization (5 msg/s average)

| CCU | Photon | UGS | Cloudflare DO | Custom VPS |
|-----|--------|-----|---------------|------------|
| 50 | $50 | $0 | $32 | $6 |
| 100 | $100 | $13 | $65 | $12 |
| 200 | $200 | $39 | $130 | $24 |
| 500 | $500 | $117 | $325 | $48 |
| 1000 | $1,000 | $242 | $650 | $96 |
| 2000 | $2,000 | $492 | $1,300 | $192 |

**Winner at 5 msg/s:** Custom VPS cheapest, UGS is clear #2

---

## Visual Comparison (1000 CCU)

```
Monthly Cost at 1000 Concurrent Users:

Photon Fusion     ████████████████████████████████████████  $1,000

Cloudflare DO
  @ 20 msg/s      ████████████████████████████████████████████████████████████████████████████████████████████████████████  $2,600
  @ 10 msg/s      ████████████████████████████████████████████████████████  $1,300
  @ 5 msg/s       ██████████████████████████  $650
  @ 3 msg/s       ████████████████  $390

Custom VPS        ████  $96
```

---

## Hidden Costs & Considerations

### Photon Fusion

| Factor | Impact |
|--------|--------|
| CCU Overages | Charged if you exceed plan |
| Voice (Photon Voice) | Additional cost if used |
| Chat (Photon Chat) | Additional cost |
| Relay Servers | Included |
| Global Infrastructure | Included |
| Support | Included at higher tiers |

**True cost:** Base price covers most features, but voice/chat add-ons exist.

---

### Unity Gaming Services (UGS)

| Factor | Impact |
|--------|--------|
| Relay CCU | $0.16/CCU after 50 free |
| Relay Bandwidth | $0.09-0.16/GiB after 150 GiB free |
| Lobby | Usually within free tier |
| Vivox Voice | FREE up to 5,000 PCU (huge benefit) |
| Vivox Text | Included with voice |
| Authentication | Free |
| Global Infrastructure | Included (Unity's relay network) |
| $800 Credit | New projects get $800 multiplayer credit |

**True cost:** Very competitive. Vivox's 5,000 PCU free tier is a major advantage over Photon Voice.

**Key advantages over Photon:**
- 50 CCU free (vs ~20 for Photon)
- Vivox voice FREE for 5,000 PCU
- First-party Unity integration
- $800 new joiner credit
- Bandwidth-based = pay for actual usage

**Potential gotchas:**
- Bandwidth can add up with high tick rates
- Vivox gets expensive above 5,000 PCU
- Less battle-tested than Photon

---

### Cloudflare Durable Objects

| Factor | Impact |
|--------|--------|
| Request costs | $0.15/million (main cost) |
| Duration costs | Near-zero with hibernation |
| Storage | $0.20/GB (minimal for game state) |
| D1 Database | $5/month for persistence |
| Workers | Included in requests |
| Global Edge | Included |
| WebRTC Signaling | Included (same WebSocket) |
| Chat | Included (same WebSocket) |

**True cost:** Message cost is everything. No hidden fees for features.

**Optimization strategies:**
- Delta compression (only send changes)
- Adaptive tick rate (idle players = fewer updates)
- Batch updates (combine multiple state changes)
- Binary protocol instead of JSON (smaller messages)

---

### Custom WebSocket (VPS)

| Factor | Impact |
|--------|--------|
| Server hosting | $6-192/month |
| Bandwidth overage | Usually 1-5TB free, then $0.01/GB |
| SSL Certificate | Free (Let's Encrypt) |
| Domain | Already have (metadyn.xyz) |
| Load balancer | $10-20/month at scale |
| Monitoring | $0-20/month (Grafana Cloud free tier) |
| Backups | $1-5/month |
| DevOps time | Your time to maintain |
| DDoS protection | Need Cloudflare proxy ($0 if proxied) |

**True cost:** ~$10-250/month depending on scale + your maintenance time.

**Hidden effort:**
- Server setup and hardening
- SSL configuration
- Deployment pipeline
- Monitoring and alerting
- Scaling decisions
- Security patches
- Uptime responsibility

---

## Feature Comparison

| Feature | Photon | UGS | Cloudflare DO | Custom VPS |
|---------|--------|-----|---------------|------------|
| WebSocket support | Yes | Yes (Unity Transport) | Yes | Yes |
| Global edge servers | Yes (Photon cloud) | Yes (Unity Relay) | Yes (300+ locations) | No (single region)* |
| Auto-scaling | Yes | Yes | Yes | Manual |
| State synchronization | Built-in | Built-in (NGO) | DIY | DIY |
| Interest management | Built-in | Built-in (NGO) | DIY | DIY |
| Lag compensation | Built-in | Basic (NGO) | DIY | DIY |
| Host migration | Built-in | Manual | DIY | DIY |
| Voice chat | Add-on ($) | **Vivox FREE (5k PCU)** | DIY (WebRTC) | DIY |
| Text chat | Add-on ($) | Vivox included | Included | Included |
| Matchmaking/Lobby | Built-in | Built-in (Lobby) | DIY | DIY |
| Analytics | Dashboard | Unity Dashboard | Cloudflare Analytics | DIY |
| Unity integration | Good (SDK) | **Native (first-party)** | DIY | DIY |
| WebGL support | Full | Full | Full | Full |
| Maintenance | Zero | Zero | Near-zero | Medium |
| Learning curve | Medium | Medium | Low | Low |
| Vendor lock-in | High | Medium | Medium | None |
| Open source option | No | NGO is open source | No | Yes |

*Can deploy to multiple regions with additional cost/complexity

---

## Latency Comparison

| Solution | Typical Latency | Notes |
|----------|-----------------|-------|
| Photon Fusion | 20-80ms | Global relay servers |
| UGS Relay | 20-80ms | Unity's global relay network |
| Cloudflare DO | 10-50ms | Edge deployment, closest location |
| Custom VPS (US) | 20-150ms | Single region, varies by user location |
| Custom VPS (Multi-region) | 20-80ms | Complex setup required |

**For MetaDyn's global audience:** Cloudflare DO has best latency, UGS Relay is comparable to Photon.

---

## Recommendation Matrix

### Choose Photon Fusion if:
- You want the most battle-tested multiplayer solution
- You need advanced features (lag compensation, interest management)
- Development speed matters more than cost
- You're OK with vendor lock-in and higher costs
- Budget: $50-1000/month

### Choose Unity Gaming Services if:
- You want managed infrastructure at lower cost than Photon
- Native Unity integration is valuable
- You need voice chat (Vivox 5k PCU free is huge)
- You prefer staying in Unity ecosystem
- Budget: $0-500/month (significantly cheaper than Photon)

### Choose Cloudflare DO if:
- You already use Cloudflare (MetaDyn does)
- You can optimize message rate to ≤5 msg/s
- You want lowest latency (edge deployment)
- You value unified infrastructure (CDN + realtime + AI)
- Budget: $30-650/month (at 5 msg/s)

### Choose Custom VPS if:
- Cost is the absolute primary concern
- You're comfortable with server management
- Single-region latency is acceptable OR you'll set up multi-region
- You want zero vendor lock-in
- You have DevOps capacity
- Budget: $10-200/month

---

## MetaDyn-Specific Recommendation

Given MetaDyn's current setup:
- Already on Cloudflare (CDN, DNS, Vectorize)
- WebGL target (latency-sensitive)
- Global audience expected
- AI memory on Cloudflare Vectorize
- Need voice chat

**Recommended approaches (pick based on priority):**

### Option A: Lowest Cost Managed Solution → UGS
1. **Migrate to UGS** (Netcode + Relay + Vivox)
   - 50 CCU free, then ~$0.16/CCU + bandwidth
   - Vivox voice FREE up to 5,000 PCU
   - Native Unity integration
   - Cost at 500 CCU: ~$117/month (vs Photon $500)
   - Cost at 1000 CCU: ~$242/month (vs Photon $1000)

### Option B: Best Latency + Unified Infra → Cloudflare DO
1. **Migrate to Cloudflare DO** with optimized message rate
   - Best latency (edge deployment)
   - Same network as CDN, Vectorize, D1
   - Requires message optimization (5 msg/s target)
   - Keep WebRTC for voice (already working)
   - Cost at 500 CCU: ~$325/month

### Option C: Lowest Absolute Cost → Custom VPS
1. **Deploy custom WebSocket server**
   - $48-96/month for 500-1000 CCU
   - Requires DevOps maintenance
   - Single region (or complex multi-region)
   - Build everything yourself

### Option D: Fastest Time-to-Market → Stay with Photon
1. **Keep Photon Fusion**
   - Already working
   - Most features built-in
   - Higher cost but zero migration effort
   - Cost at 500 CCU: $500/month

**Our recommendation for MetaDyn:**

| Phase | Recommendation | Why | Cost |
|-------|----------------|-----|------|
| Now (Beta) | Stay with Photon | Already working, focus on features | $50-100 |
| Post-Launch | Evaluate UGS vs Cloudflare | UGS for simplicity, CF for unified infra | $100-300 |
| Scale (500+ CCU) | UGS or Cloudflare | Both ~75% cheaper than Photon at scale | $117-325 |
| Scale (2000+ CCU) | UGS | Best cost/feature ratio | ~$500 |

**Key insight:** UGS is the most balanced option - cheaper than Photon, easier than Cloudflare, more features than custom VPS. The free Vivox tier alone saves significant money if you need voice.

---

## Message Rate Optimization Techniques

To make Cloudflare DO cost-competitive:

| Technique | Savings | Complexity |
|-----------|---------|------------|
| Client-side interpolation | 50% (20→10 msg/s) | Low |
| Delta compression | 20-30% | Medium |
| Adaptive tick rate | 30-50% | Medium |
| Binary protocol | 10-20% (smaller messages) | Medium |
| Dead reckoning | 50%+ | High |
| Area of interest | 50%+ (only sync nearby) | High |

**Realistic target:** 5-7 msg/s average with interpolation + adaptive tick rate.

---

## Cost Projection for MetaDyn Growth

| Phase | Expected CCU | Photon | UGS | Cloudflare (5 msg/s) | Custom VPS |
|-------|--------------|--------|-----|----------------------|------------|
| Beta | 20-50 | $50 | **$0** | $20-32 | $6 |
| Launch | 100-200 | $100-200 | **$13-39** | $65-130 | $12-24 |
| Growth | 500-1000 | $500-1000 | **$117-242** | $325-650 | $48-96 |
| Scale | 2000+ | $2000+ | **$492+** | $1300+ | $192+ |

---

## Summary

| Scale | Cheapest | #2 | #3 | Most Expensive |
|-------|----------|----|----|----------------|
| 50 CCU | **UGS ($0)** | VPS ($6) | CF ($32) | Photon ($50) |
| 100 CCU | VPS ($12) | **UGS ($13)** | CF ($65) | Photon ($100) |
| 500 CCU | VPS ($48) | **UGS ($117)** | CF ($325) | Photon ($500) |
| 1000 CCU | VPS ($96) | **UGS ($242)** | CF ($650) | Photon ($1000) |
| 2000 CCU | VPS ($192) | **UGS ($492)** | CF ($1300) | Photon ($2000) |

---

## Final Verdict

| Priority | Best Choice | Why |
|----------|-------------|-----|
| **Lowest cost (managed)** | UGS | 75% cheaper than Photon, free voice |
| **Lowest cost (absolute)** | Custom VPS | 90% cheaper than Photon, DIY effort |
| **Best latency** | Cloudflare DO | Edge deployment, unified with CDN |
| **Fastest development** | Photon | Already working, most features |
| **Best voice value** | UGS | Vivox 5000 PCU free |
| **Best Unity integration** | UGS | First-party, native support |
| **Lowest vendor lock-in** | Custom VPS | Full control, open source |
| **Best for MetaDyn** | **UGS or Cloudflare** | Both work well with current stack |

---

**Bottom line:**
- **UGS** is the new winner for managed solutions - significantly cheaper than Photon with comparable features
- **Custom VPS** remains cheapest but requires DevOps effort
- **Cloudflare DO** is best if you prioritize unified infrastructure and lowest latency
- **Photon** is now hardest to justify unless you need its specific advanced features

**Savings at 1000 CCU vs Photon ($1000/month):**
- UGS: Save **$758/month** (76% cheaper)
- Cloudflare (5 msg/s): Save **$350/month** (35% cheaper)
- Custom VPS: Save **$904/month** (90% cheaper)
