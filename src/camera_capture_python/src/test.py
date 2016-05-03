import datetime
from datetime import datetime
d =  datetime.now()

file_name = d.strftime("%m-%d-%y_%H")
hour = d.strftime("%H")
print hour
file_name = file_name + ".avi"
print file_name

