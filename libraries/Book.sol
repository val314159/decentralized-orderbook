// SPDX-License-Identifier: Unlicense
pragma solidity >0.8.5;
import "libraries/BokkyPooBahsRedBlackTreeLibrary.sol";
import "libraries/Util.sol";
import "libraries/OrderQ.sol";

import "node_modules/@openzeppelin/contracts/token/ERC20/IERC20.sol";

struct Side {
    bool ascending;
    mapping(uint => Queue) priceQ;
    BokkyPooBahsRedBlackTreeLibrary.Tree prices;
}
struct Book {
    uint id;
    Side[2] sides;

    IERC20 instrument;
    IERC20 currency;
    
    mapping(address => uint) instrumentBalance;
    mapping(address => uint)   currencyBalance;
    mapping(address => uint) instrumentHold;
    mapping(address => uint)   currencyHold;
}
library BookLib {
    using BokkyPooBahsRedBlackTreeLibrary for BokkyPooBahsRedBlackTreeLibrary.Tree;
    using OrderLib for Order;
    using QueueLib for Queue;
    using  BookLib for Book;

    function _instrumentAvailableBalance(Book storage self, address who_)view internal returns(uint){
	return (self.instrumentBalance[who_] - self.instrumentHold[who_]);}

    function _addInstrumentBalance(Book storage self, address who_, uint amt_)internal{
	self.instrumentBalance[who_] += amt_;
    }

    function _subInstrumentBalance(Book storage self, address who_, uint amt_)internal{
	self.instrumentBalance[who_] -= amt_;
    }

    function _depositInstrumentBalance(Book storage self, address who_, address contract_, uint amt_)internal{
	self.instrument.transferFrom(who_, contract_, amt_);
	self.instrumentBalance[who_] += amt_;
    }

    function _withdrawInstrumentBalance(Book storage self, address who_, address contract_, uint amt_)internal{
	require(amt_ > self._instrumentAvailableBalance(who_),
		"not enough avaliable funds");
	self.instrument.transferFrom(contract_, who_, amt_);
	self.instrumentBalance[who_] -= amt_;
    }

    function _holdInstrumentBalance(Book storage self, address who_, uint amt_)internal{
	require(self._instrumentAvailableBalance(who_) > amt_,
		"not enough avaliable funds");
	self.instrumentHold[who_] += amt_;
    }

    function _unholdInstrumentBalance(Book storage self, address who_, uint amt_)internal{
	require(amt_ < self.instrumentHold[who_],
		"not enough held funds");
	self.instrumentHold[who_] -= amt_;
    }

    function _currencyAvailableBalance(Book storage self, address who_)view internal returns(uint){
	return (self.currencyBalance[who_] - self.currencyHold[who_]);}

    function _addCurrencyBalance(Book storage self, address who_, uint amt_)internal{
	self.currencyBalance[who_] += amt_;
    }

    function _subCurrencyBalance(Book storage self, address who_, uint amt_)internal{
	self.currencyBalance[who_] -= amt_;
    }

    function _depositCurrencyBalance(Book storage self, address who_, address contract_, uint amt_)internal{
	self.currency.transferFrom(who_, contract_, amt_);
	self.currencyBalance[who_] += amt_;
    }

    function _withdrawCurrencyBalance(Book storage self, address who_, address contract_, uint amt_)internal{
	require(amt_ > self._currencyAvailableBalance(who_),
		"not enough avaliable funds");
	self.currency.transferFrom(contract_, who_, amt_);
	self.currencyBalance[who_] -= amt_;
    }

    function _holdCurrencyBalance(Book storage self, address who_, uint amt_)internal{
	require(self._currencyAvailableBalance(who_) > amt_,
		"not enough avaliable funds");
	self.currencyHold[who_] += amt_;
    }

    function _unholdCurrencyBalance(Book storage self, address who_, uint amt_)internal{
	require(amt_ < self.currencyHold[who_],
		"not enough held funds");
	self.currencyHold[who_] -= amt_;
    }

    function _init(Book storage self, uint id_,
		   address instrumentAddress,
		   address currencyAddress
		   )internal{
	self.id = id_;
	self.sides[BID].ascending = boolean(BID);
	self.sides[ASK].ascending = boolean(ASK);
	self.instrument = IERC20(instrumentAddress);
	self.currency   = IERC20(currencyAddress);
    }
    function _dleteOrder(Book storage self, Order memory order_)internal{
	uint side_ = side(order_.side);
	uint price_ = order_.price;
	self.sides[side_].priceQ[price_]._dlt(order_);}
    function _orderAt(Book storage self,
		      uint side_, uint price_, uint pos_)internal view returns(Order storage){
        return self.sides[side_].priceQ[price_]._at(pos_);}
    function _orderBy(Book storage self,
		      uint side_, uint price_, uint id_)internal view returns(Order storage){
        return self.sides[side_].priceQ[price_]._by(id_);}
    function _bestPrice(Book storage self,
			uint side_)view internal returns(uint){
	if(side_==BID){
	    return self.sides[BID].prices.last();
	}else{
	    return self.sides[ASK].prices.first();
	}
    }
    function _bestVolume(Book storage self,
			 uint side_)view internal returns(uint){
	uint price = self._bestPrice(side_);
	if(price == 0) return 0;
	if(side_==BID){
	    return self.sides[BID].priceQ[price].volume;
	}else{
	    return self.sides[ASK].priceQ[price].volume;
	}
    }
    function _bestVolume2(Book storage self,
			  uint side_, uint price)view internal returns(uint){
	if(price == 0) return 0;
	if(side_==BID)
	    return self.sides[BID].priceQ[price]._whead().size;
	else
	    return self.sides[ASK].priceQ[price]._whead().size;
    }
    function _setOrderSize(Book storage book,
			   uint side_, uint price_, uint size_) internal returns(uint){
	book.sides[side_].priceQ[price_]._whead().size = size_;
	return book.sides[side_].priceQ[price_]._whead().size;
    }
    function _createLimitOrder(Book storage self,
			  uint side_, uint price_, uint size_, address owner_)internal{
	require(price_ != 0, "illegal price");
	require(size_ != 0, "illegal size");
	
	Order memory order = mkOrder(side_, price_, size_, owner_);

	emit CreateOrder(order);
		
	/* before we actually stick the order in the book, let's match it
	 * first.  that way, we only put outstanding orders in the book.
	 */

	//if(!self._attemptMatch(order)){
	if(!self._attemptMatches(order, 16)){
	    // if we don't get fully matched, put in book
	    
	    self.sides[side_].priceQ[price_]._push(order);
	
	    if (!self.sides[side_].prices.exists(price_))
		self.sides[side_].prices.insert(price_);
	
	    // emit event
	    /* NYI */
	}
    }

    function _createMarketOrder(Book storage self,
			  uint side_, uint size_, address owner_)internal{
	require(size_ != 0, "illegal size");

	Order memory order = mkOrder(side_, 0, size_, owner_);

	emit CreateOrder(order);
	
	/* before we actually stick the order in the book, let's match it
	 * first.  that way, we only put outstanding orders in the book.
	 */

	if(!self._attemptMatches(order, 16)){
	    // if we don't get fully matched, throw it away.

	    // emit event
	    /* NYI */
	}
    }
    function _cancelOrderId(Book storage self, uint side_, uint price_, uint id_)internal{
	require(self.sides[side_].prices.exists(price_), "no price");
	Queue storage priceQ = self.sides[side_].priceQ[price_];
	Order memory order = priceQ._by(id_);
	priceQ._dlt(order);
    }
    
    function _cancelOrder(Book storage self, Order memory order_)internal{
	order_.cancelled = true;
	/* NYI */
	// emit event
        self._dleteOrder(order_);}
    
    function _fillOrder(Book storage self, Order memory order_, bool dlt)internal{
	order_.filled = true;
	/* NYI */
	// emit event
        if(dlt)self._dleteOrder(order_);}
    
    function _matchOrders(Book storage self,
			  Order storage thisOrder_, Order memory thatOrder_)internal{
        thisOrder_.sibling   = thatOrder_._getId();
        thatOrder_.sibling   = thisOrder_._getId();
        //thisOrder_.fillPrice = thisOrder_.price;
        //thatOrder_.fillPrice = thisOrder_.price;
        uint size_ = (thisOrder_.size < thatOrder_.size ?
		      thisOrder_.size : thatOrder_.size);
	// emit event
        //print(f'Matched {thisOrder_} {thatOrder_} {size_}');
        thisOrder_.size -= size_;
        thatOrder_.size -= size_;
        if(thisOrder_.size == 0)self._fillOrder(thisOrder_,  true);
	if(thatOrder_.size == 0)self._fillOrder(thatOrder_, false);}
    function _flipSide(Book storage self, uint side_)internal view returns(Side storage){
	return self.sides[flip(side_)];}
    function _thisSide(Book storage self, uint side_)internal view returns(Side storage){
	return self.sides[side_];}
    function _attemptMatch(Book storage self,
			   Order memory newOrder)internal returns(bool){
	// true  = fully matches
	// false = not fully matches, put in book
	
	// returns size of match
	require(newOrder.size > 0, "bad size");

	uint flipped = flip(side(newOrder.side));

	Side storage sid = self.sides[flipped];

	uint best = self._bestPrice(flipped);
	    
	if (best==0)
	    return false; // not fully matched, put in book

	uint newOrderPrice = newOrder.price;

	if (newOrder.price == 0)
	    newOrderPrice = best;

	if(flipped==BID){
	    if(best < newOrderPrice)
		return false; // not fully matched, put in book
	}else{
	    if(best > newOrderPrice)
		return false; // not fully matched, put in book
	}

	Queue storage priceQ = sid.priceQ[best];

	uint osize = newOrder.size;
	    
	uint size = osize;

	Order storage oldOrder = priceQ._whead();

	uint nsize = oldOrder.size;

	bool ret = true;
	
	if (osize == nsize){
	    // exact match, get rid of the order
	    // emit here
	    priceQ._shift();
	    if(priceQ._isEmpty()){
		delete sid.priceQ[best];
		sid.prices.remove(best);
	    }
	} else if (osize > nsize){
	    // ask for more than we have on top
	    size = nsize;
	    // emit here
	    priceQ._shift();
	    if(priceQ._isEmpty()){
		delete sid.priceQ[best];
		sid.prices.remove(best);
	    }
	    ret = false;
	} else {
	    priceQ.volume -= size;
	    oldOrder.size -= size;
	}

	// release the buyer hold
	// release the seller hold

	// do the swap
	/*
	if(side(newOrder.side)==BID){
	    self._unholdInstrumentBalance(oldOrder.owner, size);
	    self._subInstrumentBalance(oldOrder.owner,    size);
	    self._addInstrumentBalance(newOrder.owner,    size);

	    self._unholdCurrencyBalance(newOrder.owner, best);
	    self._subCurrencyBalance(newOrder.owner,    best);
	    self._addCurrencyBalance(oldOrder.owner,    best);
	}else{
	    self._unholdInstrumentBalance(newOrder.owner, size);
	    self._subInstrumentBalance(newOrder.owner,    size);
	    self._addInstrumentBalance(oldOrder.owner,    size);

	    self._unholdCurrencyBalance(oldOrder.owner, best);
	    self._subCurrencyBalance(oldOrder.owner,    best);
	    self._addCurrencyBalance(newOrder.owner,    best);
	}
	*/
	
	newOrder.size -= size;
	emit FillOrder(size, oldOrder, newOrder);
	return ret;
    }
    function _attemptMatches(Book storage self,
			     Order memory newOrder, uint maxFills)internal returns(bool){
	for(uint n=0; n<maxFills; ++n){
	    if(newOrder.size <= 0)
		return true;
	    self._attemptMatch(newOrder);
	}
	if(newOrder.size <= 0)
	    return true;
	return false;
    }

    event FillOrder(uint size, Order taker, Order maker);
    event CreateOrder(Order order);

}
