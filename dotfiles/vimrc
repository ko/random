" My vimrc file.
"
" 2007 Sep 12: First version
" 2008 Feb 10: Second version
"
" Ken Ko <web@yaksok.net>
"
" 2010 Oct 07: First version
" 2011 Oct 31: Second version
"

" When started as "evim", evim.vim will already have done these settings.
if v:progname =~? "evim"
  finish
endif

" Use Vim settings, rather then Vi settings (much better!).
" This must be first, because it changes other options as a side effect.
set nocompatible

" allow backspacing over everything in insert mode
set backspace=indent,eol,start

if has("vms")
  set nobackup		" do not keep a backup file, use versions instead
else
  set backup		" keep a backup file
endif

" My preferred settings
set history=500		" keep 500 lines of command line history
set ruler		" show the cursor position all the time
set showcmd		" display incomplete commands
set incsearch		" do incremental searching
set sw=4
set autowrite		" write the old file out when switching from one file to another
set backupdir=~/.vimbackup
set tabstop=4
set softtabstop=4
 set expandtab
set comments=s1:/*:,mb:*,ex:*/
"set path+=./**,../build/**
set ignorecase

" ctags shortcuts
set tags=tags;/
map <C-\> :tab split<CR>:exec("tag ".expand("<cword>"))<CR>
map <A-]> :vsp <CR>:exec("tag ".expand("<cword>"))<CR>

" cscope shortcuts
cscope add ./cscope.out

" scrolling buffer of 25 lines from the top/bottom window edges
set scrolloff=25

" Navigating tabs (vim 7+, I believe)
" ctrl + {k,j}
map <C-j> :tabp<cr>
map <C-k> :tabn<cr>

" Abbreviations
ab #d #define
ab #i #include <>

" Fix the del key
set t_kD=

" Line numbers, show them.
set number

" colorscheme desert
colorscheme blackboard

" For Win32 GUI: remove 't' flag from 'guioptions': no tearoff menu entries
" let &guioptions = substitute(&guioptions, "t", "", "g")

" Don't use Ex mode, use Q for formatting
map Q gq

" This is an alternative that also works in block mode, but the deleted
" text is lost and it only works for putting the current register.
"vnoremap p "_dp

" Switch syntax highlighting on, when the terminal has colors
" Also switch on highlighting the last used search pattern.
if &t_Co > 2 || has("gui_running")
  syntax on
  set hlsearch
endif

set cindent shiftwidth=4

" F5 - Toggle Taglist
" F6 - Close Taglist
nnoremap <silent> <F5> :TlistToggle<CR>
nnoremap <silent> <F6> :TlistClose<CR>

" We want taglist.vim to use the right hand side.
let Tlist_Use_Right_Window=1

" Only do this part when compiled with support for autocommands.
if has("autocmd")

  " Enable file type detection.
  " Use the default filetype settings, so that mail gets 'tw' set to 72,
  " 'cindent' is on in C files, etc.
  " Also load indent files, to automatically do language-dependent indenting.
  filetype plugin indent on

  " Put these in an autocmd group, so that we can delete them easily.
  augroup vimrcEx
  au!

  " For all text files set 'textwidth' to 78 characters.
  autocmd FileType text setlocal textwidth=78

  " When editing a file, always jump to the last known cursor position.
  " Don't do it when the position is invalid or when inside an event handler
  " (happens when dropping a file on gvim).
  autocmd BufReadPost *
    \ if line("'\"") > 0 && line("'\"") <= line("$") |
    \   exe "normal g`\"" |
    \ endif

  augroup END

else

  set autoindent		" always set autoindenting on

endif " has("autocmd")
