import click
from bots.controller import Currency_exchange_bot as Bot
import sys
from flask import Flask, render_template, url_for, flash, redirect, g
import logging
from logging import Formatter, FileHandler

app = Flask(__name__)
app.config.from_object('config')


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
    instance.history(update=None, context=None)
    return render_template('pages/history.html')


# Error handlers.
@app.errorhandler(500)
def internal_error(error):
    # db_session.rollback()
    return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')


# test exchange
@click.command()
@click.option('--debug', default=False, help='Debug mode to view data from model for using turn on "--debug=on"')
def debug_cli(debug):

    # app.run()
    print(debug)
    if debug == 'on':
        click.echo("Debug mode is enabled...")
        app.run()
    else:
        click.echo("Run telegram bot '{name}'...")
        instance = Bot('.token')
        instance.run()


if __name__ == '__main__':
    '''
    enter there 
    '''
    debug_cli()
