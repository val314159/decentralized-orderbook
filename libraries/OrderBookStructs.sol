pragma solidity >0.8.5;
// SPDX-License-Identifier: Unlicense
//import "node_modules/@openzeppelin/contracts/token/ERC20/ERC20.sol";
//import "node_modules/@openzeppelin/contracts/token/ERC20/IERC20.sol";

struct Order {
    bool side;
    uint price;
    uint size;
    address maker;
    bool filled;
    bool cancelled;

    // this gets set on the way in
    // zero means unset
    uint position;

    // other side of the pai
    uint sibling;
}
function mkOrder(bool side_,
		 uint price_,
		 uint size_,
		 address maker_
		 ) pure returns(Order memory){
    return Order(side_, price_, size_, maker_,
		 false, false, 0, 0);}

struct Queue {
    uint first;
    uint last;

    uint volume;
    // keep this up to date!
    
    mapping(uint => Order) q;
    mapping(uint =>  uint) x;
}

bool constant BID = false; //  buy side
bool constant ASK = true;  // sell side

struct Node {
    uint prev;
    uint curr;
    uint next;
}

struct Side {
    bool ascending;
    mapping(uint => Queue) priceQ;
    mapping(uint =>  Node) prices;
}

struct Book {
    uint id;
    Side[2]sides;
}

function boolean(uint x)pure returns(bool){
    return x>0;}

function side(bool x)pure returns(uint){
    return x?1:0;}
