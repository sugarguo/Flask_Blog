set nocompatible              " be iMproved, required
filetype off                  " required

" set the runtime path to include Vundle and initialize
set rtp+=~/.vim/bundle/Vundle.vim
call vundle#begin()
" alternatively, pass a path where Vundle should install plugins
"call vundle#begin('~/some/path/here')

" let Vundle manage Vundle, required
Plugin 'gmarik/Vundle.vim'
Plugin 'scrooloose/syntastic' 

Plugin 'nvie/vim-flake8'

" The following are examples of different formats supported.
" Keep Plugin commands between vundle#begin/end.
" plugin on GitHub repo
" Plugin 'The-NERD-Commenter'
Plugin 'scrooloose/nerdtree'
let NERDTreeWinPos='right'
let NERDTreeWinSize=30
map <F2> :NERDTreeToggle<CR>

Plugin 'OmniCppComplete'

Plugin 'taglist.vim'
let Tlist_Ctags_Cmd='ctags'
let Tlist_Show_One_File=1               "不同时显示多个文件的tag，只显示当前文件的
let Tlist_WinWidt =28                    "设置taglist的宽度
let Tlist_Exit_OnlyWindow=1             "如果taglist窗口是最后一个窗口，则退出vim
let Tlist_Use_Right_Window=1            "在右侧窗口中显示taglist窗口
let Tlist_Use_Left_Windo =1                "在左侧窗口中显示taglist窗口

Plugin 'tpope/vim-fugitive'
Plugin 'terryma/vim-multiple-cursors'
" Default mapping
let g:multi_cursor_next_key='<C-n>'
let g:multi_cursor_prev_key='<C-p>'
let g:multi_cursor_skip_key='<C-x>'
let g:multi_cursor_quit_key='<Esc>'


Plugin 'Raimondi/delimitMate'
Plugin 'Shougo/neocomplcache.vim'
let g:neocomplcache_enable_at_startup = 1
let g:neocomplcache_enable_auto_select = 1 
" Plugin 'Valloric/YouCompleteMe'
" Plugin 'rdnetto/YCM-Generator'
Plugin 'bling/vim-airline'
 "设置状态栏符号显示，下面编码用双引号"
"let g:Powerline_symbols='fancy'
"let g:airline_symbols = {}
"let g:airline_left_sep = '\u2b80' 
"let g:airline_left_alt_sep = '\u2b81'
"let g:airline_right_sep = '\u2b82'
"let g:airline_right_alt_sep = '\u2b83'
"let g:airline_symbols.branch = '\u2b60'
"let g:airline_symbols.readonly = '\u2b64'
"let g:airline_symbols.linenr = '\u2b61'

"设置顶部tabline栏符号显示"
"let g:airline#extensions#tabline#left_sep = '\u2b80'
"let g:airline#extensions#tabline#left_alt_sep = '\u2b81'
set laststatus=2



" plugin from http://vim-scripts.org/vim/scripts.html
" Plugin 'L9'

" Git plugin not hosted on GitHub
" Plugin 'git://git.wincent.com/command-t.git'
" Plugin 'file:///home/gmarik/path/to/plugin'
" Plugin 'rstacruz/sparkup', {'rtp': 'vim/'}
" Plugin 'user/L9', {'name': 'newL9'}

call vundle#end()            " required
call pathogen#infect()

filetype plugin indent on    " required
" To ignore plugin indent changes, instead use:
"filetype plugin on
"
" Brief help
" :PluginList          - list configured plugins
" :PluginInstall(!)    - install (update) plugins
" :PluginSearch(!) foo - search (or refresh cache first) for foo
" :PluginClean(!)      - confirm (or auto-approve) removal of unused plugins
"
" see :h vundle for more details or wiki for FAQ
" Put your non-Plugin stuff after this line



set encoding=utf-8			" 设置当前字符编码为 UTF-8

set langmenu=zh_CN.UTF-8		" 使用中文菜单

filetype plugin indent on		" 开启文件类型自动识别

set fencs=utf-8,usc-bom,euc-jp,gb18030,gbk,gb2312,cp936 	" 设置编码的自动识别

set nocp

syntax enable

let python_highlight_all=1
syntax on				" 语法高亮

" colorscheme desert
" endif

set ignorecase				" 搜索模式里忽略大小写
set smartcase				" 如果搜索模式包含大写字符，不使用 'ignorecase' 选项。只有在输入搜索模式并且打开 'ignorecase' 选项时才会使用。
set autowrite				" 自动把内容写回文件: 如果文件被修改过，在每个 :next、:rewind、:last、:first、:previous、:stop、:suspend、:tag、:!、:make、CTRL-] 和 CTRL-^命令时进行；用 :buffer、CTRL-O、CTRL-I、'{A-Z0-9} 或 `{A-Z0-9} 命令转到别的文件时亦然。
set autoindent				" 设置自动对齐(缩进)：即每行的缩进值与上一行相等；使用 noautoindent 取消设置
set smartindent				" 智能对齐方式
set tabstop=4				" 设置制表符(tab键)的宽度
set softtabstop=4			" 设置软制表符的宽度    
set shiftwidth=4			" (自动) 缩进使用的4个空格
set cindent				" 使用 C/C++ 语言的自动缩进方式
set linespace=6 
" set cinoptions={0,1s,t0,n-2,p2s,(03s,=.5s,>1s,=1s,:1s     "设置C/C++语言的具体缩进方式
" set backspace=2			" 设置退格键可用
set showmatch				" 设置匹配模式，显示匹配的括号
set linebreak				" 整词换行
set whichwrap=b,s,<,>,[,]		" 光标从行首和行末时可以跳到另一行去
" set hidden " Hide buffers when they are abandoned
" set mouse=a 				" Enable mouse usage (all modes)    "使用鼠标
set number				" Enable line number    "显示行号
" set previewwindow			" 标识预览窗口
set history=50				" set command history to 50    "历史记录50条


"--状态行设置--
set laststatus=2			" 总显示最后一个窗口的状态行；设为1则窗口数多于一个的时候显示最后一个窗口的状态行；0不显示最后一个窗口的状态行
set ruler				" 标尺，用于显示光标位置的行号和列号，逗号分隔。每个窗口都有自己的标尺。如果窗口有状态行，标尺在那里显示。否则，它显示在屏幕的最后一行上。

"--命令行设置--
set showcmd				" 命令行显示输入的命令
set showmode				" 命令行显示vim当前模式

"--find setting--
set incsearch				" 输入字符串就显示匹配点
set hlsearch


"=============================================================================
" Platform dependent settings
"=============================================================================

if (has("win32"))

    "-------------------------------------------------------------------------
    " Win32
    "-------------------------------------------------------------------------

    if (has("gui_running"))
        set guifont=Bitstream_Vera_Sans_Mono:h9:cANSI
        set guifontwide=NSimSun:h9:cGB2312
    endif

else

    if (has("gui_running"))
        set guifont=Bitstream\ Vera\ Sans\ Mono\ 9
    endif

endif

au BufReadPost * if line("'\"") > 0|if line("'\"") <= line("$")|exe("norm '\"")|else|exe "norm $"|endif|endif   
