import os
import json
import psycopg2
from random import randint
from dotenv import load_dotenv
from psycopg2 import Error

load_dotenv()
DB_URL = os.environ["DB_URL"]
MOZNOSTI = ['Kamen', 'Škarje', 'Papir']
MOZNOSTI_2 = ['Kamen', 'Škarje', 'Papir', 'Voda', 'Ogenj']
DATOTEKA_KSP = 'datoteke/ksp.json'
DATOTEKA_KSPOV = 'datoteke/kspov.json'
ZACETEK = 'Zacetek'

class Igra:

    def __init__(self, igralec=0, racunalnik=0):
        self.igralec = igralec
        self.racunalnik = racunalnik

    def tocka_za_igralca(self):
        self.igralec += 1
    
    def tocka_za_racunalnik(self):
        self.racunalnik += 1
    
    def delni_izid_igralca(self):
        return self.igralec
    
    def delni_izid_racunalnika(self):
        return self.racunalnik

#============================================================================================================================================================

class KamenSkarjePapir(Igra):

    def potek_igre(self, izbrano_orozje):
    #igra se do 7 iger in se bo potem določilo zmagovalca
            slovar_izbir = {'Kamen': 0, 'Škarje': 1, 'Papir': 2}

            igralec = slovar_izbir.get(MOZNOSTI[izbrano_orozje])
            racunalnik = slovar_izbir.get(self.izberi_orozje_racunalnik())

            mozni_izidi = [
                [3, 1, 2],
                [2, 3, 1],
                [1, 2, 3]
            ] # 1 pomeni, da je zmagal igralec 2 pomeni da je zmagal računalnik 3 pomeni izenačenje
            # igralec predstavlja vrstice, računalnik predstavlja stolpce
            rezultat = mozni_izidi[igralec][racunalnik]

            if rezultat == 1:
                self.tocka_za_igralca()
            elif rezultat == 2:
                self.tocka_za_racunalnik()
            elif rezultat == 3:
                pass
            else:
                assert False

    def izberi_orozje_racunalnik(self):
        return MOZNOSTI[randint(0, 2)]

    def konec_igre(self):
        return self.igralec + self.racunalnik == 7
    
    def zmaga_igralca(self):
        return self.igralec > self.racunalnik and self.konec_igre() == True
    
    def zmaga_racunalnika(self):
        return self.igralec < self.racunalnik and self.konec_igre() == True

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

#=========================================================================================================================================================

class KamenSkarjePapirOgenjVoda(Igra):

    def potek_igre_1(self, izbrano_orozje):

            slovar_izbir = {'Kamen': 0, 'Škarje': 1, 'Papir': 2, 'Ogenj': 3, 'Voda': 4}

            igralec = slovar_izbir.get(MOZNOSTI_2[izbrano_orozje])
            racunalnik = slovar_izbir.get(self.izberi_orozje_1_racunalnik())

            mozni_izidi = [
                [3, 1, 2, 2, 1],
                [2, 3, 1, 2, 1],
                [1, 2, 3, 2, 1],
                [1, 1, 1, 3, 2],
                [2, 2, 2, 1, 3]
            ]

            rezultat = mozni_izidi[igralec][racunalnik]

            if rezultat == 1:
                self.tocka_za_igralca()
            elif rezultat == 2:
                self.tocka_za_racunalnik()
            elif rezultat == 3:
                pass
            else:
                assert False
            
    def izberi_orozje_1_racunalnik(self):
        return MOZNOSTI_2[randint(0, 4)]
    
    def zmaga_igralca_1(self):
        return self.igralec > self.racunalnik and self.konec_igre_1() == True
    
    def zmaga_racunalnika_1(self):
        return self.igralec < self.racunalnik and self.konec_igre_1() == True

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

#=========================================================================================================================================================
        
def nova_igra():
    return KamenSkarjePapir(igralec=0, racunalnik=0)

def nova_igra_1():
    return KamenSkarjePapirOgenjVoda(igralec=0, racunalnik=0)

#=========================================================================================================================================================

class Datoteka:

    def __init__(self):
        self.igre = {}
        self.uporabnik = ""
        self.id = 0

    def nastavi_uporabnika(self, uporabnik):
        self.uporabnik = uporabnik

    def prosti_id_igre(self):
        self.id = self.id + 1
        return self.id
    
    def nastavi_id(self, id):
        self.id = id

