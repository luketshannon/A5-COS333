import sys
import socket
import pickle
import reg_db
import cli_input


# If query about which courses to display
# Returns list of courses that match search in the following form:
#(0, err_message) or (1, courses)
def get_courses(args):
    d_b = reg_db.Database()
    response = d_b.query_cli(args)
    # Add database error handlijg
    #print(response)
    if not response[0]:
        # If error in accessing database
        err = sys.argv[0] + ': ' + str(response[1])
        print(err, file=sys.stderr) #test this****
        return (0, 'A server error occurred. '+
        'Please contact the system administrator.')
    return (1, response[1])


# If query about details of specific courses
# Returns course details that match coursenum in the following form:
#(0, err_message) or (1, courses)
def get_dets(args):
    # use regdetials.py
    d_b = reg_db.Database()
    response = d_b.query_classid(args)
    if not response[0]:
        # If error in accessing database
        err = sys.argv[0] + ': ' + str(response[1])
        print(err, file=sys.stderr) #test this****
        return (0, 'A server error occurred. '
        + 'Please contact the system administrator.')
    if len(response[1][0]) == 0:
        err = sys.argv[0] + ': classid does not exist'
        print(err, file=sys.stderr) #test this****
        return (0, 'classid does not exist')
    return (1, response[1])


# Recieve call from reg.py
def main():
    user_input = cli_input.Input()
    user_input.parse_cli_server(sys.argv[1:])

    try:
        with socket.socket() as server_sock:
            print("Opened server socket.socket")
            host = ''
            port = int(sys.argv[1])

            server_sock.bind((host, port))
            print("Bound server socket.socket to port")
            server_sock.listen(1)
            print('Listening')

            while True:
                conn, _ = server_sock.accept()
                # try:
                print("Accepted connection, opened socket.socket")
                with conn:
                # Receive a request from the client
                    request_bytes = conn.recv(99999999)
                    request = pickle.loads(request_bytes)

                # Process the request
                    if request['type'] == 'courses':
                        print('Received command: get_overviews')
                        response = get_courses(request['info'])
                        #db = reg_db.Database()
                        #response = db.query_cli(request['info'])
                    else:
                        print('Received command: get_detail')
                        # response = get_dets(request[12345])
                        # print(1)
                        response = get_dets(request['info'])
                        #db = reg_db.Database()
                        #response = db.query_classid(request['info'])
                        #if len(response) == 0:
                            #err = argv[0] + ': classid does not exist'
                            #print(err, file=sys.stderr) #test this****

                # Send a response to the client
                    response_bytes = pickle.dumps(response)
                    conn.sendall(response_bytes)
                print('Closed socket.socket')
                # finally:
                # # Close the connection
                #     conn.close()

    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
