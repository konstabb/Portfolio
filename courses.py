import os
import os.path
import sqlite3
import pandas as pd

# poistaa tietokannan alussa (kätevä moduulin testailussa)
if os.path.exists("courses.db"):
    os.remove("courses.db")

db = sqlite3.connect("courses.db")
db.isolation_level = None

# luo tietokantaan tarvittavat taulut
def create_tables():
    db.execute("""CREATE TABLE Opettajat (
               id INTEGER PRIMARY KEY,
               nimi TEXT)""")
    db.execute("""CREATE TABLE Kurssit (
               id INTEGER PRIMARY KEY,
               nimi TEXT,
               op INTEGER)""")
    db.execute("""CREATE TABLE OpettajanKurssit (
               id INTEGER PRIMARY KEY,
               opettaja_id INTEGER REFERENCES Opettajat,
               kurssi_id INTEGER REFERENCES Kurssit)""")
    db.execute("""CREATE TABLE Opiskelijat (
               id INTEGER PRIMARY KEY,
               nimi TEXT)""")
    db.execute("""CREATE TABLE Suoritukset (
               id INTEGER PRIMARY KEY,
               opiskelija_id INTEGER REFERENCES Opiskelijat,
               kurssi_id INTEGER REFERENCES Kurssit,
               aika TIMESTAMP,
               arvosana INTEGER)""")
    db.execute("""CREATE TABLE Ryhmat (
               id INTEGER PRIMARY KEY,
               nimi TEXT)""")
    db.execute("""CREATE TABLE RyhmanJasenet (
               id INTEGER PRIMARY KEY,
               ryhma_id INTEGER REFERENCES Ryhmat,
               opiskelija_id INTEGER REFERENCES Opiskelijat,
               opettaja_id INTEGER REFERENCES Opettajat)""")


# lisää opettajan tietokantaan
def create_teacher(name):
    t = db.execute("""INSERT INTO Opettajat (nimi) VALUES (?)""",[name])
    return t.lastrowid

# lisää kurssin tietokantaan
def create_course(name, credits, teacher_ids):
    c = db.execute("""INSERT INTO Kurssit (nimi, op) VALUES (?,?)""",[name,credits])
    if len(teacher_ids) > 0:
        for t in teacher_ids:
            db.execute("""INSERT INTO OpettajanKurssit (opettaja_id, kurssi_id) VALUES (?, ?)""",[t, c.lastrowid])
    else:
        db.execute("""INSERT INTO OpettajanKurssit (opettaja_id, kurssi_id) VALUES (NULL, ?)""",[c.lastrowid])
    return c.lastrowid

# lisää opiskelijan tietokantaan
def create_student(name):
    s = db.execute("""INSERT INTO Opiskelijat (nimi) VALUES (?)""", [name])
    return s.lastrowid

# antaa opiskelijalle suorituksen kurssista
def add_credits(student_id, course_id, date, grade):
    h = db.execute("""INSERT INTO Suoritukset (opiskelija_id, kurssi_id, aika, arvosana)
                   VALUES (?,?,?,?)""", [student_id,course_id,date,grade])
    return h.lastrowid

# lisää ryhmän tietokantaan
def create_group(name, teacher_ids, student_ids):
    g = db.execute("""INSERT INTO Ryhmat (nimi) VALUES (?)""", [name])
    for t in teacher_ids:
        db.execute("""INSERT INTO RyhmanJasenet (ryhma_id, opettaja_id) VALUES (?,?)""", [g.lastrowid, t])
    for s in student_ids:
        db.execute("""INSERT INTO RyhmanJasenet (ryhma_id, opiskelija_id) VALUES (?,?)""", [g.lastrowid, s])

    return g


# hakee kurssit, joissa opettaja opettaa (aakkosjärjestyksessä)
def courses_by_teacher(teacher_name):
    a = db.execute("""SELECT K.nimi FROM Kurssit K, Opettajat O, OpettajanKurssit OK
                      WHERE O.nimi=? AND O.id=OK.opettaja_id AND K.id=OK.kurssi_id""", [teacher_name]).fetchall()
    return list(map(lambda x: x[0], a))

# hakee opettajan antamien opintopisteiden määrän
def credits_by_teacher(teacher_name):
    return db.execute("""SELECT SUM(K.op) FROM Kurssit K, Opettajat O, OpettajanKurssit OK, Suoritukset S
                      WHERE O.nimi=? AND O.id=OK.opettaja_id AND K.id=OK.kurssi_id AND S.kurssi_id = K.id""", [teacher_name]).fetchone()[0]

