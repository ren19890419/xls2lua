#!/usr/bin/python
#filename:setup.py
#coding=utf-8

from distutils.core import setup
import py2exe

#need to include lib file
includes = ["encodings", "encodings.*"] 

options = { "py2exe":
                                  {  "compressed": 1,
                                     "optimize": 2,
                                     "ascii": 1,
                                     "includes":includes,
                                     "bundle_files": 1, #all in one exe file 
								  }
}

setup(        
              version = "1.0.1",
              description = "xls2lua",
              name = "xls2lua",
              options = options,
              zipfile=None, #not generate library.zip
              console=[ { "script": "xls2lua_Int.py", 
                          "icon_resources": [(1, "xls2lua.ico")] } ]#src fiel ande icon
)