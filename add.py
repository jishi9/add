import curses
from curses import wrapper
from time import sleep

'''
A quick script written for fun. Adds two positive integers manually
'''

SECS_BETWEEN_OPERATIONS = 0.4
SECS_AFTER_FINISH = 0.6

def pad_string(string, length):
	assert(len(string) <= length)
	return ' ' * (length - len(string)) + string

def to_int(character):
	assert character == ' ' or ('0' <= character <= '9') 
	if character == ' ':
		return 0
	else:
		return ord(character) - ord('0')

def add(x, y, stdscr):
	x = str(x)
	y = str(y)

	# one more space to accommodate for an extra carry
	length = max(len(x), len(y)) + 1
	x = pad_string(x, length)
	y = pad_string(y, length)

	result_buffer = bytearray(' ' * length)
	carry_buffer = bytearray(' ' * length)

	def print_state():
		stdscr.clear()

		lines = [
			'  ' + str(carry_buffer),
			'  ' + x,
			'+ ' + y,
			'  ' + '-' * length,
			'  ' + str(result_buffer)
		]
		stdscr.addstr('\n'.join(lines))
		stdscr.refresh()
		sleep(SECS_BETWEEN_OPERATIONS)
		
	print_state()

	lst = list(enumerate(zip(x, y)))
	for i, (n1, n2) in reversed(lst):
		c = chr(carry_buffer[i])
		the_sum = to_int(n1) + to_int(n2) + to_int(c)

		# Don't add left-most column if there's nothing to add (avoids leading 0)
		if i == 0 and the_sum == 0: continue

		result_buffer[i] = str(the_sum % 10)
		print_state()

		carry = the_sum / 10
		if carry > 0:
			carry_buffer[i-1] = str(carry)
			print_state()

	sleep(SECS_AFTER_FINISH)


def main(stdscr):
	# Make cursor invisible
	curses.curs_set(0)

	import random
	while True:
		x = random.randint(0, 999999999999)
		y = random.randint(0, 999999999999)
		add(x, y, stdscr)


if __name__ == '__main__':
	wrapper(main)
