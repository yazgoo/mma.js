""" getTerminalSize()
 - get width and height of console
 - works on linux,os x,windows,cygwin(windows)

  copied from:
    http://stackoverflow.com/questions/566746/how-to-get-console-window-width-in-python

  bvdp jan/2013: I've added the python 3.3 library call and converted
                 a couple of print statements to make them py3 compatible.
   anyway.
"""

import sys, os

__all__=['getTerminalSize']


def getTerminalSize():

   # try to use the built lib call. Available in py 3.3+
   try:
      return os.get_terminal_size()
   except:
      pass

   import platform
   current_os = platform.system()
   tuple_xy=None
   if current_os == 'Windows':
       tuple_xy = _getTerminalSize_windows()
       if tuple_xy is None:
          tuple_xy = _getTerminalSize_tput()
          # needed for window's python in cygwin's xterm!
   if current_os == 'Linux' or current_os == 'Darwin' or  current_os.startswith('CYGWIN'):
       tuple_xy = _getTerminalSize_linux()
   if tuple_xy is None:
       tuple_xy = (80, 25)      # default value
   return tuple_xy

def _getTerminalSize_windows():
    res=None
    try:
        from ctypes import windll, create_string_buffer

        # stdin handle is -10
        # stdout handle is -11
        # stderr handle is -12

        h = windll.kernel32.GetStdHandle(-12)
        csbi = create_string_buffer(22)
        res = windll.kernel32.GetConsoleScreenBufferInfo(h, csbi)
    except:
        return None
    if res:
        import struct
        (bufx, bufy, curx, cury, wattr,
         left, top, right, bottom, maxx, maxy) = struct.unpack("hhhhHhhhhhh", csbi.raw)
        sizex = right - left + 1
        sizey = bottom - top + 1
        return sizex, sizey
    else:
        return None

def _getTerminalSize_tput():
    # get terminal width
    # src: http://stackoverflow.com/questions/263890/how-do-i-find-the-width-height-of-a-terminal-window
    try:
#       import subprocess
#       proc=subprocess.Popen(["tput", "cols"],stdin=subprocess.PIPE,stdout=subprocess.PIPE)
#       output=proc.communicate(input=None)
#       cols=int(output[0])
#       proc=subprocess.Popen(["tput", "lines"],stdin=subprocess.PIPE,stdout=subprocess.PIPE)
#       output=proc.communicate(input=None)
#       rows=int(output[0])
#       return (cols,rows)
       return (80,25)
    except:
       return None


def _getTerminalSize_linux():
    def ioctl_GWINSZ(fd):
        try:
            import fcntl, termios, struct, os
            cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ,'1234'))
        except:
            return None
        return cr
    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    if not cr:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)
        except:
            pass
    if not cr:
        try:
            cr = (env['LINES'], env['COLUMNS'])
        except:
            return None
    return int(cr[1]), int(cr[0])

if __name__ == "__main__":
    sizex,sizey=getTerminalSize()
    print ( 'width =',sizex,'height =',sizey)
