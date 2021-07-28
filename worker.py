from bs4 import BeautifulSoup
import bs4
import lxml
import feedparser
# from textblob_de import TextBlobDE as TextBlob
from pandas.core.common import flatten
import pandas as pd
from datetime import date
from datetime import datetime
import statistics
# import openpyxl
# from openpyxl import load_workbook
from flashtext import KeywordProcessor
import asyncio
import httpx
#import time
#import itertools
# import cchardet
# import gevent
import os
from bs4 import SoupStrainer
import psycopg2
import os
import urllib.parse as urlparse
import spacy
from spacy_sentiws import spaCySentiWS
import numpy as np


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
#print(dbname)

sqlCreateTable  = 'CREATE TABLE IF NOT EXISTS crawldata(date varchar(128), sentimentcdu numeric, sentimentgruene numeric, sentimentspd numeric, sentimentfdp numeric, sentimentafd numeric, linkscdu text,linksgruene text,linksspd text,linksfdp text,linksafd text);'
# sqlAddColumns = 'ALTER TABLE crawldata ADD COLUMN IF NOT EXISTS linkscdu varchar(2048),ADD COLUMN IF NOT EXISTS linksgruene varchar(2048),ADD COLUMN IF NOT EXISTS linksspd varchar(2048),ADD COLUMN IF NOT EXISTS linksfdp varchar(2048),ADD COLUMN IF NOT EXISTS linksafd varchar(2048)'
# sqlaltercolumns= 'ALTER TABLE crawldata ALTER COLUMN linkscdu TYPE varchar(2048),ALTER COLUMN linksgruene TYPE varchar(2048),ALTER COLUMN linksspd TYPE varchar(2048),ALTER COLUMN linksfdp TYPE varchar(2048),ALTER COLUMN linksafd TYPE varchar(2048)'
#sqlCreateTable  = 'CREATE TABLE crawldata(date,sentimentcdu,sentimentgruene,sentimentspd,sentimentfdp,sentimentafd);'
dbCursor.execute(sqlCreateTable);
# dbCursor.execute(sqlAddColumns);
# dbCursor.execute(sqlaltercolumns);




rss_urls=['https://www.spiegel.de/politik/index.rss','https://www.tagesschau.de/xml/rss2/','https://www.n-tv.de/politik/rss','https://rss.sueddeutsche.de/rss/Politik','https://www.faz.net/rss/aktuell/politik/']
content_cdu = []
content_gruene= []
content_fdp = []
content_spd = []
content_afd = []
links_cdu=[]
links_gruene=[]
links_fdp=[]
links_spd=[]
links_afd=[]
weight_cdu=[]
weight_gruene=[]
weight_fdp=[]
weight_spd=[]
weight_afd=[]
content= []

