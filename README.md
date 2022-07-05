# NETWORK PROJECT

| Domande del progetto |

## TODO:
- Inserire le domande sulle quali si basa il progetto
- Scegliere dataset: ✓


- Pulizia dataset
  - Data -> solo anno --> FATTO AL 100%
  - Time -> controllare distribuzione: se significativa gestire i null sennó togliamo la colonna
  - Location -> se c'é la virgola tenere quello che c'é dopo sennó tenere tutto. Capire come gestire URSS e Russia
  - <font color="red">Operator</font> -> Raggruppare per: militare, civile, forse terza per poste ecc.. **Raggruppamento militare fatto**
  - Flight -> ELIMINARE
  - <font color="red">Route</font> -> splittare aeroporto partenza e arrivo, attenzione rotte multiple, attenzione *"test flight"*, trovare coordinate **SPLIT ROTTE FATTO**
  - <font color="red">AC type</font> -> raggruppamento e attenzione ai similari **FATTO AL 80%**
  - Registration -> ELIMINARE
  - cn/ln -> ELIMINARE
  - <font color="red">Aboard</font> -> gestire nulli 
  - <font color="red">Aboard crew</font> -> gestire nulli 
  - <font color="red">Aboard passengers</font> -> gestire nulli 
  - <font color="red">Fatalities</font> -> gestire nulli 
  - <font color="red">Fatalities crew</font> -> gestire nulli 
  - <font color="red">Fatalities passengers</font> -> gestire nulli 
  - <font color="red">Ground</font> -> da capire cosa significa ✓ = numero morti a terra dovuto allo schianto su persone
  - <font color="red">Summary</font> -> gestire = proposta paxxa: mini *topic moddeling*?


- Analisi vera e propria
- Creare presentazione 
  - Creare poster



**Scadenza: 17 luglio**



### <font color="yellow">TODO (GABRO):</font>

- Identificare altre macro-categorie di Operatori e fare il raggruppamento (tipo ci sono quelli delle poste)
- Cercare di aggiungere le coordinate delle rotte / capire se sono necessarie per inserire il grafo in una mappa
- Sistemare il problema dei valori non upper dovuti agli Na su AC Type e decidere se ridurre ancora di più i valori univoci
 
