# *****************************************************************************
# * | File        :   main.py
# * | Author      :   Samuel Menéndez G
# * | Driver      :   Waveshare team
# * | Function    :   
# * | Info        :
# *----------------
# * | This version:   V1.0
# * | Date        :   19-01-2023
# -----------------------------------------------------------------------------

from machine import Pin
import utime
import epaper
import framebuf

page = 0

current_act = 0   # 0: menu
                  # 1: book menu
                  # 2: book
                  # 3: TBD

debounce_time=0
def btnPress(pin):
    global debounce_time, page
    pin.irq(handler=None)
    if (utime.ticks_ms()-debounce_time) > 10:
        print("interrupt")
        print(pin)
        if current_act == 2:
            if pin == Pin(21, mode=Pin.IN, pull=Pin.PULL_UP):
                page = page + 1
                print(page)
                print("next")
                book("book", page)
            if pin == Pin(22, mode=Pin.IN, pull=Pin.PULL_UP):
                page = page - 1
                print("back")
                book("book", page)
        debounce_time=utime.ticks_ms()
        pin.irq(trigger=Pin.IRQ_FALLING, handler=btnPress)
    utime.sleep(1)

def text_wrap(str,x,y,w,h,color,border=None):
	# optional box border
	if border is not None:
		epd.rect(x, y, w, h, border)
	cols = w // 8
	# for each row
	j = 0
	for i in range(0, len(str), cols):
		# draw as many chars fit on the line
		epd.text(str[i:i+cols], x, y + j, color)
		j += 8
		# dont overflow text outside the box
		if j >= h:
			break

def text_center(str, y, color):
    chars = len(str)
    epd.text(str, 64 - chars * 4, y, color)
    
def book(book_name, page):
    # blank canvas
    epd.fill(0xff)
    
    # Open book
    book = open(book_name + ".txt", "r")
    # Book title and info
    epd.fill_rect(0, 0, 128, 16, 0x00)
    text_center(book.readline().rstrip("\n"), 5, 0xFF)
    
    for i in range(page):
        book.readline()
    
    page = book.readline().rstrip("\n")
    
    if page[0] == "¿":
        text_center(page.replace("¿", ""), 136, 0x00)
    else:
        text_wrap(page, 0, 20, 128, 276, 0x00)
    
    book.close()
    epd.display(epd.buffer)

def menu(item, item_bmp):
    # item title
    epd.fill_rect(0, 4, 128, 24, 0x00)
    text_center(item, 9, 0xFF)
    # item bitemap (icon/bookcover)
    epd.rect(4, 34, 120, 174, 0x00)
    
    epd.display(epd.buffer)
    

if __name__=='__main__':
    btn_next = Pin(21, Pin.IN, Pin.PULL_UP)
    btn_back = Pin(22, Pin.IN, Pin.PULL_UP)
    
    btn_next.irq(trigger=Pin.IRQ_FALLING, handler=btnPress)
    btn_back.irq(trigger=Pin.IRQ_FALLING, handler=btnPress)
   
    epd = epaper.EPD_2in9()
    epd.Clear(0xff)
    
    epd.fill(0xff)
    
    current_act = 2
    
    if current_act == 1:
        menu("name", None)
    
    if current_act == 2:
        book("book", page)
    
    while True:
        epd.delay_ms(10)
    
    # epd.vline(10, 90, 60, 0x00)
    # epd.vline(120, 90, 60, 0x00)
    # epd.hline(10, 90, 110, 0x00)
    # epd.hline(10, 150, 110, 0x00)
    # epd.line(10, 90, 120, 150, 0x00)
    # epd.line(120, 90, 10, 150, 0x00)
    # epd.display(epd.buffer)
    # epd.delay_ms(2000)
    
    # epd.rect(10, 180, 50, 80, 0x00)
    # epd.fill_rect(70, 180, 50, 80, 0x00)
    # epd.display_Base(epd.buffer)
    # epd.delay_ms(2000)
    
    # for i in range(0, 20):
    #     book("book", page)
    #     page = page + 1
    #     epd.delay_ms(3500)
        
    epd.init()
    epd.Clear(0xff)
    epd.delay_ms(2000)
    print("sleep")
    epd.sleep()