#%%
import pandas as pd
import re
import matplotlib as mlt
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.axes as axes
import math
#!{sys.executable} -m pip install seaborn
import seaborn as sb
#%%
dataset = pd.read_csv("datasets/Airplane_Crashes_and_Fatalities_Since_1908_20190820105639.csv")
dataset
#%%
continents_dataset = pd.read_csv("datasets/continents2.csv")
#%%
cities_dataset = pd.read_csv("datasets/cities.csv")
#%% md
---
---
# Gabro
#%% md
#### Cleaning colonna **Operator**
#%%
print("numero di Na:", len([i for i in dataset.Operator if type(i) == float]))  # abbiamo solo 10 Na
print(dataset.shape)

# Eliminazione righe contenenti Na nella colonna Operator
dataset = dataset[dataset['Operator'].notna()]
print(dataset.shape)
#%% md
Identificazione e raggruppamento categoria di operatore militare
#%%
print(len(dataset['Operator'].unique()))

military_flights = []

military_words = ["army", "navy", "marine", "military", "force", "airforce", "amee de l'air", "mission"]

# Identifica tutti i nomi degli operatori che appartengono al campo militare
for operator in dataset['Operator'].unique():
    for word in military_words:
        if word.lower() in operator.lower() and operator not in military_flights: military_flights.append(operator)

# Identifica tutti i nomi degli operatori che in Route hanno Test flight e Test presumendo che si trattino anche essi di voli militari
test_flights = ["Test", "Test flight"]
for position, operator in enumerate(dataset['Operator']):
    if dataset.Route.iloc[position] in test_flights and operator not in military_flights: military_flights.append(
        operator)

print("numero di operatori militari univoci:", len(military_flights))  # 251 valori univoci relativi
#%% md
Identificazione e raggruppamento categoria di operatore postale
#%%
postal_cargo_flights = []

postal_e_cargo_words = ["postal", "mail", "aeropostale", "cargo", "express", "commercial"]

# Identifica tutti i nomi degli operatori che appartengono al campo militare
for operator in dataset['Operator'].unique():
    if type(operator) != float:
        for word in postal_e_cargo_words:
            if word.lower() in operator.lower() and operator not in postal_cargo_flights: postal_cargo_flights.append(
                operator)

print("numero di operatori postali/cargo univoci:", len(postal_cargo_flights))
#%%
private_flights = []

private_words = ["priva"]

# Identifica tutti i nomi degli operatori che appartengono al campo militare
for operator in dataset['Operator'].unique():
    if type(operator) != float:
        for word in private_words:
            if word.lower() in operator.lower() and operator not in private_flights: private_flights.append(operator)

print("numero di operatori postali/cargo univoci:", len(private_flights))
#%% md
#### Aggiunta valori per la nuova colonna
#%%
new_column = []

for value in dataset.Operator:
    if value in military_flights:
        new_column.append("Military flight")
    elif value in postal_cargo_flights:
        new_column.append("Postal/Cargo flight")
    elif value in private_flights:
        new_column.append("Private flights")
    else:
        new_column.append("Scheduled flight")
#%%
dataset = dataset.assign(New_Operator_column=new_column)
dataset
#%%
print(len(dataset.New_Operator_column.unique()))
#%% md
#### Cleaning colonna **Route**
#%%
print("numero di NaN nella colonna Route:",
      len([i for i in dataset.Route if type(i) == float]))  # 770.. da gestire
#%%
rotte = []

for position, route in enumerate(dataset.Route):
    if type(route) != float:
        rotte.append(route.split(" - "))
    else:
        rotte.append(route)

rotte_pulite = []
for position, route in enumerate(rotte):
    new_route = []
    if type(route) != float:
        for aeroport in route:
            if "," in aeroport:
                new_route.append(re.sub(f",.+", "", aeroport))
            else:
                new_route.append(aeroport)
    elif type(route) == float and dataset["New_Operator_column"].iloc[position] == "Military flight":
        new_route.append("Informazione riservata")
    else:
        new_route.append("Sconosciuto")
    rotte_pulite.append(new_route)

print(rotte_pulite)
#%% md
#### Aggiunta colonna Aeroporto_di_partenza
#%%
# Aggiunta colonna Aeroporto_di_partenza
aeroporto_partenza = [aeroporto[0] for aeroporto in rotte_pulite]
dataset = dataset.assign(Aeroporto_di_partenza=aeroporto_partenza)

dataset
#%% md
#### Aggiunta colonne per aeroporti intermedi
Il numero massimo di aeroporti nelle rotte è 7 quindi andranno create 7 nuove colonne
#%%
# for aeroporto in rotte_pulite:
#     if len(aeroporto) == 7: print(aeroporto)

aeroporto_di_destinazione = []
aeroporto_2 = []
aeroporto_3 = []
aeroporto_4 = []
aeroporto_5 = []
aeroporto_6 = []

