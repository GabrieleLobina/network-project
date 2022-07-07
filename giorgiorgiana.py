#%%
import pandas as pd
import re
import matplotlib as mlt
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.axes as axes
import  math

#!{sys.executable} -m pip install seaborn
import seaborn as sb
#%%
dataset = pd.read_csv("datasets/Airplane_Crashes_and_Fatalities_Since_1908_20190820105639.csv")
dataset
#%% md
---
---
# Gabro
#%% md
#### Cleaning colonna **Operator**
#%%
print("numero di Na:", len([i for i in dataset.Operator if type(i) == float])) # abbiamo solo 10 Na
print(dataset.shape)

# Eliminazione righe contenenti Na nella colonna Operator
dataset = dataset[dataset['Operator'].notna()]
print(dataset.shape)
#%% md
Identificazione e raggruppamento categoria di operatore militare
#%%
print(len(dataset['Operator'].unique()))

military_flights = []

military_words = ["army", "navy", "marine", "military", "force", "airforce", "amee de l'air"]

# Identifica tutti i nomi degli operatori che appartengono al campo militare
for operator in dataset['Operator'].unique():
    for word in military_words:
        if word.lower() in operator.lower() and operator not in military_flights: military_flights.append(operator)

# Identifica tutti i nomi degli operatori che in Route hanno Test flight e Test presumendo che si trattino anche essi di voli militari
test_flights = ["Test", "Test flight"]
for position, operator in enumerate(dataset['Operator']):
    if dataset.Route.iloc[position] in test_flights and operator not in military_flights: military_flights.append(operator)


print("numero di operatori militari univoci:", len(military_flights))  # 251 valori univoci relativi
#%% md
Identificazione e raggruppamento categoria di operatore postale
#%%
postal_cargo_flights = []

postal_e_cargo_words = ["postal", "mail", "aeropostale", "cargo", "express"]

# Identifica tutti i nomi degli operatori che appartengono al campo militare
for operator in dataset['Operator'].unique():
    if type(operator) != float:
        for word in postal_e_cargo_words:
            if word.lower() in operator.lower() and operator not in postal_cargo_flights: postal_cargo_flights.append(operator)

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
    else: new_column.append("Scheduled flight")
#%% md
## ambulance --> decidere se assegnare una macro categoria
#%%
dataset = dataset.assign(New_Operator_column=new_column)
dataset
#%%
print(len(dataset.New_Operator_column.unique()))
#%% md
#### Cleaning colonna **Route**
#%%
print("numero di NaN nella colonna Time:", len([i for i in dataset.Route if type(i) == float]))  # 774.. Non troppi, quindi da eliminare
#%%
rotte = []

for route in dataset.Route:
    if type(route) != float: rotte.append(route.split("-"))
    else: rotte.append(route)

rotte_pulite = []
for route in rotte:
    new_route = []
    if type(route) != float:
        for aeroport in route:
            if "," in aeroport: new_route.append(re.sub(f",.+", "", aeroport))
            else: new_route.append(aeroport)
    else: new_route.append(route)
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
    else: simplified_aircraft_names.append(airplane)

# Eliminazione dei pattern tipo "15.L ..." e "V.17 ..."
simplified_aircraft_names_1 = []
for position, airplane in enumerate(simplified_aircraft_names):
    if type(airplane) != float and len(airplane.split()) > 1:
        simplified_aircraft_names_1.append(re.sub(r"[A-Z0-9]+\.(.)+", "", airplane))
    else: simplified_aircraft_names_1.append(airplane)

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
#### Check degli NA nella colonna Location
#%%
print("numero di NaN nella colonna Location:", len([i for i in dataset.Location if type(i) == float])) # Non abbiamo NA
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
    tmp_state_cleaned. append(re.sub(rf"[^\w\s]", "", i))

print(tmp_state_cleaned)
#%% md
#### Infine andiamo a creare una nuovo variabile a ad inserirla all'interno del dataset
#%%
dataset = dataset.assign(state_location = tmp_state_cleaned)
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
        count+=1
print(count)
#%% md
#### Accorpo alcuni stati e correggo quelli scritti in modo scorretto
#%% md
##### Stati Uniti
#%%
print(list_of_states)
#%%
USA_states = ['Virginia', 'Jersey', 'Ohio', 'Pennsylvania',  'Illinois', 'Maryland', 'Kent', 'Indiana', 'Iowa', 'Columbia', 'Wyoming', 'Minnisota', 'Wisconsin', 'Nevada', 'NY', 'WY', 'States', 'York', 'Utah', 'Oregon', 'Idaho', 'Connecticut', 'Minnesota', 'Kansas', 'Texas', 'Washington', 'Tennessee', 'Greece', 'California', 'Mexico', 'Missouri', 'Massachusetts', 'Utah', 'Ilinois', 'Florida', 'Michigan', 'Arkansas', 'Colorado', 'Georgia', 'Montana', 'Mississippi', 'Alaska', 'Cailifornia', 'Indies', 'Andes', 'Guam', 'Tonkin', 'Carolina', 'Kentucky', 'Maine', 'Alabama', 'Delaware', 'Dekota', 'Hampshire', 'Washingon', 'DC', 'Tennesee', 'Deleware', 'Louisiana', 'Massachutes', 'Alakska', 'Coloado', 'Vermont', 'Dakota', 'Calilfornia', 'Alaksa', 'Mississipi', 'Arizona', 'Wisconson', 'Nebraska', 'Oklahoma', 'Airzona']
states = []
for state in dataset.state_location:
    if state in USA_states:
        states.append('USA')
    else: states.append(state)

