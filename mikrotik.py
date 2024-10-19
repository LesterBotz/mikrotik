import routeros_api

# Fungsi untuk menghubungkan ke MikroTik
def connect_to_mikrotik(host, username, password):
    try:
        api = routeros_api.RouterOsApiPool(host, username=username, password=password, plaintext_login=True)
        connection = api.get_api()
        print("Berhasil terhubung ke MikroTik.")
        return connection
    except Exception as e:
        print(f"Gagal terhubung ke MikroTik: {e}")
        return None

# Fungsi untuk menambahkan IP Address
def add_ip_address(connection, interface, ip_address, network):
    try:
        ip_api = connection.get_resource('/ip/address')
        ip_api.add(interface=interface, address=ip_address, network=network)
        print(f"IP Address {ip_address} berhasil ditambahkan ke {interface}.")
    except Exception as e:
        print(f"Gagal menambahkan IP Address: {e}")

# Fungsi untuk menambahkan NAT rule
def add_nat_rule(connection, src_address, out_interface):
    try:
        nat_api = connection.get_resource('/ip/firewall/nat')
        nat_api.add(chain="srcnat", action="masquerade", src_address=src_address, out_interface=out_interface)
        print(f"NAT rule untuk {src_address} berhasil ditambahkan.")
    except Exception as e:
        print(f"Gagal menambahkan NAT rule: {e}")

# Fungsi untuk menambahkan DNS Server
def add_dns_server(connection, dns_server):
    try:
        dns_api = connection.get_resource('/ip/dns/set')
        dns_api.set(servers=dns_server)
        print(f"DNS server {dns_server} berhasil ditambahkan.")
    except Exception as e:
        print(f"Gagal menambahkan DNS Server: {e}")

# Fungsi utama untuk eksekusi pengaturan
def setup_mikrotik(host, username, password, interface, ip_address, network, src_address, out_interface, dns_server):
    connection = connect_to_mikrotik(host, username, password)
    
    if connection:
        add_ip_address(connection, interface, ip_address, network)
        add_nat_rule(connection, src_address, out_interface)
        add_dns_server(connection, dns_server)

        # Tutup koneksi
        connection.disconnect()
        print("Koneksi ke MikroTik ditutup.")
    else:
        print("Konfigurasi gagal karena tidak dapat terhubung ke MikroTik.")

# Eksekusi script
if __name__ == "__main__":
    host = input("Masukkan IP address MikroTik: ")
    username = input("Masukkan username: ")
    password = input("Masukkan password: ")

    interface = input("Masukkan interface (contoh: ether1): ")
    ip_address = input("Masukkan IP address (contoh: 192.168.88.1/24): ")
    network = input("Masukkan network (contoh: 192.168.88.0): ")

    src_address = input("Masukkan source address (contoh: 192.168.88.0/24): ")
    out_interface = input("Masukkan out interface (contoh: ether1): ")

    dns_server = input("Masukkan DNS Server (contoh: 8.8.8.8): ")

    setup_mikrotik(host, username, password, interface, ip_address, network, src_address, out_interface, dns_server)