# Molto brutto... Decidere se cambiare
for n_aeroporti in rotte_pulite:
    if len(n_aeroporti) == 1:
        aeroporto_di_destinazione.append(n_aeroporti)
        aeroporto_2.append("Nan")
        aeroporto_3.append("Nan")
        aeroporto_4.append("Nan")
        aeroporto_5.append("Nan")
        aeroporto_6.append("Nan")
    if len(n_aeroporti) == 2:
        aeroporto_di_destinazione.append(n_aeroporti[-1])
        aeroporto_2.append("Nan")
        aeroporto_3.append("Nan")
        aeroporto_4.append("Nan")
        aeroporto_5.append("Nan")
        aeroporto_6.append("Nan")
    if len(n_aeroporti) == 3:
        aeroporto_2.append(n_aeroporti[1])
        aeroporto_di_destinazione.append(n_aeroporti[-1])
        aeroporto_3.append("Nan")
        aeroporto_4.append("Nan")
        aeroporto_5.append("Nan")
        aeroporto_6.append("Nan")
    if len(n_aeroporti) == 4:
        aeroporto_2.append(n_aeroporti[1])
        aeroporto_3.append(n_aeroporti[2])
        aeroporto_di_destinazione.append(n_aeroporti[-1])
        aeroporto_4.append("Nan")
        aeroporto_5.append("Nan")
        aeroporto_6.append("Nan")
    if len(n_aeroporti) == 5:
        aeroporto_2.append(n_aeroporti[1])
        aeroporto_3.append(n_aeroporti[2])
        aeroporto_4.append(n_aeroporti[3])
        aeroporto_di_destinazione.append(n_aeroporti[-1])
        aeroporto_5.append("Nan")
        aeroporto_6.append("Nan")
    if len(n_aeroporti) == 6:
        aeroporto_2.append(n_aeroporti[1])
        aeroporto_3.append(n_aeroporti[2])
        aeroporto_4.append(n_aeroporti[3])
        aeroporto_5.append(n_aeroporti[4])
        aeroporto_di_destinazione.append(n_aeroporti[-1])
        aeroporto_6.append("Nan")
    if len(n_aeroporti) == 7:
        aeroporto_2.append(n_aeroporti[1])
        aeroporto_3.append(n_aeroporti[2])
        aeroporto_4.append(n_aeroporti[3])
        aeroporto_5.append(n_aeroporti[4])
        aeroporto_6.append(n_aeroporti[5])
        aeroporto_di_destinazione.append(n_aeroporti[-1])

# Alcuni valori di aeroporto_di destinazione erano in una lista. Risolviamo:
for position, aeroporto in enumerate(aeroporto_di_destinazione):
    if type(aeroporto) == list:
        aeroporto_di_destinazione[position] = aeroporto[0]

dataset = dataset.assign(Aeroporto_2=aeroporto_2,
                         Aeroporto_3=aeroporto_3,
                         Aeroporto_4=aeroporto_4,
                         Aeroporto_5=aeroporto_5,
                         Aeroporto_6=aeroporto_6,
                         Aeroporto_di_destinazione=aeroporto_di_destinazione)

dataset
#%% md
### Cleaning AC type
#%% md
Ricordarsi di agiungere un .upper anche dopo il primo else una volta che abbiamo deciso di eliminare gli Na
#%%
# Prima pulizia

print(len(dataset["AC Type"].unique()))

simplified_aircraft_names = []

# Eliminazione dei pattern tipo "15-L ..." e "V-17 ..."
for airplane in dataset["AC Type"]:
    if type(airplane) != float and len(airplane.split()) > 1:
        simplified_aircraft_names.append(re.sub(r"[A-Z0-9]+-.+", "", airplane).upper())
    else:
        simplified_aircraft_names.append(airplane)

# Eliminazione dei pattern tipo "15.L ..." e "V.17 ..."
simplified_aircraft_names_1 = []
for position, airplane in enumerate(simplified_aircraft_names):
    if type(airplane) != float and len(airplane.split()) > 1:
        simplified_aircraft_names_1.append(re.sub(r"[A-Z0-9]+\.(.)+", "", airplane))
    else:
        simplified_aircraft_names_1.append(airplane)

print(simplified_aircraft_names_1)
#%% md
*Decidere se pulire maggiormente o meno*
#%%
dataset = dataset.assign(AC_Type_simplified=simplified_aircraft_names_1)
print(f"Prima della pulizia: {len(dataset['AC Type'].unique())} valori univoci")
print(f"Dopo la pulizia: {len(dataset['AC_Type_simplified'].unique())} valori univoci")
#%% md
### Controllo valori nulli delle colonne:
- Aboard
- Aboard Crew
- Aboard Passangers
- Fatalities
- Fatalities Crew
- Fatalities Passangers
- Ground
#%%
def na_counter_for_numeric_column(column, nome_colonna):
    nas = []
    for value in column:
        try:
            int(value)
        except:
            nas.append(value)
    return print(f"Numero di Na della colonna {nome_colonna}: {len(nas)}")


na_counter_for_numeric_column(dataset["Aboard"], "Aboard")
na_counter_for_numeric_column(dataset["Aboard Crew"], "Aboard Crew")
na_counter_for_numeric_column(dataset["Aboard Passangers"], "Aboard Passangers")
na_counter_for_numeric_column(dataset["Fatalities"], "Fatalities")
na_counter_for_numeric_column(dataset["Fatalities Crew"], "Fatalities Crew")
na_counter_for_numeric_column(dataset["Fatalities Passangers"], "Fatalities Passangers")
#%% md
##### **Gli Na delle colonne Aboard e Fatalities secondo me si possono eliminare, magari quelli delle altre invece li sostituiamo con le medie**
#%% md
---
---
# Maic
#%% md
### Location Variable -> estraiamo dal testo solo gli stati
#%% md
#### regex per prendere solo quello dopo l'ultima virgola
#%%
new_location = []
for w in dataset.Location:
    new_location.append(re.findall("[^ ,]\w*$", str(w)))

print(new_location)
#%% md
#### Dal momento in cui le stringhe sono dentro una lista, tramite un ciclo annidato andiamo ad estrarre le stringhe e successivamente mettiamo tutto dentro una lista di supporto
#%%
tmp_state = []
for i in new_location:
    for w in i:
        tmp_state.append(w)

print(tmp_state)
#%% md
#### Pulisco i valori
#%%
tmp_state_cleaned = []
for i in tmp_state:
    tmp_state_cleaned.append(re.sub(rf"[^\w\s]", "", i))

print(tmp_state_cleaned)
#%% md
#### Infine andiamo a creare una nuovo variabile a ad inserirla all'interno del dataset
#%%
dataset = dataset.assign(state_location=tmp_state_cleaned)
print(dataset.state_location)
#%%
list_of_states = dataset.state_location.unique()
print(list_of_states)
#%% md
#### Noto che c'è un nan value e campi vuoti non visti in precedenza
#%%
count_nan = 0
count_vuoti = 0
for i in dataset.state_location:
    if i == 'nan':
        count_nan += 1
    elif i == '':
        count_vuoti += 1

