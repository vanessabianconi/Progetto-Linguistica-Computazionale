 # -*- coding: utf-8 -*-
import sys
import codecs
import nltk
import re

def EstraiTestoTokenizzato(frasi):
	tokensTOT=[] #lista in cui inserisco i tokens
	for frase in frasi:
		tokens=nltk.word_tokenize(frase) #divido le frasi in tokens
		tokensTOT = tokensTOT+tokens
	return tokensTOT #restituisco i tokens

def AnnotazioneLinguistica(frasi) :
        tokensTOT=[] #lista in cui inserisco i tokens
        tokensPOStot=[] #lista in cui inserisco i l'analisi POS dei tokens
        for frase in frasi :
                tokens=nltk.word_tokenize(frase) #divido le frasi in tokens
                tokensPOS=nltk.pos_tag(tokens) #analisi POS dei tokens
                tokensTOT=tokensTOT+tokens
                tokensPOStot=tokensPOStot+tokensPOS
        return tokensPOStot #restituisco i tokens con l'analisi POS


def Nomi(frasi):
	listanomi = [] #lista dove inserisco i nomi 
	for frase in frasi:
		tokens = nltk.word_tokenize(frase) #divido le frasi in tokens
		tokensPOS = nltk.pos_tag(tokens) #analisi POS dei tokens
		analisi = nltk.ne_chunk(tokensPOS) #restituisce il testo come un albero 
		for nodo in analisi: #ciclo l'albero e scorro i nodi 
			NE = ""
			if hasattr(nodo, 'label'): #controllo se chunck è un nodo intermedio 
				if nodo.label() in ["PERSON"]:
					for partNE in nodo.leaves(): #ciclo le foglie del nodo selezionato
						NE = NE+''+partNE[0]
					listanomi.append(NE) #aggiungo nomi alla lista
			frequenza = nltk.FreqDist(listanomi) #frequenza dei nomi
			DieciNomi = frequenza.most_common(10) #prendo i 10 nomi più frequenti
	return DieciNomi #restituisco i nomi 



def FrasiNomi(frasi, nomi):
	listafrasi = [] #lista in cui inserisco le frasi in cui sono contenuti i nomi 
	for frase in frasi:
		for elem in nomi:
			if elem[0] in frase: #se l'elemento con indice 0 (cioè il nome) si trova nella frase, la inserisco nella lista
				listafrasi.append(frase)
	return listafrasi

def FraseBreveLunga(frasi, nomi): 
	LunghezzaMAX = 0.0 #inizializzo la lunghezza massima
	LunghezzaMIN = 0.0 #inizializzo la lunghezza minima
	FraseMAX = [] #lista in cui inserisco la frase massima
	FraseMIN = [] #lista in cui inserisco la frase minima
	for frase in frasi: 
		tokens=nltk.word_tokenize(frase) #divido la frase in tokens
		Lunghezza = len(tokens) #conto i tokens
		for elem in nomi: 
			if elem[0] in frase: #controllo se l'elemento con indice 0 (ovvero il nome) si trova nella frase
				if Lunghezza > LunghezzaMAX: #confronto la lunghezza della frase con la lunghezza massima 
					LunghezzaMAX = Lunghezza
					FraseMAX = frase
				else:
					LunghezzaMIN = Lunghezza #confronto la lunghezza della frase con la lunghezza minima 
					FraseMIN = frase
	return FraseMIN, FraseMAX #restituisco la frase minima e la frase massima

		



def Luoghi (frasi):
	listaluoghi = [] #lista dove inserisco i luoghi 
	for frase in frasi:
		tokens = nltk.word_tokenize(frase) #divido le frasi in tokens
		tokensPOS = nltk.pos_tag(tokens) #analisi POS dei tokens
		analisi = nltk.ne_chunk(tokensPOS) #restituisce il testo come un albero 
		for nodo in analisi: #ciclo l'albero e scorro i nodi 
			NE = " "
			if hasattr(nodo, 'label'): #controllo se chunck è un nodo intermedio 
				if nodo.label() in ['GPE']:
					for partNE in nodo.leaves(): #ciclo le foglie del nodo selezionato
						NE = NE+ ''+partNE[0]
					listaluoghi.append(NE) #aggiungo i luoghi alla lista
	frequenza = nltk.FreqDist(listaluoghi) #frequenza dei luoghi
	DieciLuoghi = frequenza.most_common(10) #prendo i 10 luoghi più frequenti 
	return DieciLuoghi #restituisco i luoghi 


def Sostantivi(POS):
	lista = [] #lista in cui inserisco i sostantivi 
	posSostantivi = ["NN", "NNS", "NNP", "NNPS"] #POS dei sostantivi 
	for (token, pos) in POS:
		if pos in posSostantivi:
			lista.append(token) #se il POS è giusto inserisco il token nella lista creata all'inizio 
	frequenza = nltk.FreqDist(lista) #calcolo la frequenza dei sostantivi
	DieciSostantivi = frequenza.most_common(10) #prendo i 10 sostantivi più frequenti
	return DieciSostantivi




