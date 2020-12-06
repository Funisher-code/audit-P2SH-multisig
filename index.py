#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request
from auditP2SH import *

DEVELOPMENT_ENV  = True

app = Flask(__name__)

# Default form data showing in the intergace
app_trxdata = {
	"txid":       	"72b85d8a66406ce6b7467637c798d45d18fe6491f2bc3fd0be376650fb5bf9a5",
	"name1":		"Alice",
	"name2":		"Bob",
	"name3":		"Charlie",
	"name4":		"Dan",
	"xPub1":		"xpub6D1KS6WGkwMViePWuD6x6AZTvYS9fKxSboojKTzyx96xmKoDMCPRdsQcTJL1Qn1bpgHrTXUy6TMqrjPRaYZTqhtXSMhkgMkNmCqP4LeE3ZR",
	"xPub2":		"xpub6BtKTdFaGaTtE7B1mWoEGAhezKyWGRNvnyHznYgJkYHdWMxEyW4aPns6DvrxLkUsAimS2TTfE2hfa2US8jk1fkeX3H48NE4e2wbNbK82Bzc",
	"xPub3":		"xpub6ByJ7aWK1Kk7TcUNfbYx8MVe1UAZ7HiGxUYsEYSa67yz8bLTX1sDif3AYqLidP65ZCa3boPpeQwHsvG95s7owN4NNALGEqqwMibqRnRLmYw",
	"xPub4":		"xpub6D28q2qNBssjnJAtqiwAXkBVnunSVFYQm77XR3QiXUsQb3BYtMroZ4vyeUYTuojZChXP2RiviD9DvMoraW81KyNVEEjHFQztXRVqoa7k3LH",
}

# Basic project data
app_data = {
    "name":         "Audit Bitcoin P2SH Mutli-Signature Transaction",
    "description":  "PoC: determine co-signers who signed a P2SH transaction",
    "author":       "Markus Mächler",
    "html_title":   "Audit P2SH Multisig",
    "project_name": "Audit P2SH Multisig",
    "keywords":     "bitcoin,p2sh,multisig,audit,cosigner"
}

app_data['isClean'] = True   # switch if interface is started for the first time or reset
app_data['trxFound'] = True  # switch if input transaction was found or not
app_data['trxP2SH'] = False  # switch if input transaction spends a P2SH UTXO


@app.route('/', methods = ["POST", "GET"])
def index():
		if request.method == "GET": #without this issues with in private browsing windows
			app_data['isClean'] = True
			return render_template('index.html', app_data=app_data, app_trxdata=app_trxdata)

		if request.form['buttonbelow'] == 'tryagain':
			app_data['isClean'] = True
		elif request.form['buttonbelow'] == 'notfoundtryagain':
			app_data['isClean'] = True
			app_data['trxFound'] = True
		else:
			if request.form["inputTxid"] != "": txid = request.form["inputTxid"]
			else: txid=app_trxdata['txid']

			# only override default values if user input happened
			if request.form["inputxPub1Name"] != "": app_trxdata['name1'] = request.form["inputxPub1Name"]
			if request.form["inputxPub2Name"] != "": app_trxdata['name2'] = request.form["inputxPub2Name"]
			if request.form["inputxPub3Name"] != "": app_trxdata['name3'] = request.form["inputxPub3Name"]
			if request.form["inputxPub4Name"] != "": app_trxdata['name4'] = request.form["inputxPub4Name"]
			if request.form["inputxPub1"] != "": app_trxdata['xPub1'] = request.form["inputxPub1"]
			if request.form["inputxPub2"] != "": app_trxdata['xPub2'] = request.form["inputxPub2"]
			if request.form["inputxPub3"] != "": app_trxdata['xPub3'] = request.form["inputxPub3"]
			if request.form["inputxPub4"] != "": app_trxdata['xPub4'] = request.form["inputxPub4"]

			xPubDict = {
				app_trxdata['name1']: app_trxdata['xPub1'],
				app_trxdata['name2']: app_trxdata['xPub2'],
				app_trxdata['name3']: app_trxdata['xPub3'],
				app_trxdata['name4']: app_trxdata['xPub4']
			}
			
			try:
				rawtx = getRawTrx(txid)
				if rawtx == 'Transaction not found': throw
				app_data['trxFound'] = True
				trx = deserializeRawTrxHex(rawtx)
				app_trxdata['txid'] = txid
				app_trxdata['inputs'] = getTransactionInputList(trx)
				app_trxdata['outputs'] = getTransactionOutputList(trx)

				# check if strict P2SH multisig UTXO is spent
				if any("(p2sh_multisig)" in string for string in app_trxdata['inputs']):	
					addrDict = calcAddrListFromxPubs(xPubDict, 10)
					app_trxdata['cosigners'] = findCosigners(trx, addrDict)
					app_data['trxP2SH'] = True
				else:
					app_trxdata['cosigners'] = [["NOT SPENT P2SH_MULTISIG UTXO"]]
					app_data['trxP2SH'] = False

			except:
				app_data['trxFound'] = False
		
			app_data['isClean'] = False
		
		return render_template('index.html', app_data=app_data, app_trxdata=app_trxdata)


@app.route('/about')
def about():
    return render_template('about.html', app_data=app_data)


@app.route('/contact')
def contact():
    return render_template('contact.html', app_data=app_data)


if __name__ == '__main__':
    app.run(debug=DEVELOPMENT_ENV)