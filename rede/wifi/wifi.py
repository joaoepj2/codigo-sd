# lib is too old
# it doesn't run on python 3

import wifi

for iface in interfaces
    print(f"Interface Wifi: " {iface.name()})

cells = wifi.Cell.all(iface)


for cell in cells:
    print(f"Rede: {cell.ssid}")
    print(f"  Força do sinal (dBm): {cell.signal}")
    print(f"  Criptografado? {'Sim' if cell.encrypted else 'Não'}")
    print(f"  Tipo de segurança: {cell.authentication_type}")
    print("---")