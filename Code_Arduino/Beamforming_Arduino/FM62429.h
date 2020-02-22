/*
* This file controls the FM62429 chips in the CharlesLabs SG PCB (12 channel 
* with M62429 for software amplitude control).
* 
* Author: CGrassin (http://charleslabs.fr)
* License: MIT
*/

#ifndef FM62429_H
#define FM62429_H

#include "A328_PINS.h"

#define FM62429_CLK_PIN (A3)
#define FM62429_MIN_ATT (10) // Min attenuation = -3dB. This is a more reasonnable max volume
#define FM62429_MAX_ATT (40) // Max attenuation = -83dB. This is the max attenuation for audible sound.


/* Private : builds a FM62429 control word. */
uint16_t __buildWord(uint8_t attenuation, uint8_t channel, uint8_t individual){
  //if (attenuation > 83) attenuation = 83;
  uint16_t data_word = 0x00;

  // Cap
  if (attenuation > FM62429_MAX_ATT) attenuation = FM62429_MAX_ATT;
  if (attenuation < FM62429_MIN_ATT) attenuation = FM62429_MIN_ATT;

  // Build control word (11 bits)
  data_word |= (channel    << 0);        // Channel select: 0=ch1, 1=ch2
  data_word |= (individual << 1);        // Individual/both select: 0=both, 1=individual
  data_word |= ((21 - (attenuation / 4)) << 2);  // ATT1: coarse attenuator, steps of -4dB
  data_word |= ((3 -  (attenuation % 4)) << 7);  // ATT2: fine attenuator, steps of -1dB)
  data_word |= (0b11 << 9);              // 2 last bits must be 1

  return data_word;
}

/* Private: sets 6 channels of FM62429 chips.
* WARNING: DOES NOT WORK PROPERLY FOR ATT BETWEEN 0 and 2 dB!!!!
* MIN ATT = 3 dB
*/
void __setFM62429(uint8_t att1, uint8_t att2, uint8_t att3, uint8_t att4, uint8_t att5, uint8_t att6,uint8_t channel){
  uint16_t data_word1 = __buildWord(att1,channel,1);
  uint16_t data_word2 = __buildWord(att2,channel,1);
  uint16_t data_word3 = __buildWord(att3,channel,1);
  uint16_t data_word4 = __buildWord(att4,channel,1);
  uint16_t data_word5 = __buildWord(att5,channel,1);
  uint16_t data_word6 = __buildWord(att6,channel,1);

  // Send control word
  for (uint8_t i = 0; i < 11; i++) {
    delayMicroseconds (2);
    _PIN_WRITE (_D2 , 0);
    _PIN_WRITE (_D4 , 0);
    _PIN_WRITE (_D6 , 0);
    _PIN_WRITE (_D8 , 0);
    _PIN_WRITE (_D10, 0);
    _PIN_WRITE (_D12, 0);
    delayMicroseconds (2);
    digitalWrite (FM62429_CLK_PIN, 0);
    delayMicroseconds (2);
    _PIN_WRITE (_D2 , (data_word1 >> i) & 0x01);
    _PIN_WRITE (_D4 , (data_word2 >> i) & 0x01);
    _PIN_WRITE (_D6 , (data_word3 >> i) & 0x01);
    _PIN_WRITE (_D8 , (data_word4 >> i) & 0x01);
    _PIN_WRITE (_D10, (data_word5 >> i) & 0x01);
    _PIN_WRITE (_D12, (data_word6 >> i) & 0x01);
    delayMicroseconds (2);
    digitalWrite (FM62429_CLK_PIN, 1);
  }
  delayMicroseconds (2);
  _PIN_WRITE (_D2 , 1);
  _PIN_WRITE (_D4 , 1);
  _PIN_WRITE (_D6 , 1);
  _PIN_WRITE (_D8 , 1);
  _PIN_WRITE (_D10, 1);
  _PIN_WRITE (_D12, 1);
  delayMicroseconds (2);
  digitalWrite (FM62429_CLK_PIN, 0);
}

/* Public : sets all 12 channels attenuation. */
void initFM62429(uint8_t att1, uint8_t att2, uint8_t att3, uint8_t att4,  uint8_t att5,  uint8_t att6,
                 uint8_t att7, uint8_t att8, uint8_t att9, uint8_t att10, uint8_t att11, uint8_t att12){
  pinMode(FM62429_CLK_PIN, OUTPUT);
  __setFM62429(att1,att3,att5,att7,att9, att11,0);
  __setFM62429(att2,att4,att6,att8,att10,att12,1);
}

#endif
