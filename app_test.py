import bot.controller_test as bot
def test_history():
    logger.info("test_history function is run")
    # query_history = {'start_at': '2019-11-27',
    #          'end_at': '2019-12-03',
    #          'base': 'USD',
    #          'symbols': 'CAD'
    #          }
    # query_general = {
    #     'code':'USD'
    # }
    query_to_api('general', query_general)
    pass
    logger.info("test_history function is run")


# End telegram functions
def test_main():
    # test_list()
    # TODO if value is x$ then auto choose converted type
    # test_exchange('1.25$', 'CAD', 'USD')
    # test_history()
    bot_controller = bot.Currency_exchange_bot('.token')

if __name__ == '__main__':
    test_main()