#!/usr/bin/python

import boto3
import argparse
import datetime

parser = argparse.ArgumentParser(description='Usage: to keep backups for n number of days --days <number of days>')
parser.add_argument('-d', '--days', action='store', type=int, help='number of days')
parser.add_argument('-H', '--hours', action='store', type=float, help='number of hours')
results = parser.parse_args()


time_to_keep_snap = 1000
volumes = ['vol-305de3f0']
today = datetime.datetime.now().strftime('%s')

if results.hours:
    time_to_keep_snap = (float(results.hours) * 60 * 60)

if results.days:
    time_to_keep_snap = float(results.days) * (24 * 60 * 60)


def create_snap(volume_id):
    ec2_client = boto3.client('ec2')
    ec2_client.create_snapshot(DryRun=False,
                               VolumeId=volume_id,
                               Description="backup-snapshot")


def remove_snap(snapshot_id):
    ec2 = boto3.resource('ec2')
    snap = ec2.Snapshot(snapshot_id)
    snap.delete()


# find and remove snapshots older then x number of days.
def get_snapshots(volume_id):
    count = 0
    snap_list = []
    ec2_client = boto3.client('ec2')
    snapshots = ec2_client.describe_snapshots()
    for snap in snapshots['Snapshots']:
        if snap['VolumeId'] == volume_id:
            count += 1
            print "SnapshotId: %s" % snap['SnapshotId']
            if (int(today) - int(snap['StartTime'].strftime('%s'))) >= time_to_keep_snap:
                snap_list.append(snap["SnapshotId"])

    print "Total SnapShots: %s" % count
    return snap_list

# create snapshot
for volume in volumes:
    volume_id = volume
    create_snap(volume_id)
    snapshot_id = get_snapshots(volume_id)
    for ids in snapshot_id:
        remove_snap(ids)
