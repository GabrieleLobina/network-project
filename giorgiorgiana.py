#%% md
# Airplane_Crashes network
#%% md
###### Installazione importazioni librerie
#%%
import pandas as pd
import re
import matplotlib as mlt
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.axes as axes
import math
import seaborn as sb
#%% md
#### Importazione e osservazione dataset Airplane_crashes

#%%
dataset = pd.read_csv("datasets/Airplane_Crashes_and_Fatalities_Since_1908_20190820105639.csv")
dataset
#%% md
##### Importazione dataset che utilizzeremo successivamente
#%%
continents_dataset = pd.read_csv("datasets/continents2.csv")
cities_dataset = pd.read_csv("datasets/cities.csv")
world_cities_dataset = pd.read_csv("datasets/world-cities.csv")
#%% md
#### Prime rappresentazioni grafiche
#%% md
##### In questa griglia vengono rappresentante le distribuzioni di :
##### Fatalities - Aboard - Fatalities Crew - Fatalities Passangers
#%%
fig, axes = plt.subplots(2, 2, figsize=(20, 12))
plt.grid()
axes[0, 0].hist(dataset['Fatalities'])
axes[0, 0].set_xlabel('Fatalities')
axes[0, 0].set_ylabel('Count')
axes[0, 0].set_title('Fatalities')

axes[0, 1].hist(dataset['Aboard'], bins=15,color="pink")
plt.grid()
axes[0, 1].set_xlabel('Aboard')
axes[0, 1].set_ylabel('Count')
axes[0, 1].set_title('Aboard')

# first two is using a matplotlib syntax, the next two I'll do with seaborn

axes[1, 0].set_title('Fatalities Crew')
plt.grid()
sb.histplot(dataset, x='Fatalities Crew', ax=axes[1, 0], kde=True,color="darkgreen")
axes[1, 0].set_xlabel('Fatalities Crew')
axes[1, 0].set_ylabel('Count')

axes[1, 1].set_title('Fatalities Passangers')
plt.grid()
sb.histplot(dataset, x='Fatalities Passangers', ax=axes[1, 1], kde=True,color="grey")
axes[1, 1].set_xlabel('Fatalities Passangers')
axes[1, 1].set_ylabel('Count')
plt.tight_layout(pad=2)
plt.show()
#%% md
## Pulizia dataset Airplane_crashes
#%% md
#### Eliminazione variabili poco rilevanti
#%%
col_trash = ['Flight #','Registration','cn/ln','Summary','Time']

dataset_1st = dataset
for col in dataset_1st.columns:
    if col in col_trash:
        dataset_1st = dataset_1st.drop(col, axis=1)

dataset_1st
#%% md
#### Osservazione presenza Na e gestione degli Na
#%% md
###### Cleaning colonna **Operator**
#%%
print("numero di Na:", len([i for i in dataset_1st.Operator if type(i) == float]))  # abbiamo solo 10 Na
print(dataset_1st.shape)
# Eliminazione righe contenenti Na nella colonna Operator
dataset_1st = dataset_1st[dataset_1st['Operator'].notna()]
print(dataset_1st.shape)
#%%
print("numero di NaN nella colonna Route:",
      len([i for i in dataset_1st.Route if type(i) == float]))  # 770.. da gestire
#%% md
##### Controllo valori nulli delle colonne:
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


na_counter_for_numeric_column(dataset_1st["Aboard"], "Aboard")
na_counter_for_numeric_column(dataset_1st["Aboard Crew"], "Aboard Crew")
na_counter_for_numeric_column(dataset_1st["Aboard Passangers"], "Aboard Passangers")
na_counter_for_numeric_column(dataset_1st["Fatalities"], "Fatalities")
na_counter_for_numeric_column(dataset_1st["Fatalities Crew"], "Fatalities Crew")
na_counter_for_numeric_column(dataset_1st["Fatalities Passangers"], "Fatalities Passangers")
na_counter_for_numeric_column(dataset_1st["Ground"], "Ground")
#%% md
##### Check degli NA nella colonna Location

#%%
print("numero di NaN nella colonna Location:", len([i for i in dataset.Location if type(i) == float]))  # Non abbiamo NA
#%% md
### Gestione variabili e creazione nuove variabili per implementare l’analisi
#%% md
#### Identificazione e raggruppamento categoria di operatore militare
#%%
print("numero di operatori univoci:", len(dataset_1st['Operator'].unique()))

military_flights = []

military_words = ["army", "navy", "marine", "military", "force", "airforce", "amee de l'air", "mission"]

# Identifica tutti i nomi degli operatori che appartengono al campo militare
for operator in dataset_1st['Operator'].unique():
    for word in military_words:
        if word.lower() in operator.lower() and operator not in military_flights:
            military_flights.append(operator)

print("numero di operatori militari univoci:", len(military_flights))  # 251 valori univoci relativi
#%% md
#### Identificazione e raggruppamento categoria di operatore postale
#%%
postal_cargo_flights = []

postal_e_cargo_words = ["postal", "mail", "aeropostale", "cargo", "express", "commercial"]

# Identifica tutti i nomi degli operatori che appartengono al campo militare
for operator in dataset_1st['Operator'].unique():
    if type(operator) != float:
        for word in postal_e_cargo_words:
            if word.lower() in operator.lower() and operator not in postal_cargo_flights: postal_cargo_flights.append(
                operator)

print("numero di operatori postali/cargo univoci:", len(postal_cargo_flights))
#%% md
#### Identificazione e raggruppamento categoria di operatori privati
#%%
private_flights = []

private_words = ["priva"]

# Identifica tutti i nomi degli operatori che appartengono al campo militare
for operator in dataset_1st['Operator'].unique():
    if type(operator) != float:
        for word in private_words:
            if word.lower() in operator.lower() and operator not in private_flights: private_flights.append(operator)

print("numero di operatori privati:", len(private_flights))
#%% md
#### Aggiunta valori per le nuove colonne
#%%
new_column = []

for value in dataset_1st.Operator:
    if value in military_flights:
        new_column.append("Military flight")
    elif value in postal_cargo_flights:
        new_column.append("Postal/Cargo flight")
    elif value in private_flights:
        new_column.append("Private flights")
    else:
        new_column.append("Scheduled flight")
#%%
dataset_1st = dataset_1st.assign(New_Operator_column=new_column)
dataset_1st
#%% md
#### Aggiunta colonna Aeroporto_di_partenza
#%%
rotte = []

for position, route in enumerate(dataset_1st.Route):
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
                new_route.append(re.sub(f",.+", "", aeroport.strip()))
            elif "-" in aeroport:
                a = re.sub(f"-", " ", aeroport.strip())
                new_route.append(" ".join(a.split()))
            elif aeroport[0] == " ":
                new_route.append(aeroport[1:])
                new_route.append(aeroport.strip())
            else:
                new_route.append(aeroport)
    elif type(route) == float and dataset_1st["New_Operator_column"].iloc[position] == "Military flight":
        new_route.append("Informazione riservata")
    else:
        new_route.append("Sconosciuto")
    rotte_pulite.append(new_route)

#print(rotte_pulite)
#for i in rotte_pulite:
    #print(i)
#%%
# Aggiunta colonna Aeroporto_di_partenza

