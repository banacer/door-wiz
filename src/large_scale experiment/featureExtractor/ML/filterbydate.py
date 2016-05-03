import sys
from datetime import datetime
import math
def extract(start_date, end_date,fname):
    count = 1
    with open(fname,'r') as f:

        for line in f:
            l = line.rstrip().split(',')
            line_date = datetime.fromtimestamp(math.floor(float(l[0])))
            if start_date <= line_date and line_date <= end_date:
                l[0] = str(line_date)
                print l[1:]

#get python args
cmdargs = str(sys.argv)
try:
    start_date = datetime.strptime(str(sys.argv[1]), '%b %d %Y %I:%M%p')
    end_date = datetime.strptime(str(sys.argv[2]), '%b %d %Y %I:%M%p')
    extract(start_date,end_date,str(sys.argv[3]))
except Exception as ex:
    print 'there was a problem', str(ex)

