# THANK YOU TO https://pentest.co.uk/wp-content/uploads/Avalanche2_Solution.pdf


import werkzeug
from werkzeug.security import check_password_hash
import sys
from multiprocessing import Pool
import time
starttime = time.time()
target = "pbkdf2:sha256:600000$MSok34zBufo9d1tc$b2adfafaeed459f903401ec1656f9da36f4b4c08a50427ec7841570513bf8e57" 

def crack_password(password):
    correct = werkzeug.security.check_password_hash(target, password)
    if correct:
        print("[*] Hash cracked! ({}):{}".format(password, correct))
        print('That took {} seconds'.format(time.time() - starttime)) 
        return True 
    else:
        # Overwrite the printed line to show some status 
        print("[*] Failed ({})".format(password), flush=True)

    return False

def main():
    with open('password_list.txt', 'r') as f:
        passwords = f.read().splitlines()

    with Pool(20) as pool:
        reslist = (pool.imap_unordered(crack_password, passwords))

        pool.close()
        for res in reslist:
            if res:
                pool.terminate()
                break
        pool.join()

if __name__ == '__main__':
    main()