def Verbi(POS):
	lista = [] #lista in cui inserisco i verbi
	posVerbi = ["VB", "VBD", "VBG", "VBP", "VBZ", "VBN"] #POS verbi
	for (token, pos) in POS:
		if pos in posVerbi:
			lista.append(token) #se il POS è giusto inserisco il token nella lista creata all'inizio
	frequenza = nltk.FreqDist(lista) #calcolo la frequenza dei verbi
	DieciVerbi = frequenza.most_common(10) #prendo i 10 verbi più frequenti 
	return DieciVerbi



def Date(frasi):
	Date = []
	for data in frasi:
		Date =  Date + re.findall(r'([\d]{1,2}/[\d]{1,2}/[\d]{2}|[\d]{1,2}/[\d]{1,2}/[\d]{4}|[\d]{1,2}\s(January|February|March|April|May|June|July|August|September|October|November|December)\s[\d]{4})',data) #regex per trovare le date nei seguenti formati: g(g)/m(m)/aa, g(g)/m(m)/aaaa e g(g) mese(stringa) aaaa
		frequenza = nltk.FreqDist(Date) #frequenza date
	if (Date == []): #controllo se la lista è vuota
		return("Il libro non contiene nessuna data")
	else: #se la lista non è vuota la restituisco insieme alla frequenza
		return set(Date), frequenza
	return

def Giorni(frasi):
	Giorni = []
	for giorno in frasi:
		Giorni = Giorni + re.findall(r'(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)',giorno) #regex per trovare i giorni 
		frequenza = nltk.FreqDist(Giorni) #frequenza giorni
	if (Giorni == []): #controllo se la lista è vuota
		return ("Il libro non contiene nessun giorno")       
	else: #se la lista non è vuota la restituisco insieme alla frequenza
		return set(Giorni), frequenza
	return


def Mesi(frasi): 
	Mesi = []
	for mese in frasi:
		Mesi = Mesi + re.findall(r'(January|February|March|April|May|June|July|August|September|October|November|December)',mese) #regex per trovare i mesi 
		frequenza = nltk.FreqDist(Mesi) #frequenza mesi
	if (Mesi == []): #controllo se la lista è vuota
		return("Il libro non contiene nessun mese")
	else: #se la lista non è vuota la restituisco insieme alla frequenza
		return set(Mesi), frequenza
	return

def MarkovLunghezzaFrasi(frasi):
	listafrasi = [] #lista in cui inserisco le frasi che soddisfano i criteri
	for frase in frasi:
		tokens = nltk.word_tokenize(frase) #divido la frase in token
		if len(tokens) > 7 and len(tokens) < 13:
			listafrasi.append(frase) #se la frase è lunga minino 8 tokens e massimo 12 tokens, la inserisco nella lista 
	return listafrasi	

def MarkovZero(LunghezzaCorpus, DistribuzioneDiFrequenza, frasi):
	probabilita = 1.0 #inizializzo la probabilità
	probMax = 0.0 #inizializzo la probabilità massima
	Frase = [] #lista in cui inserisco la frase con probabilità massima
	for frase in frasi:
		tokens = nltk.word_tokenize(frase) #divido le frasi in tokens
		for tok in tokens:
			probToken = (DistribuzioneDiFrequenza[tok]*1.0/LunghezzaCorpus*1.0) #calcolo la probaabilità del token
			probabilita = probabilita*probToken #calcolo la probabilità
		if probabilita > probMax: #controllo se la probabilità è > della probabilità massima
			probMax = probabilita
			Frase = frase
	return Frase, probMax #restituisco la frase e la probabilità massima



