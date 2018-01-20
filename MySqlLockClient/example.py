from mysqlLockClient import LockClient

import argparse
import getpass
import sys

parser = argparse.ArgumentParser()
parser.add_argument("--host", help="mysql database hostname")
parser.add_argument("--port", type=int, help="mysql database port")
parser.add_argument("--username", help="mysql username")
parser.add_argument("--lock_name", help="named lock to acquire")

def main():

    args = parser.parse_args()

    print "Enter your mysql password"
    password = getpass.getpass()

    lock_client = LockClient(host=args.host, port=args.port, user=args.username, passwd=str(password), lock_name=args.lock_name)

    if lock_client.aquireLock():
        print "We acquired the lock"
    else:
        print "The lock is in use or an error occurred, exiting...."
        sys.exit(1)

    if lock_client.releaseLock():
        print "Successfully released our lock"
        sys.exit(0)
    else:
        print "Failed to release lock"
        sys.exit(1)

if __name__ == '__main__':
    main()
