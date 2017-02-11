from datetime import datetime
import subprocess
import sys


def execute_command(command, split_output_lines=False):
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = p.stdout.read()
    output = output.splitlines() if split_output_lines else output
    return_value = p.wait()
    return return_value, output


class AtJob(object):
    def __init__(self, job_id, schedule, command):
        self._job_id = job_id
        self._schedule = schedule
        self._command = command

    @property
    def job_id(self):
        return self._job_id

    @property
    def schedule(self):
        return self._schedule

    @property
    def command(self):
        return self._command

    def to_dict(self):
        data_dict = {
            'job_id': self.job_id,
            'schedule': At.datetime_to_str(self.schedule),
            'command': self.command
        }
        return data_dict


class At(object):
    POSIX_AT_WHEN_FORMAT = '%Y-%m-%d %H:%M'
    DARWIN_AT_WHEN_FORMAT = '%Y-%b-%d %H:%M:%S'

    @classmethod
    def _is_darwin(cls):
        return sys.platform == 'darwin'

    @classmethod
    def _get_at_date_time(cls, at_entry):
        str_format = cls.DARWIN_AT_WHEN_FORMAT if cls._is_darwin() else cls.POSIX_AT_WHEN_FORMAT
        if cls._is_darwin():
            time = at_entry[3]
            date = '{year}-{month}-{day}'.format(year=at_entry[4],
                                                 month=at_entry[1],
                                                 day=at_entry[2])
        else:
            time = at_entry[1]
            date = at_entry[0],
        return cls._str_to_datetime(date, time, str_format)

    @classmethod
    def datetime_to_str(cls, date_time):
        str_format = cls.DARWIN_AT_WHEN_FORMAT if cls._is_darwin() else cls.POSIX_AT_WHEN_FORMAT
        schedule_string = date_time.strftime(str_format)
        return schedule_string

    @classmethod
    def _str_to_datetime(cls, date, time, fmt):
        date_time = datetime.strptime('{date} {time}'.format(date=date,
                                                             time=time), fmt)
        return date_time

    @classmethod
    def _get_jobs_info(cls):
        result = []
        _, atq_output = execute_command('atq', True)
        for job in atq_output:
            job_fields = job.split()
            job_id = job_fields[0]
            when = cls._get_at_date_time(job_fields[1:])
            result.append((job_id, when))
        return result

    @classmethod
    def _get_job_command(cls, job_id):
        at_queue_command = 'at' if cls._is_darwin() else 'atq'
        return_code, atq_output = execute_command('{cmd} -c {job_id}'.format(cmd=at_queue_command,
                                                                             job_id=job_id),
                                                  split_output_lines=True)

        if atq_output:
            return atq_output[-2]
        return None

    @classmethod
    def list_jobs(cls):
        jobs = []
        for job_id, job_schedule in cls._get_jobs_info():
            job_command = cls._get_job_command(job_id)
            if job_command:
                jobs.append(AtJob(job_id=job_id, schedule=job_schedule, command=job_command))
        return [job.to_dict() for job in jobs]

    @classmethod
    def delete_job(cls, job_id):
        return_code, _ = execute_command('atrm {job_id}'.format(job_id=job_id))
        return not return_code  # return code 0 == success

    @classmethod
    def add_job(cls, command, schedule):
        schedule_str = cls.datetime_to_str(schedule)


