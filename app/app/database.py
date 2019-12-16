from sqlalchemy import and_, func, text
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from . import Config


# recommended to use autoflush
# https://docs.sqlalchemy.org/en/13/orm/collections.html#dynamic-relationship-loaders
engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, echo=False)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


class Paging:
    def __init__(self, model, id_column, relation_on, join_over_column, join_condition, per_page, page, order_by):
        self.model = model
        self.db_session = db_session()
        self.id_column = id_column
        self.relation_on = relation_on
        self.join_over_column = join_over_column
        self.join_condition = join_condition
        self.per_page = per_page
        self.page = page
        self.order_by = order_by

        self.iterator = self.get_pages()
        self.items = dict()
        self.previous_items = dict()
        self.pages = 0

        self.get_items()

    def get_pages(self):
        """"Break a Query into windows on a given column."""

        for where_clause in self.column_windows():

            yield self.db_session.query(self.model)\
                .join(self.relation_on)\
                .filter(where_clause) \
                .filter(self.join_over_column == self.join_condition) \
                .order_by(self.order_by)

    def column_windows(self):
        """Return a series of WHERE clauses against
        a given column that break it into windows.

        Result is an iterable of tuples, consisting of
        ((start, end), where_clause), where (start, end) are the ids.

        Requires a database that supports window functions,
        i.e. Postgresql, SQL Server, Oracle.

        Enhance this yourself !  Add a "where" argument
        so that windows of just a subset of rows can
        be computed.

        """

        query = self.db_session.query(
            self.id_column.label('item_id'),
            func.row_number().over(order_by=self.id_column).label('rownum')
        ).join(self.relation_on).filter(self.join_over_column == self.join_condition)\
            .from_self(self.id_column)\
            .filter(text("rownum %% %d=1" % self.per_page))

        intervals = [rid for rid, in query]

        while intervals:
            start = intervals.pop(0)
            end = intervals[0] if intervals else None

            yield self.int_for_range(start, end)

    def int_for_range(self, start_id, end_id):
        if end_id:
            return and_(
                self.id_column >= start_id,
                self.id_column < end_id
            )
        else:
            return self.id_column >= start_id

    def get_items(self):
        current_page = 0

        while True:
            try:
                page = next(self.iterator)
                page_items = [item for item in page]

                if page_items:
                    current_page += 1
                    if current_page == self.page:
                        self.items = page_items
                        self.items[0].on_page = self.page

                    if current_page == self.page - 1:
                        self.previous_items = page_items
                        self.previous_items[0].on_page = self.page - 1

            except StopIteration as e:
                print(e)
                break

        self.pages = current_page
        if self.items:
            self.items[0].pages_count = self.pages
        if self.previous_items:
            self.previous_items[0].pages_count = self.pages if self.items else self.page - 1

