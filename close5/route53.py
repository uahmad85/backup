response = client.change_resource_record_sets(
        HostedZoneId = 'Z5BUHHSE7FRA3',
        ChangeBatch={
            'Comment': 'comment',
            'Changes': [
                {
                    'Action': 'CREATE',
                    'ResourceRecordSet': {
                        'Name': 'testing12345123.staging.close5.com',
                        'Type': 'A',
                        'SetIdentifier': 'staging',
                        'GeoLocation': {},
                        'TTL': 60,
                        'ResourceRecords': [
                            {
                                'Value': '10.10.10.10'
                            },
                        ],
                    }
                },
            ]
        }
)
