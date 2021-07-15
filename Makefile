# -*- mode:Makefile -*-
#EXEC=docker exec -it qq # set this in env
SOLC=${EXEC} solc --no-color --bin --abi --overwrite --allow-paths .
NAMEX=val314159/$Q:21.04
DOCKER_RUN=docker run -w/home/val -uval -v${PWD}:/home/val \
	--privileged --rm -it --name $Q --network host ${NAMEX}
CONTRACTS=${wildcard contracts/*.sol}
cxxall: contracts run_orderbook
xxall: contracts run_tests run_test_t run_testing run_ed run_btest
xall:  run_test_t
all:   run_testing run_ed run_btest
run_%: scripts/%.py ; ${EXEC} python3 $<
run:rm       ;${DOCKER_RUN}    bash -l
bg: rm build ;${DOCKER_RUN} -d bash -l
gg: rm build ;${DOCKER_RUN}    make g
em: rm build ;${DOCKER_RUN}    emacs -nw
rm:    ;docker rm -f $Q || echo >/dev/null
exec:  ;docker exec -it $Q bash -l
emacs: ;docker exec -it $Q emacs
qq:    ; Q=qq make build
build: ;docker build -t $Q . && docker tag $Q ${NAMEX}
pull:  ;docker pull ${NAMEX}
push:  ;docker push ${NAMEX}
g:     ;rm -f LOG && ${EXEC} ganache-cli -h0 | tee LOG
gloop: ;while true; do make g; done
clean:
	rm -fr *~ qq/*~ out [0-9]*
	find . -name __pycache__ | xargs rm -fr
realclean: clean
	rm -fr .npm .*_history .config LOG .sudo* .local .config .cache
contracts: 0.prv ${CONTRACTS:contracts/%.sol=out/%.bin}
0.prv: ; scripts/extract.sh
out/%.bin: contracts/%.sol libraries/*.sol
	rm -f out/$*.cta && ${SOLC} $< -o out
out/%.abi: contracts/%.sol libraries/*.sol
	rm -f out/$*.cta && ${SOLC} $< -o out
dockerclean:
	(docker     ps -aq | xargs docker rm  -f) || echo
dockerrealclean: dockerclean
	(docker images -aq | xargs docker rmi -f) || echo
