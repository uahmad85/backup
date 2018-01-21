aa = [
    {
        "PrefixListIds": [],
        "FromPort": 0,
        "IpRanges": [
            {"CidrIp": "172.31.0.0/16"}, {"CidrIp": "10.0.0.0/8"}],
        "ToPort": 65535,
        "IpProtocol": "tcp",
        "UserIdGroupPairs": [
            {
                "UserId": "712818841314",
                "GroupId": "sg-73be3315"
            },
            {
                "UserId": "712818841314",
                "GroupId": "sg-c063d4a7"}]},
    {
        "PrefixListIds": [],
        "FromPort": 22,
        "IpRanges": [
            {"CidrIp": "216.113.160.72/32"}],
        "ToPort": 22,
        "IpProtocol": "tcp",
        "UserIdGroupPairs": []
    },
    {
        "PrefixListIds": [],
        "FromPort": 27017,
        "IpRanges": [],
        "ToPort": 27017,
        "IpProtocol": "tcp",
        "UserIdGroupPairs": [
            {
                "VpcId": "vpc-43186027",
                "UserId": "712818841314",
                "GroupId": "sg-73a9cf15",
                "VpcPeeringConnectionId": "pcx-df8132b6",
                "PeeringStatus": "active"
            },
            {
                "UserId": "712818841314",
                "GroupId": "sg-8bbe33ed"
            },
            {
                "UserId": "712818841314",
                "GroupId": "sg-9c112dfa"
            },
            {
                "VpcId": "vpc-43186027",
                "UserId": "712818841314",
                "GroupId": "sg-9da8cefb",
                "VpcPeeringConnectionId": "pcx-df8132b6",
                "PeeringStatus": "active"
            }]}]

x = iter(aa)
for i in aa:

print x.next()
print x.next()
print x.next()
