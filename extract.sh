#!/bin/bash
set -e
grep '^(0)' LOG | grep -v ETH | cut -c5- >0.prv
grep '^(1)' LOG | grep -v ETH | cut -c5- >1.prv
grep '^(2)' LOG | grep -v ETH | cut -c5- >2.prv
grep '^(3)' LOG | grep -v ETH | cut -c5- >3.prv
grep '^(4)' LOG | grep -v ETH | cut -c5- >4.prv
grep '^(5)' LOG | grep -v ETH | cut -c5- >5.prv
grep '^(6)' LOG | grep -v ETH | cut -c5- >6.prv
grep '^(7)' LOG | grep -v ETH | cut -c5- >7.prv
grep '^(8)' LOG | grep -v ETH | cut -c5- >8.prv
grep '^(9)' LOG | grep -v ETH | cut -c5- >9.prv

grep '^(0)' LOG | grep ETH | cut -c5-46 >0.pub
grep '^(1)' LOG | grep ETH | cut -c5-46 >1.pub
grep '^(2)' LOG | grep ETH | cut -c5-46 >2.pub
grep '^(3)' LOG | grep ETH | cut -c5-46 >3.pub
grep '^(4)' LOG | grep ETH | cut -c5-46 >4.pub
grep '^(5)' LOG | grep ETH | cut -c5-46 >5.pub
grep '^(6)' LOG | grep ETH | cut -c5-46 >6.pub
grep '^(7)' LOG | grep ETH | cut -c5-46 >7.pub
grep '^(8)' LOG | grep ETH | cut -c5-46 >8.pub
grep '^(9)' LOG | grep ETH | cut -c5-46 >9.pub
