# 🛡️ Sentinel - Linux Threat Monitoring System (EDR)

![Platform](https://img.shields.io/badge/Platform-Linux-linux?style=flat&logo=linux)
![Agent](https://img.shields.io/badge/Agent-Python-blue?style=flat&logo=python)
![Backend](https://img.shields.io/badge/Backend-Go-cyan?style=flat&logo=go)
![License](https://img.shields.io/badge/license-MIT-green)

**Sentinel**, Linux tabanlı sistemler için geliştirilmiş, gerçek zamanlı bir süreç (process) izleme ve tehdit algılama sistemidir (Endpoint Detection and Response - EDR).

İşletim sistemi çekirdeğine (Kernel) yakın çalışarak process aktivitelerini izler, `/proc` dosya sistemini analiz eder ve olası zararlı aktiviteleri (Malware, Crypto Miner, Reverse Shell) sezgisel yöntemlerle (heuristics) tespit eder.

## 🚀 Proje Mimarisi

Sentinel, dağıtık bir mimariye sahiptir ve performans odaklı tasarlanmıştır:

1.  **The Agent (Python):** Hedef Linux makinede `systemd` servisi olarak çalışır. CPU/RAM üzerinde minimum yük oluşturarak `/proc` dizinini tarar ve kernel seviyesindeki process çağrılarını analiz eder.
2.  **Dashboard:** Tehditlerin görselleştirildiği yönetim paneli.

---

## 🔥 Temel Özellikler

- **Gerçek Zamanlı Process İzleme:** Sistemde başlayan her yeni işlemi milisaniyeler içinde yakalar.
- **Anomali Tespiti (Heuristics):**
  - 🚨 `/tmp` veya `/dev/shm` dizinlerinden çalıştırılan binary dosyalarını (Genel Malware davranışı) tespit eder.
  - ⚠️ `root` yetkisiyle çalışan şüpheli script dillerini (Python, Bash, Sh) izler.
- **Kernel Thread Filtreleme:** Linux çekirdek işlemlerini (kworker, migration, rcu) kullanıcı işlemlerinden ayırarak "gürültüyü" (
