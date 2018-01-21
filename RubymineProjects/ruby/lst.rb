Ohai.plugin(:Node_role) do
  provides 'node_role'

  id=`curl http://169.254.169.254/latest/meta-data/instance-id`


  collect_data(:default) do
    node_role = Mash.new
    tag = shell_out('aws ec2 describe-instances --instance-id #{id} | jq .Reservations[].Instances[].Tags[].Value')
    if tag
        node_role[:node_role] = tag
    end
  end
end