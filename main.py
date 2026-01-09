from ili9341 import Display, color565
import time
import machine
from ov7670_wrapper import *


class Screen(object):
    # Simple screen demo
    CYAN = color565(0, 255, 255)
    RED = color565(255, 0, 0)
    PURPLE = color565(255, 0, 255)
    WHITE = color565(255, 255, 255)

    def __init__(self, spi1, cam_width, cam_height):
        """Инициализация дисплея и камеры"""
        self.cam_width = cam_width
        self.cam_height = cam_height

        # Инициализация дисплея
        self.display = Display(
            spi1, dc=machine.Pin(9), cs=machine.Pin(5), rst=machine.Pin(8), width=320, height=240, rotation=90
        )

        # Устанавливаем rotation=0 (нормальная ориентация)
        # rotation=1 поворачивает на 90 градусов, что меняет координаты
        self.display.rotation = 0

        # Размеры дисплея
        self.display_width = self.display.width  # 320
        self.display_height = self.display.height  # 240

        print(f"Display: {self.display_width}x{self.display_height}")
        print(f"Camera: {self.cam_width}x{self.cam_height}")

        # Показываем начальный экран
        self.show_start_screen()

    def show_start_screen(self):
        """Начальный экран"""
        self.display.clear()
        self.display.draw_text8x8(50, 50, "OV7670 Camera", self.WHITE)
        self.display.draw_text8x8(
            30, 80, f"{self.cam_width}x{self.cam_height}", self.CYAN
        )
        self.display.draw_text8x8(50, 110, "Starting...", self.WHITE)
        time.sleep(1)
        self.display.clear()


# Инициализация камеры OV7670
data_pin_base = 12  # GPIO 12-19 для данных D0-D7
pclk_pin_no = 11
mclk_pin_no = 20
href_pin_no = 21
vsync_pin_no = 7
reset_pin_no = 10
shutdown_pin_no = 2  # PWDN - подключен к GND
sda_pin_no = 0
scl_pin_no = 1

# Инициализация I2C для конфигурации камеры
i2c = machine.I2C(
    0, freq=400000, scl=machine.Pin(scl_pin_no), sda=machine.Pin(sda_pin_no)
)

# Создание объекта камеры
ov7670 = OV7670Wrapper(
    i2c_bus=i2c,
    mclk_pin_no=mclk_pin_no,
    pclk_pin_no=pclk_pin_no,
    data_pin_base=data_pin_base,
    vsync_pin_no=vsync_pin_no,
    href_pin_no=href_pin_no,
    reset_pin_no=reset_pin_no,
    shutdown_pin_no=shutdown_pin_no,
    half_capture=False,  
)

# Конфигурация камеры
ov7670.wrapper_configure_rgb()
ov7670.wrapper_configure_base()
width, height = ov7670.wrapper_configure_size(OV7670_WRAPPER_SIZE_DIV2)  # 320x240
ov7670.wrapper_configure_test_pattern(OV7670_WRAPPER_TEST_PATTERN_NONE)

print(f"Camera initialized: {width}x{height}")
print(f"Buffer size: {width * height} bytes")
spi1 = machine.SPI(
        0,
        baudrate=20000000,
        polarity=1,
        phase=1,
        bits=8,
        firstbit=machine.SPI.MSB,
        sck=machine.Pin(6),
        mosi=machine.Pin(3),
        miso=machine.Pin(4),
    )

# Создаем экран с передачей размеров камеры
screen = Screen(spi1, width, height)

def configure_correct_rgb565(ov7670):
    """Настройка камеры для правильного RGB565"""
    # Попробуйте эту последовательность регистров:
    registers = [
        (0x12, 0x04),  # COM7: RGB формат
        (0x40, 0xD0),  # COM15: RGB565, полный диапазон
        (0x8C, 0x00),  # RGB444 отключен
        

        

    ]
    
    for reg, value in registers:
        ov7670.write_register(reg, value)
        time.sleep_ms(10)
    
    print("Камера настроена на RGB565")


def main():
    """Основная функция"""
    # Инициализация SPI для дисплея

    buf = bytearray(2*width * height)
    #configure_correct_rgb565(ov7670)
    #diagnose_camera_colors(ov7670)
    
    try:
        while True:
            # Захват кадра
            #start = time.ticks_us()
            ov7670.capture(buf)
            #buf = swap_rgb565_bytes(buf)
            #buf = convert_bgr_to_rgb(buf)
            #capture_time = time.ticks_diff(time.ticks_us(), start)

            # Выводим ASCII-арт на дисплей
            screen.display.draw_sprite(buf,0,0, 320, 240)
            # Выводим информацию о времени захвата в нижней части дисплея
            # Очищаем область для текста
            screen.display.fill_rectangle(0, 240, 240, 0, color565(0, 0, 0))

            # Выводим статистику
          
            

            # Выводим время в консоль для отладки

            #print(f"Capture: {capture_time}us | Display: {screen.display_width}x{screen.display_height}")

            # Небольшая пауза для стабильности
            #time.sleep_ms(50)

    except KeyboardInterrupt:
        screen.display.clear()
        screen.display.draw_text8x8(50, 150, "Goodbye!", screen.CYAN)
        time.sleep(2)
        screen.display.display_off()
        print("\nCamera stopped.")


# Запуск приложения
if __name__ == "__main__":
    main()
