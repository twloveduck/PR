#! /usr/bin/python

'''
Created: August 9 2016
Author: Tuck Williamson

Copyright© T.H.W LLC 2016
'''
DEBUG = False #True

import PIL
import photos
import PIL.Image, PIL.ImageChops
import io
import rater
import re 
import warnings
import pokemonData

if DEBUG:
  import PIL.ImageDraw
  
#google vision api use
import base64
import googleapiclient.discovery
import googleapiclient.errors

gapiURL = 'https://{api}.googleapis.com/$discovery/rest?version={apiVersion}'

gcvak = 'AIzaSyAd7e4JfbWOXBETPqNQAihsa68a6NXSavY'

visionSvc = googleapiclient.discovery.build('vision', 'v1', developerKey=gcvak, discoveryServiceUrl=gapiURL)

image_info = {
        '(750, 1334)':
                {
                        'regions':{
                                'star' : (650,80,710,140),
                                'cp': (200, 90, 550, 150),
                                'hp': (200, 710, 550, 740),
                                'xp': (68, 145, 682, 475),
                                'type': (20, 780, 370, 830),
                                'candy': (400, 960, 700, 1000),
                                'power': (380, 1050, 700, 1100),
                                'evolve': (500, 1150, 700, 1200)
                                },
                        'check': None,
                }
}

evolution_info = {
  'bulbasaur' : (1, 2, 3),
  'charmander' : (4, 5, 6),
  'squirtle' : (7, 8, 9),
  'caterpie' : (10, 11, 12),
  'weedle' : (13, 14, 15),
  'pidgey' : (16, 17, 18),
  'rattata' : (19, 20),
  'spearow' : (21, 22),
  'ekans' : (23, 24),
  'pikachu' : (25, 26),
  'sandshrew' : (27, 28),
  'nidoran♀' : (29, 30, 31),
  'nidoran♂' : (32, 33, 34),
  'clefairy' : (35, 36),
  'vulpix' : (37, 38),
  'jigglypuff' : (39, 40),
  'zubat' : (41, 42),
  'oddish' : (43, 44, 45),
  'paras' : (46, 47),
  'venonat' : (48, 49),
  'diglett' : (50, 51),
  'meowth' : (52, 53),
  'psyduck' : (54, 55),
  'mankey' : (56, 57),
  'growlithe' : (58, 59),
  'poliwag' : (60, 61, 62),
  'abra' : (63, 64, 65),
  'machop' : (66, 67, 68),
  'bellsprout' : (69, 70, 71),
  'tentacool' : (72, 73),
  'geodude' : (74, 75, 76),
  'ponyta' : (77, 78),
  'slowpoke' : (79,80),
  'magnemite' : (81, 82),
  "farfech'd" : (83),
  'duduo' : (84, 85),
  'seel' : (86, 87),
  'grimer' : (88, 89),
  'shellder' : (90, 91),
  'gastly' : (92, 93, 94),
  'onix' : (95),
  'drowzee' : (96, 97),
  'krabby' : (98, 99),
  'voltorb' : (100, 101),
  'exeggcute' : (102, 103),
  'cubone' : (104, 105),
  'hitmonlee' : (106),
  'hitmonchan' : (107),
  'lickitung' : (108),
  'koffing' : (109, 110),
  'rhyhorn' : (111, 112),
  'chansey' : (113),
  'tangela' : (114),
  'kangaskhan' : (115),
  'horsea' : (116, 117),
  'goldeen' : (118, 119),
  'staryu' : (120, 121),
  'mr. mime' : (122),
  'scyther' : (123),
  'jynx' : (124),
  'electabuzz' : (125),
  'magmar' : (126),
  'pinsir' : (127),
  'tauros' : (128),
  'magikarp' : (129, 130),
  'lapras' : (131),
  'ditto' : (132),
  'eevee' : (133, 134, 135, 136),
  'porygon' : (137),
  'omanyte' : (138, 139),
  'kabuto' : (140, 141),
  'aerodactyl' : (142),
  'snorlax' : (143),
  'articuno' : (144),
  'zapdos' : (145),
  'moltres' : (146),
  'dratini' : (147, 148, 149),
  'mewtwo' : (150),
  'mew' : (151),
}

'''This will contain a dictionary that is composed of the first 4 letters of each Pokémon and the 
indexes above in evolution_info.
'''
#evolution_info_4key = {}

