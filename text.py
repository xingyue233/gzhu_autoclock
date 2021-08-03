import re
from login import login
from clock import clock_in

res = login('2006100062', '257314')
clock_in(res[0],'2006100062','1057072764@qq.com')
