import datetime
import pause

from src.utils.date_utils import DateUtils

time_string = "173000"
target_time = DateUtils.get_target_time(time=time_string, seconds_before=60)

# Use pause to wait until target time
pause.until(target_time)

print("60 seconds before", time_string)
print(datetime.datetime.now())
