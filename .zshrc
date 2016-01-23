HISTFILE=~/.zsh_history
HISTSIZE=1000
SAVEHIST=1000

setopt autocd extendedglob nomatch notify correctall promptsubst
unsetopt appendhistory beep
autoload -U colors compinit
colors 
compinit

[[ -a $(whence -p pacman-color) ]] && compdef _pacman pacman-color=pacman

eval $(dircolors ~/.dircolors)
autoload -U pick-web-browser
alias -s {go,txt,cfg,c,cpp,rb,asm,nim}=subl3
alias -s {avi,mpeg,mpg,mov,m2v}=mplayer
alias -s {html,htm}=chromium
alias -s {png,jpg,gif,svg}=viewnior
alias ls='ls --group-directories-first --time-style=+"%d.%m.%Y %H:%M" --color=auto -F'
alias ll='ls -lah --group-directories-first --time-style=+"%d.%m.%Y %H:%M" --color=auto -F'
alias la='ls -ah --group-directories-first --time-style=+"%d.%m.%Y %H:%M" --color=auto -F'
alias cp='cp -i'
alias df='df -h'
alias nvidia='vblank_mode=0 optirun -b primus'
alias unlock='sudo rm /var/lib/pacman/db.lck'
alias free='free -m'
alias grep='grep --colour=auto'
alias nimc='nim c --verbosity:0'
alias nimcr='nim c -r --verbosity:0 -d:release --opt:speed'
alias nimcrssl='nim c -d:ssl --threads:on -r --verbosity:0 -d:debug --gc:boehm --threadAnalysis:off'
alias nimi='nim secret'
alias gs='git status'
alias ga='git add'
alias gc='git commit -m'
alias gp='git push origin'
alias gpl='git pull origin'
alias gd='git diff'
alias gr='git rm'
alias gl='git lg'
alias wiki='wiki-search' # arch-wiki-lite
alias rm='rm -rf'
alias S='sudo pacman -S'
alias Ss='sudo pacman -Ss'
alias Syu='sudo pacman -Syu'
alias Syua='yaourt -Syua'
alias Q='sudo pacman -Q'
alias R='sudo pacman -R'
alias Rsc='sudo pacman -Rsc'
alias aS='yaourt -S'
alias aSs='yaourt -Ss'
alias pgp='gpg --recv-key'
alias feh='feh -q -g 1500x800 --scale-down --auto-zoom'
alias pycode='~/Documents/Python/'

bindkey '\e[3~' delete-char  # del
bindkey ';5D' backward-word  # ctrl+left
bindkey ';5C' forward-word   # ctrl+right

# extract <file>
ex () {
  if [ -f $1 ] ; then
    case $1 in
      *.tar.bz2)   tar xjf $1   ;;
      *.tar.gz)    tar xzf $1   ;;
      *.bz2)       bunzip2 $1   ;;
      *.rar)       unrar x $1   ;;
      *.gz)        gunzip $1    ;;
      *.tar)       tar xf $1    ;;
      *.tbz2)      tar xjf $1   ;;
      *.tgz)       tar xzf $1   ;;
      *.zip)       unzip $1     ;;
      *.Z)         uncompress $1;;
      *.7z)        7z x $1      ;;
      *)           echo "'$1' cannot be extracted via ex()" ;;
    esac
  else
    echo "'$1' is not a valid file"
  fi
}

sudo-command-line() {
    [[ -z $BUFFER ]] && zle up-history
    if [[ $BUFFER == sudo\ * ]]; then
        LBUFFER="${LBUFFER#sudo }"
    else
        LBUFFER="sudo $LBUFFER"
    fi
}
zle -N sudo-command-line
bindkey "\e\e" sudo-command-line

typeset -A key
key[Home]=${terminfo[khome]}
key[End]=${terminfo[kend]}
key[PageUp]=${terminfo[kpp]}
key[PageDown]=${terminfo[knp]}
[[ -n "${key[Home]}"     ]]  && bindkey  "${key[Home]}"     beginning-of-line
[[ -n "${key[End]}"      ]]  && bindkey  "${key[End]}"      end-of-line
[[ -n "${key[PageUp]}"   ]]  && bindkey  "${key[PageUp]}"   beginning-of-buffer-or-history
[[ -n "${key[PageDown]}" ]]  && bindkey  "${key[PageDown]}" end-of-buffer-or-history
if (( ${+terminfo[smkx]} )) && (( ${+terminfo[rmkx]} )); then
    function zle-line-init () {
        printf '%s' "${terminfo[smkx]}"
    }
    function zle-line-finish () {
        printf '%s' "${terminfo[rmkx]}"
    }
    zle -N zle-line-init
    zle -N zle-line-finish
fi

local gitprompt='$(~/dotfiles/gitprompt.py)'
export PROMPT="%{$fg_bold[blue]%}% %~${gitprompt} %{$fg[white]%}% $ %{$reset_color%}%u"
byobu; clear;