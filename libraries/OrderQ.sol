// SPDX-License-Identifier: Unlicense
pragma solidity >0.8.5;
import "libraries/Util.sol";
struct Order {
    bool side; // could (should) be bool

    uint price;
    uint size;
    address owner;

    bool maker;    
    bool filled;
    bool cancelled;
    uint sibling;
    uint position;}
function mkOrder(uint side_, uint price, uint size, address owner) pure returns(Order memory){
    return Order(boolean(side_), price, size, owner, false, false, false, 0, 0);}
library OrderLib {
    using OrderLib for Order;
    function _getSide(Order memory self) pure internal returns(uint){return side(self.side);}
    function _increaseSize(Order storage self, uint32 amount) internal {
	// should have a range check in here
	self.size += amount;}
    function _decreaseSize(Order storage self, uint32 amount) internal {
	// should have a range check in here
	self.size -= amount;}
    function _getId(Order memory self) pure internal returns(uint){
	return uint(keccak256(abi.encodePacked(self.side,self.price,self.owner)));}}
struct Queue {
    uint volume;
    mapping(uint => Order) q; // pos -> Order
    mapping(uint =>  uint) i; //  id -> pos
    uint first;
    uint  last;}
library QueueLib {
    using OrderLib for Order;
    using QueueLib for Queue;
    function _at(Queue storage self, uint pos_)view internal
	returns(Order storage){return self.q[pos_];}
    function _by(Queue storage self, uint  id_)view internal
	returns(Order storage){return self._at(self.i[id_]);}
    function _dlt(Queue storage self, Order memory order_)internal{
	self.volume -= order_.size;
	uint id = order_._getId();
	uint pos = self.i[id];
	delete self.i[id];
	delete self.q[pos];}
    function _unsafeAddAt(Queue storage self, uint pos_, Order memory order_)internal{
	self.volume += order_.size;
	self.q[pos_] = order_;
	self.i[order_._getId()] = pos_;}
    function _addAt(Queue storage self, uint  pos_, Order memory order_)internal{
	Order memory oldOrder = self.q[pos_];
	if (oldOrder.size > 0)
	    self.volume -= oldOrder.size;
	_unsafeAddAt(self, pos_, order_);}
    ////////////////////////////////////////
    function _init(Queue storage self)internal{self.first = 1;}
    function _isEmpty(Queue storage self)view internal
	returns(bool){return self.first > self.last;}
    function _whead(Queue storage self)view internal
	returns(Order storage){return self._at(self.first);}
    function _wtail(Queue storage self)view internal
	returns(Order storage){return self._at(self.last);}
    function _push(Queue storage self, Order memory order_)internal{
	if(self.first == 0)
	    self.first = 1;
	self.last += 1;
	self._unsafeAddAt(self.last, order_);}
    function _shift(Queue storage self)internal{
	if(self.first == 0)
	    self.first = 1;
	self._dlt(self._whead());
	self.first += 1;}}
