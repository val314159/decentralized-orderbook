pragma solidity >0.8.5;
// SPDX-License-Identifier: Unlicense
// From Mikhail Vladimirov via
// https://ethereum.stackexchange.com/questions/69825/decrypt-message-on-chain
// // jul 2, 2021, added salt for a little more security
//function crypt (bytes memory data, bytes memory key)
function crypt (bytes memory data, bytes memory key, bytes memory salt)
    pure returns (bytes memory result) {
    // Store data length on stack for later use
    uint256 length = data.length;
    assembly {
    	// Set result to free memory pointer
        result := mload (0x40)
	// Increase free memory pointer by lenght + 32
	mstore (0x40, add (add (result, length), 32))
	// Set result length
	mstore (result, length)
    }    
    // Iterate over the data stepping by 32 bytes
    for (uint i = 0; i < length; i += 32) {
	// Generate hash of the key and offset
	//bytes32 hash = keccak256 (abi.encodePacked (key, i));
	bytes32 hash2 = keccak256 (abi.encodePacked (key, i, salt));
	bytes32 chunk;
	assembly {
	    // Read 32-bytes data chunk
	    chunk := mload (add (data, add (i, 32)))
	}
	// XOR the chunk with hash
	//chunk ^= hash;
	chunk ^= hash2;
	assembly {
	    // Write 32-byte encrypted chunk
	    mstore (add (result, add (i, 32)), chunk)
	}
    }
}
