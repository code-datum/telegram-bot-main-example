import click
from bots.controller import Currency_exchange_bot as Bot
from flask import Flask, render_template, url_for, flash, redirect, g
import logging


logging.basicConfig(filename='debug.log', filemode='w', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)




app = Flask(__name__)

DEBUG = app.config['DEBUG']



labels = [
    'JAN', 'FEB', 'MAR', 'APR',
    'MAY', 'JUN', 'JUL', 'AUG',
    'SEP', 'OCT', 'NOV', 'DEC'
]

values = [
    967.67, 1190.89, 1079.75, 1349.19,
    2328.91, 2504.28, 2873.83, 4764.87,
    4349.29, 6458.30, 9907, 16297
]

colors = [
    "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA",
    "#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1",
    "#C71585", "#FF4500", "#FEDCBA", "#46BFBD"]

@app.route('/')
def home():
    return "<h2>homepage</h2>" \
           "<ul><li><a href='/exchange'>Exchange</li>" \
           "<li><a href='/list'>List</li>" \
           "<li><a href='/history'>History</li>" \
           "</ul>"


@app.route('/exchange')
def exchange():
    instance = Bot(token_path='.token', debug=DEBUG)
    instance.exchange(update=None, context=None)
    return render_template('pages/exchange.html')


# test list
@app.route('/list')
def list(update=None, context=None):
    instance = Bot(token_path='.token', debug=DEBUG)
    instance.list(update=None, context=None)
    return render_template('pages/list.html')


# test history
@app.route('/history')
def history(update=None, context=None):
    instance = Bot(token_path='.token', debug=DEBUG)
    content = instance.history(update=None, context=None)
    '''content = {'rates': {'2020-02-26': {'CAD': 1.3304827586}, '2020-03-02': {'CAD': 1.3358208955},... 
    '2020-02-28': {'CAD': 1.3443563815}}, 'start_at': '2020-02-25', 'base': 'USD', 'end_at': '2020-03-03'}'''

    # app.logger.info("{}".format(rates_key))
    line_labels = labels
    line_values = values

    return render_template('pages/history.html', debug_view=True,
                           title='Bitcoin Monthly Price in USD', max=17000,
                           labels=line_labels, values=line_values)


# Error handlers.
@app.errorhandler(500)
def internal_error(error):
    # db_session.rollback()
    return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


def test_run():
    instance = Bot(token_path='.token', debug=DEBUG)
    instance.test_run()

# test exchange
@click.command()
@click.option('--debug', default=False, help='Debug mode to view data from model for using turn on "--debug=on"')
@click.option('--test', default=False, help='Test the main methods in controller "test=on"')
def debug_cli(debug, test):

    # app.run()
    print(debug)
    if debug == 'on':
        click.echo("Debug mode is enabled...")
        app.run()
    elif test == 'on':
        click.echo("Test mode is enabled...")
        test_run()
    else:
        click.echo("Run telegram bot '{name}'...")
        instance = Bot('.token')
        instance.run()


if __name__ == '__main__':
    '''
    enter there 
    '''
    debug_cli()