aeroporto_partenza = [aeroporto[0] for aeroporto in rotte_pulite]
dataset_1st = dataset_1st.assign(Aeroporto_di_partenza=aeroporto_partenza)

dataset_1st
#%% md
#### Aggiunta colonne per aeroporti intermedi
Il numero massimo di aeroporti nelle rotte è 7 quindi andranno create 7 nuove colonne
#%%
aeroporto_2 = []
aeroporto_3 = []
aeroporto_4 = []
aeroporto_5 = []
aeroporto_6 = []
ultimo_aeroporto = []


for n_aeroporti in rotte_pulite:
    if len(n_aeroporti) == 1:
        ultimo_aeroporto.append(n_aeroporti)
        aeroporto_2.append("Nan")
        aeroporto_3.append("Nan")
        aeroporto_4.append("Nan")
        aeroporto_5.append("Nan")
        aeroporto_6.append("Nan")
    if len(n_aeroporti) == 2:
        ultimo_aeroporto.append(n_aeroporti[-1])
        aeroporto_2.append("Nan")
        aeroporto_3.append("Nan")
        aeroporto_4.append("Nan")
        aeroporto_5.append("Nan")
        aeroporto_6.append("Nan")
    if len(n_aeroporti) == 3:
        aeroporto_2.append(n_aeroporti[1])
        ultimo_aeroporto.append(n_aeroporti[-1])
        aeroporto_3.append("Nan")
        aeroporto_4.append("Nan")
        aeroporto_5.append("Nan")
        aeroporto_6.append("Nan")
    if len(n_aeroporti) == 4:
        aeroporto_2.append(n_aeroporti[1])
        aeroporto_3.append(n_aeroporti[2])
        ultimo_aeroporto.append(n_aeroporti[-1])
        aeroporto_4.append("Nan")
        aeroporto_5.append("Nan")
        aeroporto_6.append("Nan")
    if len(n_aeroporti) == 5:
        aeroporto_2.append(n_aeroporti[1])
        aeroporto_3.append(n_aeroporti[2])
        aeroporto_4.append(n_aeroporti[3])
        ultimo_aeroporto.append(n_aeroporti[-1])
        aeroporto_5.append("Nan")
        aeroporto_6.append("Nan")
    if len(n_aeroporti) == 6:
        aeroporto_2.append(n_aeroporti[1])
        aeroporto_3.append(n_aeroporti[2])
        aeroporto_4.append(n_aeroporti[3])
        aeroporto_5.append(n_aeroporti[4])
        ultimo_aeroporto.append(n_aeroporti[-1])
        aeroporto_6.append("Nan")
    if len(n_aeroporti) == 7:
        aeroporto_2.append(n_aeroporti[1])
        aeroporto_3.append(n_aeroporti[2])
        aeroporto_4.append(n_aeroporti[3])
        aeroporto_5.append(n_aeroporti[4])
        aeroporto_6.append(n_aeroporti[5])
        ultimo_aeroporto.append(n_aeroporti[-1])

# Alcuni valori di aeroporto_di destinazione erano in una lista. Risolviamo:
for position, aeroporto in enumerate(ultimo_aeroporto):
    if type(aeroporto) == list:
        ultimo_aeroporto[position] = aeroporto[0]

dataset_1st = dataset_1st.assign(Aeroporto_2=aeroporto_2,
                         Aeroporto_3=aeroporto_3,
                         Aeroporto_4=aeroporto_4,
                         Aeroporto_5=aeroporto_5,
                         Aeroporto_6=aeroporto_6,
                         Ultimo_aeroporto=ultimo_aeroporto)

dataset_1st
#%% md
### Cleaning AC type
#%%
print(len(dataset_1st["AC Type"].unique()))
simplified_aircraft_names = []
# Eliminazione dei pattern tipo "15-L ..." e "V-17 ..."
for airplane in dataset_1st["AC Type"]:
    if type(airplane) != float and len(airplane.split()) > 1:
        simplified_aircraft_names.append(re.sub(r"[A-Z0-9]+-.+", "", airplane).strip().upper())
    else:
        simplified_aircraft_names.append(airplane)

# Eliminazione dei pattern tipo "15.L ..." e "V.17 ..."
simplified_aircraft_names_1 = []
for position, airplane in enumerate(simplified_aircraft_names):
    if type(airplane) != float and len(airplane.split()) > 1:
        simplified_aircraft_names_1.append(re.sub(r"[A-Z0-9]+\.(.)+", "", airplane).strip())
    else:
        simplified_aircraft_names_1.append(airplane)

print(simplified_aircraft_names_1)
#%%
dataset_1st = dataset_1st.assign(AC_Type_simplified=simplified_aircraft_names_1)
print(f"Prima della pulizia: {len(dataset_1st['AC Type'].unique())} valori univoci")
print(f"Dopo la pulizia: {len(dataset_1st['AC_Type_simplified'].unique())} valori univoci")
#%% md
#### Change data format

#%%
print(dataset_1st['Date'])
#%%
new_date = []
#%%
for i in dataset_1st.Date :
    new_date.append(*re.findall('[0-9]{4}',i))
print(new_date)

#%%
dataset_1st = dataset_1st.assign(Year=new_date)
#%% md
##### Controlliamo che la variabile sia presente e la sua tipologia
#%%
dataset_1st.columns
#%%
for i in dataset_1st.Year:
    print(type(i))
#%%
dataset_1st["Year"] = dataset_1st["Year"].astype(int)
#%% md
La colonna Date è rimasta all'interno del dataset senza subire modifiche, è stata invece aggiunta una nuova colonna denominata Year contenente solo l'anno presente nella colonna Date, al fine di eliminare il problemma di disomogeneità dei dati a causa dei diversi formati dd/mm/yyyy e mm/dd/yyyy presenti nel dataset a causa delle differene fra sistema anglosassone ed europeo.
#%% md
##### Si è deciso di aggiungere una variabile di nome decadi in modo da poter osservare l'aggregazione dei dati.
#%%
decadi=[]
for i in dataset_1st["Year"]:
    if i >= 1900 and i <= 1910:
        i = "1910_20"
        decadi.append(i)
    elif i > 1910 and i <= 1920:
        i = "1910_20"
        decadi.append(i)
    elif i > 1920 and i <= 1930:
        i = "1920_30"
        decadi.append(i)
    elif i > 1930 and i <= 1940:
        i = "1930_40"
        decadi.append(i)
    elif i > 1940 and i <= 1950:
        i = "1940_50"
        decadi.append(i)
    elif i > 1950 and i <= 1960:
        i = "1950_60"
        decadi.append(i)
    elif i > 1960 and i <= 1970:
        i = "1960_70"
        decadi.append(i)
    elif i > 1970 and i <= 1980:
        i = "1970_80"
        decadi.append(i)
    elif i > 1980 and i <= 1990:
        i = "1980_90"
        decadi.append(i)
    elif i > 1990 and i <= 2000:
        i = "1990_00"
        decadi.append(i)
    elif i > 2000 and i <= 2010:
        i = "2000_10"
        decadi.append(i)
    elif i > 2010 and i <= 2020:
        i = "2010_20"
        decadi.append(i)
    elif i > 2020 and i <= 2030:
        i = "2020_30"
        decadi.append(i)
    else:
        pass
