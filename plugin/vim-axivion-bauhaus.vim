if !has("python3")
  echo "vim has to be compiled with +python3 for this plugin"
  finish
endif

if exists("g:vim_axivion_bauhaus_loaded")
  finish
endif

let s:plugin_root_dir = fnamemodify(resolve(expand("<sfile>:p")), ":h")

" Add python script to sys path
python3 << EOF
import sys
from os.path import normpath, join
import vim

plugin_root_dir = vim.eval("s:plugin_root_dir")
python_root_dir = normpath(join(plugin_root_dir, ".."))

sys.path.insert(0, python_root_dir)
EOF


function! PrintStuff()
  python3 bh2err.print_stuff()
endfunction

command! -nargs=0 PrintStuff call PrintStuff()



let g:vim_axivion_bauhaus_loaded = 1
