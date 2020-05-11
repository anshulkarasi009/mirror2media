def get_username_from_user():
    print('\n\n\n----------------------Twitter Scraping Tool----------------------\n')
    user_list = []
    while(True):
        print('\nEnter twitter username if done press Enter')
        username = input('Username without @:')
        if username == '':
            print('\nyour list of username is ',user_list)
            break
        user_list.append(username)
    return user_list