print(decadi)
#%%
from matplotlib import cm
from matplotlib.pyplot import figure

cs = sb.color_palette("tab20")
#cs =["darkgrey","darkred","green","purple","aqua","blue","yellow","sienna","orangered","deeppink","springgreen","violet", "pink","dodgerblue"]

dataset_1st=dataset_1st.assign(decadi=decadi)
#dz = dict(df["Q5"].drop(0).value_counts())
dz=dict(dataset_1st["decadi"].drop(0).value_counts())
sb.set_style("whitegrid")
pie, ax = plt.subplots(figsize=[10,12])
Labels = [k for k in dz.keys()]
Data   = [float(v) for v in dz.values()]
plt.pie(x = Data, labels=Labels, autopct="%.1f%%", pctdistance=0.5, colors=cs);
plt.title("Frequency of Decadi", fontsize=14);
#%% md
### Analisi variabili fatalities, crew and passengers e ripartizione fatalities

#%%
print(np.max(dataset_1st.Fatalities), np.min(dataset_1st.Fatalities), np.mean(dataset_1st.Fatalities),
      np.median(dataset_1st.Fatalities), np.nanmedian(dataset_1st.Fatalities))
print(np.max(dataset_1st["Ground"]), np.max(dataset_1st["Fatalities"]), np.max(dataset_1st["Fatalities Passangers"]),
      np.max(dataset_1st["Fatalities Crew"]))
print(dataset_1st.shape)
dataset_1st = dataset_1st[dataset_1st["Fatalities"].notna()]
dataset_1st = dataset_1st[dataset_1st["Fatalities Crew"].notna()]
dataset_1st = dataset_1st[dataset_1st["Fatalities Passangers"].notna()]
dataset_1st = dataset_1st[dataset_1st["Ground"].notna()]
print(dataset_1st.shape)
#%% md
##### Qui creiamo nuove variabili per fare in modo che fatalities rappresenti la somma delle sue componenti, e che nel caso fatalities sia maggiore di questa somma la differenza venga aggiunga a new_fatalities_crew
#%%
new_fatalities = []
new_fatalities_passangers = []
new_ground = []
new_fatalities_crew = []
for position, i in enumerate(dataset_1st["Fatalities"]):
    ##try and except per gestione na presenti nel dataset originali, tenuti per scelta stilistica e non per motivi computazionali
    try:
        total_death = (dataset_1st["Fatalities Crew"].iloc[position] + dataset_1st["Fatalities Passangers"].iloc[position] +
                       dataset_1st["Ground"].iloc[position])
        diff_death = i - total_death
        if i == total_death:
            new_fatalities.append(i)
            new_fatalities_crew.append(dataset_1st["Fatalities Crew"].iloc[position])
            new_fatalities_passangers.append(dataset_1st["Fatalities Passangers"].iloc[position])
            new_ground.append(dataset_1st["Ground"].iloc[position])
        elif i > total_death:
            new_fatalities.append(i)
            new_fatalities_crew.append(dataset_1st["Fatalities Crew"].iloc[position])
            new_fatalities_passangers.append(dataset_1st["Fatalities Passangers"].iloc[position])
            new_ground.append(dataset_1st["Ground"].iloc[position])
        elif i < total_death:
            i = total_death
            new_fatalities.append(i)
            new_fatalities_crew.append(dataset_1st["Fatalities Crew"].iloc[position])
            new_fatalities_passangers.append(dataset_1st["Fatalities Passangers"].iloc[position])
            new_ground.append(dataset_1st["Ground"].iloc[position])
    except:
        new_fatalities.append(i)
        new_fatalities_crew.append(dataset_1st["Fatalities Crew"].iloc[position])
        new_fatalities_passangers.append(dataset_1st["Fatalities Passangers"].iloc[position])
        new_ground.append(dataset_1st["Ground"].iloc[position])
print(len(new_fatalities), "new fatalities")
print(len(new_ground), "new ground")
print(len(new_fatalities_passangers), "new fatalities passangers")
print(len(new_fatalities_crew), "new fatalities crew")
#%% md
##### Inseriamo le nuove variabili nel dataset
#%%
dataset_1st = dataset_1st.assign(new_fatalities=new_fatalities, new_fatalities_crew=new_fatalities_crew, new_fatalities_passangers=new_fatalities_passangers, new_ground=new_ground)
dataset_1st
#%% md
###### Lo stesso passaggio precedente viene eseguito anche su Aboard con ripartizione su Aboard Crew
#%%
print(dataset_1st.shape)
dataset_1st = dataset_1st[dataset_1st["Aboard"].notna()]
dataset_1st = dataset_1st[dataset_1st["Aboard Passangers"].notna()]
dataset_1st = dataset_1st[dataset_1st["Aboard Crew"].notna()]
print(dataset_1st.shape)
#%%
new_aboard = []
new_aboard_passangers = []
new_aboard_crew = []
for position, i in enumerate(dataset_1st.Aboard):
    try:
        total_ab = (dataset_1st["Aboard Passangers"].iloc[position] + dataset_1st["Aboard Crew"].iloc[position])
        diff_ab= dataset_1st["Aboard"].iloc[position]-total_ab
        if i == total_ab:
            new_aboard.append(i)
            new_aboard_crew.append(dataset_1st["Aboard Crew"].iloc[position])
            new_aboard_passangers.append(dataset_1st["Aboard Passangers"].iloc[position])
        elif i > total_ab:
            new_aboard.append(i)
            a=(dataset_1st["Aboard Crew"].iloc[position]+diff_ab)
            new_aboard_crew.append(a)
            new_aboard_passangers.append(dataset_1st["Aboard Passangers"].iloc[position])
        elif i < total_ab:
            i=total_ab
            new_aboard.append(i)
            new_aboard_crew.append(dataset_1st["Aboard Crew"].iloc[position])
            new_aboard_passangers.append(dataset_1st["Aboard Passangers"].iloc[position])
    except:
        print("mannaggia")
#%%
dataset_1st = dataset_1st.assign(new_aboard=new_aboard, new_aboard_crew=new_aboard_crew, new_aboard_passangers=new_aboard_passangers)
dataset_1st
#%% md
### Location Variable -> estraiamo dal testo solo gli stati
#### regex per prendere solo quello dopo l'ultima virgola
#%%
new_location = []
for w in dataset_1st.Location:
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
#### Puliamo i valori
#%%
tmp_state_cleaned = []
for i in tmp_state:
    tmp_state_cleaned.append(re.sub(rf"[^\w\s]", "", i))

print(tmp_state_cleaned)
#%% md
#### Infine andiamo a creare una nuovo variabile a ad inserirla all'interno del dataset
#%%
dataset_1st = dataset_1st.assign(state_location=tmp_state_cleaned)
print(dataset_1st.state_location)
#%%
list_of_states = dataset_1st.state_location.unique()
print(list_of_states)
#%% md
#### Notiamo la presenza di un nan value e campi vuoti non visti in precedenza
#%%
count_nan = 0
count_vuoti = 0
for i in dataset_1st.state_location:
    if i == 'nan':
        count_nan += 1
    elif i == '':
        count_vuoti += 1

