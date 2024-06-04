package main

import (
	"crypto/aes"
	"crypto/cipher"
	"encoding/hex"
	"fmt"
	"log"
)

func main() {

	encryptedData := "6f7e9007dd0882f3f320a08690a230b84fcfa66b483dc4f4352123276622af4cc5c656bf0171c36271700f8f4f0f41d14d7c20baec601c70f670acc8b6037a"
	keyString := "6eba99bf3fac4c92a857b05cff433a39"

	key, err := hex.DecodeString(keyString)
	if err != nil {
		log.Fatal(err)
	}
	ciphertext, err := hex.DecodeString(encryptedData)
	if err != nil {
		log.Fatal(err)
	}

	block, err := aes.NewCipher(key)
	if err != nil {
		log.Fatal(err)
	}
	if len(ciphertext)%aes.BlockSize != 0 {
		log.Fatal("The length of the encrypted data is incorrect")
	}

	iv := ciphertext[:aes.BlockSize]
	ciphertext = ciphertext[aes.BlockSize:]

	mode := cipher.NewCBCDecrypter(block, iv)
	mode.CryptBlocks(ciphertext, ciphertext)

	padding := int(ciphertext[len(ciphertext)-1])
	if padding < 1 || padding > aes.BlockSize {
		log.Fatal("This is incorrect padding.")
	}
	for _, val := range ciphertext[len(ciphertext)-padding:] {
		if int(val) != padding {
			log.Fatal("This is incorrect padding.")
		}
	}
	ciphertext = ciphertext[:len(ciphertext)-padding]

	fmt.Printf("Decrypted message: %s\n", string(ciphertext))
}
