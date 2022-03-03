# VIM

## 配置思路

## 配置说明

### 基本设置

```
" Basic
set nocompatible
set mouse=a
set encoding=utf-8
set t_Co=256
filetype on
filetype plugin on
set wildmenu
set wildmode=longest:list,full
set autoread
set nobackup
set nowb
set noswapfile
```

### 显示相关

```
" Display
syntax on
set showmode
set showcmd
set number          " 显示行号
set relativenumber  " 显示相对行号
set cursorline      " 高亮当前光标所在行
set textwidth=120	" 显示行宽
set wrap            " 自动折行
set wrapmargin=2    " 折行边缘宽度
set linebreak       " 单词内不折行
set scrolloff=5
set ruler
set matchtime=1
set laststatus=2
set statusline=%F%m%r%h%w%=%{\"[\".(\"\"?&enc:&fenc).((exists(\"+bomb\")\ &&\ &bomb)?\"+\":\"\").\"]\"}[%{&ff}]%y%10.(%l,%c%V%)\|%P

" Searching
set showmatch
set hlsearch
set incsearch
set ignorecase
set smartcase

" Edit
autocmd FileType markdown,tex set spell spelllang=en,cjk
```

### 缩进

```
" Indent
filetype indent on  " file type based indentation
set autoindent      " 按下回车键后，下一行的缩进会自动跟上一行的缩进保持一致。
set smartindent     " 智能缩进
set tabstop=4       " 按下 Tab 键时，Vim 显示的空格数。
set softtabstop=4   " 按退格键时退回缩进的长度
set shiftwidth=4    " 按下缩进字符数
set expandtab
autocmd FileType make set noexpandtab shiftwidth=8 softtabstop=0
```

## 编码效率

### 操作

```
let mapleader=" "
inoremap jj <Esc>
map j gj
map k gk
```

### 补全

包括：

- 括号自动补全。支持 C/C++ 式大括号补全；
- 智能 Tab 判断。支持智能跳出括号、文本补全、Tab 输入；

```
" Completion
inoremap ( ()<Left>
inoremap [ []<Left>
inoremap { {}<Left>
inoremap {<Space> {}<Left><Space><Space><Left>
inoremap {<CR> {}<Left><CR><CR><Esc>kA<Tab>
inoremap ' ''<Left>
inoremap " ""<Left>

func SmartTab()
    let pos = col('.')-1
    let char = getline('.')[pos]
    if char == ')' || char == ']' || char == '}' || char == '"' || char == "'"
        return "\<Esc>la"
    elseif !pos || getline('.')[pos-1] !~ '\k'
        return "\<Tab>"
    else
        return "\<C-N>"
    endif
endfunc
inoremap <Tab> <C-R>=SmartTab()<CR>
```

### 快速注释

```
" Commenting blocks of code.
let b:comment_leader = '//'
autocmd FileType sh,ruby,python,perl   let b:comment_leader = '#'
autocmd FileType conf,fstab            let b:comment_leader = '#'
autocmd FileType tex                   let b:comment_leader = '%'
autocmd FileType mail                  let b:comment_leader = '>'
autocmd FileType vim                   let b:comment_leader = '"'
noremap <silent> <Leader>c :<C-B>silent <C-E>s/^\(\s*\)/\1<C-R>=escape(b:comment_leader,'\/')<CR>/<CR>:nohlsearch<CR>
noremap <silent> <Leader>u :<C-B>silent <C-E>s/^\(\s*\)\V<C-R>=escape(b:comment_leader,'\/')<CR>/\1/e<CR>:nohlsearch<CR>/
```

### 文件头

```
" Template for Shell/Python scripts
func ScriptHeader()
    if &filetype == 'sh'
        call setline(1, "#!/bin/bash")
    elseif &filetype == 'python'
        call setline(1, "#!/usr/bin/python3")
    else
    endif
endfunc
autocmd BufNewFile *.{sh,py} call ScriptHeader()

" Template for C/C++ header file
function! s:insert_gates()
    let gatename = substitute(toupper(expand("%:t")), "\\.", "_", "g")
    execute "normal! i#ifndef " . gatename
    execute "normal! o#define " . gatename . " "
    execute "normal! Go#endif /* " . gatename . " */"
    normal! kk
endfunction
autocmd BufNewFile *.{h,hpp} call <SID>insert_gates()
```

### 代码格式化

```
" Code Formatting
func FormatCode()
    normal gg=G
    %s/\s\+$//e
endfunc
map <Leader>f gg=G
autocmd BufWritePre *.{c,cpp,python,sh,java} call FormatCode()
```

### 缩写

```
" Abbreviation for C/C++
abbr #i #include
abbr #d #define
```



## IDE

### F2 - 文件浏览器

