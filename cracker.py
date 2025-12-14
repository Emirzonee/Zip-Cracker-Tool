import zipfile
import time
import sys
import os

def attempt_crack(zip_file, password):
    """
    Deneme fonksiyonu.
    Basarili olursa True doner.
    """
    try:
        zip_file.extractall(pwd=password.encode('utf-8'))
        return True
    except (RuntimeError, zipfile.BadZipFile):
        return False
    except Exception:
        # Kodlama hatasi vs olursa pas gec
        return False

def main():
    # Basit bir baslik
    print("Zip Password Recovery Tool v1.0")
    print("-" * 30)
    
    # Kullanici girisleri 
    zip_filename = input("Target zip file path: ").strip()
    
    if not os.path.exists(zip_filename):
        print(f"Error: File '{zip_filename}' not found.")
        sys.exit(1)

    wordlist_filename = input("Password list path: ").strip()

    if not os.path.exists(wordlist_filename):
        print(f"Error: File '{wordlist_filename}' not found.")
        sys.exit(1)

    try:
        zip_obj = zipfile.ZipFile(zip_filename)
    except zipfile.BadZipFile:
        print("Error: Invalid or corrupted zip file.")
        sys.exit(1)

    print(f"\nScanning started on {zip_filename}...")
    start_time = time.time()
    count = 0

    try:
        with open(wordlist_filename, 'r', errors='ignore') as f:
            for line in f:
                password = line.strip()
                count += 1

                # Her 1000 denemede bir bilgi ver
                if count % 1000 == 0:
                    print(f"Checked {count} passwords...", end='\r')

                if attempt_crack(zip_obj, password):
                    elapsed = time.time() - start_time
                    print(f"\nPassword found: {password}")
                    print(f"Elapsed time: {elapsed:.2f} seconds")
                    return

            print(f"\nPassword not found in wordlist. Total attempts: {count}")

    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")

if __name__ == "__main__":
    main()