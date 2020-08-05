from random import randint

MOZNOSTI = ['Kamen', 'Škarje', 'Papir']
MOZNOSTI_2 = ['Kamen', 'Škarje', 'Papir', 'Voda', 'Ogenj']
ZACETNO_STANJE = 'Začetno stanje'

class Igra:

    def __init__(self):
        self.igralec = 0
        self.racunalnik = 0

    def tocka_za_igralca(self):
        self.igralec += 1
    
    def tocka_za_racunalnik(self):
        self.racunalnik += 1
    
    def delni_izid_igralca(self):
        return self.igralec
    
    def delni_izid_racunalnika(self):
        return self.racunalnik

class KamenSkarjePapir(Igra):

    def potek_igre(self, izbrano_orozje):
    # Sprememba!!! igra se do 7 iger in se bo potem določilo zmagovalca
            slovar_izbir = {'Kamen': 0, 'Škarje': 1, 'Papir': 2}

            igralec = slovar_izbir.get(MOZNOSTI[izbrano_orozje])
            racunalnik = slovar_izbir.get(self.izberi_orozje_racunalnik())

            mozni_izidi = [
                [0, 1, -1],
                [-1, 0, 1],
                [1, -1, 0]
            ] # 1 pomeni, da je zmagal igralec -1 pomeni da je zmagal računalnik 0 pomeni izenačenje
            # igralec predstavlja vrstice, računalnik predstavlja stolpce
            rezultat = mozni_izidi[igralec][racunalnik]

            if rezultat == 1:
                self.tocka_za_igralca()
            elif rezultat == -1:
                self.tocka_za_racunalnik()
            elif rezultat == 0:
                pass
            else:
                assert False

    def izberi_orozje_racunalnik(self):
        return MOZNOSTI[randint(0, 2)]

    def konec_igre(self):
        return self.igralec + self.racunalnik == 7
    
    def zmaga_igralca(self):
        return self.igralec > self.racunalnik and self.konec_igre() == True

    def koncni_izid_racunalnika(self):
        if self.konec_igre() == True:
            return self.racunalnik
        else:
            pass

    def koncni_izid_igralca(self):
        if self.konec_igre() == True:
            return self.igralec
        else:
            pass

class KamenSkarjePapirOgenjVoda(Igra):

    def potek_igre_1(self, izbrano_orozje):

            slovar_izbir = {'Kamen': 0, 'Škarje': 1, 'Papir': 2, 'Ogenj': 3, 'Voda': 4}

            igralec = slovar_izbir.get(MOZNOSTI_2[izbrano_orozje])
            racunalnik = slovar_izbir.get(self.izberi_orozje_1_racunalnik())

            mozni_izidi = [
                [0, 1, -1, -1, 1],
                [-1, 0, 1, -1, 1],
                [1, -1, 0, -1, 1],
                [1, 1, 1, 0, -1],
                [-1, -1, -1, 1, 0]
            ]

            rezultat = mozni_izidi[igralec][racunalnik]

            if rezultat == 1:
                self.tocka_za_igralca()
            elif rezultat == -1:
                self.tocka_za_racunalnik()
            elif rezultat == 0:
                pass
            else:
                assert False
            
    def izberi_orozje_1_racunalnik(self):
        return MOZNOSTI_2[randint(0, 4)]
    
    def zmaga_igralca_1(self):
        return self.igralec > self.racunalnik and self.konec_igre_1() == True

    def konec_igre_1(self):
        return self.racunalnik + self.igralec == 15
        #tukaj se bo igra igrala do 15 iger
    def koncni_izid_racunalnika_1(self):
        if self.konec_igre_1() == True:
            return self.racunalnik
        else:
            pass

    def koncni_izid_igralca_1(self):
        if self.konec_igre_1() == True:
            return self.igralec
        else:
            pass
        
def nova_igra():
    return KamenSkarjePapir()

def nova_igra_1():
    return KamenSkarjePapirOgenjVoda()

class DatotekaKSP:

    def __init__(self):
        self.igre = {}
    
    def prosti_id_igre(self):
        if len(self.igre) == 0:
            return 0
        else:
            return len(self.igre) + 1

    def nova_igra(self):
        nov_id = self.prosti_id_igre()
        sveza_igra = nova_igra()
            
        self.igre[nov_id] = (sveza_igra, ZACETNO_STANJE)
        return nov_id


        