print('counter nan: ', count_nan)
print('counter spazi vuoti: ', count_vuoti)
#%% md
#### Li elimino
#%%
dataset = dataset[dataset.state_location != 'nan']
dataset = dataset[dataset.state_location != '']
print(dataset)
#%% md
#### Check finale
#%%
count = 0
for i in dataset.state_location:
    if i == 'nan' or i == '':
        count += 1
print(count)
#%% md
#### Accorpo alcuni stati e correggo quelli scritti in modo scorretto
#%% md
##### Stati Uniti
#%%
list_of_states_cleaned = dataset.state_location.unique()
print(list_of_states_cleaned)
#%%

#%%
USA_states = ['Virginia', 'Jersey', 'Ohio', 'Pennsylvania', 'Illinois', 'Maryland', 'Kent', 'Indiana', 'Iowa',
              'Columbia', 'Wyoming', 'Minnisota', 'Wisconsin', 'Nevada', 'NY', 'WY', 'States', 'York', 'Utah', 'Oregon',
              'Idaho', 'Connecticut', 'Minnesota', 'Kansas', 'Texas', 'Washington', 'Tennessee', 'Greece', 'California',
              'Mexico', 'Missouri', 'Massachusetts', 'Utah', 'Ilinois', 'Florida', 'Michigan', 'Arkansas', 'Colorado',
              'Georgia', 'Montana', 'Mississippi', 'Alaska', 'Cailifornia', 'Indies', 'Andes', 'Guam', 'Tonkin',
              'Carolina', 'Kentucky', 'Maine', 'Alabama', 'Delaware', 'Dekota', 'Hampshire', 'Washingon', 'DC',
              'Tennesee', 'Deleware', 'Louisiana', 'Massachutes', 'Alakska', 'Coloado', 'Vermont', 'Dakota',
              'Calilfornia', 'Alaksa', 'Mississipi', 'Arizona', 'Wisconson', 'Nebraska', 'Oklahoma', 'Airzona', 'HI', 'Hawaii']
states = []
for state in dataset.state_location:
    if state in USA_states:
        states.append('United States')
    else:
        states.append(state)

print(states)
#%%
print(sorted(set(states)))
#%% md
##### Correzioni varie
#%%
states2 = []
for state in states:
    states2.append(state.replace('Canada2', 'Canada').
                   replace('CA', 'Canada').
                   replace('UAR', 'Emirates').
                   replace('Emirates', 'Emirates').
                   replace('UAE', 'Emirates').
                   replace('Djbouti', 'Djibouti').
                   replace('Bulgeria', 'Bulgaria').
                   replace('bulgaria', 'Bulgaria').
                   replace('Aregntina', 'Argentina').
                   replace('Amsterdam', 'Belgium').
                   replace('Ontario', 'Canada').
                   replace('Okinawa', 'Japan').
                   replace('karkov', 'Ukraine').
                   replace('Jamacia', 'Jamaica').
                   replace('Argenina', 'Argentina').
                   replace('Airstrip', 'Airport').
                   replace('Algiers', 'Algeria').
                   replace('Russian', 'Russia').
                   replace('Swden', 'Sweden').
                   replace('coast', 'Coast').
                   replace('BO', 'Bolivia').
                   replace('Rico', 'Costa Rica').
                   replace('Rica', 'Costa Rica').
                   replace('Karkinitsky', 'Ukraine').
                   replace('Saskatchewan', 'Canada').
                   replace('Australila', 'Australia').
                   replace('Inodnesia', 'Indonesia').
                   replace('Chili', 'Chile').
                   replace('Korean', 'Korea').
                   replace('Uzbekstan', 'Uzbekistan').
                   replace('Cogo', 'Congo').
                   replace('Zaire', 'Democratic Republic of Congo').
                   replace('Inagua', 'Bahamas').
                   replace('Bimini', 'Bahamas').
                   replace('Philipines', 'Philippines').
                   replace('Marroco', 'Morocco').
                   replace('Yugosalvia', 'Yugoslavia').
                   replace('Ariège', 'France').
                   replace('Arabia', 'Saudi Arabia').
                   replace('Cachoeria', 'Brazil').
                   replace('Kirghizia', 'Kyrgyzstan').
                   replace('Reunion', 'France').
                   replace('Volta', 'Ghana').
                   replace('Manmar', 'Myanmar').
                   replace('Baangladesh', 'Bangladesh').
                   replace('Papua', 'Papua New Guinea').
                   replace('Mauretania', 'Mauritania').
                   replace('Azores', 'Portugal').
                   replace('Antigua', 'Bermuda').
                   replace('Zealand', 'New Zealand').
                   replace('Elalat', 'Saudi Arabia').
                   replace('Sarawak', 'Mali').
                   replace('Phillipines', 'Philippines').
                   replace('Afghanstan', 'Afghanistan').
                   replace('Boliva', 'Bolivia').
                   replace('Napal', 'Nepal').
                   replace('Bosnia', 'Bosnia').
                   replace('Burma', 'Myanmar').
                   replace('Nambia', 'Namibia').
                   replace('Malaya', 'Malaysia').
                   replace('Hati', 'Haiti').
                   replace('Labrador', 'Canada').
                   replace('Coatia', 'Croatia').
                   replace('Province', 'France').
                   replace('Crete', 'Greece').
                   replace('Tanganyika', 'Tanzania').
                   replace('Lanka', 'Sri Lanka').
                   replace('Karkov', 'Ukraine').
                   replace('Kong', 'China').
                   replace('Leone', 'Sierra Leone').
                   replace('Manitoba', 'Canada').
                   replace('Salvador', 'El Salvador').
                   replace('Herzegovina', 'Bosnia').
                   replace('Hunary', 'Hungary').
                   replace('Luqa', 'Malta').
                   replace('Verde', 'Cabo Verde').
                   replace('Surinam', 'Suriname').
                   replace('Indian', 'India').
                   replace('Cameroons', 'Cameroon').
                   replace('Sirte', 'Libya').
                   replace('Kazakistan', 'Kazakhstan').
                   replace('Bugaria', 'Bulgaria').
                   replace('Surinamee', 'Suriname').
                   replace('Mexic', 'Mexico').
                   replace('Tomé', 'Principe').
                   replace('Principe', 'Principe'))