print('counter nan: ', count_nan)
print('counter spazi vuoti: ', count_vuoti)
#%% md
#### Li andiamo ad eliminare
#%%
dataset_1st = dataset_1st[dataset_1st.state_location != 'nan']
dataset_1st = dataset_1st[dataset_1st.state_location != '']
print(dataset_1st)
#%% md
#### Check finale
#%%
count = 0
for i in dataset_1st.state_location:
    if i == 'nan' or i == '':
        count += 1
print(count)
#%% md
#### Accorpiamo alcuni stati e correggiamo quelli scritti in modo scorretto
#%% md
##### Stati Uniti
#%%
list_of_states_cleaned = dataset_1st.state_location.unique()
print(list_of_states_cleaned)
#%%
USA_states = ['Virginia', 'Jersey', 'Ohio', 'Pennsylvania', 'Illinois', 'Maryland', 'Kent', 'Indiana', 'Iowa',
              'Columbia', 'Wyoming', 'Minnisota', 'Wisconsin', 'Nevada', 'NY', 'WY', 'States', 'York', 'Utah', 'Oregon',
              'Idaho', 'Connecticut', 'Minnesota', 'Kansas', 'Texas', 'Washington', 'Tennessee', 'Greece', 'California',
              'Mexico', 'Missouri', 'Massachusetts', 'Utah', 'Ilinois', 'Florida', 'Michigan', 'Arkansas', 'Colorado',
              'Georgia', 'Montana', 'Mississippi', 'Alaska', 'Cailifornia', 'Indies', 'Andes', 'Guam', 'Tonkin',
              'Carolina', 'Kentucky', 'Maine', 'Alabama', 'Delaware', 'Dekota', 'Hampshire', 'Washingon', 'DC',
              'Tennesee', 'Deleware', 'Louisiana', 'Massachutes', 'Alakska', 'Coloado', 'Vermont', 'Dakota',
              'Calilfornia', 'Alaksa', 'Mississipi', 'Arizona', 'Wisconson', 'Nebraska', 'Oklahoma', 'Airzona', 'HI',
              'Hawaii']
states = []
for state in dataset_1st.state_location:
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
#### Infine andiamo ad inserire la variabile nel dataset
#%%
dataset_1st = dataset_1st.assign(States=states3)
#%% md
#### Eliminiamo altre due osservazioni che non siamo riusciti a classificare
#%%
dataset_1st = dataset_1st[dataset_1st.States != 'AK']
dataset_1st = dataset_1st[dataset_1st.States != 'Nag']
dataset_1st.States
#%% md
### Seb_Regioni
#%% md
#### Importiamo un dataset di supporto tramite il quale andremo a fare un match tra i paesi e i territori
#%%
continents_dataset = pd.read_csv("datasets/continents2.csv")
#%%
continents_dataset
#%%
macro_aree = continents_dataset['sub-region'].unique()
print(macro_aree)
#%% md
#### Creiamo la lista dei paesi per ciascuna seb_regione
#%%
Southern_Asia = continents_dataset['name']._where(continents_dataset['sub-region'] == 'Southern Asia').unique()

Northern_Europe = continents_dataset['name']._where(continents_dataset['sub-region'] == 'Northern Europe').unique()

Southern_Europe = continents_dataset['name']._where(continents_dataset['sub-region'] == 'Southern Europe').unique()

Northern_Africa = continents_dataset['name']._where(continents_dataset['sub-region'] == 'Northern Africa').unique()

Polynesia = continents_dataset['name']._where(continents_dataset['sub-region'] == 'Polynesia').unique()

Sub_Saharan_Africa = continents_dataset['name']._where(
    continents_dataset['sub-region'] == 'Sub-Saharan Africa').unique()

Latin_America = continents_dataset['name']._where(
    continents_dataset['sub-region'] == 'Latin America and the Caribbean').unique()

Western_Asia = continents_dataset['name']._where(continents_dataset['sub-region'] == 'Western Asia').unique()

Australia_and_Zealand = continents_dataset['name']._where(
    continents_dataset['sub-region'] == 'Australia and New Zealand').unique()

Western_Europe = continents_dataset['name']._where(continents_dataset['sub-region'] == 'Western Europe').unique()

Eastern_Europe = continents_dataset['name']._where(continents_dataset['sub-region'] == 'Eastern Europe').unique()

Northern_America = continents_dataset['name']._where(continents_dataset['sub-region'] == 'Northern America').unique()

South_Eastern_Asia = continents_dataset['name']._where(
    continents_dataset['sub-region'] == 'South-eastern Asia').unique()

Eastern_Asia = continents_dataset['name']._where(continents_dataset['sub-region'] == 'Eastern Asia').unique()

Melanesia = continents_dataset['name']._where(continents_dataset['sub-region'] == 'Melanesia').unique()

Micronesia = continents_dataset['name']._where(continents_dataset['sub-region'] == 'Micronesia').unique()

Central_Asia = continents_dataset['name']._where(continents_dataset['sub-region'] == 'Central Asia').unique()


#print(Southern_Europe)
#%% md
#### Facciamo un match per ogni sub_regione tra gli stati del dataset e quelli del dataset di supporto
#%%
sub_regions = []
for nation in dataset_1st.States:
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
#### Classifichiamo manualmente alcuni paesi che sono rimasti fuori dal match
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
#### Creiamo la nuova colonna con le sub_regioni
#%%
dataset_1st = dataset_1st.assign(Sub_Regions=sub_regions2)
#%%
dataset_1st.Sub_Regions
#%% md
#### Infine controlliamo le ultime osservazioni che non sono utili ai fini dell'analisi
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
        count_Africa += 1
    elif i == 'Base':
        count_Base += 1
    elif i == 'Channel':
        count_channel += 1
    elif i == 'Newfoundland':
        count_newfoundland += 1
    elif i == 'Ocean':
        count_Ocean += 1
    elif i == 'Sea':
        count_Sea += 1
    elif i == 'Sound':
        count_sound += 1
    elif i == 'Station':
        count_station += 1
    elif i == 'Territory':
        count_Territory += 1
    elif i == 'Island':
        count_island += 1
    elif i == 'Islands':
        count_islands += 1
    elif i == 'Airport':
        count_airport += 1
    elif i == 'Coast':
        count_coast += 1
    elif i == 'Gulf':
        count_gulf += 1
    elif i == 'Republic':
        count_republic += 1
    elif i == 'USSR':
        count_USSR += 1

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
#### E alcune decidiamo di eliminarle (tutte tranne 'Africa')
#%%
dataset_1st = dataset_1st[dataset_1st.Sub_Regions != 'Territory']
dataset_1st = dataset_1st[dataset_1st.Sub_Regions != 'Station']
dataset_1st = dataset_1st[dataset_1st.Sub_Regions != 'Sound']
dataset_1st = dataset_1st[dataset_1st.Sub_Regions != 'Base']
dataset_1st = dataset_1st[dataset_1st.Sub_Regions != 'Channel']
dataset_1st = dataset_1st[dataset_1st.Sub_Regions != 'Newfoundland']
dataset_1st = dataset_1st[dataset_1st.Sub_Regions != 'Ocean']
dataset_1st = dataset_1st[dataset_1st.Sub_Regions != 'Island']
dataset_1st = dataset_1st[dataset_1st.Sub_Regions != 'Islands']
dataset_1st = dataset_1st[dataset_1st.Sub_Regions != 'Airport']
dataset_1st = dataset_1st[dataset_1st.Sub_Regions != 'Coast']
dataset_1st = dataset_1st[dataset_1st.Sub_Regions != 'Gulf']
dataset_1st = dataset_1st[dataset_1st.Sub_Regions != 'Republic']
dataset_1st = dataset_1st[dataset_1st.Sub_Regions != 'Sea']
#%%
dataset_1st.Sub_Regions
#%% md
#### Adesso andiamo a creare un'altra variabile che racchiude le sub_regioni nei continenti
#%%
dataset_1st.Sub_Regions.unique()
#%%
continents_dataset.region.unique()
#%% md
#### Creiamo una variabile per ogni continente utilizzando il dataset di supporto
#%%
Asia = continents_dataset['sub-region']._where(continents_dataset['region'] == 'Asia').unique()

