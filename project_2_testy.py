import pytest
import mysql.connector
from datetime import date
@pytest.fixture(scope="function")
def db_setup():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456789",
        database="project_2_testovaci"
    )
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS test_ukoly (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nazev VARCHAR(50),
            popis TEXT,
            stav VARCHAR (20) DEFAULT 'Nezahájeno',
            datum DATE
        )
    ''')
    conn.commit() 
    yield conn, cursor
    cursor.execute("DROP TABLE IF EXISTS test_ukoly")
    conn.commit()
    cursor.close()
    conn.close()
#testy pro pridat_ukol
def test_pridat_ukol(db_setup):
    conn, cursor = db_setup
    cursor.execute("INSERT INTO test_ukoly (nazev, popis) VALUES ('Úkol1', 'Testovací úkol')")
    conn.commit()
    cursor.execute("SELECT * FROM test_ukoly WHERE nazev = 'Úkol1'")
    result = cursor.fetchone()
    assert result is not None, "Záznam nebyl vložen do tabulky."
    assert result[1] == "Úkol1", "Název není správný."
    assert result[2] == "Testovací úkol", "Popis není správný."
def test_pridat_neplatny_ukol(db_setup):
    conn, cursor = db_setup
    with pytest.raises(mysql.connector.Error, match="Data too long"):
        cursor.execute("INSERT INTO test_ukoly (nazev) VALUES (%s)", ('a' * 51))
        conn.commit()
#testy pro aktualizovat_ukol
def test_aktualizovat_ukol(db_setup):
    conn, cursor = db_setup
    cursor.execute("INSERT INTO test_ukoly (nazev, popis) VALUES ('Úkol1', 'Testovací úkol')")
    conn.commit()
    cursor.execute("UPDATE test_ukoly SET stav = 'Hotovo' WHERE nazev = 'Úkol1'")
    conn.commit()
    cursor.execute("SELECT stav FROM test_ukoly WHERE nazev = 'Úkol1'")
    result = cursor.fetchone()
    assert result[0] == 'Hotovo', "Stav úkolu nebyl správně aktualizován."
def test_aktualizovat_neexistujici_ukol(db_setup):
    conn, cursor = db_setup
    cursor.execute("INSERT INTO test_ukoly (nazev, popis) VALUES ('Úkol1','Testovací úkol')")
    conn.commit()
    cursor.execute("SELECT COUNT(*) FROM test_ukoly WHERE stav = 'Nezahájeno'")
    puvodni_pocet = cursor.fetchone()[0]
    cursor.execute("UPDATE test_ukoly SET stav = 'Probíhá' WHERE nazev = 'Úkol999'")
    conn.commit()
    cursor.execute("SELECT COUNT(*) FROM test_ukoly WHERE stav = 'Probíhá'")
    konecny_pocet = cursor.fetchone()[0]
    assert puvodni_pocet == konecny_pocet, "Aktualizace neexistujícího záznamu změnila stav databáze."
#testy pro odstranit_ukol
def test_odstranit_ukol(db_setup):
    conn, cursor = db_setup
    cursor.execute("INSERT INTO test_ukoly (nazev, popis) VALUES ('Úkol1', 'Testovací úkol')")
    conn.commit()
    cursor.execute("DELETE FROM test_ukoly WHERE nazev = 'Úkol1'")
    conn.commit()
    cursor.execute("SELECT * FROM test_ukoly WHERE nazev = 'Úkol1'")
    result = cursor.fetchone()
    assert result is None, "Záznam nebyl správně smazán."
def test_odstranit_neexistujici_ukol(db_setup):
    conn, cursor = db_setup
    cursor.execute("SELECT COUNT(*) FROM test_ukoly")
    puvodni_pocet = cursor.fetchone()[0]
    cursor.execute("DELETE FROM test_ukoly WHERE nazev = 'Úkol99'")
    conn.commit()
    cursor.execute("SELECT COUNT(*) FROM test_ukoly")
    konecny_pocet = cursor.fetchone()[0]
    assert puvodni_pocet == konecny_pocet, "Mazání neexistujícího záznamu změnilo stav databáze."