```
" F2: File browser (netrw is good enough)
nmap <F2> :Lexplore<CR><C-w>l
let g:netrw_keepdir = 0 
let g:netrw_liststyle = 3 " Tree mode
let g:netrw_banner = 0 " Remove banner
let g:netrw_browse_split = 3 " Open behevior (open in new tab)
let g:netrw_winsize = 20 " The width of the directory explore (%)
let g:netrw_list_hide = '\(^\|\s\s\)\zs\.\S\+' " Do not display dotfile (use gh to toggle hidden files)

function! NetrwMapping()
    "nmap <buffer> H u
    "nmap <buffer> h -^
    nmap <buffer> l <CR>
    nmap <buffer> L <CR><F2>
    nmap <buffer> . gh
    nmap <buffer> P <C-w>z
endfunction

augroup netrw_mapping
    autocmd!
    autocmd filetype netrw call NetrwMapping()
augroup END
```

### F3 - 标签和窗口

```
" Tab Setting
" F3
" F4
nmap <Leader><Tab>  :tabc<CR>
nmap <silent> <Tab>  :tabn<CR>
" TODO 
nmap <silent> <F3> :tabp<CR>
nmap <silent> <F4> :tabn<CR> 
" window move
nmap <Leader>h <C-w>h
nmap <Leader>l <C-w>l
nmap <Leader>j <C-w>j
nmap <Leader>k <C-w>k
```



### F5 - 运行单文件脚本/代码

```
" F5: Run single script (Shell/Python/C) 
func! CompileRunGcc()
    exec "w"
    if &filetype == 'sh'
        :!time bash %
    elseif &filetype == 'python'
        exec "!time python3 %"
    elseif &filetype == 'c'
        exec "!gcc % -o %<"
        exec "! ./%"
    else
    endif
endfunc
```

### 其他

```
" F11   Full Screen
set pastetoggle=<F11>

" F12: List white characters
set listchars=tab:»·,trail:.,eol:¶
map <F12> :set list!<CR> 
```



## 配置示例

### 轻量

```
"""""""""""""""""""""""""""""
" Lightweight
"""""""""""""""""""""""""""""
" 基本设置
set nocompatible	" 不与 vi 兼容
set showmode		" 设置底部显示当前模式
set showcmd			" 设置底部显示当前键入指令
set encoding=utf-8	" 设置编码
set mouse=a			" 支持鼠标
set t_Co=256		" 设置 256 色
set noerrorbells	" 取消错误警告声
filetype on
filetype plugin on
filetype indent on

" 外观显示
set number			" 显示行数
set relativenumber	" 显示相对行号
set cursorline		" 光标所在行高亮
set textwidth=80	" 设置行宽
set wrap			" 设置自动折行显示
set wrapmargin=2	" 设置折行处与右边缘空格数
set linebreak		" 单词内部不折行
set scrolloff=5		" 垂直滚动时光标距离顶部/底部行数
set laststatus=2	" 显示状态栏
set ruler			" 状态栏显示光标当前位置（行、列）
set listchars=tab:>-,trail:.
set list			" 修改空白字符显示效果

" 缩进
set autoindent		" 回车后保持缩进
set smartindent		" 智能缩进
set tabstop=4		" 编辑模式按下 Tab 显示的宽度
set shiftwidth=4	" 命令模式按下缩进 >> 显示的宽度
set expandtab 		" 设置 Tab 自动转为空格
set softtabstop=4	" 设置 Tab 转为空格的个数
autocmd FileType make set noexpandtab shiftwidth=8 softtabstop=0
autocmd 
set formatoptions=tcrqn

" 搜索
set showmatch		" 高亮匹配括号
set matchtime=1		" 匹配括号高亮显示时间 1/10 秒
set hlsearch		" 高亮搜索结果
set incsearch		" 搜索时自动跳转到当前输入字符的第一个匹配位置
set ignorecase		" 搜索忽略大小写
set smartcase		" 智能搜索大小写

" 编辑
syntax on			" 语法高亮
autocmd FileType markdown,tex set spell spelllang=en,cjk		" 设置文本文件的单词拼写检查
set wildmenu		" 命令模式下 Tab 自动补全命令
set wildmode=longest:list,full
set autoread		" 文件监视，编辑过程中外部改变发出提示
set nobackup		" 不创建备份文件
set nowb			" 不创建写时备份文件
set noswapfile		" 不创建交换文件
set undofile		" 保留撤销历史

" 映射
map j gj			" 移动物理行
map k gk			" 移动物理行
map Y y$			" 复制到行尾
inoremap jj <ESC>	" jj 退出编辑模式

"""""""""""""""""""""""""
" IDE
""""""""""""""""""""""""""
map <F5> :call CompileRunGcc()<CR>
func! CompileRunGcc()
	exec "w"
	if &filetype == 'sh'
		:!time bash %
	elseif &filetype = 'c'
		exec "!gcc % -o %<"
		exec "! ./%<"
	elseif &filetype == 'python'
		exec "!time python3 %"
	endif
endfunc
```

## 参考

- https://blog.csdn.net/u013920085/article/details/46953293