print(sorted(set(states2)))
#%% md
##### Regno Unito
#%%
states_UK = ['UK', 'Wales', 'Scotland', 'Eire', 'Union', 'Kingdom', 'England', 'Caledonia', 'Man']
states3 = []
for state in states2:
    if state in states_UK:
        states3.append('United Kingdom')
    else:
        states3.append(state)

print(set(states3))
#%% md
#### Infine inserisco la variabile nel dataset
#%%
dataset = dataset.assign(States=states3)
#%% md
#### Elimino altre due osservazioni che non siamo riusciti a classificare
#%%
dataset = dataset[dataset.States != 'AK']
dataset = dataset[dataset.States != 'Nag']
dataset.States
#%% md
### Macro-aree
#%% md
#### Importiamo un dataset di supporto che ci permette di fare un match tra i paesi e i territori
#%%

continents_dataset
#%%
macro_aree = continents_dataset['sub-region'].unique()
print(macro_aree)
#%% md
#### Creo la lista dei paesi per ogni macro-area
#%%
Southern_Asia = continents_dataset['name']._where(continents_dataset['sub-region'] == 'Southern Asia').unique()

Northern_Europe = continents_dataset['name']._where(continents_dataset['sub-region'] == 'Northern Europe').unique()

Southern_Europe = continents_dataset['name']._where(continents_dataset['sub-region'] == 'Southern Europe').unique()

Northern_Africa = continents_dataset['name']._where(continents_dataset['sub-region'] == 'Northern Africa').unique()

Polynesia = continents_dataset['name']._where(continents_dataset['sub-region'] == 'Polynesia').unique()

Sub_Saharan_Africa = continents_dataset['name']._where(continents_dataset['sub-region'] == 'Sub-Saharan Africa').unique()

Latin_America = continents_dataset['name']._where(continents_dataset['sub-region'] == 'Latin America and the Caribbean').unique()

Western_Asia = continents_dataset['name']._where(continents_dataset['sub-region'] == 'Western Asia').unique()

Australia_and_Zealand = continents_dataset['name']._where(continents_dataset['sub-region'] == 'Australia and New Zealand').unique()

Western_Europe = continents_dataset['name']._where(continents_dataset['sub-region'] == 'Western Europe').unique()

Eastern_Europe = continents_dataset['name']._where(continents_dataset['sub-region'] == 'Eastern Europe').unique()

Northern_America = continents_dataset['name']._where(continents_dataset['sub-region'] == 'Northern America').unique()

South_Eastern_Asia = continents_dataset['name']._where(continents_dataset['sub-region'] == 'South-eastern Asia').unique()

Eastern_Asia = continents_dataset['name']._where(continents_dataset['sub-region'] == 'Eastern Asia').unique()

Melanesia = continents_dataset['name']._where(continents_dataset['sub-region'] == 'Melanesia').unique()

Micronesia = continents_dataset['name']._where(continents_dataset['sub-region'] == 'Micronesia').unique()

Central_Asia = continents_dataset['name']._where(continents_dataset['sub-region'] == 'Central Asia').unique()


#print(Southern_Europe)
#%% md
#### Faccio un match per ogni zona tra gli stati del dataset e quelli del dataset di supporto
#%%
sub_regions = []
for nation in dataset.States:
    if nation in Southern_Asia:
        sub_regions.append('Southern Asia')
    elif nation in Northern_Europe:
        sub_regions.append('Northern Europe')
    elif nation in Southern_Europe:
        sub_regions.append('Southern Europe')
    elif nation in Northern_Africa:
        sub_regions.append('Northern Africa')
    elif nation in Polynesia:
        sub_regions.append('Polynesia')
    elif nation in Sub_Saharan_Africa:
        sub_regions.append('Sub-Saharan Africa')
    elif nation in Latin_America:
        sub_regions.append('Latin America and the Caribbean')
    elif nation in Western_Asia:
        sub_regions.append('Western Asia')
    elif nation in Australia_and_Zealand:
        sub_regions.append('Australia and New Zealand')
    elif nation in Western_Europe:
        sub_regions.append('Western Europe')
    elif nation in Eastern_Europe:
        sub_regions.append('Eastern Europe')
    elif nation in Northern_America:
        sub_regions.append('Northern America')
    elif nation in South_Eastern_Asia:
        sub_regions.append('South-eastern Asia')
    elif nation in Eastern_Asia:
        sub_regions.append('Eastern Asia')
    elif nation in Melanesia:
        sub_regions.append('Melanesia')
    elif nation in Micronesia:
        sub_regions.append('Micronesia')
    elif nation in Central_Asia:
        sub_regions.append('Central Asia')
    else: sub_regions.append(nation)

