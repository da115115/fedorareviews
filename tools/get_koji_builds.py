#!/usr/bin/env python
# Provide script with a package_name, version, and tag_name and it will 
# search through all current koji packages for successful build information.
# The process is not very efficient, first it checks the package for the 
# build_id, then it checked the build id for the task_id, and finally, it
# checks the task_id to check if it successfully built.


import koji, optparse
from operator import itemgetter

usage = 'usage: %prog [options] package_name release'
parser = optparse.OptionParser(usage=usage)
(options, args) = parser.parse_args()


class checkKojiPackage:
    def __init__(self):
		if len(args) > 2 or len(args) < 2:
			parser.error('Provide a package_name and a distribution release such as: fc17, fc18, el5, el6')
		package_name = str(args[0])
		package_release = str(args[1])
		build_report = self.checkPackage(package_name, package_release)
		print "\nBuild report:\n" + str(build_report)
       
    # Loop through koji servers and check if package exists, extract the the task_id
    def checkPackage(self, package_name, package_release):
		tag_name = 'f17-final'
		server = "http://koji.fedoraproject.org/kojihub/"
		session = koji.ClientSession(server)
		tables = session.queryHistory(package=package_name)
		build_report = []
		#print histdata
		for table in tables:
			build = tables[table]
			pre_release = 0
			for x in build:
				if 'release' in x:
					build_status = {}
					build_release = (x['release'].split('.'))[1]
					if package_release == build_release:
						build_version = x['version']
						build_id = x['build_id']
						build_tag = x['tag.name']
						build_status ['build_id'] = build_id
						build_status ['version'] = build_version
						build_status ['tag'] = build_tag
						#print "\nx: " + str(x)
						build_url = "http://koji.fedoraproject.org/koji/buildinfo?buildID=" + str(build_id)
						build_report.append (build_status)
						#print "\n" + build_url + " (version: " + str(build_version) + ", tag: " + build_tag + ")"
        # End of for statement
		build_report_sorted = sorted (build_report, key=itemgetter('version'), reverse=True)
		return build_report_sorted

if __name__ == '__main__':
    checkKojiPackage()

