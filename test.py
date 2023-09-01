import binascii

# Input string
input_string = "\t\x00\x00\x00"

# Convert the string to hexadecimal
hex_representation = binascii.hexlify(input_string)

print((hex_representation.decode())) 