print(sorted(set(sub_regions)))
#%% md
#### Classifico manualmente alcuni paesi che sono rimasti fuori dal match
#%%
sub_regions2 = []
for sub in sub_regions:
    sub_regions2.append(sub.replace('Timor', 'South-eastern Asia').
                        replace('Sardinia', 'Southern Europe').
                        replace('Chechnya', 'Western Asia').
                        replace('Trinidad', 'Latin America and the Caribbean').
                        replace('Bosnia and Herzegovina', 'Canada').
                        replace('Borneo', 'South-eastern Asia').
                        replace('Somaliland', 'Sub-Saharan Africa').
                        replace('Brunei', 'South-eastern Asia').
                        replace('Czechoslovakia', 'Eastern Europe').
                        replace('Yugoslavia', 'Southern Europe').
                        replace('Himalayas', 'Southern Asia').
                        replace('Tasmania', 'Sub-Saharan Africa').
                        replace('Tahiti', 'Australia and New Zealand').
                        replace('Rhodesia', 'Sub-Saharan Africa').
                        replace('Kosovo', 'Southern Europe').
                        replace('Korea', 'Eastern Asia').
                        replace('Costa Costa Rica', 'Latin America and the Caribbean').
                        replace('Bosnia', 'Southern Europe').
                        replace('Principe', 'Sub-Saharan Africa').
                        replace('Emirates', 'Western Asia').
                        replace('Morroco', 'Northern Africa').
                        replace('Democratic Republic of Congo', 'Sub-Saharan Africa').
                        replace('Antilles', 'Latin America and the Caribbean').
                        replace('USSR', 'Eastern Europe'))

print(sorted(set(sub_regions2)))
#%% md
#### Creo la nuova colonna con i sub_continenti
#%%
dataset = dataset.assign(Sub_Regions=sub_regions2)
#%%
dataset.Sub_Regions
#%% md
#### Infine controllo le ultime osservazioni che non sono utili ai fini dell'analisi
#%%
count_Africa = 0
count_Base = 0
count_channel = 0
count_newfoundland = 0
count_Ocean = 0
count_Sea = 0
count_sound = 0
count_station = 0
count_Territory = 0
count_island = 0
count_islands = 0
count_airport = 0
count_coast = 0
count_gulf = 0
count_republic = 0
count_USSR = 0

for i in sub_regions2:
    if i == 'Africa':
        count_Africa+=1
    elif i == 'Base':
        count_Base+=1
    elif i == 'Channel':
        count_channel+=1
    elif i == 'Newfoundland':
        count_newfoundland+=1
    elif i == 'Ocean':
        count_Ocean+=1
    elif i == 'Sea':
        count_Sea+=1
    elif i == 'Sound':
        count_sound+=1
    elif i == 'Station':
        count_station+=1
    elif i == 'Territory':
        count_Territory+=1
    elif i == 'Island':
        count_island+=1
    elif i == 'Islands':
        count_islands+=1
    elif i == 'Airport':
        count_airport+=1
    elif i == 'Coast':
        count_coast+=1
    elif i == 'Gulf':
        count_gulf+=1
    elif i == 'Republic':
        count_republic+=1
    elif i == 'USSR':
        count_USSR+=1


print(
    count_Africa,
    count_Base,
    count_channel,
    count_newfoundland,
    count_Ocean,
    count_Sea,
    count_sound,
    count_station,
    count_Territory,
    count_island,
    count_islands,
    count_airport,
    count_coast,
    count_gulf,
    count_republic,
    count_USSR
)
# Totale: 175
#da eliminare sicuro: Territory, Station, Sound, Base, Channel, Newfoundland, gulf, airport, coast,
# Valutare anche le altre, io eliminerei tutto tranne 'Africa' perché 1) 175 non sono troppe, 2) sono generiche e non è possibile avere una localizzazione geografica.
#%% md
#### E alcune decido di eliminarle (tutte tranne 'Africa')
#%%
dataset = dataset[dataset.Sub_Regions != 'Territory']
dataset = dataset[dataset.Sub_Regions != 'Station']
dataset = dataset[dataset.Sub_Regions != 'Sound']
dataset = dataset[dataset.Sub_Regions != 'Base']
dataset = dataset[dataset.Sub_Regions != 'Channel']
dataset = dataset[dataset.Sub_Regions != 'Newfoundland']
dataset = dataset[dataset.Sub_Regions != 'Ocean']
dataset = dataset[dataset.Sub_Regions != 'Island']
dataset = dataset[dataset.Sub_Regions != 'Islands']
dataset = dataset[dataset.Sub_Regions != 'Airport']
dataset = dataset[dataset.Sub_Regions != 'Coast']
dataset = dataset[dataset.Sub_Regions != 'Gulf']
dataset = dataset[dataset.Sub_Regions != 'Republic']
dataset = dataset[dataset.Sub_Regions != 'Sea']
#%%
dataset.Sub_Regions
#%% md
#### Adesso vado a creare un'altra variabile che racchiude le macro-aree in continenti
#%%
dataset.Sub_Regions.unique()
#%%
continents_dataset.region.unique()
#%% md
#### Creo una variabile per ogni continente utilizzando il dataset di supporto
#%%
Asia = continents_dataset['sub-region']._where(continents_dataset['region'] == 'Asia').unique()

Europe = continents_dataset['sub-region']._where(continents_dataset['region'] == 'Europe').unique()

Africa = continents_dataset['sub-region']._where(continents_dataset['region'] == 'Africa').unique()

America = continents_dataset['sub-region']._where(continents_dataset['region'] == 'Americas').unique()

Oceania = continents_dataset['sub-region']._where(continents_dataset['region'] == 'Oceania').unique()

print(Africa)
#%% md
#### Faccio il matching tra le macroaree precedentemente definite
#%%
regions = []
for sub_region in dataset.Sub_Regions:
    if sub_region in Asia:
        regions.append('Asia')
    elif sub_region in Europe:
        regions.append('Europe')
    elif sub_region in Africa:
        regions.append('Africa')
    elif sub_region in America:
        regions.append('America')
    elif sub_region in Oceania:
        regions.append('Oceania')
    else: regions.append(sub_region)

print(sorted(set(regions)))
#%% md
#### creo la nuova variabile e la aggiungo al dataset
#%%
dataset = dataset.assign(Continent=regions)
#%%
dataset
#%% md
## Estrazione delle città in cui è caduto (Non utilizziamo per ora)
#%%
cities_location = []
for city in dataset.Location:
    cities_location.append(re.findall("^(.+?),", str(city)))