Europe = continents_dataset['sub-region']._where(continents_dataset['region'] == 'Europe').unique()

Africa = continents_dataset['sub-region']._where(continents_dataset['region'] == 'Africa').unique()

America = continents_dataset['sub-region']._where(continents_dataset['region'] == 'Americas').unique()

Oceania = continents_dataset['sub-region']._where(continents_dataset['region'] == 'Oceania').unique()

print(Africa)
#%% md
#### Andiamo a fare il matching tra le Sub_Regioni precedentemente definite
#%%
Continents = []
for sub_region in dataset_1st.Sub_Regions:
    if sub_region in Asia:
        Continents.append('Asia')
    elif sub_region in Europe:
        Continents.append('Europe')
    elif sub_region in Africa:
        Continents.append('Africa')
    elif sub_region in America:
        Continents.append('America')
    elif sub_region in Oceania:
        Continents.append('Oceania')
    else: Continents.append(sub_region)

print(sorted(set(Continents)))
#%%
a=0
b=0
for i in Continents:
    if i == "Antarctica":
        a+=1
    elif i == "Atlantic":
        b+=1

print(a,b)
#        Continents.append(i)
print(len(Continents))
#%%
print(set(Continents))
#%% md
#### Creiamo la nuova variabile e la andiamo ad aggiungere al dataset
#%%
dataset_1st = dataset_1st.assign(Continent=Continents)
#%%
dataset_1st = dataset_1st._where(dataset_1st.Continent != "Atlantic")
dataset_1st = dataset_1st._where(dataset_1st.Continent != "Antarctica")

#%%
dataset_1st.Continent.unique()
#%% md
## Estrazione città da Aeroporto di partenza

#%%
dataset_1st
#%%
dataset_1st.Aeroporto_di_partenza.unique()
#%%
aerop_matched = []
aerop_not_matched = []
for aerop in dataset_1st.Aeroporto_di_partenza:
    if aerop in world_cities_dataset.name.unique():
        aerop_matched.append(aerop)
    elif aerop == 'Demonstration':
        aerop_matched.append(aerop)
    elif aerop == 'Test flight':
        aerop_matched.append(aerop)
    elif aerop == 'Sconosciuto':
        aerop_matched.append(aerop)
    elif aerop == 'Informazione riservata':
        aerop_matched.append(aerop)
    elif aerop == 'Military exercise':
        aerop_matched.append(aerop)
    elif aerop == 'Exercises':
        aerop_matched.append(aerop)
    elif aerop == 'Test':
        aerop_matched.append(aerop)
    elif aerop == 'Test Flight':
        aerop_matched.append(aerop)
    elif aerop in cities_dataset.name.unique():
        aerop_matched.append(aerop)
    elif aerop in dataset_1st.States.unique():
        aerop_matched.append(aerop)
    else: aerop_not_matched.append(aerop)

print(f'città matchate: {len(aerop_matched)}')
print(f'città NON matchate: {len(aerop_not_matched)}')
#%%
print(len(set(aerop_matched)))
#%%
for i in dataset_1st.Aeroporto_di_partenza:
    if i in aerop_not_matched:
        dataset_1st = dataset_1st[dataset_1st.Aeroporto_di_partenza != i]
#%% md
#### Aggiunta colonna relativa agli stati degli aeroporti di partenza

#%%
a = {}
for i in dataset_1st["Aeroporto_di_partenza"]:
    if i in cities_dataset["name"].values:
        b = str(cities_dataset["country_name"][cities_dataset["name"] == i]).split()[1]
        if i == "Paris":
            a["Paris"] = "France"
        elif i == "Washington":
            a[i] = "United States"
        elif b == "United":
            a[i] = b + " " + str(cities_dataset["country_name"][cities_dataset["name"] == i]).split()[2]
        elif i == "London":
            a[i] = "United Kingdom"
        else:
            a[i] = b
    else:
        a[i] = i
state_aerop_partenza = [a[state] for state in dataset_1st["Aeroporto_di_partenza"]]

dataset_1st = dataset_1st.assign(State_Aeroporto_di_partenza=state_aerop_partenza)
dataset_1st
#%%
continents_dataset
#%%
continent = {}
for i in dataset_1st["State_Aeroporto_di_partenza"]:
    if i in dataset_1st["States"].values:
        continent[i] = str(dataset_1st["Continent"][dataset_1st["States"] == i]).split()[1]
    else:
        continent[i] = i

continente_aerop_partenza = [continent[continente] for continente in dataset_1st["State_Aeroporto_di_partenza"]]

dataset_1st = dataset_1st.assign(Continent_Aeroporto_di_partenza=continente_aerop_partenza)

