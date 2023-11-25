# manage.py


import unittest
import redis
from flask.cli import FlaskGroup
from rq import Connection, Worker
from flask import request

from project.server import create_app
# from project.server.main.tasks import create_export_task
# from project.server.main.test.test_app_module import test_export_module
from project.server.main.test.test_app_module import test_app_module
from project.server.main.test.test_auth_module import test_auth_module
from project.server.main.test.test_forgotpassword_module import test_forgot_password_module
from project.server.main.test.test_register_module import test_register_module
from project.server.main.test.test_transaction_module import test_transaction_module
from project.server.main.test.test_transactionlist_module import test_transaction_list_module

import logging
import traceback
from time import strftime


app = create_app()
cli = FlaskGroup(create_app=create_app)

@cli.command()
def test():
    """Runs the unit tests without test coverage."""
    tests = unittest.TestLoader().discover("project/tests", pattern="test*.py")
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@cli.command("run_worker")
def run_worker():
    redis_url = app.config["REDIS_URL"]
    redis_connection = redis.from_url(redis_url)
    with Connection(redis_connection):
        worker = Worker(app.config["QUEUES"])
        worker.work()

# @cli.command("github_push")
# def github_push():
#     create_export_task(43591000)

@cli.command("export_test")
def export_test():
    test_app_module()
    test_auth_module()
    test_forgot_password_module()
    test_register_module()
    test_transaction_module()
    test_transaction_list_module()


if __name__ == "__main__":
    cli()
