#! /usr/bin/python

'''
Created: 
Author: Tuck Williamson

Copyright© T.H.W LLC 2016
'''

import appex
import photos
import testing
import dialogs
import Image
import ui
import io

class PokeInfoView(ui.View):
  
  def __init__(self):
    ui.load_view('pokemon.pyui')
    pass
    
  def doOkay(self, sender):
    self.close()
    
  def doCancel(self, sender):
    self.close()

def displayPokemon(data):
  '''This method displays a dialog for the user to confirm/edit the Pokémon info scanned.
  
  params:
    data - a tuple with dictionaries that have the parsed region information and the images where the data
      was parsed from.
      
  returns:
    A tuple of:
     None if user cancelled or the updated Pokémon data.
     The image regions where the data was parsed from.
  '''
  
  fields = []
  info, images = data
  
  for key in info.keys():
    field = {'type':'number', 'title': key, 'key':key}
    if info[key]:
      field['value'] = str(info[key])
    icon = images.get(key, None)
    if icon:
      outBytes = io.BytesIO()
      icon.save(outBytes, 'PNG')
      field['icon'] = ui.Image.from_data(outBytes.getvalue())
      
    fields.append(field)
  
  info = dialogs.form_dialog(title="Pokémon Information", fields=fields)
  
  return (info, images)
  
if __name__ == '__main__':
  
  piv = PokeInfoView()
  piv.present(hide_title_bar=True)
  piv.wait_modal()
  
  raise Exception('hi')
  
  images = []
  if appex.is_running_extension():
    images = appex.get_images()
  else:
    for i in (-1,-2,-3):
      images.append(photos.get_screenshots_album().assets[i])
  
  confirm_all = False
  user_level = 0
  dialog_rtn = dialogs.form_dialog(title="Enter Your Trainer Level", 
    sections=(
      ('Required', (
        {'type':'number', 'title':'Your Level*', 'key':'user_level'},),'*It is very important this is correct for the image otherwise Pokémon level may be wrong.'), 
      ('Options', (
        {'type':'switch', 'title':'Confirm each Pokémon scan', 'key': 'confirm_all', 'value':confirm_all},))
      ))
  
  if dialog_rtn:
    user_level = dialog_rtn['user_level']
    try:
      user_level = int(user_level)
      confirm_all = dialog_rtn['confirm_all']
    except:
      dialogs.alert('Error', 'The level you entered (%s) is not valid. Aborted.' % user_level, 'Okay', hide_cancel_button=True)
    if user_level < 1 or user_level > 40:
      dialogs.alert('Error', 'The level you entered (%s) is not valid in the valid range (1 - 40). Aborted.' % user_level, 'Okay', hide_cancel_button=True)
  else:
    print('User cancelled.')
    
  testing.initialize()
  
  for image in images:
    data = testing.getPokemonInformation(image.get_image(), user_level)
    if True:
      displayPokemon(data)
    
      

