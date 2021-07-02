import re

import sqlalchemy

from app import db
from app.models import Cost


def process_message(chat_id, user_id, user_name, message):
    try:
        message = re.sub(r'\s{2,}', '', message).split(' ')
        if message[0] == '/start':
            return 'Hi, this is SpendBot. I can help you count your' \
                   ' spends. \n' \
                   'To add spends just print /add, input amount, name,' \
                   ' cost, place and type of product. \n' \
                   'Use only one word to describe you spends, because' \
                   ' «Therefore, since brevity is the soul of wit...».\n' \
                   'And separate this words by space. ' \
                   'Like /add 1 Carlsberg 20 Market beer\n' \
                   'Good luck:)'
        elif message[0] == '/help':
            return 'Hi! This is list of commands.\n' \
                   '/add - add your spend. Use only one word to describe ' \
                   'you spends and separate this words by space.\n' \
                   '/chat_spends - show all spends of this chat.\n' \
                   '/my_spends - show only yours spends in this chat.\n' \
                   '/spends_by_category - show spends of this chat by category. ' \
                   'Input category after space.\n' \
                   '/del_product - delete last product by name that you input. ' \
                   'Input category after space.'
        elif message[0] == '/add':
            return add_product(chat_id, user_id, message[1:])
        elif message[0] == '/chat_spends':
            return show_chat_spends(chat_id)
        elif message[0] == '/my_spends':
            return show_my_spends(chat_id, user_id, user_name)
        elif message[0] == '/spends_by_category':
            return show_by_category(chat_id, message[1])
        elif message[0] == '/del_product':
            return delete_spend(chat_id, user_id, message[1])
        else:
            return "Unknown command"
    except IndexError:
        return 'Something are missing.'


def add_product(chat_id, user_id, product_info):
    try:
        amount, product_name, price, place, product_type = product_info
        product = Cost(chat_id=chat_id,
                       user_id=user_id,
                       amount=float(amount),
                       product=product_name.title(),
                       price=float(price),
                       place=place.capitalize(),
                       product_type=product_type.lower(),
                       cost=round(float(price)/float(amount), 2))
        db.session.add(product)
        db.session.commit()
        return f"{product_name} added"
    except ValueError:
        return f"Can't add {' '.join(product_info)}. Please check you input."


def show_chat_spends(chat_id):
    request_to_db = Cost.query.filter_by(chat_id=chat_id).all()
    result = [f"This chat spend:"]
    total_spend = 0
    for item in request_to_db:
        total_spend += item.price
        result.append(f"Buy {item.amount} {item.product} for {item.price} "
                      f"in {item.place} {item.timestamp.strftime('%d-%m-%Y')} "
                      f"{item.product_type}")
    result.append("Total spends {}".format(round(total_spend, 2)))
    return '\n'.join(result)


def show_my_spends(chat_id, user_id, user_name):
    request_to_db = Cost.query.filter_by(chat_id=chat_id,
                                         user_id=user_id).all()
    print(request_to_db)
    if not request_to_db:
        return f"There no spends by {user_name}"
    else:
        result = [f"{user_name} spend:"]
        total_spend = 0
        for item in request_to_db:
            total_spend += item.price
            result.append(f"Buy {item.amount} {item.product} for {item.price} "
                          f"in {item.place} {item.timestamp.strftime('%d-%m-%Y')} "
                          f"{item.product_type}")
        result.append("Total spends {}".format(round(total_spend, 2)))
        return '\n'.join(result)


def show_by_category(chat_id, product_type):
    print(product_type)
    request_to_db = Cost.query.filter_by(chat_id=chat_id,
                                         product_type=str(product_type)).all()
    if not request_to_db:
        return f"There no spends in {product_type} category."
    else:
        total_spend = 0.
        for item in request_to_db:
            total_spend += item.cost
        return f"Total amount spend for {product_type}: {round(total_spend, 2)}"


def delete_spend(chat_id, user_id, product):
    try:
        request_to_db = Cost.query.filter_by(chat_id=chat_id, user_id=user_id, product=str(product)).last()
        db.session.delete(request_to_db)
        db.session.commit()
        return f"{product} deleted"
    except sqlalchemy.orm.exc.UnmappedInstanceError:
        return f'Product {product} to delete are missing.'

