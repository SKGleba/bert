#!/usr/bin/env python3

import sys, os, struct, code, binascii
import serial, time, re, math


def read_all(port, size):
	data = b''
	while len(data) < size:
		data += port.read(size - len(data))
	assert len(data) == size
	return data

class Client(object):
	def __init__(self, uart_port):
		self._port = serial.Serial(uart_port, baudrate=38400, timeout=0)

	def read_all(self, size):
		return read_all(self._port, size)

	def read_line(self, terminator=b'\n'):
		data = []
		c = b''
		while c != terminator:
			c = self.read_all(1)
			data.append(c)
		return b''.join(data)

	def checksum(self, data):
		cksum = 0
		for c in data:
			cksum += c
			cksum &= 0xFF
		return cksum

	def send_cmd(self, cmd):
		# note: cmds with args must have a space after each arg
		# sometimes, the last arg needs a space after it too?
		cmd = cmd.encode('ascii')
		cmd += ':{0:02X}\r\n'.format(self.checksum(cmd)).encode('ascii')
		#print('send: {0}'.format(cmd[:-1].decode('ascii')))
		self._port.write(cmd)



client = Client('COM6')

cmd = sys.argv[1]

client.send_cmd(cmd)
cur_line = client.read_line()
print(cur_line.decode("ascii"), end ='')