Chef::Log.info("CUSTOM PARAMS  tenantid: #{node['tenantid']} agentIP #{node['agent_ip']} visitorIP #{node['visitor_ip']} RCI_IP #{node['rci_ip']}")

cookbook_file "/tmp/test.py" do
  source "test.py"
  mode 0755
end

execute "install my lib" do
  command "sudo python /tmp/test.py"
end