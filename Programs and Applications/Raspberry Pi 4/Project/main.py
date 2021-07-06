from threading import Thread

from funcs.ergonomics import start_ergonomics
from funcs.ambient import start_ambient
from funcs.heartbeat import start_hearbeat
from funcs.respiration import start_respiration

# Initialize Ergonomics
# start_ergonomics()
thread_ergonomics = Thread(target=start_ergonomics, args=())
thread_ergonomics.start()

# Initialize Ambient
# start_ambient()
thread_ambient = Thread(target=start_ambient, args=())
thread_ambient.start()

# Initialize Heartbeat
thread_i2c = Thread(target=start_hearbeat, args=())
thread_i2c.start()

# Initialize Respiration
thread_i2c = Thread(target=start_respiration, args=())
thread_i2c.start()

# Celebrate
" (ɔ◔‿◔)ɔ ♥ "
