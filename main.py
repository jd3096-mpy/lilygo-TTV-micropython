import network,time
from machine import I2C,Pin,SPI,ADC
from ssd1309 import Display
from time import sleep
import pcf8563
from IR import IR

#IR
nec = IR(13)
#ADC
adc = ADC(Pin(34)) 
adc.atten(ADC.ATTN_11DB)
#TOUCH
touchen=Pin(32,Pin.OUT)
touchen.value(1)
touch=Pin(15,Pin.IN,Pin.PULL_UP)
#POWER
power=Pin(2,Pin.OUT)
power.value(1)
#OLED SSD1309
oledpower=Pin(33,Pin.OUT)
oledpower.value(1)
spi = SPI(1, baudrate=1000000, sck=Pin(18), mosi=Pin(23))
display = Display(spi, dc=Pin(19), cs=Pin(5), rst=Pin(4))
#RTC
i2c = I2C(scl=Pin(25), sda=Pin(26))
r = pcf8563.PCF8563(i2c)

def updatetime():
    ntptime.NTP_DELTA = 3155644800   # 可选 UTC+8偏移时间（秒），不设置就是UTC0
    ntptime.host = 'ntp1.aliyun.com'  # 可选，ntp服务器，默认是"pool.ntp.org"
    ntptime.settime()   # 修改设备时间,到这就已经设置好了
    
def WIFI_Connect():
    wlan = network.WLAN(network.STA_IF) #STA模式
    wlan.active(True)                   #激活接口
    start_time=time.time()              #记录时间做超时判断

    if not wlan.isconnected():
        print('connecting to network...')
        #wlan.connect('turang1226', '12345678') #输入WIFI账号密码
        wlan.connect('findx3', '800080008000') #输入WIFI账号密码
        while not wlan.isconnected():
            if time.time()-start_time > 15 :
                print('WIFI Connected Timeout!')
                break

    if wlan.isconnected():
        print('network information:', wlan.ifconfig())
        return True
        
#main program
#screen
display.clear_buffers()
display.monoFB.text('TEST 1:SCREEN',0,0,1)
display.monoFB.text('helloworld',0,20,1)
display.monoFB.fill_rect(100,20,10,10,1)
display.monoFB.text('tap to continue',0,40,1)
display.present()
while touch.value()==0:
    pass
#adc
time.sleep_ms(500)
while touch.value()==0:
    display.clear_buffers()
    display.monoFB.text('TEST 2:ADC',0,0,1)
    bat=adc.read()
    display.monoFB.text('battery:'+str(bat),0,20,1)
    display.monoFB.text('tap to continue',0,40,1)
    display.present()
    time.sleep_ms(500)
#IR
time.sleep_ms(500)
display.clear_buffers()
display.monoFB.text('TEST 3:IR',0,0,1)
display.monoFB.text('IRCMD:',0,20,1)
display.monoFB.text('tap to continue',0,40,1)
display.present()
while touch.value()==0:
    cmd=nec.getIR()
    if cmd!=None:
        display.clear_buffers()
        display.monoFB.text('TEST 3:IR',0,0,1)
        display.monoFB.text('IRCMD:'+str(cmd),0,20,1)
        display.monoFB.text('tap to continue',0,40,1)
        display.present()
        time.sleep_ms(200)

#time
time.sleep_ms(500)
#sync systemtime first
r.write_now()
while 1:
    display.clear_buffers()
    dt=r.datetime()
    #print(dt)
    year='20'+str(dt[0])
    month=dt[1]
    if month<10:
        month='0'+str(dt[1])
    else:
        month=str(dt[1])
    day=dt[2]
    if day<10:
        day='0'+str(dt[2])
    else:
        day=str(dt[2])
    weekday=dt[3]
    if weekday==0:
        weekday='Mon'
    elif weekday==1:
        weekday='Tue'
    elif weekday==2:
        weekday='Wes'
    elif weekday==3:
        weekday='Thr'
    elif weekday==4:
        weekday='Fri'
    elif weekday==5:
        weekday='Sat'
    elif weekday==6:
        weekday='Sun'
    hour=dt[4]
    if hour<10:
        hour='0'+str(dt[4])
    else:
        hour=str(dt[4])
    minute=dt[5]
    if minute<10:
        minute='0'+str(dt[5])
    else:
        minute=str(dt[5])
    sec=dt[6]
    if sec<10:
        sec='0'+str(dt[6])
    else:
        sec=str(dt[6])
    daystr=year+'-'+month+'-'+day
    timestr=hour+':'+minute+':'+sec
    display.monoFB.text('TEST 4:RTC',0,0,1)
    display.monoFB.text(daystr,15,15,1)
    display.monoFB.text(timestr,15,25,1)
    display.monoFB.text(weekday,90,25,1)
    display.monoFB.text('All test done!',0,40,1)
    display.present()














