from bs4 import BeautifulSoup
import bs4
import lxml
import feedparser
from textblob_de import TextBlobDE as TextBlob
from pandas.core.common import flatten
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date
from datetime import datetime
import statistics
import openpyxl
from openpyxl import load_workbook
from flashtext import KeywordProcessor
import asyncio
import httpx
import time
import itertools
import cchardet
import gevent
import os
from bs4 import SoupStrainer
import psycopg2
import os
import urllib.parse as urlparse

url = urlparse.urlparse(os.environ['DATABASE_URL'])
dbname = url.path[1:]
user = url.username

password = url.password
host = url.hostname
port = url.port

con = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
            )
dbCursor = con.cursor()
print(dbname)

sqlCreateTable  = 'CREATE TABLE IF NOT EXISTS crawldata(date varchar(128), sentimentcdu numeric, sentimentgruene numeric, sentimentspd numeric, sentimentfdp numeric, sentimentafd numeric);'
#sqlCreateTable  = 'CREATE TABLE crawldata(date,sentimentcdu,sentimentgruene,sentimentspd,sentimentfdp,sentimentafd);'
dbCursor.execute(sqlCreateTable);
print('test')

#server = app.server
# ran = 0
# import time
# # data = pd.read_excel('Sentiments.xlsx')
#
#
# data['Tag'] = pd.to_datetime(data['Tag'], format='%d/%m/%Y %H:%M:%S')
#
# data.sort_values('Tag', inplace=True)
# starttime = time.time()



rss_urls=['https://www.spiegel.de/politik/index.rss','https://www.tagesschau.de/xml/rss2/','https://www.n-tv.de/politik/rss','https://rss.sueddeutsche.de/rss/Politik']
content_cdu = []
content_gruene= []
content_fdp = []
content_spd = []
content_afd = []
content= []
content_clean=[]
links = []
tagesschau_links= []
ntv_links = []
sueddeutsche_links = []
# HTTP GET requests
h = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko)     Chrome/23.0.1271.64 Safari/537.11'}


whitelist = [
    'p'
]
async def get_content(index: int, url: str) -> str:
    async with httpx.AsyncClient(timeout=None) as client:
        try:
            response = await client.get(url)
            #print(url)
        except:
            print(f'Error response {exc.response.status_code} while requesting {exc.request.url!r}.')
        #soup = bs4.BeautifulSoup(response.text, 'lxml', parse_only = SoupStrainer('p'))
        content.append([t for t in bs4.BeautifulSoup(response.text, 'lxml',parse_only = SoupStrainer('p')).find_all(text=True) if t.parent.name in whitelist])
        #del soup

