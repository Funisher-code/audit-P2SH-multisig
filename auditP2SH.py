import bitcoinlib.transactions as transactions
import bitcoinlib.keys as keys
import requests

#if __name__ == '__main__':

def getRawTrx(querytxid):	
	# fetch a trx from a blockchain explorer
	resp = requests.get('https://blockchain.info/rawtx/'+querytxid+'?format=hex')
	return resp.text
	
def deserializeRawTrxHex(rawTrxHex):	
	trx = transactions.transaction_deserialize(rawTrxHex)
	return trx
	
def getTransactionInputList(trx):
	inputList = []
	for input in trx.inputs:
		inputList.append(input.address + " (" + input.script_type + ")")
	return inputList

def getTransactionOutputList(trx):
	outputList = []
	for output in trx.outputs:
		outputList.append(output.address + " (" + output.script_type + ")")
	return outputList
	
	
def findCosigners(trx, addrDict):
    cosignerList = []
    for input in trx.inputs: # loop over all the inputs
        transaction_hash = trx.signature_hash(input.index_n, witness_type=input.witness_type)
        for sig in input.signatures: # loop over all the signatures of an input
            for key in input.keys: # loop over all the keys of an input
                if sig.verify(transaction_hash, key): # check if signature matches the key
                    sigAddress = key.address_obj.address
                    xPubmatch = addrDict.get(sigAddress)
                    if xPubmatch: # check if address matches xpub dictionary
                        cosignerName = xPubmatch
                    else:
                        cosignerName = "UNKNOWN XPUB"
                    cosignerList.append([cosignerName,sigAddress,key])   

    return cosignerList

def calcAddrListFromxPubs(xPubDict, depth):
    addrDict = {}
    #addrDict.update({"1abC": "Alice"})
    for xPub in xPubDict:
        name = xPub
        key = keys.HDKey(xPubDict.get(xPub))
        for i in range(depth):
            addrDict.update({key.subkey_for_path("m/0/"+str(i)).address() : name}) #receiving address
            addrDict.update({key.subkey_for_path("m/1/"+str(i)).address() : name}) #change address   
    return addrDict