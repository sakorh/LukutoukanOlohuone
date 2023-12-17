# LukutoukanOlohuone
Lukutoukan olohuone on kaikkialla mukana kulkeva kirjasto, jossa asiakkaat voivat lainata, palauttaa ja arvioida hyllystä löytyviä kirjoja. Kokoelmaan voi myös toivoa uusia teoksia, jotka sovelluksen ylläpitäjä voi lisätä, mikäli halukkaita lukijoita on tarpeeksi. 

## Sovelluksen ominaisuudet:
* Käyttäjä voi kirjautua sisään ja ulos, ja rekisteröidä uuden tunnuksen
* Käyttäjä näkee etusivulla listan kirjoista
* Jos kirja ei ole kellään lainassa, käyttäjä voi lainata sen itselleen
* Käyttäjä näkee listan omista lainoista, ja voi palauttaa lainan
* Käyttäjä voi antaa arvion kirjalle, jonka on lainannut
* Käyttäjä voi lukea muiden lisäämiä arvioita
* Ylläpitäjä voi lisätä uusia kirjoja, ja poistaa hyllyssä olevia
* Käyttäjä voi etsiä kirjoja, joiden nimi sisältää annetun hakusanan
* Käyttäjä voi rajata kirjoja kirjailijan perusteella
* Käyttäjä voi toivoa uutta kirjaa lisättäväksi hyllyyn, ja äänestää muiden toiveita
* Käyttäjä voi tallentaa kirjan lukulistalleen
* Ylläpitäjä voi nähdä tilaston kirjojen lainausmääristä

## Sovelluksen käynnistysohjeet paikalliseen testaukseen:
* Kloonaa repositorio koneellesi ja siirry sen juurikansioon
* Lisää kansioon ```.env```-tiedosto ja sen sisällöksi:
  ```
  DATABASE_URL=postgres:///username
  SECRET_KEY=<salainen-avain>
  ```
* Aktivoi virtuaaliympäristö ja asenna riippuvuudet:
  ```
  python3 -m venv venv
  source venv/bin/activate
  pip install -r ./requirements.txt
  ```
* Määritä tietokanta:
  ```
  psql < schema.sql
  ```
* Käynnistä sovellus:
  ```
  flask run
  ```
Tietokannan määrittely lisää sovellukseen valmiiksi ylläpitäjä-käyttäjän, sillä itse sovelluksessa tunnuksen rekisteröinti luo automaattisesti asiakas-käyttäjän, jolla ei ole kaikkia ylläpitäjän toiminnallisuuksia. Sovelluksen toimintojen testausta varten ylläpitäjän käyttäjätunnus ja salasana löytyvät tiedostosta ```login.txt```.
