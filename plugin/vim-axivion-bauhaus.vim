if !has('python3')
  echo 'vim has to be compiled with +python3 for this plugin'
  finish
endif

if exists('g:vim_axivion_bauhaus_loaded')
  finish
endif

let s:plugin_root_dir = fnamemodify(resolve(expand('<sfile>:p')), ':h')

" Add python script to sys path
python3 << EOF
import sys
from os.path import normpath, join
import vim

plugin_root_dir = vim.eval('s:plugin_root_dir')
python_root_dir = normpath(join(plugin_root_dir, '..'))

sys.path.insert(0, python_root_dir)
import bh2err
EOF

" Define Options and their defaults
if !exists('g:bauhaus_version')
  let g:bauhaus_version = '6.9.15'
endif

if !exists('g:vim_axivion_bauhaus_open_error_list')
  let g:vim_axivion_bauhaus_open_error_list = 0
endif

if !exists('g:vim_axivion_bauhaus_jump_to_error')
  let g:vim_axivion_bauhaus_jump_to_error = 1
endif


" Define functions and commands

function! s:PopulateListWithErrors()
  let l:items = py3eval('dicts')
  if len(l:items) > 0
    call setqflist(l:items, 'r')
    if g:vim_axivion_bauhaus_jump_to_error
      :cc
    endif
    if g:vim_axivion_bauhaus_open_error_list
      :copen
    endif
  else
    echo 'No errors parsed.'
  endif
endfunction

function! ConvertBauhausFromFile(path)

  if filereadable(a:path)
python3 << EOF
path = vim.eval('a:path')
bh_version = vim.eval('g:bauhaus_version')
dicts = bh2err.convert_file(path, bh_version)
EOF
    call s:PopulateListWithErrors()
  else
    echo 'No such file.'
  endif

endfunction

function! ConvertBauhausFromInput(input)
python3 << EOF
content = vim.eval('a:input')
bh_version = vim.eval('g:bauhaus_version')
dicts = bh2err.convert_text(content, bh_version)
EOF
  call s:PopulateListWithErrors()
endfunction

function! ConvertBauhausFromCommand(input)
  let l:text = system(a:input)
python3 << EOF
content = vim.eval('l:text')
bh_version = vim.eval('g:bauhaus_version')
dicts = bh2err.convert_text(content, bh_version)
EOF
  call s:PopulateListWithErrors()
endfunction

command! -nargs=1 -complete=file ConvBh call ConvertBauhausFromFile(<f-args>)
command! -nargs=+ -complete=file ConvBhRaw call ConvertBauhausFromInput(<args>)
command! -nargs=+ -complete=file ConvBhCmd call ConvertBauhausFromCommand(<q-args>)

let g:vim_axivion_bauhaus_loaded = 1
