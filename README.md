# swarmanon

swarmanon serves Swarm content through a Nym-addressed service. A Bee ultra-light node retrieves content on Swarm mainnet, Swarm Gateway resolves ENS names using an Ethereum RPC, and a read-only filter limits requests before they reach the gateway. Nym RPC transports requests between a local client and the service using the Nym mixnet.

## Start the service

Install Docker and Docker Compose, then run:

```sh
docker compose up -d --build
```

Set `ENS_RPC_URL` in the environment to use a different Ethereum mainnet RPC. The default Bee password is for disposable prototype data only. Bee and the Nym service state are stored in Docker volumes; preserve the Nym volume to retain the service identity. The filter and Bee API are private to the Compose network.

Get the Nym service address from the logs:

```sh
docker compose logs nym-service | grep 'Nym address:'
```

## Connect from a laptop

Set `NYM_SERVICE_ADDRESS` to the service address and start the client profile:

```sh
export NYM_SERVICE_ADDRESS='<service Nym address>'
docker compose --profile client up -d nym-client
```

Then open `http://127.0.0.1:18081/bzz/<name.eth>/` or `/bzz/<reference>/` in the laptop browser. The client listens only on the laptop loopback interface. For example, `apps.ontheswarm.eth` is an existing public Swarm page that can be used for testing. The service itself is addressed by its Nym address; it does not require an ENS name.

The filter permits GET requests for 64-character hexadecimal references and ASCII `.eth` names, rejects query strings, and caps responses at 2 MiB. Bee ultra-light downloads are subject to peers' free-tier limits. The prototype's fixed upstream prevents the Nym service from acting as a general-purpose relay.

See [ARCHITECTURE.md](ARCHITECTURE.md) for component and request-flow diagrams.