print(states)
#%%
print(set(states))
#%% md
##### Correzioni varie
#%%
states2 = []
for state in states:
    states2.append(state.replace('USSR', 'Russia').
                   replace('Canada2','Canada').
                   replace('UAR','UAE').
                   replace('Emirates','UAE').
                   replace('Djibouti','Djbouti').
                   replace('Bulgeria','Bulgaria').
                   replace('bulgaria','Bulgaria').
                   replace('Aregntina','Argentina').
                   replace('Amsterdam','Belgium').
                   replace('Ontario','Canada').
                   replace('Okinawa','Japan').
                   replace('karkov','Ukraine').
                   replace('Jamacia','Jamaica').
                   replace('Argenina','Argentina').
                   replace('Airstrip','Airport').
                   replace('Algiers','Algeria').
                   replace('Russian', 'Russia').
                   replace('Swden', 'Sweden').
                   replace('coast', 'Coast'))

print(set(states2))
#%% md
##### Regno Unito
#%%
states_UK = ['UK','Wales','Scotland', 'Eire', 'Union', 'Kingdom', 'England']
states3 = []
for state in states2:
    if state in states_UK:
        states3.append('UK')
    else: states3.append(state)

print(set(states3))
#%% md
#### Infine inserisco la variabile nel dataset
#%%
dataset = dataset.assign(States = states3)
#%% md

###    Leo
#%% md
Change data format

#%%
print(dataset['Date'])
#%% md

#%%
new_date=[]
#%%
for i in dataset.Date :
    #print (re.findall('[0-9]{4}',i))
    new_date.append(*re.findall('[0-9]{4}',i))
    #a = a.append(i[i.re.findall('[0-9]{4}',i)])
print(new_date)

#%%
dataset=dataset.assign(Year=new_date)
#%%
dataset.columns
#%%
print(type(dataset.Year))
#%%
for i in dataset.Year:
    print(type(i))
#%%
dataset["Year"]=dataset["Year"].astype(int)
#%% md
La colonna Date è rimasta all'interno del dataset senza subire modifiche, è stata invece aggiunta una nuova colonna denominata Year contenente solo l'anno presente nella colonna Date, al fine di eliminare il problemma di disomogeneità dei dati a causa dei diversi formati dd/mm/yyyy e mm/dd/yyyy presenti nel dataset a causa delle differene fra sistema anglosassone ed europeo.
#%% md

#%% md
Ovviamente nel codice sono presenti dei print esclusivamente a fini di comprensione del lavoro che possono essere eliminati nella versione finale.
#%% md
###     Osservazione variabile Time

#%%
ore=[]
#%%
for i in dataset.Time :
        #if type(i) == float:
         #   print(i)
        if type(i) == str:
            ore.append(i)

print(ore,len(ore))
#%%
bbb= 0
for i in dataset.Time :
        if type(i) == float:
            bbb = bbb+1
print(bbb)
#%%
bb= 0
for i in dataset.Time :
        if type(i) == str:
            bb = bb+1
print(bb)
#%%
new_ore = []
for i in ore:
    #print(i,re.sub(rf"[:].*","",i))
    #i = (re.sub(rf"[:].*","",i))
    new_ore.append(re.sub(rf"[:].*","",i))
print(new_ore,len(new_ore))


#%%
f=0
for i in new_ore:
    i=int(i)
    f=f+1
    #print(i,type(i))
print(f)
#%%
int_ore=[]
for i in new_ore:
    int_ore.append(int(i))
print(len(int_ore),int_ore,type(int_ore[2]))
#%%
dataset=dataset.assign(Hour=new_ore)
#%%

#%% md

#%% md
###    Leo
#%% md
Change data format

#%%
print(dataset['Date'])
#%% md

#%%
new_date=[]
#%%
for i in dataset.Date :
    #print (re.findall('[0-9]{4}',i))
    new_date.append(*re.findall('[0-9]{4}',i))
    #a = a.append(i[i.re.findall('[0-9]{4}',i)])
print(new_date)

#%%
dataset=dataset.assign(Year=new_date)
#%%
dataset.columns
#%%
print(type(dataset.Year))
#%%
for i in dataset.Year:
    print(type(i))
