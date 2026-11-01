# Makefile for Banker's Algorithm (C and C++)

CC = gcc
CXX = g++
CFLAGS = -Wall -Wextra -O2 -std=c99
CXXFLAGS = -Wall -Wextra -O2 -std=c++17

all: bankers_cpp bankers_c

bankers_cpp: bankers_algorithm.cpp
	$(CXX) $(CXXFLAGS) -o bankers_cpp bankers_algorithm.cpp

bankers_c: bankers_algorithm.c
	$(CC) $(CFLAGS) -o bankers_c bankers_algorithm.c

clean:
	rm -f bankers_cpp bankers_c *.o *.exe
