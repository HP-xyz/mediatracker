__author__ = 'heinrich.potgieter@gmail.com'

import logging
import unittest

from src.core.daemon import Daemon


class MyTestCase(unittest.TestCase):
    def setUp(self):
        logging.basicConfig(
            filename='MediaTracker.log',
            level=logging.DEBUG,
            format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
            datefmt='%m-%d %H:%M',
            filemode='a')
        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '%(name)-12s: %(levelname)-8s %(message)s')
        console.setFormatter(formatter)
        logging.getLogger('').addHandler(console)

    def test_daemon_can_start(self):
        daemon = Daemon.Daemon()
        daemon.run()


if __name__ == '__main__':
    unittest.main()
