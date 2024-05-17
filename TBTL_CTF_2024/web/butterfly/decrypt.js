const CryptoJS = require('crypto-js');

const KEY = 'secret key is very secure';
const CIPHERTEXT = 'U2FsdGVkX19wWL7itIL7TZcLTP/e1ulrZolI9AHTA8OBGOCodb';

try {
    const decrypted = CryptoJS.AES.decrypt(CIPHERTEXT, KEY).toString(CryptoJS.enc.Utf8);
    console.log(decrypted);
} catch (error) {
    console.error('Decryption error:', error.message);
}