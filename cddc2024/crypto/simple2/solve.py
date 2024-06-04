from Crypto.Cipher import AES
import binascii

def main():
    
    hex_chars = '0123456789abcdef'
    for i in hex_chars:
        for j in hex_chars:
            append = i+j
            print(append)
            encrypted_data = f"6f7e9007dd0882f3f320a08690a230b84fcfa66b483dc4f4352123276622af4cc5c656bf0171c36271700f8f4f0f41d14d7c20baec601c70f670acc8b6037a{append}"
            key_string = "6eba99bf3fac4c92a857b05cff433a39"

            key = bytes.fromhex(key_string)
            ciphertext = bytes.fromhex(encrypted_data)

            block_size = AES.block_size
            if len(ciphertext) % block_size != 0:
                print(block_size)
                print(len(ciphertext))
                print(len(ciphertext) % block_size)
                print(ciphertext)
                print("The length of the encrypted data is incorrect")

            iv = ciphertext[:block_size]
            ciphertext = ciphertext[block_size:]

            cipher = AES.new(key, AES.MODE_CBC, iv)
            plaintext = cipher.decrypt(ciphertext)

            padding = plaintext[-1]
            if padding < 1 or padding > block_size:
                print("This is incorrect padding.")
            if not all(byte == padding for byte in plaintext[-padding:]):
                print("This is incorrect padding.")

            plaintext = plaintext[:-padding]

            print("Decrypted message:", plaintext.decode())

if __name__ == "__main__":
    main()