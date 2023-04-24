
class Output:

    def __init__(self):
        pass

    # Takes data generated from user's reg.py command and returns
    # formatted output to return to client
    def to_cli(self, db_output):
        db_output.sort(key=lambda x: (x[1], x[2]))

        courses = []
        for row in db_output:
            courses.append('{:>5} {:>4} {:>6} {:>4} {}'.format(
                row[0], row[1], row[2], row[3], row[4]))

        return courses

    # Takes data generated from user's regdetails.py command and
    # returns formatted output to return to client
    def courseid(self, db_output):
        info = ''
        # Print all standard info
        info += ('Course Id: {}'.format(db_output[0][0][0]))+'\n'
        info += '\n'
        info += (('Days: {}'.format(db_output[0][0][1]))
             + (' ' if not db_output[0][0][1] else ''))+'\n'
        info += (('Start time: {}'.format( db_output[0][0][2]))
            + (' ' if not db_output[0][0][2] else ''))+'\n'
        info += (('End time: {}'.format(db_output[0][0][3]))
            + (' ' if not db_output[0][0][3] else ''))+'\n'
        info += (('Building: {}'.format(db_output[0][0][4]))
            + (' ' if not db_output[0][0][4] else ''))+'\n'
        info += (('Room: {}'.format(db_output[0][0][5]))
            + (' ' if not db_output[0][0][5] else ''))+'\n'
        info += '\n'
        # Print all department and numbers
        for dept_num in sorted(db_output[2]):
            info += (('Dept and Number: {} {}'.format(
                dept_num[0], dept_num[1])))+'\n'
        info += '\n'
        info += (('Area: {}'.format(db_output[0][0][8]))
         + (' ' if not db_output[0][0][8] else ''))+'\n'
        info += '\n'
        info += ((
            'Title: {}'.format(db_output[0][0][9])))+'\n'
        info += '\n'
        info += (('Description: {}'.format(
            db_output[0][0][10])))+'\n'
        info += '\n'
        info += (('Prerequisites: {}'.format(
            db_output[0][0][11])))+'\n'
        # Print all professors (if any)
        if len(db_output[1]) > 0:
            info += '\n'
            for prof in sorted(db_output[1]):
                info += (('Professor: {}'.format(
                    prof[0])))+'\n'
        else: info += '\n'

        return info
