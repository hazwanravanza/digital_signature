from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

def PembangkitanKunciRSA(size):
    key = RSA.generate(size)
    kunci_publik = key.publickey()

    public_pem = kunci_publik.exportKey('PEM')
    private_pem = key.exportKey('PEM', passphrase="passwordku", pkcs=8, protection="scryptAndAES128-CBC")

    return {
        "success": True,
        "message": "Kunci berhasil dibuat!",
        "publicKey": public_pem.decode(),  
        "privateKey": private_pem.decode()
    }


def menandatangani(pesan, file_kunci):
    pesan = pesan.encode('utf-8')
    nilai_hash = SHA256.new(pesan)

    with open(file_kunci, "rb") as file:
        kunci_privat = RSA.import_key(file.read(), passphrase='passwordku')

    tanda_tangan = pkcs1_15.new(kunci_privat).sign(nilai_hash)
    return tanda_tangan


def memverifikasi(tandatangan, pesan, file_kunci):
    pesan = pesan.encode('utf-8')
    nilai_hash = SHA256.new(pesan)
  
    with open(file_kunci, "rb") as file:
        kunci_publik = RSA.import_key(file.read())
 
    try:
        pkcs1_15.new(kunci_publik).verify(nilai_hash, tandatangan)
        return 1 
    except (ValueError, TypeError):
        return 0 