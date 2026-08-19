#Read file example
def read_from_file(filename):
    try:
        with open(filename, 'r') as f:
            data = f.read()
            print("data", data)
    except FileNotFoundError:
        print("File not found")

read_from_file('example2.txt')

#Write file example
def write_to_file(filename, content):
    try:
        with open(filename, 'w') as f:
            f.write(content)
            print("Data written to file")
    except FileNotFoundError:
        print("File not found")

#Append file example
def append_to_file(filename, content):
    try:
        with open(filename, 'a') as f:
            f.write(content)
            print("Data appended to file")
    except FileNotFoundError:
        print("File not found")

filename = 'example2.txt'
content = 'This is an example of writing to a file.\n'
content2 = "Hellow, how are you?"
write_to_file(filename=filename, content=content)
append_to_file(filename=filename, content=content2)

#Copy binrary file
def copy_binary_file(src, dest):
    try:
        with open(src, 'rb') as f_src:
            data = f_src.read()
        with open(dest, 'wb') as f_dest:
            f_dest.write(data)
    except FileNotFoundError:
        print("File not found")

filename_src = 'Hummingbird.webp'
filename_dest = 'images/Hummingbird.webp'
copy_binary_file(src=filename_src, dest=filename_dest)
