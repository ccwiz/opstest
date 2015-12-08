import sys, getopt
import fileinput
import os
import re
from string import Template

def appendToFile(file, data):

	with open(file, "a") as conffile:
		conffile.write(data)
		conffile.close()

def doUpstreamConfig(tenant, ECF_IP, ECF_visitor_IP, RCI_IP):
	upstreamTempl = Template('''
upstream $t{
	server $ecfip:8443;
}                       
upstream ${t}_visitor{
	server $ecfv:8443;
}
upstream ${t}_rci{
	server $rciip:8443;
}
	''')
	
	data = upstreamTempl.safe_substitute(t=tenant, ecfip=ECF_IP, ecfv=ECF_visitor_IP, rciip=RCI_IP)
	return data;

def doLocationConfig(tenant):
	locTempl = Template('''
# redirect based on tenant -> $t  
location ^~ /$t/ {
	location ^~ /$t/RCI {
		location ^~/$t/RCI/rest/tasks/ {
			auth_basic           "restricted";
			auth_basic_user_file /etc/nginx/.htpasswd;
			dav_methods  PUT DELETE;
			proxy_pass https://${t}_rci/RCI/rest/tasks/;
			proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
		}

		#for RCI allow PUT DELETE
		dav_methods  PUT DELETE;
		proxy_pass https://${t}_rci/RCI/;
		proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
	}
			
	location ^~/$t/visitor/ {
		# redirect based on yaas tenant  - visitor side
		proxy_pass https://${t}_visitor/;
		#for websocket
		proxy_http_version 1.1;
		proxy_set_header Upgrade $http_upgrade;
		proxy_set_header Connection $connection_upgrade;
		proxy_cookie_path /ecfs/ /$t/visitor/ecfs/;
		proxy_read_timeout 90s; #Atmosphere heart beat is by default 60sec
		proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
	}
			
	proxy_pass https://${t}/;
	#for websocket
	proxy_http_version 1.1;
	proxy_set_header Upgrade $http_upgrade;
	proxy_set_header Connection $connection_upgrade;
	proxy_cookie_path /ecfs/ /$t/ecfs/;
	proxy_read_timeout 90s; #Atmosphere heart beat is by default 60sec
	proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
}
	''')
	
	data = locTempl.safe_substitute(t=tenant)
	return data;	
	
def main(argv):
		
	#print ("Dir to perform Search-Replace on:")
	try: tenant = sys.argv[1]
	except:
		print ("give tenant id:")
		tenant = raw_input( "> " ) 
		pass
	try: ECF_IP = sys.argv[2]
	except:
		print ("ECF IP address:")
		ECF_IP = raw_input( "> " ) 
		pass
	try: ECF_visitor_IP = sys.argv[3]
	except: 
		print ("Visitor ECF address:")
		ECF_visitor_IP  = raw_input( "> " )
		pass
	try: RCI_IP = sys.argv[4]
	except: 
		print ("RCI address:")
		RCI_IP = raw_input( "> " )
		pass
	
	
	print tenant
	print ECF_IP
	print ECF_visitor_IP
	print RCI_IP
	#data = doUpstreamConfig(tenant, ECF_IP, ECF_visitor_IP, RCI_IP)
	filename = "/etc/nginx/sites-available/locations.conf"
	data = doLocationConfig(tenant)
	appendToFile(filename, data)
	filename = "/etc/nginx/conf.d/upstreams.conf"
	data = doUpstreamConfig(tenant, ECF_IP, ECF_visitor_IP, RCI_IP)
	appendToFile(filename, data)

if __name__ == "__main__":
	main(sys.argv[1:])