#============================================================================================================================================================
   
class KSP(Datoteka):

    def nova_igra(self):
        self.preberi_iz_datoteke()
        nov_id = self.prosti_id_igre()
        sveza_igra = nova_igra()

        self.igre[nov_id] = sveza_igra
        self.shrani_v_datoteko()
        return nov_id

    def potek_igre(self, id_igre, orozje):
        self.preberi_iz_datoteke()
        trenutna_igra = self.igre[id_igre]

        trenutna_igra.potek_igre(orozje)
        self.igre[id_igre] = trenutna_igra

        self.shrani_v_datoteko()

    def shrani_v_datoteko(self):
        # Preberi obstoječe podatke
        if os.path.exists(DATOTEKA_KSP) and os.stat(DATOTEKA_KSP).st_size > 0:
            with open(DATOTEKA_KSP, "r", encoding="utf-8") as izhodna:
                vsi_uporabniki = json.load(izhodna)
        else:
            vsi_uporabniki = {}

        # Shranimo igre za trenutnega uporabnika
        vsi_uporabniki[self.uporabnik] = {
            id_igre: (igra.igralec, igra.racunalnik) for id_igre, igra in self.igre.items()
        }

        with open(DATOTEKA_KSP, "w", encoding="utf-8") as izhodna:
            json.dump(vsi_uporabniki, izhodna, ensure_ascii=False, indent=2)


    def preberi_iz_datoteke(self):
        if not os.path.exists(DATOTEKA_KSP) or os.stat(DATOTEKA_KSP).st_size == 0:
            self.igre = {}
            return

        with open(DATOTEKA_KSP, "r", encoding="utf-8") as vhodna:
            vsi_uporabniki = json.load(vhodna)

        # Preberi samo igre za prijavljenega uporabnika
        if self.uporabnik in vsi_uporabniki:
            igre = vsi_uporabniki[self.uporabnik]
            self.igre = {
                int(id_igre): KamenSkarjePapir(igralec, racunalnik)
                for id_igre, (igralec, racunalnik) in igre.items()
            }
        else:
            self.igre = {}

    def insert_game_ksp(self, game_id, player_score, computer_score):
        connection = psycopg2.connect(DB_URL)
        cursor = connection.cursor()

        upsert_sql = """
            INSERT INTO ksp (username, game_id, player, computer)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (username, game_id) DO UPDATE
                SET player   = EXCLUDED.player,
                    computer = EXCLUDED.computer
            """
        cursor.execute(upsert_sql, (self.uporabnik, game_id, player_score, computer_score))

        connection.commit()
        cursor.close()
        connection.close()
        print("Data loaded into ksp.")
    
    def get_id_ksp(self):
        conn = psycopg2.connect(DB_URL)
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT MAX(game_id) FROM ksp WHERE username = %s",
                    (self.uporabnik,)
                )
                row = cur.fetchone()
                max_id = row[0]
                if max_id is not None:
                    self.id = row[0]
                else:
                    self.id = 0
        finally:
            conn.close()

    def load_user_history_ksp(self):
        conn = psycopg2.connect(DB_URL)
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT game_id, player, computer
                    FROM ksp
                    WHERE username = %s
                    ORDER BY game_id
                    """,
                    (self.uporabnik,)
                )
                rows = cur.fetchall()

            user_games = {
                str(gid): [player, computer]
                for gid, player, computer in rows
            }

            with open(DATOTEKA_KSP, "r", encoding="utf-8") as f:
                    try:
                        all_data = json.load(f)
                    except json.JSONDecodeError:
                        all_data = {}

            existing = all_data.get(self.uporabnik, {})
            existing.update(user_games)
            all_data[self.uporabnik] = existing

            with open(DATOTEKA_KSP, "w", encoding="utf-8") as f:
                json.dump(all_data, f, indent=2, ensure_ascii=False)

        finally:
            conn.close()

    def delete_ksp(self):
        conn = psycopg2.connect(DB_URL)
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "DELETE FROM ksp WHERE username = %s",
                    (self.uporabnik,)
                )
            conn.commit()
            self.id = 0
        finally:
            conn.close()
        
#=========================================================================================================================================================

class KSPOV(Datoteka):

    def nova_igra_1(self):
        self.preberi_iz_datoteke()
        nov_id = self.prosti_id_igre()
        sveza_igra = nova_igra_1()

        self.igre[nov_id] = sveza_igra
        self.shrani_v_datoteko()
        return nov_id

    def potek_igre_1(self, id_igre, orozje):
        self.preberi_iz_datoteke()
        trenutna_igra = self.igre[id_igre]

        trenutna_igra.potek_igre_1(orozje)
        self.igre[id_igre] = trenutna_igra

        self.shrani_v_datoteko()


    def shrani_v_datoteko(self):
        # Preberi obstoječe podatke
        if os.path.exists(DATOTEKA_KSPOV) and os.stat(DATOTEKA_KSPOV).st_size > 0:
            with open(DATOTEKA_KSPOV, "r", encoding="utf-8") as izhodna:
                vsi_uporabniki = json.load(izhodna)
        else:
            vsi_uporabniki = {}

        # Shranimo igre za trenutnega uporabnika
        vsi_uporabniki[self.uporabnik] = {
            id_igre: (igra.igralec, igra.racunalnik) for id_igre, igra in self.igre.items()
        }

        with open(DATOTEKA_KSPOV, "w", encoding="utf-8") as izhodna:
            json.dump(vsi_uporabniki, izhodna, ensure_ascii=False, indent=2)


    def preberi_iz_datoteke(self):
        if not os.path.exists(DATOTEKA_KSPOV) or os.stat(DATOTEKA_KSPOV).st_size == 0:
            self.igre = {}
            return

        with open(DATOTEKA_KSPOV, "r", encoding="utf-8") as vhodna:
            vsi_uporabniki = json.load(vhodna)

        if self.uporabnik in vsi_uporabniki:
            igre = vsi_uporabniki[self.uporabnik]
            self.igre = {
                int(id_igre): KamenSkarjePapirOgenjVoda(igralec, racunalnik)
                for id_igre, (igralec, racunalnik) in igre.items()
            }
        else:
            self.igre = {}

    def insert_game_kspov(self, game_id, player_score, computer_score):
        connection = psycopg2.connect(DB_URL)
        cursor = connection.cursor()

        upsert_sql = """
            INSERT INTO kspov (username, game_id, player, computer)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (username, game_id) DO UPDATE
                SET player   = EXCLUDED.player,
                    computer = EXCLUDED.computer
            """
        cursor.execute(upsert_sql, (self.uporabnik, game_id, player_score, computer_score))

        connection.commit()
        cursor.close()
        connection.close()
        print("Data loaded into kspov.")

    def get_id_kspov(self):
        conn = psycopg2.connect(DB_URL)
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT MAX(game_id) FROM kspov WHERE username = %s",
                    (self.uporabnik,)
                )
                row = cur.fetchone()
                max_id = row[0]
                if max_id is not None:
                    self.id = row[0]
                else:
                    self.id = 0
        finally:
            conn.close()

    def load_user_history_kspov(self):
        conn = psycopg2.connect(DB_URL)
        try:
            with conn.cursor() as cur:
                cur.execute(
                """
                 SELECT game_id, player, computer
                 FROM kspov
                 WHERE username = %s
                 ORDER BY game_id
                """,
                (self.uporabnik,)
                )
                rows = cur.fetchall()
            user_games = { str(gid): [player, computer] for gid, player, computer in rows }

            with open(DATOTEKA_KSPOV, "r", encoding="utf-8") as f:
                try:
                    all_data = json.load(f)
                except json.JSONDecodeError:
                    all_data = {}
                
            existing = all_data.get(self.uporabnik, {})
            existing.update(user_games)         # add/overwrite only those game_ids
            all_data[self.uporabnik] = existing

            with open(DATOTEKA_KSPOV, "w", encoding="utf-8") as f:
                json.dump(all_data, f, indent=2, ensure_ascii=False)
        finally:
            conn.close()

    def delete_kspov(self):
        conn = psycopg2.connect(DB_URL)
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "DELETE FROM kspov WHERE username = %s",
                    (self.uporabnik,)
                )
            conn.commit()
            self.id = 0
        finally:
            conn.close()

#pomembno je da beležim rezultat igre in sicer to lahko shranim v datoteko kot {id_igre: [igralec, racunalnik]



        