# IMPORT 
import pandas as pd
import numpy as np

#MAIN
# Creazione del dataframe con le informazioni delle startup
data = {
    'company': ['Doctolib', 'K Health', 'Zocdoc', 'WeDoctor', 'Carbon Health', 'Cerebral', 'Transcarent', 'KRY'],
    'founding_year': [2013, 2016, 2007, 2010, 2015, 2019, 2018, 2014],
    'country': ['France', 'United States', 'United States', 'China', 'United States', 'United States', 'United States', 'Sweden'],
    'industry': ['Bookings & Referalls', 'Telehealth', 'Bookings & Referalls', 'Telehealth', 'Telehealth', 'Mental Health', 'Bookings & Referalls', 'Telehealth'],
    'macro-industry': ['Telemedicine', 'Telemedicine', 'Telemedicine', 'Telemedicine', 'Telemedicine', 'Telemedicine', 'Telemedicine', 'Telemedicine'],
    'last_round': ['Mar 2022', 'Jan 2021', 'Feb 2021', 'Jan 2021', 'Jul 2021', 'Dec 2021', 'Nov 2022', 'Apr 2021'],
    'Fundings_Last_Round': ['$549M', '$132M', '$150M', '$411M', '$350M', '$300M', '$200M', '$319M'],
    'Numero Round Finanziamento': [9, 8, 10, 8, 10, 3, 3, 9],
    'Type Round': ['Series F', 'Series E', 'Series E', 'Series F', 'Series D', 'Series C', 'Series C', 'Series D'],
    'valuation': ['$6.4B', '$1.5B', '$1.8B', '$7.0B', '$3.0B', '$4.8B', '$1.6B', '$2.0B'],
    'Numero investitori': [13, 23, 19, 16, 46, 15, 16, 11],
    'Numbero di Acquisizioni effettuate': [4, 1, 0, 1, 4, 0, 2, 1],
    'TOTAL FUNDINGS': ['$815M', '$271M', '$375.9M', '$1,400.00M', '$622.18M', '$462.65M', '$298M', '$729M'],
    'Number Emloyee': ['1000-5000', '251-500', '501-1000', '1,000-5,000', '501-1000', '1,000-5,000', '251-500', '501-1000'],
    'Job offer active Maggio 2022': [19, 41, 32, 4, 251, 98, 21, 34],
    'Job offer active Novemebre 2022': [11, 20, 30, 6, 421, 115, 9, 46],
    'Job offer active Maggio 2023': [198, 24, 37, 10, 354, 182, 2, 96]
}

df = pd.DataFrame(data)

# varibiabili globali:
# Define the weights for funding types
funding_type_weights = {'Pre-seed': 0.3, 'Series A': 0.4, 'Series B': 0.5, 'Series C': 0.6, 'Series D': 0.7, 'Series E': 0.8, 'Series F': 0.9}

# Define the weights for employee numbers
score_number_dipendenti = {'251-500': 0.3, '501-1000': 0.55, '1000-5000': 0.8}

#FUNCTIONS

def data_manipulation(df):
    # Rimozione del simbolo "$" e "M" dalla colonna "TOTAL FUNDINGS"
    df['TOTAL FUNDINGS'] = df['TOTAL FUNDINGS'].str.replace('$', '', regex=False).str.replace('M', '', regex=False).str.replace(',', '', regex=False)

    # Rimozione del simbolo "$" e "B" dalla colonna "valuation"
    df['valuation'] = df['valuation'].str.replace('$', '', regex=False).str.replace('B', '', regex=False)

    # Rimozione del simbolo "$" e "M" dalla colonna "Fundings_Last_Round"
    df['Fundings_Last_Round'] = df['Fundings_Last_Round'].str.replace('$', '', regex=False).str.replace('M', '', regex=False)

    # Conversione delle colonne in numeri interi
    df['TOTAL FUNDINGS'] = df['TOTAL FUNDINGS'].astype(float).astype(int)
    df['valuation'] = df['valuation'].astype(float).astype(int)
    df['Fundings_Last_Round'] = df['Fundings_Last_Round'].astype(float).astype(int)

    # Rimozione delle virgole e conversione in numeri interi per la colonna "Number Emloyee"
    df['Number Emloyee'] = df['Number Emloyee'].str.replace(',', '', regex=False).astype(str)
    df['Number Emloyee'] = df['Number Emloyee'].apply(lambda x: int(x.split('-')[1]) - int(x.split('-')[0]))
    return df


def success_score(df):
    # Calculate the success score for each startup
    success_score = (
        ((df['country'].map({'United States': 0.8, 'China': 0.75, 'France': 0.70, 'Sweden': 0.70}).fillna(0.6)) +
        ((df['Job offer active Maggio 2023'] - df['Job offer active Maggio 2022']) / df['Job offer active Maggio 2023']).fillna(0)) +
        (df['Type Round'].map(funding_type_weights)).fillna(0) +
        (df['Number Emloyee'].map(score_number_dipendenti)).fillna(0) +
        (df['TOTAL FUNDINGS'] - df['TOTAL FUNDINGS'].min()) / (df['TOTAL FUNDINGS'].max() - df['TOTAL FUNDINGS'].min()) +
        ((df['valuation'] - df['TOTAL FUNDINGS']) / df['valuation']).fillna(0)
    ) / 6

    # Add the success score to the DataFrame
    df['success_score'] = success_score

    # Normalize the values between 0 and 1
    df['success_score'] = (df['success_score'] - df['success_score'].min()) / (df['success_score'].max() - df['success_score'].min())

    # Sort the DataFrame by success score in descending order
    df = df.sort_values(by='success_score', ascending=False)
    
    # Save the DataFrame to an Excel file
    df.to_excel('startup_success_scores.xlsx', index=False)

    # Display the DataFrame
    print(df)

def maturity_score(df):
    # Calcola l'anno corrente come punto di riferimento per calcolare eta delle startup
    current_year = pd.to_datetime('today').year
    
    # Calcola eta delle startup in anni
    df['startup_age'] = current_year - df['founding_year']
    
    # Calcola lo score eta basato sull'andamento logaritmico
    df['age_score'] = np.log(df['startup_age'] + 1)
    max_age_score = df['age_score'].max()
    df['age_score'] = df['age_score'] / max_age_score
    
    # Calcola lo score basato sulla proporzione tra il numero di finanziamenti e eta della startup
    df['funding_ratio'] = df['Numero Round Finanziamento'] / df['startup_age']
    max_funding_ratio = df['funding_ratio'].max()
    df['funding_score'] = df['funding_ratio'] / max_funding_ratio
    
    df['type_round_sys'] =(df['Type Round'].map(funding_type_weights)).fillna(0)
    # Calcola lo score complessivo di maturita
    df['maturity_score'] = (df['age_score'] + df['funding_score'] + df['type_round_sys'] ) / 3
    
    # Normalizza lo score tra 0 e 1
    df['maturity_score'] = (df['maturity_score'] - df['maturity_score'].min()) / (df['maturity_score'].max() - df['maturity_score'].min())
    # Sort the DataFrame by success score in descending order
    df = df.sort_values(by='maturity_score', ascending=False)
    
    # Save the DataFrame to an Excel file
    df.to_excel('startup_maturity_scores.xlsx', index=False)

    # Display the DataFrame
    print(df)


# Call functions
dfclean=data_manipulation(df)
success_score(dfclean)
print("-"*50)
maturity_score(dfclean)
