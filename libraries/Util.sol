// SPDX-License-Identifier: Unlicense
pragma solidity >0.8.5;
uint constant BID = 0;
uint constant ASK = 1;
function boolean(uint x) pure returns(bool){return x>0;}
function side(bool x) pure returns(uint){return x?1:0;}
function flip(uint x) pure returns(uint){return side(!boolean(x));}
