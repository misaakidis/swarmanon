# Architecture

The intended prototype offers our Swarm gateway as a Nym-addressed service. The Nym transport and end-to-end request are still being verified.

```mermaid
flowchart LR
    U[User HTTP client] -->|HTTP on loopback| C[Nym RPC client\nraw TCP listener]
    C <-->|Nym mixnet mainnet\nanonymous replies| S[Nym RPC server\npersistent service address]
    S -->|pinned TCP upstream| F[Read-only HTTP filter\n127.0.0.1:18080]
    F -->|HTTP on loopback| G[Our Swarm Gateway\n127.0.0.1:13000]
    G -->|private Docker network| B[Our Bee ultra-light node]
    B <-->|Swarm peer protocol| P[Swarm mainnet peers]
```

The gateway sees a request from the local filter, not the user's IP. The Nym entry gateway sees the user's network address; application data can still identify a user. This diagram does not claim end-to-end anonymity has been demonstrated.

```mermaid
sequenceDiagram
    participant User as User HTTP client
    participant Client as Local Nym client
    participant Mix as Nym mixnet
    participant Service as Gateway Nym service
    participant Filter as Read-only filter
    participant Gateway as Swarm Gateway
    participant Bee as Bee ultra-light
    participant Swarm as Swarm peers
    User->>Client: GET /bzz/reference/
    Client->>Mix: Send request to service address
    Mix->>Service: Deliver request
    Service->>Filter: Forward to pinned local upstream
    Filter->>Gateway: Forward permitted GET
    Gateway->>Bee: Retrieve reference
    Bee->>Swarm: Request content
    Swarm-->>Bee: Content
    Bee-->>Gateway: HTTP response
    Gateway-->>Filter: HTTP response
    Filter-->>Service: Bounded response
    Service->>Mix: Send response using reply blocks
    Mix-->>Client: Deliver response
    Client-->>User: HTTP response
```

The current filter accepts 64-character hexadecimal references and caps responses at 2 MiB. Bee ultra-light downloads depend on peers' free-tier limits. The service Nym identity must persist, and its address must be distributed to users separately.
