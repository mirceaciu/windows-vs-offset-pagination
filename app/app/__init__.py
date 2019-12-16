from flask import Flask, render_template
from .config import Config
from .database import db_session, Paging
from datetime import datetime
import time

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

from .models import User, Article

print(Config.__dict__)


def add_test_data():
    def users_gen():
        for u in range(Config.TEST_DATA_Q):
            user = User()
            user.email = f'{u}test@email.com'
            user.first_name = f'{u} first name'
            user.first_name = f'{u} last name'

            yield user

    def articles_gen():
        for a in range(Config.TEST_DATA_Q):
            article = Article()
            article.title = f'{a} title'
            article.publish_date = datetime.utcnow()

            yield article

    users_data = list(users_gen())
    articles_data = list(articles_gen())

    for index, user in enumerate(users_data):
        user.articles = (list(articles_data))

    db_session.add_all(users_data)
    db_session.add_all(articles_data)
    db_session.commit()


@app.route('/ping')
def give_ping():
    return 'pong!'


@app.route('/test')
def run_test():
    user = User.query.filter_by(id=1).first()
    if not user:
        app.logger.info('building database, please wait')
        add_test_data()
        app.logger.info('database is ready')
    else:
        app.logger.info('db already built')

    times = {}
    per_page = 20

    rows = Config.TEST_DATA_Q
    total_pages = int(rows / per_page)

    for page in [1, int(total_pages / 2), total_pages]:

        page_times = []
        for _ in range(11):
            start = time.time()
            user = User.query.filter_by(id=1).first()

            if Config.USE_CORE_DB:
                if user:
                    articles_paging = Paging(
                        model=Article,
                        id_column=Article.id,
                        relation_on=Article.users,
                        join_over_column=User.email,
                        join_condition=user.email,
                        per_page=per_page,
                        page=page,
                        order_by=Article.title
                    )

                    # if requested page has no items return previous one
                    items = articles_paging.items if articles_paging.items else articles_paging.previous_items
            else:
                if user:
                    items = user.articles.paginate(page, per_page, False).items

            end = time.time()
            page_times.append(end - start)

        times[page] = page_times

    return render_template(
        "show_results.html",
        data=times,
        env_quantity=Config.TEST_DATA_Q,
        orm_type='SqlAlchemy Core' if Config.USE_CORE_DB else 'Flask-SqlAlchemy'
    )