print(cities_location)
#%%
tmp_cities = []
for i in cities_location:
    for w in i:
        tmp_cities.append(w)

print(tmp_cities)
#%%
tmp_cities_cleaned = []
for i in tmp_cities:
    tmp_cities_cleaned.append(re.sub(rf"[^\w\s]", "", i))

print(tmp_cities_cleaned)
#%%
print(len(sorted(set(tmp_cities_cleaned))))
print(sorted(set(tmp_cities_cleaned)))
#%%
cities_dataset.state_name.unique()
#%%
matched_cities = []
no_matched_cities = []
for city in tmp_cities_cleaned:
    if city in list(cities_dataset.state_name.unique()):
        matched_cities.append(city)
    else: no_matched_cities.append(city)

print(matched_cities)
print(len(no_matched_cities))
#%% md

#    Leo
#%% md
Change data format

#%%
print(dataset['Date'])
#%% md

#%%
new_date = []
#%%
for i in dataset.Date:
    #print (re.findall('[0-9]{4}',i))
    new_date.append(*re.findall('[0-9]{4}', i))
    #a = a.append(i[i.re.findall('[0-9]{4}',i)])
print(new_date)

#%%
dataset = dataset.assign(Year=new_date)
#%%
dataset.columns
#%%
print(type(dataset.Year))
#%%
for i in dataset.Year:
    print(type(i))
#%%
dataset["Year"] = dataset["Year"].astype(int)
#%% md
La colonna Date è rimasta all'interno del dataset senza subire modifiche, è stata invece aggiunta una nuova colonna denominata Year contenente solo l'anno presente nella colonna Date, al fine di eliminare il problemma di disomogeneità dei dati a causa dei diversi formati dd/mm/yyyy e mm/dd/yyyy presenti nel dataset a causa delle differene fra sistema anglosassone ed europeo.
#%% md

#%% md
Ovviamente nel codice sono presenti dei print esclusivamente a fini di comprensione del lavoro che possono essere eliminati nella versione finale.
#%% md
###     Osservazione variabile Time

#%%
ore = []
#%%
for i in dataset.Time:
    #if type(i) == float:
    #   print(i)
    if type(i) == str:
        ore.append(i)

print(ore, len(ore))
#%%
bbb = 0
for i in dataset.Time:
    if type(i) == float:
        bbb = bbb + 1
print(bbb)
#%%
bb = 0
for i in dataset.Time:
    if type(i) == str:
        bb = bb + 1
print(bb)
#%%
new_ore = []
for i in ore:
    #print(i,re.sub(rf"[:].*","",i))
    #i = (re.sub(rf"[:].*","",i))
    new_ore.append(re.sub(rf"[:].*", "", i))
print(new_ore, len(new_ore))


#%%
f = 0
for i in new_ore:
    i = int(i)
    f = f + 1
    #print(i,type(i))
print(f)
#%%
int_ore = []
for i in new_ore:
    int_ore.append(int(i))
print(len(int_ore), int_ore, type(int_ore[2]))
#%%
# dataset = dataset.assign(Hour=new_ore)
#%%
int_ore = []
for i in new_ore:
    int_ore.append(int(i))
print(len(int_ore), int_ore, type(int_ore[2]))
#%%
for i in int_ore:
    if i > 24:
        print(i)
import math
import numpy

print(numpy.mean(int_ore))
#%%

patches = plt.hist(int_ore)
# np.arange()

plt.xlabel("Values")
plt.ylabel("Frequency")
plt.title("Histogram")
plt.show()
#%%
#dataset=dataset.assign(Hour=new_ore)
#%% md
##### Si è scelto di non utilizzare la colonna Time in quanto poco significativa come distribuzione e poiché presenta un 30% circa di nan
#%% md
# Analisi variabili fatalities, crew and passengers e ripartizione fatalities

#%% md
#### Commenta sti cazzo di print

#%%
dataset.keys()
#%%
print(np.max(dataset.Fatalities), np.min(dataset.Fatalities), np.mean(dataset.Fatalities),
      np.median(dataset.Fatalities), np.nanmedian(dataset.Fatalities))
print(np.max(dataset["Ground"]), np.max(dataset["Fatalities"]), np.max(dataset["Fatalities Passangers"]),
      np.max(dataset["Fatalities Crew"]))
print(dataset.shape)
dataset = dataset[dataset["Fatalities"].notna()]
dataset = dataset[dataset["Fatalities Crew"].notna()]
dataset = dataset[dataset["Fatalities Passangers"].notna()]
dataset = dataset[dataset["Ground"].notna()]
print(dataset.shape)
#%%
new_fat = []
new_pass = []
new_ground = []
new_crew = []
for position, i in enumerate(dataset[
                                 "Fatalities"]):  ##try and except per gestione na presenti nel dataset originali, tenuti per scelta stilistica e non per motivi computazionali
    try:
        total_death = (dataset["Fatalities Crew"].iloc[position] + dataset["Fatalities Passangers"].iloc[position] +
                       dataset["Ground"].iloc[position])
        diff_death = i - total_death
        if i == total_death:
            new_fat.append(i)
            new_crew.append(dataset["Fatalities Crew"].iloc[position])
            new_pass.append(dataset["Fatalities Passangers"].iloc[position])
            new_ground.append(dataset["Ground"].iloc[position])
        elif i > total_death:
            new_fat.append(i)
            new_crew.append(dataset["Fatalities Crew"].iloc[position])
            new_pass.append(dataset["Fatalities Passangers"].iloc[position])
            new_ground.append(dataset["Ground"].iloc[position])
        elif i < total_death:
            i = total_death
            new_fat.append(i)
            new_crew.append(dataset["Fatalities Crew"].iloc[position])
            new_pass.append(dataset["Fatalities Passangers"].iloc[position])
            new_ground.append(dataset["Ground"].iloc[position])
    except:
        new_fat.append(i)
        new_crew.append(dataset["Fatalities Crew"].iloc[position])
        new_pass.append(dataset["Fatalities Passangers"].iloc[position])
        new_ground.append(dataset["Ground"].iloc[position])
