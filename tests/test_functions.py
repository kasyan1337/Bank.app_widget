import os

import pytest

from utils import functions


@pytest.fixture
def raw_data():
    """
    :param filepath:
    :return: open json file from parent directory
    """
    return os.path.join(os.path.dirname(__file__), '..', 'operations.json')


def test_get_last_five_raw(raw_data):
    """
    :param raw_data:
    :return: list of last 5 transactions unformatted
    """
    transactions = functions.get_last_five_raw(raw_data)
    assert len(transactions) == 5
    for transaction in transactions:
        assert transaction["state"] == "EXECUTED"


def test_mask_card():
    """
    :param card_info:
    :return: masked card info
    """
    assert functions.mask_card('Maestro 7810846596785568') == "Maestro 7810 84** **** 5568"
    assert functions.mask_card('Visa Classic 2842878893689012') == "Visa Classic 2842 87** **** 9012"
    assert functions.mask_card('2842878893689012') == " 2842 87** **** 9012"


def test_mask_account():
    """
    :param account_info:
    :return: masked account info
    """
    assert functions.mask_account('Счет 77613226829885488381') == "Счет **8381"
    assert functions.mask_account('77613226829885488381') == " **8381"
    assert functions.mask_account('7761322682988548838177613226829885488381') == " **8381"
    assert functions.mask_account('Инностранный счет 77613226829885488381') == "Инностранный счет **8381"


def test_show_last_five_formatted(raw_data):
    """
    :param raw_data:
    :return: list of last 5 transactions formatted
    """
    assert functions.show_last_five_formatted(raw_data) == ("08.12.2019 Открытие вклада\n"
                                                       "-> Счет **5907\n41096.24 USD\n"
                                                       "\n07.12.2019 Перевод организации\n"
                                                       "Visa Classic 2842 87** **** 9012 -> Счет **3655\n48150.39 USD\n"
                                                       "\n19.11.2019 Перевод организации\nMaestro 7810 84** **** 5568 "
                                                       "-> Счет **2869\n30153.72 руб.\n"
                                                       "\n13.11.2019 Перевод со счета на счет"
                                                       "\nСчет **9794 -> Счет **8125\n62814.53 руб.\n"
                                                       "\n05.11.2019 Открытие вклада\n-> Счет **8381\n21344.35 руб.\n")
