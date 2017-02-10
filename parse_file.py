file = 'config'

with open(file) as f:
    for line in f:
        if 'qy_access_key_id' in line:
            print line.split()[-1]
        elif 'qy_secret_access_key' in line:
            print  line.split()[-1]
        elif 'zone' in line:
            print  line.split()[-1]
