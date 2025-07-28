import argparse
from platform import system
from subprocess import call

def ping(address, count):
    flag = '-n' if system() == 'Windows' else '-c'
    commandToRun = ['ping', flag, count, address]
    result = call(commandToRun)
    return result

def traceroute(address, max, resolve):
    if max <= 30:
        maxFlag = '-h'
    elif max >= 30:
        exit(1)
    elif max == 30:
        maxFlag = ''
    else:
        maxFlag = ''
    if resolve is True:
        resolveFlag = '-d'
        commandToRun = ['tracert', resolveFlag, maxFlag, str(max), address]
        result = call(commandToRun)
    else:
        commandToRun = ['tracert', maxFlag, str(max), address]
        result = call(commandToRun)
    return result

def main():
    parser = argparse.ArgumentParser(prog='debug-tool.py',
                                     description='A Debugging Tool for Network Troubleshooting.',
                                     epilog='End of the help text.')
    subParser = parser.add_subparsers(title='subcommands', help='sub-command help', dest='command', required=True)
    # Ping command
    ping_parser = subParser.add_parser('ping', aliases=['p'], help='Pings a host using standard ping application.')
    ping_parser.add_argument('ip', type=str, help='IPv4 Address in the notation of X.X.X.X', default='127.0.0.1')
    ping_parser.add_argument('-c', '--count', metavar='N', type=int, default=4, help='Number of times to ping the host.')
    ping_parser.add_argument('-l', '--size', metavar='M', type=int, default=64, help='Size of each packet.')
    ping_parser.add_argument('-t', action='store_true', required=False, help='Ping the specified host until stopped.')
    # Traceroute command
    trace_parser = subParser.add_parser('traceroute', aliases=['tr'], help='Traceroute to a host.')
    trace_parser.add_argument('ip', type=str, help='IPv4 Address in the notation of X.X.X.X', default='127.0.0.1')
    trace_parser.add_argument('-d', help='Do not resolve addresses to hostnames.', required=False, action='store_true', dest='resolve')
    trace_parser.add_argument('-m', '--maximum-hops', metavar='N', dest='max', default=30, type=int, required=False, help='Maximum number of hops to search for target.')

    arguments = parser.parse_args()

    if arguments.command in ['ping', 'p']:
        ping(arguments.ip, str(arguments.count))
    elif arguments.command in ['traceroute', 'tr']:
        traceroute(arguments.ip, arguments.max, arguments.resolve)

    print("\nFinished - Exiting.")


if __name__ == "__main__":
    main()