correct_continent = []
for i in dataset_1st["Continent_Aeroporto_di_partenza"]:
    if i == "Mexico":
        correct_continent.append("America")
    elif i == "Czech":
        correct_continent.append("Europe")
    elif i == "Papua":
        correct_continent.append("Asia")
    elif i == "South":
        correct_continent.append("Asia")
    elif i == "Israel":
        correct_continent.append("Asia")
    elif i == "Serbia":
        correct_continent.append("Europe")
    elif i == "Mauritius":
        correct_continent.append("Africa")
    elif i == "Moldova":
        correct_continent.append("Europe")
    elif i == "Georgia":
        correct_continent.append("Europe")
    elif i == "Sri":
        correct_continent.append("Asia")
    elif i == "Costa":
        correct_continent.append("America")
    elif i == "New":
        correct_continent.append("Asia")
    elif i == "Saint":
        correct_continent.append("America")
    elif i == "Bonaire":
        correct_continent.append("America")
    elif i == "Belarus":
        correct_continent.append("Europe")
    elif i == "Cote":
        correct_continent.append("Africa")
    elif i == "Saudi":
        correct_continent.append("Asia")
    elif i == "Democratic":
        correct_continent.append("Africa")
    elif i == "Lithuania":
        correct_continent.append("Europe")
    elif i == "Montenegro":
        correct_continent.append("Africa")
    elif i == "Haiti":
        correct_continent.append("America")
    elif i == "United Arab":
        correct_continent.append("Asia")
    elif i == "Slovenia":
        correct_continent.append("Europe")
    elif i == "Belize":
        correct_continent.append("America")
    elif i == "Brunei":
        correct_continent.append("Africa")
    elif i == "Micronesia":
        correct_continent.append("Oceania")
    elif i == "Central":
        correct_continent.append("Africa")
    elif i == "Burkina":
        correct_continent.append("Africa")
    elif i == "Burundi":
        correct_continent.append("Africa")
    elif i == "Exercises":
        correct_continent.append("Sconosciuto")
    elif i == "Test":
        correct_continent.append("Sconosciuto")
    elif i == "Military exercise":
        correct_continent.append("Sconosciuto")
    elif i == "Test Flight":
        correct_continent.append("Sconosciuto")
    elif i == "Demonstration":
        correct_continent.append("Sconosciuto")
    elif i == "Informazione riservata":
        correct_continent.append("Sconosciuto")
    elif i == "Mexico City":
        correct_continent.append("America")
    elif i == "Antananarivo":
        correct_continent.append("Africa")
    elif i == "Hong Kong":
        correct_continent.append("Asia")
    elif i == "Milano":
        correct_continent.append("Europe")
    elif i == "Mar del Plata":
        correct_continent.append("America")
    elif i == "NaN":
        correct_continent.append("Sconosciuto")
    elif i == "Juba":
        correct_continent.append("Africa")
    elif i == "Miandrivazo":
        correct_continent.append("Africa")
    elif i == "Papeete":
        correct_continent.append("Oceania")
    elif i == "Niamey":
        correct_continent.append("Africa")
    elif i == "Coihaique":
        correct_continent.append("America")
    elif i == "Savannakhét":
            correct_continent.append("Asia")
    elif i == "Kiev":
        correct_continent.append("Europe")
    elif i == "Francistown":
        correct_continent.append("Africa")
    elif i == "Iwakuni":
            correct_continent.append("Asia")
    elif i == "Malakal":
        correct_continent.append("Africa")
    elif i == "N'Djamena":
        correct_continent.append("Africa")
    elif i == "Ulan Bator":
            correct_continent.append("Asia")
    elif i == "Nouakchott":
        correct_continent.append("Africa")
    elif i == "Maintirano":
        correct_continent.append("Africa")
    elif i == "Pago Pago":
        correct_continent.append("Oceania")
    elif i == "Dushanbe":
        correct_continent.append("Africa")
    elif i == "Pristina":
        correct_continent.append("Europe")
    elif i == "Dakhla":
        correct_continent.append("Africa")
    elif i == "Astana":
        correct_continent.append("Asia")
    elif i == "Bonaire,":
        correct_continent.append("America")
    elif type(i) == float:
        correct_continent.append("Sconosciuto")
    elif i == "Bogotá":
        correct_continent.append("America")
    elif i == "Test flight":
            correct_continent.append("America")
    else:
        correct_continent.append(i)

dataset_1st = dataset_1st.assign(Continent_Aeroporto_di_partenza=correct_continent)
dataset_1st["Continent_Aeroporto_di_partenza"].unique()
#%%
sub_r = {}
for i in dataset_1st["State_Aeroporto_di_partenza"]:
    if i in continents_dataset["name"].values:
        sub_r[i] = str(continents_dataset["sub-region"][continents_dataset["name"] == i]).split()[1]
    else:
        sub_r[i] = i

sub_regione_aerop_partenza = [sub_r[s_r] for s_r in dataset_1st["State_Aeroporto_di_partenza"]]

dataset_1st = dataset_1st.assign(SubRegion_Aeroporto_di_partenza=sub_regione_aerop_partenza)
#%% md
##### Ora eliminiamo le vecchie variabili e riosserviamo il dataset prima di procedere

#%%
dataset_1st.columns
#%%
col_trash_2 = ["Aboard", "Aboard Passangers", 'Aboard Crew', 'Fatalities',
               'Fatalities Passangers', 'Fatalities Crew', 'Ground', "AC Type",
               "Date", "Location", "Operator","Route","state_location"]
dataset_def=dataset_1st
for i in dataset_def.columns:
    if i in col_trash_2:
        dataset_def = dataset_def.drop(i, axis=1)
dataset_def


#%% md
### Nuove rappresentazioni grafiche
#%%
dataset_def.keys()
#%%
dataset_def.Continent.unique()
#%%
from matplotlib.pyplot import figure
cs = sb.color_palette("tab20")
#cs =["darkgre
# y","darkred","green","purple","aqua","blue","yellow","sienna","orangered","deeppink","springgreen","violet", "pink","dodgerblue"]
dz=dict(dataset_def["Continent"].drop(0).value_counts())
sb.set_style("whitegrid")
pie, ax = plt.subplots(figsize=[14,16])
Labels = [k for k in dz.keys()]

Data   = [float(v) for v in dz.values()]
figure(dpi=200);
plt.pie(x = Data, labels=Labels, autopct="%.1f%%", pctdistance=0.8, colors=cs);
plt.title("Frequency of Continent", fontsize=30);
#%%
sb.scatterplot(x=dataset_1st["new_aboard"],y=dataset_1st["new_fatalities"], hue="Continent", data=dataset_1st)
#%%
sb.scatterplot(sizes=200,x=dataset_1st["new_aboard"], y=dataset_1st["new_ground"], hue="Continent", style="decadi",data=dataset_1st)
#%%
sb.scatterplot(sizes=200,x=dataset_1st["new_aboard"], y=dataset_1st["new_fatalities_passangers"], hue="Continent", style="decadi",data=dataset_1st)
#%% md
# Grafi (Gabro)
#%%
import networkx as nx
#%%
nodes = nx.Graph()
#%%
nodes.add_nodes_from(dataset_def["Aeroporto_di_partenza"])
#%%
nx.draw(nodes)
#%%
test = nx.Graph()
test.add_edge("a", "b", weight=3)
test.add_edge("b", "c", weight=10)
test.add_edge("c", "a", weight=3)

pos = nx.spring_layout(test, seed=7)  # positions for all nodes - seed for reproducibility

# nodes
nx.draw_networkx_nodes(test, pos, node_size=700)

# edges
nx.draw_networkx_edges(test, pos, width=6)
nx.draw_networkx_edges(
    test, pos, width=6, alpha=0.5, edge_color="b"
)

# node labels
nx.draw_networkx_labels(test, pos, font_size=30)
#%%
dataset_def
#%% md
Ok bisogna creare un dizionario con tutti i nomi degli aeroporti come chiavi e come valori gli aeroporti con i quali sono collegati.
#%% md
Sistemare il codice facendo una funzione
#%%
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

