import binascii

def byte_to_binary(n):
    return ''.join(str((n & (1 << i)) and 1) for i in reversed(range(8)))

def hex_to_binary(h):
    return ''.join(byte_to_binary(ord(b)) for b in binascii.unhexlify(h))


testbytes = [
	'AA0C04000CFFFFE830C03007C51003010803A2E9',
]

#THIS EXAMPLE HAS THE WRONG PACKET CONTROL HEADER
#in this example it would be 1100 0000 because we have network and GPIO data
'''I have changed the packet control header in testbytes to represet the actual data represented'''


#THIS EXAMPLE HAS THE WRONG NETWORK CONTROL FIELD VALUE
#In this example it's 0011 0000
'''Again I have changed the value ofthe networkControlField in testbytes to repreest the values the data holds
occording to the example'''


counter = 2


#I tried several methods to get through the data while storing the index of which data has already been read.
#conceptually this type of funciton isn't ideal since it realies on outside variables but it works for now
#so... keeping it for now. I should find a better way to do it


def byteselection(string,length):
	global counter
	counter += length
	return string[counter-length:counter]

class decodeSignal:
	def __init__(self,string):
		#Take in the tag to host communication as a string of characters
		#Then we split up the relative number of 'bytes' into their corresponding definitions
		#a byte is represented by two characters
		self.b = string

		#the first two characters are just filler/ identification. AA = tag to host. 55 = host to tag. Ignoring that for now
		#since this is to decode messages from the tag to the host.
		self.packetLength = byteselection(string,2)
		self.packetType = byteselection(string,2)


		self.tagID = byteselection(string,4)
		self.readerID = byteselection(string,4)
		self.packetNumber = byteselection(string,2)

		#TODO: Packet type changes based on the type of signal. Beacon (30) response packet (31). Need to add detection of these types
		#and create a new tree for each type of packet type. The current tree below is for beacon packets (30)
		self.tagPacketType = byteselection(string,2)
		
		#The contorl header field is the first value to have more data inside the byte that we must decode
		#Read data, turn it into binary so we can read the bits, look at each bit and create definitions
		#for the data that is there. If a value is zero then the data is not present and a definition is not created.

		#read data
		self.packetControlHeader = byteselection(string,2)

		#turn into binary. Returns a list of integer binary values
		y = [int(char) for char in str(hex_to_binary(self.packetControlHeader))]

		#do stuff with data
		if y[0]:
			'''Network Field present'''
			
			#Network field is another byte that includes information to which data follows it.
			#Use same procerude as with the control header.

			self.networkControlField = byteselection(string,2)

			x = [int(char) for char in str(hex_to_binary(self.networkControlField))]

			if x[0]:
				'''Current Time report'''
				#PUT THIS IN. NOT SURE WHAT THE BYTE LENGTH IS
				pass
			if x[1]:
				'''Transmit Interval report'''
				self.transmitInterval = byteselection(string,2)
			if x[2]:
				'''#transmit Power report'''
				self.transmitPower = byteselection(string,2)
			if x[3]:
				'''#battery voltage'''
				self.batteryVoltage = byteselection(string,2)
			if x[4]:
				'''#current mode report'''
				self.currentMode = byteselection(string,2)
			#REST OF THE BYTES SHOULD ALWAYS BE ZERO FOR THE NETWORK CONTROL FIELD

		if y[1]:
			'''GPIO field present'''
			self.GPIOfield = byteselection(string,2)
			x = [int(char) for char in str(hex_to_binary(self.GPIOfield))]

			#Take out the bytes that are present occriding to the GPIO field

			if x[0]:
				'''#Analog Digital config report'''
				#returns a tuple of of form (PIN, DIGITAL/ANALOG)
				self.analogdigitalConfigReport = byteselection(string,2)
				# 1 = analog, 0 = digital and outputs will be 0
				self.analogdigitalConfigReport = zip(['A7','A6','A5','A4','A3','A2','A1','A0'], [int(char) for char in str(hex_to_binary(self.analogdigitalConfigReport))])
			if x[1]:
				'''#I/O config report'''
				pass
			if x[2]:
				'''#Digital Report'''
				pass
			if x[3]:
				'''#Analog Reference'''
				pass
			if x[4]:
				'''#Analog Report'''
				pass
			#rest should always be zero

		if y[2]:
			'''#Alarm Field present'''
			pass
		if y[3]:
			'''#Trigger field present'''
			pass
		if y[4]:
			'''#User Memory field present'''
			pass
		if y[5]:
			'''#Data samping field present'''
			pass
		if y[6]:
			'''#RTLS present'''
			pass
		if y[7]:
			'''#Should always be zero'''
			pass



signal = decodeSignal(testbytes[0])


# print signal.packetLength
# print signal.packetType
# print signal.tagID
# print signal.readerID
# print signal.packetNumber
# print signal.tagPacketType
print "Control Header:   " + signal.packetControlHeader
print "network control:  " + signal.networkControlField
print "tranmist power:   " + signal.transmitPower
print "batt voltage:     " + signal.batteryVoltage
print "gpio field:       " + signal.GPIOfield


"""
other Crap


Transmit Power
0x07
Battery Voltage
0xC5
GPIO Field Control Header
0x10
Only the Analog Report sub field is present.
Confidential Page 110 9/7/2010
Analog Report
0x03
This means that data for Pin 1 and Pin 2 will be reported
Analog Data
0x0108 0x03A2
These bytes represent the 10-bit value of the voltages at Pin 1 and Pin 2.
RSSI
0xE9
"""