def main(file1, file2) :
    fileInpu1 = codecs.open(file1, "r", "utf-8") #apro i files con codecs
    fileInput2 = codecs.open(file2, "r", "utf-8")

    raw1 = fileInpu1.read() #leggo i files con read
    raw2 = fileInput2.read()

    sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle') #tokenizzatore nltk

    frasi1 = sent_tokenizer.tokenize(raw1) #divido i corpus in frasi
    frasi2 = sent_tokenizer.tokenize(raw2)

    Testotok1 = EstraiTestoTokenizzato(frasi1) #funzione che tokenizza tutte le frasi del corpus
    Testotok2 = EstraiTestoTokenizzato(frasi2)

    Dnomi1 = Nomi(frasi1) #funzione che estrae i nomi proori 
    Dnomi2 = Nomi(frasi2)

    Fnomi1 = FrasiNomi(frasi1, Dnomi1) #funzione che estrae tutte le frasi che contengono i nomi propri 
    Fnomi2 = FrasiNomi(frasi2, Dnomi2)


    Testotokenizzato1 = EstraiTestoTokenizzato(Fnomi1) #funzione che tokenizza le frasi in cui sono contenuti i nomi propri
    Testotokenizzato2 = EstraiTestoTokenizzato(Fnomi2)

    POS1 = AnnotazioneLinguistica(Testotokenizzato1) #funzione che fa l'analisi POS delle frasi in cui sono contenuti i nomi propri
    POS2 = AnnotazioneLinguistica(Testotokenizzato2)

   

    FraseBreve1, FraseLunga1 = FraseBreveLunga(Fnomi1, Dnomi1) #funzione che estrae la frase più breve e più lunga in cui sono contenuti i nomi propri 
    FraseBreve2, FraseLunga2 = FraseBreveLunga(Fnomi2, Dnomi2)

    print("Frase breve del", file1, ":" ,FraseBreve1, "\n\nFrase lunga del", file1, ":", FraseLunga1) #stampo la frase massima e la frase minima
    print("\nFrase breve del",file2,":" ,FraseBreve2, "\n\nFrase lunga del", file2, ":", FraseLunga2)
    
    
    


    Luoghi1 = Luoghi(Fnomi1) #funzione che estrae i luoghi che sono contenuti nelle frasi che contengono i nomi propri 
    Luoghi2 = Luoghi(Fnomi2)

    print("\nI 10 luoghi che compaiono nelle frasi in cui sono contenuti i nomi propri del", file1, "sono:", Luoghi1) #stampo i 10 luoghi più frequenti che si trovano nelle frasi in cui compaiono i nomi propri
    print("\nI 10 luoghi che compaiono nelle frasi in cui sono contenuti i nomi propri del", file2, "sono:", Luoghi2)

    Persone1 = Nomi(Fnomi1) #funzione che estrae i nomi di persona dalle frasi che contengono i nomi propri 
    Persone2 = Nomi(Fnomi2)

    print("\nI 10 nomi di persona che compaiono nelle frasi in cui sono contenuti i nomi propri del", file1, "sono:", Persone1) #stampo i 10 nomi propri più frequenti che si trovano nelle frasi in cui compaiono i nomi propri
    print("\nI 10 nomi di persona che compaiono nelle frasi in cui sono contenuti i nomi propri del", file2, "sono:", Persone2)

    Sostantivi1 = Sostantivi(POS1) #funzione che estrae i sostantivi dalle frasi che contengono i nomi propri 
    Sostantivi2 = Sostantivi(POS2)

    print("\nI 10 sostantivi che compaiono nelle frasi in cui sono contenuti i nomi propri del", file1, "sono:", Sostantivi1) #stampo i 10 sostantivi più frequenti che si trovano nelle frasi in cui compaiono i nomi propri
    print("\nI 10 sostantivi che compaiono nelle frasi in cui sono contenuti i nomi propri del", file2, "sono:", Sostantivi2)

    Verbi1 = Verbi(POS1) #funzione che estae i verbi dalle frasi che contengono i nomi propri 
    Verbi2 = Verbi(POS2)

    print("\nI 10 verbi che compaiono nelle frasi in cui sono contenuti i nomi propri del", file1, "sono:", Verbi1) #stampo i 10 verbi più frequenti che si trovano nelle frasi in cui compaiono i nomi propri
    print("\nI 10 verbi che compaiono nelle frasi in cui sono contenuti i nomi propri del", file2, "sono:", Verbi2)


    Date1 = Date(Fnomi1) #funzione che estrae le date
    Date2 = Date(Fnomi2)

    print("\nLe date del", file1, "sono:", Date1)
    print("\nLe date del", file2, "sono:", Date2)

    Giorni1 = Giorni(Fnomi1) #funzione che estrae i giorni della settimana
    Giorni2 = Giorni(Fnomi2)

    print("\nI giorni del", file1, "sono:", Giorni1)
    print("\nI giorni del", file2, "sono:", Giorni2)

    Mesi1 = Mesi(Fnomi1) #funzioni che estrae i mesi 
    Mesi2 = Mesi(Fnomi2)

    print("\nI mesi del", file1, "sono:", Mesi1)
    print("\nI mesi del", file2, "sono:", Mesi2)

    

    MLunghezzaFrasi1 = MarkovLunghezzaFrasi(Fnomi1) #funzione che estrae le frasi che hanno minimo 8 tokens e massimo 12 tokens
    MLunghezzaFrasi2 = MarkovLunghezzaFrasi(Fnomi2)

    Testo1 = len(Testotok1) #calcolo la lunghezza di tutto il corpus
    Testo2 = len(Testotok2) 

    Freq1 = nltk.FreqDist(Testotok1) #calcolo la frequenza dei token di tutto il corpus
    Freq2 = nltk.FreqDist(Testotok2)

    Markovzero1 = MarkovZero(Testo1, Freq1, MLunghezzaFrasi1) #funzione che calcola la probabilità massima con Markov zero
    Markovzero2 = MarkovZero(Testo2, Freq2, MLunghezzaFrasi2)

    print("\nLa frase con probabilità più alta, calcolata con un modello di Markov di ordine 0 del", file1, "è:", Markovzero1)
    print("\nLa frase con probabilità più alta, calcolata con un modello di Markov di ordine 0 del", file2, "è:", Markovzero2)

    
    

main(sys.argv[1], sys.argv[2])