#%%
dataset["Year"]=dataset["Year"].astype(int)
#%% md
La colonna Date è rimasta all'interno del dataset senza subire modifiche, è stata invece aggiunta una nuova colonna denominata Year contenente solo l'anno presente nella colonna Date, al fine di eliminare il problemma di disomogeneità dei dati a causa dei diversi formati dd/mm/yyyy e mm/dd/yyyy presenti nel dataset a causa delle differene fra sistema anglosassone ed europeo.
#%% md

#%% md
Ovviamente nel codice sono presenti dei print esclusivamente a fini di comprensione del lavoro che possono essere eliminati nella versione finale.
#%% md
###     Osservazione variabile Time

#%%
ore=[]
#%%
for i in dataset.Time :
        #if type(i) == float:
         #   print(i)
        if type(i) == str:
            ore.append(i)

print(ore,len(ore))
#%%
bbb= 0
for i in dataset.Time :
        if type(i) == float:
            bbb = bbb+1
print(bbb)
#%%
bb= 0
for i in dataset.Time :
        if type(i) == str:
            bb = bb+1
print(bb)
#%%
new_ore = []
for i in ore:
    #print(i,re.sub(rf"[:].*","",i))
    #i = (re.sub(rf"[:].*","",i))
    new_ore.append(re.sub(rf"[:].*","",i))
print(new_ore,len(new_ore))


#%%
f=0
for i in new_ore:
    i=int(i)
    f=f+1
    #print(i,type(i))
print(f)
#%%
int_ore=[]
for i in new_ore:
    int_ore.append(int(i))
print(len(int_ore),int_ore,type(int_ore[2]))
#%%
for i in int_ore:
    if i > 24:
        print(i)
import math
import numpy
print(numpy.mean(int_ore))
#%%

patches=plt.hist(int_ore)
np.arange()

plt.xlabel("Values")
plt.ylabel("Frequency")
plt.title("Histogram")
plt.show()
#%%
#dataset=dataset.assign(Hour=new_ore)
#%% md

#%% md
###    Leo
#%% md
Change data format

#%%
print(dataset['Date'])
#%% md

#%%
new_date=[]
#%%
for i in dataset.Date :
    #print (re.findall('[0-9]{4}',i))
    new_date.append(*re.findall('[0-9]{4}',i))
    #a = a.append(i[i.re.findall('[0-9]{4}',i)])
print(new_date)

#%%
dataset=dataset.assign(Year=new_date)
#%%
dataset.columns
#%%
print(type(dataset.Year))
#%%
for i in dataset.Year:
    print(type(i))
#%%
dataset["Year"]=dataset["Year"].astype(int)
#%% md
La colonna Date è rimasta all'interno del dataset senza subire modifiche, è stata invece aggiunta una nuova colonna denominata Year contenente solo l'anno presente nella colonna Date, al fine di eliminare il problemma di disomogeneità dei dati a causa dei diversi formati dd/mm/yyyy e mm/dd/yyyy presenti nel dataset a causa delle differene fra sistema anglosassone ed europeo.
#%% md

#%% md
Ovviamente nel codice sono presenti dei print esclusivamente a fini di comprensione del lavoro che possono essere eliminati nella versione finale.
#%% md
###     Osservazione variabile Time

#%%
ore=[]
#%%
for i in dataset.Time :
        #if type(i) == float:
         #   print(i)
        if type(i) == str:
            ore.append(i)

print(ore,len(ore))
#%%
bbb= 0
for i in dataset.Time :
        if type(i) == float:
            bbb = bbb+1
print(bbb)
#%%
bb= 0
for i in dataset.Time :
        if type(i) == str:
            bb = bb+1
print(bb)
#%%
new_ore = []
for i in ore:
    #print(i,re.sub(rf"[:].*","",i))
    #i = (re.sub(rf"[:].*","",i))
    new_ore.append(re.sub(rf"[:].*","",i))
print(new_ore,len(new_ore))


#%%
f=0
for i in new_ore:
    i=int(i)
    f=f+1
    #print(i,type(i))
print(f)
#%%
int_ore=[]
for i in new_ore:
    int_ore.append(int(i))
print(len(int_ore),int_ore,type(int_ore[2]))
#%%
for i in int_ore:
    if i > 24:
        print(i)
import math
import numpy
print(numpy.mean(int_ore))
#%%

patches=plt.hist(int_ore)
np.arange()

plt.xlabel("Values")
plt.ylabel("Frequency")
plt.title("Histogram")
plt.show()
#%%
#dataset=dataset.assign(Hour=new_ore)
#%% md

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
dataset.shape
dataset = dataset.assign(new_fat=new_fat, new_crew=new_crew, new_pass=new_pass, new_ground=new_ground)
dataset
print(dataset.shape)
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

print(dataset.shape)
dataset = dataset[dataset["Fatalities"].notna()]
dataset = dataset[dataset["Fatalities Crew"].notna()]
dataset = dataset[dataset["Fatalities Passangers"].notna()]
dataset = dataset[dataset["Ground"].notna()]
print(dataset.shape)
print(np.mean(dataset("")))
dataset = dataset["Ground"].dropna
dataset.keys()
dataset = dataset.assign(new_fat=new_fat, new_crew=new_crew)