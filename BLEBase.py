import asyncio
from bleak import BleakClient

# Gantilah MAC Address dari device BLE yang ditemukan saat scan
MAC = "70:87:9E:61:15:5D"

# UUID dari layanan dan karakteristik device BLE (sesuaikan jika perlu gunakan NRF connect)
SERVICE_UUID = "0000181d-0000-1000-8000-00805f9b34fb"  
CHARACTERISTIC_UUID = "00002a9d-0000-1000-8000-00805f9b34fb" 

# Fungsi untuk menampilkan data raw dari BLE
def device_callback(sender, data):
    print(f" (Hex: {data.hex()} (RAW: {list(data)})")

# Fungsi utama untuk membaca data dari BLE
async def read_device_data():
    async with BleakClient(MAC) as client:
        print(f"Terhubung ke {MAC}")

        # Mendaftarkan callback untuk menerima data dari device
        await client.start_notify(CHARACTERISTIC_UUID, device_callback)

        print("Menunggu data dari BLE...")
        await asyncio.sleep(30)  # Biarkan program berjalan selama 30 detik untuk menerima data

        # Hentikan notifikasi sebelum keluar
        await client.stop_notify(CHARACTERISTIC_UUID)
        print("Notifikasi dimatikan.")

asyncio.run(read_device_data())