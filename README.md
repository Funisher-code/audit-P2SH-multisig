# Audit P2SH Multisig Transaction

This webpage was created as part of an assignment in the CAS in Blockchain at the University of Zurich in 2020.
The purpose is to provide auditability for P2SH mutlisig transaction.

It determines the co-signers for any given P2SH multisig transaction hash.
By providing xPubs one can additionally put a name tag on the co-signers.

![website](https://github.com/Funisher-code/audit-P2SH-multisig/blob/main/images/PoC_small.gif)

## Dependencies

```bash
pip install flask bitcoinlib
```

## Running it locally

```bash
git clone https://github.com/Funisher-code/audit-P2SH-multisig/
cd audit-P2SH-multisig
python index.py
```

Your app should be accessible on [localhost:5000](http://localhost:5000/).

![running](https://github.com/Funisher-code/audit-P2SH-multisig/blob/main/images/startup_small.gif)

----

### Installation issues on Windows

If you want to run it on a Windows system you might get an error when trying to install the bitcoinlib dependency scrypt.

#### Solution: 

- install Visual C++ 14.0
- install OpenSSL and place it in the following folder: ```C:\OpenSSL-Win64```


