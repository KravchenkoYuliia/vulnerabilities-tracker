import requests
import psycopg2     # tool to talk with database
import os
from dotenv import load_dotenv
from pathlib import Path
import random

URL = 'https://services.nvd.nist.gov/rest/json/cves/2.0/?pubStartDate=2026-08-01T00:00:00.000&pubEndDate=2026-08-30T00:00:00.000&resultsPerPage=1000'

try:
    r = requests.get( URL, timeout=30 )
except requests.exceptions.RequestException as e:
    raise SystemExit( f"Error: can't connect to the site to initiate database\n{e}" )

env_file = Path( __file__ ).resolve().parent.parent / ".env"
if env_file.exists():
    load_dotenv( env_file  )
conn = psycopg2.connect( host=os.getenv( 'POSTGRES_HOST' ), dbname=os.getenv( 'POSTGRES_DB' ),
                        user=os.getenv( 'POSTGRES_USER' ), password=os.getenv( 'POSTGRES_PASSWORD' ) )
cur = conn.cursor()

cur.execute( 'SELECT count( * ) FROM vulnerabilities' )
if cur.fetchone()[0] > 0:
    raise SystemExit( 'Vulnerabilities table is not empty, skipping.' )

cur.execute( 'SELECT id FROM products' )
product_ids = [row[0] for row in cur.fetchall()]

for vuln in r.json()['vulnerabilities']:
    cve = vuln['cve']
    title = next( d['value'] for d in cve['descriptions'] if d['lang'] == 'en' )[:255]
    cvss, severity = None, 'NONE'
    for key in ( 'cvssMetricV40', 'cvssMetricV31', 'cvssMetricV30' ):
        if key in cve.get( 'metrics', {} ):
            data = cve['metrics'][key][0]['cvssData']
            cvss, severity = data['baseScore'], data['baseSeverity']
            break
    cur.execute( 
        '''INSERT INTO vulnerabilities ( cve_id, title, cvss, severity, status, product_id, fixed_in_version )
           VALUES ( %s, %s, %s, %s, 'NEW', %s, NULL ) ON CONFLICT ( cve_id ) DO NOTHING''',
        ( cve['id'], title, cvss, severity, random.choice( product_ids ) ) )

conn.commit()
print( 'Inserted CVEs from NVD' )