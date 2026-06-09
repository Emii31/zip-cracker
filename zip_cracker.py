import itertools
import sys
import os
import time
import math

try:
    import pyzipper
except ImportError:
    print("\033[91m[!] CRITICAL ERROR: 'pyzipper' library is not installed.\033[0m")
    print("Run: pip install pyzipper")
    sys.exit(1)

# ANSI Color Codes
C_RED = '\033[91m'
C_GREEN = '\033[92m'
C_CYAN = '\033[96m'
C_YELLOW = '\033[93m'
C_RESET = '\033[0m'
C_BOLD = '\033[1m'

def clear_screen():
    """Wipes the terminal clean for a fresh UI."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    banner = f"""{C_CYAN}{C_BOLD}
___________      .__.__ _________  ____ 
\\_   _____/_____ |__|__|\\_____  \\/_   |
 |    __)_\\     \\|  |  |  _(__  < |   |
 |        \\  Y Y  \\  |  | /       \\|   |
/_______  /__|_|  /__|__|/______  /|___|
        \\/      \\/              \\/      
{C_RESET}{C_CYAN}{C_BOLD}╔══════════════════════════════════════╗
║        EMII31 ZIP CRACKER v1.0       ║
╚══════════════════════════════════════╝{C_RESET}
{C_YELLOW}[>] Author:   Imam Hossain (Emii31){C_RESET}
{C_YELLOW}[>] Telegram: @Hossain31{C_RESET}
{C_YELLOW}[>] GitHub:   github.com/Emii31{C_RESET}
========================================
"""
    print(banner)

def get_case_variations(fragment):
    return list(set(map(''.join, itertools.product(*((c.upper(), c.lower()) for c in fragment)))))

def test_password(zf, target_file, password_guess):
    try:
        with zf.open(target_file, 'r', pwd=password_guess.encode('utf-8')) as f:
            f.read(1)
        return True
    except RuntimeError:
        return False
    except Exception:
        return False

def run_benchmark(zip_path, target_file):
    with pyzipper.AESZipFile(zip_path, 'r', compression=pyzipper.ZIP_DEFLATED, encryption=pyzipper.WZ_AES) as zf:
        start = time.time()
        for _ in range(50):
            test_password(zf, target_file, "benchmark_dummy_pwd")
        end = time.time()
        
    duration = end - start
    if duration <= 0: duration = 0.001
    return 50 / duration

def format_time(seconds):
    if seconds < 60: return f"{seconds:.1f} seconds"
    mins, secs = divmod(seconds, 60)
    if mins < 60: return f"{int(mins)}m {int(secs)}s"
    hours, mins = divmod(mins, 60)
    if hours < 24: return f"{int(hours)}h {int(mins)}m"
    days, hours = divmod(hours, 24)
    return f"{int(days)}d {int(hours)}h {int(mins)}m"

def handle_success(zf, password, attempts, start_time):
    """Handles the post-crack logic: saving the password and prompting for extraction."""
    elapsed = round(time.time() - start_time, 2)
    print(f"\n\n{C_GREEN}{C_BOLD}" + "="*40)
    print("SUCCESS! PASSWORD FOUND.")
    print(f"Total attempts: {attempts:,}")
    print(f"Time elapsed: {format_time(elapsed)}")
    print(f"Password: {password}")
    print("="*40 + f"{C_RESET}")
    
    # Auto-save password to file
    try:
        with open("cracked_password.txt", "w") as f:
            f.write(f"Password: {password}\n")
        print(f"{C_CYAN}[*] Backup saved to 'cracked_password.txt'{C_RESET}")
    except Exception as e:
        print(f"{C_RED}[!] Failed to save password log: {e}{C_RESET}")

    # Prompt for extraction instead of forcing it
    extract_choice = input(f"\n{C_BOLD}Extract files using this script? (y/N)\n{C_RED}WARNING: Python extraction is VERY slow for large files. Use ZArchiver for better speed.{C_RESET}\n> ").strip().lower()
    
    if extract_choice in ['y', 'yes']:
        print(f"\n{C_CYAN}[*] Extracting files...{C_RESET}")
        file_list = zf.infolist()
        for i, file_info in enumerate(file_list, 1):
            print(f"{C_YELLOW}[*] Extracting ({i}/{len(file_list)}): {file_info.filename}{C_RESET}")
            zf.extract(file_info, pwd=password.encode('utf-8'))
        print(f"{C_GREEN}[+] Extraction complete.{C_RESET}")
    else:
        print(f"{C_GREEN}[*] Extraction skipped. Use your native archive app.{C_RESET}")

def run_dictionary_attack(zip_path, wordlist_path):
    print(f"\n{C_CYAN}[*] Initiating Dictionary Attack...{C_RESET}")
    print(f"{C_CYAN}[*] Loading wordlist: {wordlist_path}{C_RESET}")
    
    try:
        with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
            passwords = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"{C_RED}[!] CRITICAL ERROR: Wordlist file not found.{C_RESET}")
        return

    attempts = 0
    start_time = time.time()
    
    with pyzipper.AESZipFile(zip_path, 'r', compression=pyzipper.ZIP_DEFLATED, encryption=pyzipper.WZ_AES) as zf:
        encrypted_files = [f for f in zf.infolist() if f.flag_bits & 0x1]
        if not encrypted_files:
             print(f"{C_RED}[!] Error: No encrypted files found in this zip.{C_RESET}")
             return
        target_file = encrypted_files[0]
        
        for pwd in passwords:
            attempts += 1
            if attempts % 500 == 0:
                print(f"\r{C_YELLOW}[*] Tested {attempts} passwords...{C_RESET}", end='', flush=True)
                
            if test_password(zf, target_file, pwd):
                handle_success(zf, pwd, attempts, start_time)
                return
                
    print(f"\n\n{C_RED}" + "="*40)
    print("FAILURE. Password not found in the wordlist.")
    print("="*40 + f"{C_RESET}")

def run_permutation_attack(zip_path, raw_fragments, deep_mode=False):
    print(f"\n{C_CYAN}[*] Initializing Fragment Permutation Attack...{C_RESET}")
    
    base_fragments = [frag.strip() for frag in raw_fragments.split(',') if frag.strip()]
    final_fragments = []
    
    if deep_mode:
        print(f"{C_YELLOW}[!] Deep Mode Active: Generating case variations...{C_RESET}")
        for frag in base_fragments:
            final_fragments.extend(get_case_variations(frag))
    else:
        final_fragments = base_fragments
        
    final_fragments = list(set(final_fragments))
    n = len(final_fragments)
    r_max = len(base_fragments)
    
    total_combinations = sum(math.perm(n, i) for i in range(1, r_max + 1))
    
    with pyzipper.AESZipFile(zip_path, 'r', compression=pyzipper.ZIP_DEFLATED, encryption=pyzipper.WZ_AES) as zf:
        encrypted_files = [f for f in zf.infolist() if f.flag_bits & 0x1]
        if not encrypted_files:
             print(f"{C_RED}[!] Error: No encrypted files found in this zip.{C_RESET}")
             return
        target_file = encrypted_files[0]
        
        print(f"{C_CYAN}[*] Benchmarking hardware speed...{C_RESET}")
        gps = run_benchmark(zip_path, target_file)
        estimated_seconds = total_combinations / gps
        
        print(f"\n{C_BOLD}--- ATTACK PROFILE ---{C_RESET}")
        print(f"Base Fragments:   {len(base_fragments)}")
        print(f"Total Pool Size:  {n}")
        print(f"Total Variations: {C_RED}{total_combinations:,}{C_RESET}")
        print(f"Hardware Speed:   ~{int(gps)} guesses/sec")
        print(f"Estimated Time:   {C_RED}{format_time(estimated_seconds)}{C_RESET}")
        print(f"----------------------\n")
        
        if deep_mode:
            confirm = input(f"{C_YELLOW}Press ENTER to begin attack, or CTRL+C to abort...{C_RESET}")

    print(f"\n{C_CYAN}[*] Commencing Attack...{C_RESET}\n")

    attempts = 0
    start_time = time.time()
    
    with pyzipper.AESZipFile(zip_path, 'r', compression=pyzipper.ZIP_DEFLATED, encryption=pyzipper.WZ_AES) as zf:
        for length in range(1, r_max + 1):
            for permutation in itertools.permutations(final_fragments, length):
                password_guess = "".join(permutation)
                attempts += 1
                
                if attempts % 100 == 0:
                    print(f"\r{C_YELLOW}[*] {attempts:,}/{total_combinations:,} | Pwd: {password_guess[:12]:<12}{C_RESET}", end='', flush=True)
                
                if test_password(zf, target_file, password_guess):
                    handle_success(zf, password_guess, attempts, start_time)
                    return
                    
    print(f"\n\n{C_RED}" + "="*40)
    print("FAILURE. Password not found in these permutations.")
    print("="*40 + f"{C_RESET}")

def main():
    clear_screen()
    print_banner()
    
    zip_path = input(f"{C_BOLD}Enter exact ZIP file path:\n> {C_RESET}").strip()
    if not os.path.exists(zip_path):
        print(f"{C_RED}[!] Error: The specified ZIP file does not exist.{C_RESET}")
        sys.exit(1)
        
    print(f"\n{C_BOLD}Wordlist Attack?{C_RESET}")
    print("Enter path to wordlist.txt (or press Enter to skip).")
    wordlist_path = input(f"> {C_RESET}").strip()
    
    if wordlist_path:
        if not os.path.exists(wordlist_path):
            print(f"{C_RED}[!] Error: Wordlist file not found.{C_RESET}")
            sys.exit(1)
        run_dictionary_attack(zip_path, wordlist_path)
    else:
        print(f"\n{C_BOLD}Enter known fragments (comma separated).{C_RESET}")
        fragments_input = input(f"> {C_RESET}").strip()
        
        if not fragments_input:
            print(f"{C_RED}[!] Error: You must provide fragments.{C_RESET}")
            sys.exit(1)
            
        print(f"\n{C_BOLD}Enable DEEP MODE (Automatic Case Toggling)?{C_RESET}")
        print(f"{C_RED}WARNING: Multiplies combinations exponentially.{C_RESET}")
        deep_mode_input = input(f"Enable? (y/N) > {C_RESET}").strip().lower()
        
        is_deep_mode = deep_mode_input in ['y', 'yes']
            
        run_permutation_attack(zip_path, fragments_input, deep_mode=is_deep_mode)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{C_RED}[!] Process interrupted by user. Exiting...{C_RESET}")
        sys.exit(0)
