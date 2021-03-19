# WebParser.py - v1
# 
# Simple WebURL parser that has mild issues
# It will take a txt file of web addresses you supply it via a command prompt argument
# It will then spit it out into an output file for you, seperating web domains that will be manually blocked
# and entire top-level-domains.
# 
# Purpose was to build and update firewall lists with an easy script
import sys;

class WebURLParser(object):
	
	# Change these as needed

	# Variables; supply without a dot (period)
	TopLevelDomainListing = []; # Will Auto Supply; however you can enter TLDs here manually if desired
	TopLevelDomainExcept  = [ "com", "net", "org", "edu", "gov" ]; # Enter TLDs here to exclude them from being mass blocked
	DomainListing		  = []; # Used to track domains, this will auto-populate 

	def __init__(self, fname):
		with open( fname, "r" ) as reader, open( "output-" + fname, "w" ) as writer:
			for url in reader:
				try:
					url = self.seperationTesting(url);
					if (type(url) == None) or (url == "*."):
						continue;
					elif url in self.DomainListing:
						continue;
					else:
						self.DomainListing.append(url)
				except TypeError:
					continue;
			writer.write(("# Top-Level Domain Blockers\n{}\n\n# Websites\n{}".format("\n".join([("*." + x) for x in sorted(self.TopLevelDomainListing)]), "\n".join([x for x in sorted(self.DomainListing)]))))

	def __str__(self):
		return("# Top-Level Domain Blockers\n{}\n\n# Websites\n{}".format("\n".join([("*." + x) for x in sorted(self.TopLevelDomainListing)]), "\n".join([x for x in sorted(self.DomainListing)])));

	def seperationTesting(self, url): # Parse URL

		# If NoneType, break function and continue loop
		if type(url) == None:
			raise TypeError;

		# Remove / Ignore Comments
		if "#" == url[0]:
			raise TypeError;

		# Remove URL Wrapper Text
		parsedURL = url.strip().split( ":" ); # Splits Wrapper

		# Remove HTTP, HTTPS
		try:
			if ("http" in parsedURL[0]) and ("//" in parsedURL[1][0:2]): # Attempts to ensure that an HTTP wrapper does exist
				parsedURL.pop( 0 ); # Pops the HTTP out, and moved the list up by 1
				if "//" == parsedURL[0:2]: #Removes two '/' from the beginning of string
					parsedURL[0] = parsedURL[0][2:];
		except IndexError:
			pass;

		# Check if the TLD is already accounted for, otherwise add it
		if not (parsedURL[0].split( "." )[-1]).split("/")[0].lower() in self.TopLevelDomainListing:
			if not (parsedURL[0].split( "." )[-1]).split("/")[0].lower() in self.TopLevelDomainExcept:
				if not (parsedURL[0].split( "." )[-1]).split("/")[0] == "":
					self.TopLevelDomainListing.append((parsedURL[0].split( "." )[-1]).split("/")[0].lower());
				raise TypeError;
		
		if (parsedURL[0].split( "." )[-1]).split("/")[0].lower() in self.TopLevelDomainListing:
			raise TypeError;


		# Change these as needed

		# Returns domain with a wildcard
		return "*." + ".".join(parsedURL[0].split( "." )[-2:]);
  
		# Returns full domain without the specific file location
		# return ".".join(parsedURL.split( "/" )[0]);
    
		# Returns the URL provided
		# return url.strip();
		

if __name__ == "__main__":
	WebURLParser(sys.argv[1]);
