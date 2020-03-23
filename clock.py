from apscheduler.schedulers.blocking import BlockingScheduler

import main
# from time import sleep
from os import getenv
from dotenv import load_dotenv
load_dotenv()
sched = BlockingScheduler()

@sched.scheduled_job('interval', seconds = int(getenv('REFRESH_SEC')))
def run():
    print(getenv('REFRESH_SEC'))
    main.runner()
    # sleep(int(getenv('REFRESH_SEC')))

sched.start()
