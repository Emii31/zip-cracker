# Emii31 Zip Cracker v1.0

A highly optimized, brutally efficient AES-256 ZIP password cracker designed specifically for Termux and Linux environments. 

Standard Python extraction libraries fail against modern ZArchiver AES encryption, and traditional cracking scripts destroy mobile CPUs by constantly writing garbage data to your storage disk. This tool solves both problems by utilizing the `pyzipper` library and testing cryptographic hashes entirely in your device's RAM.

### Core Features
* **AES-256 Support:** Natively handles modern ZIP encryption protocols.
* **In-Memory Decryption:** Tests passwords in RAM without extracting or writing a single byte to your disk, increasing speed exponentially.
* **Fragment Permutation Attack:** Know a few pieces of your password? Input them (e.g., `name, 123, @@`), and the script will mathematically test every possible arrangement.
* **Deep Mode (Case Toggling):** Automatically maps and tests every uppercase and lowercase variation of your fragments. 
* **Dictionary Attack:** Supports standard `.txt` wordlist parsing for brute-force dictionary attacks.
* **Hardware Micro-Benchmarking:** Runs a silent pre-attack CPU benchmark to calculate your exact Guesses Per Second (GPS) and provides a mathematically precise Estimated Time of Arrival (ETA).
* **Auto-Save Logging:** Instantly writes cracked passwords to `cracked_password.txt` so you don't lose the key if your terminal crashes.


<img width="1080" height="2400" alt="1000006120" src="https://github.com/user-attachments/assets/5c8c7712-cabe-487a-86f3-1437cd869b7d" />
<img width="1080" height="2400" alt="1000006119" src="https://github.com/user-attachments/assets/0658eeb8-92fa-4a3e-94d1-378bd38955e9" />
<img width="1080" height="2400" alt="1000006116" src="https://github.com/user-attachments/assets/bf6ed1c1-37b1-4c66-8480-62b67d443e92" />
<img width="1080" height="2400" alt="1000006115" src="https://github.com/user-attachments/assets/f15421cb-5439-46eb-808e-fca5ef708d7a" />


---

### Installation & Setup

You must have Python and Git installed. This script requires the `pyzipper` library to handle AES encryption. The standard `zipfile` library will NOT work.

**For Termux (Android):**

pkg update && pkg upgrade -y

pkg install python git -y

pip install pyzipper

termux-setup-storage

---
**For Linux (Debian/Ubuntu):**

sudo apt update

sudo apt install python3 git -y

pip3 install pyzipper

**How to Run (Usage)**
Clone this repository to your local machine:
git clone [https://github.com/Emii31/zip-cracker.git](https://github.com/Emii31/zip-cracker.git)

cd zip-cracker

python zip_cracker.py


Follow the on-screen interactive prompts. You will be asked to provide the absolute path to your target ZIP file, choose your attack vector (Wordlist or Fragments), and confirm the attack after reviewing your hardware benchmark.
Disclaimer: Built by Emii31 (@Hossain31). This tool is designed for data recovery and educational purposes only. You are solely responsible for how you use this script.
