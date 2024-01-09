import datetime
import json


# import os
# filepath = os.path.join(os.path.dirname(__file__), '..', 'operations.json')

def last_five_raw(filepath):
    with open(filepath, 'r') as file:
        data = json.load(file)

    executed_transaction = [trans for trans in data if trans.get("state") == "EXECUTED"]

    sorted_trasactions = sorted(executed_transaction, key=lambda x: x.get("date"), reverse=True)

    last_five_trans = sorted_trasactions[:5]
    return last_five_trans


def mask_card(card_info):
    number_str = str(card_info)
    number_digit_only = ''.join(filter(str.isdigit, number_str))

    parts = card_info.split()
    card_name = []

    for part in parts:
        if not part.isdigit():
            card_name.append(part)

    return ' '.join(card_name) + ' ' + number_digit_only[:4] + ' ' + number_digit_only[
                                                                     4:6] + '** **** ' + number_digit_only[-4:]


def mask_account(account_info):
    parts = account_info.split()

    account_str = str(account_info)
    account_number_only = ''.join(filter(str.isdigit, account_str))

    account_name = []
    for part in parts:
        if not part.isdigit():
            account_name.append(part)

    return ' '.join(account_name) + ' **' + account_number_only[-4:]


def last_five_formatted(filepath):
    """
    <дата перевода> <описание перевода>
    <откуда> -> <куда>
    <сумма перевода> <валюта>
    :return:
    """
    data = last_five_raw(filepath)
    formatted_output = []

    for i in data:
        date = datetime.datetime.strptime(i['date'], '%Y-%m-%dT%H:%M:%S.%f').strftime('%d.%m.%Y')

        from_account = i.get(
            'from')  # some transactions don't have 'from' (deposits), used GET so it would return None
        to_account = i['to']

        if from_account:
            if 'Счет' in from_account:
                from_account_formatted = mask_account(from_account)
            else:
                from_account_formatted = mask_card(from_account)

        if 'Счет' in to_account:
            to_account_formatted = mask_account(to_account)
        else:
            to_account_formatted = mask_card(to_account)

        description = i['description']
        amount = i['operationAmount']['amount']
        currency = i['operationAmount']['currency']['name']

        combined_str = f"{date} {description}\n"
        if from_account:  # deposits don't have 'from'
            combined_str += f"{from_account_formatted} "
        combined_str += f"-> {to_account_formatted}\n{amount} {currency}\n"

        formatted_output.append(combined_str)

    return '\n'.join(formatted_output)
