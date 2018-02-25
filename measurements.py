def read_values(input_string):
    read_list = list(input_string.rsplit(','))
    read_list_int = [float(element) for element in read_list]
    return read_list_int

my_file = open('measurements.txt', 'r')
counter_line = 0
for line in my_file:
    if counter_line % 2 != 0:
        current_line = str(line)
        X_mm = read_values(current_line)
        my_file.readline()
        current_line = str(my_file.readline())
        MP_inertia = read_values(current_line)
    counter_line += 1


