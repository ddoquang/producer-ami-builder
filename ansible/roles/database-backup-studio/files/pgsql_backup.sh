#!/bin/sh
# backup all databases of PgSQL Server
# Mathieu Lavigne 2020-08-05
# --->  set permissions to 700 for postgres to run as cron

umask 077
DUMP=/bin/pg_dumpall
startdate=`date "+%Y-%m-%d-%H%M%S"`

### Variables (Contant)
LOGFILE=/var/lib/pgsql/12/cron/log/${startdate}

(
echo Backuping PgSQL on ${HOSTNAME}
echo
echo startdate ${startdate}
echo uptime `uptime`
echo
BACKUPD=/backups/pgsql/${startdate}
mkdir $BACKUPD

  BACKUPF=$BACKUPD/${startdate}
  echo $DUMP -c > $BACKUPF
  echo start `date "+%y%m%d%H%M%S"`
  exec 2>&1
($DUMP -c > $BACKUPF)
 gzip $BACKUPF
  echo finish `date "+%y%m%d%H%M%S"`
  echo

echo Done
echo uptime `uptime`
echo enddate `date "+%y%m%d%H%M%S"`

) >$LOGFILE

echo  >> $LOGFILE
echo "Removing backup older then 5 days." >> $LOGFILE
echo  >> $LOGFILE
find /backups/pgsql/* -type d -mtime +5 -exec echo rm -rf {} \; -exec rm -rf {} \; >>$LOGFILE 2>&1

echo "Subject: PgSQL backup log from $HOSTNAME" |\
cat - $LOGFILE | /usr/lib/sendmail -f sysadmin@toonboom.com sysadmin@toonboom.com