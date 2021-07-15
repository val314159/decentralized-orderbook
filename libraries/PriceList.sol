// SPDX-License-Identifier: Unlicense
pragma solidity >0.8.5;
import "libraries/Util.sol";
struct  Node {
    uint cur;
    uint nxt;
    uint prv;
}
library NodeLib {
    using NodeLib for Node;
}
//mapping(uint => Node) p; // this is a PriceList
library PriceListLib {
    using NodeLib for Node;
    using PriceListLib for mapping(uint => Node);
    function _insert(mapping(uint => Node) storage self,
		    uint x, uint n, uint p)internal{
	self[x].cur = x;
	self[x].nxt = n;
	self[x].prv = p;
	self[n].prv = x;
	self[p].nxt = x;}
    function _prepend(mapping(uint => Node) storage self,
		    uint x)internal{
	uint n = self[0].nxt;
	self._insert(x, n, 0);
    }
    function _append(mapping(uint => Node) storage self,
		     uint x)internal{
	uint p = self[0].prv;
	self._insert(x, 0, p);
    }
    function _remove(mapping(uint => Node) storage self,
		     uint x)internal{
	uint n = self[0].nxt;
	uint p = self[0].prv;
	delete self[x];
	self[n].prv = p;
	self[p].nxt = n;
    }
    function _shift(mapping(uint => Node) storage self
		    )internal{
	uint n = self[0].nxt;
	require(n != 0, 'shift from empty PriceList');
	self._remove(n);}
    function _pop(mapping(uint => Node) storage self
		  )internal{
	uint p = self[0].prv;
	require(p != 0, 'shift from empty PriceList');
	self._remove(p);}
    function _findClosest(mapping(uint => Node) storage self,
			  uint x, uint side_)internal view returns(uint){
	return(side_==BID)?self._findGE(x):self._findLE(x);}
    function _findClosest(mapping(uint => Node) storage self,
			  uint x, bool side_)internal view returns(uint){
	return self._findClosest(x, side(side_));}
    
    function _findGE(mapping(uint => Node) storage self,
		     uint x)view internal returns(uint r_){
	if(self._has(x))
	    return x;
	uint n = self[0].nxt;
	uint p = self[0].prv;
	require(x > p,
		'above range');
	if(x < n)
	    return n;
	while(x > n){
	    if(self._has(x))
		return x;
	    x += 1;
	}
	require(false, "shouldnt ever get here");
    }
    function _findLE(mapping(uint => Node) storage self,
		     uint x)view internal returns(uint r_){
	if(self._has(x))
	    return x;
	uint n = self[0].nxt;
	uint p = self[0].prv;
	if(x > p)
	    return p;
	require(x < n,
		'below range');
	while(x > n){
	    if(self._has(x))
		return x;
	    x += 1;
	}
	require(false, "shouldnt ever get here");
    }    
    function _has(mapping(uint => Node) storage self,
		 uint x)view internal returns(bool){
	return(self[x].cur != 0);}
}

