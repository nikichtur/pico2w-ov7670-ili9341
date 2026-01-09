import machine
from ov7670_wrapper import *
import time

data_pin_base = 12  # 0 and the next 7 pins. So GPIO 0-7 in this case.
pclk_pin_no = 11
mclk_pin_no = 20
href_pin_no = 21
vsync_pin_no = 7
reset_pin_no = 10
shutdown_pin_no = 2
sda_pin_no = 0
scl_pin_no = 1

i2c = machine.I2C(
    0, freq=400000, scl=machine.Pin(scl_pin_no), sda=machine.Pin(sda_pin_no)
)
ov7670 = OV7670Wrapper(
    i2c_bus=i2c,
    mclk_pin_no=mclk_pin_no,
    pclk_pin_no=pclk_pin_no,
    data_pin_base=data_pin_base,
    vsync_pin_no=vsync_pin_no,
    href_pin_no=href_pin_no,
    reset_pin_no=reset_pin_no,
    shutdown_pin_no=shutdown_pin_no,
    half_capture=False,  # Capture only (first) greyscale byte of YUV pixel color.
)

ov7670.wrapper_configure_yuv()
ov7670.wrapper_configure_base()
width, height = ov7670.wrapper_configure_size(OV7670_WRAPPER_SIZE_DIV2)
ov7670.wrapper_configure_test_pattern(OV7670_WRAPPER_TEST_PATTERN_NONE)
# while(True):
#     buf = bytearray(width * height)
#     print("capture start")
#     ov7670.capture(buf)
#     print("capture end")
#     print(buf)


for _ in range(50):
    # time.sleep(0.5)
    buf = bytearray(2 * width * height)
    start = time.ticks_us()
    ov7670.capture(buf)
    #print(len(buf))
    print(time.ticks_diff(time.ticks_us(), start), end="\n")
    # chars = " .:-=+*#%@"
    # for y in range(height):
    #     for x in range(width):
    #         value = buf[(y*width+x)]
    #         print(chars[value*len(chars)//256], end='')
    #     print('')
