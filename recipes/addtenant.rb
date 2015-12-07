Chef::Log.info('I am a message from the #{recipe_name} recipe in the #{cookbook_name} cookbook.')

cookbook_file "/tmp/test.py" do
  source "test.py"
  mode 0755
end

execute "install my lib" do
  command "sudo /tmp/test.py"
end