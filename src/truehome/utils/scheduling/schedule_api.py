from truehome.utils.scheduling.at.wrapper import At


def get_scheduled_jobs():
    return _get_at_jobs()


def add_scheduled_task(controller_id, target_state, when, onetime=True, **kwargs):
    pass


def _get_cron_jobs():
    pass


def _get_at_jobs():
    return At.list_jobs()


def delete_at_job(job_id):
    return At.delete_job(job_id)


def delete_cron_job():
    pass