import re


def get_ip(prompt):
    while True:
        ip = input(prompt).strip()
        parts = ip.split('.')
        if len(parts) == 4 and all(p.isdigit() and 0 <= int(p) <= 255 for p in parts):
            return ip
        print("  Geçersiz IP adresi, tekrar deneyin.")


def get_mac(prompt):
    while True:
        mac = input(prompt).strip()
        if mac == "":
            return None
        parts = mac.split(':')
        if len(parts) == 6 and all(len(p) == 2 and all(c in '0123456789abcdefABCDEF' for c in p) for p in parts):
            return mac.lower()
        print("  Geçersiz MAC adresi (örnek: 0c:aa:d4:60:00:01), tekrar deneyin.")


def ip_arti_bir(ip):
    parts = ip.split('.')
    parts[-1] = str(int(parts[-1]) + 1)
    return '.'.join(parts)


def guncelle_simple_ipv4(ip, gw, path="/v3.08/emu/simple_ipv4.py"):
    with open(path, "r") as f:
        content = f.read()

    content = re.sub(
        r"ipv4\s*=\s*Ipv4\('[^']*'\)",
        f"ipv4 = Ipv4('{ip}')",
        content
    )
    content = re.sub(
        r"dg\s*=\s*Ipv4\('[^']*'\)",
        f"dg = Ipv4('{gw}')",
        content
    )

    with open(path, "w") as f:
        f.write(content)
    print(f"simple_ipv4.py guncellendi ipv4='{ip}', dg='{gw}'")


def guncelle_simple_icmp(ip, gw, path="/v3.08/emu/simple_icmp.py"):
    with open(path, "r") as f:
        content = f.read()

    content = re.sub(
        r"ipv4\s*=\s*Ipv4\('[^']*'\)",
        f"ipv4 = Ipv4('{ip}')",
        content
    )
    content = re.sub(
        r"dg\s*=\s*Ipv4\('[^']*'\)",
        f"dg = Ipv4('{gw}')",
        content
    )

    with open(path, "w") as f:
        f.write(content)
    print(f"simple_icmp.py guncellendi ipv4='{ip}', dg='{gw}'")


def guncelle_simple_icmp1(eth0_ip, eth0_gw, eth1_ip, eth1_gw, path="/v3.08/emu/simple_icmp1.py"):
    with open(path, "r") as f:
        content = f.read()

    # if i==0 blogu → eth0
    content = re.sub(
        r"(if i==0:.*?ipv4\s*=\s*Ipv4\(')([^']*)('\))",
        rf"\g<1>{eth0_ip}\g<3>",
        content,
        flags=re.DOTALL
    )
    content = re.sub(
        r"(if i==0:.*?dg\s*=\s*Ipv4\(')([^']*)('\))",
        rf"\g<1>{eth0_gw}\g<3>",
        content,
        flags=re.DOTALL
    )

    # else blogu → eth1
    content = re.sub(
        r"(else:.*?ipv4\s*=\s*Ipv4\(')([^']*)('\))",
        rf"\g<1>{eth1_ip}\g<3>",
        content,
        flags=re.DOTALL
    )
    content = re.sub(
        r"(else:.*?dg\s*=\s*Ipv4\(')([^']*)('\))",
        rf"\g<1>{eth1_gw}\g<3>",
        content,
        flags=re.DOTALL
    )

    # transe addr → eth0_gw:9001
    content = re.sub(
        r"('transe'\s*:\s*\{'addr'\s*:\s*')[^']*(')",
        rf"\g<1>{eth0_gw}:9001\g<2>",
        content
    )

    with open(path, "w") as f:
        f.write(content)
    print(f"simple_icmp1.py guncellendi eth0: ipv4='{eth0_ip}', dg='{eth0_gw}' | eth1: ipv4='{eth1_ip}', dg='{eth1_gw}' | transe addr='{eth0_gw}:9001'")


def guncelle_simple_icmp_local(ip, gw, path="/v3.08/emu/simple_icmp_local.py"):
    with open(path, "r") as f:
        content = f.read()

    content = re.sub(
        r"ipv4\s*=\s*Ipv4\('[^']*'\)",
        f"ipv4 = Ipv4('{ip}')",
        content
    )
    content = re.sub(
        r"dg\s*=\s*Ipv4\('[^']*'\)",
        f"dg = Ipv4('{gw}')",
        content
    )

    # transe addr → eth0_gw:9001
    content = re.sub(
        r"('transe'\s*:\s*\{'addr'\s*:\s*')[^']*(')",
        rf"\g<1>{gw}:9001\g<2>",
        content
    )

    with open(path, "w") as f:
        f.write(content)
    print(f"simple_icmp_local.py guncellendi ipv4='{ip}', dg='{gw}', transe addr='{gw}:9001'")


