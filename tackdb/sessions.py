import sys
from tackdb.views import DataView, RootViewException


def db_session(input_lines):
    view = DataView()

    for line in input_lines:
        cmd, args = parse_command(line)
        
        if cmd == "end":
            break
        
        view, out = execute(view, cmd, *args)
        yield out

def parse_command(command_string):
    split = command_string.split()
    return (split[0].lower(), split[1:])


def execute(view, command, *args):
    if command == "get":
        try:
            return view, view.GET(*args)
        except:
            return view, "NULL"
    
    elif command == "set":
        view.SET(*args)
        return view, None

    elif command == "unset":
        view.UNSET(*args)
        return view, None

    elif command == "numequalto":
        return view, str(view.NUMEQUALTO(*args))

    elif command == "begin":
        return view.BEGIN(), None

    elif command == "rollback":
        try:
            last_view = view.ROLLBACK()
            return last_view, None
            
        except RootViewException:
            return view, "NO TRANSACTION"
    
    elif command == "commit":
        try:
            root_view = view.COMMIT()
            return root_view, None

        except RootViewException:
            return view, "NO TRANSACTION"

    else:
        return view, "INVALID COMMAND: {}".format(command)


def stdin_lines():
    while True:
        cmd = sys.stdin.readline()
        if cmd == '':
            break
        else:
            yield cmd


def main():
    for out in db_session(stdin_lines()):
        if out is not None:
            print(out)

if __name__ == "__main__":
    main()
