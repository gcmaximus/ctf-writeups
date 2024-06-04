function bytesToStr(bytes) {
    return String.fromCharCode(...bytes);
}

function decodeWasm(encodedHexStr) {
    // Convert hex string to bytes
    let encodedBytes = new Uint8Array(encodedHexStr.match(/.{1,2}/g).map(byte => parseInt(byte, 16)));

    // Create a memory buffer
    const memory = new WebAssembly.Memory({ initial: 1 });
    const memArr = new Uint8Array(memory.buffer);

    // Copy the encoded bytes into the memory buffer
    for (let i = 0; i < encodedBytes.length; i++) {
        memArr[i] = encodedBytes[i];
    }

    // Placeholder for the Wasm decode function (reverse of encode)
    function decode(length) {
        for (let i = 0; i < length; i++) {
            memArr[i] = ~memArr[i] & 0xFF; // Inverting the bits back
            memArr[i] = memArr[i] >>> 1 | (memArr[i] & 0x01) << 7; // Reverse bitwise operation
        }
    }

    // Assuming the length of the encoded string is the same as the original
    const length = encodedBytes.length;
    decode(length);

    // Read the decoded bytes
    const decodedBytes = memArr.slice(0, length);

    // Convert bytes back to string
    return bytesToStr(decodedBytes);
}

// Example usage with the encoded string obtained from the original script
const encodedStr = "541c49061616531c040815190d0e5f121a0b0d";
console.log(decodeWasm(encodedStr));