links = []
linklist=[]
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
    # 'article__text',
    # 'article-body',
    # 'content'
]
async def get_content(index: int, url: str) -> str:
    async with httpx.AsyncClient(timeout=None) as client:
        try:
            if ".faz.net" in url:
                url+="?printPagedArticle=true"
                response = await client.get(url)
                #print(url)
            else:
                response = await client.get(url)
            #print(url)
        except:
            print(f'Error response while requesting.')
            response ="0"
        #soup = bs4.BeautifulSoup(response.text, 'lxml', parse_only = SoupStrainer('p'))
        content.append((url,[t for t in bs4.BeautifulSoup(response.text, 'lxml',parse_only = SoupStrainer('p')).find_all(text=True) if t.parent.name in whitelist]))

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
    'FDP-',
    '(FDP)',
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
        'Horst Seehofer',
        'CDU-',
        'CSU-',
        'CDU/CSU-',
        'Unionskanzlerkandidat',
        '(CDU)',
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
        'Julia Verlinden','Daniela Wagner','Beate Walter-Rosenheimer','Wolfgang Wetzel','Gerhard Zickenheiner','Die Grünen','Grünen','Grünen-','(Die Grünen)']


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
    'Stefan Zierke','Jens Zimmermann','SPD','sozialdemokraten','(SPD)','Sozialdemokratische Partei Deutschlands'
    ]

    keyword_afd = ['Dr. Bernd Baumann','Marc Bernhard','Andreas Bleck','Peter Boehringer','Stephan Brandner','Jürgen Braun','Marcus Bühl','Matthias Büttner','Petr Bystron','Tino Chrupalla','Joana Cotar','Gottfried Curio','Siegbert F. Droese','Thomas Ehrhorn','Berengar Elsner von Gronow','Dr. Michael Espendiller','Peter Felser','Dietmar Friedhoff','Dr. Anton Friesen','Markus Frohnmaier','Dr. Götz Frömming','Dr. Alexander Gauland','Prof. Dr. med. Axel Gehrke','Albrecht Glaser','Franziska Gminder','Wilhelm von Gottberg','Kay Gottschalk','Amin-Paulus Hampel','Mariana Harder-Kühnel','Dr. Roland Hartwig','Jochen Haug','Martin Hebner','Udo Hemmelgarn','Waldemar Herdt','Martin Hess','Heiko Hessenkemper','Karsten Hilse','Nicole Höchst','Martin Hohmann','Bruno Hollnagel','Leif-Erik Holm','Johannes Huber','Fabian Jacobi','Marc Jongen','Jens Kestner','Stefan Keuter','Norbert Kleinwächter','Enrico Komning','Jörn König','Steffen Kotré','Rainer Kraft','Rüdiger Lucassen','Frank Magnitz','Lothar Maier','Jens Maier','Birgit Malsack-Winkemann','Corinna Miazga','Andreas Mrosek','Hansjörg Müller','Volker Münz','Sebastian Münzenmaier','Christoph Neumann','Jan Nolte','Ulrich Oehme','Gerold Otten','Tobias Matthias Peterka','Paul Viktor Podolay','Jürgen Pohl','Stephan Protschka','Martin Reichardt','Martin E. Renner','Roman Reusch','Ulrike Schielke-Ziesing','Robby Schlund','Jörg Schneider','Uwe Schulz','Thomas Seitz','Martin Sichert','Detlev Spangenberg','Dirk Spaniel','René Springer','Beatrix von Storch','Alice Weidel','Harald Weyel','Wolfgang Wiehle','Heiko Wildberg','Christian Wirth','Uwe Witt','AFD','afd','AfD','(AFD)','Alternative für Deutschland']

    # keyword_cdu2 = [i.split(' ', 1)[1] for i in keyword_cdu if ' ' in i & ""]
    # keyword_gruene2 = [i.split(' ', 1)[1] for i in keyword_gruene if ' ' in i]
    # keyword_fdp2 = [i.split(' ', 1)[1] for i in keyword_fdp if ' ' in i]
    # keyword_spd2 = [i.split(' ', 1)[1] for i in keyword_spd[:-1] if ' ' in i]
    # keyword_afd2 = [i.split(' ', 1)[1] for i in keyword_afd[:-1] if ' ' in i]
    #
    # keyword_cdu = keyword_cdu + keyword_cdu2
    # keyword_gruene = keyword_gruene + keyword_gruene2
    # keyword_fdp = keyword_fdp + keyword_fdp2
    # keyword_spd = keyword_spd + keyword_spd2
    # keyword_afd = keyword_afd + keyword_afd2

    keyword_dict = {
                'CDU': keyword_cdu,
                'Gruene':keyword_gruene,
                'FDP': keyword_fdp,
                'SPD': keyword_spd,
                'AFD': keyword_afd,
    }


    nlp = spacy.load("de_core_news_md")
    sentiws = spaCySentiWS(sentiws_path='data/sentiws/')
    nlp.add_pipe(sentiws)
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
    # del keyword_cdu2
    # del keyword_spd2
    # del keyword_afd2
    # del keyword_gruene2
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

    del task_list
    # for idx, i in enumerate(itertools.chain.from_iterable(content)):
    for idx in range(len(content)):
        #print(content[idx][0])
        keywords_found= keyword_processor.extract_keywords(str(content[idx][1]))
        count_gruene = keywords_found.count('Gruene')
        count_cdu = keywords_found.count('CDU')
        count_fdp = keywords_found.count('FDP')
        count_spd = keywords_found.count('SPD')
        count_afd = keywords_found.count('AFD')

        if count_gruene >= 1:
            content_gruene.append((content[idx][0],count_gruene,content[idx][1]))
        if count_cdu >= 1:
            content_cdu.append((content[idx][0],count_cdu,content[idx][1]))
        if count_fdp >= 1:
            content_fdp.append((content[idx][0],count_fdp,content[idx][1]))
        if count_spd >= 1:
            content_spd.append((content[idx][0],count_spd,content[idx][1]))
        if count_afd >= 1:
            content_afd.append((content[idx][0],count_afd,content[idx][1]))





    for cdu,gruene,fdp,spd,afd in zip(content_cdu, content_gruene, content_fdp, content_spd, content_afd ):
        blob= nlp(str(cdu[2:]))
        for token in blob:
            #print(token)
            if token._.sentiws is not None:
                sentiment_cdu.append(token._.sentiws)
                weight_cdu.append(cdu[1])
        if str(cdu[0]) not in links_cdu:
                links_cdu.append(str(cdu[0]))

        blob = nlp(str(gruene[2:]))
        for token in blob:
            if token._.sentiws is not None:
                sentiment_gruene.append(token._.sentiws)
                weight_gruene.append(gruene[1])
        if str(gruene[0]) not in links_gruene:
            links_gruene.append(str(gruene[0]))
        blob = nlp(str(fdp[2:]))
        for token in blob:
            if token._.sentiws is not None:
                sentiment_fdp.append(token._.sentiws)
                weight_fdp.append(fdp[1])
        if str(fdp[0]) not in links_fdp:
            links_fdp.append(str(fdp[0]))

        blob = nlp(str(spd[2:]))
        for token in blob:
            if token._.sentiws is not None:
                sentiment_spd.append(token._.sentiws)
                weight_spd.append(spd[1])
        if str(spd[0]) not in links_spd:
            links_spd.append(str(spd[0]))
        blob = nlp(str(afd[2:]))
        for token in blob:
            if token._.sentiws is not None:
                sentiment_afd.append(token._.sentiws)
                weight_afd.append(afd[1])
        if str(afd[0]) not in links_afd:
            links_afd.append(str(afd[0]))

        #print(sentiment_cdu)



    if sentiment_cdu:
        #meancdu = statistics.mean(sentiment_cdu)
        print(type(sentiment_cdu))
        print(type(weight_cdu))
        meancdu = np.average(sentiment_cdu, weights=weight_cdu)
    if sentiment_gruene:
        #meangruene = statistics.mean(sentiment_gruene)
        meangruene = np.average(sentiment_gruene, weights=weight_gruene)
    if sentiment_fdp:
        #meanfdp = statistics.mean(sentiment_fdp)
        meanfdp = np.average(sentiment_fdp, weights=weight_fdp)
    if sentiment_spd:
        #meanspd = statistics.mean(sentiment_spd)
        meanspd = np.average(sentiment_spd, weights=weight_spd)
    if sentiment_afd:
        #meanafd = statistics.mean(sentiment_afd)
        meanafd = np.average(sentiment_afd, weights=weight_afd)

    #today = date.today()
    now = datetime.now()
    today = str(now.strftime('%d/%m/%Y %H:%M:%S'))
    #sqlinsert = 'INSERT INTO crawldata (date,sentimentcdu,sentimentgruene,sentimentspd,sentimentfdp,sentimentafd) VALUES ();'
    #sqlinsert = 'INSERT INTO crawldata VALUES ();'




    mean = (today,meancdu,meangruene,meanfdp,meanspd,meanafd,links_cdu,links_gruene,links_spd,links_fdp,links_afd)


    add_data =  ("INSERT INTO crawldata "
               "(date,sentimentcdu,sentimentgruene,sentimentspd,sentimentfdp,sentimentafd,linkscdu,linksgruene,linksspd,linksfdp,linksafd) "
               "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")

    dbCursor.execute(add_data, mean)
    con.commit()




if __name__ == '__main__':
    asyncio.run(main(),debug=False)

print('done')




#if __name__ == '__main__':