async def main():
    print('##############run#######################')

    keyword_fdp = [
    'Grigorios Aggelidis',
    'Renata Alt',
    'Christine Aschenberg-Dugnus',
    'Nicole Bauer',
    'Jens Beeck',
    'Jens Brandenburg',
    'Mario Brandenburg',
    'Sandra Bubendorfer-Licht',
    'Marco Buschmann',
    'Karlheinz Busen',
    'Carl-Julius Cronenberg',
    'Britta Katharina Dassler',
    'Bijan Djir-Sarai',
    'Christian Dürr',
    'Hartmut Ebbing',
    'Marcus Faber',
    'Daniel Föst',
    'Otto Fricke',
    'Christopher Gohl',
    'Alexander Graf Lambsdorff',
    'Thomas Hacker',
    'Reginald Hanke',
    'Peter Heidt',
    'Katrin Helling-Plahr',
    'Markus Herbrand',
    'Torsten Herbst',
    'Katja Hessel',
    'Gero Hocker',
    'Manuel Höferlin',
    'Christoph Hoffmann',
    'Reinhard Houben',
    'Ulla Ihnen',
    'Olaf in der Beek',
    'Gyde Jensen',
    'Karsten Klein',
    'Marcel Klinge',
    'Daniela Kluckert',
    'Pascal Kober',
    'Lukas Köhler',
    'Carina Konrad',
    'Wolfgang Kubicki',
    'Konstantin Kuhle',
    'Alexander Kulitz',
    'Ulrich Lechte',
    'Christian Lindner',
    'Michael Link',
    'Oliver Luksic',
    'Till Mansmann',
    'Jürgen Martens',
    'Christoph Meyer',
    'Alexander Müller',
    'Roman Müller-Böhm',
    'Frank Müller-Rosentritt',
    'Martin Neumann',
    'Matthias Nölke',
    'Hagen Reinhold',
    'Bernd Reuther',
    'Thomas Sattelberger',
    'Christian Sauter',
    'Frank Schäffler',
    'Wieland Schinnenburg',
    'Matthias Seestern-Pauly',
    'Frank Sitta',
    'Judith Skudelny',
    'Hermann Otto Solms',
    'Bettina Stark-Watzinger',
    'Marie-Agnes Strack-Zimmermann',
    'Benjamin Strasser',
    'Katja Suding',
    'Linda Teuteberg',
    'Michael Theurer',
    'Stephan Thomae',
    'Manfred Todtenhausen',
    'Florian Toncar',
    'Andrew Ullmann',
    'Gerald Ullrich',
    'Johannes Vogel',
    'Sandra Weeser',
    'Nicole Westig',
    'Katharina Willkomm',
    'Volker Wissing',
    'FDP',
    'Freie Demokratische Partei',
    'FDP-'
    ]

    keyword_cdu = [
        'CDU',
        'CSU',
        'CDU/CSU',
        '(CDU)',
        '(CSU)',
        'Union',
        'Christlich Demokratische Union',
        'Michael von Abercron',
        'Stephan Albani',
        'Norbert Altenkamp',
        'Peter Altmaier',
        'Philipp Amthor',
        'Peter Aumer',
        'Artur Auernhammer',
        'Dorothee Bär',
        'Thomas Bareiß',
        'Norbert Barthle',
        'Maik Beermann',
        'Manfred Behrens',
        'André Berghegger',
        'Veronika Bellmann',
        'Sybille Benning',
        'Melanie Bernstein',
        'Marc Biadacz',
        'Christoph Bernstiel',
        'Peter Beyer',
        'Steffen Bilger',
        'Michael Brand',
        'Peter Bleser',
        'Norbert Brackmann',
        'Silvia Breher',
        'Sebastian Brehm',
        'Reinhard Brandl',
        'Helge Braun',
        'Heike Brehmer',
        'Carsten Brodesser',
        'Ralph Brinkhaus',
        'Gitta Connemann',
        'Astrid Damerow',
        'Alexander Dobrindt',
        'Michael Donth',
        'Marie-Luise Dött',
        'Hansjörg Durz',
        'Thomas Erndl',
        'Bernd Fabritius',
        'Hermann Färber',
        'Uwe Feiler',
        'Enak Ferlemann',
        'Maria Flachsbarth',
        'Hans-Peter Friedrich',
        'Thorsten Frei',
        'Maika Friemnann-Jennert',
        'Michael Frieser',
        'Hans-Joachim Fuchtel',
        'Ingo Gädchens',
        'Thomas Gebhart',
        'Alois Gerig',
        'Eberhard Gienger',
        'Eckhard Gnodkte',
        'Hermann Gröhe',
        'Ursula Groden-Kranich',
        'Klaus-Dieter Gröhler',
        'Michael Grosse-Brömer',
        'Manfred Grund',
        'Astrid Grotelüschen',
        'Markus Grübel',
        'Oliver Grundmann',
        'Olav Gutting',
        'Monika Grütters',
        'Fritz Güntzler',
        'Christian Haase',
        'Florian Hahn',
        'Jürgen Hardt',
        'Matthias Hauer',
        'Matthias Heider',
        'Frank Heinrich',
        'Mechtild Heil',
        'Thomas Heilmann',
        'Mark Helfrich',
        'Marc Henrichmann',
        'Rudolf Henke',
        'Michael Hennrich',
        'Ansgar Heveling',
        'Alexander Hoffmann',
        'Christian Hirte',
        'Heribert Hirte',
        'Hendrik Hoppenstedt',
        'Karl Holmeier',
        'Erich Irlstorfer',
        'Hans-Jürgen Irmer',
        'Thomas Jarzombek',
        'Andreas Jung',
        'Ingmar Jung',
        'Alois Karl',
        'Anja Karliczek',
        'Torbjörn Kartes',
        'Volker Kauder',
        'Dr. Stefan Kaufmann',
        'Michael Kießling',
        'Ronja Kemmer',
        'Roderich Kiesewetter',
        'Georg Kippels',
        'Jens Koeppen',
        'Volkmar Klein',
        'Axel Knoerig',
        'Markus Koob',
        'Alexander Krauß',
        'Carsten Köber',
        'Kordula Kovac',
        'Gunter Krichbaum',
        'Michael Kuffer',
        'Günter Krings',
        'Rüdiger Kruse',
        'Roy Kühne',
        'Karl A. Lamers',
        'Andreas G. Lämmel',
        'Katharina Landgraf',
        'Ulrich Lange',
        'Silke Launert',
        'Paul Lehrieder',
        'Jens Lehmann',
        'Katja Leikert',
        'Andreas Lenz',
        'Andrea Lindholz',
        'Antje Lezius',
        'Carsten Linnemann',
        'Bernhard Loos',
        'Jan-Marco Luczak',
        'Saskia Ludwig',
        'Daniela Ludwig',
        'Yvonne Magwas',
        'Thomas de Maizière',
        'Gisela Manderla',
        'Astrid Mannes',
        'Hans-Georg von der Marwitz',
        'Andreas Mattfeldt',
        'Matern von Marschall',
        'Stephan Mayer',
        'Angela Merkel',
        'Jan Metzler',
        'Michael Meister',
        'Hans Michelbach',
        'Dietrich Monstadt',
        'Matthias Middleberg',
        'Karsten Möring',
        'Elisabeth Motschmann',
        'Axel Müller',
        'Carsten Müller',
        'Sepp Müller',
        'Stefan Müller',
        'Christian Natterer',
        'Andreas Nick',
        'Petra Nicolaisen',
        'Michaela Noll',
        'Kristina Nordt',
        'Wilfried Oellers',
        'Florian Oßner',
        'Josef Oster',
        'Tim Ostermann',
        'Henning Otte',
        'Ingrid Pahlmann',
        'Sylvia Pantel',
        'Martin Patzelt',
        'Joachim Pfeiffer',
        'Stephan Pilsinger',
        'Eckhard Pols',
        'Christoph Ploß',
        'Thomas Rachel',
        'Kerstin Radomski',
        'Alexander Radwan',
        'Alois Rainer',
        'Eckhardt Rehberg',
        'Lothar Riebsamen',
        'Peter Ramsauer',
        'Josef Rief',
        'Erwin Rüddel',
        'Norbert Röttgen',
        'Johannes Röring',
        'Stefan Rouenhoff',
        'Albert Rupprecht',
        'Stefan Sauer',
        'Anita Schäfer',
        'Wolfgang Schäuble',
        'Andreas Scheuer',
        'Jana Schmike',
        'Christian Schmidt',
        'Tankred Schipanski',
        'Claudia Schmidtke',
        'Patrick Schnieder',
        'Felix Schreiner',
        'Nadine Schön',
        'Klaus-Peter Schulze',
        'Uwe Schummer',
        'Torsten Schweiger',
        'Johannes Selle',
        'Detlef Seif',
        'Reinhold Sendker',
        'Patrick Sensburg',
        'Thomas Silberhorn',
        'Bernd Siebert',
        'Björn Simon',
        'Jens Spahn',
        'Katrin Staffler',
        'Tino Sorge',
        'Frank Steffel',
        'Andreas Steier',
        'Albert Stegemann',
        'Wolfgang Stefinger',
        'Peter Stein',
        'Johannes Steiniger',
        'Christian Frhr. von Stetten',
        'Sebastian Steineke',
        'Dieter Stier',
        'Stephan Stracke',
        'Max Straubinger',
        'Gero Storjohann',
        'Hermann-Josef Tebroke',
        'Hans-Jürgen Thies',
        'Alexander Throm',
        'Dietlind Tiemann',
        'Antje Tillmann',
        'Markus Uhl',
        'Volker Ullreich',
        'Arnold Vaatz',
        'Kerstin Vieregge',
        'Thomas Viesehon',
        'Volkmar Vogel',
        'Kees de Vries',
        'Johann David Wadephul',
        'Marco Wanderwitz',
        'Nina Warken',
        'Kai Wegner',
        'Marcus Weinberg',
        'Anja Weisberger',
        'Albert H. Weiler',
        'Peter Weiß',
        'Ingo Wellenreuther',
        'Kai Whittaker',
        'Sabine Weiss',
        'Marian Wendt',
        'Bettina Margarethe Wiesmann',
        'Elisabeth Winkelmeier-Becker',
        'Anette Widmann-Mauz',
        'Klaus-Peter Willsch',
        'Christoph de Vries',
        'Emmi Zeulner',
        'Paul Ziemiak',
        'Matthias Zimmer',
        'Armin Laschet',
        'Laschet',
        'Markus Söder',
        'Annegret Kramp-Karrenbauer',
        'Ursula von der Leyen',
        'Horst Seehofer'
        'CDU-'
        'CSU-'
        'CDU/CSU-'
        ]

    keyword_gruene = ['Luise Amtsberg',
        'Lisa Badum','Annalena Baerbock','Margarete Bause','Canan Bayram','Franziska Brantner','Agnieszka Brugger',
        'Anna Christmann','Janosch Dahmen','Ekin Deligöz','Katharina Dröge','Harald Ebner','Marcel Emmerich','Matthias Gastel','Kai Gehring','Stefan Gelbhaar'
        'Katrin Göring-Eckardt','Erhard Grundl','Anja Hajduk','Britta Haßelmann','Bettina Hoffmann','Anton Hofreiter','Ottmar von Holtz'
        'Dieter Janecek','Kirsten Kappert-Gonther','Uwe Kekeritz','Katja Keul','Sven-Christian Kindler','Maria Klein-Schmeink','Sylvia Kotting-Uhl'
        'Oliver Krischer','Christian Kühn','Renate Künast','Markus Kurth','Monika Lazar','Sven Lehmann','Steffi Lemke','Tobias Lindner'
        'Irene Mihalic','Claudia Müller','Beate Müller-Gemmeke','Ingrid Nestle','Konstantin von Notz','Omid Nouripour','Friedrich Ostendorff'
        'Cem Özdemir','Lisa Paus','Filiz Polat','Tabea Rößner','Claudia Roth','Manuela Rottmann','Corinna Rüffer','Manuel Sarrazin','Ulle Schauws','Frithjof Schmidt'
        'Stefan Schmidt','Charlotte Schneidewind-Hartnagel','Kordula Schulz-Asche','Wolfgang Strengmann-Kuhn','Margit Stumpp','Markus Tressel','Jürgen Trittin'
        'Julia Verlinden','Daniela Wagner','Beate Walter-Rosenheimer','Wolfgang Wetzel','Gerhard Zickenheiner','Die Grünen','Grünen','Grünen-']


    keyword_spd = ['Niels Annen', 'Ingrid Arndt-Bauer', 'Bela Bach', 'Heike Baehrens', 'Ulrike Bahr', 'Nezahat Baradari','Katarina Barley','Doris Barnett','Matthias Bartke',
    'Sören Bartol','Bärbel Bas','Lothar Binding','Eberhard Brecht','Leni Breymaier','Karl-Heinz Brunner','Katrin Budde','Marco Bülow','Martin Burkert','Lars Castellucci',
    'Bernhard Daldrup','Daniela De Ridder','Karamba Diaby','Esther Dilcher','Sabine Dittmar','Wiebke Esdar','Saskia Esken','Yasmin Fahimi','Johannes Fechner',
    'Fritz Felgentreu','Edgar Franke','Ulrich Freese','Dagmar Freitag','Sigmar Gabriel','Michael Gerdes','Martin Gerster','Angelika Glöckner','Timon Gremmels',
    'Kerstin Griese','Michael Groß','Uli Grötsch','Bettina Hagedorn','Rita Hagl-Kehl','Metin Hakverdi','Sebastian Hartmann','Dirk Heidenblut',
    'Hubertus Heil','Gabriela Heinrich','Marcus Held','Wolfgang Hellmich','Barbara Hendricks','Gustav Herzog','Gabriele Hiller-Ohm','Thomas Hitschler',
    'Eva Högl','Frank Junge','Josip Juratovic','Thomas Jurk','Oliver Kaczmarek','Johannes Kahrs','Elisabeth Kaiser','Ralf Kapschack','Gabriele Katzmarek',
    'Ulrich Kelber','Cansel Kiziltepe','Arno Klare','Lars Klingbeil','Bärbel Kofler','Daniela Kolbe','Elvan Korkmaz-Emre','Anette Kramme',
    'Christine Lambrecht','Christian Lange','Karl Lauterbach','Sylvia Lehmann','Helge Lindh','Burkhard Lischka','Hiltrud Lotze','Kirsten Lühmann',
    'Heiko Maas','Isabel Mackensen-Geis','Caren Marks','Dorothee Martin','Katja Mast','Christoph Matschie','Hilde Mattheis','Matthias Miersch',
    'Klaus Mindrup','Susanne Mittag','Falko Mohrs','Claudia Moll','Siemtje Möller','Bettina Müller','Detlef Müller','Michelle Müntefering',
    'Rolf Mützenich','Andrea Nahles','Dietmar Nietan','Ulli Nissen','Thomas Oppermann','Josephine Ortleb','Mahmut Özdemir','Aydan Özoğuz',
    'Markus Paschke','Christian Petry','Detlev Pilger','Sabine Poschmann','Florian Post','Achim Post','Florian Pronold','Sascha Raabe',
    'Martin Rabanus','Mechthild Rawert','Carola Reimann','Andreas Rimkus','Sönke Rix','Dennis Rohde','Martin Rosemann','René Röspel',
    'Ernst Dieter Rossmann','Michael Roth','Susann Rüthrich','Bernd Rützel','Sarah Ryglewski','Johann Saathoff','Axel Schäfer',
    'Nina Scheer','Marianne Schieder','Udo Schiefner','Nils Schmid','Uwe Schmidt','Ulla Schmidt','Dagmar Schmidt','Carsten Schneider',
    'Johannes Schraps','Michael Schrodi','Manja Schüle','Ursula Schulte','Martin Schulz','Swen Schulz','Ewald Schurer','Frank Schwabe',
    'Stefan Schwartze','Andreas Schwarz','Rita Schwarzelühr-Sutter','Rainer Spiering','Svenja Stadler','Martina Stamm-Fibich',
    'Sonja Amalie Steffen','Mathias Stein','Kerstin Tack','Claudia Tausend','Michael Thews','Markus Töns','Carsten Träger','Ute Vogt',
    'Marja-Liisa Völlers','Dirk Vöpel','Gabi Weber','Joe Weingarten','Bernd Westphal','Dirk Wiese','Gülistan Yüksel','Dagmar Ziegler',
    'Stefan Zierke','Jens Zimmermann','SPD','sozialdemokraten','Sozialdemokratische Partei Deutschlands'
    ]

    keyword_afd = ['Dr. Bernd Baumann','Marc Bernhard','Andreas Bleck','Peter Boehringer','Stephan Brandner','Jürgen Braun','Marcus Bühl','Matthias Büttner','Petr Bystron','Tino Chrupalla','Joana Cotar','Gottfried Curio','Siegbert F. Droese','Thomas Ehrhorn','Berengar Elsner von Gronow','Dr. Michael Espendiller','Peter Felser','Dietmar Friedhoff','Dr. Anton Friesen','Markus Frohnmaier','Dr. Götz Frömming','Dr. Alexander Gauland','Prof. Dr. med. Axel Gehrke','Albrecht Glaser','Franziska Gminder','Wilhelm von Gottberg','Kay Gottschalk','Amin-Paulus Hampel','Mariana Harder-Kühnel','Dr. Roland Hartwig','Jochen Haug','Martin Hebner','Udo Hemmelgarn','Waldemar Herdt','Martin Hess','Heiko Hessenkemper','Karsten Hilse','Nicole Höchst','Martin Hohmann','Bruno Hollnagel','Leif-Erik Holm','Johannes Huber','Fabian Jacobi','Marc Jongen','Jens Kestner','Stefan Keuter','Norbert Kleinwächter','Enrico Komning','Jörn König','Steffen Kotré','Rainer Kraft','Rüdiger Lucassen','Frank Magnitz','Lothar Maier','Jens Maier','Birgit Malsack-Winkemann','Corinna Miazga','Andreas Mrosek','Hansjörg Müller','Volker Münz','Sebastian Münzenmaier','Christoph Neumann','Jan Nolte','Ulrich Oehme','Gerold Otten','Tobias Matthias Peterka','Paul Viktor Podolay','Jürgen Pohl','Stephan Protschka','Martin Reichardt','Martin E. Renner','Roman Reusch','Ulrike Schielke-Ziesing','Robby Schlund','Jörg Schneider','Uwe Schulz','Thomas Seitz','Martin Sichert','Detlev Spangenberg','Dirk Spaniel','René Springer','Beatrix von Storch','Alice Weidel','Harald Weyel','Wolfgang Wiehle','Heiko Wildberg','Christian Wirth','Uwe Witt','AFD','afd','AfD','Alternative für Deutschland']

    keyword_dict = {
                'CDU': keyword_cdu,
                'Gruene': keyword_gruene,
                'FDP': keyword_fdp,
                'SPD': keyword_spd,
                'AFD': keyword_afd,



    }



    sentiment_cdu = []
    sentiment_gruene = []
    sentiment_fdp = []
    sentiment_spd = []
    sentiment_afd = []
    keyword_processor = KeywordProcessor()
    keyword_processor.add_keywords_from_dict(keyword_dict)
    del keyword_dict
    del keyword_cdu
    del keyword_spd
    del keyword_afd
    del keyword_gruene
    feeds = []
    for url in rss_urls:
        feeds.extend(feedparser.parse(url).entries)
        #print(feeds)
    for i in feeds:
        links.append(i.link)
        #print(links)
    del feeds

    task_list = []
    for index, link in enumerate(links):
        task_list.append(get_content(index, link))
    await asyncio.gather(*task_list)
    print('DEBUG')
    del task_list
    for i in itertools.chain.from_iterable(content):
        keywords_found= keyword_processor.extract_keywords(str(i))
        #print(keywords_found)
        if keywords_found.count('Gruene') >= 1:
            content_gruene.append(i)
        if keywords_found.count('CDU') >= 1:
            content_cdu.append(i)
        if keywords_found.count('FDP') >= 1:
            content_fdp.append(i)
        if keywords_found.count('SPD') >= 1:
            content_spd.append(i)
        if keywords_found.count('AFD') >= 1:
            content_afd.append(i)




    for cdu,gruene,fdp,spd,afd in zip(content_cdu, content_gruene, content_fdp, content_spd, content_afd ):
        blob= TextBlob(str(cdu))
        sentiment_cdu.append(blob.sentiment.polarity)
        blob = TextBlob(str(gruene))
        sentiment_gruene.append(blob.sentiment.polarity)
        blob = TextBlob(str(fdp))
        sentiment_fdp.append(blob.sentiment.polarity)
        blob = TextBlob(str(spd))
        sentiment_spd.append(blob.sentiment.polarity)
        blob = TextBlob(str(afd))
        sentiment_afd.append(blob.sentiment.polarity)
        #print(sentiment_cdu)

    if not sentiment_cdu:
        sentiment_cdu.append(0)
    if not sentiment_gruene:
        sentiment_gruene.append(0)
    if not sentiment_fdp:
        sentiment_fdp.append(0)
    if not sentiment_fdp:
        sentiment_spd.append(0)
    if not sentiment_afd:
        sentiment_afd.append(0)

    #today = date.today()
    now = datetime.now()
    today = str(now.strftime('%d/%m/%Y %H:%M:%S'))
    #sqlinsert = 'INSERT INTO crawldata (date,sentimentcdu,sentimentgruene,sentimentspd,sentimentfdp,sentimentafd) VALUES ();'
    #sqlinsert = 'INSERT INTO crawldata VALUES ();'
    meancdu = statistics.mean(sentiment_cdu)
    meangruene = statistics.mean(sentiment_gruene)
    meanfdp = statistics.mean(sentiment_fdp)
    meanspd = statistics.mean(sentiment_spd)
    meanafd = statistics.mean(sentiment_afd)
    mean = (today,meancdu,meangruene,meanfdp,meanspd,meanafd)


    add_data =  ("INSERT INTO crawldata "
               "(date,sentimentcdu,sentimentgruene,sentimentspd,sentimentfdp,sentimentafd) "
               "VALUES (%s, %s, %s, %s, %s, %s)")
    #dbCursor.execute("""INSERT INTO crawldata (today,meancdu,meangruene,meanfdp,meanspd,meanafd) VALUES (%s, %s, %s, %s, %s, %s);""")
    dbCursor.execute(add_data, mean)
    con.commit()
    #dbCursor.execute(sqlinsert);
    # postgreSQL_select_Query = "select * from crawldata"
    #
    # dbCursor.execute(postgreSQL_select_Query)
    # print("Selecting rows from mobile table using cursor.fetchall")
    # mobile_records = dbCursor.fetchall()
    #
    # print("Print each row and it's columns values")
    # for row in mobile_records:
    #     print(row)


    # ws.append([today,statistics.mean(sentiment_cdu),statistics.mean(sentiment_gruene),statistics.mean(sentiment_fdp),statistics.mean(sentiment_spd),statistics.mean(sentiment_afd)])
    # wb.save('Sentiments.xlsx')


if __name__ == '__main__':
    asyncio.run(main(),debug=False)

print('done')




#if __name__ == '__main__':
