from apscheduler.schedulers.blocking import BlockingScheduler
import main
sched = BlockingScheduler()

@sched.scheduled_job('interval', seconds = 30)
def run():
    main.runner()

sched.start()
