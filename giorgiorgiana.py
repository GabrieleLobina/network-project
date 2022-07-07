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
#%%
print("numero di NaN nella colonna Time:", len([i for i in dataset.Time if type(i) == float])) # abbiamo solo 10 Na
#%%
for w in dataset.Location:
    print(w)
#%%
dataset.keys()
#%%
dataset.keys()
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