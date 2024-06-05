# Show ipa adhoc devices udid
# 使用方式： python ipa-ad-hoc-devices.py xxx.ipa

import os
import plistlib
import tempfile
import zipfile


def get_provision_path(temp_dir):
    for root, dirs, files in os.walk(temp_dir):
        for dir in dirs:
            if dir.endswith(".app"):
                app_path = os.path.join(root, dir)
                break

    provision_path = os.path.join(app_path, "embedded.mobileprovision")
    return provision_path


def extract_udids_from_ipa(ipa_path):
    print("The ipa path is:", ipa_path)
    # 创建临时目录
    with tempfile.TemporaryDirectory() as temp_dir:
        # 解压 IPA 文件
        with zipfile.ZipFile(ipa_path, "r") as ipa_zip:
            ipa_zip.extractall(temp_dir)

        # 找到 embedded.mobileprovision 文件
        provision_path = get_provision_path(temp_dir)

        # 解析 embedded.mobileprovision 文件
        with open(provision_path, "rb") as f:
            provision_data = f.read()

        plist_start = provision_data.find(b"<?xml")
        plist_end = provision_data.find(b"</plist>") + len(b"</plist>")
        plist_data = provision_data[plist_start:plist_end]

        plist = plistlib.loads(plist_data)
        udids = plist.get("ProvisionedDevices", [])

        return udids


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Extract UDIDs from an adhoc IPA file."
    )
    parser.add_argument("ipa_path", help="Path to the IPA file")

    args = parser.parse_args()
    udids = extract_udids_from_ipa(args.ipa_path)

    if udids:
        print("Extracted UDIDs:")
        for udid in udids:
            print(udid)
    else:
        print("No UDIDs found.")
