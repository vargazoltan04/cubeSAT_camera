# cubeSAT_camera
This is a project in which we make the camera system for a cubeSAT which can make videos, and images.

# Protocol 
`<start_char><content><end_char><checksum>`

start_char: 1 byte
content: 59 bytes (3 bytes destination, 57 bytes parameters, which contains the useful data as well. Between parameters, there are a comma. )
end_char: 1 byte
checksum: 1 bytes
end: \r\n 2 bytes

Packet only contains readable characters. 
Checksum is calculated by summing every byte from start_char to end_char (including start_char and end_char) and moduloing them with 256

# PC -> Camera

start_char: $
end_char: %

Content is in string format.

# Camera -> PC

start_char: #
end_char: %

Content is in hex format, because it is in RGB, and converting it to ascii doesnt necessarily means it will be a readable character. 
It converts the destination, and everything to hex, not just the raw RGB data.