def guncelle_simple_igmp(ip, gw, path="/v3.08/emu/simple_igmp.py"):
    with open(path, "r") as f:
        content = f.read()

    content = re.sub(
        r"ipv4\s*=\s*Ipv4\('[^']*'\)",
        f"ipv4 = Ipv4('{ip}')",
        content
    )
    content = re.sub(
        r"dg\s*=\s*Ipv4\('[^']*'\)",
        f"dg = Ipv4('{gw}')",
        content
    )

    with open(path, "w") as f:
        f.write(content)
    print(f"simple_igmp.py guncellendi ipv4='{ip}', dg='{gw}'")


def guncelle_dhcpsrv_relay(ip, gw, path="/v3.08/emu/dhcpsrv_relay.py"):
    with open(path, "r") as f:
        content = f.read()

    # srv_ip default → eth0_ip + 1
    content = re.sub(
        r"(parser\.add_argument\('--srv_ip'.*?default\s*=\s*\")[^\"]*?(\")",
        rf"\g<1>{ip}\g<2>",
        content,
        flags=re.DOTALL
    )

    # srv_dg_ip default → eth0_gw
    content = re.sub(
        r"(parser\.add_argument\('--srv_dg_ip'.*?default\s*=\s*\")[^\"]*?(\")",
        rf"\g<1>{gw}\g<2>",
        content,
        flags=re.DOTALL
    )

    # exclude satirini ekle → "prefix" satırının hemen altina
    # once eski exclude varsa temizle, sonra ekle
    content = re.sub(
        r'(\s*"prefix"\s*:\s*\d+,?)(\s*"exclude"\s*:\s*\[[^\]]*\])?',
        r'\1\n                    "exclude": ["1.1.2.1","1.1.2.255"]',
        content
    )

    with open(path, "w") as f:
        f.write(content)
    print(f"dhcpsrv_relay.py guncellendi srv_ip='{ip}', srv_dg_ip='{gw}'")


print("=== TRex Konfigürasyon Olusturucu ===\n")

print("--- eth0 Ayarlari ---")
eth0_ip  = get_ip("eth0 IP adresi         : ")
eth0_gw  = get_ip("eth0 Default Gateway   : ")
eth0_mac = get_mac("eth0 Dest MAC adresi (bos gecmek icin Enter): ")

print("\n--- eth1 Ayarlari ---")
eth1_ip  = get_ip("eth1 IP adresi         : ")
eth1_gw  = get_ip("eth1 Default Gateway   : ")
eth1_mac = get_mac("eth1 Dest MAC adresi (bos gecmek icin Enter): ")

# eth0_ip + 1  →  py dosyalari icin
eth0_ip_py = ip_arti_bir(eth0_ip)


def port_entry(ip, gw, mac):
    lines = []
    lines.append(f"                 - ip         : {ip}")
    lines.append(f"                   default_gw : {gw}")
    if mac:
        lines.append(f"                   dest_mac   : \"{mac}\"")
    return "\n".join(lines)


yaml_content = f"""- port_limit    : 2
  version       : 2
  low_end       : true
  interfaces    : ["eth0", "eth1"]
  port_info     :  # set eh mac addr
{port_entry(eth0_ip, eth0_gw, eth0_mac)}
{port_entry(eth1_ip, eth1_gw, eth1_mac)}
"""

# /etc/trex_cfg.yaml → gercek eth0_ip
output_path = "/etc/trex_cfg.yaml"
with open(output_path, "w") as f:
    f.write(yaml_content)
print(f"\nKonfigurasyon '{output_path}' dosyasina kaydedildi.")

# py dosyalari → eth0_ip + 1
guncelle_simple_ipv4(eth0_ip_py, eth0_gw)
guncelle_simple_icmp(eth0_ip_py, eth0_gw)
guncelle_simple_icmp1(eth0_ip_py, eth0_gw, eth1_ip, eth1_gw)
guncelle_simple_icmp_local(eth0_ip_py, eth0_gw)
guncelle_simple_igmp(eth0_ip_py, eth0_gw)
guncelle_dhcpsrv_relay(eth0_ip_py, eth0_gw)

print("\n--- Olusturulan YAML ---")
print(yaml_content)