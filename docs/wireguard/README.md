1. Architecture Overview

Current mode: Host-based WireGuard

WireGuard runs directly on the host OS

Interface name: wg0

VPN subnet: 10.8.0.0/24

ELP acts as a WireGuard server

This approach is:

Simple to debug

Representative of real industrial gateways

Suitable for production

Future-proof (can migrate to container-based WireGuard later)

2. Important Paths and Files
/etc/wireguard/
├── wg0.conf                # Active WireGuard configuration
├── keys/
│   ├── server_private.key  # Server private key (root only)
│   └── server_public.key   # Server public key


3. Security rules:

wg0.conf must never be committed to git

Private keys must be root-only (permissions 600)

The repository should only contain .example files

4. Operational Commands
Check WireGuard status
sudo wg

Show details for interface wg0
sudo wg show wg0

Show interface IP and state
ip a show wg0

Verify traffic and handshake
sudo wg show wg0


Look for:

latest handshake

transfer counters

5. Service Management
Start WireGuard
sudo systemctl start wg-quick@wg0

Stop WireGuard
sudo systemctl stop wg-quick@wg0

Restart WireGuard
sudo systemctl restart wg-quick@wg0

Enable at boot
sudo systemctl enable wg-quick@wg0

6. Adding a New WireGuard Peer
6.1 Generate client keys
wg genkey | tee client_private.key | wg pubkey > client_public.key

6.2 Register the peer on the server

Edit the server configuration:

sudo nano /etc/wireguard/wg0.conf


Add:

[Peer]
PublicKey = <CLIENT_PUBLIC_KEY>
AllowedIPs = 10.8.0.2/32

6.3 Apply changes without restarting the tunnel
sudo wg syncconf wg0 /etc/wireguard/wg0.conf


This avoids disconnecting existing peers.

7. Client Configuration Example
[Interface]
PrivateKey = <CLIENT_PRIVATE_KEY>
Address = 10.8.0.2/24
DNS = 1.1.1.1

[Peer]
PublicKey = <SERVER_PUBLIC_KEY>
Endpoint = <SERVER_PUBLIC_IP>:51820
AllowedIPs = 10.8.0.1/32
PersistentKeepalive = 25



recuerdame agregar rutas de servicios que levantan el docker