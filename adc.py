from machine import Pin, ADC
import time

# ADC Setup
adc_pin_1 = 0  # ADC an GPIO0
adc_pin_2 = 1  # ADC an GPIO1

adc_1 = ADC(Pin(adc_pin_1))
adc_1.width(ADC.WIDTH_12BIT)  # 12-Bit-Auflösung (0–4095)
adc_1.atten(ADC.ATTN_11DB)
adc_2 = ADC(Pin(adc_pin_2))
adc_2.width(ADC.WIDTH_12BIT)  # 12-Bit-Auflösung (0–4095)
adc_2.atten(ADC.ATTN_11DB)

# Spannungsbereiche für Adressen (berechnet aus den Widerstandswerten)
ADDRESS_RANGES = [
    (3.2, 3.4),  # Spannung für Adresse 1 (ca. 3.30 V ± Toleranz)
    (1.5, 1.9),  # Spannung für Adresse 2 (ca. 1.71 V ± Toleranz)
    (1.0, 1.4),  # Spannung für Adresse 3 (ca. 1.22 V ± Toleranz)
    (0.4, 0.8),  # Spannung für Adresse 4 (ca. 0.64 V ± Toleranz)
    (0.0, 0.2),  # Spannung für Adresse 5 (ca. 0.00 V ± Toleranz)
]


def address_from_table(voltage):
    for i, (low, high) in enumerate(ADDRESS_RANGES):
        if low <= voltage <= high:
            return i + 1  # Adresse ist 1-basiert


def get_address():
    voltage_1 = (adc_1.read() / 1000)  # Spannung berechnen
    voltage_2 = (adc_2.read() / 1000)  # Spannung berechnen
    print(f"Measured Voltage: channel1: {voltage_1:.2f} V channel2: {voltage_2:.2f} V")
    address_ones = address_from_table(voltage_1)
    address_tens = address_from_table(voltage_2)
    print(f"Calculated address: {address_tens}.{address_ones}")
    addr = address_tens * 10 + address_ones if address_ones and address_tens else 0
    return addr


def get_voltage(adc_pin=3):
    adc = ADC(adc_pin)
    adc.width(ADC.WIDTH_12BIT)  # 12-Bit-Auflösung (0–4095)
    adc.atten(ADC.ATTN_11DB)  # Spannung bis 3,3 V
    voltage = (adc.read() / 1000) # Spannung berechnen (0–3,3 V Bereich)
    print(f"Measured Voltage at GPIO{adc_pin}: {voltage:.2f} V")
    return voltage


def main():
    while True:
        address = get_address()
        if address:
            print(f"Meine Adresse: {address}")
        else:
            print("Unbekannte Adresse!")
        time.sleep(1)


if __name__ == "__main__":
    main()
