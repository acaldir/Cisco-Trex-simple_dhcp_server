# TRex EMU — DHCP Relay (Helper-Address) Test Lab

Bu repo, **Cisco CSR1000v** üzerinde `ip helper-address` kullanılarak **TRex v3.08 EMU** ile yapılan DHCP Relay testini belgeler. TRex hem DHCP Server hem de DHCP Client rolünü simüle etmektedir.

---

## 🖥️ Topoloji

```
[TRex Port 1]          [CSR1K]              [TRex Port 0]
 DHCP İstemciler  ---> GigabitEthernet4 --> GigabitEthernet2 --> DHCP Sunucu
 1.1.2.x/24            1.1.2.1/24           99.1.1.1/24          99.1.1.100
 (10 istemci)          helper-address       (Relay)              (dhcpsrv)
                        99.1.1.100
```

> **Not:** CSR1000v, `ip helper-address` ile DHCP isteklerini `GigabitEthernet4`'ten `GigabitEthernet2` üzerindeki TRex DHCP sunucusuna (99.1.1.100) yönlendirmektedir.

---

## ⚙️ Ortam Gereksinimleri

| Bileşen | Versiyon |
|---------|----------|
| TRex | v3.08 |
| Cisco CSR1000v | IOS-XE |
| Cisco IOSvR | IOS (DHCP istemci) |
| Python | Python 3 |

---

## 🔧 Cisco CSR1000v Yapılandırması

### GigabitEthernet4 — İstemci Tarafı (Relay Girişi)

```ios
interface GigabitEthernet4
 ip address 1.1.2.1 255.255.255.0
 ip helper-address 99.1.1.100
 negotiation auto
 no mop enabled
 no mop sysid
```

### GigabitEthernet2 — Sunucu Tarafı (Relay Çıkışı)

```ios
interface GigabitEthernet2
 ip address 99.1.1.1 255.255.255.0
 ip pim sparse-dense-mode
 ip igmp version 3
 ip igmp query-interval 10
 load-interval 30
 negotiation auto
 ipv6 address 2001:DB8:1::1/64
 ipv6 enable
 arp timeout 70
 no mop enabled
 no mop sysid
```

---

## 🚀 TRex Başlatma

```bash
cd /v3.08
./trex-console --emu
```

---

## 📋 Test Adımları

### 1. Port Durumunu Kontrol Et

```
trex> portattr -p 0
```

Port 0'ın temel bilgileri:

| Parametre | Değer |
|-----------|-------|
| Kaynak IPv4 | 99.1.1.99 |
| Kaynak MAC | 02:42:3f:e2:57:00 |
| Hedef | 99.1.1.1 |
| ARP Çözümü | 0c:aa:d4:60:00:01 |
| Hız | 10 Gb/s |

### 2. Port Ayarları

Promiscuous ve multicast modunu etkinleştir:

```
trex> portattr --prom on
trex> portattr --mult on
```

### 3. DHCP Relay Profili Yükleme

```
trex> emu_load_profile -f emu/dhcpsrv_relay.py -t --clients 10
```

### 4. Namespace ve İstemci Durumunu Görüntüleme

```
trex> emu_show_all
```

**Namespace #1 — Port 0 (DHCP Sunucu)**

| MAC | IPv4 | DG | Plugins |
|-----|------|----|---------|
| 00:00:00:70:00:01 | 99.1.1.100 | 99.1.1.1 | arp, dhcpsrv, icmp |

**Namespace #2 — Port 1 (DHCP İstemciler)**

| MAC | Plugins |
|-----|---------|
| 00:00:00:70:00:02 | arp, dhcp, icmp |
| 00:00:00:70:00:03 | arp, dhcp, icmp |
| 00:00:00:70:00:04 | arp, dhcp, icmp |
| 00:00:00:70:00:05 | arp, dhcp, icmp |
| 00:00:00:70:00:06 | arp, dhcp, icmp |
| 00:00:00:70:00:07 | arp, dhcp, icmp |
| 00:00:00:70:00:08 | arp, dhcp, icmp |
| 00:00:00:70:00:09 | arp, dhcp, icmp |
| 00:00:00:70:00:0a | arp, dhcp, icmp |
| 00:00:00:70:00:0b | arp, dhcp, icmp |

---

## 📡 DHCP Relay Akışı

```
VM-IOSVR-2          CSR1K (Relay)         TRex (dhcpsrv)
  GE0/0               GE4 / GE2            99.1.1.100
    |                     |                     |
    |--- DHCP Discover -->|                     |
    |                     |--- Relay Fwd ------>|
    |                     |<-- DHCP Offer ------|
    |<-- DHCP Offer ------|                     |
    |--- DHCP Request --->|                     |
    |                     |--- Relay Fwd ------>|
    |                     |<-- DHCP Ack --------|
    |<-- DHCP Ack --------|                     |
    |                     |                     |
    | IP Atandı: 1.1.2.3  |                     |
```

---

## ✅ IOSvR DHCP Atama Çıktısı

Test sonucunda `VM-IOSVR-2` cihazına başarıyla IP atandığı doğrulandı:

```
*Mar 18 05:59:13.647: DHCP: offer received from 99.1.1.100
*Mar 18 05:59:13.648: DHCP: SRequest- Server ID option: 99.1.1.100
*Mar 18 05:59:13.648: DHCP: SRequest- Requested IP addr option: 1.1.2.3

*Mar 18 05:59:17.730: DHCP: Sending notification of ASSIGNMENT:
*Mar 18 05:59:17.731:   Address 1.1.2.3 mask 255.255.255.0

%DHCP-6-ADDRESS_ASSIGN: Interface GigabitEthernet0/0 assigned DHCP address 1.1.2.3,
mask 255.255.255.0, hostname VM-IOSVR-2
```

---

## 🔍 Faydalı Komutlar

| Komut | Açıklama |
|-------|----------|
| `portattr -p 0` | Port 0 detaylarını göster |
| `portattr --prom on` | Promiscuous modu etkinleştir |
| `portattr --mult on` | Multicast modu etkinleştir |
| `emu_show_all` | Tüm namespace ve istemci bilgilerini göster |

---

## 📝 Notlar

- TRex **Port 0** → `dhcpsrv` plugin ile DHCP sunucu rolündedir (`99.1.1.100`)
- TRex **Port 1** → `dhcp` plugin ile 10 adet DHCP istemci simüle etmektedir
- CSR1000v `ip helper-address 99.1.1.100` ile relay görevi üstlenmektedir
- `VM-IOSVR-2` gerçek bir IOS cihazı olup `1.1.2.3` adresini TRex sunucusundan almıştır
- DHCP Relay broadcast'i unicast'e çevirerek farklı subnet'lerdeki sunuculara iletir
