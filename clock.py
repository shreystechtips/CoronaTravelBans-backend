from apscheduler.schedulers.blocking import BlockingScheduler
import main
sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=3)
def run():
    main.runner()

sched.start()
