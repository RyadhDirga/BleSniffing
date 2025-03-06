import asyncio
from bleak import BleakClient

# Ganti dengan alamat MAC FORA IR42 yang ditemukan saat scan
FORA_IR42_MAC = "C0:26:DA:3C:AC:13"

# UUID dari layanan dan karakteristik FORA IR42
SERVICE_UUID = "00001809-0000-1000-8000-00805f9b34fb"  # Health Thermometer
CHARACTERISTIC_UUID = "00002a1c-0000-1000-8000-00805f9b34fb"  # Temperature Measurement
DESCRIPTOR_UUID = "00002902-0000-1000-8000-00805f9b34fb"  # CCCD Descriptor

# Fungsi parsing suhu dari data BLE (IEEE 11073 Floating Point)
def parse_temperature(data):
    if len(data) < 4:
        return None

    mantissa = int.from_bytes(data[1:3], byteorder="little", signed=True)
    exponent = int.from_bytes([data[3]], byteorder="little", signed=True)

    temperature = mantissa * (10 ** exponent)/10
    return temperature

# Callback saat menerima data suhu dari BLE
def temperature_callback(sender, data):
    temperature = parse_temperature(data)
    if temperature is not None:
        print(f"Suhu dalam Celsius: {temperature:.1f}°C")
    else:
        print("Gagal membaca suhu.")

async def read_temperature():
    async with BleakClient(FORA_IR42_MAC) as client:
        print(f"Terhubung ke {FORA_IR42_MAC}")

        # Menulis ke descriptor CCCD untuk mengaktifkan indikasi
        try:
            print("Mengaktifkan indikasi suhu...")
            await client.write_gatt_descriptor(DESCRIPTOR_UUID, b"\x02\x00")
            print("Indikasi suhu aktif.")
        except Exception as e:
            print(f"ERROR: Gagal menulis ke CCCD - {e}")

        # Mendaftarkan callback untuk menerima data suhu
        await client.start_notify(CHARACTERISTIC_UUID, temperature_callback)

        print("Menunggu data suhu...")
        await asyncio.sleep(30)  # Biarkan program berjalan selama 30 detik untuk menerima suhu

        # Hentikan notifikasi sebelum keluar
        await client.stop_notify(CHARACTERISTIC_UUID)

asyncio.run(read_temperature())