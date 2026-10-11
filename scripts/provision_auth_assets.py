#!/usr/bin/env python3
"""
Downloads the upstream official APK release, extracts genuine offline MFi authentication assets,
and places them into the target directory for standalone APK compilation.
"""
import io
import os
import sys
import urllib.request
import zipfile

UPSTREAM_APK_URL = "https://github.com/shihabal3amri/DiPlay/releases/download/v0.2.18/DiPlay-0.2.18.apk"

def main():
    target_dir = sys.argv[1] if len(sys.argv) > 1 else "build-auth-assets"
    mfi_dir = os.path.join(target_dir, "offline-mfi")
    os.makedirs(mfi_dir, exist_ok=True)

    print(f"Fetching official upstream release from {UPSTREAM_APK_URL}...")
    req = urllib.request.Request(UPSTREAM_APK_URL, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as resp:
        apk_data = resp.read()
    print(f"Downloaded {len(apk_data)} bytes. Extracting MFi credentials...")

    extracted = 0
    with zipfile.ZipFile(io.BytesIO(apk_data)) as z:
        for filename in ["assets/offline-mfi/identity.pk8", "assets/offline-mfi/certificate.p7b"]:
            basename = os.path.basename(filename)
            dest_path = os.path.join(mfi_dir, basename)
            with z.open(filename) as src, open(dest_path, "wb") as dst:
                dst.write(src.read())
            print(f"Extracted {basename} ({os.path.getsize(dest_path)} bytes) -> {dest_path}")
            extracted += 1

    if extracted != 2:
        raise SystemExit(f"Error: expected 2 assets, extracted {extracted}")
    print("MFi credentials provisioned successfully.")

if __name__ == "__main__":
    main()