for aer in dataset_def["ultimo_aeroporto"].unique():
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
                elif aeroporto_2[position] == "Nan" and ultimo_aeroporto[position] != "Nan":
                    mini_edge = sorted([aeroport, ultimo_aeroporto[position]])
                    if mini_edge not in edges:
                        edges.append(mini_edge)

    elif aeroport in aeroporto_2:
        for position, i in enumerate(aeroporto_2):
            if i == aeroport:
                mini_edge = sorted([aeroport, aeroporto_3[position]])
                if aeroporto_3[position] != "Nan" and mini_edge not in edges:
                    edges.append(mini_edge)
                elif aeroporto_3[position] == "Nan" and ultimo_aeroporto[position] != "Nan":
                    mini_edge = sorted([aeroport, ultimo_aeroporto[position]])
                    if mini_edge not in edges:
                        edges.append(mini_edge)

    elif aeroport in aeroporto_3:
        for position, i in enumerate(aeroporto_3):
            if i == aeroport:
                mini_edge = sorted([aeroport, aeroporto_4[position]])
                if aeroporto_4[position] != "Nan" and mini_edge not in edges:
                    edges.append(mini_edge)
                elif aeroporto_4[position] == "Nan" and ultimo_aeroporto[position] != "Nan":
                    mini_edge = sorted([aeroport, ultimo_aeroporto[position]])
                    if mini_edge not in edges:
                        edges.append(mini_edge)

    elif aeroport in aeroporto_4:
        for position, i in enumerate(aeroporto_4):
            if i == aeroport:
                mini_edge = sorted([aeroport, aeroporto_5[position]])
                if aeroporto_5[position] != "Nan" and mini_edge not in edges:
                    edges.append(mini_edge)
                elif aeroporto_5[position] == "Nan" and ultimo_aeroporto[position] != "Nan":
                    mini_edge = sorted([aeroport, ultimo_aeroporto[position]])
                    if mini_edge not in edges:
                        edges.append(mini_edge)

    elif aeroport in aeroporto_5:
        for position, i in enumerate(aeroporto_5):
            if i == aeroport:
                mini_edge = sorted([aeroport, aeroporto_6[position]])
                if aeroporto_6[position] != "Nan" and mini_edge not in edges:
                    edges.append(mini_edge)
                elif aeroporto_6[position] == "Nan" and ultimo_aeroporto[position] != "Nan":
                    mini_edge = sorted([aeroport, ultimo_aeroporto[position]])
                    if mini_edge not in edges:
                        edges.append(mini_edge)

    elif aeroport in aeroporto_6:
        for position, i in enumerate(aeroporto_6):
            if i == aeroport:
                mini_edge = sorted([aeroport, ultimo_aeroporto[position]])
                if ultimo_aeroporto[position] != "Nan" and mini_edge not in edges:
                    edges.append(mini_edge)
                elif ultimo_aeroporto[position] == "Nan" and ultimo_aeroporto[position] != "Nan":
                    mini_edge = sorted([aeroport, ultimo_aeroporto[position]])
                    if mini_edge not in edges:
                        edges.append(mini_edge)

    elif aeroport in ultimo_aeroporto:
        for position, i in enumerate(ultimo_aeroporto):
            if i == aeroport:
                mini_edge = sorted([aeroport, ultimo_aeroporto[position]])
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
#%% md
### Estrazione macro aree per gli aeroporti
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

# bubu = []
# for i in edges:
#     if "Paris" in i: bubu.append(i)
gg.add_edges_from(edges[:250])

figure(figsize=(25, 25), dpi=300)
nx.draw(gg, with_labels=True, font_weight='bold', pos=nx.spring_layout(gg))
plt.show()
#%%
""" Codice per fare grafi """

from collections import defaultdict

# SCEGLIERE LE COLONNE DA INCROCIARE E INSERIRLE AL POSTO DI "Continent", "AC_Type_simplified", edge_attr="Continent"
new_graph = nx.from_pandas_edgelist(dataset_def, "Continent", "AC_Type_simplified", edge_attr="Continent",
                                    create_using=nx.MultiGraph)

# DEGREE DEI NODI ORIGINARIO
deg = [name[0] for name in new_graph.degree]

# MODIFICA DEGREE
new_node_degree = defaultdict(int)

for position, n in enumerate(dataset_def["Continent"]):
    new_node_degree[n] += 0.05 * dataset_def["new_fat"].iloc[position]

# SE NON VOGLIAMO METTERE IL PESO A TUTTI I NODI
for i in deg:
    if not i in new_node_degree:
        new_node_degree[i] = 0
#
new_node_degree = [int(v) for v in new_node_degree.values()]

# LAYOUT
pos_norm = nx.kamada_kawai_layout(new_graph)

# CREAZIONE GRAFO
figure(figsize=(20, 15), dpi=80)
nx.draw(new_graph, with_labels=False, node_size=new_node_degree, edge_color="yellow",
        node_color="orange", pos=pos_norm)

# SELEZIONE LABELS DA MOSTRARE
labels = {}
for node in new_graph.nodes():
    if node in dataset_def["Continent"].unique():  # indicare la colonna da utilizzare per i labels
        labels[node] = node

nx.draw_networkx_labels(new_graph, pos_norm, labels, font_size=10)
plt.show()
#%%
new_graph = nx.from_pandas_edgelist(dataset_def, "State_Aeroporto_di_partenza", "New_Operator_column",
                                    edge_attr="State_Aeroporto_di_partenza",
                                    create_using=nx.MultiGraph)

figure(figsize=(15, 10), dpi=80)

# DEGREE DEI NODI ORIGINARIO
deg = [name[0] for name in new_graph.degree]

# MODIFICA DEGREE
new_node_degree = defaultdict(int)

for position, n in enumerate(dataset_def["State_Aeroporto_di_partenza"]):
    new_node_degree[n] += 0.05 * dataset_def["new_fat"].iloc[position]

# SE NON VOGLIAMO METTERE IL PESO A TUTTI I NODI
for i in deg:
    if not i in new_node_degree:
        new_node_degree[i] = 0
#
new_node_degree = [int(v) for v in new_node_degree.values()]

# LAYOUT
pos_norm = nx.kamada_kawai_layout(new_graph)

# CREAZIONE GRAFO
figure(figsize=(20, 15), dpi=80)
nx.draw(new_graph, with_labels=True, node_size=new_node_degree, edge_color="yellow",
        node_color="orange", pos=pos_norm)
#%%
only_poland = dataset_def[dataset_def["State_Aeroporto_di_partenza"] == "Germany"]

new_graph = nx.from_pandas_edgelist(only_poland, "State_Aeroporto_di_partenza", "States",
                                    edge_attr="New_Operator_column",
                                    create_using=nx.MultiGraph)

figure(figsize=(15, 10), dpi=80)

# DEGREE DEI NODI ORIGINARIO
deg = [name[0] for name in new_graph.degree]

# MODIFICA DEGREE
new_node_degree = defaultdict(int)

for position, n in enumerate(dataset_def["State_Aeroporto_di_partenza"]):
    new_node_degree[n] += 0.05 * dataset_def["new_fat"].iloc[position]

# SE NON VOGLIAMO METTERE IL PESO A TUTTI I NODI
for i in deg:
    if not i in new_node_degree:
        new_node_degree[i] = 0
#
new_node_degree = [int(v) for v in new_node_degree.values()]

# LAYOUT
pos_norm = nx.kamada_kawai_layout(new_graph)

# CREAZIONE GRAFO
figure(figsize=(20, 15), dpi=80)
nx.draw(new_graph, with_labels=True, edge_color="yellow",
        node_color="orange", pos=pos_norm)
#%%
only_military = dataset_def[dataset_def["New_Operator_column"] == "Military flight"]

new_graph = nx.from_pandas_edgelist(only_military, "Continent_Aeroporto_di_partenza", "States",
                                    edge_attr="New_Operator_column",
                                    create_using=nx.MultiGraph)

figure(figsize=(15, 10), dpi=80)

# DEGREE DEI NODI ORIGINARIO
deg = [name[0] for name in new_graph.degree]

# MODIFICA DEGREE
new_node_degree = defaultdict(int)

for position, n in enumerate(only_military["Continent_Aeroporto_di_partenza"]):
    new_node_degree[n] += 0.05 * only_military["new_fat"].iloc[position]

