import MySQLdb

class LockClient(object):


    def __init__(self, host, port, user, passwd, lock_name, timeout=-1):

        self.username = user
        self.password = passwd
        self.mysql_host = host
        self.mysql_port = port
        self.lock_name = lock_name

        """
        We default the timeout to -1 for an infinite lock
        If an infinite lock is used the lock is only released if the connection terminates
        """
        self.lock_timeout = timeout

        self.mysql_connection = self._setupMySqlConnection()

    def _setupMySqlConnection(self):

        # This will raise an OperationError exception if one of the parameters is incorret
        return MySQLdb.connect(host=self.mysql_host, passwd=self.password, user=self.username, port=self.mysql_port)


    def aquireLock(self):

        cursor = self.mysql_connection.cursor()

        # First lets check if the the lock is free
        cursor.execute("SELECT IS_FREE_LOCK('{}')".format(self.lock_name))

        # IS_FREE_LOCK will return 0 if the lock is in use, 1 if the lock is free, or NULL for an error
        result = cursor.fetchone()
        if result[0] == 0:
            # lock is in use
            print "Lock is currently in use"
            return False
        elif result[0] == 1:
            # Lock is free attempt to acquire it
            cursor.execute("SELECT GET_LOCK('{}', {})".format(self.lock_name, self.lock_timeout))
            lock_result = cursor.fetchone()
            if lock_result[0] == 0:
                # Lock attempt failed
                print "Failed to acquire lock"
                return False
            elif lock_result[0] == 1:
                # Locked
                print "Successfully acquire lock: {}".format(self.lock_name)
                return True
            else:
                # Error occurred
                print "An error occurred will trying to acquire lock"
                return False
        else:
            # NULL return
            print "Unable to check lock status"
            return False

    def releaseLock(self):

        cursor = self.mysql_connection.cursor()

        cursor.execute("SELECT RELEASE_LOCK('{}')".format(self.lock_name))

        result = cursor.fetchone()

        # The release lock will return 0 if our connection doesn't own the lock, 1 if it is released, and null if the lock doesn't exist

        if result[0] == 0:
            print "we don't own the lock, couldn't release"
            return False
        elif result[0] == 1:
            print "Successfully release lock"
            return True
        else:
            print "Named lock: {} doesn't exist".format(self.lock_name)
            return False
