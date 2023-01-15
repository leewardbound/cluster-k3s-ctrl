# Rclone Backup Scheme for Cloud Services

This helper script provides kubernetes cronjob entrypoints for the following backup lifecycle tasks:

+ Sync some remote services (GDrive, GPhotos) to a ceph-block PVC to form a "personal datalake"

+ Generate metadata file with the sync success and stats backup metadata per-service (last modified timestamp, total backup size, and list of large folders)

+ Weekly Slack checkin with a summary of the sync events in the last 7 days
