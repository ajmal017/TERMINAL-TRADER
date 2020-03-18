import sqlite3

class ORM:
#PARENT CLASS-- handles all general functions & eliminates code repetition. 
    dbpath = ""
    tablename = ""

    fields = []

    #Empty DBPATH, tablename and fields -- these are CLASS SPECIFIC and will be specified in child classes.

    def __init__(self, **kwargs):
        raise NotImplementedError

    def save(self):
    #Inserts into DB if PK does not exist -- updates if exists. 
        if self.pk is None:
            self._insert()
        else:
            self._update()

    def _insert(self):
        with sqlite3.connect(self.dbpath) as conn:
            curs = conn.cursor()
            fieldlist = ", ".join(self.fields)

            # number of ?'s in VALUES = number of fields
            question_marks = ", ".join(['?' for _ in self.fields])
            SQLPATTERN = """ INSERT INTO {tablename} ({fieldlist})
                             VALUES ({question_marks}) """
            SQL = SQLPATTERN.format(
                tablename=self.tablename,
                fieldlist=fieldlist,
                question_marks=question_marks)

            # gettattr(self, field) is like self.column. If the value of field is "column", populating the list of values to pass to execute
            values = [getattr(self, field) for field in self.fields]
            curs.execute(SQL, values)

            # After creating a new row, there is a pk for this object to have
            pk = curs.lastrowid
            self.pk = pk

    def _update(self):
        # column1=?, column2=?, etc. for UPDATE syntax
        field_eqs = ["{field}=?".format(field=field) for field in self.fields]
        set_tos = ", ".join(field_eqs)

        SQLPATTERN = """ UPDATE {tablename} SET {set_tos}
                         WHERE PK = ? """
        SQL = SQLPATTERN.format(
                tablename=self.tablename, set_tos=set_tos)

        with sqlite3.connect(self.dbpath) as conn:
            curs = conn.cursor()

            columnvalues = [getattr(self, field) for field in self.fields]
            # pk value added to values for WHERE pk=?
            values = columnvalues + [self.pk]
            curs.execute(SQL, values)

    def delete(self):
        # If this object has a pk, remove that row from the database
        if self.pk: 
            SQLPATTERN = "DELETE FROM {tablename} WHERE pk=?; "
            SQL = SQLPATTERN.format(tablename=self.tablename)

            with sqlite3.connect(self.dbpath) as conn:
                curs = conn.cursor()
                curs.execute(SQL, (self.pk, ))

        # regardless of whether or not it was in a database, set all of its
        # attributes to zero
        for field in self.fields + ['pk']:
            setattr(self, field, None)

    @classmethod
    def one_from_where_clause(cls, where_clause="", values=tuple()):
        """ where_clause is something like 'WHERE pk=?' and values is a tuple
        corresponding to the ?'s in the clause. Returns None or one instance of
        this class. """
        SQLPATTERN = "SELECT * FROM {tablename} {where_clause}"
        SQL = SQLPATTERN.format(
            tablename=cls.tablename, where_clause=where_clause)
        with sqlite3.connect(cls.dbpath) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute(SQL, values)

            row = cur.fetchone()
            if not row:
                return None
            return cls(**row)

    @classmethod
    def all_from_where_clause(cls, where_clause="", values=tuple()):
        SQLPATTERN = "SELECT * FROM {tablename} {where_clause}"
        SQL = SQLPATTERN.format(
            tablename=cls.tablename, where_clause=where_clause)

        with sqlite3.connect(cls.dbpath) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute(SQL, values)

            rows = cur.fetchall()
            result=[]
            for row in rows:
                result.append(cls(**row))
            return result

    @classmethod
    def one_from_pk(cls, pk):
        #Returns ONE object based on inputted PK.
        return cls.one_from_where_clause("WHERE pk=?", (pk, ))

    @classmethod
    def delete_all(cls):
        SQL = "DELETE FROM {}".format(cls.tablename)
        with sqlite3.connect(cls.dbpath) as conn:
            cur = conn.cursor()
            cur.execute(SQL)

    def __repr__(self):
        pattern = "<{} ORM: pk={}>"
        return pattern.format(self.tablename, self.pk)