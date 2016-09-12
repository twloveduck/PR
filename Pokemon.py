import ui

class PokemonView(ui.View):
  def __init__(self):
    
    pass
    
  def did_load(self):
    self['ok_btn'].action = self.doOkay
    self['cancel_btn'].action = self.doCancel
    self['btnInfoPokeLevel'].action = self.doInfo_PokemonLevel
    
    print('loaded')
    
  def doOkay(self, sender):
    self.close()
    
  def doCancel(self, sender):
    self.close()
    
  def doInfo_PokemonLevel(self, sender):
    pass

t=ui.load_view()
t.present('sheet')
