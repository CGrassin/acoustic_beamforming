#!/bin/sh

javac $(find . -name "*.java") && java fr.charleslabs.beamforming.BeamformingCodeGenerator
