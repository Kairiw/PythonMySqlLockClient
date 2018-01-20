# PythonMySqlLockClient
Simple locking client for python using MySQL named locks


Exampe usage
```bash
python example.py --host localhost --port 3306 --username $USER --lock_name test_lock
Enter your mysql password
Password: 
Successfully acquire lock: test_lock
We acquired the lock
Successfully release lock
Successfully released our lock
```