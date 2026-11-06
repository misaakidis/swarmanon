# Swarm over Nym prototype

Our Swarm Gateway and a Bee ultra-light node run on Swarm mainnet. `gateway.py` binds a read-only filter to loopback port 18080 and forwards `/bzz/<64-hex-reference>/...` to our gateway on loopback port 13000. Bee is not exposed to the host. Ultra-light downloads are subject to peers' free-tier limits.

The intended Nym service uses [nym-rpc](https://github.com/nymtech/nym-rpc) in raw TCP mode, with the server pinned to `127.0.0.1:18080`. Pinning is required to prevent an open relay. Its administrative HTTP API must remain loopback-only. Publish the server's Nym address to users; the client exposes a local HTTP port. Both sides use Nym mainnet by default.

Build the gateway image from `ethersphere/swarm-gateway` commit `dffb61e65b6450066947d7706b5fa9a8060dbbb8` as `swarmanon-gateway:dffb61e`, then run `docker compose up -d` and `python3 gateway.py`. The Nym transport and end-to-end retrieval have not yet been verified. The fixed Bee password is for disposable prototype data only. Neither traffic anonymity nor content integrity has been independently verified.

Once nym-rpc has been built, start the service with:

```sh
nym-rpc-server --config-dir ./nym-state --pin-upstream 127.0.0.1:18080
```

Copy its Nym address to the client and start the tunnel:

```sh
nym-rpc-client --raw --listen-port 18081 --upstream 127.0.0.1:18080 -x '<NYM_ADDRESS>'
curl http://127.0.0.1:18081/bzz/<REFERENCE>/
```

These commands are planned and have not been tested against the network. Store `nym-state` securely: it contains the service identity. The filter limits responses to 2 MiB and intentionally accepts only simple reference paths; unsupported methods return 501.

See [ARCHITECTURE.md](ARCHITECTURE.md) for the intended component and request-flow diagrams.
