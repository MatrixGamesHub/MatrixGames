import logging


class LogHandler(logging.Handler):
   """
   A logging handler that sends logs to an update function
   """

   def __init__(self, updateCallback):
       logging.Handler.__init__(self)

       self.level = logging.DEBUG
       self.terminator = ""
       self._updateCallback = updateCallback

   def emit(self, record):
       self._updateCallback(self.format(record))


class StreamToLogger():
   """
   Fake file-like stream object that redirects writes to a logger instance.
   """

   def __init__(self, logger, logLevel=logging.INFO):
      self._logger = logger
      self._logLevel = logLevel

   def write(self, buf):
       for line in buf.rstrip().splitlines():
           self._logger.log(self._logLevel, line.rstrip())