print(len(new_fat), "new fat")
print(len(new_ground), "new gr")
print(len(new_pass), "new pass")
print(len(new_crew), "new crew")
#%%
dataset = dataset.assign(new_fat=new_fat, new_crew=new_crew, new_pass=new_pass, new_ground=new_ground)
dataset
#%%
print(dataset.shape)
dataset = dataset[dataset["Aboard"].notna()]
dataset = dataset[dataset["Aboard Passangers"].notna()]
dataset = dataset[dataset["Aboard Crew"].notna()]
print(dataset.shape)
#%%
new_aboard = []
new_aboard_pass = []
new_aboard_crew = []
for position, i in enumerate(dataset.Aboard):
    try:
        total_ab = (dataset["Aboard Passangers"].iloc[position] + dataset["Aboard Crew"].iloc[position])
        if i == total_ab:
            print("tutto ok", i, dataset["Aboard Crew"].iloc[position], dataset["Aboard Passangers"].iloc[position])
            new_aboard.append(i)
            new_aboard_crew.append(dataset["Aboard Crew"].iloc[position])
            new_aboard_pass.append(dataset["Aboard Passangers"].iloc[position])
        else:
            print("nada ok", i, dataset["Aboard Crew"].iloc[position], dataset["Aboard Passangers"].iloc[position])
            i = total_ab
            new_aboard.append(i)
            new_aboard_crew.append(dataset["Aboard Crew"].iloc[position])
            new_aboard_pass.append(dataset["Aboard Passangers"].iloc[position])
    except:
        print("mannaggia")
#%%
print(dataset.shape)
dataset = dataset.assign(new_aboard=new_aboard, new_aboard_crew=new_aboard_crew, new_aboard_pass=new_aboard_pass)
dataset
#%% md
# Il codice quà sotto serve?
#%%
print(dataset["Aboard"], new_aboard)
coo = 0
dataset = dataset[dataset["Fatalities"].notna()]
for position, i in enumerate(dataset.Fatalities):
    #if type(i) != float:
    if i == 0.0:
        print("fata", "fata crew", "fata pass")
        print(i, dataset["Fatalities Crew"].iloc[position], dataset["Fatalities Passangers"].iloc[position])
        coo = coo + 1
print(coo)
#%%
def na_counter_for_numeric_column(column, nome_colonna):
    nas = []
    for value in column:
        try:
            int(value)
        except:
            nas.append(value)
    return print(f"Numero di Na della colonna {nome_colonna}: {len(nas)}")


na_counter_for_numeric_column(dataset["Aboard"], "Aboard")
na_counter_for_numeric_column(dataset["Aboard Crew"], "Aboard Crew")
na_counter_for_numeric_column(dataset["Aboard Passangers"], "Aboard Passangers")
na_counter_for_numeric_column(dataset["Fatalities"], "Fatalities")
na_counter_for_numeric_column(dataset["Fatalities Crew"], "Fatalities Crew")
na_counter_for_numeric_column(dataset["Fatalities Passangers"], "Fatalities Passangers")
na_counter_for_numeric_column(dataset["Ground"], "Ground")

""" La parte quà sotto era già stata fatta """
# print(dataset.shape)
# dataset = dataset[dataset["Fatalities"].notna()]
# dataset = dataset[dataset["Fatalities Crew"].notna()]
# dataset = dataset[dataset["Fatalities Passangers"].notna()]
# dataset = dataset[dataset["Ground"].notna()]
# print(dataset.shape)
# print(np.mean(dataset("")))
# dataset = dataset[dataset["Ground"].notna()]
dataset.keys()
# dataset = dataset.assign(new_fat=new_fat, new_crew=new_crew)
#%% md
# Eliminazione Variabili (maic)
#%%

col_to_del = ['Date', 'Time', 'Location', 'Flight #', 'Registration', 'cn/ln', 'state_location', 'Ac Type', 'Route',
              'Fatalities', 'Fatalities Crew', 'Fatalities Passangers', 'Grounds']

dataset_def = dataset
for col in dataset_def.columns:
    if col in col_to_del:
        dataset_def = dataset_def.drop(col, axis=1)

dataset_def
#%% md
# Grafi (Gabro)
#%%
import networkx as nx
#%%
nodes = nx.Graph()
#%%
nodes.add_nodes_from(dataset["Aeroporto_di_partenza"])
#%%
nx.draw(nodes)
#%%
test = nx.Graph()
test.add_edge("a", "b")
test.add_edge("b", "c")
test.add_edge("c", "a")

nx.draw(test)
#%% md
Ok bisogna creare un dizionario con tutti i nomi degli aeroporti come chiavi e come valori gli aeroporti con i quali sono collegati.
#%% md
Sistemare il codice facendo una funzione
#%%
print(len(dataset_def["Aeroporto_di_partenza"].unique()))
univ_aerop = [i for i in dataset_def["Aeroporto_di_partenza"].unique() if type(i) != float]

for aer in dataset_def["Aeroporto_2"].unique():
    if aer not in univ_aerop and type(aer) != float: univ_aerop.append(aer)

for aer in dataset_def["Aeroporto_3"].unique():
    if aer not in univ_aerop and type(aer) != float: univ_aerop.append(aer)

for aer in dataset_def["Aeroporto_4"].unique():
    if aer not in univ_aerop and type(aer) != float: univ_aerop.append(aer)

for aer in dataset_def["Aeroporto_5"].unique():
    if aer not in univ_aerop and type(aer) != float: univ_aerop.append(aer)

for aer in dataset_def["Aeroporto_6"].unique():
    if aer not in univ_aerop and type(aer) != float: univ_aerop.append(aer)

