# -*- coding: UTF-8 -*-
#!/usr/bin/env python3
#DNSHEALTH-12
import dns.resolver
from dns.exception import DNSException
import src.checks.check_helpers as helpers

def DESCRIPTION():
    return "Checking for authoritative answers"

def answer_authoritatively(domain, name_servers,ipv6):

    for server in name_servers:
        
        ip = helpers.getTheIPofAServer(server,ipv6,DESCRIPTION())

        if ip["result"] == False:
            return ip

        try:

            var = dns.message.make_query(domain,dns.rdatatype.SOA)

            response = dns.query.udp(var, ip["result"])
            
        
        except DNSException as e:
            
            return {"result": False,"description" : DESCRIPTION(), "details": e.msg}

        if len(response.answer) == 0:
            return {"result": False ,"description": DESCRIPTION(), "details": "Resolved 0 authoritative servers"}

    return {"result": True,"description": DESCRIPTION() ,"details": "Successfully validated authoritative answers"}

def run(domain, list_of_name_servers,ipv6):
    return answer_authoritatively(domain,list_of_name_servers,ipv6)