# hakee opiskelijan suorittamat kurssit arvosanoineen (aakkosjärjestyksessä)
def courses_by_student(student_name):
    return db.execute("""SELECT K.nimi, S.arvosana FROM Kurssit K, Opiskelijat O, Suoritukset S
                      WHERE O.nimi=? AND O.id=S.opiskelija_id AND K.id=S.kurssi_id""", [student_name]).fetchall()

# hakee tiettynä vuonna saatujen opintopisteiden määrän
def credits_by_year(year):
    return db.execute("""SELECT SUM(K.op) FROM Suoritukset S, Kurssit K 
                      WHERE LOWER(?) = SUBSTR(S.aika,0,5) AND K.id=S.kurssi_id""", [year]).fetchone()[0]


# hakee kurssin arvosanojen jakauman (järjestyksessä arvosanat 1-5)
def grade_distribution(course_name):
   a = db.execute("""SELECT S.arvosana, COUNT(*) FROM Suoritukset S LEFT JOIN Kurssit K ON K.id=S.kurssi_id
                     WHERE K.nimi=? GROUP BY S.arvosana""", [course_name]).fetchall()
   b = dict(zip(range(1,6), [0]*5))
   b.update(a)
   return b

# hakee listan kursseista (nimi, opettajien määrä, suorittajien määrä) (aakkosjärjestyksessä)
def course_list():
    return db.execute("""SELECT K.nimi, COUNT(DISTINCT OK.opettaja_id), COUNT(DISTINCT S.opiskelija_id)
                      FROM Kurssit K LEFT JOIN OpettajanKurssit OK ON K.id = OK.kurssi_id
                      LEFT JOIN Suoritukset S ON K.id = S.kurssi_id
                      GROUP BY K.nimi
                      ORDER BY K.nimi""").fetchall()

# hakee listan opettajista kursseineen (aakkosjärjestyksessä opettajat ja kurssit)
def teacher_list():
    a = db.execute("""SELECT O.nimi, K.nimi
                      FROM Opettajat O LEFT JOIN OpettajanKurssit OK ON O.id=OK.opettaja_id
                      LEFT JOIN Kurssit K ON K.id=OK.kurssi_id ORDER BY O.nimi""").fetchall()
    tulos = pd.DataFrame(a, columns=["O.nimi", "K.nimi"])
    tulos = tulos.groupby("O.nimi")["K.nimi"].apply(list).reset_index()
    return list(tulos.itertuples(index=False, name=None))

# hakee ryhmässä olevat henkilöt (aakkosjärjestyksessä)
def group_people(group_name):
    a = db.execute("""SELECT O.nimi nimi FROM Opettajat O, RyhmanJasenet RJ, Ryhmat R
                    WHERE O.id=RJ.opettaja_id AND RJ.ryhma_id=R.id AND R.nimi=?
                    UNION ALL
                    SELECT O.nimi nimi FROM Opiskelijat O, RyhmanJasenet RJ, Ryhmat R
                    WHERE O.id=RJ.opiskelija_id AND RJ.ryhma_id=R.id AND R.nimi=?
                    ORDER BY nimi""", [group_name]*2).fetchall()
    return list(map(lambda x:x[0], a))

# hakee ryhmissä saatujen opintopisteiden määrät (aakkosjärjestyksessä)
def credits_in_groups():
    return db.execute("""SELECT R.nimi, IFNULL(SUM(K.op),0)
                      FROM RyhmanJasenet RJ LEFT JOIN Ryhmat R ON R.id=RJ.ryhma_id
                      LEFT JOIN Suoritukset S ON RJ.opiskelija_id=S.opiskelija_id
                      LEFT JOIN Kurssit K ON K.id=S.kurssi_id
                      GROUP BY R.nimi
                      ORDER BY R.nimi""").fetchall()

# hakee ryhmät, joissa on tietty opettaja ja opiskelija (aakkosjärjestyksessä)
def common_groups(teacher_name, student_name):
    a = db.execute(""" SELECT OpenRyhmat.nimi FROM
                   (SELECT R.nimi 
                      FROM RyhmanJasenet RJ LEFT JOIN Ryhmat R ON R.id=RJ.ryhma_id
                      LEFT JOIN Opettajat Ope ON RJ.opettaja_id=Ope.id
                      WHERE Ope.nimi=?) OpenRyhmat,
                   
                    (SELECT R.nimi 
                      FROM RyhmanJasenet RJ LEFT JOIN Ryhmat R ON R.id=RJ.ryhma_id
                      LEFT JOIN Opiskelijat Opi ON RJ.opiskelija_id=Opi.id
                      WHERE Opi.nimi=?) OpinRyhmat
                   
                   WHERE OpenRyhmat.nimi=OpinRyhmat.nimi
                   ORDER BY OpenRyhmat.nimi""",[teacher_name, student_name]).fetchall()
    
    return list(map(lambda x:x[0], a))