for aer in dataset_def["Aeroporto_di_destinazione"].unique():
    if aer not in univ_aerop and type(aer) != float: univ_aerop.append(aer)
print(len(univ_aerop))
#%% md
#### Creazione lista di tuple
#%% md
Creare lista di tuple che contiene i nodi e i collegamenti tra di loro a due a due. In ogni tupla ci saranno due nodi, in ordine alfabetico in modo da evitare doppioni.
#%%
edges = []
for aeroport in univ_aerop:
    if aeroport in aeroporto_partenza:
        for position, i in enumerate(aeroporto_partenza):
            if i == aeroport:
                mini_edge = sorted([aeroport, aeroporto_2[position]])
                if aeroporto_2[position] != "Nan" and mini_edge not in edges:
                    edges.append(mini_edge)
                elif aeroporto_2[position] == "Nan" and aeroporto_di_destinazione[position] != "Nan":
                    mini_edge = sorted([aeroport, aeroporto_di_destinazione[position]])
                    if mini_edge not in edges:
                        edges.append(mini_edge)

    elif aeroport in aeroporto_2:
        for position, i in enumerate(aeroporto_2):
            if i == aeroport:
                mini_edge = sorted([aeroport, aeroporto_3[position]])
                if aeroporto_3[position] != "Nan" and mini_edge not in edges:
                    edges.append(mini_edge)
                elif aeroporto_3[position] == "Nan" and aeroporto_di_destinazione[position] != "Nan":
                    mini_edge = sorted([aeroport, aeroporto_di_destinazione[position]])
                    if mini_edge not in edges:
                        edges.append(mini_edge)

    elif aeroport in aeroporto_3:
        for position, i in enumerate(aeroporto_3):
            if i == aeroport:
                mini_edge = sorted([aeroport, aeroporto_4[position]])
                if aeroporto_4[position] != "Nan" and mini_edge not in edges:
                    edges.append(mini_edge)
                elif aeroporto_4[position] == "Nan" and aeroporto_di_destinazione[position] != "Nan":
                    mini_edge = sorted([aeroport, aeroporto_di_destinazione[position]])
                    if mini_edge not in edges:
                        edges.append(mini_edge)

    elif aeroport in aeroporto_4:
        for position, i in enumerate(aeroporto_4):
            if i == aeroport:
                mini_edge = sorted([aeroport, aeroporto_5[position]])
                if aeroporto_5[position] != "Nan" and mini_edge not in edges:
                    edges.append(mini_edge)
                elif aeroporto_5[position] == "Nan" and aeroporto_di_destinazione[position] != "Nan":
                    mini_edge = sorted([aeroport, aeroporto_di_destinazione[position]])
                    if mini_edge not in edges:
                        edges.append(mini_edge)

    elif aeroport in aeroporto_5:
        for position, i in enumerate(aeroporto_5):
            if i == aeroport:
                mini_edge = sorted([aeroport, aeroporto_6[position]])
                if aeroporto_6[position] != "Nan" and mini_edge not in edges:
                    edges.append(mini_edge)
                elif aeroporto_6[position] == "Nan" and aeroporto_di_destinazione[position] != "Nan":
                    mini_edge = sorted([aeroport, aeroporto_di_destinazione[position]])
                    if mini_edge not in edges:
                        edges.append(mini_edge)

    elif aeroport in aeroporto_6:
        for position, i in enumerate(aeroporto_6):
            if i == aeroport:
                mini_edge = sorted([aeroport, aeroporto_di_destinazione[position]])
                if aeroporto_di_destinazione[position] != "Nan" and mini_edge not in edges:
                    edges.append(mini_edge)
                elif aeroporto_di_destinazione[position] == "Nan" and aeroporto_di_destinazione[position] != "Nan":
                    mini_edge = sorted([aeroport, aeroporto_di_destinazione[position]])
                    if mini_edge not in edges:
                        edges.append(mini_edge)

    elif aeroport in aeroporto_di_destinazione:
        for position, i in enumerate(aeroporto_di_destinazione):
            if i == aeroport:
                mini_edge = sorted([aeroport, aeroporto_di_destinazione[position]])
                if aeroporto_6[position] != "Nan":
                    edges.append(mini_edge)
                elif aeroporto_5[position] != "Nan":
                    edges.append(mini_edge)
                elif aeroporto_4[position] != "Nan":
                    edges.append(mini_edge)
                elif aeroporto_3[position] != "Nan":
                    edges.append(mini_edge)
                elif aeroporto_2[position] != "Nan":
                    edges.append(mini_edge)


# print(edges)
#%%
# class Graph(object):
#     def __init__(self):
#         self.nodes = {}
#
#     def V(self):
#         return self.nodes.keys()
#
#     def size(self):
#         return len(self.nodes)
#
#     def adj(self, u):
#         if u in self.nodes:
#             return self.nodes[u]
#
#     def insertNode(self, u):
#         if u not in self.nodes: self.nodes[u] = {}
#
#     def insertEdge(self, u, v, w=0):
#         self.insertNode(u)
#         self.insertNode(v)
#         self.nodes[u][v] = w
#
# g = Graph()
#
# for u, v in edges:
#     g.insertEdge(u, v)
#
# for u in g.V():
#     print(u, "->", g.adj(u))
#
# nx.draw(g.nodes)

from matplotlib.pyplot import figure
import random

gg = nx.Graph()

bubu = []
for i in edges:
    if "Paris" in i: bubu.append(i)
gg.add_edges_from(bubu)

figure(figsize=(25, 25), dpi=30)
nx.draw(gg, with_labels=True, font_weight='bold', pos=nx.spring_layout(gg))
plt.show()
#%%
b_graph = nx.Graph()

# new = pd.DataFrame(dataset_def["States"], dataset_def["New_Operator_column"])
# new
nx.from_pandas_edgelist(dataset_def, dataset_def["States"], dataset_def["New_Operator_column"])