def initialize():
  '''
  Setup the image_info dictionary.
  '''

  """
  #This just loads in the PIL library - there is some load magic that goes on and I didn't want to fully
  # delve into it.
  # TODO: Figure this out so that I can remove this cludge
  i = photos.get_screenshots_album().assets[-1]
  i.get_image()
  """

  for key in image_info.keys():
    image_info[key]['check'] = PIL.Image.open(key + '.bmp')

  '''
  for key in evolution_info.keys():
    key4 = key[:4]
    if key4 in evolution_info_4key.keys():
      evolution_info_4key.pop(key4, None)
      
    evolution_info_4key[key4] = evolution_info[key]
  '''  

def getImageRegion(image, region):
  img_key = str(image.size)
  if img_key in image_info.keys():
    img_info = image_info[img_key]
    if region.lower() in img_info['regions']:
      return image.crop(img_info['regions'][region])
    else:
      raise RuntimeError('Region %s unknown.' % (region))
  else:
    raise RuntimeError('Screenshot size not supported. Please report to the developer. TODO')

def checkIfPokemon(image):
  '''This checks to see if the image passed in looks like it is a screenshot from PG.

  returns:
  a PIL.Image
  '''
  img_size = str('(' + image.pixel_width + ', ' + image_pixel_height + ')')
  if img_size in image_info.keys():
    star_check = image_info[str(img_size)]['check']
  else:
    return (False, None)

  def filter(p):
    if p > 230:
      return 255
    else:
      return 0

  bw_star = getImageRegion(image, 'star').convert("L").point(filter)

  '''Now calculate the threshold for how much difference there can be - grab the count of white
  pixels for the check image, and allow a small fraction of those in the difference.
  '''
  maxDiff = int( star_check.histogram()[-1] * 0.1)

  tooDifferent = PIL.ImageChops.difference(star_check, bw_star).histogram()[-1] > maxDiff

  if DEBUG:
    star_check.show()
    bw_star.show()
    return [bw_star, star_check, tooDifferent]

  return tooDifferent

def getPGScreenShots():
  '''This method goes through all the screen shots and extracts those that it believes are from PG.

  returns: array of images that appear to be from PG
  '''

  rtn = []
  for ss_img in photos.get_screenshots_album().assets:
    img = ss_img.get_image()
    if checkIfPokemon(img):
      rtn.append(img)

  return rtn


def getTest(idx = -1):
  return photos.get_screenshots_album().assets[idx].get_image()

def whiteFilter(pixelVal):
  if pixelVal != 255:
    return 0
  else:
    return pixelVal

def nearWhiteFilter(pixelVal):
  if pixelVal < 250:
    return 0
  else:
    return 255

def nearBlackFilter(pixelVal):
  if pixelVal > 190:
    return 255
  else:
    return 0

ocrReMatches = {
  'type': re.compile('([a-zA-Z]+)'),
  'candy': re.compile('([a-zA-Z]+) CANDY'),
  'power': re.compile('(\d+)\D*(\d+)'),
  'hp' : re.compile('HP ?\d+.(\d+)'),
  'cp' : re.compile('CP(\d+)'),
  'evolve' : re.compile('.?(\d+)'),
}

def cleanOCRData(data):
  rtn = {}
  for key, data in data.items():
    if key in ('type', 'candy'):
      #pull the first two words out.
      rtn[key] = ocrReMatches[key].findall(data)
    elif key in ('cp', 'hp', 'evolve'):
      try:
        number = ocrReMatches[key].findall(data)[0]
        rtn[key] = int(number)
      except:
        rtn[key] = None
    elif key == 'power':
      try:
        pu_dust, pu_candy = ocrReMatches[key].findall(data)[0]
        rtn['dust'] = int(pu_dust)
        rtn['power'] = int(pu_candy)
      except:
        rtn['dust'] = None
        rtn['power'] = None
    else:
      rtn[key] = data
      
  return rtn
  
  
