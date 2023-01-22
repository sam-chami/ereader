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
import os

page = 0
reading = "" # ej: DonQuijote

current_act = 0   # 0: menu
                  # 1: book menu
                  # 2: book
                  # 3: TBD


# scan for books
unstripped = os.listdir('books')
items = []

for i in range(len(unstripped)):
    items.append(unstripped[i].split(".")[0])
items.append("scrClear")
print(items)

debounce_time=0
def btnPress(pin):
    global debounce_time, page, items, current_act, reading
    pin.irq(handler=None)
    if (utime.ticks_ms()-debounce_time) > 20:
        print(page)
        print(pin)
        # When in bookshelf mode
        if current_act == 1:
            if pin == Pin(20, mode=Pin.IN, pull=Pin.PULL_UP):
                if items[page] == "scrClear":
                    epd.Clear(0xff)
                else:
                    current_act = 2
                    reading = items[page]
                    book(reading, 0)
                    page = 0
            if pin == Pin(21, mode=Pin.IN, pull=Pin.PULL_UP):
                if page != len(items) - 1:
                    page = page + 1
                else:
                    page = 0
                menu(items[page])
            if pin == Pin(22, mode=Pin.IN, pull=Pin.PULL_UP):
                if page == 0:
                    page = len(items) - 1
                else:
                    page = page - 1
                menu(items[page])
            pin.irq(trigger=Pin.IRQ_FALLING, handler=btnPress)
            debounce_time=utime.ticks_ms()
            return 0
        # When in reading mode
        if current_act == 2:
            if pin == Pin(20, mode=Pin.IN, pull=Pin.PULL_UP):
                current_act = 1
                page = 0
                menu(items[page])
            if pin == Pin(21, mode=Pin.IN, pull=Pin.PULL_UP):
                page = page + 1
                book(reading, page)
            if pin == Pin(22, mode=Pin.IN, pull=Pin.PULL_UP):
                page = page - 1
                book(reading, page)
            pin.irq(trigger=Pin.IRQ_FALLING, handler=btnPress)
            debounce_time=utime.ticks_ms()
            return 0
    debounce_time=utime.ticks_ms()

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
    book = open("/books/" + book_name + ".txt", "r")
    # Book title and info
    epd.fill_rect(0, 0, 128, 16, 0x00)
    text_center("Page " + str(page + 1), 5, 0xFF)
    
    for i in range(page):
        book.readline()
    
    try:
        page = book.readline().rstrip("\n")
    except:
        page = "¿The End"
    
    if page[0] == "¿":
        text_center(page.replace("¿", ""), 136, 0x00)
    else:
        text_wrap(page, 0, 20, 128, 276, 0x00)
    
    book.close()
    epd.display(epd.buffer)

def menu(item, page = None):
    with open("/pics/" + item + ".pbm", 'rb') as fd:
        pbm_format = fd.readline().strip()
        if pbm_format != b'P4':
            print("ERROR: input file must be binary PBM (type P4)")
            return 1
        pbm_dims = [int(d) for d in fd.readline().strip().split()]
        pbm_data = fd.read()

    bmp = bytearray(pbm_data)
    
    epd.display(bmp)

if __name__=='__main__':
    btn_ok = Pin(20, Pin.IN, Pin.PULL_UP)
    btn_next = Pin(21, Pin.IN, Pin.PULL_UP)
    btn_back = Pin(22, Pin.IN, Pin.PULL_UP)
    
    btn_ok.irq(trigger=Pin.IRQ_FALLING, handler=btnPress)
    btn_next.irq(trigger=Pin.IRQ_FALLING, handler=btnPress)
    btn_back.irq(trigger=Pin.IRQ_FALLING, handler=btnPress)
   
    epd = epaper.EPD_2in9()
    epd.Clear(0xff)
    
    epd.fill(0xff)
    
    current_act = 1
    menu(items[page])
    
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