# SE NON VOGLIAMO METTERE IL PESO A TUTTI I NODI
for i in deg:
    if not i in new_node_degree:
        new_node_degree[i] = 0
#
new_node_degree = [int(v) for v in new_node_degree.values()]

# LAYOUT
pos_norm = nx.kamada_kawai_layout(new_graph)

# CREAZIONE GRAFO
figure(figsize=(20, 15), dpi=80)
nx.draw(new_graph, with_labels=False, edge_color="yellow", node_size=new_node_degree,
        node_color="orange", pos=pos_norm)

# SELEZIONE LABELS DA MOSTRARE
labels = {}
for node in new_graph.nodes():
    if node in only_military[
        "Continent_Aeroporto_di_partenza"].unique():  # indicare la colonna da utilizzare per i labels
        labels[node] = node

nx.draw_networkx_labels(new_graph, pos_norm, labels, font_size=10)
plt.show()
#%% md
c'è qualcosa che non va...
#%%
anni_00_40 = dataset_def[dataset_def["Year"] <= 1940]

new_graph = nx.from_pandas_edgelist(anni_00_40, "New_Operator_column", "State_Aeroporto_di_partenza",
                                    edge_attr="New_Operator_column",
                                    create_using=nx.MultiGraph)

figure(figsize=(15, 10), dpi=80)

# DEGREE DEI NODI ORIGINARIO
deg = [name[0] for name in new_graph.degree]

# MODIFICA DEGREE
new_node_degree = defaultdict(int)

for position, n in enumerate(anni_00_40["New_Operator_column"]):
    new_node_degree[n] += anni_00_40["new_fat"].iloc[position]

# SE NON VOGLIAMO METTERE IL PESO A TUTTI I NODI
for i in deg:
    if not i in new_node_degree:
        new_node_degree[i] = 0
#
new_node_degree = [int(v) for v in new_node_degree.values()]

# LAYOUT
pos_norm = nx.kamada_kawai_layout(new_graph)

# CREAZIONE GRAFO
figure(figsize=(20, 15), dpi=80)
nx.draw(new_graph, with_labels=True, edge_color="yellow", node_size=new_node_degree,
        node_color="orange", pos=pos_norm)

# SELEZIONE LABELS DA MOSTRARE
# labels = {}
# for node in new_graph.nodes():
#     if node in anni_00_40["New_Operator_column"].unique():  # indicare la colonna da utilizzare per i labels
#         labels[node] = node
#
# nx.draw_networkx_labels(new_graph, pos_norm, labels, font_size=10)
# plt.show()
#%%
anni_00_40 = dataset_def[dataset_def["Year"] <= 1940]
anni_00_40 = anni_00_40[anni_00_40["State_Aeroporto_di_partenza"] == "Papua"]
anni_00_40


# new_graph = nx.from_pandas_edgelist(anni_00_40, "Operator", "State_Aeroporto_di_partenza",
#                                     edge_attr="Operator",
#                                     create_using=nx.MultiGraph)
#
# figure(figsize=(15, 10), dpi=80)
#
# # DEGREE DEI NODI ORIGINARIO
# deg = [name[0] for name in new_graph.degree]
#
# # MODIFICA DEGREE
# new_node_degree = defaultdict(int)
#
# for position, n in enumerate(anni_00_40["Operator"]):
#     new_node_degree[n] += anni_00_40["new_fat"].iloc[position]
#
# # SE NON VOGLIAMO METTERE IL PESO A TUTTI I NODI
# for i in deg:
#     if not i in new_node_degree:
#         new_node_degree[i] = 0
# #
# new_node_degree = [int(v) for v in new_node_degree.values()]
#
# # LAYOUT
# pos_norm = nx.kamada_kawai_layout(new_graph)
#
# # CREAZIONE GRAFO
# figure(figsize=(20, 15), dpi=80)
# nx.draw(new_graph, with_labels=True, edge_color="yellow", node_size=new_node_degree,
#         node_color="orange", pos=pos_norm)
#
# SELEZIONE LABELS DA MOSTRARE
# labels = {}
# for node in new_graph.nodes():
#     if node in anni_00_40["New_Operator_column"].unique():  # indicare la colonna da utilizzare per i labels
#         labels[node] = node
#
# nx.draw_networkx_labels(new_graph, pos_norm, labels, font_size=10)
# plt.show()
#%%
anni_40_80 = dataset_def[dataset_def["Year"] >= 1940]
anni_40_80 = anni_40_80[anni_40_80["Year"] <= 1980]

new_graph = nx.from_pandas_edgelist(anni_40_80, "New_Operator_column", "State_Aeroporto_di_partenza",
                                    edge_attr="New_Operator_column",
                                    create_using=nx.MultiGraph)

figure(figsize=(15, 10), dpi=80)

# DEGREE DEI NODI ORIGINARIO
deg = [name[0] for name in new_graph.degree]

# MODIFICA DEGREE
new_node_degree = defaultdict(int)

for position, n in enumerate(anni_40_80["New_Operator_column"]):
    new_node_degree[n] += anni_40_80["new_fat"].iloc[position]

# SE NON VOGLIAMO METTERE IL PESO A TUTTI I NODI
for i in deg:
    if not i in new_node_degree:
        new_node_degree[i] = 0
#
new_node_degree = [int(v) for v in new_node_degree.values()]

# LAYOUT
pos_norm = nx.kamada_kawai_layout(new_graph)

# CREAZIONE GRAFO
figure(figsize=(20, 15), dpi=80)
nx.draw(new_graph, with_labels=True, edge_color="yellow", node_size=new_node_degree,
        node_color="orange", pos=pos_norm)

# SELEZIONE LABELS DA MOSTRARE
# labels = {}
# for node in new_graph.nodes():
#     if node in anni_00_40["New_Operator_column"].unique():  # indicare la colonna da utilizzare per i labels
#         labels[node] = node
#
# nx.draw_networkx_labels(new_graph, pos_norm, labels, font_size=10)
# plt.show()
#%%
new_graph = nx.from_pandas_edgelist(dataset_def, "Continent_Aeroporto_di_partenza", "Continent_Aeroporto_di_partenza",
                                    edge_attr="Continent_Aeroporto_di_partenza",
                                    create_using=nx.MultiGraph)

figure(figsize=(15, 10), dpi=80)

# DEGREE DEI NODI ORIGINARIO
deg = [name[0] for name in new_graph.degree]

# MODIFICA DEGREE
new_node_degree = defaultdict(int)

for position, n in enumerate(dataset_def["Continent_Aeroporto_di_partenza"]):
    new_node_degree[n] += 0.05 * dataset_def["new_fat"].iloc[position]

# SE NON VOGLIAMO METTERE IL PESO A TUTTI I NODI
for i in deg:
    if not i in new_node_degree:
        new_node_degree[i] = 0
#
new_node_degree = [int(v) for v in new_node_degree.values()]

# LAYOUT
pos_norm = nx.kamada_kawai_layout(new_graph)

# CREAZIONE GRAFO
figure(figsize=(20, 15), dpi=80)
nx.draw(new_graph, with_labels=True, node_size=new_node_degree, edge_color="yellow",
        node_color="orange", pos=pos_norm)