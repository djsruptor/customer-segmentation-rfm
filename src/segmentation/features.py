import pandas as pd
import pycountry

def parse_datatypes(df):
    df = df.copy()
    df['first_purchase_date'] = pd.to_datetime(df['first_purchase_date'])
    df['last_purchase_date'] = pd.to_datetime(df['last_purchase_date'])
    df = df.convert_dtypes()
    for col in ['device_type', 'favorite_category', 'gender']:
        df[col] = df[col].astype('category')
    return df

def recreate_customer_id(df):
    df = df.sort_values(by='first_purchase_date').reset_index(drop=True)
    df['customer_id'] = [f'CUST-{i:06d}' for i in range(1, len(df) + 1)]
    return df

replacements = {
    'Korea': 'South Korea',
    'Micronesia': 'Federated States of Micronesia',
    'Cape Verde': 'Cabo Verde',
    'Saint Martin': 'Saint Martin (French part)',
    'Svalbard & Jan Mayen Islands': 'Svalbard and Jan Mayen',
    'United States Virgin Islands': 'Virgin Islands, U.S.',
    'Saint Helena': 'Saint Helena, Ascension and Tristan da Cunha',
    'Swaziland': 'Eswatini',
    "Cote d'Ivoire": "Côte d'Ivoire",
    'Pitcairn Islands': 'Pitcairn',
    'Slovakia (Slovak Republic)': 'Slovakia',
    'Palestinian Territory': 'Palestine, State of',
    'Saint Barthelemy': 'Saint Barthélemy',
    'Antarctica (the territory South of 60 deg S)': 'Antarctica',
    'Libyan Arab Jamahiriya': 'Libya',
    'British Indian Ocean Territory (Chagos Archipelago)': 'British Indian Ocean Territory',
    'Reunion': 'Réunion',
    'Bouvet Island (Bouvetoya)': 'Bouvet Island',
    'Turkey': 'Türkiye',
    'Netherlands Antilles': 'Curaçao'
    }

def clean_countries(df):
    df = df.copy()
    df['country'] = df['country'].replace(replacements)

    def get_ISO3 (countryname):
        try:
            return pycountry.countries.lookup(countryname).alpha_3
        except Exception:
            return None
    
    df["ISO3"] = df["country"].apply(get_ISO3)
    return df

def wrangle_data(df):
    df = parse_datatypes(df)
    df = recreate_customer_id(df)
    df = clean_countries(df)
    return df