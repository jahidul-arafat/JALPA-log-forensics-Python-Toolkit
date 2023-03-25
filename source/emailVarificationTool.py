import re
import smtplib
import dns.resolver
#if dns.resolver does not working use: pip install --upgrade dnspython

def emailValidityChecker(emailAddessesToBeChecked):
    # Address used for SMTP MAIL FROM command
    fromAddress = 'corn@bt.com'
    #emailAddessesToBeChecked=["jahidapon@gmail.com","jahid.gmail.com","duki@duki.com","jarafat@baiust.edu.bd"]
    addressValidityDict={}
    # Simple Regex for syntax checking whether any invalid email address remains
    regex = '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,})$'

    # Email address to verify
    emailCounter=1
    for email in emailAddessesToBeChecked:
        #print("\n")
        #inputAddress = input('Please enter the emailAddress to verify:')
        #addressToVerify = str(inputAddress)
        print("Counter: {} Email Verifying: {}".format(emailCounter,email))
        #print("------------------------------------------")
        emailCounter+=1
        addressToVerify=email

        # Syntax check
        match = re.match(regex, addressToVerify)
        if match == None:
            status="Bad Syntax"
            addressValidityDict[addressToVerify]=status
            #print(status)
            continue
        	#raise ValueError(status)

        # Get domain for DNS lookup
        splitAddress = addressToVerify.split('@')
        domain = str(splitAddress[1])
        #print('Domain:', domain)

        # MX record lookup
        records = dns.resolver.query(domain, 'MX')
        mxRecord = records[0].exchange
        mxRecord = str(mxRecord)



        # SMTP lib setup (use debug level for full output)
        server = smtplib.SMTP()
        server.set_debuglevel(0)

        # SMTP Conversation
        try:
            server.connect(mxRecord)
        except:
            status="DNS refused"
            addressValidityDict[addressToVerify]=status
            #print(status)
            continue


        server.helo(server.local_hostname) ### server.local_hostname(Get local server hostname)
        server.mail(fromAddress)
        code, message = server.rcpt(str(addressToVerify))
        server.quit()

        #print(code)
        #print(message)

        # Assume SMTP response 250 is success
        if code == 250:
            status="Success"
            #print('Success')
        else:
            status="invalid username"
            #print(status)
        addressValidityDict[addressToVerify]=status
    #---------------end of for loop-------------

    #print (addressValidityDict)
    return addressValidityDict

def main():
    emailAddessesToBeChecked=["jahidapon@gmail.com","jahid.gmail.com","duki@duki.com",
    "jarafat@baiust.edu.bd","foo123@gmail.com","foo123@google.com"]
    statusDict=emailValidityChecker(emailAddessesToBeChecked)

if __name__ == '__main__':
  main()

