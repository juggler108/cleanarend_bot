import aiogram
assert aiogram.__version__.split('.')[0] == '3', 'Current module requires aiogram package version 3.x.x'

from core.aiogram3_calendar.simple_calendar import SimpleCalendarCallback as simple_cal_callback, SimpleCalendar
