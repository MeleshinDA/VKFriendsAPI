import argparse

from VKUserData import VKUserData


def main():
    parser = argparse.ArgumentParser(description='Based')
    parser.add_argument("-user", dest="user", help='userId, который будет сканироваться', required=True)
    parser.add_argument("-token", dest="token", help='Токен доступа к профилю', required=True)
    args = parser.parse_args()

    vkUser = VKUserData(args.user, args.token)
    vkUser.print_user_info()


if __name__ == '__main__':
    main()
