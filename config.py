from getpass import getpass
import my_pass


# type the query you want to find
search = 'like'


# to change the limit of 50 GET/hour to 5000 GET/hour by GithubApi
# input here you Github login and password in string type
# or you can use getpass to type your password every time you use GET to Api
# just choose what you want and the another comment with the '#'
login = 'tuipik'
password = my_pass.password
# password = getpass.getpass()

auth = (login, password)

# number of Threads to download avatars
ava_threads = 3

# number of Threads to compose collage
collage_threads = 3