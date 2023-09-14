import os
from Page import Page

class Download(Page):
	def defaultAction(self):
		self._data = self._type = None
		self.writeHTML()
		if self._data and self._type:
			try:
				response = self.response()
				response.reset()
				response.setHeader('Content-Type', self._type)
				response.setHeader('Content-Disposition', 'attachment; filename="%s"' %self._file_save)
				response.write(self._data)
			except Exception:
				self.writeError('File cannot be viewed!')


	def writeContent(self):
		req = self.request()
		if req.hasField('filename'):
			filename = req.field('filename')
			file_save = req.field('file_save')
			self._file_save = file_save
			if not os.path.exists(filename):
				self.write('<p style="color:red">'
						   f'Datei nicht gefunden</p>')
				return
			self._type = req.field('content_type') 
			fx = open(filename, 'rb')
			self._data = fx.read()
			fx.close()
			# temporäre Datei entfernen
			if os.path.exists(filename):
				os.remove(filename) 
		else:
			self.writeln('<p>Datei-Download: Aufruf mit Download.py?filename=Dateiname/Pfad&file_save=Name der Datei&content_type=Content Type</p>')
