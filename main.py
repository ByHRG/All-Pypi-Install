# -*- coding: utf-8 -*-
import subprocess
subprocess.run(
    ["pip", "install", "httpx"],
    check=True,
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
)
subprocess.run(
    ["pip", "install", "bs4"],
    check=True,
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
)
import httpx
from bs4 import BeautifulSoup

def install_all_pypi_packages():
    url = "https://pypi.org/simple/"

    try:
        htx = httpx.get(url, timeout=60)
        htx.raise_for_status()
    except Exception as e:
        print("Unable to import data:", e)
        return

    try:
        soup = BeautifulSoup(htx.text, "html.parser")
        package_links = soup.find_all("a")
        package_names = [a.text.strip() for a in package_links if a.text]
    except Exception as e:
        print("Error parsing package name:", e)
        return

    print(f"found a total of {len(package_names)} package names")

    for name in package_names:
        print(f"install: {name} …")
        try:
            subprocess.run(
                ["pip", "install", name],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        except subprocess.CalledProcessError:
            print(f"  → install failed: {name}")
        break

if __name__ == "__main__":
    install_all_pypi_packages()
