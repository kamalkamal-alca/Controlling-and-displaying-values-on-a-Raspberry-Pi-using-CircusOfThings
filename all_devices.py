import requests   
import json     
import time
import RPi.GPIO as GPIO

from w1thermsensor import W1ThermSensor
sensor = W1ThermSensor()

KEY_1   ="22646"              
VALUE_1 = "ON1" 
KEY_2   ="27323"           
VALUE_2 = 0 
KEY_3   ="24690" #temp C DS18B20         
VALUE_3 = 0               
KEY_4   ="21992" #temp F DS18B20          
VALUE_4 = 0 
                 
TOKEN  ="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" #the token is found under account in circusofthings.com     

data_1={'Key':'0','Value':0,'Token':'0'} 

redLED = 23 

GPIO.setwarnings(False)			#disable warnings
GPIO.setmode(GPIO.BCM)		#set pin numbering system

GPIO.setup(redLED,GPIO.OUT)
pi_pwm = GPIO.PWM(redLED,1000)		#create PWM instance with frequency
pi_pwm.start(0)	
#======================================================================
dataPin  = 24  # Pin for Data (GPIO 24)
latchPin = 23  # Pin for Latch (GPIO 23)
clockPin = 18  # Pin for Clock (GPIO 18)

GPIO.setup(dataPin, GPIO.OUT)
GPIO.setup(clockPin, GPIO.OUT)
GPIO.setup(latchPin, GPIO.OUT)

# Variables
shift_data = 0b00000000  # Initial state of the shift register (all LEDs off)
previous_shift_data = 0b00000000

# Function to update shift register
def update_shift_register():
    global shift_data, previous_shift_data
    if shift_data != previous_shift_data:
        previous_shift_data = shift_data
        GPIO.output(latchPin, GPIO.LOW)
        shift_out(shift_data)
        GPIO.output(latchPin, GPIO.HIGH)

# Shift out data (similar to Arduino's shiftOut function)
def shift_out(data):
    for i in range(8):
        GPIO.output(clockPin, GPIO.LOW)
        GPIO.output(dataPin, (data >> (7 - i)) & 0x01)
        GPIO.output(clockPin, GPIO.HIGH)
#======================================================================
while True:
    temp_c = sensor.get_temperature()
    temp_C = str(round(temp_c))
    temp_F = (float(temp_c)*1.8+32)
    print("The temperature_C %s C" % temp_C)
    print("The temperature_F %s C" % temp_F)

    data_1={'Key':'22646','Value':0,'Token':'0'}     
    data_2={'Key':'27323','Value':0,'Token':'0'}
    data_3={'Key':'24690','Value':'temp_C','Token':'0'}  
    data_4={'Key':'30792','Value':'temp_F','Token':'0'} 

    data_1['Key'] = KEY_1 
    data_1['Value']=VALUE_1
    data_1['Token']=TOKEN

    data_2['Key'] = KEY_2
    data_2['Value']=VALUE_2
    data_2['Token']=TOKEN

    data_3['Key'] = KEY_3 
    data_3['Value']=temp_C
    data_3['Token']=TOKEN

    data_4['Key'] = KEY_4 
    data_4['Value']=temp_F
    data_4['Token']=TOKEN

#========================================================================
    payload = data_1
    response=requests.get('https://circusofthings.com/ReadValue',params=payload)

    datahandling=json.loads(response.content)  
    print(datahandling["Value"]) #here we parse and get the value of the signal

    # Remove the global declaration here since we're in the global scope already
    if (datahandling["Value"])==0:
       shift_data |= 0b00000001  # Turn LED1 on
       print("LED1=0")
    elif (datahandling["Value"])== 1:
       shift_data &= 0b11111110  # Turn LED1 off
       print("LED1=1")

    elif (datahandling["Value"])== 2:
       shift_data |= 0b00000010  # Turn LED2 on
       print("LED2=0")
    elif (datahandling["Value"])== 3:
       shift_data &= 0b11111101  # Turn LED2 off       
       print("LED2=1")

    elif (datahandling["Value"])== 4:
       shift_data |= 0b00000100  # Turn LED3 on
       print("LED3=0")
    elif (datahandling["Value"])== 5:
       shift_data &= 0b11111011  # Turn LED3 off
       print("LED3=1")
    elif (datahandling["Value"])== 6:
       shift_data |= 0b00001000  # Turn LED4 on
       print("LED4=0")
    elif (datahandling["Value"])== 7:
       shift_data &= 0b11110111  # Turn LED4 off
       print("LED4=1")
    
    # Add update call to actually send data to shift register
    update_shift_register()     
#========================================================================
    payload = data_2
    response=requests.get('https://circusofthings.com/ReadValue',params=payload)

    datahandling=json.loads(response.content)  
    i = datahandling["Value"]
    print(i)
    pi_pwm.ChangeDutyCycle(i)
#========================================================================
    response=requests.put('https://circusofthings.com/WriteValue',
				data=json.dumps(data_3),headers={'Content-Type':'application/json'}) 
    if(response.status_code==200):
        print("succsess")
    else:
        print("error %d" % (response.status_code))

    payload = data_3
    response=requests.get('https://circusofthings.com/ReadValue',params=payload)
    datahandling=json.loads(response.content)  
#========================================================================
    response=requests.put('https://circusofthings.com/WriteValue',
				data=json.dumps(data_4),headers={'Content-Type':'application/json'}) 
    if(response.status_code==200):
        print("succsess")
    else:
        print("error %d" % (response.status_code))
    payload = data_4
    response=requests.get('https://circusofthings.com/ReadValue',params=payload)
    datahandling=json.loads(response.content)   
    
    time.sleep(2)
