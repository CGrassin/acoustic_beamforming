#ifndef    A328_PINS_H
#define    A328_PINS_H

#include   "Arduino.h"

// LOGICAL PIN LOOK-UP TABLE
#define	   _BOGUS	_NAP, _NAP, _NAP, _NAP,  _NAP, _NAP, _NAP

#define	   _LB0		0x05, 0x04, 0x03, PORTB, DDRB, PINB, 0
#define	   _LB1		0x05, 0x04, 0x03, PORTB, DDRB, PINB, 1
#define	   _LB2		0x05, 0x04, 0x03, PORTB, DDRB, PINB, 2
#define	   _LB3		0x05, 0x04, 0x03, PORTB, DDRB, PINB, 3
#define	   _LB4		0x05, 0x04, 0x03, PORTB, DDRB, PINB, 4
#define	   _LB5		0x05, 0x04, 0x03, PORTB, DDRB, PINB, 5
#define	   _LB6		0x05, 0x04, 0x03, PORTB, DDRB, PINB, 6
#define	   _LB7		0x05, 0x04, 0x03, PORTB, DDRB, PINB, 7

#define	   _LC0		0x08, 0x07, 0x06, PORTC, DDRC, PINC, 0
#define	   _LC1		0x08, 0x07, 0x06, PORTC, DDRC, PINC, 1
#define	   _LC2		0x08, 0x07, 0x06, PORTC, DDRC, PINC, 2
#define	   _LC3		0x08, 0x07, 0x06, PORTC, DDRC, PINC, 3
#define	   _LC4		0x08, 0x07, 0x06, PORTC, DDRC, PINC, 4
#define	   _LC5		0x08, 0x07, 0x06, PORTC, DDRC, PINC, 5
#define	   _LC6		0x08, 0x07, 0x06, PORTC, DDRC, PINC, 6
#define	   _LC7		0x08, 0x07, 0x06, PORTC, DDRC, PINC, 7

#define	   _LD0		0x0b, 0x0a, 0x09, PORTD, DDRD, PIND, 0
#define	   _LD1		0x0b, 0x0a, 0x09, PORTD, DDRD, PIND, 1
#define	   _LD2		0x0b, 0x0a, 0x09, PORTD, DDRD, PIND, 2
#define	   _LD3		0x0b, 0x0a, 0x09, PORTD, DDRD, PIND, 3
#define	   _LD4		0x0b, 0x0a, 0x09, PORTD, DDRD, PIND, 4
#define	   _LD5		0x0b, 0x0a, 0x09, PORTD, DDRD, PIND, 5
#define	   _LD6		0x0b, 0x0a, 0x09, PORTD, DDRD, PIND, 6
#define	   _LD7		0x0b, 0x0a, 0x09, PORTD, DDRD, PIND, 7

// PHYSICAL TO LOGICAL PIN ALIASES (28 pin DIP)
#define    _P1		_LC6
#define    _P2		_LD0
#define    _P3		_LD1
#define    _P4		_LD2
#define    _P5		_LD3
#define    _P6		_LD4
#define    _P7		_BOGUS
#define    _P8		_BOGUS
#define    _P9		_LB6
#define    _P10		_LB7
#define    _P11		_LD5
#define    _P12		_LD6
#define    _P13		_LD7
#define    _P14		_LB0
#define    _P15		_LB1
#define    _P16		_LB2
#define    _P17		_LB3
#define    _P18		_LB4
#define    _P19		_LB5
#define    _P20		_BOGUS
#define    _P21		_BOGUS
#define    _P22		_BOGUS
#define    _P23		_LC0
#define    _P24		_LC1
#define    _P25		_LC2
#define    _P26		_LC3
#define    _P27		_LC4
#define    _P28		_LC5

// ARDUINO PIN TO PHYSICAL PIN ALIASES
#define	   _D0		_P2
#define	   _D1		_P3
#define	   _D2		_P4
#define	   _D3		_P5
#define	   _D4		_P6
#define	   _D5		_P11
#define	   _D6		_P12
#define	   _D7		_P13
#define	   _D8		_P14
#define	   _D9		_P15
#define	   _D10		_P16
#define	   _D11		_P17
#define	   _D12		_P18
#define	   _D13		_P19
#define	   _D14		_P23
#define	   _D15		_P24
#define	   _D16		_P25
#define	   _D17		_P26
#define	   _D18		_P27
#define	   _D19		_P28

// PIN ACCESS MACROS
#define __PIN_O( o, d, i, O, D, I, B    )  asm( "sbi " #d ", " #B )
#define __PIN_I( o, d, i, O, D, I, B    )  asm( "cbi " #d ", " #B )
#define __PIN_P( o, d, i, O, D, I, B    )  asm( "cbi " #d ", " #B ); \
				    	   asm( "sbi " #o ", " #B )
#define __PIN_R( o, d, i, O, D, I, B    )  (  ( I ) & ( _BV(B) ) )
#define __PIN_1( o, d, i, O, D, I, B    )  (  ( I ) & ( _BV(B) ) )
#define __PIN_0( o, d, i, O, D, I, B    )  ( ~( I ) & ( _BV(B) ) )
#define __PIN_W( o, d, i, O, D, I, B, V )  if (V) { asm("sbi " #o "," #B ); } \
					   else   { asm("cbi " #o "," #B ); }
#define __PIN_S( o, d, i, O, D, I, B    )  asm( "sbi " #o ", " #B )
#define __PIN_C( o, d, i, O, D, I, B    )  asm( "cbi " #o ", " #B )
#define __PIN_T( o, d, i, O, D, I, B    )  asm( "sbi " #i ", " #B )

// USER MACRO WRAPPERS AROUND PIN ACCESS MACROS
#define _PIN_CONFIG_OUT( P    )		__PIN_O( P    )
#define _PIN_CONFIG_IN(  P    )		__PIN_I( P    )
#define _PIN_CONFIG_INP( P    )		__PIN_P( P    )
#define _PIN_READ(       P    )		__PIN_R( P    )
#define _PIN_IS_1(       P    )		__PIN_1( P    )
#define _PIN_IS_0(       P    )		__PIN_0( P    )
#define _PIN_WRITE(      P, V )		__PIN_W( P, V )
#define _PIN_SET(        P    )		__PIN_S( P    )
#define _PIN_CLEAR(      P    )		__PIN_C( P    )
#define _PIN_TOGGLE(     P    )		__PIN_T( P    )

#endif
