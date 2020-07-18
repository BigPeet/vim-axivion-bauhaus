from bh2err.parsers import sv_parser, mv_parser, av_parser, de_parser, cl_parser, cy_parser

Parsers = sorted([sv_parser.SVParser,
                  av_parser.AVParser,
                  de_parser.DEParser,
                  cl_parser.CLParser,
                  cy_parser.CYParser,
                  mv_parser.MVParser], key=lambda p: p.priority(), reverse=True)
