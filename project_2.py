import mysql.connector
try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456789",
        database="project_2"
    )
    print("\nPřipojení k databázi bylo úspěšné.")
except mysql.connector.Error as err:
    print(f"\nChyba při připojování: {err}")
cursor = conn.cursor()
try:
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ukoly (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nazev VARCHAR(50),
            popis TEXT,
            stav VARCHAR (20) DEFAULT 'Nezahájeno',
            datum DATE
        )
    ''')
    print("Tabulka 'ukoly' je připravena.\n")
except mysql.connector.Error as err:
    print(f"Chyba při vytváření tabulky: {err}")
def pridat_ukol():
    nazev_ukolu=input("\nZadejte název úkolu: ").strip()
    while not nazev_ukolu:
        nazev_ukolu=input("Zadali jste prázdný název úkolu. Prosím zadejte znovu: ")
    popis_ukolu=input("Zadejte popis úkolu: ").strip()
    while not popis_ukolu:
        popis_ukolu=input(f"Zadali jste prázdný popis k úkolu {nazev_ukolu}. Zadejte popis: ").strip()
    from datetime import date
    datum_vytvoreni=date.today()
    novy_ukol = (nazev_ukolu, popis_ukolu, datum_vytvoreni)
    try:
        cursor.execute("INSERT INTO ukoly (nazev, popis, datum) VALUES (%s, %s, %s)", novy_ukol)
        conn.commit()
        print("Záznam byl vložen.")
        print(f"Úkol '{nazev_ukolu}' byl přidán.\n")
    except mysql.connector.Error as err:
        print(f"Chyba při vkládání dat: {err}\n")
def zobrazit_ukoly():
    cursor.execute("SELECT id, nazev, popis, stav FROM ukoly WHERE stav != 'Hotovo'")
    ukoly=cursor.fetchall()
    if not ukoly:
        print("\nMomentálně tu nejsou žádné úkoly.\n")
        return
    print("\nSeznam úkolů:")
    for row in ukoly: 
        print(f"ID: {row[0]} | Název: {row[1]} | Popis: {row[2]} | Stav: {row[3]}")
    print()
def aktualizovat_ukol():
    cursor.execute("SELECT id, nazev, stav FROM ukoly")
    ukoly=cursor.fetchall()
    if not ukoly:
        print("\nNejsou tu žádné úkoly k aktualizování.\n")
        return
    print("\nSeznam úkolů:")
    for row in ukoly:
        print(f"{row[0]}. {row[1]} ({row[2]})") 
    while True:
        try:
            id_ukolu=int(input("Zadejte číslo úkolu, který chcete aktualizovat: "))
            cursor.execute("SELECT 1 FROM ukoly WHERE id = %s", (id_ukolu,))
            rows_returned=cursor.fetchone() 
            if rows_returned is not None:
                print("\nVyberte 1 pro změnu stavu na Probíhá\n" \
                    "Vyberte 2 pro změnu stavu na Hotovo")
                cislo_stavu=input("Vyberte možnost 1 nebo 2: ")
                while cislo_stavu not in ("1", "2"):
                    cislo_stavu=input("Vyberte prosím možnost 1 nebo 2: ")
                if cislo_stavu =="1":
                    stav_ukolu=('Probíhá')
                elif cislo_stavu =="2":
                    stav_ukolu=('Hotovo')
                cursor.execute("UPDATE ukoly SET stav = %s WHERE id = %s", (stav_ukolu, id_ukolu))
                conn.commit()
                print(f"Úkol č. {id_ukolu} byl aktualizován a nyní je ve stavu {stav_ukolu}.\n")
                break
            else:
                print("Chyba. Úkol s tímto číslem neexistuje.")
        except ValueError:
            print("Zadejte prosím číslo.")
def odstranit_ukol():
    cursor.execute("SELECT id, nazev, popis, stav, datum FROM ukoly")
    ukoly=cursor.fetchall()
    if not ukoly:
        print("\nMomentálně tu nejsou žádné úkoly k mazání.\n")
        return
    print("\nSeznam úkolů:")
    for row in ukoly:
        print(f"{row[0]}. Název: {row[1]} | Popis: {row[2]} | Stav: {row[3]}| Datum založení: {row[4]}") 
    while True:
        try:
            id_ukolu=int(input("\nZadejte číslo úkolu, který chcete odstranit: ")) 
            cursor.execute("SELECT 1 FROM ukoly WHERE id = %s", (id_ukolu,))
            rows_returned=cursor.fetchone()
            if rows_returned is not None:
                cursor.execute("DELETE from ukoly WHERE id = %s",  (id_ukolu,))
                conn.commit()
                print(f"\nÚkol č. {id_ukolu} byl odstraněn.\n")
                break
            else:
                print("Chyba. Pokoušíte se smazat neexistující úkol.")
        except ValueError:
            print("Chyba. Zadejte platné číslo úkolu.")
def hlavni_menu():
    while True:
        print("Správce úkolů: Hlavní menu\n" \
        "1. Přidat nový úkol\n" \
        "2. Zobrazit úkoly\n" \
        "3. Aktualizovat úkol\n" \
        "4. Odstranit úkol\n" \
        "5. Ukončit program")
        user_input=input("Vyberte možnost (1-5): ")
        while user_input not in ("1", "2", "3", "4", "5"):
            user_input=input("Prosím vyberte platnou možnost (1-5): ")
        if user_input=="1":
            print ("\nVybrali jste 1 - Přidat úkol")
            pridat_ukol()
        elif user_input=="2":
            print("\nVybrali jste 2 - Zobrazit úkoly")
            zobrazit_ukoly()
        elif user_input=="3":
            print("\nVybrali jste 3 - Aktualizovat úkol")
            aktualizovat_ukol()
        elif user_input=="4":
            print("\nVybrali jste 4 - Odstranit úkol")
            odstranit_ukol()
        elif user_input=="5":
            cursor.close() 
            conn.close() 
            print("\nPřipojení k databázi bylo uzavřeno.") 
            print("Konec programu.")
            break
hlavni_menu()
