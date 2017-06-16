# -*- coding: utf-8 -*-

from app import app, db
import os
from oauth2client.client import OAuth2WebServerFlow, OAuth2Credentials # gsuite
import httplib2
from apiclient import discovery
from flask_oauthlib.client import OAuth # qbo

tablename_prefix = os.path.dirname(os.path.realpath(__file__)).split("/")[-1]

class Base(db.Model):
    __abstract__  = True
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

class AuthenticationTokens(Base):
    __tablename__ = "{0}_authentication_tokens".format(tablename_prefix)
    company_id = db.Column(db.BigInteger)
    oauth_token = db.Column(db.String(120))
    oauth_token_secret = db.Column(db.String(120))

def store_qbo_authentication_tokens(tokens, company_id):
    authorization_tokens = AuthenticationTokens.query.filter_by(company_id=company_id).first()
    if authorization_tokens is None:
        authorization_tokens = AuthenticationTokens(company_id=company_id)
    authorization_tokens.oauth_token = tokens['oauth_token']
    authorization_tokens.oauth_token_secret = tokens['oauth_token_secret']
    db.session.add(authorization_tokens)
    db.session.commit()

def update_chart_of_accounts(qbo, qbo_company_id, gsuite_credentials, sheet_id):
    skip_list = [u'Retained Earnings', u'Sales of Product Income', u'Services', u'Uncategorized Asset', u'Uncategorized Expense', u'Uncategorized Income', u'Undeposited Funds', u'Opening Balance Equity']

    # delete existing accounts, except un-delete-ables
    for account in qbo.get("https://quickbooks.api.intuit.com/v3/company/{0}/query?query=select%20%2A%20from%20account&minorversion=4".format(qbo_company_id), headers={'Accept': 'application/json'}).data['QueryResponse']['Account']:
        if account['FullyQualifiedName'] not in skip_list:
            account['Active'] = False
            response = qbo.post("https://quickbooks.api.intuit.com/v3/company/{0}/account?operation=update".format(qbo_company_id), format='json', headers={'Accept': 'application/json', 'Content-Type': 'application/json', 'User-Agent': 'wfbot'}, data=account)
            if response.status != 200:
                raise LookupError, "update {0} {1} {2}".format(response.status, response.data, account)

    # get chart of accounts from google sheet
    http_auth = gsuite_credentials.authorize(httplib2.Http())
    sheets = discovery.build('sheets', 'v4', http_auth)
    result = sheets.spreadsheets().values().get(spreadsheetId=sheet_id, range='A:Z').execute()
    rows = result.get('values', [])
    header = rows.pop(0)
    accounts = []
    for row in rows:
        a = {};
        for i, value in enumerate(row):
            a[header[i]] = value
        accounts.append(a)

    # important! create accounts closer to the root of the tree first, further away later, so the latter can reference the former
    accounts = sorted(accounts, key=lambda a: a['FullyQualifiedName'].count(':'))

    for i, account in enumerate(accounts):
        if account['FullyQualifiedName'] not in skip_list:
            fqn = account['FullyQualifiedName']
            if fqn.count(':') > 0:
                parent_fully_qualified_name, name = fqn.rsplit(":", 1)
                accounts[i]['Name'] = name
                parent_account = next(a for a in accounts if a["FullyQualifiedName"] == parent_fully_qualified_name)
                accounts[i]['ParentRef'] = {"value": parent_account["Id"]}
            else:
                accounts[i]['Name'] = fqn

            response = qbo.post("https://quickbooks.api.intuit.com/v3/company/{0}/account".format(qbo_company_id), format='json', headers={'Accept': 'application/json', 'Content-Type': 'application/json', 'User-Agent': 'wfbot'}, data=accounts[i])
            if response.status != 200:
                raise LookupError, "create {0} {1} {2}".format(response.status, response.data, account)
            accounts[i]['Id'] = response.data['Account']['Id']
