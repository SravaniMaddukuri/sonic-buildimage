#!/usr/bin/env bash

rm -f /var/run/rsyslogd.pid

supervisorctl start rsyslogd

supervisorctl start syncd

supervisorctl start mlnx-sfpd

