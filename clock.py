# from apscheduler.schedulers.blocking import BlockingScheduler
import main
import time
# sched = BlockingScheduler()

# @sched.scheduled_job('interval', seconds = 30)
def run():
    main.runner()
    time.sleep(30000)

# sched.start()
