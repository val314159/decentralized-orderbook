pragma solidity >0.8.5;
// SPDX-License-Identifier: MIT

import "libraries/Book.sol";

contract OrderBookContract {
    using BokkyPooBahsRedBlackTreeLibrary for BokkyPooBahsRedBlackTreeLibrary.Tree;
    using OrderLib for Order;
    using QueueLib for Queue;
    using  BookLib for Book;

    Book book;

    constructor(address instrument, address currency) {
	book._init(100,instrument,currency);
    }

    function getOrderId(uint side_, uint price_, address owner_) pure external returns(uint){

	return uint(keccak256(abi.encodePacked(side_, price_, owner_)));

    }
    function cancelOrderId(uint side_, uint price_, uint id_) external{
	book._cancelOrderId( side_,  price_, id_);
    }

    function instrumentAvailableBalance(address who_)external view returns(uint){
	return book._instrumentAvailableBalance(who_);
    }
    function depositInstrumentBalance(address who_, uint amt_)external{
	book._depositInstrumentBalance(who_,  address(this),  amt_);
    }
    function withdrawInstrumentBalance(address who_, uint amt_)external{
	book._withdrawInstrumentBalance(who_,  address(this), amt_);
    }
    function holdInstrumentBalance(address who_, uint amt_)external{
	book._holdInstrumentBalance(who_,  amt_);
    }
    function unholdInstrumentBalance(address who_, uint amt_)external{
	book._unholdInstrumentBalance(who_,  amt_);
    }

    function currencyAvailableBalance(address who_)external view returns(uint){
	return book._currencyAvailableBalance(who_);
    }
    function depositCurrencyBalance(address who_, uint amt_)external{
	book._depositCurrencyBalance(who_,  address(this),  amt_);
    }
    function withdrawCurrencyBalance(address who_, uint amt_)external{
	book._withdrawCurrencyBalance(who_,  address(this), amt_);
    }
    function holdCurrencyBalance(address who_, uint amt_)external{
	book._holdCurrencyBalance(who_,  amt_);
    }
    function unholdCurrencyBalance(address who_, uint amt_)external{
	book._unholdCurrencyBalance(who_,  amt_);
    }

    //event Log(string where, uint key, uint value);
    //event Match(string where, uint key, uint value);

    function getOrderSize(uint side_, uint price_)view external returns(uint){
	return book.sides[side_].priceQ[price_]._whead().size;
    }

    function setOrderSize(uint side_, uint price_, uint size_) external{
	book._setOrderSize( side_,  price_,  size_);
    }

    function bestPrice(uint side_)view external returns(uint){
	return book._bestPrice(side_);}
    function bestVolume(uint side_)view external returns(uint){
	return book._bestVolume(side_);}
    function bestVolume2(uint side_,uint price_)view external returns(uint){
	return book._bestVolume2(side_,price_);}

    bool useHolds = false;
    
    function createLimitOrder(uint side_, uint size_, uint price_)external{
	require(price_!=0, "price cant be zero");
	if (useHolds){
	    if(side_==BID)
		this.holdCurrencyBalance(msg.sender, size_);
	    else
		this.holdInstrumentBalance(msg.sender, size_);
	}
	book._createLimitOrder(side_, price_, size_, msg.sender);}
    
    function createMarketOrder(uint side_, uint size_)external{
	if (useHolds){
	    if(side_==BID)
		this.holdCurrencyBalance(msg.sender, size_);
	    else
		this.holdInstrumentBalance(msg.sender, size_);
	}
	book._createMarketOrder(side_, size_, msg.sender);}
}
