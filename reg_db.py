import contextlib
import sqlite3

DATABASE_URL = 'file:reg.sqlite?mode=ro'

class Database:

    def __init__(self):
        pass

    def query(self, stmt_str, args):
        try:
            with sqlite3.connect(DATABASE_URL,
            isolation_level=None, uri=True) as connection:
                with contextlib.closing(connection.cursor()) as cursor:
                # Create a prepared statement and substitute values.
                    cursor.execute(stmt_str, args)
                    table = cursor.fetchall()
                    return (1, table)
        except Exception as ex:
            return (0, ex)
            #print(ex, file=sys.stderr)
            #sys.exit(1)

    def query_cli(self, parsed_args):
        stmt_str = "SELECT classes.classid, crosslistings.dept, "
        stmt_str += "crosslistings.coursenum, courses.area, "
        stmt_str += "courses.title "
        stmt_str += "FROM classes, courses, crosslistings "
        stmt_str += "WHERE classes.courseid=crosslistings.courseid "
        stmt_str += "AND classes.courseid=courses.courseid "

        #NEW
        special_char = '#'

        if parsed_args['d']:
            stmt_str += "AND crosslistings.dept "
            stmt_str += "LIKE ? ESCAPE \'#\'"
        if parsed_args['n']:
            stmt_str += "AND crosslistings.coursenum "
            stmt_str += "LIKE ? ESCAPE \'#\'"
        if parsed_args['a']:
            stmt_str += "AND courses.area "
            stmt_str += "LIKE ? ESCAPE \'#\'"
        if parsed_args['t']:
            stmt_str += "AND courses.title "
            stmt_str += "LIKE ? ESCAPE \'#\'"

        args = tuple ('%' + arg
            .replace('#', '##')
            .replace('%', special_char+'%')
            .replace('_', special_char+'_')
            .replace('\'', special_char+'\'') +
                '%' for arg in
            [parsed_args['d'], parsed_args['n'],
            parsed_args['a'], parsed_args['t']]
            if arg)
        return self.query(stmt_str, args)

    def query_classid(self, classid):
        args = [classid]

        stmt_str = "SELECT classes.courseid, days, starttime, endtime, "
        stmt_str += "bldg, roomnum, dept, coursenum, area, "
        stmt_str += "title, descrip, prereqs "
        stmt_str += "FROM classes, courses, crosslistings "
        stmt_str += "WHERE classes.courseid = courses.courseid "
        stmt_str += "AND classes.courseid = crosslistings.courseid "
        stmt_str += "AND classes.classid = ?"

        prof_stmt_str = "SELECT profname "
        prof_stmt_str += "FROM classes, coursesprofs, profs "
        prof_stmt_str += "WHERE classes.courseid = "
        prof_stmt_str += "coursesprofs.courseid "
        prof_stmt_str += "AND coursesprofs.profid = profs.profid "
        prof_stmt_str += "AND classes.classid = ?"

        dept_stmt_str = "SELECT dept, coursenum "
        dept_stmt_str += "FROM classes, crosslistings "
        dept_stmt_str += "WHERE classes.courseid = "
        dept_stmt_str += "crosslistings.courseid "
        dept_stmt_str += "AND classes.classid = ?"

        details = [self.query(stmt_str, args),
        self.query(prof_stmt_str, args),
        self.query(dept_stmt_str, args)]
        # If any exceptions thrown when accessing details in database
        if not details[0][0]:
            return (0, details[0][1])
        if not details[1][0]:
            return (0, details[1][1])
        if not details[2][0]:
            return (0, details[2][1])
        # If no errors, return the data
        return (1, [details[0][1], details[1][1], details[2][1]])
