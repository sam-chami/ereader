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

from machine import Pin, SPI
import framebuf
import utime
import epaper

page = 0

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
    
    text_wrap(book.readline().rstrip("\n"), 0, 20, 128, 276, 0x00)
    book.close()
    epd.display(epd.buffer)

if __name__=='__main__':
    epd = epaper.EPD_2in9()
    epd.Clear(0xff)
    
    epd.fill(0xff)
    
    
    epd.delay_ms(2000)
    
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
    
    for i in range(0, 10):
        book("book", page)
        page = page + 1
        epd.delay_ms(2000)
        
    epd.init()
    # epd.Clear(0xff)
    epd.delay_ms(2000)
    print("sleep")
    epd.sleep()