def getKeyImageAttributes(image):

  if not isinstance(image, PIL.Image.Image):
    image = image.get_image()

  if not str(image.size) in image_info.keys():
    return {}

  regionDict = image_info[str(image.size)]['regions']

  returnDict = {}
  regions = []

  #topNext = 0
  batch_request = []

  for region in regionDict.keys():
    regionImg = image.crop(regionDict[region])
    if region == 'cp':
      regionImg = PIL.ImageChops.invert(regionImg.convert('L').point(whiteFilter))
    elif region in ('xp', 'star'):
      continue
      #regionImg = regionImg.convert('L').point(nearWhiteFilter)

    elif region in ('power', 'candy', 'type', 'hp', 'evolve'):
      regionImg = regionImg.convert('L').point(nearBlackFilter)

    scanPic = PIL.Image.new('L', regionImg.size, 'white')
    scanPic.paste(regionImg, (0, 0))
    #topNext += regionImg.size[1] + 20

    outBytes = io.BytesIO()
    scanPic.save(outBytes, 'PNG')
    batch_request.append(({
            'image': {'content': base64.b64encode(outBytes.getvalue()).decode('UTF-8')},
            'features': [{'type': 'TEXT_DETECTION','maxResults': 10,}]}))
    outBytes.close()

    returnDict[region] = regionImg
    regions.append(region)
    
    if DEBUG:
      scanPic.show()

  request = visionSvc.images().annotate(body={'requests': batch_request})

  try:
    #return request
    responses = request.execute(num_retries=2)
    if 'responses' not in responses:
      print('No response from Google Vision API')
      return {}
    text_response = {}
    for region, response in zip(regions, responses['responses']):
      if 'error' in response:
        print("API Error for %s: %s" % (region,
        response['error']['message']
        if 'message' in response['error']
        else ''))
        continue
      if 'textAnnotations' in response:
        text_response[region] = response['textAnnotations'][0]['description']
      else:
        text_response[region] = None
      
    if DEBUG:
      print(text_response)
      
    return (cleanOCRData(text_response), returnDict)

  except errors.HttpError as e:
    #TODO propagate up
    print("Http Error for %s: %s" % (filename, e))
  except KeyError as e2:
    #TODO Propagate up
    print("Key error: %s" % e2)

  #return returnDict

def getPokemonLevel(trainer_level, xp_img):
  xp_img = getImageRegion(xp_img, 'xp')
  x,y = xp_img.size
  radius = (x/2)-5
  angles = rater.getPossibleArcPoints(trainer_level)
  
  '''have to reverse the angle list because the line is white up to the point
  so starting at the end where the line will be grey and proceeding backward
  we will know the angle as the first all white pixel. 
  '''

  img = xp_img.copy()
  drw = PIL.ImageDraw.Draw(img)
  
  coords = [rater.polarToCartesian(x/2, y-0, radius, ang + 1) for ang in reversed(angles)]
  level=1.5 + trainer_level
  for point in coords:
    if sum(xp_img.getpixel(point)) == 765:
      drw.rectangle((point, (point[0]+2,point[1]+2)), fill='red')
      if DEBUG:
        img.show()
      
      return (level, img)
      
    else:
      drw.rectangle((point, (point[0]+2,point[1]+2)), fill='yellow')
      
      level -= 0.5
  
  if DEBUG:
    img.show()
      
  return (None, img)
  
  
def getPokemonInformation(image, trainer_level):
  poke_info, region_images = getKeyImageAttributes(image)
  poke_level, level_img = getPokemonLevel(trainer_level, image)

  poke_info['level'] = poke_level
  region_images['level'] = level_img

  return (poke_info, region_images)
  
def testGCV(image_bytes):
  batch_request = [{
          'image': {'content': base64.b64encode(image_bytes).decode('UTF-8')
          },
          'features': [{'type': 'TEXT_DETECTION','maxResults': 100,}]}]

  request = visionSvc.images().annotate(body={'requests': batch_request})

  try:
    responses = request.execute(num_retries=2)
    if 'responses' not in responses:
      print('No response from Google Vision API')
      return {}
    text_response = []
    for response in responses['responses']:
      if 'error' in response:
        print("API Error: %s" % (response['error']['message']
        if 'message' in response['error']
        else ''))
        continue
      if 'textAnnotations' in response:
        text_response.append(response['textAnnotations'])
    return text_response
  except errors.HttpError as e:
    print("Http Error for %s: %s" % (filename, e))
  except KeyError as e2:
    print("Key error: %s" % e2)


if __name__ == '__main__':
  initialize()
  #d = getKeyImageAttributes(getTest(-1))

