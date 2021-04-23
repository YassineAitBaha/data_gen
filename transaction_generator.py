from data_generator import *

def generate_transaction(file_name, nrows):

    names = [
        'Altaran',
        'Renault',
        'Nissan',
        'Tesla',
        'Elon Musk',
        'John Coulberg',
        'Laurent Alexandre',
        'Walmart',
        'Chevron',
        'ConocoPhillips',
        'Exxon Mobil',
        'McKesson',
        'General Motos',
        'Activision Blizard'
    ]

    countries = [
        'FR',
        'SWI',
        'ITA',
        'SPA',
        'US',
        'GER',
        'SP',
        'JAP',
        'UK',
        'CHI',
    ]

    requirements = [

        {
            'name': 'account_sender_name',
            'generator': lambda nrows, df: np.random.choice(names, nrows)
        },

        {
            'name': 'country_sender',
            'generator': lambda nrows, df: np.random.choice(countries, nrows)
        },

        {
            'name': 'account_receiver_name',
            'generator': lambda nrows, df: np.random.choice(names, nrows)
        },

        {
            'name': 'country_receiver',
            'generator': lambda nrows, df: np.random.choice(countries, nrows)
        },

        {
            'name': 'datetime_timestamp',
            'generator': lambda nrows, df: 1000 * np.arange(nrows)
        },

        {
            'name': 'amount',
            'generator': lambda nrows, df: np.random.randint(1, 10000000, nrows)
        }
    ]

    df = generate_df(requirements, nrows)
    df.to_csv(file_name, index=False)



generate_transaction('transactions_big.csv', 3000)