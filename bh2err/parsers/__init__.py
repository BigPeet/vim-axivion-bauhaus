from .sv_parser import SVParser
from .mv_parser import MVParser
from .av_parser import AVParser
from .de_parser import DEParser
from .cl_parser import CLParser
from .cy_parser import CYParser


Parsers = sorted([SVParser,
                  AVParser,
                  DEParser,
                  CLParser,
                  CYParser,
                  MVParser], key=lambda p: p.priority(), reverse=True)
