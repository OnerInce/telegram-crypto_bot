from datetime import date

from src.style_message import style_message


def test_message_style():
    test_time = date(2022, 11, 16)
    day = test_time.strftime("%m/%d/%Y")
    time = test_time.strftime("%H:%M:%S")

    test_price = ['Paribu', 'USDT', '50000', 3.1]
    styled_msg = style_message(
        lang_code='en', coin_sym='BTC', coin_name='Bitcoin', fetch_time=test_time, user='Oner', all_prices=test_price
    )
    correct_msg = f"""
    {day}, <b>{time}GMT</b>
    Hello <i>Oner</i>
    BTC (Bitcoin) Price: 
    <code>Paribu</code>   > <b>50000</b> <i>USDT</i>      %3.1
    """

    assert ''.join(correct_msg.split()) == ''.join(styled_msg.split())
