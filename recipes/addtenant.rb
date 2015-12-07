Chef::Log.info("CUSTOM PARAMS  tenantid: #{node['tenantid']} agentIP #{node['agent_ip']} visitorIP #{node['visitor_ip']} RCI_IP #{node['rci_ip']}")

tenantid = node['tenantid']
agentip = node['agent_ip']
visitorip = node['visitor_ip']
rciip = node['rci_ip']

if tenantid && agentip && vistiorip && rciip
	cookbook_file "/tmp/test.py" do
	  source "test.py"
	  mode 0755
	end

	execute "install my lib" do
	  command "sudo python /tmp/test.py #{tenantid} #{agentip} #{visitorip} #{rciip}"
	end
end