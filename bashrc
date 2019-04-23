## terminal appearance
alias ls='ls -G'
export CLICOLOR=1
export LSCOLORS=ExFxCxDxBxegedabagacad

alias ll='ls -lrth'
alias l='ls -lrth'
alias rmtilda='rm *~'
alias dh='du -h -d 1'

## top
alias t='top -o cpu'

## code
alias code='cd ~/Documents/code'

## text editor
alias x='xemacs'
#open /Applications/Sublime\ Text.app/Contents/MacOS/Sublime\ Text &'

## PATH
PATH=${PATH}:/Users/tgadfort/Documents/mva/phantomjs/bin
PATH=${PATH}:/usr/local/sbin

## MVA
alias mva='cd /Users/tgadfort/Documents/mva'
alias pymva='cd /Users/tgadfort/Documents/pymva'

## resource file
alias opentch='x ~/.bashrc'
alias copytch='cp bashrc .bashrc'
alias sourcetch='source ~/.bashrc'

## gotos
alias fin='cd ~/Documents/finance'
alias down='cd ~/Downloads'
alias doc='cd ~/Documents'

## Python Music
alias tag='python ~/Python/mp3TagSetter.py'
alias alb='python ~/Python/mp3AlbumFinder.py'

## Conda
condaname="py36"
alias condaupdate='conda update conda'
alias condacreate='conda create -n ${condaname} python=3.6 anaconda'
alias condadone='conda remove -n ${condaname} -all'
alias condaactivate='source activate ${condaname}'
alias act='source activate ${condaname}'
alias jup='jupyter notebook'

alias pyinst='python setup.py clean ; python setup.py install'

## Git
git config --global user.name "tgadf"
git config --global user.email tgadfort@gmail.com


## CUDA
export LD_LIBRARY_PATH=/usr/local/cuda/lib:${LD_LIBRARY_PATH}
