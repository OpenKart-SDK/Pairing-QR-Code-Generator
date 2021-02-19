import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtSvg import QSvgWidget, QSvgRenderer

from qrcodegen import QrCode, QrSegment
from bitarray import *
import argparse
import binascii


def convertEndian(value):
    if (len(value) % 2):
        value = "0" + str(value)
    length = int(len(value) / 2)
    string = ""
    for i in range(0, length):
        count = length - i - 1
        string += "" + value[count * 2:(count * 2) + 2]
    return string


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('-ssid')
  parser.add_argument('-seed')
  parser.add_argument('-ch')
  parser.add_argument('-hexseed')
  args = parser.parse_args()


  if (len(args.ssid) != 23):
    print("Error: SSID can't be shorter/longer than 23 characters.")
    exit()
  if (args.hexseed in ["True", "true"]):
    if (not ((len(args.seed)/2) == 16.0)):
      print("Error: Seed can't be shorter/longer than 32 hex digits.")
      exit()
  elif (len(args.seed) != 16):
      print("Error: Seed can't be shorter/longer than 16 characters.")
      exit()
  if (int(args.ch) not in [1, 6, 11]):
    print("Error: Channel can only be 1, 6, or 11")
    exit()
    
  if (args.hexseed in ["True", "true"]):
    data = args.seed.encode().decode()
  else:
    data = binascii.hexlify(args.seed.encode()).decode()


  data = data + binascii.hexlify(
      args.ssid.encode()).decode() + "000000000000000000" + convertEndian(args.ch) + "00" + "0000000000000000000000000"
  
  # Debug Info
  
  #print(data)
  #print("0" + "{0:8b}".format(int(data, 16)))
  #print(bytearray(bin(int(data, 16))[2:]), "binary")

  # Debug Info
  
  databits = bitarray("0" + "{0:8b}".format(int(data, 16)))
  segs = [QrSegment(QrSegment.Mode.BYTE, len(
      databits) // 8, databits)]
  qr = QrCode.encode_segments(segs, QrCode.Ecc.MEDIUM, 4, 4, -1, False)

  svg_bytes = bytearray(qr.to_svg_str(8), encoding='utf-8')


  app = QApplication(sys.argv)
  svgWidget = QSvgWidget()
  svgWidget.renderer().load(svg_bytes)
  svgWidget.setGeometry(100,100,300,300)
  svgWidget.show()
  sys.exit(app.exec_())
  

if __name__ == '__main__':
    main()
