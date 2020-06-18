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

if !exists('g:bauhaus_version')
  let g:bauhaus_version = '6.9.15'
endif

function! ConvertBauhaus(path)

python3 << EOF
path = vim.eval('a:path')
bh_version = vim.eval('g:bauhaus_version')
dicts = bh2err.convert_to_dicts(path, bh_version)
EOF

  let l:items = py3eval('dicts')
  call setqflist(l:items, 'r')
  "let w:quickfix_title = 'Bauhaus Issues'
  ":cw
  :cc

endfunction

command! -nargs=1 ConvBh call ConvertBauhaus(<args>)

let g:vim_axivion_bauhaus_loaded = 1
