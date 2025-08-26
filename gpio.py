from machine import Pin, PWM, Timer, UART
from adc import get_voltage
import neopixel

NEO_PIXEL_PIN_BUILTIN = 8

ADC_PINS = [2, 3, 4, 5]
PWM_PINS = [15, 18, 19, 20, 21, 22]  #
DIGITAL_PINS = [15, 18, 19, 20, 21, 22]
UART_PIN = 14
UART_BAUDRATE = 921600

rgb = neopixel.NeoPixel(Pin(NEO_PIXEL_PIN_BUILTIN), 1)
rgb[0] = (0, 0, 0)
rgb.write()

uart1 = UART(1, UART_BAUDRATE, tx=UART_PIN)


def set_pin(pin, value):
    pin = Pin(pin, Pin.OUT)
    pin.value(value)


def get_pin(pin):
    pin = Pin(pin, Pin.IN)
    return pin.value()


def read_adc(pin):
    return f"{get_voltage(pin):.2f}"


def set_pwm(pin, freq=500, duty_percent=0):
    duty = duty_percent * 65535 // 100
    PWM(Pin(pin), freq=freq, duty_u16=duty)


# Helper function to sanitize and convert input
def sanitize_input(value):
    return int(value) if value else None


def execute(pin=None, typ=None, direction=None, value=None, freq=None):
    try:
        # Extracted type conversion for input sanitization
        pin = sanitize_input(pin)
        try:
            value_int = sanitize_input(value)
        except:
            value_int = None
            pass
        freq = sanitize_input(freq)

        if typ == "pwm" and pin in PWM_PINS:
            print(f'set_pwm({pin}, {freq}, {value_int})')
            set_pwm(pin, freq, value_int)
        elif typ == "adc" and pin in ADC_PINS:
            return read_adc(pin)
        elif typ == "gpio" and pin in DIGITAL_PINS:
            if direction is None:
                print(f"set_pin({pin}, {value_int})")
                set_pin(pin, value_int)
            if direction == "?":
                return str(int(get_pin(pin)))
        elif typ == "uart":
            uart1.write(f"{value}\n".encode())

        return None
    except Exception as e:
        return f"Error: {e}"
