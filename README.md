‎Emii31 Zip Cracker v1.0
‎
‎A highly optimized, brutally efficient AES-256 ZIP password cracker designed specifically for Termux and Linux environments.
‎Standard Python extraction libraries fail against modern ZArchiver AES encryption, and traditional cracking scripts destroy mobile CPUs by constantly writing garbage data to your storage disk. This tool solves both problems by utilizing the pyzipper library and testing cryptographic hashes entirely in your device's RAM.
‎
‎### Core Features
‎ * **AES-256 Support:** Natively handles modern ZIP encryption protocols.
‎ * **In-Memory Decryption:** Tests passwords in RAM without extracting or writing a single byte to your disk, increasing speed exponentially.
‎ * **Fragment Permutation Attack:** Know a few pieces of your password? Input them (e.g., name, 123, @@), and the script will mathematically test every possible arrangement.
‎ * **Deep Mode (Case Toggling):** Automatically maps and tests every uppercase and lowercase variation of your fragments.
‎ * **Dictionary Attack:** Supports standard .txt wordlist parsing for brute-force dictionary attacks.
‎ * **Hardware Micro-Benchmarking:** Runs a silent pre-attack CPU benchmark to calculate your exact Guesses Per Second (GPS) and provides a mathematically precise Estimated Time of Arrival (ETA).
‎ * **Auto-Save Logging:** Instantly writes cracked passwords to cracked_password.txt so you don't lose the key if your terminal crashes.
‎

<img width="1080" height="2400" alt="1000006120" src="https://github.com/user-attachments/assets/09753e56-8040-4f46-97fa-0da6bd57771e" />
<img width="1080" height="2400" alt="1000006119" src="https://github.com/user-attachments/assets/5d9bf1a3-f4f1-478e-9730-edd3952765fb" />


‎### Installation & Setup
‎You must have Python and Git installed. This script requires the pyzipper library to handle AES encryption. The standard zipfile library will NOT work.
‎**For Termux (Android):**
‎
‎pkg update && pkg upgrade -y
‎pkg install python git -y
‎pip install pyzipper
‎termux-setup-storage
‎

‎**For Linux (Debian/Ubuntu):**
‎
‎sudo apt update
‎sudo apt install python3 git -y
‎pip3 install pyzipper
‎
‎
‎### How to Run (Usage)
‎ 1. Clone this repository to your local machine:
‎
‎git clone [https://github.com/Emii31/zip-cracker.git](https://github.com/Emii31/zip-cracker.git)
‎
‎ 2. Navigate into the folder:
‎cd zip-cracker
‎
‎
‎ 3. Execute the script:
‎
‎python zip_cracker.py
‎


‎Follow the on-screen interactive prompts. You will be asked to provide the absolute path to your target ZIP file, choose your attack vector (Wordlist or Fragments), and confirm the attack after reviewing your hardware benchmark.
‎*Disclaimer: Built by Emii31 (@Hossain31). This tool is designed for data recovery and educational purposes only. You are solely responsible for how you use this script.*
