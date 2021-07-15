# -*-mode:sh-*-
export PYTHONPATH=.
export PATH=$PATH:./scripts
export WEB3_INFURA_PROJECT_ID=3471ef2a9eda43ee9b06159a1cb470ea
export WEB3_INFURA_SECRET=222660a87589473ba9fd9fb27890f6cf
alias g='make g'
alias c='sh extract.sh && make contracts'
alias m='make'
alias mc='make clean'
alias mrc='make realclean'
